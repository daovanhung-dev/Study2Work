from __future__ import annotations

from app.core.passwords import hash_password, password_needs_rehash, verify_password


def test_passwords_use_argon2id_without_exposing_plaintext() -> None:
    password = "temporary-root-password"
    password_hash = hash_password(password)

    assert password_hash.startswith("$argon2id$")
    assert password not in password_hash
    assert verify_password(password_hash, password)
    assert not verify_password(password_hash, "wrong-password")
    assert password_needs_rehash(password_hash) is False
