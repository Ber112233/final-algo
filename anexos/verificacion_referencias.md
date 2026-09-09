# Verificación automatizada de metadatos DOI

Fecha: 2026-09-08. Método: consulta de los 14 DOI mediante el registro Crossref y contraste de título, año, venue y páginas. Esta comprobación detecta referencias inexistentes o metadatos cruzados, pero no sustituye la lectura humana del paper.

| DOI | Resultado |
|---|---|
| 10.1016/0022-0000(79)90044-8 | Coincide: Carter–Wegman, JCSS 1979, 143–154 |
| 10.1137/0606031 | Coincide: Tarjan, SIAM 1985, 306–318 |
| 10.1145/42404.42410 | Coincide: Larson, CACM 1988, 446–457 |
| 10.1137/S0097539791194094 | Coincide: Dynamic Perfect Hashing, 1994, 738–761 |
| 10.1007/PL00009236 | Coincide: Linear Probing Hashing, 1998, 490–515 |
| 10.1007/3-540-48447-7_4 | Coincide: Resizable Arrays, WADS 1999, 37–48 |
| 10.1016/j.jalgor.2003.12.002 | Coincide: Cuckoo Hashing, 2004, 122–144 |
| 10.1145/2220357.2220361 | Coincide: Simple Tabulation, JACM 2012, 1–50 |
| 10.14778/2850583.2850585 | Coincide: Seven-Dimensional Analysis, PVLDB 2015, 96–107 |
| 10.1109/ICDE51399.2021.00070 | Coincide: DyCuckoo, ICDE 2021, 744–755 |
| 10.1109/FOCS52979.2021.00115 | Coincide: Linear Probing Revisited, publicación 2022, 1171–1182 |
| 10.1145/3625817 | Coincide: Iceberg Hashing, JACM 2023, 1–51 |
| 10.14778/3611479.3611485 | Coincide: Vectorized Hash Tables, PVLDB 2023, 2755–2768 |
| 10.1137/23M1575792 | Coincide: Optimal Resizable Arrays, SIAM 2024, 1354–1380 |

## Corrección aplicada

`investigacion_hashing_dinamico.md` asociaba la versión JACM 2012 de *The Power of Simple Tabulation Hashing* con `10.1145/1993636.1993638`; ese DOI corresponde a la versión STOC 2011 de 1–10 páginas. Para mantener la referencia JACM 59(3), se corrigió `referencias.bib` a `10.1145/2220357.2220361`.

## Verificación estudiantil pendiente

Cada integrante debe abrir las fuentes que utilice, confirmar que contienen la afirmación atribuida y registrarlo en su bitácora. Crossref y Codex no reemplazan ese paso.
