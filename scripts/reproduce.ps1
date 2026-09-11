$ErrorActionPreference = 'Stop'

python -m pip install -r requirements.txt
python -m pytest -q
python main.py experiment --repetitions 30 --max-n 100000 --overwrite
python analysis/validate_results.py
python main.py analyze
python main.py plot
python analysis/export_latex.py

pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex

Copy-Item -LiteralPath 'main.pdf' -Destination 'articulo.pdf' -Force

Write-Host 'Reproducción completa: datos, figuras y articulo.pdf generados.'
