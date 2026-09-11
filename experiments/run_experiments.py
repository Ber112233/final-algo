"""Factorial runner with reproducible blocking and auditable CSV output."""

from __future__ import annotations

import csv
from dataclasses import fields
import gc
import os
from pathlib import Path
import platform as platform_module
import random
import statistics
import subprocess
import sys
import time
import tracemalloc
from typing import Iterable, Sequence

from experiments.configurations import GROWTH_FACTORS, INITIAL_CAPACITY, INSTANCE_SIZES, LOAD_THRESHOLDS
from src.dynamic_hash_table import DynamicHashTable
from src.generators import generate_workload
from src.metrics import ExperimentResult


DEFAULT_OUTPUT = Path("data/raw/results.csv")
DEFAULT_RESIZE_OUTPUT = Path("data/raw/resize_events.csv")


def _git_commit() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short=12", "HEAD"], text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return "unknown"


def _percentile(values: list[int], percentile: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    position = (len(ordered) - 1) * percentile
    lower = int(position)
    upper = min(lower + 1, len(ordered) - 1)
    fraction = position - lower
    return ordered[lower] * (1 - fraction) + ordered[upper] * fraction


def run_experiment(
    keys: Sequence[int], growth_factor: float, load_threshold: float,
    hash_seed: int, repetition: int, input_type: str,
    key_seed: int | None = None, order_seed: int | None = None,
    initial_capacity: int = INITIAL_CAPACITY, trace_memory: bool = True,
) -> tuple[ExperimentResult, list[dict[str, object]]]:
    key_seed = hash_seed if key_seed is None else key_seed
    order_seed = hash_seed if order_seed is None else order_seed
    run_id = f"n{len(keys)}-g{growth_factor:g}-t{load_threshold:g}-r{repetition}-h{hash_seed}"
    table = DynamicHashTable(initial_capacity, growth_factor, load_threshold, hash_seed)
    latencies: list[int] = []
    if trace_memory:
        tracemalloc.start()
    start_total = time.perf_counter_ns()
    for key in keys:
        start_insert = time.perf_counter_ns()
        table.insert(key)
        latencies.append(time.perf_counter_ns() - start_insert)
    elapsed_ns = time.perf_counter_ns() - start_total
    trace_peak = tracemalloc.get_traced_memory()[1] if trace_memory else 0
    if trace_memory:
        tracemalloc.stop()
    table.validate_invariants()
    n = len(keys)
    pair_bound = n * (n - 1) / (2 * table.capacity) if table.capacity else 0.0
    gamma_values = [event.gamma_effective for event in table.resize_history]
    result = ExperimentResult(
        run_id=run_id, git_commit=_git_commit(), python_version=platform_module.python_version(),
        platform=platform_module.platform(), cpu=platform_module.processor() or os.environ.get("PROCESSOR_IDENTIFIER", "unknown"),
        n=n, gamma_nominal=growth_factor,
        gamma_effective_mean=statistics.fmean(gamma_values) if gamma_values else 1.0,
        tau=load_threshold, m0=table.initial_capacity, final_capacity=table.capacity,
        final_size=table.size, final_load_factor=table.load_factor(), key_family=input_type,
        key_seed=key_seed, order_seed=order_seed, hash_seed=hash_seed, repetition=repetition,
        elapsed_ns=elapsed_ns, time_per_operation_ns=elapsed_ns / n if n else 0.0,
        latency_p50_ns=_percentile(latencies, .50), latency_p95_ns=_percentile(latencies, .95),
        latency_p99_ns=_percentile(latencies, .99), latency_max_ns=max(latencies, default=0),
        resize_count=table.resize_count, moved_entries=table.moved_entries,
        migrations_per_insertion=table.moved_entries / n if n else 0.0,
        hash_evaluations=table.hash_evaluations, key_comparisons=table.key_comparisons,
        insert_collision_events=table.insert_collision_events,
        pair_collisions=table.pair_collisions_current,
        pair_collisions_per_key=table.pair_collisions_current / n if n else 0.0,
        universal_pair_bound=pair_bound,
        bound_ratio=table.pair_collisions_current / pair_bound if pair_bound else 0.0,
        max_chain_length=table.max_chain_length, bucket_assignments=table.bucket_assignments,
        bucket_slots_peak=table.allocated_bucket_slots_peak,
        unused_capacity=table.unused_capacity(), structural_bytes_final=table.structural_bytes(),
        bytes_per_element=table.structural_bytes() / n if n else 0.0,
        tracemalloc_peak_bytes=trace_peak, gc_enabled=gc.isenabled(),
        hash_a=table.hash_function.a, hash_b=table.hash_function.b, hash_prime=table.hash_function.prime,
    )
    events = [{"run_id": run_id, **event.to_dict()} for event in table.resize_history]
    return result, events


def _write_dataclasses(results: Iterable[ExperimentResult], path: Path, overwrite: bool) -> None:
    if path.exists() and path.stat().st_size and not overwrite:
        raise FileExistsError(f"{path} already exists; use --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=[field.name for field in fields(ExperimentResult)])
        writer.writeheader()
        writer.writerows(result.to_dict() for result in results)


def _write_dicts(rows: list[dict[str, object]], path: Path, overwrite: bool) -> None:
    if path.exists() and path.stat().st_size and not overwrite:
        raise FileExistsError(f"{path} already exists; use --overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def warm_up() -> None:
    table = DynamicHashTable(initial_capacity=11, growth_factor=2, load_threshold=.75, seed=1)
    for key in range(500):
        table.insert(key)


def run_matrix(
    instance_sizes: Sequence[int] = INSTANCE_SIZES, repetitions: int = 30,
    base_seed: int = 42, input_type: str = "random", output_path: Path = DEFAULT_OUTPUT,
    overwrite: bool = False, initial_capacity: int = INITIAL_CAPACITY,
    resize_output_path: Path = DEFAULT_RESIZE_OUTPUT, trace_memory: bool = True,
) -> list[ExperimentResult]:
    warm_up()
    results: list[ExperimentResult] = []
    resize_events: list[dict[str, object]] = []
    configurations = [(growth, threshold) for growth in GROWTH_FACTORS for threshold in LOAD_THRESHOLDS]
    for n in instance_sizes:
        for repetition in range(1, repetitions + 1):
            key_seed = base_seed + 10_000 * repetition + n
            order_seed = base_seed + 20_000 * repetition + n
            hash_seed = base_seed + 30_000 * repetition + n
            keys = generate_workload(input_type, n, key_seed, order_seed)
            ordered_configs = configurations.copy()
            random.Random(base_seed + n + repetition).shuffle(ordered_configs)
            for number, (growth_factor, load_threshold) in enumerate(ordered_configs, 1):
                print(f"n={n} rep={repetition}/{repetitions} treatment={number}/20 gamma={growth_factor} tau={load_threshold}")
                result, events = run_experiment(
                    keys, growth_factor, load_threshold, hash_seed, repetition, input_type,
                    key_seed, order_seed, initial_capacity, trace_memory,
                )
                results.append(result)
                resize_events.extend(events)
    _write_dataclasses(results, output_path, overwrite)
    _write_dicts(resize_events, resize_output_path, overwrite)
    return results


def write_results(results: Iterable[ExperimentResult], output_path: Path = DEFAULT_OUTPUT,
                  overwrite: bool = False) -> None:
    _write_dataclasses(results, output_path, overwrite)
