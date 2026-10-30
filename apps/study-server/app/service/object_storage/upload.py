"""Cung cấp upload/delete S3-compatible dùng chung cho metadata API #34."""

from __future__ import annotations

import os
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, BinaryIO, Protocol
from urllib.parse import urlsplit

import boto3  # type: ignore[import-untyped]
from botocore.config import Config  # type: ignore[import-untyped]


class UploadStorageProvider(Protocol):
    """Giao diện Object Storage có thể thay thế trong route và kiểm thử."""

    def upload(self, *, storage_key: str, file_obj: BinaryIO, content_type: str) -> str:
        """Tải stream lên storage và trả URL công khai của object."""

    def delete(self, *, storage_key: str) -> None:
        """Xóa object theo key khi ghi metadata thất bại."""


class UploadStorageUnavailableError(RuntimeError):
    """Báo cấu hình hoặc thao tác storage lỗi mà không chứa thông tin nhạy cảm."""


@dataclass(frozen=True, slots=True)
class S3UploadStorageConfiguration:
    """Giữ các giá trị S3 đã kiểm tra để khởi tạo client lazy."""

    bucket: str
    region: str
    access_key_id: str
    secret_access_key: str
    public_base_url: str
    endpoint_url: str | None


class S3UploadStorageProvider:
    """Upload stream S3-compatible với key do API caller sinh bằng UUID."""

    def __init__(self, *, client_factory: Callable[..., Any] | None = None) -> None:
        """Lưu factory tùy chọn để kiểm thử adapter mà không gọi storage thật."""

        self._client_factory = client_factory or boto3.client

    def upload(self, *, storage_key: str, file_obj: BinaryIO, content_type: str) -> str:
        """Đọc cấu hình, gửi stream lên bucket và tạo URL từ public base URL."""

        storage_config = _read_storage_configuration()
        try:
            client = self._create_client(storage_config)
            client.upload_fileobj(
                file_obj,
                storage_config.bucket,
                storage_key,
                ExtraArgs={"ContentType": content_type},
            )
        except Exception:
            raise UploadStorageUnavailableError("Object Storage upload failed.") from None
        return f"{storage_config.public_base_url.rstrip('/')}/{storage_key}"

    def delete(self, *, storage_key: str) -> None:
        """Gọi delete_object để dọn object sau khi giao dịch metadata thất bại."""

        storage_config = _read_storage_configuration()
        try:
            client = self._create_client(storage_config)
            client.delete_object(Bucket=storage_config.bucket, Key=storage_key)
        except Exception:
            raise UploadStorageUnavailableError("Object Storage delete failed.") from None

    def _create_client(self, storage_config: S3UploadStorageConfiguration) -> Any:
        """Tạo client với timeout ngắn và một lần thử như adapter storage hiện có."""

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
        return self._client_factory("s3", **client_options)


def get_upload_storage_provider() -> UploadStorageProvider:
    """Tạo provider lazy để thiếu cấu hình không chặn app startup."""

    return S3UploadStorageProvider()


def _read_storage_configuration() -> S3UploadStorageConfiguration:
    """Đọc cấu hình S3 bắt buộc mà không đưa giá trị cấu hình vào thông báo lỗi."""

    bucket = os.environ.get("OBJECT_STORAGE_BUCKET", "").strip()
    region = os.environ.get("OBJECT_STORAGE_REGION", "").strip()
    access_key_id = os.environ.get("OBJECT_STORAGE_ACCESS_KEY_ID", "").strip()
    secret_access_key = os.environ.get("OBJECT_STORAGE_SECRET_ACCESS_KEY", "").strip()
    public_base_url = os.environ.get("OBJECT_STORAGE_PUBLIC_BASE_URL", "").strip()
    if not all((bucket, region, access_key_id, secret_access_key, public_base_url)):
        raise UploadStorageUnavailableError("Object Storage configuration is incomplete.")

    parsed_public_url = urlsplit(public_base_url)
    if parsed_public_url.scheme not in {"http", "https"} or not parsed_public_url.netloc:
        raise UploadStorageUnavailableError("Object Storage public URL is invalid.")

    endpoint_url = os.environ.get("OBJECT_STORAGE_ENDPOINT_URL", "").strip() or None
    return S3UploadStorageConfiguration(
        bucket=bucket,
        region=region,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        public_base_url=public_base_url,
        endpoint_url=endpoint_url,
    )
