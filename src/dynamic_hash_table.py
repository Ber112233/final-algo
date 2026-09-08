"""Dynamic integer hash table implemented with separate chaining."""

import math
import sys
from typing import Iterator

from src.universal_hash import DEFAULT_PRIME, UniversalHash


class DynamicHashTable:
    """A manually implemented dynamic hash table for controlled experiments."""

    def __init__(
        self,
        initial_capacity: int = 16,
        growth_factor: float = 2.0,
        load_threshold: float = 0.75,
        seed: int = 42,
        prime: int = DEFAULT_PRIME,
    ) -> None:
        if initial_capacity <= 0:
            raise ValueError("initial_capacity must be positive")
        if growth_factor <= 1:
            raise ValueError("growth_factor must be greater than 1")
        if not 0 < load_threshold < 1:
            raise ValueError("load_threshold must be between 0 and 1")

        self.initial_capacity = initial_capacity
        self.capacity = initial_capacity
        self.size = 0
        self.growth_factor = growth_factor
        self.load_threshold = load_threshold
        self.table: list[list[int]] = [[] for _ in range(self.capacity)]
        self.hash_function = UniversalHash(seed=seed, prime=prime)

        self.collisions = 0
        self.rehashes = 0
        self.rehash_operations = 0
        self.original_insertions = 0
        self.insert_cost = 0
        self.rehash_cost = 0
        self.resize_history: list[tuple[int, int, int]] = []

    @property
    def total_operation_cost(self) -> int:
        return self.insert_cost + self.rehash_cost

    def _index(self, key: int) -> int:
        return self.hash_function.hash(key, self.capacity)

    def contains(self, key: int) -> bool:
        bucket = self.table[self._index(key)]
        return key in bucket

    def insert(self, key: int) -> bool:
        index = self._index(key)
        bucket = self.table[index]
        if key in bucket:
            # Hash and bucket access were still performed.
            self.insert_cost += 2
            return False

        if bucket:
            self.collisions += 1
        bucket.append(key)
        self.size += 1
        self.original_insertions += 1
        # One unit each for hashing, bucket access, and append.
        self.insert_cost += 3

        if self.load_factor() > self.load_threshold:
            self.resize()
        return True

    def load_factor(self) -> float:
        return self.size / self.capacity

    def _keys(self) -> Iterator[int]:
        for bucket in self.table:
            yield from bucket

    def _insert_without_resize(self, key: int) -> None:
        self.table[self._index(key)].append(key)
        # Same three primitives as insertion, charged to rehash instead.
        self.rehash_cost += 3

    def resize(self) -> None:
        old_capacity = self.capacity
        keys = list(self._keys())
        new_capacity = max(old_capacity + 1, math.ceil(old_capacity * self.growth_factor))

        self.capacity = new_capacity
        self.table = [[] for _ in range(new_capacity)]
        for key in keys:
            self._insert_without_resize(key)

        self.rehashes += 1
        self.rehash_operations += len(keys)
        self.resize_history.append((old_capacity, new_capacity, len(keys)))

    def amortized_cost(self) -> float:
        if self.original_insertions == 0:
            return 0.0
        return self.total_operation_cost / self.original_insertions

    def unused_capacity(self) -> int:
        return self.capacity - self.size

    def utilization(self) -> float:
        return self.size / self.capacity

    def estimate_memory(self) -> int:
        """Approximate Python object memory, not process resident memory."""
        total = sys.getsizeof(self.table)
        for bucket in self.table:
            total += sys.getsizeof(bucket)
            total += sum(sys.getsizeof(key) for key in bucket)
        return total
