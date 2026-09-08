# Influencia del factor de redimensionamiento y el umbral de carga en tablas hash dinámicas con hashing universal

## Propósito y alcance del documento

Este documento reúne una investigación bibliográfica verificable y un diseño experimental listo para convertirse en el trabajo final de Algorítmica II. La pregunta rectora es:

> **¿Cómo influyen el factor de redimensionamiento y el umbral de carga en el costo amortizado, el consumo de memoria y el número esperado de colisiones de una tabla hash dinámica con hashing universal?**

El texto distingue tres niveles de afirmación:

- **Hecho respaldado por una fuente:** resultado explícito de un artículo o libro citado.
- **Deducción analítica para este estudio:** consecuencia matemática derivada de las definiciones y de resultados publicados.
- **Hipótesis experimental:** predicción que debe contrastarse con mediciones; no se presenta como resultado ya obtenido.

Las claves entre corchetes, por ejemplo `[@CarterWegman1979]`, corresponden a las entradas BibTeX del final. Para la versión LaTeX, deben convertirse en `\cite{CarterWegman1979}` o al comando de citación que use la plantilla.

---

## 1. Síntesis ejecutiva

La literatura no ofrece un único artículo que estudie simultáneamente el factor multiplicativo de crecimiento `γ`, el umbral máximo de carga `τ`, la memoria, el costo amortizado y las colisiones bajo una familia universal. La contribución razonable del trabajo consiste, por tanto, en **integrar tres líneas bien establecidas**:

1. El hashing universal limita la probabilidad de colisión de cada par de claves distintas y permite acotar el número esperado de pares que colisionan [@CarterWegman1979].
2. Las tablas dinámicas preservan el rendimiento controlando la carga y redistribuyendo elementos; las políticas de crecimiento global, crecimiento incremental y reconstrucción tienen costos y perfiles de latencia distintos [@Larson1988; @PaghRodler2004; @BenderEtAl2023].
3. El redimensionamiento presenta un intercambio inevitable entre tiempo y espacio. El crecimiento geométrico clásico logra tiempo amortizado constante usando espacio lineal, mientras estructuras más sofisticadas reducen el espacio sobrante con mecanismos y análisis adicionales [@Tarjan1985; @BrodnikEtAl1999; @TarjanZwick2024].

Para aislar correctamente la pregunta, se recomienda que el experimento principal use **encadenamiento separado** y claves enteras. Con encadenamiento, el número de pares de claves que reciben el mismo bucket puede medirse directamente y compararse con la cota de hashing universal. Un experimento secundario puede usar sondeo lineal, pero no debe asumir que universalidad 2-independiente basta para reproducir las fórmulas clásicas de uniform hashing: el grado y la estructura de independencia de la función importan [@PatrascuThorup2012; @BenderKuszmaulKuszmaul2022].

La hipótesis principal es que no existe una combinación que minimice simultáneamente las tres métricas. Para inserciones solamente:

- un `γ` mayor debe reducir el número de redimensionamientos y el trabajo de migración amortizado, pero aumentar la memoria ociosa y el pico temporal de memoria;
- un `τ` menor debe reducir la carga y las colisiones, pero aumentar la capacidad reservada por elemento;
- `γ` también debe afectar indirectamente las colisiones, porque después de crecer la carga cae aproximadamente de `τ` a `τ/γ`;
- el costo observado en tiempo real puede apartarse del conteo abstracto por efectos de caché, asignación de objetos, recolector de basura e implementación de Python [@RichterAlvarezDittrich2015; @BoetherEtAl2023].

---

## 2. Definiciones operacionales y delimitación

### 2.1 Parámetros

Sea:

- `n`: cantidad de claves almacenadas;
- `m`: cantidad de buckets de la tabla;
- `α = n/m`: factor de carga realizado;
- `τ`: umbral superior de carga que dispara crecimiento;
- `γ > 1`: factor nominal de crecimiento, de modo que `m' ≈ γm`;
- `m₀`: capacidad inicial;
- `p`: primo mayor que cualquier clave admitida por el experimento;
- `h`: función elegida aleatoriamente de una familia universal.

### 2.2 Tabla principal recomendada

La implementación principal debe ser una tabla con **encadenamiento separado**:

- arreglo de `m` buckets;
- cada bucket almacena una secuencia de pares clave–valor;
- al insertar una clave nueva, se registra la longitud previa del bucket y se agrega el elemento;
- antes de una inserción, si `(n + 1)/m > τ`, se crea una tabla con capacidad `next_prime(ceil(γm))`, se elige una nueva función universal y se reinsertan todas las claves.

La decisión de redimensionar **antes** de insertar debe mantenerse constante en todas las configuraciones. Cambiarla altera el máximo de carga alcanzado y dificulta la comparación.

### 2.3 Familia universal propuesta

Para claves enteras `x` en un universo menor que un primo `p`, puede utilizarse la familia clásica:

\[
h_{a,b,m}(x)=((ax+b)\bmod p)\bmod m,
\]

con `a` elegido uniformemente en `{1,…,p−1}` y `b` en `{0,…,p−1}`. En cada redimensionamiento se deben sortear nuevos `a` y `b` a partir de un generador pseudoaleatorio con semilla registrada. El tamaño efectivo será primo y puede diferir de `γm`; por ello debe guardarse también `γ_efectivo = m'/m`.

**Precaución:** el informe final debe citar con precisión la variante de universalidad utilizada. Si la demostración del curso usa una familia o rango diferente, debe conservarse esa definición y adaptar las capacidades. No debe afirmarse “colisiones exactamente uniformes” cuando la propiedad disponible solo da una cota superior.

### 2.4 Tres significados de “colisión” que no deben mezclarse

1. **Evento de inserción en bucket ocupado:** la clave llega a un bucket cuya longitud previa es mayor que cero.
2. **Pares en colisión:**

   \[
   C_{pares}=\sum_{j=0}^{m-1}\binom{L_j}{2},
   \]

   donde `L_j` es la longitud del bucket `j`. Esta es la métrica más directamente comparable con hashing universal.
3. **Costo de resolución:** comparaciones o probes realizados por insertar/buscar. Depende del método de resolución, del orden y de la carga; no es sinónimo del número de pares que colisionan.

El trabajo debe reportar las tres por separado.

---

## 3. Predicciones teóricas que guían el experimento

### 3.1 Colisiones bajo hashing universal

Para una familia universal, dos claves distintas colisionan con probabilidad a lo sumo `1/m`. Si `X_{ij}` indica que el par `{i,j}` colisiona, entonces:

\[
C_{pares}=\sum_{1\le i<j\le n}X_{ij}.
\]

Por linealidad de la esperanza:

\[
\mathbb{E}[C_{pares}]
=\sum_{i<j}\mathbb{E}[X_{ij}]
\le \binom{n}{2}\frac{1}{m}
=\frac{n(n-1)}{2m}
=\frac{\alpha(n-1)}{2}.
\]

Esta es una **cota**, no necesariamente una igualdad. Para una nueva clave que se inserta cuando ya existen `n` claves, el número esperado de claves anteriores que comparten su bucket queda acotado por:

\[
\mathbb{E}[C_{nueva}]\le \frac{n}{m}=\alpha.
\]

Estas deducciones se apoyan en la propiedad de colisión por pares del hashing universal [@CarterWegman1979].

### 3.2 Efecto directo de `τ`

Justo antes de un crecimiento, `α≈τ`. Por ello:

\[
\mathbb{E}[C_{pares}]\lesssim \frac{\tau(n-1)}{2}.
\]

Reducir `τ` reduce linealmente esta cota para un `n` fijo, pero obliga a reservar más buckets. Justo antes de crecer, la cantidad de buckets por elemento es aproximadamente:

\[
\frac{m}{n}\approx\frac{1}{\tau}.
\]

### 3.3 Efecto directo de `γ`

Después de redimensionar desde `m` hasta `m'≈γm`, manteniendo `n≈τm`:

\[
\alpha_{después}\approx\frac{\tau}{\gamma}.
\]

Durante un ciclo de inserciones, la carga recorre aproximadamente:

\[
\alpha\in[\tau/\gamma,\tau].
\]

En el momento del crecimiento, la cota esperada de pares que colisionan cae aproximadamente por un factor `1/γ` al rehashear el mismo conjunto:

\[
\frac{\mathbb{E}[C'_{pares}]}{\mathbb{E}[C_{pares}]}
\lesssim \frac{1}{\gamma}.
\]

Esta comparación es una deducción del cambio de `m`; el valor empírico depende de la familia, la semilla y el conjunto de claves.

### 3.4 Trabajo de migración amortizado

Supóngase inserción solamente, capacidades geométricas exactas `m_j=m₀γ^j` y costo de reconstrucción proporcional al número de elementos reinsertados. Entre dos crecimientos consecutivos se agregan aproximadamente:

\[
\Delta n_j\approx\tau m_j(\gamma-1).
\]

La reconstrucción al final del ciclo mueve cerca de `τm_j` elementos. Por ciclo, el costo de migración por inserción es entonces:

\[
\frac{\tau m_j}{\tau m_j(\gamma-1)}=\frac{1}{\gamma-1}.
\]

Sumando la serie geométrica hasta `N`, el total de elementos movidos es `O(N/(γ−1))`; al sumar el costo normal de las inserciones, la operación conserva costo amortizado `O(1)` para cualquier `γ>1` constante. La constante, sin embargo, crece con rapidez cuando `γ→1`. Esta es una deducción del esquema geométrico, compatible con la teoría general de amortización [@Tarjan1985] y con la observación de que duplicar/reducir permite redimensionamiento esperado amortizado constante [@PaghRodler2004].

### 3.5 Frecuencia de redimensionamiento

Una aproximación al número de crecimientos para alcanzar `N` claves es:

\[
R(N)\approx\left\lceil\log_{\gamma}\left(\frac{N}{\tau m_0}\right)\right\rceil.
\]

En la implementación real debe calcularse a partir del registro de eventos, no solo con esta fórmula, debido al redondeo, el uso de `next_prime` y la convención de redimensionar antes de insertar.

### 3.6 Memoria estable y pico temporal

Inmediatamente después de crecer, la capacidad por elemento es aproximadamente:

\[
\frac{m'}{n}\approx\frac{\gamma}{\tau},
\]

y la fracción ociosa aproximada es `1−τ/γ`. Justo antes del siguiente crecimiento, la fracción ociosa es `1−τ`.

Si la reconstrucción asigna primero la tabla nueva y libera después la anterior, el pico transitorio de buckets es aproximadamente `(1+γ)m`. Respecto de los `n≈τm` elementos presentes:

\[
\text{buckets pico por elemento}\approx\frac{1+\gamma}{\tau}.
\]

Esta medición del pico es esencial: medir solo la memoria después de liberar la tabla vieja ocultaría uno de los costos principales de aumentar `γ`.

### 3.7 Predicción conjunta

Una aproximación útil de la carga media a lo largo de un ciclo, ponderando uniformemente las inserciones del ciclo, es:

\[
\overline{\alpha}_{ciclo}\approx\frac{\tau/\gamma+\tau}{2}
=\frac{\tau}{2}\left(1+\frac{1}{\gamma}\right).
\]

Por tanto, aumentar `γ` puede reducir las colisiones medias del ciclo además de reducir las reconstrucciones, pero lo hace reservando más memoria. El experimento debe buscar una **frontera de Pareto** y no un “mejor valor” universal.

---

## 4. Metodología de búsqueda y criterios de selección

### 4.1 Criterios de inclusión

- Publicación académica verificable en editor, sociedad científica, repositorio institucional o proceedings oficiales.
- Relación directa con al menos uno de estos ejes: hashing universal, colisiones, carga, tablas dinámicas, redimensionamiento, análisis amortizado, intercambio tiempo–espacio o evaluación experimental de tablas hash.
- Metadatos bibliográficos confirmables: autores, título, año, venue y DOI o URL estable.
- Preferencia por artículos revisados por pares y fuentes primarias.
- Inclusión de trabajos recientes solo cuando agregan un resultado pertinente; la novedad cronológica no sustituye la relevancia.

### 4.2 Criterios de exclusión

- Entradas de Wikipedia, blogs, foros, diapositivas y tutoriales como evidencia académica.
- Preprints recientes sin publicación revisada por pares cuando ya existe literatura arbitrada suficiente.
- Trabajos de hashing criptográfico sin relación con diccionarios o tablas hash.
- Artículos que mencionan tablas hash únicamente como componente incidental.
- Fuentes cuyos metadatos o afirmaciones centrales no pudieron verificarse.

### 4.3 Resultado de selección

Se seleccionaron **15 fuentes**:

- **14 publicaciones revisadas por pares:** 11 artículos de revista o proceedings serializados y 3 trabajos en conferencias académicas arbitradas.
- **1 libro de referencia:** no se cuenta como artículo revisado por pares.
- **4 fuentes publicadas dentro de los cinco años anteriores a la fecha de búsqueda (2026-09-08):** Bender et al. (publicado en proceedings 2022), Bender et al. (2023), Böther et al. (2023) y Tarjan–Zwick (2024). Li et al. (2021) se conserva por pertinencia, pero no se cuenta para este criterio temporal estricto.
- **Fuentes fundacionales:** Carter–Wegman (1979), Tarjan (1985) y Knuth (edición de referencia de 1998).

---

## 5. Fichas críticas de las fuentes

### F1. Carter y Wegman (1979) — fuente fundacional de hashing universal

- **Referencia completa:** J. Lawrence Carter y Mark N. Wegman. “Universal Classes of Hash Functions”. *Journal of Computer and System Sciences*, 18(2), 143–154, 1979.
- **Tipo / venue:** artículo de revista; Elsevier, *Journal of Computer and System Sciences*.
- **DOI:** [10.1016/0022-0000(79)90044-8](https://doi.org/10.1016/0022-0000(79)90044-8).
- **Revisión por pares:** sí.
- **Problema:** evitar que una función hash fija tenga entradas patológicas, eligiendo aleatoriamente una función de una clase con garantía de colisión.
- **Método:** definición y análisis probabilístico de clases universales; promedio sobre la elección aleatoria de la función, no sobre una distribución favorable de entradas.
- **Resultado principal:** para cualquier secuencia fija de entradas, la elección aleatoria desde una clase adecuada permite tiempo esperado lineal total para almacenamiento y recuperación; la propiedad por pares fundamenta la cota de colisiones.
- **Limitación/supuesto:** la esperanza es respecto a la función elegida; el adversario no debe adaptar las claves después de observar el secreto aleatorio si se pretende conservar la interpretación adversarial estándar.
- **Uso en el estudio:** justifica `E[C_pares]≤n(n−1)/(2m)`, la repetición sobre semillas de hash y el uso de conjuntos fijos de claves.

### F2. Tarjan (1985) — fundamento del análisis amortizado

- **Referencia completa:** Robert Endre Tarjan. “Amortized Computational Complexity”. *SIAM Journal on Algebraic and Discrete Methods*, 6(2), 306–318, 1985.
- **Tipo / venue:** artículo de revista; SIAM.
- **DOI:** [10.1137/0606031](https://doi.org/10.1137/0606031).
- **Revisión por pares:** sí.
- **Problema:** analizar secuencias de operaciones cuando algunas operaciones aisladas son caras, pero su frecuencia está limitada por el estado de la estructura.
- **Método:** formalización de la complejidad amortizada y aplicación a estructuras de datos.
- **Resultado principal:** la amortización proporciona cotas robustas por operación sobre secuencias, sin asumir que cada operación cuesta lo mismo ni depender de una distribución de entradas.
- **Limitación/supuesto:** no analiza la política específica `(γ,τ)` de este experimento ni el tiempo real de Python.
- **Uso en el estudio:** sustenta separar costo real, costo abstracto y costo amortizado; permite justificar el agregado geométrico del trabajo de rehash.

### F3. Larson (1988) — tablas hash dinámicas, carga y expansión

- **Referencia completa:** Per-Åke Larson. “Dynamic Hash Tables”. *Communications of the ACM*, 31(4), 446–457, 1988.
- **Tipo / venue:** artículo de revista; ACM.
- **DOI:** [10.1145/42404.42410](https://doi.org/10.1145/42404.42410).
- **Revisión por pares:** sí.
- **Problema:** adaptar linear hashing y spiral storage, concebidos para archivos externos, a tablas en memoria principal y compararlos con una tabla fija y un árbol.
- **Método:** diseño de estructuras, análisis matemático de costo esperado y evaluación empírica. Estudia control de carga y crecimiento gradual; además identifica que el costo de una política de rehash global depende de capacidad inicial, carga máxima y factor de expansión.
- **Resultado principal:** el crecimiento incremental evita una reorganización global; para cardinalidad desconocida, linear hashing mostró el mejor rendimiento general entre las alternativas evaluadas. El trabajo documenta variación cíclica de rendimiento durante la expansión.
- **Limitación/supuesto:** arquitectura, lenguaje y costos de memoria de 1988; encadenamiento y parámetros no equivalen automáticamente a Python moderno ni a direccionamiento abierto.
- **Uso en el estudio:** es la fuente más próxima al vínculo conjunto entre umbral, factor de expansión, memoria y costo de carga; motiva registrar la trayectoria completa del ciclo y no solo el estado final.

### F4. Dietzfelbinger et al. (1994) — hashing perfecto dinámico

- **Referencia completa:** Martin Dietzfelbinger, Anna Karlin, Kurt Mehlhorn, Friedhelm Meyer auf der Heide, Hans Rohnert y Robert E. Tarjan. “Dynamic Perfect Hashing: Upper and Lower Bounds”. *SIAM Journal on Computing*, 23(4), 738–761, 1994.
- **Tipo / venue:** artículo de revista; SIAM.
- **DOI:** [10.1137/S0097539791194094](https://doi.org/10.1137/S0097539791194094).
- **Revisión por pares:** sí.
- **Problema:** mantener un diccionario dinámico con inserción, borrado y consulta, combinando rapidez y espacio lineal.
- **Método:** estructura aleatorizada multinivel, reconstrucciones y análisis de cotas superiores e inferiores.
- **Resultado principal:** consultas en `O(1)` peor caso, inserciones y borrados en `O(1)` esperado amortizado y espacio proporcional al conjunto almacenado; también presenta cotas inferiores para una clase de esquemas deterministas.
- **Limitación/supuesto:** la estructura es más compleja que la tabla simple del experimento y su garantía no determina el mejor `γ` o `τ` práctico.
- **Uso en el estudio:** demuestra que dinamismo, aleatorización, espacio lineal y costo amortizado constante pueden coexistir; sirve como referencia teórica, no como implementación base.

### F5. Flajolet, Poblete y Viola (1998) — análisis de sondeo lineal

- **Referencia completa:** Philippe Flajolet, Patricio Poblete y Alfredo Viola. “On the Analysis of Linear Probing Hashing”. *Algorithmica*, 22, 490–515, 1998.
- **Tipo / venue:** artículo de revista; Springer.
- **DOI:** [10.1007/PL00009236](https://doi.org/10.1007/PL00009236).
- **Revisión por pares:** sí.
- **Problema:** caracterizar el costo de construcción de tablas con sondeo lineal en tablas llenas y dispersas.
- **Método:** análisis de momentos y distribuciones límite mediante combinatoria analítica.
- **Resultado principal:** en tablas dispersas con razón de llenado fija menor que uno, el costo de construcción tiene esperanza lineal y desviación estándar de orden raíz; en tablas llenas el comportamiento cambia drásticamente.
- **Limitación/supuesto:** analiza sondeo lineal bajo modelos probabilísticos específicos, no encadenamiento con familia universal ni política de crecimiento concreta.
- **Uso en el estudio:** fundamenta por qué `α` y el mecanismo de resolución deben fijarse o analizarse por separado; sirve para el experimento secundario de direccionamiento abierto.

### F6. Brodnik et al. (1999) — arreglos redimensionables con bajo espacio extra

- **Referencia completa:** Andrej Brodnik, Svante Carlsson, Erik D. Demaine, J. Ian Munro y Robert Sedgewick. “Resizable Arrays in Optimal Time and Space”. En *Algorithms and Data Structures (WADS 1999)*, LNCS 1663, 37–48, Springer, 1999.
- **Tipo / venue:** artículo de conferencia en proceedings.
- **DOI:** [10.1007/3-540-48447-7_4](https://doi.org/10.1007/3-540-48447-7_4).
- **Revisión por pares:** sí.
- **Problema:** mantener un arreglo que crece y decrece con acceso por índice eficiente y menos desperdicio que la duplicación monolítica.
- **Método:** representación por bloques y análisis de tiempo y espacio.
- **Resultado principal:** operaciones en tiempo constante y `O(√n)` de espacio extra más allá de los elementos almacenados.
- **Limitación/supuesto:** no es una tabla hash y cambia la representación; no equivale a escoger otro factor multiplicativo en un arreglo contiguo.
- **Uso en el estudio:** contextualiza que el intercambio observado con crecimiento geométrico no es una imposibilidad universal, sino una propiedad de una política simple y contigua.

### F7. Pagh y Rodler (2004) — cuckoo hashing y reconstrucción esperada

- **Referencia completa:** Rasmus Pagh y Flemming Friche Rodler. “Cuckoo Hashing”. *Journal of Algorithms*, 51(2), 122–144, 2004.
- **Tipo / venue:** artículo de revista; Elsevier.
- **DOI:** [10.1016/j.jalgor.2003.12.002](https://doi.org/10.1016/j.jalgor.2003.12.002).
- **Revisión por pares:** sí.
- **Problema:** construir un diccionario simple con consulta constante peor caso y actualización esperada eficiente.
- **Método:** dos ubicaciones candidatas mediante funciones universales, desplazamientos, análisis probabilístico de inserción y rehash.
- **Resultado principal:** consultas en tiempo constante peor caso e inserciones en tiempo esperado amortizado constante bajo las condiciones del esquema. El artículo señala que duplicar/reducir permite redimensionar en tiempo esperado amortizado constante por actualización.
- **Limitación/supuesto:** el umbral de carga admisible y la noción de colisión difieren del encadenamiento; los fallos de inserción pueden forzar rehash aun sin alcanzar un umbral global.
- **Uso en el estudio:** relaciona universalidad, rehash y amortización; evidencia que la interpretación de `τ` depende del esquema de resolución.

### F8. Pătraşcu y Thorup (2012) — independencia práctica de funciones hash

- **Referencia completa:** Mihai Pătraşcu y Mikkel Thorup. “The Power of Simple Tabulation Hashing”. *Journal of the ACM*, 59(3), artículo 14, 1–50, 2012.
- **Tipo / venue:** artículo de revista; ACM.
- **DOI:** [10.1145/1993636.1993638](https://doi.org/10.1145/1993636.1993638).
- **Revisión por pares:** sí.
- **Problema:** determinar si una función muy rápida y con independencia limitada puede ofrecer garantías típicamente asociadas con mayor aleatoriedad.
- **Método:** análisis probabilístico de simple tabulation y aplicaciones a concentración, minwise, cuckoo hashing y sondeo lineal.
- **Resultado principal:** simple tabulation, aunque no es 4-independiente, ofrece garantías fuertes para varias aplicaciones y es práctica de evaluar.
- **Limitación/supuesto:** las garantías son específicas de la estructura de tabulation; no toda familia 2-universal hereda automáticamente los mismos resultados.
- **Uso en el estudio:** justifica incluir “familia de hash” como control experimental y evita atribuir todo cambio de probes únicamente a `γ` y `τ`.

### F9. Richter, Alvarez y Dittrich (2015) — evaluación multidimensional

- **Referencia completa:** Stefan Richter, Victor Alvarez y Jens Dittrich. “A Seven-Dimensional Analysis of Hashing Methods and its Implications on Query Processing”. *Proceedings of the VLDB Endowment*, 9(3), 96–107, 2015.
- **Tipo / venue:** artículo PVLDB / conferencia VLDB.
- **DOI:** [10.14778/2850583.2850585](https://doi.org/10.14778/2850583.2850585).
- **Revisión por pares:** sí.
- **Problema:** medir cómo distribución, carga, tamaño, mezcla de operaciones, éxito de consultas, esquema de colisión y función hash determinan rendimiento y memoria.
- **Método:** estudio experimental de múltiples combinaciones de esquemas y funciones, con cargas entre 25 % y 90 % y diferentes distribuciones y workloads.
- **Resultado principal:** elegir la combinación apropiada puede producir diferencias de hasta un orden de magnitud; carga, función, esquema, memoria y hardware interactúan. En su plataforma, sondeo lineal muestra clustering perceptible a cargas altas, mientras otras técnicas cambian el intercambio.
- **Limitación/supuesto:** código C/C++, claves de 64 bits y plataforma concreta; sus números no deben trasladarse directamente a Python.
- **Uso en el estudio:** modelo metodológico para factoriales, workloads, tamaños y memoria; respalda que el tiempo de pared sea una métrica secundaria con contexto de hardware.

### F10. Li et al. (2021) — DyCuckoo y redimensionamiento en GPU

- **Referencia completa:** Yuchen Li, Qiwei Zhu, Zheng Lyu, Zhongdong Huang y Jianling Sun. “DyCuckoo: Dynamic Hash Tables on GPUs”. En *2021 IEEE 37th International Conference on Data Engineering (ICDE)*, 744–755, 2021.
- **Tipo / venue:** artículo de conferencia; IEEE ICDE.
- **DOI:** [10.1109/ICDE51399.2021.00070](https://doi.org/10.1109/ICDE51399.2021.00070).
- **Revisión por pares:** sí.
- **Problema:** soportar crecimiento dinámico eficiente en tablas cuckoo sobre GPU, donde redimensionar y mover datos es costoso.
- **Método:** diseño por subtablas y estrategia de expansión orientada a paralelismo GPU, con análisis y evaluación empírica.
- **Resultado principal:** muestra que la estrategia concreta de crecimiento puede reducir la penalización de redimensionamiento frente a reconstrucciones monolíticas en el entorno evaluado.
- **Limitación/supuesto:** arquitectura GPU, concurrencia y cuckoo hashing; no permite inferir constantes para una implementación secuencial de Python.
- **Uso en el estudio:** fuente reciente que confirma que “cómo” se redimensiona es una dimensión separada de “cuándo” y “cuánto”; se usa para delimitar el experimento a reconstrucción global.

### F11. Bender, B. Kuszmaul y W. Kuszmaul (2022) — carga alta y clustering

- **Referencia completa:** Michael A. Bender, Bradley C. Kuszmaul y William Kuszmaul. “Linear Probing Revisited: Tombstones Mark the Demise of Primary Clustering”. En *2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS)*, 1171–1182, publicación de proceedings 2022.
- **Tipo / venue:** artículo de conferencia; IEEE FOCS.
- **DOI:** [10.1109/FOCS52979.2021.00115](https://doi.org/10.1109/FOCS52979.2021.00115).
- **Revisión por pares:** sí.
- **Problema:** revisar la conclusión clásica de que sondeo lineal necesariamente se degrada por clustering primario a carga alta, especialmente con borrados y tombstones.
- **Método:** análisis probabilístico y amortizado de workloads de inserción/borrado y de ventanas de reconstrucción; propuesta de graveyard hashing.
- **Resultado principal:** para carga `1−1/x`, el costo clásico de la última inserción puede ser `Θ(x²)`, pero configuraciones con tombstones y reconstrucción adecuada logran mejores costos amortizados; graveyard hashing obtiene costo esperado `O(x)` por operación bajo sus condiciones.
- **Limitación/supuesto:** sondeo lineal ordenado, manejo específico de tombstones y modelo de workload; no aplica directamente al encadenamiento.
- **Uso en el estudio:** demuestra que umbral y frecuencia de reconstrucción interactúan con la semántica de borrado; motiva separar inserción-only de workloads mixtos.

### F12. Bender et al. (2023) — Iceberg hashing

- **Referencia completa:** Michael A. Bender, Alex Conway, Martín Farach-Colton, William Kuszmaul y Guido Tagliavini. “Iceberg Hashing: Optimizing Many Hash-Table Criteria at Once”. *Journal of the ACM*, 70(6), artículo 40, 1–51, 2023.
- **Tipo / venue:** artículo de revista; ACM.
- **DOI:** [10.1145/3625817](https://doi.org/10.1145/3625817).
- **Revisión por pares:** sí.
- **Problema:** combinar operaciones rápidas, carga muy alta, redimensionamiento dinámico, estabilidad, eficiencia de caché y espacio sucinto.
- **Método:** construcción teórica front-yard/backyard, waterfall addressing, concentración probabilística y quotienting.
- **Resultado principal:** presenta una tabla dinámica sucinta con operaciones constantes con alta probabilidad y solo `O(log log n)` bits extra por clave frente al óptimo informacional, bajo el régimen indicado; logra carga `1−O(log log n/log n)`.
- **Limitación/supuesto:** estructura compleja; algunas garantías de probabilidad extremadamente alta requieren funciones totalmente aleatorias o supuestos más fuertes, señalados por los autores.
- **Uso en el estudio:** frontera moderna del problema y advertencia de que el crecimiento global simple no es la única solución; ayuda a discutir validez externa y trabajo futuro.

### F13. Böther et al. (2023) — carga, colisiones y arquitectura

- **Referencia completa:** Maximilian Böther, Lawrence Benson, Ana Klimovic y Tilmann Rabl. “Analyzing Vectorized Hash Tables Across CPU Architectures”. *Proceedings of the VLDB Endowment*, 16(11), 2755–2768, 2023.
- **Tipo / venue:** artículo PVLDB / conferencia VLDB.
- **DOI:** [10.14778/3611479.3611485](https://doi.org/10.14778/3611479.3611485).
- **Revisión por pares:** sí.
- **Problema:** determinar cómo técnicas vectorizadas y distintos esquemas se comportan en arquitecturas x86, ARM y POWER, especialmente a cargas altas.
- **Método:** microbenchmarks comparativos con cargas de 25 %, 50 %, 70 % y 90 %, tamaños, proporciones de consultas y varias arquitecturas.
- **Resultado principal:** bajar la carga reduce colisiones y probes, pero implica alto costo de memoria; a cargas altas, el esquema y la arquitectura cambian sustancialmente el rendimiento relativo.
- **Limitación/supuesto:** implementaciones vectorizadas nativas y hardware específico; no estudia hashing universal clásico ni factores de crecimiento.
- **Uso en el estudio:** respalda medir tanto contadores abstractos como tiempo y memoria, y registrar el entorno para no generalizar una medición de Python como ley algorítmica.

### F14. Tarjan y Zwick (2024) — frontera tiempo–espacio en arreglos redimensionables

- **Referencia completa:** Robert E. Tarjan y Uri Zwick. “Optimal Resizable Arrays”. *SIAM Journal on Computing*, 53(5), 1354–1380, 2024.
- **Tipo / venue:** artículo de revista; SIAM.
- **DOI:** [10.1137/23M1575792](https://doi.org/10.1137/23M1575792).
- **Revisión por pares:** sí.
- **Problema:** mantener arreglos que crecen y decrecen con acceso constante, distinguiendo espacio permanente y espacio temporal durante la modificación.
- **Método:** construcciones parametrizadas y análisis exacto de un juego de crecimiento, con cotas superiores e inferiores.
- **Resultado principal:** para entero `r≥2`, obtiene almacenamiento `N+O(N^{1/r})`, espacio temporal `N+O(N^{1−1/r})`, acceso peor caso `O(1)` y crecimiento/decrecimiento amortizado `O(r)`; prueba una cota inferior `Ω(r)` para una clase amplia.
- **Limitación/supuesto:** arreglos redimensionables, no tablas hash; la representación sofisticada no es equivalente al esquema multiplicativo contiguo estudiado.
- **Uso en el estudio:** fuente reciente y rigurosa para discutir por separado memoria estable, pico temporal y costo amortizado, exactamente las tres mediciones necesarias durante el rehash.

### Fuente adicional de referencia: Knuth (1998)

- **Referencia completa:** Donald E. Knuth. *The Art of Computer Programming, Volume 3: Sorting and Searching*, 2.ª ed., Addison-Wesley, 1998.
- **Tipo:** libro/monografía de referencia; no se contabiliza como artículo revisado por pares.
- **ISBN/enlace:** ISBN 0-201-89685-0; [página bibliográfica del autor](https://www-cs-faculty.stanford.edu/~knuth/taocp.html).
- **Problema y método:** exposición y análisis clásico de búsqueda y hashing, con modelos probabilísticos y fórmulas de sondeo.
- **Resultado relevante:** consolida el análisis clásico de direccionamiento abierto y el efecto de la carga.
- **Limitación:** libro, no experimento reproducible moderno; varias fórmulas dependen de uniform hashing y no deben atribuirse sin más a cualquier familia universal.
- **Uso:** contexto teórico y comparación con resultados modernos sobre carga alta.

---

## 6. Matriz bibliográfica

| Referencia | Problema/objetivo | Método | Resultado relevante | Limitación/supuesto | Uso en nuestro estudio |
|---|---|---|---|---|---|
| Carter y Wegman (1979) | Evitar entradas patológicas para una función fija | Familias aleatorias y análisis por pares | Probabilidad controlada de colisión y tiempo esperado sobre la función | Esperanza respecto a `h`; adversario no adaptativo | Cota de pares que colisionan y diseño por semillas |
| Tarjan (1985) | Costear secuencias con operaciones ocasionalmente caras | Análisis amortizado | Cotas por operación sobre secuencias completas | No prescribe `γ` ni `τ` | Marco agregado/contable/potencial |
| Larson (1988) | Hacer hashing dinámico en memoria | Análisis + implementación + experimentos | Carga controlada y expansión gradual evitan reorganización global | Plataforma y representación antiguas | Núcleo para umbral, expansión y ciclos |
| Dietzfelbinger et al. (1994) | Diccionario dinámico rápido con espacio lineal | Estructura aleatorizada y reconstrucciones | Consulta `O(1)` peor caso; actualizaciones `O(1)` esperado amortizado | Estructura compleja | Referente teórico de hashing dinámico |
| Flajolet et al. (1998) | Costo de construcción con sondeo lineal | Combinatoria analítica y leyes límite | Régimen disperso y lleno tienen comportamientos distintos | Modelo de sondeo lineal | Robustez para direccionamiento abierto |
| Brodnik et al. (1999) | Arreglo dinámico con poco espacio extra | Bloques y análisis asintótico | `O(1)` por operación y `O(√n)` extra | No usa arreglo monolítico ni hashing | Alternativa al crecimiento geométrico |
| Pagh y Rodler (2004) | Consultas constantes y actualizaciones eficientes | Dos hashes universales, desplazamientos y rehash | Actualización esperada amortizada constante | Umbral y fallos propios de cuckoo | Vincula universalidad, rehash y amortización |
| Pătraşcu y Thorup (2012) | Hash rápido con garantías fuertes | Análisis de simple tabulation | Independencia estructurada basta para varias aplicaciones | No toda familia universal se comporta igual | Control de la familia y experimento secundario |
| Richter et al. (2015) | Comparar dimensiones prácticas del hashing | Experimento factorial amplio | Configuración puede cambiar rendimiento hasta un orden de magnitud | C/C++ y hardware concreto | Plantilla de metodología experimental |
| Li et al. (2021) | Redimensionamiento dinámico eficiente en GPU | DyCuckoo por subtablas y evaluación | El mecanismo incremental modifica la penalización de resize | GPU, concurrencia, cuckoo | Delimita a reconstrucción global y trabajo futuro |
| Bender et al. (2022) | Reexaminar clustering a carga alta con borrados | Análisis amortizado y graveyard hashing | Tombstones y ventana de rebuild cambian el costo asintótico | Sondeo lineal y políticas específicas | Casos mixtos/adversos y frecuencia de rebuild |
| Bender et al. (2023) | Combinar carga alta, rapidez, estabilidad y resize | Iceberg + waterfall addressing | Tabla dinámica sucinta con fuertes garantías | Complejidad y supuestos de aleatoriedad | Estado del arte y límites de generalización |
| Böther et al. (2023) | Hash vectorizado en varias CPU | Microbenchmarks multi-arquitectura | Carga, memoria y arquitectura interactúan | No estudia `γ` ni universalidad clásica | Métricas de tiempo/memoria y validez externa |
| Tarjan y Zwick (2024) | Frontera tiempo–espacio de arrays dinámicos | Construcciones parametrizadas + cotas | Separa memoria estable, temporal y costo amortizado | No es tabla hash simple | Marco moderno para memoria pico y estable |
| Knuth (1998) | Sistematizar búsqueda y hashing clásico | Monografía analítica | Fórmulas clásicas de hashing y sondeo | No es artículo; supuestos fuertes de uniformidad | Contexto y contraste histórico |

---

## 7. Tres papers núcleo

### 7.1 Carter y Wegman (1979)

**Problema.** Una función hash determinista puede ser excelente para unas claves y desastrosa para otras. El artículo pregunta cómo obtener garantías independientes de la distribución de entradas.

**Método.** Escoger aleatoriamente una función de una clase universal y analizar la probabilidad de que dos claves distintas colisionen. El conjunto de claves puede ser arbitrario, siempre que quede fijado independientemente de la elección secreta.

**Resultado.** La propiedad por pares permite acotar la esperanza de colisiones y el tiempo esperado de operaciones en esquemas apropiados. En este trabajo, mediante variables indicadoras, da `E[C_pares]≤binom(n,2)/m`.

**Limitación.** La garantía no dice que cada ejecución tendrá pocas colisiones ni que los probes de todo esquema de direccionamiento abierto sigan el modelo de hash totalmente aleatorio.

**Relación.** Es la base probabilística de la variable dependiente “número esperado de colisiones” y obliga a promediar sobre elecciones independientes de `h`.

### 7.2 Larson (1988)

**Problema.** Una tabla cuyo tamaño final se desconoce debe crecer sin que la carga destruya el rendimiento ni cada ampliación cause una pausa global costosa.

**Método.** Adaptar y comparar crecimiento incremental mediante linear hashing y spiral storage, analizar la carga esperada y medir implementaciones. El artículo hace explícito que en el rehash global intervienen capacidad inicial, carga máxima y factor de expansión.

**Resultado.** El crecimiento incremental mueve solo una fracción local a cada paso; el costo y rendimiento fluctúan durante ciclos de expansión. La carga debe controlarse y la representación determina memoria y tiempo.

**Limitación.** La implementación y hardware son antiguos; el factor de carga en encadenamiento puede superar uno y no es comparable sin cuidado al de direccionamiento abierto.

**Relación.** Es el antecedente más directo de la pregunta experimental. Justifica observar toda la serie temporal de carga, colisiones, memoria y migraciones, no únicamente promedios finales.

### 7.3 Tarjan y Zwick (2024)

**Problema.** Reducir el espacio sobrante de un arreglo redimensionable conservando acceso constante y crecimiento eficiente, distinguiendo memoria normal de memoria temporal.

**Método.** Familias de estructuras parametrizadas, análisis exacto y cotas inferiores.

**Resultado.** Exhibe una curva explícita entre espacio estable, espacio temporal y costo amortizado, y muestra que optimizar una dimensión exige pagar en otra dentro del modelo estudiado.

**Limitación.** No es una tabla hash y utiliza estructuras más sofisticadas que un arreglo monolítico multiplicado por `γ`.

**Relación.** Proporciona el marco contemporáneo para interpretar el resultado del experimento como intercambio tiempo–espacio, y refuerza la necesidad de medir el pico durante el rehash.

---

## 8. Estado del arte organizado por temas

### 8.1 Hashing universal

Carter y Wegman introducen el enfoque de aleatorizar la función en lugar de asumir que las claves provienen de una distribución benigna [@CarterWegman1979]. La garantía básica controla colisiones por pares y funciona para cualquier conjunto fijo de claves. Trabajos posteriores muestran que la cantidad o estructura de independencia requerida depende de la aplicación: una familia útil para encadenamiento no necesariamente conserva los costos del sondeo lineal o cuckoo hashing [@PaghRodler2004; @PatrascuThorup2012].

**Implicación:** el estudio debe declarar la familia exacta, volver a sortear sus parámetros en cada ensayo y no usar la función integrada de Python como sustituto tácito de una familia universal.

### 8.2 Colisiones y factor de carga

En encadenamiento, la universalidad da una relación limpia entre `α` y colisiones esperadas. En direccionamiento abierto, la carga modifica la longitud de probes y puede inducir clustering; el comportamiento depende del esquema y de la independencia del hash [@FlajoletPobleteViola1998; @BenderKuszmaulKuszmaul2022]. Los estudios empíricos muestran que subir la carga ahorra espacio, pero cambia sustancialmente el rendimiento y la importancia relativa de cada esquema [@RichterAlvarezDittrich2015; @BoetherEtAl2023].

**Implicación:** `C_pares`, eventos de bucket ocupado, longitud de cadena y tiempo no son intercambiables. Deben graficarse por separado contra la carga realizada.

### 8.3 Redimensionamiento dinámico

La reconstrucción global reasigna un arreglo mayor y rehashéa todas las claves. El crecimiento geométrico limita cuántas veces puede pagarse ese costo. Linear hashing distribuye el crecimiento bucket por bucket [@Larson1988]; cuckoo hashing añade reconstrucciones por fallos de inserción [@PaghRodler2004]; DyCuckoo explota subtablas en GPU [@LiEtAl2021]; Iceberg usa waterfall addressing para crecimiento fino sin indirection [@BenderEtAl2023].

**Implicación:** el estudio debe declarar que evalúa **rehash global geométrico**, no “todas las tablas dinámicas”. La comparación con técnicas incrementales pertenece a discusión o trabajo futuro.

### 8.4 Análisis amortizado

La amortización analiza una secuencia completa y no es un promedio probabilístico [@Tarjan1985]. En una política geométrica, una reconstrucción `Θ(n)` es infrecuente porque antes deben ocurrir `Θ((γ−1)n)` inserciones. La aleatoriedad entra en el costo de colisiones; la amortización entra en la frecuencia de reconstrucciones. Son dos esperanzas/promedios conceptualmente distintos y deben presentarse por separado.

**Implicación:** se reportarán (a) costo amortizado determinista de migración, (b) costo esperado de colisiones sobre semillas y (c) tiempo empírico.

### 8.5 Análisis esperado y aleatorización

Dynamic perfect hashing y cuckoo hashing combinan reconstrucción y aleatorización para ofrecer operaciones esperadas eficientes [@DietzfelbingerEtAl1994; @PaghRodler2004]. La esperanza debe indicar siempre su espacio de probabilidad: elección de `h`, orden de claves, workload o todos ellos. La linealidad de la esperanza no exige independencia entre todos los indicadores, pero sí una cota válida para cada par.

**Implicación:** usar bloques experimentales: el mismo conjunto de claves se prueba con múltiples semillas de hash y todas las combinaciones `(γ,τ)`.

### 8.6 Evaluación experimental

Richter et al. muestran que distribución, tamaño, proporción lectura/escritura, éxitos, esquema y función pueden interactuar [@RichterAlvarezDittrich2015]. Böther et al. muestran además que conclusiones de rendimiento pueden cambiar con arquitectura y vectorización [@BoetherEtAl2023]. Por ello, los contadores algorítmicos reproducibles deben ser la evidencia primaria, mientras nanosegundos por operación y bytes de Python son evidencia secundaria dependiente de plataforma.

**Implicación:** publicar semillas, versiones, comandos, CSV crudo, notebook/script de gráficos y especificación del equipo.

---

## 9. Vacío de investigación y contribución propuesta

La literatura seleccionada explica por separado:

- cómo la universalidad limita colisiones;
- cómo la carga afecta costos de hashing;
- cómo el crecimiento y la reconstrucción pueden amortizarse;
- cómo memoria, carga y hardware alteran resultados prácticos.

No se encontró, dentro del conjunto verificado, un estudio pedagógico y reproducible que barra explícitamente una cuadrícula de factores multiplicativos `γ` y umbrales `τ` sobre **la misma tabla con encadenamiento y la misma familia universal**, registrando simultáneamente migraciones, colisiones por pares, comparaciones y memoria estable/pico. Ese es el espacio concreto que puede cubrir el proyecto.

Esta afirmación debe redactarse como **“no se encontró en la búsqueda realizada”**, no como “no existe ningún trabajo”.

---

## 10. Formulación del estudio

### 10.1 Hipótesis principal

> **H1.** En una tabla hash dinámica con encadenamiento separado y hashing universal, aumentar el factor de crecimiento `γ` reducirá el número de redimensionamientos y el costo de migración amortizado aproximadamente según `1/(γ−1)`, pero incrementará la capacidad ociosa y el pico de memoria; reducir el umbral `τ` disminuirá el número esperado de colisiones al mantener menor carga, pero aumentará la memoria reservada. La interacción `(γ,τ)` producirá una frontera de Pareto y no un óptimo único para tiempo, memoria y colisiones.

### 10.2 Hipótesis secundarias

- **H1a:** `elementos_migrados/N` decrece monótonamente al aumentar `γ`, salvo pequeñas irregularidades por redondeo y capacidades primas.
- **H1b:** para `n,m` observados, la media de `C_pares` sobre semillas no excederá sistemáticamente `n(n−1)/(2m)` más allá de la variabilidad esperable y errores de implementación.
- **H1c:** a `γ` fijo, disminuir `τ` reducirá `α` media, colisiones y comparaciones, y aumentará buckets por elemento.
- **H1d:** a `τ` fijo, aumentar `γ` reducirá la carga inmediatamente posterior al crecimiento `≈τ/γ`, pero aumentará el espacio ocioso máximo.
- **H1e:** las tendencias en contadores abstractos serán más estables entre equipos que las tendencias en tiempo de pared.

### 10.3 Hipótesis nula útil

> **H0.** Una vez controlada la carga realizada `α`, `γ` y `τ` no tienen efecto adicional sobre colisiones por pares; cualquier efecto residual procede de la trayectoria de cargas, redondeo, elección de nuevos hashes o ruido experimental.

Esta hipótesis separa el mecanismo directo (`α`) del efecto indirecto de la política (`γ,τ`).

---

## 11. Variables

### 11.1 Independientes principales

| Variable | Valores iniciales recomendados | Justificación |
|---|---:|---|
| Factor de crecimiento `γ` | 1.25, 1.5, 2, 3, 4 | Incluye crecimiento conservador, duplicación y factores agresivos |
| Umbral superior `τ` | 0.50, 0.70, 0.80, 0.90 | Barre carga baja a alta sin exceder 1 en el experimento secundario |

### 11.2 Factores de bloqueo/control

- tamaño final `N ∈ {10³,10⁴,10⁵}`;
- semilla de la función universal;
- conjunto de claves;
- orden de inserción;
- capacidad inicial `m₀`;
- familia universal y primo `p`;
- estrategia de colisión;
- versión de Python, sistema operativo y hardware;
- criterio exacto para crecer;
- activación del recolector de basura en mediciones temporales.

### 11.3 Dependientes primarias

- costo abstracto total y por operación;
- número total de elementos migrados;
- cantidad de redimensionamientos;
- `C_pares` después de cada checkpoint y al final;
- eventos de inserción en bucket ocupado;
- comparaciones de clave por inserción y búsqueda;
- capacidad `m`, buckets por elemento y fracción ociosa;
- memoria estable y pico durante rehash.

### 11.4 Dependientes secundarias

- tiempo total y nanosegundos por operación;
- pausa máxima y percentiles de latencia de inserción (`p50`, `p95`, `p99`, máximo);
- longitud máxima y distribución de longitudes de bucket;
- tasa de consultas exitosas/no exitosas si se añaden búsquedas.

### 11.5 Variables derivadas

- `γ_efectivo = m_nuevo/m_viejo`;
- `α_pre` y `α_post` en cada crecimiento;
- `migraciones_por_inserción = total_migrado/N`;
- `colisiones_pares_por_clave = C_pares/n`;
- `ratio_cota = C_pares / (n(n−1)/(2m))`;
- `bytes_por_elemento` y `pico/estable`;
- área bajo la curva de `α` por operación.

---

## 12. Línea base y tratamientos

### 12.1 Línea base

`γ=2`, `τ=0.75`, encadenamiento separado, `m₀=11`, familia universal modular, crecimiento global antes de insertar y nueva función `h` en cada rehash.

La línea base es una convención experimental razonable; no debe presentarse como valor universalmente óptimo.

### 12.2 Diseño factorial principal

- 5 valores de `γ` × 4 valores de `τ` = 20 tratamientos.
- 3 tamaños `N`.
- al menos 30 semillas independientes por celda si el tiempo lo permite.
- mismo conjunto de claves y orden para todos los tratamientos de un bloque.
- orden de ejecución aleatorizado para reducir sesgo térmico o de carga del sistema.

Total sugerido: `20 × 3 × 30 = 1800` ejecuciones por tipo de conjunto. Iniciar con un piloto de 5 semillas y `N≤10⁴`; ajustar después el número de repeticiones con base en la varianza observada.

### 12.3 Unidad experimental

Una ejecución completa con una combinación `(γ,τ,N,tipo_claves,semilla_hash,semilla_orden)` constituye una unidad experimental. Checkpoints dentro de la misma ejecución son medidas repetidas, no réplicas independientes.

---

## 13. Casos normales, límite y adversos

### 13.1 Normales

- claves enteras únicas pseudoaleatorias;
- claves secuenciales `0,…,N−1` con orden barajado;
- inserción solamente hasta `N`;
- búsquedas 50 % exitosas y 50 % fallidas después de construir la tabla.

### 13.2 Límite

- `γ=1.25`: muchos redimensionamientos; debe elevar el costo de migración;
- `γ=4`: gran caída de carga después de crecer; debe maximizar memoria ociosa/pico;
- `τ=0.50`: pocas colisiones y mayor reserva;
- `τ=0.90`: cadenas más largas y menor reserva;
- `N` muy cercano a un umbral de crecimiento y `N` inmediatamente posterior;
- capacidad pequeña, donde redondear al siguiente primo distorsiona `γ`.

### 13.3 Adversos no adaptativos

- claves con patrones estructurados: múltiplos de potencias de dos, progresiones aritméticas y bits bajos repetidos;
- orden creciente, decreciente y permutado;
- conjunto fijo elegido antes de sortear `(a,b)`;
- consultas fallidas dirigidas a buckets largos **solo para medir costo posterior**, sin elegir nuevas claves observando el secreto hash.

### 13.4 Adverso adaptativo, separado

Un adversario que observa `a,b` y fabrica colisiones puede invalidar la garantía práctica. Si se incluye, debe llamarse “experimento de exposición del hash” y no mezclarse con la prueba de hashing universal. Su objetivo sería mostrar el límite del supuesto de adversario no adaptativo.

### 13.5 Workload mixto con borrados

Debe ser un experimento secundario. Introducir un umbral de contracción `σ` que cumpla:

\[
\gamma\sigma<\tau,
\]

para evitar que contraer dispare inmediatamente un crecimiento. Una opción simétrica es `σ=τ/γ²`, pues después de contraer la carga vuelve aproximadamente a `τ/γ`. Incluir un caso adverso que oscile alrededor de los umbrales para demostrar el costo de una histéresis mal diseñada. Relacionar la discusión con la frecuencia de reconstrucción de Bender et al. [@BenderKuszmaulKuszmaul2022].

---

## 14. Instrumentación recomendada en Python

### 14.1 Contadores deterministas

La clase debe registrar explícitamente:

```text
hash_evaluations
key_comparisons
insert_collision_events
pair_collisions_current
pair_collisions_accumulated_at_checkpoints
resize_count
moved_entries
allocated_bucket_slots_current
allocated_bucket_slots_peak
max_chain_length
```

Para actualizar `pair_collisions_current` en `O(1)`, si una clave entra en un bucket de longitud `L`, agregar `L`; al remover una clave de un bucket de longitud previa `L`, restar `L−1`. Durante rehash, reconstruir el contador desde cero para la nueva distribución.

### 14.2 Costo abstracto

Definir antes de ejecutar:

\[
C_{abstracto}=w_hH+w_cC+w_mM+w_aA,
\]

donde `H` son evaluaciones de hash, `C` comparaciones, `M` elementos migrados y `A` asignaciones de bucket. La presentación principal debe mostrar cada componente sin pesos. Si se muestra una suma ponderada, justificar y hacer análisis de sensibilidad; no ocultar conclusiones detrás de pesos arbitrarios.

### 14.3 Memoria

Reportar dos vistas:

1. **Modelo estructural independiente de Python:** cantidad de buckets, elementos, referencias y buckets pico durante el rehash.
2. **Memoria física aproximada:** `sys.getsizeof` con recorrido que evite doble conteo por identidad; opcionalmente `tracemalloc` para pico del proceso Python.

No usar solo RSS del proceso, porque incluye intérprete, allocator y memoria no devuelta al sistema. No usar solo `tracemalloc`, porque no representa necesariamente toda la memoria nativa.

### 14.4 Tiempo

- usar `time.perf_counter_ns()`;
- ejecutar calentamiento fuera de medición;
- medir construcción completa y, por separado, latencia individual en una muestra para no introducir demasiado overhead;
- evitar I/O y logging dentro de la región medida;
- registrar si GC está activado;
- repetir en proceso limpio cuando sea viable;
- guardar mediana y distribución, no solo el mínimo.

### 14.5 Archivos de salida

```text
src/universal_hash.py
src/dynamic_hash_table.py
src/workloads.py
src/metrics.py
experiments/run_factorial.py
analysis/analyze_results.py
analysis/plots.py
tests/test_hash_family.py
tests/test_resize_invariants.py
tests/test_collision_counter.py
data/raw/results.csv
data/processed/summary.csv
figures/
environment.txt
requirements.txt
README.md
```

### 14.6 Esquema mínimo del CSV

```text
run_id,git_commit,python_version,platform,cpu,
gamma_nominal,gamma_effective,tau,sigma,m0,n_final,m_final,
key_family,key_seed,order_seed,hash_seed,a,b,p,
resize_count,moved_entries,hash_evaluations,key_comparisons,
insert_collision_events,pair_collisions,max_chain,
bucket_slots_peak,structural_bytes_final,tracemalloc_peak_bytes,
elapsed_ns
```

---

## 15. Validaciones previas a experimentar

1. **Invariante de tamaño:** `n` coincide con la suma de longitudes de buckets.
2. **Unicidad:** ninguna clave aparece dos veces.
3. **Ubicación:** cada clave está en el bucket indicado por la función vigente.
4. **Carga:** después de cada operación se respeta la convención del umbral.
5. **Conservación en rehash:** conjunto antes = conjunto después.
6. **Contador de pares:** contador incremental = suma completa `Σ binom(L_j,2)`.
7. **Determinismo:** misma semilla y parámetros producen el mismo CSV de contadores.
8. **Universalidad empírica diagnóstica:** para pares fijos y muchas elecciones de `(a,b)`, la frecuencia observada no debe indicar una violación sistemática de la cota; esta prueba no sustituye la demostración.
9. **Casos pequeños exhaustivos:** comparar contra un diccionario simple para secuencias de insertar/buscar/borrar.
10. **Resize exacto:** comprobar `α_pre`, `α_post`, `γ_efectivo` y conteo de elementos movidos.

---

## 16. Plan de análisis estadístico y visual

### 16.1 Resúmenes

Para cada celda `(γ,τ,N,tipo_claves)`:

- media, mediana, desviación estándar e intervalo de confianza bootstrap del 95 %;
- distribución sobre semillas de `C_pares`, comparaciones y tiempo;
- normalización por `N` cuando corresponda.

### 16.2 Modelos

- modelo principal para `migraciones/N`: efectos de `γ`, `τ`, tamaño e interacción;
- modelo para `C_pares/n`: carga realizada como mediador, más tipo de claves y semilla como bloque;
- modelo para bytes/elemento: `γ`, `τ` e interacción;
- no interpretar significancia estadística sin tamaño de efecto e intervalos.

Si las distribuciones son sesgadas, usar bootstrap o modelos robustos en lugar de forzar normalidad.

### 16.3 Gráficos obligatorios

1. Heatmap de `migraciones/N` por `(γ,τ)`.
2. Heatmap de bytes/elemento por `(γ,τ)`.
3. Heatmap de `C_pares/n` por `(γ,τ)`.
4. Curva temporal de `α`, memoria y colisiones alrededor de varios resizes.
5. Observado frente a cota `n(n−1)/(2m)`.
6. Número de resizes frente a `log_γ(N/(τm₀))`.
7. Frontera de Pareto: migraciones, memoria y colisiones.
8. Boxplots o violin plots sobre semillas.

### 16.4 Criterio de apoyo a H1

H1 recibe apoyo si:

- las migraciones normalizadas decrecen consistentemente con `γ` y siguen el orden previsto por `1/(γ−1)`;
- la memoria ociosa y el pico crecen con `γ/τ` y `(1+γ)/τ`;
- colisiones/comparaciones aumentan con la carga realizada y, a igualdad aproximada de otras condiciones, con `τ`;
- ninguna configuración domina simultáneamente en todas las métricas, o las dominancias se explican y delimitan.

---

## 17. Amenazas a la validez

### 17.1 Validez de constructo

- “Colisión” puede significar bucket ocupado, par colisionante o probe adicional.
- `sys.getsizeof`, `tracemalloc` y slots teóricos miden cosas distintas.
- Tiempo de pared no equivale a costo algorítmico.
- En encadenamiento, `α` puede superar 1; limitarla a menos de 1 es decisión experimental, no requisito estructural.

**Mitigación:** definiciones previas, varias métricas y resultados separados.

### 17.2 Validez interna

- Cambiar la función al redimensionar mezcla el efecto de capacidad con una nueva aleatorización.
- Usar `next_prime` altera `γ` efectivo.
- GC, allocator, temperatura y procesos del sistema contaminan tiempo y memoria.
- Reutilizar semillas de modo incorrecto crea pseudorreplicación.
- Medir cada inserción puede cambiar el rendimiento.

**Mitigación:** registrar `γ_efectivo`, usar bloques y semillas separadas, aleatorizar orden de tratamientos y priorizar contadores.

### 17.3 Validez externa

- Python agrega overhead y su jerarquía de memoria difiere de C/C++.
- Claves enteras no representan strings u objetos costosos.
- Encadenamiento no generaliza a sondeo lineal, cuckoo, Robin Hood o Iceberg.
- Ejecución monohilo no generaliza a concurrencia, GPU o memoria persistente.

**Mitigación:** limitar las conclusiones y presentar variantes como trabajo futuro.

### 17.4 Validez estadística

- Pocas semillas pueden ocultar colas o eventos raros.
- Checkpoints de la misma corrida no son independientes.
- Muchas comparaciones aumentan falsos positivos.
- Cronometrías cortas tienen baja relación señal/ruido.

**Mitigación:** piloto, potencia basada en varianza, intervalos, corrección por multiplicidad cuando corresponda y replicación por ejecución completa.

### 17.5 Amenaza teórica principal

Universalidad por pares basta para la cota de pares que colisionan, pero no para todas las concentraciones, máximos de bucket o costos de sondeo. No extender una garantía más allá del modelo de la fuente [@PatrascuThorup2012; @BenderEtAl2023].

---

## 18. Relación esperada entre teoría y resultados

| Predicción | Base | Evidencia que debe verse | Interpretación si no aparece |
|---|---|---|---|
| `α_post≈τ/γ` | Identidad algebraica | Checkpoints de cada resize | Error de convención, redondeo o cálculo |
| Migración amortizada `≈1/(γ−1)` | Serie geométrica | `moved_entries/N` por `γ` | Efectos de `m₀`, final truncado o primes |
| `E[C_pares]≤n(n−1)/(2m)` | Universalidad + indicadores | Media sobre hashes bajo la cota | Posible función mal implementada o ensayos insuficientes |
| Menor `τ` → menos colisiones | Menor carga máxima/media | Caída de `C_pares/n` | Familia, tamaño pequeño o métrica mezclada |
| Mayor `γ` → mayor memoria pico | Asignación vieja+nueva | Pico cercano a `(1+γ)m` | Resize in-place/incremental o medición incompleta |
| Tiempo no sigue exactamente contadores | Caché/runtime | Diferencias entre plataformas | Si coincide, reportar que ocurrió sin universalizar |

Los resultados empíricos no “demuestran” la cota universal; pueden ser consistentes con ella o detectar una implementación incompatible. La demostración proviene de la propiedad matemática de la familia.

---

## 19. Registro de búsqueda reproducible

**Fecha de todas las búsquedas:** 2026-09-08.  
**Nota sobre conteos:** los portales/motores consultados no siempre exponen el total de coincidencias. “Resultados encontrados” registra candidatos académicos relevantes visibles y examinados, no el tamaño completo del índice.

| Base/portal | Fecha | Consulta exacta | Filtros | Resultados encontrados | Fuentes seleccionadas |
|---|---|---|---|---:|---|
| Búsqueda web académica + páginas de editor | 2026-09-08 | `"dynamic hash table" resizing amortized analysis paper` | Fuentes primarias; inglés | ≥8 candidatos relevantes | Larson 1988; Pagh–Rodler 2004; Iceberg 2023 |
| ScienceDirect / ACM | 2026-09-08 | `"universal hashing" expected collisions paper DOI` | Artículos con DOI | ≥6 | Carter–Wegman 1979; Pătraşcu–Thorup 2012 |
| Springer / VLDB | 2026-09-08 | `"hash table" "load factor" performance journal` | Journal/proceedings | ≥7 | Richter et al. 2015; Böther et al. 2023 |
| ACM Digital Library | 2026-09-08 | `site:dl.acm.org hash table resizing load factor 2021 2022 2023` | 2021–2023 | ≥5 | Bender et al. 2022; Iceberg 2023 |
| SIAM | 2026-09-08 | `site:epubs.siam.org dynamic hash table load factor amortized` | Revista SIAM | ≥3 | Dietzfelbinger et al. 1994 |
| IEEE Xplore | 2026-09-08 | `site:ieeexplore.ieee.org dynamic hash table resizing 2021 GPU` | 2021; proceedings IEEE | ≥2 | Li et al. 2021 |
| ACM / repositorios de autores | 2026-09-08 | `Mihai Patrascu Mikkel Thorup The Power of Simple Tabulation Hashing Journal ACM DOI` | Título exacto | 2 versiones | Pătraşcu–Thorup 2012 |
| IEEE / repositorio FOCS | 2026-09-08 | `"Linear Probing Revisited: Tombstones Mark the Demise" DOI` | Título exacto | 3 registros/versiones | Bender et al. 2022 |
| Springer | 2026-09-08 | `Flajolet Poblete Viola On the analysis of linear probing hashing DOI` | Título/autores exactos | 2 | Flajolet et al. 1998 |
| SIAM / Princeton | 2026-09-08 | `Tarjan Amortized Computational Complexity SIAM 1985 DOI` | Artículo original | 3 | Tarjan 1985 |
| Springer / Waterloo / páginas de autor | 2026-09-08 | `"Resizable Arrays in Optimal Time and Space" DOI` | Proceedings verificados | 4 | Brodnik et al. 1999 |
| SIAM | 2026-09-08 | `"Optimal Resizable Arrays" SIAM DOI` | 2021–2026; revista | 2 | Tarjan–Zwick 2024 |
| PVLDB | 2026-09-08 | `"A Seven-Dimensional Analysis of Hashing Methods" DOI` | Proceedings VLDB | 3 | Richter et al. 2015 |
| PVLDB | 2026-09-08 | `"Analyzing Vectorized Hash Tables Across CPU Architectures" DOI` | 2021–2026 | 4 | Böther et al. 2023 |
| IEEE / SMU | 2026-09-08 | `"DyCuckoo" "10.1109/ICDE51399.2021.00070"` | DOI/título exacto | 4 | Li et al. 2021 |
| Stanford / Google Books | 2026-09-08 | `Knuth Art of Computer Programming volume 3 hashing load factor ISBN` | Libro de referencia | 3 | Knuth 1998 |

### Verificación bibliográfica aplicada

- DOI y metadatos contrastados en ACM, IEEE, SIAM, Springer, ScienceDirect, PVLDB o página institucional/autoral.
- Cuando se consultó una versión arXiv o PDF de autor para leer contenido, la referencia final apunta a la versión publicada revisada por pares.
- No se incluyeron blogs, Wikipedia ni foros como fuentes de afirmaciones académicas.
- El preprint “Hive Hash Table” (2025) se excluyó porque no se confirmó una versión arbitrada estable durante esta búsqueda.
- Una revisión narrativa amplia de 2025 se excluyó del núcleo porque no aporta evidencia primaria específica sobre el factorial `(γ,τ)`.

---

## 20. Borrador de actualización para la bitácora individual

**Advertencia:** todas las filas están marcadas como **borrador para verificar**. No deben incorporarse como actividades realizadas sin que la persona responsable confirme fecha, autoría, evidencia y verificación. Las filas futuras describen trabajo propuesto, no trabajo completado.

| Fecha | Hito | Actividad | Decisión técnica | Evidencia/archivo | Fuente consultada | Uso de IA | Verificación realizada | Resultado/aprendizaje |
|---|---|---|---|---|---|---|---|---|
| 2026-09-08 — **borrador para verificar** | Definición de la pregunta | Delimitar relación entre `γ`, `τ`, costo amortizado, memoria y colisiones | Tratar la pregunta como intercambio multiobjetivo | Enunciado de investigación | Material del curso | IA usada para organizar variables | Pendiente de validación con docente/equipo | Pregunta medible con factorial `(γ,τ)` |
| 2026-09-08 — **borrador para verificar** | Búsqueda bibliográfica | Revisar fuentes fundacionales, dinámicas y recientes | Priorizar editor/DOI y excluir referencias no verificables | `investigacion_hashing_dinamico.md` | Carter–Wegman; Larson; Tarjan; fuentes de matriz | IA usada para búsqueda, síntesis y control de metadatos | DOI/enlaces contrastados; lectura humana pendiente | La literatura se divide en universalidad, resize y trade-off tiempo–espacio |
| Fecha pendiente — **borrador para verificar** | Diseño experimental | Definir tabla principal, tratamientos, semillas y métricas | Encadenamiento separado; línea base `(2,0.75)`; rehash global | `design.md` o sección metodológica | Carter–Wegman; Richter et al. | IA propuesta para revisar consistencia | **No realizada** | Resultado pendiente |
| Fecha pendiente — **borrador para verificar** | Implementación Python | Implementar familia universal, tabla e instrumentación | Nueva `(a,b)` por rehash; registrar `γ_efectivo` y memoria pico | `src/`, `tests/` | Carter–Wegman; Pagh–Rodler | IA propuesta para apoyo de código y tests | **No realizada** | Resultado pendiente |
| Fecha pendiente — **borrador para verificar** | Piloto | Ejecutar casos pequeños y 5 semillas | Ajustar `N` y réplicas según varianza/tiempo | `data/raw/pilot.csv` | Metodología de Richter et al. | IA propuesta para scripts/análisis | **No realizada** | Resultado pendiente |
| Fecha pendiente — **borrador para verificar** | Experimento factorial | Ejecutar 20 configuraciones × tamaños × semillas | Orden aleatorizado y bloques comunes | `data/raw/results.csv`, `environment.txt` | Plan experimental | IA propuesta para automatización | **No realizada** | Resultado pendiente |
| Fecha pendiente — **borrador para verificar** | Análisis | Comparar observado con fórmulas y construir Pareto | Priorizar contadores; tiempo como resultado dependiente de plataforma | `summary.csv`, `figures/` | Tarjan; Böther et al. | IA propuesta para revisión de gráficos | **No realizada** | Resultado pendiente |
| Fecha pendiente — **borrador para verificar** | Redacción final | Integrar teoría, método, resultados y amenazas | Separar hechos, deducciones e inferencias | `main.tex`, PDF | Todas las fuentes seleccionadas | IA propuesta para conversión LaTeX | **No realizada** | Resultado pendiente |

---

## 21. Instrucciones para la posterior redacción en LaTeX

1. Mantener la pregunta de investigación exactamente como aparece al inicio.
2. Utilizar una estructura: Introducción, Marco teórico, Estado del arte, Metodología, Hipótesis, Diseño experimental, Resultados, Discusión, Amenazas, Conclusiones, Referencias y Anexos.
3. No presentar las fórmulas de la sección 3 como resultados empíricos; etiquetarlas como deducciones teóricas del modelo.
4. No atribuir a Carter–Wegman resultados específicos de sondeo lineal.
5. No atribuir a Tarjan–Zwick una política hash `(γ,τ)`; usarlo como marco tiempo–espacio para arreglos.
6. En Resultados, reemplazar toda frase predictiva por números del CSV, intervalos y figuras reales.
7. Mantener visible la distinción entre costo amortizado, costo esperado y promedio empírico.
8. Explicar que el valor de `τ` es un umbral de política y `α` es la carga efectivamente observada.
9. Presentar línea base como convención, no como estándar óptimo.
10. Conservar limitaciones de Python, encadenamiento, claves enteras y ejecución monohilo.
11. Usar las claves BibTeX provistas; si el gestor bibliográfico modifica mayúsculas de títulos como “GPU”, protegerlas con llaves.
12. Antes de entregar, abrir cada DOI, comprobar autores/páginas y eliminar cualquier fuente que ya no pueda verificarse.

---

## 22. Referencias verificadas con enlaces directos

1. Carter, J. L., y Wegman, M. N. (1979). “Universal Classes of Hash Functions”. *Journal of Computer and System Sciences*, 18(2), 143–154. [DOI](https://doi.org/10.1016/0022-0000(79)90044-8).
2. Tarjan, R. E. (1985). “Amortized Computational Complexity”. *SIAM Journal on Algebraic and Discrete Methods*, 6(2), 306–318. [DOI](https://doi.org/10.1137/0606031).
3. Larson, P.-Å. (1988). “Dynamic Hash Tables”. *Communications of the ACM*, 31(4), 446–457. [DOI](https://doi.org/10.1145/42404.42410).
4. Dietzfelbinger, M., Karlin, A., Mehlhorn, K., Meyer auf der Heide, F., Rohnert, H., y Tarjan, R. E. (1994). “Dynamic Perfect Hashing: Upper and Lower Bounds”. *SIAM Journal on Computing*, 23(4), 738–761. [DOI](https://doi.org/10.1137/S0097539791194094).
5. Flajolet, P., Poblete, P., y Viola, A. (1998). “On the Analysis of Linear Probing Hashing”. *Algorithmica*, 22, 490–515. [DOI](https://doi.org/10.1007/PL00009236).
6. Brodnik, A., Carlsson, S., Demaine, E. D., Munro, J. I., y Sedgewick, R. (1999). “Resizable Arrays in Optimal Time and Space”. *WADS 1999*, LNCS 1663, 37–48. [DOI](https://doi.org/10.1007/3-540-48447-7_4).
7. Pagh, R., y Rodler, F. F. (2004). “Cuckoo Hashing”. *Journal of Algorithms*, 51(2), 122–144. [DOI](https://doi.org/10.1016/j.jalgor.2003.12.002).
8. Pătraşcu, M., y Thorup, M. (2012). “The Power of Simple Tabulation Hashing”. *Journal of the ACM*, 59(3), artículo 14, 1–50. [DOI](https://doi.org/10.1145/1993636.1993638).
9. Richter, S., Alvarez, V., y Dittrich, J. (2015). “A Seven-Dimensional Analysis of Hashing Methods and its Implications on Query Processing”. *PVLDB*, 9(3), 96–107. [DOI](https://doi.org/10.14778/2850583.2850585).
10. Li, Y., Zhu, Q., Lyu, Z., Huang, Z., y Sun, J. (2021). “DyCuckoo: Dynamic Hash Tables on GPUs”. *IEEE ICDE 2021*, 744–755. [DOI](https://doi.org/10.1109/ICDE51399.2021.00070).
11. Bender, M. A., Kuszmaul, B. C., y Kuszmaul, W. (2022). “Linear Probing Revisited: Tombstones Mark the Demise of Primary Clustering”. *IEEE FOCS 2021*, 1171–1182. [DOI](https://doi.org/10.1109/FOCS52979.2021.00115).
12. Bender, M. A., Conway, A., Farach-Colton, M., Kuszmaul, W., y Tagliavini, G. (2023). “Iceberg Hashing: Optimizing Many Hash-Table Criteria at Once”. *Journal of the ACM*, 70(6), artículo 40, 1–51. [DOI](https://doi.org/10.1145/3625817).
13. Böther, M., Benson, L., Klimovic, A., y Rabl, T. (2023). “Analyzing Vectorized Hash Tables Across CPU Architectures”. *PVLDB*, 16(11), 2755–2768. [DOI](https://doi.org/10.14778/3611479.3611485).
14. Tarjan, R. E., y Zwick, U. (2024). “Optimal Resizable Arrays”. *SIAM Journal on Computing*, 53(5), 1354–1380. [DOI](https://doi.org/10.1137/23M1575792).
15. Knuth, D. E. (1998). *The Art of Computer Programming, Volume 3: Sorting and Searching*, 2.ª ed. Addison-Wesley. ISBN 0-201-89685-0. [Página oficial](https://www-cs-faculty.stanford.edu/~knuth/taocp.html).

---

## 23. BibTeX depurado

```bibtex
@article{CarterWegman1979,
  author  = {Carter, J. Lawrence and Wegman, Mark N.},
  title   = {Universal Classes of Hash Functions},
  journal = {Journal of Computer and System Sciences},
  year    = {1979},
  volume  = {18},
  number  = {2},
  pages   = {143--154},
  doi     = {10.1016/0022-0000(79)90044-8},
  url     = {https://doi.org/10.1016/0022-0000(79)90044-8}
}

@article{Tarjan1985,
  author  = {Tarjan, Robert Endre},
  title   = {Amortized Computational Complexity},
  journal = {SIAM Journal on Algebraic and Discrete Methods},
  year    = {1985},
  volume  = {6},
  number  = {2},
  pages   = {306--318},
  doi     = {10.1137/0606031},
  url     = {https://doi.org/10.1137/0606031}
}

@article{Larson1988,
  author  = {Larson, Per-{\AA}ke},
  title   = {Dynamic Hash Tables},
  journal = {Communications of the ACM},
  year    = {1988},
  volume  = {31},
  number  = {4},
  pages   = {446--457},
  doi     = {10.1145/42404.42410},
  url     = {https://doi.org/10.1145/42404.42410}
}

@article{DietzfelbingerEtAl1994,
  author  = {Dietzfelbinger, Martin and Karlin, Anna and Mehlhorn, Kurt and Meyer auf der Heide, Friedhelm and Rohnert, Hans and Tarjan, Robert E.},
  title   = {Dynamic Perfect Hashing: Upper and Lower Bounds},
  journal = {SIAM Journal on Computing},
  year    = {1994},
  volume  = {23},
  number  = {4},
  pages   = {738--761},
  doi     = {10.1137/S0097539791194094},
  url     = {https://doi.org/10.1137/S0097539791194094}
}

@article{FlajoletPobleteViola1998,
  author  = {Flajolet, Philippe and Poblete, Patricio and Viola, Alfredo},
  title   = {On the Analysis of Linear Probing Hashing},
  journal = {Algorithmica},
  year    = {1998},
  volume  = {22},
  pages   = {490--515},
  doi     = {10.1007/PL00009236},
  url     = {https://doi.org/10.1007/PL00009236}
}

@inproceedings{BrodnikEtAl1999,
  author    = {Brodnik, Andrej and Carlsson, Svante and Demaine, Erik D. and Munro, J. Ian and Sedgewick, Robert},
  title     = {Resizable Arrays in Optimal Time and Space},
  booktitle = {Algorithms and Data Structures: 6th International Workshop, WADS 1999},
  series    = {Lecture Notes in Computer Science},
  volume    = {1663},
  year      = {1999},
  pages     = {37--48},
  publisher = {Springer},
  doi       = {10.1007/3-540-48447-7_4},
  url       = {https://doi.org/10.1007/3-540-48447-7_4}
}

@article{PaghRodler2004,
  author  = {Pagh, Rasmus and Rodler, Flemming Friche},
  title   = {Cuckoo Hashing},
  journal = {Journal of Algorithms},
  year    = {2004},
  volume  = {51},
  number  = {2},
  pages   = {122--144},
  doi     = {10.1016/j.jalgor.2003.12.002},
  url     = {https://doi.org/10.1016/j.jalgor.2003.12.002}
}

@article{PatrascuThorup2012,
  author  = {P{\u{a}}tra{\c{s}}cu, Mihai and Thorup, Mikkel},
  title   = {The Power of Simple Tabulation Hashing},
  journal = {Journal of the ACM},
  year    = {2012},
  volume  = {59},
  number  = {3},
  pages   = {14:1--14:50},
  articleno = {14},
  doi     = {10.1145/1993636.1993638},
  url     = {https://doi.org/10.1145/1993636.1993638}
}

@article{RichterAlvarezDittrich2015,
  author  = {Richter, Stefan and Alvarez, Victor and Dittrich, Jens},
  title   = {A Seven-Dimensional Analysis of Hashing Methods and its Implications on Query Processing},
  journal = {Proceedings of the VLDB Endowment},
  year    = {2015},
  volume  = {9},
  number  = {3},
  pages   = {96--107},
  doi     = {10.14778/2850583.2850585},
  url     = {https://doi.org/10.14778/2850583.2850585}
}

@inproceedings{LiEtAl2021,
  author    = {Li, Yuchen and Zhu, Qiwei and Lyu, Zheng and Huang, Zhongdong and Sun, Jianling},
  title     = {{DyCuckoo}: Dynamic Hash Tables on {GPUs}},
  booktitle = {2021 IEEE 37th International Conference on Data Engineering (ICDE)},
  year      = {2021},
  pages     = {744--755},
  publisher = {IEEE},
  doi       = {10.1109/ICDE51399.2021.00070},
  url       = {https://doi.org/10.1109/ICDE51399.2021.00070}
}

@inproceedings{BenderKuszmaulKuszmaul2022,
  author    = {Bender, Michael A. and Kuszmaul, Bradley C. and Kuszmaul, William},
  title     = {Linear Probing Revisited: Tombstones Mark the Demise of Primary Clustering},
  booktitle = {2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS)},
  year      = {2022},
  pages     = {1171--1182},
  publisher = {IEEE},
  doi       = {10.1109/FOCS52979.2021.00115},
  url       = {https://doi.org/10.1109/FOCS52979.2021.00115}
}

@article{BenderEtAl2023,
  author  = {Bender, Michael A. and Conway, Alex and Farach-Colton, Mart{\'{i}}n and Kuszmaul, William and Tagliavini, Guido},
  title   = {Iceberg Hashing: Optimizing Many Hash-Table Criteria at Once},
  journal = {Journal of the ACM},
  year    = {2023},
  volume  = {70},
  number  = {6},
  articleno = {40},
  pages   = {1--51},
  doi     = {10.1145/3625817},
  url     = {https://doi.org/10.1145/3625817}
}

@article{BoetherEtAl2023,
  author  = {B{\"o}ther, Maximilian and Benson, Lawrence and Klimovic, Ana and Rabl, Tilmann},
  title   = {Analyzing Vectorized Hash Tables Across CPU Architectures},
  journal = {Proceedings of the VLDB Endowment},
  year    = {2023},
  volume  = {16},
  number  = {11},
  pages   = {2755--2768},
  doi     = {10.14778/3611479.3611485},
  url     = {https://doi.org/10.14778/3611479.3611485}
}

@article{TarjanZwick2024,
  author  = {Tarjan, Robert E. and Zwick, Uri},
  title   = {Optimal Resizable Arrays},
  journal = {SIAM Journal on Computing},
  year    = {2024},
  volume  = {53},
  number  = {5},
  pages   = {1354--1380},
  doi     = {10.1137/23M1575792},
  url     = {https://doi.org/10.1137/23M1575792}
}

@book{Knuth1998,
  author    = {Knuth, Donald E.},
  title     = {The Art of Computer Programming, Volume 3: Sorting and Searching},
  edition   = {2},
  year      = {1998},
  publisher = {Addison-Wesley},
  isbn      = {0-201-89685-0},
  url       = {https://www-cs-faculty.stanford.edu/~knuth/taocp.html}
}
```

---

## 24. Lista de control antes de convertir a entrega final

- [ ] Confirmar con el docente si encadenamiento separado es el esquema esperado.
- [ ] Confirmar la definición exacta de familia universal vista en clase.
- [ ] Elegir `p` y demostrar que cubre el universo de claves.
- [ ] Congelar `γ`, `τ`, `m₀`, convención de resize y semillas antes de ejecutar.
- [ ] Ejecutar piloto y decidir réplicas con base en varianza, no conveniencia.
- [ ] Guardar código, commit, entorno, CSV crudo y gráficos.
- [ ] Verificar invariantes y contador de pares con tests.
- [ ] Reportar memoria estable y pico.
- [ ] Separar resultados de inserción-only y workload con borrados.
- [ ] No generalizar de Python a todas las arquitecturas.
- [ ] Sustituir todas las predicciones por evidencia real en la sección Resultados.
- [ ] Abrir y verificar nuevamente todos los DOI antes de entregar.
