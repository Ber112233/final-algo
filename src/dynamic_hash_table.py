"""Instrumented dynamic hash table using separate chaining."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import sys
from typing import Iterator

from src.universal_hash import DEFAULT_PRIME, UniversalHash


def is_prime(value: int) -> bool:
    if value < 2:
        return False
    if value % 2 == 0:
        return value == 2
    divisor = 3
    while divisor * divisor <= value:
        if value % divisor == 0:
            return False
        divisor += 2
    return True


def next_prime(value: int) -> int:
    candidate = max(2, value)
    while not is_prime(candidate):
        candidate += 1
    return candidate


@dataclass(frozen=True)
class ResizeEvent:
    resize_number: int
    old_capacity: int
    new_capacity: int
    gamma_effective: float
    size: int
    trigger_load: float
    alpha_pre: float
    alpha_post: float
    moved_entries: int
    pair_collisions_after: int
    old_hash_a: int
    old_hash_b: int
    new_hash_a: int
    new_hash_b: int

    def to_dict(self) -> dict[str, int | float]:
        return asdict(self)


class DynamicHashTable:
    """Integer hash table instrumented for the factorial experiment."""

    def __init__(self, initial_capacity: int = 11, growth_factor: float = 2.0,
                 load_threshold: float = 0.75, seed: int = 42,
                 prime: int = DEFAULT_PRIME) -> None:
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        if growth_factor <= 1:
            raise ValueError("growth_factor must be greater than 1")
        if not 0 < load_threshold < 1:
            raise ValueError("load_threshold must be between 0 and 1")
        self.initial_capacity = next_prime(initial_capacity)
        self.capacity = self.initial_capacity
        self.size = 0
        self.growth_factor = growth_factor
        self.load_threshold = load_threshold
        self.table: list[list[int]] = [[] for _ in range(self.capacity)]
        self.hash_function = UniversalHash(seed=seed, prime=prime)
        self.hash_evaluations = 0
        self.key_comparisons = 0
        self.insert_collision_events = 0
        self.pair_collisions_current = 0
        self.resize_count = 0
        self.moved_entries = 0
        self.bucket_assignments = 0
        self.original_insertions = 0
        self.max_chain_length = 0
        self.allocated_bucket_slots_peak = self.capacity
        self.resize_history: list[ResizeEvent] = []

    @property
    def collisions(self) -> int:
        return self.insert_collision_events

    @property
    def rehashes(self) -> int:
        return self.resize_count

    @property
    def rehash_operations(self) -> int:
        return self.moved_entries

    @property
    def insert_cost(self) -> int:
        return self.original_insertions + self.key_comparisons

    @property
    def rehash_cost(self) -> int:
        return self.moved_entries

    @property
    def total_operation_cost(self) -> int:
        """Unweighted diagnostic sum; individual components are primary."""
        return self.hash_evaluations + self.key_comparisons + self.moved_entries + self.bucket_assignments

    def _index(self, key: int) -> int:
        self.hash_evaluations += 1
        return self.hash_function.hash(key, self.capacity)

    def contains(self, key: int) -> bool:
        bucket = self.table[self._index(key)]
        for stored_key in bucket:
            self.key_comparisons += 1
            if stored_key == key:
                return True
        return False

    def insert(self, key: int) -> bool:
        if not isinstance(key, int):
            raise TypeError("DynamicHashTable only supports integer keys")
        if (self.size + 1) / self.capacity > self.load_threshold:
            self.resize(trigger_load=(self.size + 1) / self.capacity)
        bucket = self.table[self._index(key)]
        for stored_key in bucket:
            self.key_comparisons += 1
            if stored_key == key:
                return False
        length = len(bucket)
        if length:
            self.insert_collision_events += 1
        self.pair_collisions_current += length
        bucket.append(key)
        self.bucket_assignments += 1
        self.size += 1
        self.original_insertions += 1
        self.max_chain_length = max(self.max_chain_length, length + 1)
        return True

    def load_factor(self) -> float:
        return self.size / self.capacity

    def _keys(self) -> Iterator[int]:
        for bucket in self.table:
            yield from bucket

    def _place_migrated(self, key: int) -> None:
        bucket = self.table[self._index(key)]
        self.pair_collisions_current += len(bucket)
        bucket.append(key)
        self.bucket_assignments += 1
        self.moved_entries += 1
        self.max_chain_length = max(self.max_chain_length, len(bucket))

    def resize(self, trigger_load: float | None = None) -> None:
        old_capacity = self.capacity
        old_a, old_b = self.hash_function.a, self.hash_function.b
        keys = list(self._keys())
        new_capacity = next_prime(math.ceil(old_capacity * self.growth_factor))
        self.allocated_bucket_slots_peak = max(self.allocated_bucket_slots_peak, old_capacity + new_capacity)
        self.capacity = new_capacity
        self.table = [[] for _ in range(new_capacity)]
        self.hash_function.regenerate()
        self.pair_collisions_current = 0
        self.max_chain_length = 0
        moved_before = self.moved_entries
        for key in keys:
            self._place_migrated(key)
        self.resize_count += 1
        self.resize_history.append(ResizeEvent(
            self.resize_count, old_capacity, new_capacity, new_capacity / old_capacity,
            self.size, trigger_load if trigger_load is not None else self.load_factor(),
            self.size / old_capacity, self.size / new_capacity,
            self.moved_entries - moved_before, self.pair_collisions_current,
            old_a, old_b, self.hash_function.a, self.hash_function.b,
        ))

    def amortized_cost(self) -> float:
        return self.total_operation_cost / self.original_insertions if self.original_insertions else 0.0

    def unused_capacity(self) -> int:
        return self.capacity - self.size

    def utilization(self) -> float:
        return self.load_factor()

    def structural_bytes(self) -> int:
        seen: set[int] = set()
        def add_once(value: object) -> int:
            identity = id(value)
            if identity in seen:
                return 0
            seen.add(identity)
            return sys.getsizeof(value)
        total = add_once(self.table)
        for bucket in self.table:
            total += add_once(bucket)
            for key in bucket:
                total += add_once(key)
        return total

    def estimate_memory(self) -> int:
        return self.structural_bytes()

    def validate_invariants(self) -> None:
        keys = list(self._keys())
        if len(keys) != self.size or len(set(keys)) != self.size:
            raise AssertionError("size or uniqueness invariant violated")
        for index, bucket in enumerate(self.table):
            for key in bucket:
                if self.hash_function.hash(key, self.capacity) != index:
                    raise AssertionError("key stored in an invalid bucket")
        pairs = sum(len(bucket) * (len(bucket) - 1) // 2 for bucket in self.table)
        if pairs != self.pair_collisions_current:
            raise AssertionError("pair-collision counter is invalid")
        if self.load_factor() > self.load_threshold and self.size:
            raise AssertionError("load threshold violated")
