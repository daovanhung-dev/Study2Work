"""Kiểm tra Data URL avatar và Student Bearer cho API #13."""

from __future__ import annotations

import base64
import binascii
import re
from dataclasses import dataclass

from app.core.responses import ErrorDetail, error_response
from app.modules.guest.api_13_users_me_avatar.models import AvatarUploadRequest
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

MAX_AVATAR_BYTES = 5 * 1024 * 1024
DATA_URL_PATTERN = re.compile(r"data:(image/(?:png|jpeg|webp));base64,([A-Za-z0-9+/]*={0,2})\Z")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
JPEG_SIGNATURE = b"\xff\xd8\xff"


@dataclass(frozen=True, slots=True)
class AvatarImage:
    """Giữ payload ảnh đã giải mã cùng MIME đã được kiểm tra chữ ký."""

    content: bytes
    content_type: str


class AvatarInputError(ValueError):
    """Mô tả lỗi Data URL để validator ánh xạ thành field error an toàn."""

    def __init__(self, code: str, message: str) -> None:
        """Lưu mã và thông điệp kiểm tra không chứa nội dung ảnh đầu vào."""

        super().__init__(message)
        self.code = code


def parse_avatar_data_url(value: str) -> AvatarImage:
    """Giải mã Data URL và kiểm tra MIME, chữ ký ảnh cùng giới hạn 5 MiB."""

    match = DATA_URL_PATTERN.fullmatch(value)
    if match is None:
        raise AvatarInputError(
            "INVALID_DATA_URL",
            "Image must be a PNG, JPEG, or WebP base64 Data URL.",
        )

    content_type, encoded_content = match.groups()
    if not encoded_content:
        raise AvatarInputError("EMPTY_IMAGE", "Image data must not be empty.")

    try:
        content = base64.b64decode(encoded_content, validate=True)
    except (binascii.Error, ValueError):
        raise AvatarInputError("INVALID_BASE64", "Image data is not valid base64.") from None

    if not content:
        raise AvatarInputError("EMPTY_IMAGE", "Image data must not be empty.")
    if len(content) > MAX_AVATAR_BYTES:
        raise AvatarInputError(
            "IMAGE_TOO_LARGE",
            "Image must not exceed 5 MiB after decoding.",
        )
    if not _signature_matches(content_type, content):
        raise AvatarInputError(
            "IMAGE_SIGNATURE_MISMATCH",
            "Image content does not match its declared MIME type.",
        )

    return AvatarImage(content=content, content_type=content_type)


def validate_avatar_upload_request(
    authorization: str | None,
    user_data: AvatarUploadRequest,
    *,
    trace_id: str,
) -> tuple[int, AvatarImage] | JSONResponse:
    """Xác thực Student trước, sau đó giải mã và kiểm tra Data URL avatar."""

    authentication = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    user_id, _roles = authentication

    try:
        avatar_image = parse_avatar_data_url(user_data.image)
    except AvatarInputError as exc:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Avatar input is invalid.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="image",
                    code=exc.code,
                    message=str(exc),
                )
            ],
        )

    return user_id, avatar_image


def _signature_matches(content_type: str, content: bytes) -> bool:
    """So khớp chữ ký file tối thiểu với MIME đã khai báo trong Data URL."""

    if content_type == "image/png":
        return content.startswith(PNG_SIGNATURE)
    if content_type == "image/jpeg":
        return content.startswith(JPEG_SIGNATURE)
    if content_type == "image/webp":
        return len(content) >= 12 and content.startswith(b"RIFF") and content[8:12] == b"WEBP"
    return False
