"""Password hashing and verification."""

from __future__ import annotations

import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

_password_hasher = PasswordHasher(
    time_cost=3,
    memory_cost=64 * 1024,
    parallelism=1,
)


def hash_password(password: str) -> str:
    """Hash a new password using Argon2id."""

    return _password_hasher.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
    """Verify a password against Argon2id or legacy bcrypt.

    ``algorithm`` is retained as an optional compatibility argument for older
    callers. When omitted, the hash prefix determines the verification method.
    """

    normalized_algorithm = algorithm.upper() if algorithm else None

    if normalized_algorithm in {"ARGON2", "ARGON2ID"}:
        return _verify_argon2(password, hashed_password)

    if normalized_algorithm == "BCRYPT":
        return _verify_bcrypt(password, hashed_password)

    if normalized_algorithm is not None:
        return False

    if hashed_password.startswith("$argon2"):
        return _verify_argon2(password, hashed_password)

    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        return _verify_bcrypt(password, hashed_password)

    return False


def needs_password_rehash(
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
    """Return whether the stored password should be upgraded."""

    normalized_algorithm = algorithm.upper() if algorithm else None
    if normalized_algorithm == "BCRYPT":
        return True
    if normalized_algorithm in {"ARGON2", "ARGON2ID"}:
        return _needs_argon2_rehash(hashed_password)
    if normalized_algorithm is not None:
        return True

    if not hashed_password.startswith("$argon2"):
        return True

    return _needs_argon2_rehash(hashed_password)


def _needs_argon2_rehash(hashed_password: str) -> bool:
    try:
        return _password_hasher.check_needs_rehash(hashed_password)
    except (InvalidHashError, TypeError):
        return True


def _verify_argon2(
    password: str,
    hashed_password: str,
) -> bool:
    try:
        return _password_hasher.verify(
            hashed_password,
            password,
        )
    except (
        VerifyMismatchError,
        VerificationError,
        InvalidHashError,
    ):
        return False


def _verify_bcrypt(
    password: str,
    hashed_password: str,
) -> bool:
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False
