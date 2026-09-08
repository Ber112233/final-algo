"""Aggregate raw experimental executions without modifying the source CSV."""

from pathlib import Path

import pandas as pd


DEFAULT_INPUT = Path("results/raw/results.csv")
DEFAULT_OUTPUT = Path("results/summary/summary.csv")
GROUP_COLUMNS = ["n", "growth_factor", "load_threshold", "input_type"]
METRICS = [
    "elapsed_time",
    "time_per_operation",
    "collisions",
    "rehashes",
    "rehash_operations",
    "final_capacity",
    "unused_capacity",
    "utilization",
    "estimated_memory",
    "total_operation_cost",
    "amortized_cost",
]


def summarize_results(
    input_path: Path = DEFAULT_INPUT, output_path: Path = DEFAULT_OUTPUT
) -> pd.DataFrame:
    data = pd.read_csv(input_path)
    missing = set(GROUP_COLUMNS + METRICS) - set(data.columns)
    if missing:
        raise ValueError(f"missing required columns: {sorted(missing)}")
    summary = (
        data.groupby(GROUP_COLUMNS, as_index=False)[METRICS]
        .agg(["mean", "median", "std", "min", "max"])
    )
    summary.columns = [
        "_".join(str(part) for part in column if part)
        if isinstance(column, tuple)
        else column
        for column in summary.columns
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    summary.to_csv(output_path, index=False)
    return summary
