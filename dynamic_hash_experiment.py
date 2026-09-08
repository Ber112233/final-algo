#!/usr/bin/env python3
"""Reproducible experiment for dynamic hash tables with universal hashing.

The experiment varies the growth factor and maximum load factor, then measures
rehashes, probing collisions, capacity, and running time while inserting the
same keys.  It intentionally uses only the Python standard library.
"""

from __future__ import annotations

import argparse
import csv
import random
import time
from dataclasses import dataclass
from pathlib import Path
from statistics import mean, median, stdev


PRIME = 2_147_483_647  # large Mersenne prime; keys are reduced modulo PRIME


class DynamicHashTable:
    """Open-addressed table using linear probing and a universal hash family."""

    def __init__(self, growth_factor: float, max_load: float, seed: int,
                 initial_capacity: int = 8) -> None:
        if growth_factor <= 1.0:
            raise ValueError("growth_factor must be > 1")
        if not 0.0 < max_load < 1.0:
            raise ValueError("max_load must be between 0 and 1")
        self.growth_factor = growth_factor
        self.max_load = max_load
        self.rng = random.Random(seed)
        self.capacity = initial_capacity
        self.slots: list[int | None] = [None] * self.capacity
        self.size = 0
        self.rehashes = 0
        self.probe_collisions = 0
        self.total_probes = 0
        self.hash_a = 1
        self.hash_b = 0
        self._new_hash_parameters()

    def _new_hash_parameters(self) -> None:
        self.hash_a = self.rng.randrange(1, PRIME)
        self.hash_b = self.rng.randrange(0, PRIME)

    def _index(self, key: int) -> int:
        return ((self.hash_a * (key % PRIME) + self.hash_b) % PRIME) % self.capacity

    def _place(self, key: int, count_stats: bool) -> int:
        index = self._index(key)
        probes = 0
        while self.slots[index] is not None:
            if self.slots[index] == key:
                return probes + 1
            probes += 1
            if count_stats:
                self.probe_collisions += 1
            index = (index + 1) % self.capacity
        self.slots[index] = key
        return probes + 1

    def _resize(self) -> None:
        old_slots = self.slots
        new_capacity = max(self.capacity + 1, int(self.capacity * self.growth_factor))
        self.capacity = new_capacity
        self.slots = [None] * self.capacity
        self._new_hash_parameters()
        self.rehashes += 1
        for key in old_slots:
            if key is not None:
                self._place(key, count_stats=False)

    def insert(self, key: int) -> None:
        if (self.size + 1) / self.capacity > self.max_load:
            self._resize()
        probes = self._place(key, count_stats=True)
        self.total_probes += probes
        self.size += 1


@dataclass
class Measurement:
    growth_factor: float
    max_load: float
    n: int
    repetition: int
    rehashes: int
    collisions: int
    probes: int
    final_capacity: int
    elapsed_seconds: float


def run_once(n: int, growth_factor: float, max_load: float,
             repetition: int, seed: int) -> Measurement:
    key_rng = random.Random(seed + 10_000_019)
    keys = key_rng.sample(range(1, PRIME - 1), n)
    table = DynamicHashTable(growth_factor, max_load, seed=seed)
    start = time.perf_counter()
    for key in keys:
        table.insert(key)
    elapsed = time.perf_counter() - start
    return Measurement(growth_factor, max_load, n, repetition,
                       table.rehashes, table.probe_collisions,
                       table.total_probes, table.capacity, elapsed)


def summarize(rows: list[Measurement]) -> list[dict[str, object]]:
    groups: dict[tuple[float, float, int], list[Measurement]] = {}
    for row in rows:
        groups.setdefault((row.growth_factor, row.max_load, row.n), []).append(row)
    output = []
    for (growth, load, n), values in sorted(groups.items()):
        def avg(field: str) -> float:
            return mean(getattr(v, field) for v in values)
        def sd(field: str) -> float:
            nums = [getattr(v, field) for v in values]
            return stdev(nums) if len(nums) > 1 else 0.0
        output.append({
            "growth_factor": growth, "max_load": load, "n": n,
            "repetitions": len(values),
            "mean_rehashes": avg("rehashes"),
            "mean_collisions": avg("collisions"),
            "median_collisions": median(v.collisions for v in values),
            "sd_collisions": sd("collisions"),
            "mean_probes": avg("probes"),
            "mean_final_capacity": avg("final_capacity"),
            "mean_elapsed_seconds": avg("elapsed_seconds"),
        })
    return output


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sizes", nargs="+", type=int, default=[1_000, 5_000, 10_000])
    parser.add_argument("--growth-factors", nargs="+", type=float, default=[1.5, 2.0, 3.0])
    parser.add_argument("--max-loads", nargs="+", type=float, default=[0.50, 0.75, 0.90])
    parser.add_argument("--repetitions", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260908)
    parser.add_argument("--output-dir", type=Path, default=Path("results"))
    args = parser.parse_args()
    if args.repetitions < 1 or any(n < 1 for n in args.sizes):
        parser.error("sizes and repetitions must be positive")

    raw: list[Measurement] = []
    for n in args.sizes:
        for growth in args.growth_factors:
            for load in args.max_loads:
                for repetition in range(args.repetitions):
                    run_seed = args.seed + repetition + 1_000 * n
                    raw.append(run_once(n, growth, load, repetition, run_seed))

    raw_dicts = [vars(row) for row in raw]
    write_csv(args.output_dir / "raw_measurements.csv", raw_dicts)
    write_csv(args.output_dir / "summary.csv", summarize(raw))
    print(f"Wrote {len(raw)} runs to {args.output_dir}/")


if __name__ == "__main__":
    main()
