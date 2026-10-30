from __future__ import annotations

from io import BytesIO
from typing import Any, BinaryIO, cast

import app.modules.student.api_34_uploads.view as upload_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.student.api_34_uploads.models import UploadPurpose
from app.service.object_storage.upload import S3UploadStorageProvider, get_upload_storage_provider
from fastapi import FastAPI
from fastapi.testclient import TestClient
from starlette.datastructures import UploadFile as StarletteUploadFile


class FakeSession:
    """Theo dõi commit/rollback để xác nhận API #34 sở hữu transaction."""

    def __init__(self, *, commit_error: Exception | None = None) -> None:
        """Khởi tạo bộ đếm transaction và lỗi commit tùy chọn."""

        self.commit_error = commit_error
        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận commit hoặc phát sinh lỗi đã cấu hình."""

        self.commit_count += 1
        if self.commit_error is not None:
            raise self.commit_error

    def rollback(self) -> None:
        """Ghi nhận rollback khi quyền hoặc metadata thất bại."""

        self.rollback_count += 1


class FakeUploadStorageProvider:
    """Ghi nhận stream upload/delete để kiểm tra side effect ngoài hệ thống."""

    def __init__(self, *, upload_error: Exception | None = None) -> None:
        """Khởi tạo provider giả với lỗi upload tùy chọn."""

        self.upload_error = upload_error
        self.upload_calls: list[dict[str, Any]] = []
        self.delete_calls: list[str] = []

    def upload(self, *, storage_key: str, file_obj: BinaryIO, content_type: str) -> str:
        """Đọc stream đã rewind, lưu tham số upload và trả URL giả."""

        content = file_obj.read()
        self.upload_calls.append(
            {
                "storage_key": storage_key,
                "content": content,
                "content_type": content_type,
            }
        )
        if self.upload_error is not None:
            raise self.upload_error
        return f"https://cdn.example.test/{storage_key}"

    def delete(self, *, storage_key: str) -> None:
        """Ghi nhận yêu cầu dọn object."""

        self.delete_calls.append(storage_key)


def override_db(session: FakeSession):
    """Tạo dependency cung cấp session giả cho route API #34."""

    def dependency():
        """Yield session giả được giữ trong closure của test."""

        yield session

    return dependency


def install_route_dependencies(
    client: TestClient,
    *,
    session: FakeSession,
    provider: FakeUploadStorageProvider,
) -> None:
    """Thay database và Object Storage để HTTP test không dùng dịch vụ thật."""

    cast(FastAPI, client.app).dependency_overrides[get_db] = override_db(session)
    cast(FastAPI, client.app).dependency_overrides[get_upload_storage_provider] = lambda: provider


def allow_student_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Cung cấp claims Student hợp lệ mà không cần ký JWT trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": ["STUDENT"]},
    )


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Cung cấp claims Mentor hợp lệ mà không cần ký JWT trong test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "2002", "roles": ["MENTOR"]},
    )


def fake_query_one(calls: list[dict[str, Any]], *, insert_error: Exception | None = None):
    """Tạo query stub cho enrollment, direct owner và metadata INSERT."""

    def query_one(db, query: str, params: dict[str, Any]):
        """Ghi nhận SQL/params và trả kết quả theo loại truy vấn."""

        calls.append({"query": query, "params": params})
        if "INSERT INTO uploads" in query:
            if insert_error is not None:
                raise insert_error
            return {"id": 34001}
        if "FROM enrollments" in query or "FROM courses" in query:
            return {"id": 1}
        raise AssertionError("Unexpected API #34 query")

    return query_one


def test_student_submission_upload_persists_metadata_and_returns_asset(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra Student upload đo byte thật, sinh UUID key và commit UploadAsset."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_student_token(monkeypatch)
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(upload_view, "query_one", fake_query_one(calls))

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "SUBMISSION"},
        files={"file": ("report.bin", b"binary\x00content", "application/x-example")},
    )

    assert response.status_code == 201
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert response.json()["data"] == {
        "id": 34001,
        "name": "report.bin",
        "url": f"https://cdn.example.test/{provider.upload_calls[0]['storage_key']}",
        "content_type": "application/x-example",
        "size_bytes": len(b"binary\x00content"),
        "status": "UPLOADED",
    }
    assert provider.upload_calls[0]["storage_key"].startswith("uploads/")
    assert len(provider.upload_calls[0]["storage_key"]) == len("uploads/") + 36
    assert provider.upload_calls[0]["content"] == b"binary\x00content"
    assert calls == [
        {
            "query": upload_view.INSERT_UPLOAD_ASSET,
            "params": {
                "owner_id": 1001,
                "purpose": "SUBMISSION",
                "course_id": None,
                "storage_key": provider.upload_calls[0]["storage_key"],
                "file_name": "report.bin",
                "url": response.json()["data"]["url"],
                "content_type": "application/x-example",
                "size_bytes": len(b"binary\x00content"),
            },
        }
    ]
    assert session.commit_count == 1
    assert session.rollback_count == 0
    assert provider.delete_calls == []


def test_student_submission_with_course_requires_active_enrollment(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra course_id của Student chỉ upload khi enrollment ACTIVE tồn tại."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_student_token(monkeypatch)
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(upload_view, "query_one", fake_query_one(calls))

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "SUBMISSION", "course_id": "123"},
        files={"file": ("work.pdf", b"pdf", "application/pdf")},
    )

    assert response.status_code == 201
    assert "FROM enrollments" in calls[0]["query"]
    assert calls[0]["params"] == {"student_id": 1001, "course_id": 123}
    assert calls[1]["params"]["course_id"] == 123


def test_student_without_active_enrollment_is_denied_before_storage(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra enrollment không có hàng ACTIVE trả 403 trước khi upload object."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_student_token(monkeypatch)
    monkeypatch.setattr(upload_view, "query_one", lambda *_args, **_kwargs: None)

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "SUBMISSION", "course_id": "123"},
        files={"file": ("work.pdf", b"pdf", "application/pdf")},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert provider.upload_calls == []
    assert session.rollback_count == 1


def test_mentor_lecture_requires_direct_course_owner(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra Mentor ghi metadata cho course được courses.mentor_id trực tiếp sở hữu."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_mentor_token(monkeypatch)
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(upload_view, "query_one", fake_query_one(calls))

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "LECTURE", "course_id": "123"},
        files={"file": ("slide.pptx", b"slides", "application/vnd.ms-powerpoint")},
    )

    assert response.status_code == 201
    assert "c.mentor_id = :mentor_id" in calls[0]["query"]
    assert calls[0]["params"] == {"mentor_id": 2002, "course_id": 123}


def test_mentor_course_not_directly_owned_is_denied_before_storage(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra course không khớp direct owner trả 403 mà không tạo object."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(upload_view, "query_one", lambda *_args, **_kwargs: None)

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "LECTURE", "course_id": "123"},
        files={"file": ("slide.pptx", b"slides", "application/vnd.ms-powerpoint")},
    )

    assert response.status_code == 403
    assert provider.upload_calls == []


@pytest.mark.parametrize(
    ("role", "purpose"),
    [("STUDENT", "LECTURE"), ("MENTOR", "SUBMISSION")],
)
def test_role_purpose_mismatch_is_denied_before_database_or_storage(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    role: str,
    purpose: str,
) -> None:
    """Kiểm tra role chỉ dùng purpose tương ứng và bị chặn trước DB/storage."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "1001", "roles": [role]},
    )
    monkeypatch.setattr(
        upload_view,
        "query_one",
        lambda *_args, **_kwargs: pytest.fail("Role mismatch must not query DB"),
    )

    data = {"purpose": purpose}
    if purpose == "LECTURE":
        data["course_id"] = "123"
    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data=data,
        files={"file": ("report.bin", b"data", "application/octet-stream")},
    )

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert provider.upload_calls == []


@pytest.mark.parametrize(
    ("data", "files"),
    [
        ({}, {"file": ("report.bin", b"data", "application/octet-stream")}),
        ({"purpose": "SUBMISSION"}, {}),
        ({"purpose": "OTHER"}, {"file": ("report.bin", b"data", "application/octet-stream")}),
        ({"purpose": "LECTURE"}, {"file": ("report.bin", b"data", "application/octet-stream")}),
        (
            {"purpose": "SUBMISSION", "course_id": "not-an-integer"},
            {"file": ("report.bin", b"data", "application/octet-stream")},
        ),
    ],
)
def test_malformed_multipart_fields_return_422_before_storage(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    data: dict[str, str],
    files: dict[str, tuple[str, bytes, str | None]],
) -> None:
    """Kiểm tra multipart thiếu/sai field và thiếu course LECTURE trả 422."""

    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=FakeSession(), provider=provider)
    if data.get("purpose") == "LECTURE":
        allow_mentor_token(monkeypatch)
    else:
        allow_student_token(monkeypatch)

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data=data,
        files=files,
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert provider.upload_calls == []


def test_missing_content_type_uses_contract_fallback(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra part file không có Content-Type dùng MIME fallback đã chốt."""

    session = FakeSession()
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_student_token(monkeypatch)
    monkeypatch.setattr(upload_view, "query_one", fake_query_one([]))

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "SUBMISSION"},
        files={"file": ("no-type.bin", b"raw", None)},
    )

    assert response.status_code == 201
    assert response.json()["data"]["name"] == "no-type.bin"
    assert response.json()["data"]["content_type"] == "application/octet-stream"


def test_missing_filename_uses_contract_fallback(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra UploadFile không có filename dùng tên mặc định upload."""

    allow_student_token(monkeypatch)
    monkeypatch.setattr(upload_view, "query_one", fake_query_one([]))
    session = FakeSession()
    provider = FakeUploadStorageProvider()
    uploaded_file = StarletteUploadFile(file=BytesIO(b"raw"), filename=None)

    response = upload_view.create_upload(
        authorization="Bearer access-token",
        file=uploaded_file,
        purpose=UploadPurpose.SUBMISSION,
        course_id=None,
        db=session,
        provider=provider,
        trace_id="00000000-0000-0000-0000-000000000034",
    )

    assert isinstance(response, dict)
    assert response["data"]["name"] == "upload"
    assert response["data"]["content_type"] == "application/octet-stream"


def test_storage_failure_returns_503_and_attempts_cleanup(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra lỗi Object Storage trả 503 và thử xóa key có thể đã được tạo một phần."""

    session = FakeSession()
    provider = FakeUploadStorageProvider(upload_error=RuntimeError("private storage detail"))
    install_route_dependencies(client, session=session, provider=provider)
    allow_student_token(monkeypatch)
    monkeypatch.setattr(upload_view, "query_one", fake_query_one([]))

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "SUBMISSION"},
        files={"file": ("report.bin", b"data", "application/octet-stream")},
    )

    assert response.status_code == 503
    assert response.json()["businessCode"] == "DESIGN_DEPENDENCY_UNAVAILABLE"
    assert "private storage detail" not in response.text
    assert provider.delete_calls == [provider.upload_calls[0]["storage_key"]]
    assert session.rollback_count == 1


@pytest.mark.parametrize("failure_stage", ["insert", "commit"])
def test_database_failure_returns_500_rolls_back_and_cleans_object(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    failure_stage: str,
) -> None:
    """Kiểm tra lỗi INSERT hoặc commit rollback metadata và best-effort xóa object."""

    commit_error = RuntimeError("private database detail") if failure_stage == "commit" else None
    session = FakeSession(commit_error=commit_error)
    provider = FakeUploadStorageProvider()
    install_route_dependencies(client, session=session, provider=provider)
    allow_student_token(monkeypatch)
    calls: list[dict[str, Any]] = []
    monkeypatch.setattr(
        upload_view,
        "query_one",
        fake_query_one(
            calls,
            insert_error=(
                RuntimeError("private database detail") if failure_stage == "insert" else None
            ),
        ),
    )

    response = client.post(
        "/api/v1/uploads",
        headers={"Authorization": "Bearer access-token"},
        data={"purpose": "SUBMISSION"},
        files={"file": ("report.bin", b"data", "application/octet-stream")},
    )

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private database detail" not in response.text
    assert session.rollback_count == 1
    assert provider.delete_calls == [provider.upload_calls[0]["storage_key"]]


def test_s3_provider_streams_content_and_builds_public_url(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra adapter dùng object key UUID, metadata MIME, bucket và public URL."""

    for key, value in {
        "OBJECT_STORAGE_BUCKET": "study-public",
        "OBJECT_STORAGE_REGION": "us-east-1",
        "OBJECT_STORAGE_ACCESS_KEY_ID": "test-access-key",
        "OBJECT_STORAGE_SECRET_ACCESS_KEY": "test-secret-key",
        "OBJECT_STORAGE_PUBLIC_BASE_URL": "https://cdn.example.test/assets/",
    }.items():
        monkeypatch.setenv(key, value)

    calls: list[dict[str, Any]] = []

    class FakeS3Client:
        """Ghi lại lời gọi boto3 mà không kết nối bucket thật."""

        def upload_fileobj(
            self,
            file_obj,
            bucket: str,
            storage_key: str,
            *,
            ExtraArgs: dict[str, str],
        ) -> None:
            """Lưu bytes và tham số được provider truyền vào."""

            calls.append(
                {
                    "content": file_obj.read(),
                    "bucket": bucket,
                    "storage_key": storage_key,
                    "extra_args": ExtraArgs,
                }
            )

    client_options: dict[str, Any] = {}

    def client_factory(service_name: str, **options: Any) -> FakeS3Client:
        """Lưu cấu hình client và trả S3 stub."""

        client_options.update(service_name=service_name, **options)
        return FakeS3Client()

    provider = S3UploadStorageProvider(client_factory=client_factory)
    url = provider.upload(
        storage_key="uploads/123e4567-e89b-12d3-a456-426614174000",
        file_obj=BytesIO(b"streamed"),
        content_type="application/x-example",
    )

    assert url == "https://cdn.example.test/assets/uploads/123e4567-e89b-12d3-a456-426614174000"
    assert calls == [
        {
            "content": b"streamed",
            "bucket": "study-public",
            "storage_key": "uploads/123e4567-e89b-12d3-a456-426614174000",
            "extra_args": {"ContentType": "application/x-example"},
        }
    ]
    assert client_options["service_name"] == "s3"
    assert client_options["aws_access_key_id"] == "test-access-key"
