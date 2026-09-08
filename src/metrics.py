"""Serializable metrics produced by one complete experimental execution."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentResult:
    n: int
    growth_factor: float
    load_threshold: float
    seed: int
    repetition: int
    input_type: str
    elapsed_time: float
    time_per_operation: float
    collisions: int
    collisions_per_operation: float
    rehashes: int
    rehash_operations: int
    final_capacity: int
    final_size: int
    final_load_factor: float
    unused_capacity: int
    utilization: float
    insert_cost: int
    rehash_cost: int
    total_operation_cost: int
    amortized_cost: float
    estimated_memory: int
    initial_capacity: int
    hash_a: int
    hash_b: int
    hash_prime: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
