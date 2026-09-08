# TRABAJO FINAL DE INVESTIGACIÓN CIENTÍFICA

## Diseño y Análisis de Algoritmos Estudio teórico-experimental reproducible

El trabajo final deberá integrar el bloque final de Algorítmica II mediante una pregunta de investigación concreta, análisis teórico, revisión bibliográfica verificable, implementación en Python, experimentación reproducible, interpretación de resultados y defensa individual. El objetivo no es producir un informe enciclopédico, sino investigar un problema central sin perder la visión global de los contenidos del curso.

todos los temas deben comprenderse y relacionarse; los pertinentes se desarrollan en profundidad

Cada equipo trabajará un problema central. Todos los temas y subtemas del bloque final deberán aparecer en una Matriz Maestra de Cobertura Temática, indicando si aplican, aplican parcialmente o no aplican, siempre con justificación técnica. Al menos dos unidades temáticas del bloque final deberán incorporarse de manera sustantiva al estudio teórico o experimental. La matriz completa será obligatoria aunque algunos subtemas no formen parte del desarrollo principal del artículo.

## 1. Composición de los grupos y verificación individual

El trabajo podrá realizarse en grupos de hasta cinco integrantes. El tamaño del grupo no reduce la responsabilidad individual: cada estudiante deberá demostrar participación técnica verificable y comprensión global del estudio

Cada integrante podrá asumir una responsabilidad primaria (por ejemplo: estado del arte, modelación/análisis, implementación, experimentación o integración del artículo), pero esta asignación no limita lo que debe conocer. En la defensa, cualquier integrante podrá ser consultado sobre la pregunta de investigación, los algoritmos, la bibliografía, la metodología, los resultados, la Matriz Maestra y las conclusiones.

### Bitácora individual: instrumento imprescindible

La bitácora individual es obligatoria e imprescindible para verificar la autoría, la participación y el proceso de aprendizaje de cada estudiante. No podrá sustituirse por una declaración grupal, una lista final de tareas ni por la palabra de los compañeros.

Cada integrante mantendrá su propia bitácora durante todo el proyecto y la actualizará, como mínimo, en cada hito y cada vez que realice una contribución sustantiva.

La bitácora individual deberá registrar, de manera breve pero verificable:

- fecha e hito del proyecto;
- actividad realizada y decisión técnica adoptada;
- evidencia concreta de la contribución: archivo, sección, script, experimento, tabla, figura, commit o artefacto equivalente;
- fuente o paper consultado cuando corresponda;
- uso de LLM/IA, incluyendo propósito y prompt representativo cuando se haya utilizado;
- verificación o modificación realizada por el estudiante;
- resultado obtenido, problema encontrado o aprendizaje relevante.

#### Criterio de trazabilidad

La bitácora no se calificará por extensión. Se evaluará por coherencia, especificidad, trazabilidad y consistencia con el repositorio/archivos entregados, las evidencias experimentales y la defensa oral.

Cada estudiante deberá entregar su bitácora en formato PDF + fuente LaTeX. Se proporciona una plantilla específica. La ausencia o insuficiencia de la bitácora impedirá acreditar plenamente la contribución individual.

## 2. Alcance temático obligatorio y desglose completo

El trabajo deberá mantener el foco en todo el tramo final del sílabo. Esto no significa implementar cada técnica, sino estudiarla, ubicarla y justificar su pertinencia o no pertinencia respecto del problema investigado.

### Regla de cobertura

Todo subtema deberá quedar clasificado como A = aplica, P = aplica parcialmente/complementa o N = no aplica. Una marca N sin explicación técnica no recibirá crédito. En la defensa, cualquier integrante podrá ser interrogado sobre cualquier fila de la matriz, incluso si fue marcada N.

| Unidad | Subtema del sílabo | Evidencia mínima esperada |
|--------|-------------------|---------------------------|
| **Análisis amortizado** | Secuencias de operaciones | Distinguir costo de una operación aislada del costo de una secuencia; decidir si esta perspectiva es pertinente. |
| | Método agregado | Explicar o aplicar la suma del costo total de una secuencia y su cota amortizada; si no aplica, justificar. |
| | Método contable | Explicar cargos/créditos amortizados y condición de crédito suficiente; aplicar sólo si es pertinente. |
| | Método potencial | Explicar o proponer una función potencial válida cuando corresponda; justificar si no es apropiada. |
| | Arreglos dinámicos | Relacionar redimensionamiento y costo amortizado cuando la estructura estudiada lo permita. |
| | Contadores y operaciones sobre estructuras | Reconocer otras secuencias o estructuras donde una operación costosa ocasional pueda amortizarse. |
| **Probabilidad y esperanza** | Probabilidad básica | Identificar eventos y probabilidades relevantes en algoritmos o experimentos aleatorizados. |
| | Esperanza matemática | Distinguir y, cuando corresponda, calcular costo/valor esperado. |
| | Variables indicadoras | Reconocer su utilidad para expresar conteos y esperanzas por linealidad. |
| | Amortizado vs. esperado | Explicar con precisión por qué el análisis amortizado no requiere una distribución probabilística. |
| **Algoritmos aleatorizados** | Las Vegas | Identificar que siempre entrega una respuesta correcta pero con tiempo aleatorio; analizar si es aplicable. |
| | Monte Carlo | Identificar tiempo acotado/decidido y posibilidad de error; analizar si es aplicable. |
| | Probabilidad de error | Explicar cómo se mide y, si corresponde, cómo disminuye mediante repetición. |
| | Garantías de ejecución | Comparar garantía de corrección, tiempo esperado y probabilidad de fallo según el enfoque. |
| | Selección aleatoria | Relacionar pivotes/muestras/decisiones aleatorias con el comportamiento esperado cuando corresponda. |
| | Hashing universal | Reconocer aleatorización de la familia hash, colisiones esperadas y condiciones de uso. |
| **P, NP y verificadores** | Problemas de decisión | Formular la versión de decisión del problema cuando corresponda. |
| | Certificados | Identificar qué información permitiría demostrar una respuesta "sí". |
| | Verificadores | Explicar un verificador polinomial y su relación con el certificado. |
| | Clase P | Determinar si existe un algoritmo polinomial conocido para la versión de decisión estudiada. |
| | Clase NP | Justificar pertenencia mediante certificado/verificación cuando corresponda. |
| | Decisión vs. optimización | Distinguir formalmente ambas formulaciones y explicar su relación. |
| **Reducciones y NP-completitud** | Reducciones polinomiales | Explicar qué preserva una reducción y cómo se utiliza para comparar dificultad. |
| | Dirección de una reducción | Justificar la dirección correcta; evitar usar una reducción en sentido inverso sin demostración. |
| | Estructura de prueba de NP-completitud | Identificar: pertenencia a NP + reducción desde un problema NP-completo conocido. |
| | SAT / 3-SAT | Reconocer su papel como problemas base clásicos y su uso en cadenas de reducciones. |
| | Clique | Explicar formulación y relación con otros problemas clásicos cuando sea pertinente. |
| | Conjunto independiente | Explicar formulación y relaciones conocidas con clique/cobertura cuando sea pertinente. |
| | Cobertura de vértices | Explicar formulación y su doble papel como problema NP-difícil y caso de aproximación. |
| | Ciclo hamiltoniano | Reconocer la formulación de decisión y su diferencia con recorridos/caminos polinomiales. |
| | Errores frecuentes en reducciones | Identificar al menos un error de dirección, equivalencia o transformación que invalidaría una prueba. |
| | Consecuencias prácticas de NP-completitud | Explicar qué implica y qué no implica para el diseño de algoritmos y el tamaño de instancia. |
| **Aproximación** | Algoritmos de aproximación | Distinguirlos de heurísticas y reconocer que producen soluciones factibles con garantía demostrable. |
| | Razón de aproximación | Definir e interpretar la relación entre valor obtenido y óptimo según minimización/maximización. |
| | Análisis de garantías | Explicar la garantía teórica y las condiciones bajo las cuales se sostiene. |

Los algoritmos de bloques anteriores (programación dinámica, conjuntos disjuntos, MST, caminos mínimos, flujo, emparejamiento, etc.) pueden utilizarse como línea base, componente o contexto, pero no sustituyen la cobertura del bloque final.

## 3. Naturaleza científica del trabajo

El artículo deberá responder una pregunta investigable y contrastable. La estructura conceptual recomendada es:

**problema → pregunta → hipótesis/expectativa → método → resultados → discusión**

### Ejemplos de preguntas válidas:

- ¿Cómo cambia el costo amortizado, tiempo real y memoria al variar el factor de crecimiento de un arreglo dinámico?
- ¿Cómo se comporta una estrategia aleatorizada frente a una determinista bajo diferentes distribuciones de entrada?
- ¿Qué relación existe entre el tamaño de una instancia NP-difícil, el tiempo de una solución exacta y la calidad de una aproximación?
- ¿Qué diferencia experimental existe entre una garantía amortizada y una garantía esperada?
- ¿Cómo se comporta una heurística frente a un algoritmo con razón de aproximación conocida?

### No se aceptará

Un trabajo que sólo describa algoritmos, copie teoría, implemente código sin pregunta de investigación o presente gráficos sin explicar la metodología y el significado de los resultados.

## 4. Bibliografía científica obligatoria

Una investigación científica requiere antecedentes verificables. Los LLM pueden ayudar a buscar y comprender, pero no son fuentes científicas.

El artículo deberá utilizar al menos 8 fuentes académicas verificables, con la siguiente composición mínima:

- **5 artículos científicos o papers revisados por pares.** En Ciencias de la Computación se aceptan artículos de revista y proceedings de conferencias con revisión por pares.
- **2 fuentes recientes** publicadas en los últimos cinco años, cuando el tema disponga de literatura reciente pertinente.
- **1 fuente fundacional o de referencia:** artículo clásico, trabajo original, libro académico reconocido o fuente primaria del algoritmo/problema.

Pueden utilizarse como apoyo adicional libros, documentación oficial, tesis, arXiv, blogs técnicos o videos, pero estas fuentes no reemplazan el mínimo de papers revisados por pares. Un preprint de arXiv sólo contará como paper revisado por pares si se identifica además su versión publicada en una revista o conferencia con revisión. Se recomienda buscar en Google Scholar, ACM Digital Library, IEEE Xplore, SpringerLink, ScienceDirect y bases equivalentes disponibles para los estudiantes.

### Reglas de trazabilidad

1. Toda referencia incluida en la bibliografía deberá haber sido abierta y consultada por el equipo.
2. Toda afirmación técnica relevante deberá estar respaldada por una fuente o por una derivación/experimento propio claramente explicado.
3. Las referencias sugeridas por IA deberán verificarse manualmente antes de incorporarse.
4. No se aceptarán referencias inexistentes, datos bibliográficos inventados ni atribuciones a una fuente que no contenga la afirmación citada.
5. Siempre que sea posible, el registro bibliográfico deberá incluir DOI, ISBN o enlace estable al editor/venue.

## 5. Evidencias bibliográficas obligatorias

Además de la sección de referencias, el equipo entregará en anexos:

### A. Matriz bibliográfica

Para cada fuente académica:

| Referencia | Problema/objetivo | Método | Resultado relevante | Uso en nuestro estudio |
|------------|-------------------|--------|--------------------|------------------------|
| Autor, año | | | | |

Debe incluir además una limitación, supuesto o amenaza identificada en cada uno de los tres papers principales.

### B. Registro de búsqueda

Registrar al menos las búsquedas principales realizadas:

| Base/portal | Fecha | Consulta/palabras clave | Filtros | Resultado/selección |
|-------------|-------|------------------------|---------|---------------------|
| ACM/IEEE/etc. | | | | |

El equipo identificará tres fuentes como papers núcleo. En la defensa el docente podrá seleccionar cualquiera de ellas y solicitar:

- problema investigado;
- método utilizado;
- resultado principal;
- limitación relevante;
- relación concreta con el artículo del equipo.

## 6. Uso permitido de LLM e IA generativa

**LLM ayuda a investigar ≠ LLM reemplaza la investigación**

Se permite utilizar LLM para:

- generar términos de búsqueda y palabras clave;
- aclarar conceptos;
- revisar pseudocódigo o sintaxis;
- proponer casos de prueba;
- apoyar depuración;
- sugerir formas de visualizar resultados;
- revisar redacción;
- preparar la defensa.

No se permite:

- citar un LLM como fuente científica;
- incorporar referencias sugeridas por IA sin verificarlas;
- presentar un estado del arte generado por IA sin consultar las fuentes originales;
- incluir demostraciones, código o análisis que el estudiante no pueda explicar, verificar o modificar;
- atribuir a un paper una afirmación que no aparece en él.

El artículo incluirá una sección titulada **Declaración de uso de IA**, indicando como mínimo: herramienta, propósito, prompt representativo, fragmento aprovechado, modificación/verificación realizada y responsabilidad final del equipo.

## 7. Metodología e implementación

La implementación principal deberá realizarse en Python. El equipo deberá definir:

- **variables independientes** (por ejemplo: tamaño, densidad, distribución, factor de crecimiento, número de repeticiones);
- **variables dependientes** (tiempo, memoria, costo, calidad, error, colisiones, número de operaciones, etc.);
- **línea base o algoritmo de comparación;**
- **casos normales, límite y adversos;**
- **procedimiento reproducible** para generar o seleccionar instancias;
- **entorno de ejecución** y versiones relevantes;
- **criterio para aceptar o rechazar** la hipótesis/expectativa.

El estudio deberá utilizar múltiples tamaños de instancia. Cuando exista aleatoriedad, deberán realizarse suficientes repeticiones independientes para interpretar la variabilidad (se recomienda alrededor de 30 por configuración, salvo justificación técnica de otro número).

## 8. Resultados y discusión

No basta con mostrar tablas o gráficos. Cada resultado debe responder:

1. ¿Qué observamos?
2. ¿Coincide con la teoría?
3. ¿Qué explica la diferencia entre teoría y medición?
4. ¿Qué limitaciones tiene el experimento?
5. ¿Qué conclusión puede sostenerse y cuál no?

Cuando corresponda, reportar media, mediana y alguna medida de dispersión básica; no se exige estadística avanzada, pero sí una interpretación honesta de la variabilidad.

## 9. Matriz Maestra de Cobertura Temática

El artículo deberá incorporar en anexos la Matriz Maestra de Cobertura Temática completa, con una fila por cada subtema del desglose anterior. No se permite condensar varias filas en una sola respuesta genérica.

Cada fila tendrá como mínimo:

| Unidad | Subtema | A/P/N | Justificación técnica | Evidencia/sección |
|--------|---------|-------|----------------------|-------------------|
| Ejemplo | Método potencial | P | Se utiliza para contrastar el costo amortizado, pero no forma parte del algoritmo implementado. | Sec. 4.3 |

### Interpretación de estados:

- **A - Aplica:** el subtema forma parte sustantiva del análisis, implementación o experimento.
- **P - Aplica parcialmente:** aporta como contraste, fundamento, alternativa o explicación complementaria.
- **N - No aplica:** no es pertinente al problema o diseño elegido, y se explica técnicamente por qué.

La matriz no reemplaza el desarrollo científico del artículo; funciona como evidencia de cobertura y preparación integral. Una marca N sin argumento técnico no recibirá crédito.

## 10. Formato obligatorio del artículo

El artículo final deberá estar escrito y compilado en LaTeX. Se permite trabajar en Overleaf o en un entorno local. No se aceptará como entrega final un documento originado en Word/Google Docs y convertido posteriormente a PDF.

Extensión sugerida: **8 a 12 páginas** de contenido principal, sin contar referencias y anexos.

### Estructura mínima:

1. Título y autores.
2. Resumen y palabras clave.
3. Introducción.
4. Pregunta de investigación e hipótesis/expectativa.
5. Estado del arte / trabajos relacionados.
6. Fundamento teórico y algoritmos.
7. Integración del bloque final y referencia a la Matriz Maestra de Cobertura Temática.
8. Metodología y diseño experimental.
9. Resultados.
10. Discusión.
11. Limitaciones y amenazas a la validez.
12. Conclusiones y trabajo futuro.
13. Declaración de uso de IA.
14. Referencias bibliográficas.
15. Anexos: Matriz Maestra de Cobertura Temática, matriz bibliográfica, registro de búsqueda y material complementario.

Las referencias deberán gestionarse mediante un archivo `.bib` y citarse desde LaTeX. Se recomienda BibLaTeX/Biber o BibTeX.

## 11. Paquete de entrega

El equipo entregará un único archivo comprimido con esta estructura mínima:

```
ApellidoGrupo_TrabajoFinal.zip
|-- articulo.pdf
|-- main.tex
|-- referencias.bib
|-- figuras/
|-- src/               # codigo Python
|-- data/              # datos o generadores
|-- results/           # resultados reproducibles
|-- README.md          # instrucciones para reproducir
|-- bitacoras/
|   |-- Apellido1_Nombre_bitacora.pdf
|   |-- Apellido1_Nombre_bitacora.tex
|   |-- ... una bitacora por integrante ...
`-- anexos/            # material complementario
```

El PDF y las fuentes LaTeX son ambos obligatorios. También son obligatorias las bitácoras individuales en PDF y LaTeX. La ausencia del código o de instrucciones suficientes para reproducir el experimento afectará la evaluación de reproducibilidad; la ausencia de una bitácora afectará directamente la acreditación individual de ese integrante.

## 12. Hitos de seguimiento

Las fechas específicas serán definidas por el docente. Se prevén los siguientes hitos:

1. **Protocolo de investigación:** problema, pregunta, hipótesis/expectativa, dos algoritmos o enfoques a contrastar, cinco fuentes preliminares, Matriz Maestra de Cobertura Temática inicial y plan experimental. Cada integrante presenta su primera entrada de bitácora.

2. **Revisión bibliográfica:** mínimo ocho fuentes verificadas, matriz bibliográfica y registro de búsqueda. Cada integrante actualiza su bitácora con fuentes revisadas y aportes realizados.

3. **Avance experimental:** implementación funcional, casos de prueba y primeros resultados. La bitácora deberá identificar scripts, experimentos, resultados o decisiones atribuibles a cada integrante.

4. **Artículo final:** PDF compilado en LaTeX, fuentes, código, datos/resultados, anexos y bitácoras individuales completas.

5. **Defensa individual:** explicación, interpretación y posible modificación breve, contrastada con la bitácora y las evidencias técnicas.

## 13. Defensa individual

Aunque el artículo sea elaborado en equipo, la validación del aprendizaje será individual. La defensa se contrastará con la bitácora individual y con evidencias técnicas concretas. El docente podrá solicitar:

- explicar una fuente bibliográfica seleccionada al azar;
- identificar y demostrar una contribución registrada en su bitácora;
- explicar una evidencia técnica propia (archivo, script, experimento, tabla, figura, commit o sección);
- justificar una decisión algorítmica;
- explicar una demostración o garantía;
- interpretar una tabla o gráfico;
- explicar por qué cualquier subtema de la Matriz Maestra aplica, aplica parcialmente o no aplica;
- modificar una parte breve del código o experimento;
- diferenciar amortizado de esperado, Las Vegas de Monte Carlo, P de NP, decisión de optimización, reducción de equivalencia, y heurística de aproximación; además, explicar cualquiera de los problemas clásicos incluidos en el desglose.

## 14. Rúbrica de evaluación y calificación individual

| Criterio | Puntos |
|----------|--------|
| Problema, pregunta de investigación e hipótesis/expectativa | 8 |
| Bibliografía científica, estado del arte y trazabilidad de fuentes | 15 |
| Cobertura integral y Matriz Maestra del bloque final | 15 |
| Profundización algorítmica y calidad del modelo/implementación | 12 |
| Corrección, complejidad y garantías teóricas | 10 |
| Diseño experimental y reproducibilidad | 15 |
| Resultados, discusión y limitaciones | 10 |
| Redacción científica, LaTeX, figuras y referencias | 5 |
| **Puntaje grupal base G** | **90** |
| **Defensa individual Dᵢ** | **10** |

La calificación final de cada integrante se obtendrá mediante:

```
Nᵢ = G · Cᵢ + Dᵢ
```

donde Cᵢ es un coeficiente individual de trazabilidad y contribución determinado a partir de la bitácora, la evidencia técnica y la coherencia con la defensa.

| Coeficiente | Descripción |
|-------------|-------------|
| 1.00 | Bitácora completa y consistente; contribuciones sustantivas verificables; dominio coherente en la defensa. |
| 0.90 | Participación sustantiva verificable, con vacíos menores de trazabilidad o consistencia. |
| 0.80 | Evidencia parcial; existen aportes reales, pero hay vacíos materiales en bitácora, trazabilidad o dominio. |
| 0.70 | Participación insuficientemente documentada o difícil de atribuir individualmente. |
| < 0.70 | Podrá asignarse cuando la evidencia individual sea mínima, contradictoria o no permita acreditar una participación suficiente. |

### Carácter imprescindible de la bitácora

Un integrante que no entregue su bitácora individual no podrá acreditar plenamente su participación; en tal caso, Cᵢ no podrá ser superior a 0.70, sin perjuicio de una reducción adicional si la defensa y la evidencia técnica muestran una contribución menor.

### Integridad científica

Las referencias que no puedan verificarse no contarán como evidencia bibliográfica. La fabricación de referencias, resultados, datos o atribuciones será tratada conforme a las reglas de honestidad académica de la materia y de la Universidad.

## 15. Lista de cotejo antes de entregar

- [ ] El grupo tiene como máximo cinco integrantes.
- [ ] Cada integrante entregó su bitácora individual en PDF y LaTeX.
- [ ] Cada bitácora contiene evidencias concretas y es consistente con los archivos, resultados y defensa.
- [ ] La pregunta de investigación es concreta y respondible.
- [ ] El trabajo no es sólo descriptivo; existe comparación o contraste.
- [ ] Se incluyeron al menos 8 fuentes académicas y 5 papers revisados por pares.
- [ ] Todas las referencias fueron consultadas y citadas correctamente.
- [ ] Los tres papers núcleo pueden ser defendidos oralmente.
- [ ] La Matriz Maestra contiene una fila por cada subtema del desglose completo.
- [ ] Al menos dos unidades temáticas del bloque final se desarrollan sustantivamente, sin omitir la preparación del resto de subtemas para la defensa.
- [ ] La implementación principal está en Python.
- [ ] El experimento es reproducible y utiliza varias instancias/tamaños.
- [ ] Los resultados se interpretan y se discuten limitaciones.
- [ ] Se incluye declaración de uso de IA.
- [ ] El artículo fue escrito y compilado en LaTeX.
- [ ] Se entregan PDF, .tex, .bib, código, datos/resultados y README.

---

El trabajo final será considerado exitoso cuando el equipo pueda sostener con evidencia:

**qué pregunta investigó, qué predijo la teoría, qué mostró el experimento y qué puede concluirse**