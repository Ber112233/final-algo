$ErrorActionPreference = 'Stop'

pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'Falló pdflatex para main.tex' }
bibtex main
if ($LASTEXITCODE -ne 0) { throw 'Falló bibtex para main.tex' }
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'Falló la segunda pasada de main.tex' }
pdflatex -interaction=nonstopmode -halt-on-error main.tex
if ($LASTEXITCODE -ne 0) { throw 'Falló la tercera pasada de main.tex' }

$journals = @(
    'Jose_Cisternas_bitacora.tex',
    'Gabriel_Olarte_bitacora.tex',
    'Bernardo_del_Aguila_bitacora.tex',
    'Wara_Murillo_bitacora.tex'
)
foreach ($journal in $journals) {
    pdflatex -interaction=nonstopmode -halt-on-error -output-directory=bitacoras (Join-Path 'bitacoras' $journal)
    if ($LASTEXITCODE -ne 0) { throw "Falló la compilación de $journal" }
}

New-Item -ItemType Directory -Path 'output/pdf' -Force | Out-Null
New-Item -ItemType Directory -Path 'entregables' -Force | Out-Null
Copy-Item -LiteralPath 'main.pdf' -Destination 'output/pdf/articulo.pdf' -Force
Copy-Item -LiteralPath 'main.pdf' -Destination 'entregables/articulo.pdf' -Force
foreach ($journal in $journals) {
    $pdfName = [System.IO.Path]::ChangeExtension($journal, '.pdf')
    Copy-Item -LiteralPath (Join-Path 'bitacoras' $pdfName) -Destination (Join-Path 'output/pdf' $pdfName) -Force
    Copy-Item -LiteralPath (Join-Path 'bitacoras' $pdfName) -Destination (Join-Path 'entregables' $pdfName) -Force
}

Write-Host 'Artículo y cuatro bitácoras compilados en output/pdf/ y entregables/.'
