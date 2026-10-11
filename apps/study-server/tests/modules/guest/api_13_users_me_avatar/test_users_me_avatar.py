from __future__ import annotations

import base64
from typing import Any, cast

import app.utils.auth as auth_utils
import boto3  # type: ignore[import-untyped]
import pytest
from app.core.database import get_db
from app.modules.guest.api_13_users_me_avatar.validate import (
    AvatarImage,
    AvatarInputError,
    parse_avatar_data_url,
)
from app.service.object_storage.avatar import (
    AvatarStorageConfigurationError,
    S3AvatarStorageProvider,
    get_avatar_storage_provider,
)
from botocore.config import Config  # type: ignore[import-untyped]
from botocore.stub import Stubber  # type: ignore[import-untyped]
from fastapi import FastAPI
from fastapi.testclient import TestClient

PNG_CONTENT = b"\x89PNG\r\n\x1a\n" + b"png-data"
JPEG_CONTENT = b"\xff\xd8\xff" + b"jpeg-data"
WEBP_CONTENT = b"RIFF" + b"\x00\x00\x00\x00" + b"WEBP" + b"webp-data"


class FakeAvatarStorageProvider:
    """Ghi lại yêu cầu upload hoặc phát sinh lỗi để kiểm tra route không gọi storage thật."""

    def __init__(self, error: Exception | None = None) -> None:
        """Khởi tạo provider giả với lỗi upload tùy chọn."""

        self.error = error
        self.upload_calls: list[dict[str, Any]] = []

    def upload(self, *, user_id: int, content: bytes, content_type: str) -> str:
        """Ghi lại payload và trả URL giả hoặc phát sinh lỗi đã cấu hình."""

        self.upload_calls.append(
            {
                "user_id": user_id,
                "content": content,
                "content_type": content_type,
            }
        )
        if self.error is not None:
            raise self.error
        return f"https://cdn.example.test/avatars/{user_id}"


def data_url(content_type: str, content: bytes) -> str:
    """Mã hóa bytes thành Data URL để tái sử dụng trong test request và parser."""

    encoded_content = base64.b64encode(content).decode("ascii")
    return f"data:{content_type};base64,{encoded_content}"


def student_claims() -> dict[str, Any]:
    """Tạo claim hợp lệ cho một Student có user ID 1001."""

    return {"sub": "1001", "roles": ["STUDENT"]}


def valid_payload() -> dict[str, str]:
    """Tạo JSON body có chữ ký PNG hợp lệ cho API #13."""

    return {"image": data_url("image/png", PNG_CONTENT)}


def install_storage_provider(
    client: TestClient,
    provider: FakeAvatarStorageProvider,
) -> None:
    """Thay dependency storage để route test không kết nối Object Storage thật."""

    cast(FastAPI, client.app).dependency_overrides[get_avatar_storage_provider] = lambda: provider


@pytest.mark.parametrize(
    ("content_type", "content"),
    [
        ("image/png", PNG_CONTENT),
        ("image/jpeg", JPEG_CONTENT),
        ("image/webp", WEBP_CONTENT),
    ],
)
def test_parse_avatar_data_url_accepts_supported_images(
    content_type: str,
    content: bytes,
) -> None:
    """Kiểm tra parser chấp nhận Data URL của PNG, JPEG và WebP có chữ ký phù hợp."""

    parsed = parse_avatar_data_url(data_url(content_type, content))

    assert parsed == AvatarImage(content=content, content_type=content_type)


@pytest.mark.parametrize(
    ("value", "expected_code"),
    [
        ("", "INVALID_DATA_URL"),
        ("https://cdn.example.test/avatar.png", "INVALID_DATA_URL"),
        ("data:image/gif;base64,AA==", "INVALID_DATA_URL"),
        ("data:image/png;base64,", "EMPTY_IMAGE"),
        ("data:image/png;base64,A", "INVALID_BASE64"),
        ("data:image/png;base64,%%%", "INVALID_DATA_URL"),
        (data_url("image/jpeg", PNG_CONTENT), "IMAGE_SIGNATURE_MISMATCH"),
        (data_url("image/png", JPEG_CONTENT), "IMAGE_SIGNATURE_MISMATCH"),
    ],
)
def test_parse_avatar_data_url_rejects_invalid_input(
    value: str,
    expected_code: str,
) -> None:
    """Kiểm tra parser từ chối chuỗi rỗng/sai, MIME ngoài allowlist và chữ ký không khớp."""

    with pytest.raises(AvatarInputError) as error:
        parse_avatar_data_url(value)

    assert error.value.code == expected_code


def test_parse_avatar_data_url_rejects_content_over_five_mib() -> None:
    """Kiểm tra giới hạn tính theo payload đã giải mã thay vì chuỗi base64."""

    oversized_content = b"\x89PNG\r\n\x1a\n" + b"x" * (5 * 1024 * 1024)

    with pytest.raises(AvatarInputError, match="5 MiB") as error:
        parse_avatar_data_url(data_url("image/png", oversized_content))

    assert error.value.code == "IMAGE_TOO_LARGE"


def test_parse_avatar_data_url_accepts_exactly_five_mib() -> None:
    """Kiểm tra payload đúng 5 MiB được nhận vì giới hạn là bao gồm."""

    max_size_content = b"\x89PNG\r\n\x1a\n" + b"x" * (5 * 1024 * 1024 - 8)

    parsed = parse_avatar_data_url(data_url("image/png", max_size_content))

    assert len(parsed.content) == 5 * 1024 * 1024


def test_upload_avatar_returns_public_url_and_does_not_use_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra response 201 chỉ có avatar_url và route không gọi database."""

    provider = FakeAvatarStorageProvider()
    install_storage_provider(client, provider)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: student_claims())
    database_calls: list[bool] = []

    def unexpected_database_access() -> None:
        """Ghi nhận việc route yêu cầu DB nếu xuất hiện dependency ngoài contract."""

        database_calls.append(True)
        raise AssertionError("API #13 must not use the database")

    cast(FastAPI, client.app).dependency_overrides[get_db] = unexpected_database_access
    response = client.post(
        "/api/v1/users/me/avatar",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 201
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert response.json()["data"] == {
        "avatar_url": "https://cdn.example.test/avatars/1001",
    }
    assert set(response.json()["data"]) == {"avatar_url"}
    assert provider.upload_calls == [
        {
            "user_id": 1001,
            "content": PNG_CONTENT,
            "content_type": "image/png",
        }
    ]
    assert database_calls == []


def test_upload_avatar_requires_student_bearer_before_storage(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra thiếu token trả 401 và role khác Student trả 403 trước khi gọi storage."""

    provider = FakeAvatarStorageProvider()
    install_storage_provider(client, provider)
    missing_auth_response = client.post(
        "/api/v1/users/me/avatar",
        json=valid_payload(),
    )

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": ["MENTOR"]},
    )
    wrong_role_response = client.post(
        "/api/v1/users/me/avatar",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert missing_auth_response.status_code == 401
    assert missing_auth_response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert wrong_role_response.status_code == 403
    assert wrong_role_response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert provider.upload_calls == []


@pytest.mark.parametrize(
    "payload",
    [
        {},
        {"image": None},
        {"image": 5},
        {"image": data_url("image/png", PNG_CONTENT), "extra": "not allowed"},
        {"image": "data:image/png;base64,A"},
        {"image": data_url("image/png", JPEG_CONTENT)},
    ],
)
def test_upload_avatar_rejects_invalid_request_before_storage(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    payload: dict[str, Any],
) -> None:
    """Kiểm tra body sai schema, Data URL lỗi và MIME không khớp đều trả 422 an toàn."""

    provider = FakeAvatarStorageProvider()
    install_storage_provider(client, provider)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: student_claims())

    response = client.post(
        "/api/v1/users/me/avatar",
        headers={"Authorization": "Bearer access-token"},
        json=payload,
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert provider.upload_calls == []


@pytest.mark.parametrize(
    "provider_error",
    [
        RuntimeError("provider key secret detail"),
        TimeoutError("provider timeout secret detail"),
    ],
)
def test_upload_avatar_maps_storage_failure_to_safe_internal_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    provider_error: Exception,
) -> None:
    """Kiểm tra lỗi provider và timeout trả 500 mà không lộ nội dung exception."""

    provider = FakeAvatarStorageProvider(error=provider_error)
    install_storage_provider(client, provider)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: student_claims())

    response = client.post(
        "/api/v1/users/me/avatar",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["message"] == "Avatar could not be uploaded."
    assert "provider key secret detail" not in response.text
    assert "provider timeout secret detail" not in response.text


def test_missing_storage_configuration_fails_only_on_avatar_request(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra thiếu cấu hình không chặn app khởi động và endpoint trả 500 an toàn."""

    for name in (
        "OBJECT_STORAGE_BUCKET",
        "OBJECT_STORAGE_REGION",
        "OBJECT_STORAGE_ACCESS_KEY_ID",
        "OBJECT_STORAGE_SECRET_ACCESS_KEY",
        "OBJECT_STORAGE_PUBLIC_BASE_URL",
    ):
        monkeypatch.delenv(name, raising=False)
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: student_claims())

    response = client.post(
        "/api/v1/users/me/avatar",
        headers={"Authorization": "Bearer access-token"},
        json=valid_payload(),
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "configuration" not in response.text
    assert "OBJECT_STORAGE" not in response.text


def test_s3_avatar_provider_uploads_expected_object_with_boto_stub(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra adapter dùng client stub, object key cố định, MIME, URL và timeout đã chốt."""

    monkeypatch.setenv("OBJECT_STORAGE_BUCKET", "study-public")
    monkeypatch.setenv("OBJECT_STORAGE_REGION", "us-east-1")
    monkeypatch.setenv("OBJECT_STORAGE_ACCESS_KEY_ID", "test-access-key")
    monkeypatch.setenv("OBJECT_STORAGE_SECRET_ACCESS_KEY", "test-secret-key")
    monkeypatch.setenv("OBJECT_STORAGE_PUBLIC_BASE_URL", "https://cdn.example.test/assets/")
    monkeypatch.setenv("OBJECT_STORAGE_ENDPOINT_URL", "https://s3.example.test")

    client = boto3.session.Session().client(
        "s3",
        region_name="us-east-1",
        aws_access_key_id="test-access-key",
        aws_secret_access_key="test-secret-key",
        endpoint_url="https://s3.example.test",
        config=Config(
            connect_timeout=5,
            read_timeout=30,
            retries={"total_max_attempts": 1},
        ),
    )
    stubber = Stubber(client)
    stubber.add_response(
        "put_object",
        {"ETag": '"avatar-etag"'},
        expected_params={
            "Bucket": "study-public",
            "Key": "avatars/1001",
            "Body": PNG_CONTENT,
            "ContentType": "image/png",
        },
    )
    client_options: dict[str, Any] = {}

    def client_factory(service_name: str, **options: Any) -> Any:
        """Ghi lại client options rồi trả boto3 client được Stubber kiểm soát."""

        client_options.update(service_name=service_name, **options)
        return client

    with stubber:
        provider = S3AvatarStorageProvider(client_factory=client_factory)
        avatar_url = provider.upload(
            user_id=1001,
            content=PNG_CONTENT,
            content_type="image/png",
        )

    assert avatar_url == "https://cdn.example.test/assets/avatars/1001"
    assert client_options["service_name"] == "s3"
    assert client_options["endpoint_url"] == "https://s3.example.test"
    assert client_options["aws_access_key_id"] == "test-access-key"
    assert client_options["aws_secret_access_key"] == "test-secret-key"
    assert client_options["config"].connect_timeout == 5
    assert client_options["config"].read_timeout == 30
    assert client_options["config"].retries["total_max_attempts"] == 1
    stubber.assert_no_pending_responses()


def test_s3_avatar_provider_rejects_missing_configuration_without_client() -> None:
    """Kiểm tra cấu hình bắt buộc thiếu được phát hiện trước khi tạo boto3 client."""

    provider = S3AvatarStorageProvider(client_factory=lambda *_args, **_kwargs: pytest.fail())

    with pytest.raises(AvatarStorageConfigurationError):
        provider.upload(
            user_id=1001,
            content=PNG_CONTENT,
            content_type="image/png",
        )
