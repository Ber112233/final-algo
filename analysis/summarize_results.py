"""Statistical summaries with deterministic bootstrap confidence intervals."""

from pathlib import Path
import numpy as np
import pandas as pd

DEFAULT_INPUT = Path("data/raw/results.csv")
DEFAULT_OUTPUT = Path("data/processed/summary.csv")
GROUP_COLUMNS = ["n", "gamma_nominal", "tau", "key_family"]
METRICS = [
    "elapsed_ns", "time_per_operation_ns", "migrations_per_insertion",
    "pair_collisions_per_key", "key_comparisons", "bytes_per_element",
    "tracemalloc_peak_bytes", "resize_count", "max_chain_length", "bound_ratio",
]


def _bootstrap_ci(values: np.ndarray, seed: int, samples: int = 1000) -> tuple[float, float]:
    if len(values) < 2:
        value = float(values[0]) if len(values) else 0.0
        return value, value
    rng = np.random.default_rng(seed)
    means = rng.choice(values, size=(samples, len(values)), replace=True).mean(axis=1)
    low, high = np.percentile(means, [2.5, 97.5])
    return float(low), float(high)


def summarize_results(input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT) -> pd.DataFrame:
    data = pd.read_csv(input_path)
    missing = set(GROUP_COLUMNS + METRICS) - set(data.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    rows: list[dict[str, object]] = []
    for group_index, (group_values, group) in enumerate(data.groupby(GROUP_COLUMNS, sort=True)):
        row = dict(zip(GROUP_COLUMNS, group_values))
        row["repetitions"] = len(group)
        for metric_index, metric in enumerate(METRICS):
            values = group[metric].to_numpy(dtype=float)
            low, high = _bootstrap_ci(values, seed=20260908 + 100 * group_index + metric_index)
            row.update({
                f"{metric}_mean": float(np.mean(values)),
                f"{metric}_median": float(np.median(values)),
                f"{metric}_std": float(np.std(values, ddof=1)) if len(values) > 1 else 0.0,
                f"{metric}_ci95_low": low,
                f"{metric}_ci95_high": high,
            })
        rows.append(row)
    summary = pd.DataFrame(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)
    return summary
