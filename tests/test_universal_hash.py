import pytest

from src.universal_hash import DEFAULT_PRIME, UniversalHash


def test_hash_indices_are_valid() -> None:
    universal_hash = UniversalHash(seed=42)
    for table_size in (1, 2, 17, 100):
        for key in range(-100, 101):
            assert 0 <= universal_hash.hash(key, table_size) < table_size


def test_same_seed_reproduces_parameters_and_hashes() -> None:
    first = UniversalHash(seed=123)
    second = UniversalHash(seed=123)
    assert (first.a, first.b) == (second.a, second.b)
    assert [first.hash(key, 31) for key in range(50)] == [
        second.hash(key, 31) for key in range(50)
    ]


def test_regenerate_keeps_parameters_in_valid_ranges() -> None:
    universal_hash = UniversalHash(seed=7)
    for _ in range(20):
        universal_hash.regenerate()
        assert 1 <= universal_hash.a < DEFAULT_PRIME
        assert 0 <= universal_hash.b < DEFAULT_PRIME


def test_invalid_table_size_is_rejected() -> None:
    with pytest.raises(ValueError):
        UniversalHash(seed=1).hash(10, 0)


def test_non_integer_key_is_rejected() -> None:
    with pytest.raises(TypeError):
        UniversalHash(seed=1).hash("10", 8)  # type: ignore[arg-type]
