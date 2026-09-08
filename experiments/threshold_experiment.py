"""Observe the individual operation cost around a resize threshold."""

import csv
from pathlib import Path

from src.dynamic_hash_table import DynamicHashTable


DEFAULT_OUTPUT = Path("results/raw/threshold_experiment.csv")


def run_threshold_experiment(
    initial_capacity: int = 1_000,
    growth_factor: float = 2.0,
    load_threshold: float = 0.75,
    seed: int = 42,
    window: int = 5,
    output_path: Path = DEFAULT_OUTPUT,
    overwrite: bool = False,
) -> list[dict[str, int | float | bool]]:
    if output_path.exists() and output_path.stat().st_size > 0 and not overwrite:
        raise FileExistsError(f"{output_path} already exists; use --overwrite")
    trigger_operation = int(initial_capacity * load_threshold) + 1
    final_operation = trigger_operation + window
    first_recorded = max(1, trigger_operation - window)
    table = DynamicHashTable(
        initial_capacity, growth_factor, load_threshold, seed
    )
    rows: list[dict[str, int | float | bool]] = []
    for operation_number in range(1, final_operation + 1):
        previous_cost = table.total_operation_cost
        previous_rehashes = table.rehashes
        table.insert(operation_number - 1)
        if operation_number >= first_recorded:
            rows.append(
                {
                    "operation_number": operation_number,
                    "individual_operation_cost": table.total_operation_cost - previous_cost,
                    "capacity": table.capacity,
                    "load_factor": table.load_factor(),
                    "resize_occurred": table.rehashes > previous_rehashes,
                }
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows
