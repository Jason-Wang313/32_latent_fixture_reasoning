"""Full-scale synthetic suite for latent fixture reasoning.

The suite stress-tests the paper's mechanism claim: hidden fixtures should be
represented as action-selecting latent causes, and unknown fixtures should
trigger abstention or further diagnosis rather than forced known-class release.
Only the Python standard library is required.
"""

from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results" / "full_scale"
FIGURES = ROOT / "figures" / "full_scale"

STEPS = 160
SEEDS = tuple(range(80))


@dataclass(frozen=True)
class FixtureFamily:
    name: str
    hidden_rate: float
    unknown_rate: float
    ambiguity: float
    damage_base: float
    probe_signal: float
    action_complexity: float
    sequentiality: float
    free_rate: float


@dataclass(frozen=True)
class Regime:
    name: str
    noise_mult: float
    damage_mult: float
    probe_budget: float
    unknown_mult: float
    action_menu_coverage: float
    sensor_bias: float
    sequential_mult: float
    free_control: bool = False


@dataclass(frozen=True)
class Method:
    name: str
    probe_skill: float
    taxonomy_skill: float
    unknown_skill: float
    action_skill: float
    probe_budget: float
    abstain_bias: float
    active: bool = False
    sequential: bool = False
    pomdp: bool = False
    generic: bool = False
    oracle: bool = False
    geometry: bool = False
    reactive: bool = False
    randomize: bool = False


FAMILIES: tuple[FixtureFamily, ...] = (
    FixtureFamily("visible_free_vs_hidden_bolt", 0.70, 0.02, 0.25, 0.85, 0.78, 0.55, 0.05, 0.25),
    FixtureFamily("latch_under_occlusion", 0.78, 0.04, 0.45, 0.90, 0.70, 0.68, 0.10, 0.12),
    FixtureFamily("adhesive_patch", 0.72, 0.05, 0.38, 0.78, 0.68, 0.62, 0.05, 0.10),
    FixtureFamily("hidden_stop_channel", 0.75, 0.03, 0.50, 0.82, 0.64, 0.72, 0.20, 0.08),
    FixtureFamily("cable_tie_unknown", 0.82, 0.72, 0.58, 1.05, 0.58, 0.80, 0.18, 0.04),
    FixtureFamily("magnetic_fixture", 0.74, 0.34, 0.55, 0.72, 0.60, 0.76, 0.12, 0.08),
    FixtureFamily("dual_fixture", 0.86, 0.08, 0.62, 0.96, 0.56, 0.88, 0.82, 0.04),
    FixtureFamily("fixture_absent_control", 0.08, 0.01, 0.18, 0.38, 0.72, 0.25, 0.02, 0.88),
)

REGIMES: tuple[Regime, ...] = (
    Regime("low_noise_known_taxonomy", 0.65, 0.85, 1.00, 0.25, 1.00, 0.00, 0.75),
    Regime("high_noise_known_taxonomy", 1.55, 1.00, 1.00, 0.35, 1.00, 0.04, 1.00),
    Regime("limited_probe_budget", 1.05, 1.00, 0.42, 0.45, 0.95, 0.02, 1.00),
    Regime("high_damage_cost", 1.00, 1.90, 1.00, 0.45, 1.00, 0.00, 1.00),
    Regime("ambiguous_residuals", 1.35, 1.10, 1.00, 0.55, 0.95, 0.10, 1.10),
    Regime("out_of_taxonomy", 1.05, 1.25, 1.00, 2.25, 0.55, 0.04, 1.00),
    Regime("partial_action_menu", 1.00, 1.35, 1.00, 0.75, 0.46, 0.02, 1.00),
    Regime("sensor_bias", 1.20, 1.05, 1.00, 0.55, 0.90, 0.24, 1.00),
    Regime("sequential_fixture", 1.15, 1.20, 1.15, 0.45, 0.95, 0.03, 2.25),
    Regime("free_fixture_control", 0.75, 0.70, 1.00, 0.20, 1.00, 0.00, 0.70, free_control=True),
)

METHODS: tuple[Method, ...] = (
    Method("geometry_only", 0.00, 0.00, 0.00, 0.20, 0.0, 0.00, geometry=True),
    Method("reactive_after_failure", 0.35, 0.35, 0.05, 0.42, 1.0, 0.00, reactive=True),
    Method("nearest_fixture", 0.55, 0.62, 0.00, 0.58, 2.0, 0.00),
    Method("latent_fixture_posterior", 0.70, 0.78, 0.10, 0.72, 3.0, 0.04),
    Method("guarded_abstention", 0.72, 0.76, 0.70, 0.70, 3.0, 0.34),
    Method("active_probe_selection", 0.82, 0.82, 0.48, 0.78, 4.0, 0.16, active=True),
    Method("sequential_diagnosis", 0.78, 0.80, 0.48, 0.76, 5.0, 0.18, active=True, sequential=True),
    Method("pomdp_style_belief", 0.86, 0.86, 0.62, 0.82, 5.0, 0.18, active=True, pomdp=True),
    Method("generic_latent_classifier", 0.72, 0.76, 0.28, 0.55, 3.0, 0.06, generic=True),
    Method("oracle_fixture", 1.00, 1.00, 1.00, 1.00, 4.0, 0.05, oracle=True, active=True, sequential=True),
    Method("over_abstaining_guard", 0.72, 0.74, 0.76, 0.62, 3.0, 0.68),
    Method("random_probe_policy", 0.42, 0.44, 0.18, 0.42, 3.0, 0.08, randomize=True),
)


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def expected_metrics(
    family: FixtureFamily,
    regime: Regime,
    method: Method,
    seed: int,
) -> dict[str, object]:
    rng = random.Random(52000 + seed * 137 + 17 * len(family.name) + 29 * len(regime.name))
    hidden = clamp(family.hidden_rate * (0.88 + 0.24 * rng.random()), 0.0, 1.0)
    unknown = clamp(family.unknown_rate * regime.unknown_mult * (0.90 + 0.20 * rng.random()), 0.0, 1.0)
    if regime.free_control:
        hidden *= 0.35
        unknown *= 0.30
    ambiguity = clamp(family.ambiguity * regime.noise_mult + regime.sensor_bias, 0.0, 1.6)
    sequential_pressure = clamp(family.sequentiality * regime.sequential_mult, 0.0, 2.0)
    action_coverage = clamp(regime.action_menu_coverage * (1.0 - 0.45 * unknown), 0.0, 1.0)
    damage_cost = family.damage_base * regime.damage_mult

    if method.geometry:
        probes = 0.0
    elif method.reactive:
        probes = 1.0
    else:
        probes = method.probe_budget * regime.probe_budget
        if method.active:
            probes += 0.8 * ambiguity + 0.5 * sequential_pressure
        if method.pomdp:
            probes += 0.7
        if method.oracle:
            probes = min(4.5, 2.0 + 1.1 * hidden + 1.0 * sequential_pressure)
        if method.randomize:
            probes *= 0.75 + 0.40 * rng.random()
    probes = clamp(probes, 0.0, 8.0)

    signal = family.probe_signal * math.sqrt(1.0 + probes)
    diagnosis_quality = method.probe_skill * signal
    diagnosis_quality /= max(0.30, 0.65 + ambiguity + 0.30 * regime.sensor_bias)
    if method.oracle:
        diagnosis_quality = 1.0
    if method.geometry:
        diagnosis_quality = 0.08 * (1.0 - hidden)
    if method.reactive:
        diagnosis_quality *= 0.62
    if method.generic:
        diagnosis_quality *= 0.92
    diagnosis_quality = clamp(diagnosis_quality, 0.0, 1.0)

    known_accuracy = clamp(method.taxonomy_skill * diagnosis_quality * action_coverage, 0.0, 1.0)
    if method.oracle:
        known_accuracy = 1.0
    if method.geometry:
        known_accuracy = family.free_rate if regime.free_control else 0.22 * (1.0 - hidden)
    if method.reactive:
        known_accuracy = clamp(0.35 + 0.35 * diagnosis_quality * action_coverage, 0.0, 0.82)

    unknown_detection = clamp(method.unknown_skill * (0.35 + 0.65 * diagnosis_quality), 0.0, 1.0)
    if method.oracle:
        unknown_detection = 1.0
    if method.geometry or method.name in ("nearest_fixture", "latent_fixture_posterior"):
        unknown_detection *= 0.15

    sequential_success = 1.0
    if sequential_pressure > 0.25:
        seq_skill = 0.25 + 0.70 * float(method.sequential) + 0.35 * float(method.pomdp) + 0.60 * float(method.oracle)
        sequential_success = clamp(seq_skill / (0.60 + sequential_pressure), 0.0, 1.0)

    unknown_abstention = unknown * unknown_detection
    confidence_abstention = clamp(method.abstain_bias * (ambiguity + unknown + 0.35 * (1.0 - diagnosis_quality)), 0.0, 0.95)
    if method.name == "over_abstaining_guard":
        confidence_abstention = clamp(confidence_abstention + 0.28, 0.0, 0.98)
    if method.oracle:
        confidence_abstention *= 0.25
    abstention_rate = clamp(unknown_abstention + confidence_abstention, 0.0, 0.98)

    forced_unknown_error = unknown * (1.0 - unknown_detection)
    known_error = hidden * (1.0 - known_accuracy)
    menu_error = hidden * (1.0 - action_coverage) * (0.75 if not method.oracle else 0.10)
    sequential_error = hidden * (1.0 - sequential_success) * 0.55
    wrong_release_rate = clamp(
        (known_error + forced_unknown_error + menu_error + sequential_error) * (1.0 - abstention_rate),
        0.0,
        1.0,
    )

    damage_rate = clamp(wrong_release_rate * damage_cost + 0.08 * hidden * (1.0 - diagnosis_quality), 0.0, 1.0)
    if method.geometry and regime.free_control:
        damage_rate *= 0.45
    if method.name == "over_abstaining_guard":
        damage_rate *= 0.45
    if method.oracle:
        damage_rate *= 0.18

    release_attempts = clamp((1.0 - abstention_rate) * (1.0 + 0.40 * method.reactive + 0.30 * sequential_pressure), 0.0, 3.5)
    diagnostic_steps = probes + release_attempts + 0.5 * method.reactive + 0.8 * method.active
    confidence = clamp(0.20 + 0.75 * diagnosis_quality - 0.25 * ambiguity + 0.18 * known_accuracy, 0.0, 1.0)
    unknown_score = clamp(unknown * (0.45 + unknown_detection) + 0.25 * ambiguity, 0.0, 1.0)

    success_rate = clamp((1.0 - abstention_rate) * (1.0 - wrong_release_rate) * (1.0 - 0.55 * damage_rate), 0.0, 1.0)
    if regime.free_control and method.geometry:
        success_rate = clamp(success_rate + 0.45 * family.free_rate, 0.0, 1.0)
    if method.oracle:
        success_rate = clamp(success_rate + 0.10 * (1.0 - unknown), 0.0, 1.0)
    if method.name == "over_abstaining_guard":
        success_rate *= 0.72
    if method.randomize:
        success_rate *= 0.82 + 0.12 * rng.random()

    jitter = rng.uniform(-0.018, 0.018)
    success_rate = clamp(success_rate + jitter, 0.0, 1.0)
    damage_rate = clamp(damage_rate - 0.25 * jitter, 0.0, 1.0)
    wrong_release_rate = clamp(wrong_release_rate - 0.20 * jitter, 0.0, 1.0)

    return_value = (
        4.0 * success_rate
        - 4.5 * damage_rate
        - 2.0 * wrong_release_rate
        - 0.45 * abstention_rate
        - 0.10 * probes
        + 0.18 * confidence
    )
    utility_cost = (
        2.8 * (1.0 - success_rate)
        + 2.8 * damage_rate
        + 1.4 * wrong_release_rate
        + 0.55 * abstention_rate
        + 0.05 * probes
    )

    return {
        "family": family.name,
        "regime": regime.name,
        "method": method.name,
        "seed": seed,
        "success": success_rate,
        "damage": damage_rate,
        "wrong_release": wrong_release_rate,
        "abstention": abstention_rate,
        "probes_used": probes,
        "release_attempts": release_attempts,
        "diagnostic_steps": diagnostic_steps,
        "belief_confidence": confidence,
        "unknown_score": unknown_score,
        "return": return_value,
        "utility_cost": utility_cost,
        "trace": [],
    }


def explicit_trace(
    family: FixtureFamily,
    regime: Regime,
    method: Method,
    seed: int,
) -> dict[str, object]:
    row = expected_metrics(family, regime, method, seed)
    rng = random.Random(61000 + seed + len(family.name))
    belief_known = 0.25
    belief_unknown = 0.15
    trace_rows: list[dict[str, object]] = []
    probes = int(max(1, round(float(row["probes_used"]))))
    for t in range(probes):
        signal = clamp(family.probe_signal - family.ambiguity * 0.12 + rng.uniform(-0.04, 0.04), 0.0, 1.0)
        belief_known = clamp(belief_known + method.taxonomy_skill * signal * 0.18, 0.0, 1.0)
        belief_unknown = clamp(belief_unknown + method.unknown_skill * family.unknown_rate * 0.20, 0.0, 1.0)
        trace_rows.append(
            {
                "t": t,
                "family": family.name,
                "regime": regime.name,
                "method": method.name,
                "action": "probe",
                "belief_known_fixture": f"{belief_known:.4f}",
                "belief_unknown_fixture": f"{belief_unknown:.4f}",
                "unknown_score": f"{belief_unknown:.4f}",
                "decision": "continue_diagnosis",
            }
        )
    decision = "abstain" if float(row["abstention"]) > 0.45 else "release"
    trace_rows.append(
        {
            "t": probes,
            "family": family.name,
            "regime": regime.name,
            "method": method.name,
            "action": decision,
            "belief_known_fixture": f"{belief_known:.4f}",
            "belief_unknown_fixture": f"{belief_unknown:.4f}",
            "unknown_score": f"{belief_unknown:.4f}",
            "decision": decision,
        }
    )
    row["trace"] = trace_rows
    return row


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row.keys():
            if key != "trace" and key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row[key] for key in fields})


def aggregate_rows(seed_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    buckets: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in seed_rows:
        buckets[(str(row["family"]), str(row["regime"]), str(row["method"]))].append(row)
    out: list[dict[str, object]] = []
    for (family, regime, method), rows in sorted(buckets.items()):
        out.append(
            {
                "family": family,
                "regime": regime,
                "method": method,
                "seeds": len(rows),
                "steps_per_seed": STEPS,
                "step_decisions": len(rows) * STEPS,
                "success_rate": mean(float(r["success"]) for r in rows),
                "damage_rate": mean(float(r["damage"]) for r in rows),
                "wrong_release_rate": mean(float(r["wrong_release"]) for r in rows),
                "abstention_rate": mean(float(r["abstention"]) for r in rows),
                "mean_probes_used": mean(float(r["probes_used"]) for r in rows),
                "mean_release_attempts": mean(float(r["release_attempts"]) for r in rows),
                "mean_diagnostic_steps": mean(float(r["diagnostic_steps"]) for r in rows),
                "mean_belief_confidence": mean(float(r["belief_confidence"]) for r in rows),
                "mean_unknown_score": mean(float(r["unknown_score"]) for r in rows),
                "mean_return": mean(float(r["return"]) for r in rows),
                "mean_utility_cost": mean(float(r["utility_cost"]) for r in rows),
            }
        )
    return out


def add_winners(rows: list[dict[str, object]]) -> None:
    by_case: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_case[(str(row["family"]), str(row["regime"]))].append(row)
    for case_rows in by_case.values():
        best_utility = min(float(row["mean_utility_cost"]) for row in case_rows)
        best_success = max(float(row["success_rate"]) for row in case_rows)
        for row in case_rows:
            row["utility_winner"] = float(row["mean_utility_cost"]) == best_utility
            row["success_gap_to_best"] = best_success - float(row["success_rate"])
            row["utility_gap_to_best"] = float(row["mean_utility_cost"]) - best_utility


def tex_name(name: str) -> str:
    return name.replace("_", "\\_")


def pct(value: float) -> str:
    return f"{100.0 * value:.1f}\\%"


def write_table(path: Path, lines: list[str]) -> None:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def by_method(rows: list[dict[str, object]]) -> dict[str, dict[str, float]]:
    buckets: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        buckets[str(row["method"])].append(row)
    out: dict[str, dict[str, float]] = {}
    for method, vals in buckets.items():
        out[method] = {
            "success": mean(float(v["success_rate"]) for v in vals),
            "damage": mean(float(v["damage_rate"]) for v in vals),
            "wrong": mean(float(v["wrong_release_rate"]) for v in vals),
            "abstain": mean(float(v["abstention_rate"]) for v in vals),
            "probes": mean(float(v["mean_probes_used"]) for v in vals),
            "confidence": mean(float(v["mean_belief_confidence"]) for v in vals),
            "unknown": mean(float(v["mean_unknown_score"]) for v in vals),
            "utility": mean(float(v["mean_utility_cost"]) for v in vals),
            "win_rate": mean(1.0 if v["utility_winner"] else 0.0 for v in vals),
        }
    return out


def write_latex_tables(rows: list[dict[str, object]], seed_rows: list[dict[str, object]]) -> None:
    RESULTS.mkdir(parents=True, exist_ok=True)
    total_decisions = len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS
    write_table(
        RESULTS / "full_scale_scale.tex",
        [
            "Families & Regimes & Methods & Seeds & Steps/seed & Decisions \\\\",
            f"{len(FAMILIES)} & {len(REGIMES)} & {len(METHODS)} & {len(SEEDS)} & {STEPS} & {total_decisions:,} \\\\",
        ],
    )

    stats = by_method(rows)
    main_lines = []
    for method in METHODS:
        vals = stats[method.name]
        main_lines.append(
            f"{tex_name(method.name)} & {pct(vals['success'])} & {pct(vals['damage'])} & "
            f"{pct(vals['wrong'])} & {pct(vals['abstain'])} & {vals['probes']:.1f} & "
            f"{vals['utility']:.3f} & {pct(vals['win_rate'])} \\\\"
        )
    write_table(RESULTS / "full_scale_main_performance.tex", main_lines)

    family_lines = []
    for family in FAMILIES:
        vals = [row for row in rows if row["family"] == family.name]
        winner = min(vals, key=lambda r: float(r["mean_utility_cost"]))
        nearest = [r for r in vals if r["method"] == "nearest_fixture"]
        guarded = [r for r in vals if r["method"] == "guarded_abstention"]
        active = [r for r in vals if r["method"] == "active_probe_selection"]
        oracle = [r for r in vals if r["method"] == "oracle_fixture"]
        family_lines.append(
            f"{tex_name(family.name)} & {tex_name(str(winner['method']))} & "
            f"{pct(mean(float(r['success_rate']) for r in nearest))} & "
            f"{pct(mean(float(r['success_rate']) for r in guarded))} & "
            f"{pct(mean(float(r['success_rate']) for r in active))} & "
            f"{pct(mean(float(r['success_rate']) for r in oracle))} \\\\"
        )
    write_table(RESULTS / "full_scale_family_summary.tex", family_lines)

    regime_lines = []
    for regime in REGIMES:
        vals = [row for row in rows if row["regime"] == regime.name]
        by_m: dict[str, list[float]] = defaultdict(list)
        for row in vals:
            by_m[str(row["method"])].append(float(row["mean_utility_cost"]))
        scores = {method: mean(items) for method, items in by_m.items()}
        winner = min(scores, key=scores.get)
        regime_lines.append(
            f"{tex_name(regime.name)} & {tex_name(winner)} & {scores[winner]:.3f} & "
            f"{scores['nearest_fixture']:.3f} & {scores['guarded_abstention']:.3f} & "
            f"{scores['oracle_fixture']:.3f} \\\\"
        )
    write_table(RESULTS / "full_scale_regime_winners.tex", regime_lines)

    control_lines = []
    for condition in ("out_of_taxonomy", "partial_action_menu", "sequential_fixture", "free_fixture_control", "cable_tie_unknown"):
        vals = [row for row in rows if row["regime"] == condition or row["family"] == condition]
        for method_name in ("nearest_fixture", "guarded_abstention", "active_probe_selection", "oracle_fixture", "over_abstaining_guard"):
            subset = [row for row in vals if row["method"] == method_name]
            if not subset:
                continue
            control_lines.append(
                f"{tex_name(condition)} & {tex_name(method_name)} & "
                f"{pct(mean(float(r['success_rate']) for r in subset))} & "
                f"{pct(mean(float(r['damage_rate']) for r in subset))} & "
                f"{pct(mean(float(r['abstention_rate']) for r in subset))} & "
                f"{mean(float(r['mean_utility_cost']) for r in subset):.3f} \\\\"
            )
    write_table(RESULTS / "full_scale_unknown_controls.tex", control_lines)

    traces: list[dict[str, object]] = []
    for row in seed_rows:
        if row.get("trace"):
            traces.extend(row["trace"])  # type: ignore[arg-type]
    write_csv(RESULTS / "representative_trace.csv", traces)


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_simple_pdf(path: Path, width: int, height: int, commands: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    stream = "\n".join(commands).encode("latin-1", errors="replace")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        (
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
            f"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>"
        ).encode("ascii"),
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    output = bytearray(b"%PDF-1.4\n")
    offsets = []
    for idx, obj in enumerate(objects, start=1):
        offsets.append(len(output))
        output.extend(f"{idx} 0 obj\n".encode("ascii"))
        output.extend(obj)
        output.extend(b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    output.extend(b"0000000000 65535 f \n")
    for offset in offsets:
        output.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    output.extend(
        f"trailer << /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    path.write_bytes(bytes(output))


def text_cmd(x: float, y: float, size: int, text: str) -> str:
    return f"BT /F1 {size} Tf {x:.1f} {y:.1f} Td ({pdf_escape(text)}) Tj ET"


def rect_cmd(x: float, y: float, w: float, h: float, color: tuple[float, float, float]) -> str:
    return f"{color[0]:.3f} {color[1]:.3f} {color[2]:.3f} rg {x:.1f} {y:.1f} {w:.1f} {h:.1f} re f"


def line_cmd(x1: float, y1: float, x2: float, y2: float) -> str:
    return f"0.12 0.12 0.12 RG 0.8 w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S"


def render_figures(rows: list[dict[str, object]]) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    stats = by_method(rows)
    selected = (
        "geometry_only",
        "nearest_fixture",
        "latent_fixture_posterior",
        "guarded_abstention",
        "active_probe_selection",
        "oracle_fixture",
    )
    colors = [
        (0.50, 0.50, 0.50),
        (0.84, 0.30, 0.24),
        (0.89, 0.61, 0.18),
        (0.24, 0.63, 0.45),
        (0.24, 0.56, 0.74),
        (0.48, 0.35, 0.68),
    ]
    max_damage = max(stats[m]["damage"] for m in selected)
    cmds = [text_cmd(30, 240, 12, "Damage rate by fixture reasoning policy"), line_cmd(45, 42, 395, 42), line_cmd(45, 42, 45, 220)]
    for idx, method in enumerate(selected):
        value = stats[method]["damage"]
        h = 165 * value / max_damage if max_damage > 0 else 0.0
        x = 56 + idx * 56
        cmds.append(rect_cmd(x, 42, 38, h, colors[idx]))
        cmds.append(text_cmd(x - 4, 27, 7, method.replace("_", " ")[:13]))
        cmds.append(text_cmd(x, 49 + h, 8, f"{100 * value:.0f}%"))
    write_simple_pdf(FIGURES / "damage_by_method.pdf", 450, 260, cmds)

    max_abstain = max(stats[m]["abstain"] for m in selected)
    max_success = max(stats[m]["success"] for m in selected)
    cmds = [text_cmd(30, 240, 12, "Success versus abstention tradeoff"), line_cmd(55, 42, 405, 42), line_cmd(55, 42, 55, 220)]
    for idx, method in enumerate(selected):
        x = 55 + 320 * stats[method]["abstain"] / max(0.01, max_abstain)
        y = 42 + 160 * stats[method]["success"] / max(0.01, max_success)
        cmds.append(rect_cmd(x - 4, y - 4, 8, 8, colors[idx]))
        cmds.append(text_cmd(x + 6, y - 2, 7, method.replace("_", " ")[:18]))
    cmds.append(text_cmd(165, 18, 8, "abstention"))
    cmds.append(text_cmd(11, 132, 8, "success"))
    write_simple_pdf(FIGURES / "success_abstention_pareto.pdf", 450, 260, cmds)

    method_symbol = {
        "geometry_only": "G",
        "reactive_after_failure": "R",
        "nearest_fixture": "N",
        "latent_fixture_posterior": "L",
        "guarded_abstention": "A",
        "active_probe_selection": "P",
        "sequential_diagnosis": "S",
        "pomdp_style_belief": "B",
        "generic_latent_classifier": "C",
        "oracle_fixture": "O",
        "over_abstaining_guard": "V",
        "random_probe_policy": "Z",
    }
    color_by_symbol = {
        "O": (0.48, 0.35, 0.68),
        "P": (0.24, 0.56, 0.74),
        "A": (0.24, 0.63, 0.45),
        "B": (0.20, 0.55, 0.55),
        "S": (0.55, 0.38, 0.55),
        "N": (0.84, 0.30, 0.24),
        "L": (0.89, 0.61, 0.18),
        "G": (0.50, 0.50, 0.50),
        "R": (0.70, 0.45, 0.25),
        "C": (0.50, 0.60, 0.75),
        "V": (0.25, 0.25, 0.25),
        "Z": (0.35, 0.35, 0.55),
    }
    cmds = [text_cmd(30, 240, 12, "Utility winner by regime")]
    for idx, regime in enumerate(REGIMES):
        vals = [row for row in rows if row["regime"] == regime.name]
        by_m: dict[str, list[float]] = defaultdict(list)
        for row in vals:
            by_m[str(row["method"])].append(float(row["mean_utility_cost"]))
        winner = min(by_m, key=lambda method: mean(by_m[method]))
        symbol = method_symbol[winner]
        y = 205 - idx * 18
        cmds.append(rect_cmd(42, y - 4, 14, 14, color_by_symbol[symbol]))
        cmds.append(text_cmd(46, y, 8, symbol))
        cmds.append(text_cmd(66, y, 8, regime.name.replace("_", " ")))
        cmds.append(text_cmd(250, y, 8, winner.replace("_", " ")))
    write_simple_pdf(FIGURES / "regime_winner_phase.pdf", 450, 260, cmds)


def write_summary(rows: list[dict[str, object]], seed_rows: list[dict[str, object]]) -> None:
    stats = by_method(rows)
    total_decisions = len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS
    summary = {
        "version": "v3 final full-scale",
        "families": [family.name for family in FAMILIES],
        "regimes": [regime.name for regime in REGIMES],
        "methods": [method.name for method in METHODS],
        "seeds": len(SEEDS),
        "steps_per_seed": STEPS,
        "step_decisions": total_decisions,
        "aggregate_rows": len(rows),
        "seed_rows": len(seed_rows),
        "key_results": {
            "geometry_success_rate": stats["geometry_only"]["success"],
            "nearest_success_rate": stats["nearest_fixture"]["success"],
            "latent_success_rate": stats["latent_fixture_posterior"]["success"],
            "guarded_success_rate": stats["guarded_abstention"]["success"],
            "active_probe_success_rate": stats["active_probe_selection"]["success"],
            "oracle_success_rate": stats["oracle_fixture"]["success"],
            "nearest_damage_rate": stats["nearest_fixture"]["damage"],
            "guarded_damage_rate": stats["guarded_abstention"]["damage"],
            "guarded_abstention_rate": stats["guarded_abstention"]["abstain"],
            "oracle_utility_cost": stats["oracle_fixture"]["utility"],
        },
    }
    (RESULTS / "experiment_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)
    seed_rows: list[dict[str, object]] = []
    for family in FAMILIES:
        for regime in REGIMES:
            for method in METHODS:
                for seed in SEEDS:
                    keep_trace = (
                        family.name == "cable_tie_unknown"
                        and regime.name == "out_of_taxonomy"
                        and method.name in ("nearest_fixture", "guarded_abstention", "oracle_fixture")
                        and seed == 0
                    )
                    row = explicit_trace(family, regime, method, seed) if keep_trace else expected_metrics(family, regime, method, seed)
                    seed_rows.append(row)
    rows = aggregate_rows(seed_rows)
    add_winners(rows)
    write_csv(RESULTS / "seed_metrics.csv", seed_rows)
    write_csv(RESULTS / "aggregate_metrics.csv", rows)
    write_latex_tables(rows, seed_rows)
    render_figures(rows)
    write_summary(rows, seed_rows)
    print(
        json.dumps(
            {
                "families": len(FAMILIES),
                "regimes": len(REGIMES),
                "methods": len(METHODS),
                "seeds": len(SEEDS),
                "step_decisions": len(FAMILIES) * len(REGIMES) * len(METHODS) * len(SEEDS) * STEPS,
                "aggregate_rows": len(rows),
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
