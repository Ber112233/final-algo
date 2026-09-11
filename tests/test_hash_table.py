import math
import pytest

from src.dynamic_hash_table import DynamicHashTable, is_prime, next_prime
from src.linear_probing_hash_table import LinearProbingHashTable


def test_prime_capacity_helpers() -> None:
    assert next_prime(11) == 11
    assert next_prime(12) == 13
    assert is_prime(97)


def test_insert_contains_and_invariants() -> None:
    table = DynamicHashTable(initial_capacity=11, load_threshold=.9)
    for key in (10, 20, 30, 40, 50):
        assert table.insert(key)
    assert table.size == 5
    assert all(table.contains(key) for key in (10, 20, 30, 40, 50))
    table.validate_invariants()


def test_duplicate_does_not_change_size() -> None:
    table = DynamicHashTable()
    assert table.insert(10)
    assert not table.insert(10)
    assert table.size == table.original_insertions == 1


@pytest.mark.parametrize("gamma", [1.25, 1.5, 2.0, 3.0, 4.0])
def test_resize_uses_prime_capacity_and_effective_gamma(gamma: float) -> None:
    table = DynamicHashTable(initial_capacity=11, growth_factor=gamma, load_threshold=.5)
    for key in range(6):
        table.insert(key)
    expected = next_prime(math.ceil(11 * gamma))
    assert table.capacity == expected
    event = table.resize_history[0]
    assert event.gamma_effective == pytest.approx(expected / 11)
    assert event.alpha_pre == pytest.approx(5 / 11)
    assert event.alpha_post == pytest.approx(5 / expected)


def test_resize_selects_fresh_hash_and_preserves_keys() -> None:
    table = DynamicHashTable(initial_capacity=5, growth_factor=2, load_threshold=.5, seed=7)
    initial_hash = (table.hash_function.a, table.hash_function.b)
    keys = list(range(100))
    for key in keys:
        table.insert(key)
    assert table.resize_count > 0
    assert (table.hash_function.a, table.hash_function.b) != initial_hash
    assert all(table.contains(key) for key in keys)
    table.validate_invariants()


def test_pair_counter_matches_full_recomputation() -> None:
    table = DynamicHashTable(initial_capacity=11, load_threshold=.9, seed=9)
    for key in range(200):
        table.insert(key)
        expected = sum(len(bucket) * (len(bucket) - 1) // 2 for bucket in table.table)
        assert table.pair_collisions_current == expected


def test_metrics_and_peak_are_coherent() -> None:
    table = DynamicHashTable(initial_capacity=5, load_threshold=.5)
    for key in range(30):
        table.insert(key)
    assert table.hash_evaluations >= table.original_insertions
    assert table.bucket_assignments == table.original_insertions + table.moved_entries
    assert table.allocated_bucket_slots_peak >= table.capacity
    assert table.structural_bytes() > 0


@pytest.mark.parametrize("kwargs", [{"initial_capacity": 0}, {"growth_factor": 1.0},
                                     {"load_threshold": 0.0}, {"load_threshold": 1.0}])
def test_invalid_configuration(kwargs) -> None:
    with pytest.raises(ValueError):
        DynamicHashTable(**kwargs)


def test_linear_probing_secondary_rejects_duplicates_and_survives_resize() -> None:
    table = LinearProbingHashTable(initial_capacity=5, load_threshold=.5)
    for key in range(40):
        assert table.insert(key)
    assert not table.insert(10)
    assert table.size == 40
    assert table.resize_count > 0
    assert all(table.contains(key) for key in range(40))
