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
) -> bool:
    """Verify a password against Argon2id or legacy bcrypt."""

    if hashed_password.startswith("$argon2"):
        return _verify_argon2(password, hashed_password)

    if hashed_password.startswith(("$2a$", "$2b$", "$2y$")):
        return _verify_bcrypt(password, hashed_password)

    return False


def needs_password_rehash(hashed_password: str) -> bool:
    """Return whether the stored password should be upgraded."""

    if not hashed_password.startswith("$argon2"):
        return True

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
