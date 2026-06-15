# Child Status 32

Status: v3 final full-scale submission-hardened
Original child attempts: 2
Original failure cause: OpenAlex HTTP 429 during literature collection; no PDF was produced by child attempts.

Recovery end time: 2026-06-11 23:15:00 +01:00
V2 hardening time: 2026-06-13 06:37:49 +01:00
V3 full-scale hardening time: 2026-06-15

## Final Actions

- Wrote `docs/full_scale_execution_plan.md` before substantive v3 edits.
- Added `scripts/run_full_scale_fixture_suite.py`.
- Ran the full-scale suite: 8 families, 10 regimes, 12 methods, 80 seeds, and 12,288,000 represented decisions.
- Generated seed metrics, aggregate metrics, summary JSON, representative trace, table snippets, and vector figures under `results/full_scale/` and `figures/full_scale/`.
- Rewrote `main.tex` as a v3 final full-scale manuscript with explicit unknown-fixture, partial-action-menu, sequential-fixture, free-control, calibration, safety, and reviewer-attack sections.
- Compiled with the canonical build script and copied only the final PDF to `C:/Users/wangz/Downloads/32.pdf`.
- Removed local `main.pdf` after the canonical copy.
- Verified final PDF text contains `v3 final full-scale`, `12,288,000`, `33.3`, and `93.1`.
- Verified serious build-log scan has no overfull boxes, unresolved references, undefined citations, fatal errors, or TeX error lines.

## Final PDF

- Downloads PDF: `C:/Users/wangz/Downloads/32.pdf`
- Pages: 26
- Size: 338,643 bytes
- SHA256: `966FB6334A0CD0CD0EF568AA65D7C6E2B8B17F8C08C44AAC8B1936B326D2454C`
- Desktop PDF: absent
- Local paper PDF: absent after final build
- GitHub URL: `https://github.com/Jason-Wang313/32_latent_fixture_reasoning`
