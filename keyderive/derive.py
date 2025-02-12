from typing import List

import hashlib

SEED_DERIVATION_ITERATIONS = 1_000_000
DERIVED_SECRET_LENGTH = 32
SEED_LENGTH = 32
DATA_DERIVATION_ITERATIONS = 1_000


class Secret(bytes):
    def to_bytes(self) -> bytes:
        return self


class Seed(bytes):
    def to_bytes(self) -> bytes:
        return self


def pbkdf2_hmac_sha512(
    password: bytes, salt: bytes, iterations: int, length: int
) -> bytes:
    return hashlib.pbkdf2_hmac("sha512", password, salt, iterations, length)


def derive_seed_from_secret(secret: Secret) -> Seed:
    return Seed(
        pbkdf2_hmac_sha512(
            secret.to_bytes(), b"", SEED_DERIVATION_ITERATIONS, SEED_LENGTH
        )
    )


def derive_bytes(seed: Seed, salt: str, length: int) -> bytes:
    return pbkdf2_hmac_sha512(
        seed.to_bytes(),
        salt.encode("utf-8"),
        DATA_DERIVATION_ITERATIONS,
        length,
    )


def derive_secret(seed: Seed, salt: bytes) -> Secret:
    return Secret(derive_bytes(seed, salt, DERIVED_SECRET_LENGTH))


def derive_seed(seed: Seed, salt: bytes) -> Seed:
    return Seed(derive_seed_from_secret(derive_secret(seed, salt)))


def derive_seed_from_path(seed: Seed, path: List[str]) -> Seed:
    for branch in path:
        seed = derive_seed(seed, branch)

    return seed


def derive_bytes_from_path(seed: Seed, path: List[str], length: int) -> bytes:
    assert len(path) > 0
    seed = derive_seed_from_path(seed, path[:-1])
    return derive_bytes(seed, path[-1], length)
