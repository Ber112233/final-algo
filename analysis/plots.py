"""Generate the eight figures specified by the research protocol."""

from pathlib import Path
import os
os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DEFAULT_INPUT = Path("data/raw/results.csv")
DEFAULT_RESIZES = Path("data/raw/resize_events.csv")
DEFAULT_FIGURES = Path("figuras/final")


def _heatmap(data: pd.DataFrame, metric: str, title: str, path: Path) -> None:
    largest = data[data["n"] == data["n"].max()]
    pivot = largest.pivot_table(index="tau", columns="gamma_nominal", values=metric, aggfunc="mean")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    image = ax.imshow(pivot.values, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(pivot.columns)), [f"{v:g}" for v in pivot.columns])
    ax.set_yticks(range(len(pivot.index)), [f"{v:.2f}" for v in pivot.index])
    ax.set(xlabel=r"Factor de crecimiento $\gamma$", ylabel=r"Umbral $\tau$", title=title)
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            ax.text(j, i, f"{pivot.values[i, j]:.2f}", ha="center", va="center", color="white", fontsize=8)
    fig.colorbar(image, ax=ax)
    fig.tight_layout(); fig.savefig(path, dpi=180); plt.close(fig)


def generate_plots(input_path: Path = DEFAULT_INPUT, figures_dir: Path = DEFAULT_FIGURES,
                   resize_path: Path = DEFAULT_RESIZES) -> list[Path]:
    data = pd.read_csv(input_path)
    figures_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for number, metric, title, filename in [
        (1, "migrations_per_insertion", "Migraciones por inserción", "01_heatmap_migrations.png"),
        (2, "bytes_per_element", "Bytes estructurales por elemento", "02_heatmap_memory.png"),
        (3, "pair_collisions_per_key", "Colisiones por pares por clave", "03_heatmap_pair_collisions.png"),
    ]:
        path = figures_dir / filename; _heatmap(data, metric, title, path); created.append(path)

    if resize_path.exists() and resize_path.stat().st_size:
        events = pd.read_csv(resize_path)
        run_id = events["run_id"].iloc[0]
        sample = events[events["run_id"] == run_id]
        fig, ax = plt.subplots(figsize=(7, 4.5))
        ax.plot(sample["resize_number"], sample["alpha_pre"], marker="o", label=r"$\alpha_{pre}$")
        ax.plot(sample["resize_number"], sample["alpha_post"], marker="o", label=r"$\alpha_{post}$")
        ax.set(xlabel="Número de resize", ylabel="Factor de carga", title="Trayectoria de carga alrededor de los resizes")
        ax.grid(alpha=.25); ax.legend(); fig.tight_layout()
        path = figures_dir / "04_resize_trajectory.png"; fig.savefig(path, dpi=180); plt.close(fig); created.append(path)

    grouped = data.groupby(["n", "gamma_nominal", "tau"], as_index=False).mean(numeric_only=True)
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.scatter(grouped["universal_pair_bound"], grouped["pair_collisions"], alpha=.75)
    limit = max(grouped["universal_pair_bound"].max(), grouped["pair_collisions"].max())
    ax.plot([0, limit], [0, limit], "--", color="black", label="igualdad con la cota")
    ax.set(xlabel=r"Cota $n(n-1)/(2m)$", ylabel="Colisiones por pares observadas", title="Observado frente a cota universal")
    ax.legend(); ax.grid(alpha=.25); fig.tight_layout()
    path = figures_dir / "05_observed_vs_bound.png"; fig.savefig(path, dpi=180); plt.close(fig); created.append(path)

    predicted = np.log(grouped["n"] / (grouped["tau"] * grouped["m0"])) / np.log(grouped["gamma_nominal"])
    fig, ax = plt.subplots(figsize=(6, 5)); ax.scatter(predicted, grouped["resize_count"], alpha=.75)
    ax.set(xlabel=r"$\log_\gamma(N/(\tau m_0))$", ylabel="Resizes observados", title="Frecuencia de redimensionamiento")
    ax.grid(alpha=.25); fig.tight_layout(); path = figures_dir / "06_resize_prediction.png"
    fig.savefig(path, dpi=180); plt.close(fig); created.append(path)

    largest = grouped[grouped["n"] == grouped["n"].max()]
    fig, ax = plt.subplots(figsize=(7, 5))
    scatter = ax.scatter(largest["migrations_per_insertion"], largest["bytes_per_element"],
                         c=largest["pair_collisions_per_key"], s=80, cmap="plasma")
    ax.set(xlabel="Migraciones por inserción", ylabel="Bytes por elemento", title="Frontera multiobjetivo (color: colisiones/clave)")
    fig.colorbar(scatter, ax=ax, label="Colisiones por pares por clave"); ax.grid(alpha=.25); fig.tight_layout()
    path = figures_dir / "07_pareto.png"; fig.savefig(path, dpi=180); plt.close(fig); created.append(path)

    fig, ax = plt.subplots(figsize=(9, 4.8))
    labels, values = [], []
    for (gamma, tau), group in data[data["n"] == data["n"].max()].groupby(["gamma_nominal", "tau"]):
        labels.append(f"{gamma:g}/{tau:.2f}"); values.append(group["pair_collisions_per_key"].to_numpy())
    ax.boxplot(values, tick_labels=labels, showfliers=False); ax.tick_params(axis="x", rotation=60)
    ax.set(xlabel=r"$\gamma/\tau$", ylabel="Colisiones por pares por clave", title="Variabilidad entre semillas")
    ax.grid(axis="y", alpha=.25); fig.tight_layout(); path = figures_dir / "08_seed_boxplots.png"
    fig.savefig(path, dpi=180); plt.close(fig); created.append(path)
    return created
