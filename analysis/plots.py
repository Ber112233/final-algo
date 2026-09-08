"""Generate non-interactive figures from raw experiment results."""

from pathlib import Path
import os

os.environ.setdefault("MPLCONFIGDIR", str(Path(".matplotlib-cache").resolve()))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


DEFAULT_INPUT = Path("results/raw/results.csv")
DEFAULT_FIGURES = Path("figures")


LINE_PLOTS = [
    ("amortized_cost", "Costo amortizado", "01_amortized_cost.png"),
    ("collisions", "Colisiones promedio", "02_collisions.png"),
    ("collisions_per_operation", "Colisiones por operación", "03_collisions_per_operation.png"),
    ("estimated_memory", "Memoria estimada (bytes)", "04_estimated_memory.png"),
    ("unused_capacity", "Capacidad sin utilizar", "05_unused_capacity.png"),
    ("rehashes", "Número de rehashes", "06_rehashes.png"),
    ("rehash_operations", "Elementos movidos", "07_rehash_operations.png"),
    ("time_per_operation", "Tiempo por operación (s)", "08_time_per_operation.png"),
]


def _save_line_plot(data: pd.DataFrame, metric: str, label: str, path: Path) -> None:
    thresholds = sorted(data["load_threshold"].unique())
    figure, axes = plt.subplots(1, len(thresholds), figsize=(5 * len(thresholds), 4), squeeze=False)
    for axis, threshold in zip(axes[0], thresholds):
        subset = data[data["load_threshold"] == threshold]
        for growth, group in subset.groupby("growth_factor"):
            means = group.groupby("n", as_index=False)[metric].mean()
            axis.plot(means["n"], means[metric], marker="o", label=f"growth={growth:g}")
        axis.set_title(f"threshold={threshold:.2f}")
        axis.set_xlabel("n")
        axis.set_ylabel(label)
        axis.grid(alpha=0.25)
        axis.legend()
    figure.tight_layout()
    figure.savefig(path, dpi=160)
    plt.close(figure)


def generate_plots(
    input_path: Path = DEFAULT_INPUT, figures_dir: Path = DEFAULT_FIGURES
) -> list[Path]:
    data = pd.read_csv(input_path)
    figures_dir.mkdir(parents=True, exist_ok=True)
    created: list[Path] = []
    for input_type, input_data in data.groupby("input_type"):
        suffix = str(input_type).replace(" ", "_")
        for metric, label, filename in LINE_PLOTS:
            path = figures_dir / filename.replace(".png", f"_{suffix}.png")
            _save_line_plot(input_data, metric, label, path)
            created.append(path)

        largest_n = int(input_data["n"].max())
        largest = input_data[input_data["n"] == largest_n]
        grouped = largest.groupby(["growth_factor", "load_threshold"], as_index=False).mean(numeric_only=True)

        figure, axis = plt.subplots(figsize=(7, 5))
        for _, row in grouped.iterrows():
            label = f"g={row['growth_factor']:g}, t={row['load_threshold']:.2f}"
            axis.scatter(row["estimated_memory"], row["amortized_cost"], s=55, label=label)
        axis.set(xlabel="Memoria estimada (bytes)", ylabel="Costo amortizado", title=f"Trade-off para n={largest_n}")
        axis.grid(alpha=0.25)
        axis.legend(fontsize=7, ncol=2)
        figure.tight_layout()
        path = figures_dir / f"09_memory_cost_tradeoff_{suffix}.png"
        figure.savefig(path, dpi=160)
        plt.close(figure)
        created.append(path)

        labels = [f"{row.growth_factor:g}/{row.load_threshold:.2f}" for row in grouped.itertuples()]
        figure, axis = plt.subplots(figsize=(9, 4))
        axis.bar(labels, grouped["utilization"])
        axis.set(xlabel="growth/threshold", ylabel="Utilización", title=f"Utilización para n={largest_n}")
        axis.tick_params(axis="x", rotation=45)
        axis.set_ylim(0, 1)
        figure.tight_layout()
        path = figures_dir / f"10_utilization_{suffix}.png"
        figure.savefig(path, dpi=160)
        plt.close(figure)
        created.append(path)

    threshold_path = input_path.parent / "threshold_experiment.csv"
    if threshold_path.exists():
        threshold_data = pd.read_csv(threshold_path)
        figure, axis = plt.subplots(figsize=(8, 4))
        axis.plot(threshold_data["operation_number"], threshold_data["individual_operation_cost"], marker="o")
        axis.set(xlabel="Número de inserción", ylabel="Costo individual", title="Costo alrededor del resize")
        axis.grid(alpha=0.25)
        figure.tight_layout()
        path = figures_dir / "threshold_operation_cost.png"
        figure.savefig(path, dpi=160)
        plt.close(figure)
        created.append(path)

    collision_path = input_path.parent / "collision_experiment.csv"
    if collision_path.exists():
        collision_data = pd.read_csv(collision_path).groupby("alpha", as_index=False)["collisions"].mean()
        figure, axis = plt.subplots(figsize=(7, 4))
        axis.plot(collision_data["alpha"], collision_data["collisions"], marker="o")
        axis.set(xlabel="Factor de carga", ylabel="Colisiones promedio", title="Colisiones vs factor de carga")
        axis.grid(alpha=0.25)
        figure.tight_layout()
        path = figures_dir / "collision_load_factor.png"
        figure.savefig(path, dpi=160)
        plt.close(figure)
        created.append(path)
    return created
