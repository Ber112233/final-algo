# Hashing dinámico: experimento reproducible

Proyecto final de Algorítmica II de José Cisternas, Gabriel Olarte, Bernardo del Aguila y Wara Murillo.

> ¿Cómo influyen el factor de redimensionamiento y el umbral de carga en el costo amortizado, el consumo de memoria y el número esperado de colisiones de una tabla hash dinámica con hashing universal?

La implementación principal usa encadenamiento separado. El sondeo lineal adaptado de la rama `gabo` es únicamente un contraste secundario: sus colisiones son probes y no se mezclan con los pares que coinciden en un bucket.

## Estructura

- `src/`: estructuras, hashing, generadores y métricas.
- `experiments/`: factorial principal y experimentos secundarios.
- `analysis/`: resumen bootstrap y ocho figuras del protocolo.
- `data/raw/`: datos crudos y eventos de resize.
- `data/processed/`: resúmenes derivados.
- `results/`: corrida preliminar anterior, conservada por trazabilidad.
- `figuras/pilot/` y `figuras/final/`: figuras del piloto y corrida final.
- `tests/`: pruebas de invariantes y reproducibilidad.
- `anexos/` y `bitacoras/`: material LaTeX obligatorio.

## Instalación y validación

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

## Reproducción

```powershell
# Piloto: 200 corridas
python main.py experiment --repetitions 5 --max-n 10000 --overwrite

# Factorial final: 1800 corridas
python main.py experiment --repetitions 30 --max-n 100000 --overwrite
python main.py analyze
python main.py plot
```

La matriz usa cinco valores de `gamma`, cuatro de `tau`, tres tamaños y 30 semillas. Dentro de cada bloque se conservan conjunto y orden de claves, mientras el orden de los 20 tratamientos se aleatoriza. El CSV registra commit, entorno, semillas separadas, contadores deterministas, memoria estructural y pico de `tracemalloc`.

Experimentos complementarios:

```powershell
python main.py threshold-experiment --overwrite
python main.py collision-experiment --repetitions 30 --overwrite
python -c "from experiments.linear_probing_experiment import run_secondary; run_secondary(overwrite=True)"
```

## Convenciones

- Capacidad inicial prima `m0=11`.
- Crecimiento antes de insertar si `(n+1)/m > tau`.
- Nueva capacidad `next_prime(ceil(gamma*m))` y nuevo `(a,b)` por rehash.
- `insert_collision_events` y `pair_collisions` son métricas diferentes.
- Amortizado, esperado y promedio empírico no se intercambian.
- Los componentes de costo se publican por separado, sin pesos arbitrarios ocultos.

## Compilación

```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

Las bitácoras se compilan individualmente desde `bitacoras/`. Todo borrador asistido por IA debe ser revisado por el estudiante correspondiente antes de entregar.
