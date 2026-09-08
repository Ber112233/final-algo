# Experimento: tabla hash dinámica

Pregunta: ¿Cómo influyen el factor de redimensionamiento y el umbral de carga en el costo amortizado, el consumo de memoria y el número esperado de colisiones de una tabla hash dinámica con hashing universal?

`dynamic_hash_experiment.py` implementa direccionamiento abierto con sondeo lineal y una familia universal `h(k) = ((ak+b) mod p) mod m`. Para cada configuración registra:

- cantidad de redimensionamientos (`rehashes`);
- colisiones de sondeo y cantidad total de sondeos;
- capacidad final como aproximación del uso de memoria;
- tiempo de inserción.

La semilla, tamaños, factores, umbrales y repeticiones son parámetros de línea de comandos. La ejecución completa recomendada es:

```bash
python3 dynamic_hash_experiment.py --repetitions 30 --output-dir results
```

Produce `results/raw_measurements.csv` y `results/summary.csv`. La suma geométrica de las operaciones de rehash se utilizará para contrastar la predicción amortizada; las repeticiones independientes permiten reportar media, mediana y desviación estándar de las colisiones.
