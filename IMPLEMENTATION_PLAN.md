# Plan de implementación y bitácora

Este documento conserva de forma operativa el orden obligatorio del enunciado entregado. La especificación define `growth_factor = [1.5, 2.0, 3.0]`, `load_threshold = [0.50, 0.75, 0.90]`, seis tamaños hasta 100000, 30 repeticiones, separate chaining, hashing universal, métricas, CSV, estadística, diez gráficas y reproducibilidad mediante semillas.

## Fases ejecutadas

1. **Estructura:** paquetes, directorios, requirements y puntos de entrada.
2. **UniversalHash:** familia `((a*x+b) mod p) mod m` reproducible.
3. **Tabla básica:** `insert`, `contains` y `load_factor`.
4. **Resize:** crecimiento con `ceil`, rehash interno y persistencia.
5. **Métricas:** colisiones, rehashes, elementos movidos e inserciones.
6. **Costo:** costos separados, total y amortizado.
7. **Memoria:** capacidad libre, utilización y estimación Python.
8. **Generadores:** aleatorio, secuencial y agrupado.
9. **ExperimentResult:** dataclass separado de la estructura.
10. **Runner:** temporización y matriz experimental justa.
11. **CSV:** exportación y protección contra sobrescritura.
12. **Threshold:** costo individual alrededor del resize.
13. **Colisiones:** carga de 0.10 a 0.90 sin resize.
14. **Estadística:** cinco estadísticos para once métricas.
15. **Gráficas:** diez vistas principales y dos especializadas.
16. **CLI:** cinco comandos documentados.
17. **Piloto:** 81 ejecuciones; invariantes revisadas sin errores.
18. **Experimento completo:** 1620 ejecuciones aleatorias completadas después de aprobar tests y piloto; resumen y figuras regenerados desde los datos observados.

## Decisiones trazables

- Separate chaining permite observar buckets directamente y simplifica la defensa oral.
- El hash universal reduce dependencia de patrones y registra sus parámetros.
- Una colisión sólo corresponde a una inserción original nueva sobre un bucket ocupado.
- Las reinserciones integran el numerador, no el denominador del costo amortizado.
- El dataset se genera una vez por bloque comparable para evitar sesgo.
- Varias semillas permiten medir dispersión.
- Modelo fijo: 3 unidades por inserción exitosa, 2 por duplicado rechazado y 3 por elemento reubicado.

## Controles antes de la corrida definitiva

```text
python -m pytest
final_size == n
final_load_factor == final_size/final_capacity
total_operation_cost == insert_cost + rehash_cost
amortized_cost == total_operation_cost/n
rehash_operations >= rehashes cuando hubo resize
no modificar el raw CSV durante el análisis
```

```bash
python main.py experiment --repetitions 30 --max-n 100000 --input random --overwrite
```
