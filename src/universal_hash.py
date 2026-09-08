"""Universal hashing for integer keys."""

import random


DEFAULT_PRIME = 2_305_843_009_213_693_951  # 2**61 - 1, a Mersenne prime.


class UniversalHash:
    """A reproducible member of h(x)=((a*x+b) mod p) mod m."""

    def __init__(self, seed: int, prime: int = DEFAULT_PRIME) -> None:
        if prime <= 2:
            raise ValueError("prime must be greater than 2")
        self.seed = seed
        self.prime = prime
        self._random = random.Random(seed)
        self.a = 1
        self.b = 0
        self.regenerate()

    def hash(self, key: int, table_size: int) -> int:
        if not isinstance(key, int):
            raise TypeError("UniversalHash only supports integer keys")
        if table_size <= 0:
            raise ValueError("table_size must be positive")
        return ((self.a * key + self.b) % self.prime) % table_size

    def regenerate(self) -> None:
        self.a = self._random.randrange(1, self.prime)
        self.b = self._random.randrange(0, self.prime)
