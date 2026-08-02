from app.core.security import hash_password, verify_password


def test_hash_password_can_be_verified() -> None:
    password_hash = hash_password("correct horse battery staple")

    assert password_hash.startswith("$2")
    assert verify_password("correct horse battery staple", password_hash) is True
    assert verify_password("wrong password", password_hash) is False
