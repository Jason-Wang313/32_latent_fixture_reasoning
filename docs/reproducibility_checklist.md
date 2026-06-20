# Reproducibility Checklist

- [x] Full-scale runner is `scripts/run_full_scale_fixture_suite.py`.
- [x] Legacy v2 recovery/stress script remains `scripts/recover_paper32.py`.
- [x] Build script is `scripts/build_pdf.ps1`.
- [x] Main paper source is `main.tex`.
- [x] Full-scale output directory is `results/full_scale/`.
- [x] Figure directory is `figures/full_scale/`.
- [x] Final PDF path is `C:/Users/wangz/Downloads/32.pdf`.
- [x] Final PDF has 26 pages.
- [x] Final PDF SHA256 is `25EF23258F386553576BB28E4D12DB41A91852CB3D19E78B1A5480E4A33155EF`.
- [x] Local `main.pdf` is removed after canonical copy.
- [x] Visible Desktop PDF copies are absent.
- [x] Build status is written locally to ignored `data/build_status.json`.
- [x] Stable validation facts are recorded in `results/full_scale/validation.json`.
- [x] VLA-style link-box policy is configured in `main.tex`; final PDF has one-point red internal reference boxes and no cyan boxes.

Recommended verification commands:

```powershell
python scripts\run_full_scale_fixture_suite.py
powershell -ExecutionPolicy Bypass -File scripts\build_pdf.ps1
pdfinfo C:\Users\wangz\Downloads\32.pdf
Get-FileHash -Algorithm SHA256 C:\Users\wangz\Downloads\32.pdf
pdftotext C:\Users\wangz\Downloads\32.pdf - | Select-String -Pattern 'v3 final full-scale|12,288,000|33.3|93.1'
Select-String -Path build_pdflatex2.log -Pattern 'Overfull|LaTeX Warning: Reference|undefined citations|There were undefined|Fatal error|^!'
```
