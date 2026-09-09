# Protocolo congelado

Fecha de congelación: 2026-09-08. La corrida final debe corresponder al commit `2efaf13`; cualquier cambio algorítmico posterior exige regenerar datos.

## Objetivo e hipótesis

La pregunta y H1 se mantienen exactamente como aparecen en `investigacion_hashing_dinamico.md`. H1 recibe apoyo si bajan las migraciones normalizadas al crecer `gamma`, aumentan memoria ociosa/pico con `gamma/tau`, crecen pares/comparaciones con la carga realizada y no existe dominancia única sin explicación.

## Factores

- `gamma`: 1.25, 1.5, 2, 3, 4.
- `tau`: 0.50, 0.70, 0.80, 0.90.
- `N`: 1000, 10000, 100000.
- 30 semillas por celda; 1800 ejecuciones aleatorias.
- `m0=11`, encadenamiento separado y primo `p=2^61-1`.
- Resize antes de insertar; nueva capacidad prima y nuevo `(a,b)`.

## Definiciones

- Evento de colisión: clave nueva llega a bucket ocupado.
- Colisión por pares: suma de `L(L-1)/2` sobre buckets en un checkpoint.
- Comparaciones: igualdades de claves realmente evaluadas.
- Migraciones: claves reinsertadas durante rehash.
- Memoria estable: recorrido `sys.getsizeof` sin doble conteo.
- Pico: slots viejo+nuevo y, complementariamente, `tracemalloc`.
- Costo amortizado: componente total de una secuencia dividido entre inserciones originales.
- Costo esperado: esperanza sobre la selección aleatoria del hash.
- Promedio empírico: estadístico de las semillas ejecutadas.

## Reglas de datos

Los archivos de `data/raw` no se editan manualmente. El análisis sólo escribe en `data/processed`, `figuras/final` y el fragmento LaTeX generado. El piloto se conserva con prefijo `pilot_`; `results/` y `figures/` contienen evidencia preliminar del commit inicial y no se citan como resultado final.
