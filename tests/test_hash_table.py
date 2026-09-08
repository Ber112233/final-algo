import math

import pytest

from src.dynamic_hash_table import DynamicHashTable


def test_insert_contains_and_load_factor() -> None:
    table = DynamicHashTable(initial_capacity=10, load_threshold=0.9)
    for key in (10, 20, 30, 40, 50):
        assert table.insert(key)
    assert table.size == 5
    assert all(table.contains(key) for key in (10, 20, 30, 40, 50))
    assert table.load_factor() == pytest.approx(0.5)


def test_duplicate_is_rejected_without_collision() -> None:
    table = DynamicHashTable(initial_capacity=10)
    assert table.insert(10)
    collisions = table.collisions
    assert not table.insert(10)
    assert table.size == 1
    assert table.original_insertions == 1
    assert table.collisions == collisions


@pytest.mark.parametrize(
    ("growth_factor", "expected_capacity"), [(1.5, 15), (2.0, 20), (3.0, 30)]
)
def test_growth_factors(growth_factor: float, expected_capacity: int) -> None:
    table = DynamicHashTable(
        initial_capacity=10, growth_factor=growth_factor, load_threshold=0.5
    )
    for key in range(6):
        table.insert(key)
    assert table.capacity == expected_capacity


def test_resize_preserves_all_keys_and_metrics() -> None:
    table = DynamicHashTable(
        initial_capacity=4, growth_factor=2.0, load_threshold=0.5
    )
    keys = list(range(20))
    for key in keys:
        table.insert(key)
    assert table.capacity > 4
    assert table.rehashes >= 1
    assert table.rehash_operations >= table.rehashes
    assert table.size == len(keys)
    assert all(table.contains(key) for key in keys)


def test_collision_count_is_reproducible() -> None:
    table = DynamicHashTable(initial_capacity=8, load_threshold=0.9, seed=9)
    first_key = 1
    target_index = table.hash_function.hash(first_key, table.capacity)
    second_key = next(
        key
        for key in range(2, 10_000)
        if table.hash_function.hash(key, table.capacity) == target_index
    )
    table.insert(first_key)
    table.insert(second_key)
    assert table.collisions == 1


def test_cost_and_memory_metrics_are_coherent() -> None:
    table = DynamicHashTable(initial_capacity=4, load_threshold=0.5)
    for key in range(8):
        table.insert(key)
    assert table.total_operation_cost == table.insert_cost + table.rehash_cost
    assert table.amortized_cost() == pytest.approx(
        table.total_operation_cost / table.original_insertions
    )
    assert table.unused_capacity() == table.capacity - table.size
    assert table.utilization() == pytest.approx(table.size / table.capacity)
    assert table.estimate_memory() > 0


@pytest.mark.parametrize(
    "kwargs",
    [
        {"initial_capacity": 0},
        {"growth_factor": 1.0},
        {"load_threshold": 0.0},
        {"load_threshold": 1.0},
    ],
)
def test_invalid_configuration(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        DynamicHashTable(**kwargs)  # type: ignore[arg-type]
