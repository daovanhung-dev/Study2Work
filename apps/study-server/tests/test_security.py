import bcrypt
from app.core.security import hash_password, needs_password_rehash, verify_password


def test_hash_password_can_be_verified() -> None:
    """Kiểm tra mật khẩu mới được băm Argon2id và hash xác minh được mật khẩu gốc."""
    password_hash = hash_password("correct horse battery staple")

    assert password_hash.startswith("$argon2id$")
    assert verify_password("correct horse battery staple", password_hash) is True
    assert verify_password("wrong password", password_hash) is False
    assert needs_password_rehash(password_hash) is False


def test_legacy_bcrypt_hash_can_still_be_verified() -> None:
    """Kiểm tra hash bcrypt cũ vẫn xác minh được để giữ tương thích tài khoản legacy."""
    password_hash = bcrypt.hashpw(
        b"correct horse battery staple",
        bcrypt.gensalt(),
    ).decode("utf-8")

    assert verify_password("correct horse battery staple", password_hash, "BCRYPT") is True
    assert verify_password("wrong password", password_hash, "BCRYPT") is False
    assert needs_password_rehash(password_hash, "BCRYPT") is True
