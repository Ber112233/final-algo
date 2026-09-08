import pytest

from src.generators import (
    generate_clustered_keys,
    generate_random_keys,
    generate_sequential_keys,
)


@pytest.mark.parametrize("generator", [generate_random_keys, generate_clustered_keys])
def test_seeded_generators_are_reproducible(generator) -> None:
    first = generator(500, 42)
    second = generator(500, 42)
    assert first == second
    assert len(first) == len(set(first)) == 500


def test_sequential_generator() -> None:
    assert generate_sequential_keys(5) == [0, 1, 2, 3, 4]


@pytest.mark.parametrize(
    "call", [lambda: generate_random_keys(-1, 1), lambda: generate_sequential_keys(-1)]
)
def test_negative_size_is_rejected(call) -> None:
    with pytest.raises(ValueError):
        call()
