"""Measure collisions at controlled load factors without resizing."""

import csv
import math
from pathlib import Path
from typing import Sequence

from src.dynamic_hash_table import DynamicHashTable
from src.generators import generate_random_keys


DEFAULT_OUTPUT = Path("results/raw/collision_experiment.csv")
LOAD_FACTORS = [value / 10 for value in range(1, 10)]


def run_collision_experiment(
    capacity: int = 1_000,
    repetitions: int = 30,
    base_seed: int = 42,
    load_factors: Sequence[float] = LOAD_FACTORS,
    output_path: Path = DEFAULT_OUTPUT,
    overwrite: bool = False,
) -> list[dict[str, int | float]]:
    if output_path.exists() and output_path.stat().st_size > 0 and not overwrite:
        raise FileExistsError(f"{output_path} already exists; use --overwrite")
    maximum_elements = math.floor(capacity * max(load_factors))
    rows: list[dict[str, int | float]] = []
    for repetition in range(1, repetitions + 1):
        seed = base_seed + repetition - 1
        keys = generate_random_keys(maximum_elements, seed)
        for alpha in load_factors:
            number_of_elements = math.floor(capacity * alpha)
            table = DynamicHashTable(
                initial_capacity=capacity,
                growth_factor=2.0,
                load_threshold=0.99,
                seed=seed,
            )
            for key in keys[:number_of_elements]:
                table.insert(key)
            rows.append(
                {
                    "alpha": alpha,
                    "number_of_elements": number_of_elements,
                    "collisions": table.collisions,
                    "collisions_per_operation": (
                        table.collisions / number_of_elements if number_of_elements else 0.0
                    ),
                    "seed": seed,
                    "repetition": repetition,
                }
            )
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows
