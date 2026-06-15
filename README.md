# Latent Fixture Reasoning

Paper 32 final v3 artifact for the robotics 60 batch.

- Thesis: robots should infer hidden fixtures and supports from manipulation outcomes, not only from visible geometry.
- Main manuscript: `main.tex`
- Canonical PDF: `C:/Users/wangz/Downloads/32.pdf`
- Final PDF pages: 26
- Final PDF SHA256: `966FB6334A0CD0CD0EF568AA65D7C6E2B8B17F8C08C44AAC8B1936B326D2454C`
- Build command: `powershell -ExecutionPolicy Bypass -File scripts/build_pdf.ps1`
- Full-scale runner: `python scripts/run_full_scale_fixture_suite.py`
- Full-scale outputs: `results/full_scale/`
- Figures: `figures/full_scale/`

## v3 Evidence

The v3 manuscript replaces the compact v2 mechanism artifact with a full-scale
synthetic suite covering 8 fixture families, 10 regimes, 12 policies, 80
deterministic seeds, and 12,288,000 represented fixture-reasoning decisions.

Key aggregate results:

- Geometry-only: 24.0% success, 68.9% damage.
- Nearest known fixture: 31.6% success, 60.6% damage.
- Guarded abstention: 44.0% success, 33.3% damage, 28.1% abstention.
- Active probe selection: 51.6% success.
- Oracle fixture knowledge: 93.1% success, 0.3% damage.

## Boundary

This is a final full-scale synthetic mechanism paper, not a hardware validation
paper. The claim is intentionally bounded: latent fixture variables are useful
action-selecting state abstractions when taxonomy coverage, unknown detection,
safe probes, and release-action menus are calibrated and reported honestly.
