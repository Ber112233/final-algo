"""Reproducible integer input generators."""

import math
import random


def _validate_n(n: int) -> None:
    if n < 0:
        raise ValueError("n must be non-negative")


def generate_random_keys(n: int, seed: int) -> list[int]:
    """Return unique keys sampled uniformly from a range much larger than n."""
    _validate_n(n)
    random_generator = random.Random(seed)
    universe_size = max(10, n * 20)
    return random_generator.sample(range(universe_size), n)


def generate_sequential_keys(n: int) -> list[int]:
    _validate_n(n)
    return list(range(n))


def generate_clustered_keys(n: int, seed: int) -> list[int]:
    """Return unique keys concentrated around sqrt(n) randomly chosen centers.

    A center is selected uniformly for every candidate, then a Gaussian offset is
    added. Duplicate candidates are retried. This creates local groups without
    targeting the universal hash parameters.
    """
    _validate_n(n)
    if n == 0:
        return []
    random_generator = random.Random(seed)
    cluster_count = max(1, math.isqrt(n))
    spacing = max(100, n * 10)
    centers = random_generator.sample(range(spacing, spacing * (cluster_count + 2)), cluster_count)
    spread = max(2.0, math.sqrt(n))
    keys: list[int] = []
    seen: set[int] = set()
    while len(keys) < n:
        center = centers[random_generator.randrange(cluster_count)]
        candidate = center + round(random_generator.gauss(0, spread))
        if candidate not in seen:
            seen.add(candidate)
            keys.append(candidate)
    return keys


def generate_keys(input_type: str, n: int, seed: int) -> list[int]:
    if input_type == "random":
        return generate_random_keys(n, seed)
    if input_type == "sequential":
        return generate_sequential_keys(n)
    if input_type == "clustered":
        return generate_clustered_keys(n, seed)
    raise ValueError(f"unsupported input type: {input_type}")


def generate_workload(input_type: str, n: int, key_seed: int, order_seed: int) -> list[int]:
    """Generate a key set and independently control its insertion order."""
    keys = generate_keys(input_type, n, key_seed)
    random.Random(order_seed).shuffle(keys)
    return keys
