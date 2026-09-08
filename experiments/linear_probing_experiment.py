"""Small secondary comparison; collision metrics are probes, not bucket pairs."""

import csv
from pathlib import Path
import time
from src.generators import generate_workload
from src.linear_probing_hash_table import LinearProbingHashTable


def run_secondary(output: Path = Path("data/raw/linear_probing.csv"), repetitions: int = 30,
                  overwrite: bool = False) -> list[dict[str, int | float]]:
    if output.exists() and output.stat().st_size and not overwrite:
        raise FileExistsError(f"{output} exists; use overwrite")
    rows: list[dict[str, int | float]] = []
    for n in (1_000, 10_000):
        for repetition in range(1, repetitions + 1):
            keys = generate_workload("random", n, 1000 + repetition, 2000 + repetition)
            for gamma in (1.5, 2.0, 3.0):
                for tau in (.5, .75, .9):
                    table = LinearProbingHashTable(gamma, tau, 3000 + repetition)
                    start = time.perf_counter_ns()
                    for key in keys:
                        table.insert(key)
                    elapsed = time.perf_counter_ns() - start
                    rows.append({"n": n, "repetition": repetition, "gamma": gamma, "tau": tau,
                                 "probe_collisions": table.probe_collisions,
                                 "total_probes": table.total_probes, "resize_count": table.resize_count,
                                 "moved_entries": table.moved_entries, "final_capacity": table.capacity,
                                 "elapsed_ns": elapsed})
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0])); writer.writeheader(); writer.writerows(rows)
    return rows
