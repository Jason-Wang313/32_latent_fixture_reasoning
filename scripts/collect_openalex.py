import csv
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import requests


ROOT = Path(r"C:\Users\wangz\robotics_60_paper_batch\32_latent_fixture_reasoning")
DOCS = ROOT / "docs"
OUT = DOCS / "related_work_matrix.csv"
STATE = ROOT / "docs" / "openalex_state.json"


QUERIES = [
    "robot manipulation physical reasoning support relations",
    "robot fixture reasoning manipulation",
    "robot hidden support inference manipulation",
    "robot object affordance support relation",
    "robot contact-rich manipulation physical reasoning",
    "robot planning object relationships manipulation",
    "robot scene graph manipulation support",
    "robot causal reasoning manipulation physics",
    "robot tactile physical reasoning manipulation",
    "robot articulated object manipulation reasoning",
    "robot household manipulation support surfaces",
    "robot assembly support fixture manipulation",
    "robot long-horizon manipulation world model",
    "robot latent world model manipulation physical",
    "robot embodied physical reasoning benchmark manipulation",
]


def get_abstract(inv):
    if not inv:
        return ""
    return " ".join(inv.get(k, "") for k in sorted(inv))


def search_query(query, cursor="*"):
    url = "https://api.openalex.org/works"
    params = {
        "search": query,
        "per-page": 200,
        "cursor": cursor,
        "select": "id,doi,display_name,publication_year,publication_date,host_venue,authorships,cited_by_count,abstract_inverted_index,type",
    }
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text(encoding="utf-8"))
    return {"query_state": {}, "seen": {}}


def save_state(state):
    STATE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def main():
    DOCS.mkdir(exist_ok=True)
    state = load_state()
    seen = state.setdefault("seen", {})
    rows = []
    for q in QUERIES:
        cursor = state.setdefault("query_state", {}).get(q, "*")
        for _ in range(5):
            data = search_query(q, cursor)
            for w in data.get("results", []):
                wid = w.get("id") or ""
                if not wid or wid in seen:
                    continue
                seen[wid] = True
                hv = w.get("host_venue") or {}
                rows.append({
                    "openalex_id": wid,
                    "title": (w.get("display_name") or "").replace("\n", " ").strip(),
                    "year": w.get("publication_year") or "",
                    "date": w.get("publication_date") or "",
                    "venue": hv.get("display_name") or "",
                    "doi": w.get("doi") or "",
                    "cited_by_count": w.get("cited_by_count") or 0,
                    "type": w.get("type") or "",
                    "query_seed": q,
                })
            cursor = data.get("meta", {}).get("next_cursor")
            state["query_state"][q] = cursor
            save_state(state)
            if not data.get("results"):
                break
            time.sleep(0.2)

    rows.sort(key=lambda r: (-int(r["cited_by_count"]), str(r["year"]), r["title"]))
    existing = []
    if OUT.exists():
        with OUT.open("r", encoding="utf-8", newline="") as f:
            existing = list(csv.DictReader(f))
    merged = {r["openalex_id"]: r for r in existing}
    for r in rows:
        merged[r["openalex_id"]] = r
    final_rows = list(merged.values())
    final_rows.sort(key=lambda r: (-int(r.get("cited_by_count", 0) or 0), str(r.get("year", "")), r.get("title", "")))
    with OUT.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["openalex_id", "title", "year", "date", "venue", "doi", "cited_by_count", "type", "query_seed"])
        writer.writeheader()
        writer.writerows(final_rows)
    print(f"wrote {len(final_rows)} rows to {OUT}")


if __name__ == "__main__":
    main()
