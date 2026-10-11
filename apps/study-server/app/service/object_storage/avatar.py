"""Cung cấp provider S3-compatible để tải avatar mà không khởi tạo cấu hình lúc app startup."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Protocol
from urllib.parse import urlsplit

import boto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]


class AvatarStorageProvider(Protocol):
    """Định nghĩa interace provider upload avatar để route có thể inject implementation giả."""

    def upload(
        self,
        *,
        user_id: int,
        content: bytes,
        content_type: str,
    ) -> str:
        """Tải nội dung avatar cho user lên storage và trả URL công khai."""


class AvatarStorageConfigurationError(RuntimeError):
    """Báo cấu hình Object Storage thiếu hoặc không hợp lệ mà không chứa giá trị cấu hình."""


@dataclass(frozen=True, slots=True)
class S3AvatarStorageConfiguration:
    """Giữ cấu hình S3 đã được kiểm tra với kiểu không nullable."""

    bucket: str
    region: str
    access_key_id: str
    secret_access_key: str
    public_base_url: str
    endpoint_url: str | None


class S3AvatarStorageProvider:
    """Tải avatar lên bucket S3-compatible theo object key cố định cho từng user."""

    def __init__(self, *, client_factory: Callable[..., Any] | None = None) -> None:
        """Lưu factory tùy chọn để kiểm thử adapter bằng client stub."""

        self._client_factory = client_factory or boto3.client

    def upload(
        self,
        *,
        user_id: int,
        content: bytes,
        content_type: str,
    ) -> str:
        """Đọc cấu hình process environment, ghi object và tạo URL từ public base URL."""

        storage_config = _read_storage_configuration()
        client_options: dict[str, Any] = {
            "region_name": storage_config.region,
            "aws_access_key_id": storage_config.access_key_id,
            "aws_secret_access_key": storage_config.secret_access_key,
            "config": Config(
                connect_timeout=5,
                read_timeout=30,
                retries={"total_max_attempts": 1},
            ),
        }
        if storage_config.endpoint_url:
            client_options["endpoint_url"] = storage_config.endpoint_url

        try:
            client = self._client_factory("s3", **client_options)
            object_key = f"avatars/{user_id}"
            client.put_object(
                Bucket=storage_config.bucket,
                Key=object_key,
                Body=content,
                ContentType=content_type,
            )
        except Exception:
            raise RuntimeError("Avatar storage upload failed.") from None

        return f"{storage_config.public_base_url.rstrip('/')}/{object_key}"


def get_avatar_storage_provider() -> AvatarStorageProvider:
    """Tạo provider S3 lazy; thiếu cấu hình chỉ phát sinh lỗi khi endpoint upload được gọi."""

    return S3AvatarStorageProvider()


def _read_storage_configuration() -> S3AvatarStorageConfiguration:
    """Đọc các biến process environment bắt buộc mà không trả giá trị cấu hình trong lỗi."""

    bucket = os.environ.get("OBJECT_STORAGE_BUCKET", "").strip()
    region = os.environ.get("OBJECT_STORAGE_REGION", "").strip()
    access_key_id = os.environ.get("OBJECT_STORAGE_ACCESS_KEY_ID", "").strip()
    secret_access_key = os.environ.get("OBJECT_STORAGE_SECRET_ACCESS_KEY", "").strip()
    public_base_url = os.environ.get("OBJECT_STORAGE_PUBLIC_BASE_URL", "").strip()
    if not all((bucket, region, access_key_id, secret_access_key, public_base_url)):
        raise AvatarStorageConfigurationError("Object Storage configuration is incomplete.")

    parsed_public_url = urlsplit(public_base_url)
    if parsed_public_url.scheme not in {"http", "https"} or not parsed_public_url.netloc:
        raise AvatarStorageConfigurationError("Object Storage public URL is invalid.")

    endpoint_url = os.environ.get("OBJECT_STORAGE_ENDPOINT_URL", "").strip() or None
    return S3AvatarStorageConfiguration(
        bucket=bucket,
        region=region,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        public_base_url=public_base_url,
        endpoint_url=endpoint_url,
    )
