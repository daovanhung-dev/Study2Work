"""Password hashing for DB Admin application accounts."""

from __future__ import annotations

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHash, VerificationError, VerifyMismatchError

# Keep the Argon2id profile explicit and shared by bootstrap, login and
# password rotation. Password values never enter logs or audit metadata.
_HASHER = PasswordHasher(time_cost=3, memory_cost=64 * 1024, parallelism=1)


def hash_password(password: str) -> str:
    return _HASHER.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        return _HASHER.verify(password_hash, password)
    except (InvalidHash, VerificationError, VerifyMismatchError):
        return False


def password_needs_rehash(password_hash: str) -> bool:
    try:
        return _HASHER.check_needs_rehash(password_hash)
    except (InvalidHash, VerificationError):
        return True
