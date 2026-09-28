"""Băm mật khẩu mới bằng Argon2id và xác minh cả định dạng Argon2id lẫn bcrypt cũ còn được hỗ
trợ."""

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
    """Băm mật khẩu mới bằng PasswordHasher Argon2id đã cấu hình. Giá trị hash trả về chứa tham số
    thuật toán và không lưu mật khẩu gốc."""

    return _password_hasher.hash(password)


def verify_password(
    password: str,
    hashed_password: str,
    algorithm: str | None = None,
) -> bool:
    """Xác minh mật khẩu gốc với hash Argon2id hoặc bcrypt cũ. Nếu caller truyền algorithm, hàm
    dùng lựa chọn tương thích đó; nếu bỏ qua, tiền tố hash quyết định bộ xác minh. Trả False khi
    thuật toán không được hỗ trợ hoặc hash/mật khẩu không khớp."""

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
    """Quyết định hash đã lưu có cần nâng cấp hay không. Bcrypt, định dạng không nhận diện và thuật
    toán cũ không còn hỗ trợ được đánh dấu cần tạo hash mới; Argon2id được so với tham số hiện
    hành."""

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
    """Hỏi PasswordHasher liệu hash Argon2id có dùng tham số đã cũ hay không. Hash lỗi định dạng
    hoặc kiểu dữ liệu không hợp lệ được xem là cần rehash để không giữ lại credential không thể
    kiểm tra an toàn."""
    try:
        return _password_hasher.check_needs_rehash(hashed_password)
    except (InvalidHashError, TypeError):
        return True


def _verify_argon2(
    password: str,
    hashed_password: str,
) -> bool:
    """Xác minh password với hash Argon2 qua PasswordHasher. Trả True khi khớp và False cho trường
    hợp password sai, hash hỏng hoặc lỗi xác minh được thư viện báo."""
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
    """Xác minh password với hash bcrypt bằng cách mã hóa hai chuỗi thành UTF-8 rồi gọi
    bcrypt.checkpw. Trả False nếu hash hoặc kiểu dữ liệu gây ValueError hay TypeError."""
    try:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )
    except (ValueError, TypeError):
        return False
