# Submission Version Log

## v3 - 2026-06-15

- Added `docs/full_scale_execution_plan.md` before substantive v3 edits.
- Added `scripts/run_full_scale_fixture_suite.py`.
- Generated full-scale outputs under `results/full_scale/`:
  - `seed_metrics.csv`
  - `aggregate_metrics.csv`
  - `experiment_summary.json`
  - `representative_trace.csv`
  - manuscript table snippets
- Generated vector figures under `figures/full_scale/`.
- Rewrote `main.tex` as a 26-page v3 final full-scale manuscript.
- Added detailed sections on known fixtures, unknown fixtures, probe budgets, calibration, recovery after abstention, release-action menus, statistical robustness, reproducibility, limitations, and reviewer attacks.
- Built the final canonical PDF at `C:/Users/wangz/Downloads/32.pdf`.
- Verified the v3 final PDF hash before the later visual-hardening rebuild.
- Verified local `main.pdf` is absent after final build.

## v4 Visual Hardening - 2026-06-20

- Added the VLA role-model `hyperref` box policy to `main.tex`.
- Rebuilt the canonical Downloads PDF.
- Verified 26 pages, size 395,494 bytes, SHA256 `25EF23258F386553576BB28E4D12DB41A91852CB3D19E78B1A5480E4A33155EF`, and no local `main.pdf`.
- Verified one-point red internal link boxes on pages 4 and 5, with no cyan boxes. The manuscript has no cite/url link annotations, so green cite/url boxes are configured but not present.

## v2 - 2026-06-13

- Added out-of-taxonomy cable-tie stress generation to `scripts/recover_paper32.py`.
- Generated `docs/unknown_fixture_stress.csv`.
- Generated `docs/unknown_fixture_stress_table.tex`.
- Updated the manuscript with a visible v2 hardening note, stress table, narrowed abstract, and stronger limitations.
- Added `scripts/build_pdf.ps1` to build from `main.tex`, copy to Downloads, and remove local `main.pdf`.
- Removed stale Desktop-copy language from the audit status.

## v1 - 2026-06-11

- Recovered initial latent-fixture-reasoning paper package with literature sweep, deterministic toy benchmark, ICLR-style manuscript, final audit, canonical Downloads PDF, Desktop-copy status, and public GitHub repo.
