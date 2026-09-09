# Guía breve para la defensa individual

## Núcleo del estudio

La pregunta varía `gamma` y `tau`. `gamma` determina cuánto crece la capacidad; `tau` cuándo crece. La respuesta no se reduce al tiempo: contrasta migraciones, memoria y colisiones.

- Amortizado: costo total de una secuencia dividido entre operaciones; no necesita probabilidades.
- Esperado: promedio teórico respecto de la elección aleatoria de la función hash.
- Empírico: estadístico de las semillas realmente ejecutadas.
- Evento de colisión: inserción en bucket ocupado.
- Pares: `sum L_j(L_j-1)/2`; una cadena de longitud 4 contiene 6 pares.
- La universalidad acota la probabilidad de colisión de cada par, no el peor caso de cada semilla.
- `tau` es política; `alpha=n/m` es el valor realizado.

## Predicciones que deben poder derivarse

1. Migración amortizada aproximada: `1/(gamma-1)`.
2. Carga después del resize: `alpha_post ~= tau/gamma`.
3. Buckets por elemento después de crecer: `gamma/tau`.
4. Pico de buckets por elemento: `(1+gamma)/tau`.
5. Cota esperada de pares: `n(n-1)/(2m)`.
6. Resizes aproximados: `log_gamma(N/(tau*m0))`.

## Diferencia entre implementaciones

El experimento principal usa encadenamiento separado porque permite contar pares directamente. El secundario usa sondeo lineal: un choque inicia una secuencia de probes y puede producir clustering. No es válido comparar numéricamente ambos contadores como si midieran lo mismo.

## Conceptos generales del bloque final

- Las Vegas siempre responde correctamente, pero su tiempo puede depender de aleatoriedad; el hashing estudiado tiene esa interpretación parcial.
- Monte Carlo limita tiempo admitiendo error; no corresponde a esta tabla.
- P y NP se definen sobre problemas de decisión. Medir una estructura no es demostrar NP-completitud.
- Para NP-completitud se necesita pertenencia a NP y reducción desde un problema NP-completo en la dirección correcta.
- Una heurística carece necesariamente de garantía; un algoritmo de aproximación tiene razón demostrada. La frontera de Pareto aquí no es una razón de aproximación.
- Clique e independiente son complementarios en el grafo complemento; vertex cover e independiente se relacionan por complemento de vértices. Estas relaciones no convierten buckets en una reducción.

## Tres papers núcleo

- Carter y Wegman (1979): familias universales; base de la cota por pares. Limitación: no entrega automáticamente fórmulas de probes.
- Larson (1988): hashing dinámico, carga y expansión. Limitación: representación y hardware antiguos.
- Tarjan y Zwick (2024): frontera tiempo--espacio en arreglos redimensionables. Limitación: no define una política hash `(gamma,tau)`.

Cada integrante debe poder señalar en el CSV una fila, explicar sus semillas y reconstruir al menos una figura desde los datos.
