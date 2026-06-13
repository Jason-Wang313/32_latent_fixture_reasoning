# Reproducibility Checklist

- [x] Main simulator and recovery script is `scripts/recover_paper32.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Main output is `docs/latent_fixture_results.csv`.
- [x] V2 outputs are `docs/unknown_fixture_stress.csv` and `docs/unknown_fixture_stress_table.tex`.
- [x] Paper source is `main.tex`.
- [x] Canonical PDF path is `C:/Users/wangz/Downloads/32.pdf`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] Visible Desktop PDF copies are absent.

Recommended verification commands:

```powershell
python scripts\recover_paper32.py --unknown-stress-only
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
```
