"""Export a compact, data-derived LaTeX results section."""

from pathlib import Path
import pandas as pd


def _fmt(value: float, digits: int = 3) -> str:
    return f"{value:.{digits}f}"


def export_results(input_path: Path = Path("data/raw/results.csv"),
                   output_path: Path = Path("anexos/resultados_generados.tex")) -> None:
    data = pd.read_csv(input_path)
    maximum_n = int(data["n"].max())
    largest = data[data["n"] == maximum_n]
    grouped = largest.groupby(["gamma_nominal", "tau"], as_index=False).mean(numeric_only=True)
    by_gamma = largest.groupby("gamma_nominal", as_index=False).mean(numeric_only=True)
    by_tau = largest.groupby("tau", as_index=False).mean(numeric_only=True)
    min_migration = grouped.loc[grouped["migrations_per_insertion"].idxmin()]
    min_memory = grouped.loc[grouped["bytes_per_element"].idxmin()]
    min_collision = grouped.loc[grouped["pair_collisions_per_key"].idxmin()]
    gamma_corr = by_gamma["gamma_nominal"].corr(by_gamma["migrations_per_insertion"], method="spearman")
    tau_corr = by_tau["tau"].corr(by_tau["pair_collisions_per_key"], method="spearman")
    bound_mean = largest["bound_ratio"].mean()
    rows = []
    for row in by_gamma.itertuples():
        rows.append(
            f"{row.gamma_nominal:g} & {_fmt(row.migrations_per_insertion)} & "
            f"{_fmt(row.bytes_per_element,1)} & {_fmt(row.pair_collisions_per_key)} & "
            f"{_fmt(row.resize_count,1)} & {_fmt(row.time_per_operation_ns,1)} \\\\"
        )
    latex = rf"""
La corrida definitiva contiene \textbf{{{len(data)}}} unidades experimentales y
{data['repetition'].nunique()} repeticiones por celda. Para $N={maximum_n}$, la
correlación de rangos entre $\gamma$ y migraciones por inserción, promediando
$\tau$, fue {_fmt(gamma_corr)}; entre $\tau$ y colisiones por pares por clave,
promediando $\gamma$, fue {_fmt(tau_corr)}. El cociente medio entre pares
observados y la cota universal fue {_fmt(bound_mean)}. Estos valores describen
la muestra de semillas y no convierten una esperanza en cota determinista.

La menor migración media apareció en $(\gamma,\tau)=({min_migration.gamma_nominal:g},
{min_migration.tau:.2f})$; el menor uso estructural final en
({min_memory.gamma_nominal:g},{min_memory.tau:.2f}); y la menor tasa de pares en
({min_collision.gamma_nominal:g},{min_collision.tau:.2f}). Que estos puntos no
sean necesariamente el mismo tratamiento aporta evidencia empírica del
compromiso multiobjetivo.

\begin{{table}}[ht]
\centering\small
\caption{{Promedios por $\gamma$ para $N={maximum_n}$, agregados sobre $\tau$ y semillas.}}
\begin{{tabular}}{{rrrrrr}}
\toprule
$\gamma$ & migr./ins. & bytes/elem. & pares/clave & resizes & ns/oper. \\
\midrule
{chr(10).join(rows)}
\bottomrule
\end{{tabular}}
\end{{table}}
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(latex.strip() + "\n", encoding="utf-8")


if __name__ == "__main__":
    export_results()
