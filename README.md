# Implementación Experimental de una Tabla Hash Dinámica

Trabajo Final de Investigación Científica de **Algorítmica II**. El proyecto implementa desde cero una tabla hash para claves enteras y una infraestructura reproducible para estudiar:

> ¿Cómo afectan el factor de redimensionamiento y el umbral de carga de una tabla hash dinámica al costo amortizado, la memoria utilizada y el número esperado de colisiones?

La hipótesis inicial plantea un compromiso entre frecuencia de resize, colisiones y memoria. El código no impone esa conclusión: los CSV y las gráficas se usan para evaluarla.

## Diseño

- **Separate chaining:** cada posición es una lista (bucket).
- **Colisión:** una clave nueva llega a un bucket con al menos otra clave. Los duplicados rechazados y las reinserciones internas no suman colisiones.
- **Hashing universal:** `h(x) = ((a*x+b) mod p) mod m`, con `a` y `b` obtenidos de `random.Random(seed)`.
- **Primo:** `p = 2^61 - 1 = 2305843009213693951`, suficientemente grande para el universo previsto.
- **Resize:** ocurre cuando `size/capacity > load_threshold`; la capacidad nueva es `max(old+1, ceil(old*growth_factor))`.
- **Rehash:** usa un método interno; no incrementa inserciones originales, no comprueba resize y carga su costo a `rehash_cost`.

### Modelo abstracto de costo

Una inserción exitosa cuesta 3 unidades: hash, acceso al bucket y append. Un duplicado rechazado cuesta 2. Cada elemento redistribuido cuesta 3 unidades. Por tanto:

```text
total_operation_cost = insert_cost + rehash_cost
amortized_cost = total_operation_cost / original_insertions
```

El tiempo medido con `time.perf_counter()` se registra aparte y nunca se confunde con el costo abstracto.

## Estructura

```text
src/             hashing, tabla, generadores y dataclass de métricas
experiments/     configuración, matriz y experimentos especializados
analysis/        resumen estadístico y gráficas
tests/           pruebas automatizadas
results/raw/     una fila por ejecución
results/summary/ estadísticas agrupadas
figures/         imágenes PNG no interactivas
data/            datos auxiliares opcionales
```

El detalle de fases y decisiones está en [`IMPLEMENTATION_PLAN.md`](IMPLEMENTATION_PLAN.md).

## Instalación

```bash
python -m venv .venv
```

Linux/macOS: `source .venv/bin/activate`

Windows PowerShell: `.venv\Scripts\Activate.ps1`

```bash
pip install -r requirements.txt
python -m pytest
```

## Ejecución

Piloto pequeño:

```bash
python main.py experiment --repetitions 2 --max-n 5000 --overwrite
```

Experimento definitivo (6 tamaños, 9 configuraciones y 30 repeticiones):

```bash
python main.py experiment --repetitions 30 --max-n 100000 --input random --overwrite
```

Sin `--overwrite`, un CSV existente produce un error. Se admiten entradas `random`, `sequential` y `clustered`.

```bash
python main.py threshold-experiment --overwrite
python main.py collision-experiment --repetitions 30 --overwrite
python main.py analyze
python main.py plot
```

`analyze` agrupa por `n`, `growth_factor`, `load_threshold` e `input_type`, y calcula media, mediana, desviación estándar, mínimo y máximo. `plot` genera diez visualizaciones principales y las dos especializadas cuando existen sus datos.

## Reproducibilidad y equidad

Toda aleatoriedad tiene una semilla registrada. Para cada bloque `(n, seed, input_type, repetition)` el dataset se genera una sola vez y se entrega sin cambios a las nueve combinaciones. La función universal también recibe esa semilla. El generador agrupado selecciona aproximadamente `sqrt(n)` centros y usa offsets gaussianos; no conoce los parámetros del hash.

Treinta repeticiones reducen el efecto de semillas particulares y del ruido temporal. Las métricas algorítmicas son independientes del hardware.

## Memoria

`capacity`, `unused_capacity` y `utilization` son mediciones estructurales. `estimated_memory` suma `sys.getsizeof` de la lista principal, buckets y claves; es una aproximación del modelo de objetos de Python, no RAM exacta del proceso.

## Resultados incluidos

Tras validar un piloto con `n = 100, 1000, 5000`, se ejecutó la matriz definitiva aleatoria de 1620 ejecuciones: seis tamaños, nueve configuraciones y 30 repeticiones. Los CSV crudos, el resumen y las figuras incluidos corresponden a esa corrida; la interpretación científica debe considerar las limitaciones siguientes.

## Limitaciones

- Python y el sistema operativo introducen overhead y ruido temporal.
- `sys.getsizeof` no representa toda la memoria residente.
- Sólo se estudian claves `int` y distribuciones limitadas.
- Separate chaining no se generaliza automáticamente a open addressing.
- El conteo de colisiones usa la definición operacional del estudio.
- Costo amortizado y costo esperado son distintos: el primero resume una secuencia y el segundo requiere un modelo probabilístico.
