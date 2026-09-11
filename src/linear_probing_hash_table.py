"""Secondary open-addressing implementation adapted from Gabriel Olarte's branch."""

from __future__ import annotations

import math
import random
from src.dynamic_hash_table import next_prime
from src.universal_hash import DEFAULT_PRIME


class LinearProbingHashTable:
    """Dynamic integer set with linear probing; not the primary experiment."""

    def __init__(self, growth_factor: float = 2.0, load_threshold: float = .75,
                 seed: int = 42, initial_capacity: int = 11) -> None:
        if growth_factor <= 1:
            raise ValueError("growth_factor must be greater than 1")
        if not 0 < load_threshold < 1:
            raise ValueError("load_threshold must be between 0 and 1")
        self.growth_factor = growth_factor
        self.load_threshold = load_threshold
        self.rng = random.Random(seed)
        self.capacity = next_prime(initial_capacity)
        self.slots: list[int | None] = [None] * self.capacity
        self.size = 0
        self.resize_count = 0
        self.moved_entries = 0
        self.probe_collisions = 0
        self.total_probes = 0
        self.hash_a = 1
        self.hash_b = 0
        self._new_hash_parameters()

    def _new_hash_parameters(self) -> None:
        self.hash_a = self.rng.randrange(1, DEFAULT_PRIME)
        self.hash_b = self.rng.randrange(DEFAULT_PRIME)

    def _index(self, key: int) -> int:
        return ((self.hash_a * key + self.hash_b) % DEFAULT_PRIME) % self.capacity

    def _place(self, key: int, count_collisions: bool) -> tuple[bool, int]:
        index = self._index(key)
        probes = 1
        for _ in range(self.capacity):
            stored = self.slots[index]
            if stored is None:
                self.slots[index] = key
                return True, probes
            if stored == key:
                return False, probes
            if count_collisions:
                self.probe_collisions += 1
            probes += 1
            index = (index + 1) % self.capacity
        raise RuntimeError("linear-probing table has no free slot")

    def _resize(self) -> None:
        keys = [key for key in self.slots if key is not None]
        self.capacity = next_prime(math.ceil(self.capacity * self.growth_factor))
        self.slots = [None] * self.capacity
        self._new_hash_parameters()
        self.resize_count += 1
        for key in keys:
            inserted, _ = self._place(key, count_collisions=False)
            if not inserted:
                raise AssertionError("duplicate detected while rehashing")
            self.moved_entries += 1

    def insert(self, key: int) -> bool:
        if (self.size + 1) / self.capacity > self.load_threshold:
            self._resize()
        inserted, probes = self._place(key, count_collisions=True)
        self.total_probes += probes
        if inserted:
            self.size += 1
        return inserted

    def contains(self, key: int) -> bool:
        index = self._index(key)
        for _ in range(self.capacity):
            stored = self.slots[index]
            if stored is None:
                return False
            if stored == key:
                return True
            index = (index + 1) % self.capacity
        return False
