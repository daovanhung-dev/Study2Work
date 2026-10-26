from __future__ import annotations

from typing import Any

import app.modules.mentor.api_47_mentor_lectures_create.view as lecture_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    def __init__(self, *, fail_commit: bool = False) -> None:
        """Track transaction completion without opening a PostgreSQL connection."""
        self.commit_count = 0
        self.rollback_count = 0
        self.fail_commit = fail_commit

    def commit(self) -> None:
        """Record commit or simulate a failed transaction commit."""
        self.commit_count += 1
        if self.fail_commit:
            raise SQLAlchemyError("commit failed")

    def rollback(self) -> None:
        """Record rollback invoked by the view after an error."""
        self.rollback_count += 1


def override_db(session: FakeSession):
    """Provide a request-scoped fake session through the Study DB dependency."""
    def dependency():
        """Yield the fake session captured by the test."""
        yield session

    return dependency


def mentor_claims(*, roles: list[str] | None = None) -> dict[str, Any]:
    """Create valid numeric JWT claims for Mentor 1001."""
    return {"sub": "1001", "roles": roles or ["MENTOR"]}


def allow_mentor_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Replace JWT decoding with a valid Mentor identity."""
    monkeypatch.setattr(auth_utils, "decode_access_token", lambda _token: mentor_claims())


def course_row(*, mentor_id: int = 1001, status: str = "DRAFT") -> dict[str, Any]:
    """Return the minimal legacy course row used by API #47 ownership checks."""
    return {"id": 101, "mentor_id": mentor_id, "status": status}


def asset_row(asset_id: int, *, name: str) -> dict[str, Any]:
    """Return an UploadAsset metadata row projected by API #47's scoped query."""
    return {
        "id": asset_id,
        "name": name,
        "url": f"https://cdn.example.test/uploads/{asset_id}",
        "content_type": "application/pdf",
        "size_bytes": 1024 + asset_id,
        "status": "UPLOADED",
    }


def request_body(**overrides: Any) -> dict[str, Any]:
    """Return a valid lecture payload with optional field overrides."""
    return {
        "title": "Bài học mở đầu",
        "content": 9_223_372_036_854_775_000,
        "asset_refs": "[34002,34001]",
        "order": 1,
        **overrides,
    }


def install_owner_course(monkeypatch: pytest.MonkeyPatch) -> None:
    """Return the directly-owned DRAFT course from the course lookup."""
    monkeypatch.setattr(lecture_view, "query_one", lambda _db, _query, _params: course_row())


def post_lecture(client: TestClient, body: dict[str, Any] | None = None):
    """Send a create lecture request with the standard test token."""
    return client.post(
        "/api/v1/mentor/courses/101/lectures",
        json=body or request_body(),
        headers={"Authorization": "Bearer valid-token"},
    )


def test_create_lecture_returns_decimal_content_and_assets_in_request_order(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Create a published lesson while preserving decimal content and submitted asset order."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    captured_assets: dict[str, Any] = {}
    captured_assets_query: dict[str, str] = {}
    captured_insert: dict[str, Any] = {}
    captured_links: dict[str, Any] = {}
    assets = [asset_row(34001, name="first.pdf"), asset_row(34002, name="second.pdf")]

    def find_course(_db, query, params):
        assert "FROM courses" in query
        assert "status" not in query.lower()
        assert params == {"course_id": 101}
        return course_row(status="DRAFT")

    def find_assets(_db, query, params):
        if "INSERT INTO lesson_uploads" in query:
            captured_links["sql"] = query
            captured_links.update(params)
            return [{"upload_id": asset_id} for asset_id in params["asset_ids"]]
        captured_assets_query["sql"] = query
        captured_assets.update(params)
        return list(reversed(assets))

    def insert_lecture(_db, query, params):
        captured_insert.update(params)
        assert "CURRENT_TIMESTAMP" in query
        assert "'PUBLISHED'" in query
        return {
            "id": 47001,
            "course_id": 101,
            "name": "Bài học mở đầu",
            "content": str(request_body()["content"]),
            "sort_order": 1,
            "status": "PUBLISHED",
        }

    monkeypatch.setattr(lecture_view, "query_one", find_course)
    monkeypatch.setattr(lecture_view, "query_many", find_assets)
    # The second query_one call inserts the lesson after the course check.
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda db, query, params: find_course(db, query, params)
        if "FROM courses" in query
        else insert_lecture(db, query, params),
    )

    response = post_lecture(client)

    assert response.status_code == 201
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_CREATED"
    assert payload["data"]["content"] == str(request_body()["content"])
    assert payload["data"]["status"] == "PUBLISHED"
    assert [asset["id"] for asset in payload["data"]["assets"]] == [34002, 34001]
    assert [asset["name"] for asset in payload["data"]["assets"]] == ["second.pdf", "first.pdf"]
    assert "owner_id = :mentor_id" in captured_assets_query["sql"]
    assert "purpose = 'LECTURE'" in captured_assets_query["sql"]
    assert "course_id = :course_id" in captured_assets_query["sql"]
    assert captured_assets == {"asset_ids": [34002, 34001], "mentor_id": 1001, "course_id": 101}
    assert captured_insert == {
        "course_id": 101,
        "title": "Bài học mở đầu",
        "content": str(request_body()["content"]),
        "order": 1,
    }
    assert "WITH ORDINALITY" in captured_links["sql"]
    assert captured_links["lecture_id"] == 47001
    assert captured_links["asset_ids"] == [34002, 34001]
    assert session.commit_count == 1
    assert session.rollback_count == 0


def test_create_lecture_accepts_empty_assets_and_draft_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Accept [] on a directly owned DRAFT course and skip the uploads lookup."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    calls: list[str] = []

    def query_one(_db, query, _params):
        calls.append(query)
        if "FROM courses" in query:
            return course_row(status="DRAFT")
        return {
            "id": 47002,
            "course_id": 101,
            "name": "Bài học mở đầu",
            "content": "7",
            "sort_order": 0,
            "status": "PUBLISHED",
        }

    monkeypatch.setattr(lecture_view, "query_one", query_one)
    monkeypatch.setattr(
        lecture_view,
        "query_many",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("empty IDs skip lookup")),
    )

    response = post_lecture(client, request_body(asset_refs="[]", content=7, order=0))

    assert response.status_code == 201
    assert response.json()["data"]["assets"] == []
    assert len(calls) == 2
    assert session.commit_count == 1


@pytest.mark.parametrize("authorization", [None, "Basic token", "Bearer"])
def test_create_lecture_rejects_missing_or_malformed_auth_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    authorization: str | None,
) -> None:
    """Reject absent/malformed Bearer auth before any course or asset query."""
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )
    headers = {} if authorization is None else {"Authorization": authorization}

    response = client.post(
        "/api/v1/mentor/courses/101/lectures",
        json=request_body(),
        headers=headers,
    )

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"


def test_create_lecture_rejects_non_mentor_role_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Reject a valid Student JWT on the Mentor route before database access."""
    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: mentor_claims(roles=["STUDENT"]),
    )
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = post_lecture(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"


@pytest.mark.parametrize(
    ("url", "body"),
    [
        ("/api/v1/mentor/courses/9223372036854775808/lectures", request_body()),
        ("/api/v1/mentor/courses/101/lectures", request_body(content=9223372036854775808)),
        ("/api/v1/mentor/courses/101/lectures", request_body(content=-9223372036854775809)),
        ("/api/v1/mentor/courses/101/lectures", request_body(order=2147483648)),
        ("/api/v1/mentor/courses/101/lectures", request_body(order=-2147483649)),
        ("/api/v1/mentor/courses/101/lectures", request_body(title="x" * 201)),
    ],
)
def test_create_lecture_rejects_out_of_range_numbers_and_long_title(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    url: str,
    body: dict[str, Any],
) -> None:
    """Apply signed integer bounds and the legacy title column limit before DB access."""
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("query must not run")),
    )

    response = client.post(
        url,
        json=body,
        headers={"Authorization": "Bearer valid-token"},
    )

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


@pytest.mark.parametrize(
    "asset_refs",
    [
        "not-json",
        "{}",
        "[true]",
        "[1.5]",
        "[9223372036854775808]",
        "[1,1]",
    ],
)
def test_create_lecture_rejects_invalid_asset_refs_before_db(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    asset_refs: str,
) -> None:
    """Reject malformed, wrong-shape, duplicate or non-int64 asset references early."""
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: (_ for _ in ()).throw(
            AssertionError("course query must not run")
        ),
    )

    response = post_lecture(client, request_body(asset_refs=asset_refs))

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"


def test_create_lecture_returns_not_found_for_missing_course(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Return course not found and roll back the read transaction when no course exists."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(lecture_view, "query_one", lambda *_args, **_kwargs: None)

    response = post_lecture(client, request_body(asset_refs="[]"))

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_create_lecture_forbids_course_owned_by_another_mentor(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Require direct courses.mentor_id ownership regardless of other course fields."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    monkeypatch.setattr(
        lecture_view,
        "query_one",
        lambda *_args, **_kwargs: course_row(mentor_id=2002, status="PUBLISHED"),
    )

    response = post_lecture(client, request_body(asset_refs="[]"))

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert session.rollback_count == 1


@pytest.mark.parametrize("resolved_rows", [[], [asset_row(34002, name="other-course.pdf")]])
def test_create_lecture_returns_generic_not_found_for_unresolved_assets(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    resolved_rows: list[dict[str, Any]],
) -> None:
    """Hide missing or out-of-scope asset IDs behind the same 404 response."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_owner_course(monkeypatch)
    monkeypatch.setattr(lecture_view, "query_many", lambda *_args, **_kwargs: resolved_rows)

    response = post_lecture(client)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["message"] == "Requested assets were not found."
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_create_lecture_rolls_back_when_commit_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Return a safe 500 and roll back if committing the inserted lesson fails."""
    session = FakeSession(fail_commit=True)
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_owner_course(monkeypatch)
    monkeypatch.setattr(lecture_view, "query_one", lambda _db, query, _params: (
        course_row() if "FROM courses" in query else {
            "id": 47003,
            "course_id": 101,
            "name": "Bài học mở đầu",
            "content": "9",
            "sort_order": 1,
            "status": "PUBLISHED",
        }
    ))
    monkeypatch.setattr(lecture_view, "query_many", lambda *_args, **_kwargs: [])

    response = post_lecture(client, request_body(asset_refs="[]"))

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 1
    assert session.rollback_count == 1


def test_create_lecture_rolls_back_when_asset_links_are_incomplete(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Giữ lesson và asset links nguyên tử khi một link được yêu cầu bị thiếu."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)
    install_owner_course(monkeypatch)

    def query_one(_db, query, _params):
        if "FROM courses" in query:
            return course_row()
        return {
            "id": 47004,
            "course_id": 101,
            "name": "Bài học mở đầu",
            "content": "9",
            "sort_order": 1,
            "status": "PUBLISHED",
        }

    def query_many(_db, query, _params):
        if "INSERT INTO lesson_uploads" in query:
            return [{"upload_id": 34002}]
        return [asset_row(34002, name="second.pdf"), asset_row(34001, name="first.pdf")]

    monkeypatch.setattr(lecture_view, "query_one", query_one)
    monkeypatch.setattr(lecture_view, "query_many", query_many)

    response = post_lecture(client)

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_lecture_rolls_back_when_insert_query_fails(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Return a safe 500 and roll back if the lesson INSERT query raises a DB error."""
    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_mentor_token(monkeypatch)

    def query_one(_db, query, _params):
        if "FROM courses" in query:
            return course_row()
        raise SQLAlchemyError("insert failed")

    monkeypatch.setattr(lecture_view, "query_one", query_one)
    monkeypatch.setattr(lecture_view, "query_many", lambda *_args, **_kwargs: [])

    response = post_lecture(client, request_body(asset_refs="[]"))

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_create_lecture_route_openapi_contract(client: TestClient) -> None:
    """Expose the stable POST path and int64 content request/response types in OpenAPI."""
    schema = client.app.openapi()
    operation = schema["paths"]["/api/v1/mentor/courses/{course_id}/lectures"]["post"]

    assert operation["responses"]["201"]
    assert any(
        parameter["name"] == "course_id"
        and parameter["schema"].get("format") == "int64"
        for parameter in operation["parameters"]
    )
    request_schema = schema["components"]["schemas"]["CreateLectureRequest"]["properties"]
    assert request_schema["content"]["type"] == "integer"
    assert request_schema["content"]["format"] == "int64"
    response_schema = schema["components"]["schemas"]["LectureResponse"]["properties"]
    assert response_schema["content"]["anyOf"] == [
        {"type": "string"},
        {"type": "null"},
    ]
