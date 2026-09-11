"""Serializable records for the dynamic hashing experiment."""

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class ExperimentResult:
    run_id: str
    git_commit: str
    python_version: str
    platform: str
    cpu: str
    n: int
    gamma_nominal: float
    gamma_effective_mean: float
    tau: float
    m0: int
    final_capacity: int
    final_size: int
    final_load_factor: float
    key_family: str
    key_seed: int
    order_seed: int
    hash_seed: int
    repetition: int
    elapsed_ns: int
    time_per_operation_ns: float
    latency_p50_ns: float
    latency_p95_ns: float
    latency_p99_ns: float
    latency_max_ns: int
    resize_count: int
    moved_entries: int
    migrations_per_insertion: float
    hash_evaluations: int
    key_comparisons: int
    insert_collision_events: int
    pair_collisions: int
    pair_collisions_per_key: float
    universal_pair_bound: float
    bound_ratio: float
    max_chain_length: int
    bucket_assignments: int
    bucket_slots_peak: int
    unused_capacity: int
    structural_bytes_final: int
    bytes_per_element: float
    tracemalloc_peak_bytes: int
    gc_enabled: bool
    hash_a: int
    hash_b: int
    hash_prime: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
