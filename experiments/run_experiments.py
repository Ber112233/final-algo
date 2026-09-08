"""Main experiment runner and CSV export."""

import csv
import time
from dataclasses import fields
from pathlib import Path
from typing import Iterable, Sequence

from experiments.configurations import (
    GROWTH_FACTORS,
    INITIAL_CAPACITY,
    INSTANCE_SIZES,
    LOAD_THRESHOLDS,
)
from src.dynamic_hash_table import DynamicHashTable
from src.generators import generate_keys
from src.metrics import ExperimentResult


DEFAULT_OUTPUT = Path("results/raw/results.csv")


def run_experiment(
    keys: Sequence[int],
    growth_factor: float,
    load_threshold: float,
    seed: int,
    repetition: int,
    input_type: str,
    initial_capacity: int = INITIAL_CAPACITY,
) -> ExperimentResult:
    table = DynamicHashTable(
        initial_capacity=initial_capacity,
        growth_factor=growth_factor,
        load_threshold=load_threshold,
        seed=seed,
    )
    start = time.perf_counter()
    for key in keys:
        table.insert(key)
    elapsed_time = time.perf_counter() - start
    n = len(keys)
    return ExperimentResult(
        n=n,
        growth_factor=growth_factor,
        load_threshold=load_threshold,
        seed=seed,
        repetition=repetition,
        input_type=input_type,
        elapsed_time=elapsed_time,
        time_per_operation=elapsed_time / n if n else 0.0,
        collisions=table.collisions,
        collisions_per_operation=table.collisions / n if n else 0.0,
        rehashes=table.rehashes,
        rehash_operations=table.rehash_operations,
        final_capacity=table.capacity,
        final_size=table.size,
        final_load_factor=table.load_factor(),
        unused_capacity=table.unused_capacity(),
        utilization=table.utilization(),
        insert_cost=table.insert_cost,
        rehash_cost=table.rehash_cost,
        total_operation_cost=table.total_operation_cost,
        amortized_cost=table.amortized_cost(),
        estimated_memory=table.estimate_memory(),
        initial_capacity=table.initial_capacity,
        hash_a=table.hash_function.a,
        hash_b=table.hash_function.b,
        hash_prime=table.hash_function.prime,
    )


def write_results(
    results: Iterable[ExperimentResult], output_path: Path = DEFAULT_OUTPUT, overwrite: bool = False
) -> None:
    if output_path.exists() and output_path.stat().st_size > 0 and not overwrite:
        raise FileExistsError(f"{output_path} already exists; use --overwrite")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [field.name for field in fields(ExperimentResult)]
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for result in results:
            writer.writerow(result.to_dict())


def run_matrix(
    instance_sizes: Sequence[int] = INSTANCE_SIZES,
    repetitions: int = 30,
    base_seed: int = 42,
    input_type: str = "random",
    output_path: Path = DEFAULT_OUTPUT,
    overwrite: bool = False,
    initial_capacity: int = INITIAL_CAPACITY,
) -> list[ExperimentResult]:
    results: list[ExperimentResult] = []
    configurations = [
        (growth, threshold)
        for growth in GROWTH_FACTORS
        for threshold in LOAD_THRESHOLDS
    ]
    for n in instance_sizes:
        for repetition in range(1, repetitions + 1):
            seed = base_seed + repetition - 1
            keys = generate_keys(input_type, n, seed)  # Once per comparable block.
            print(f"\nInput type: {input_type}\nn: {n}\nrepetition: {repetition}/{repetitions}")
            for number, (growth_factor, load_threshold) in enumerate(configurations, 1):
                print(
                    f"[{number}/9] growth={growth_factor} "
                    f"threshold={load_threshold:.2f}"
                )
                results.append(
                    run_experiment(
                        keys,
                        growth_factor,
                        load_threshold,
                        seed,
                        repetition,
                        input_type,
                        initial_capacity,
                    )
                )
    write_results(results, output_path, overwrite)
    return results
