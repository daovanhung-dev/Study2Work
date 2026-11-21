from __future__ import annotations

from decimal import Decimal
from typing import Any

import app.modules.admin.api_91_admin_quizzes_statistics.view as statistics_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_91_admin_quizzes_statistics.query import (
    GET_ADMIN_QUIZ_STATISTICS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError

_UNSET = object()


class FakeSession:
    """Session giả ghi nhận transaction của API #91."""

    def __init__(self, *, fail_rollback: bool = False) -> None:
        """Khởi tạo bộ đếm commit/rollback cùng cờ lỗi rollback."""

        self.commit_count = 0
        self.rollback_count = 0
        self.fail_rollback = fail_rollback

    def commit(self) -> None:
        """Ghi nhận commit nếu luồng vô tình ghi dữ liệu."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback transaction đọc bị lỗi."""

        self.rollback_count += 1
        if self.fail_rollback:
            raise SQLAlchemyError("private rollback detail")


def override_db(session: FakeSession):
    """Tạo dependency override trả về session giả cho TestClient."""

    def dependency():
        """Cung cấp một session giả trong vòng đời request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp JWT giả có subject và role tùy chọn cho request test."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def statistics_request(
    client: TestClient,
    quiz_id: str,
    *,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi GET bằng raw path và Authorization tùy chọn."""

    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get(
        f"/api/v1/admin/quizzes/{quiz_id}/statistics",
        headers=headers,
    )


def install_statistics_query(
    monkeypatch: pytest.MonkeyPatch,
    *,
    row: Any = _UNSET,
    fail_query: bool = False,
) -> list[tuple[str, dict[str, Any]]]:
    """Ghi nhận query/bindings và trả projection aggregate có thể tùy biến."""

    captured: list[tuple[str, dict[str, Any]]] = []

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Trả một Quiz aggregate giả hoặc phát sinh lỗi database."""

        captured.append((query, dict(params)))
        if fail_query:
            raise SQLAlchemyError("private query detail")
        if row is not _UNSET:
            return row
        return {
            "quiz_id": params["quiz_id"],
            "passing_score": Decimal("60.00"),
            "attempt_count": 3,
            "submitted_attempt_count": 2,
            "graded_attempt_count": 2,
            "average_score": Decimal("75.000"),
            "passed_attempt_count": 1,
            "pass_rate_percent": Decimal("50.000"),
        }

    monkeypatch.setattr(statistics_view, "query_one", query_one)
    return captured


def test_statistics_returns_derived_aggregate_and_does_not_write(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả aggregate proposal với decimal string và không commit GET."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_statistics_query(monkeypatch)

    response = statistics_request(client, "5101")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"] == {
        "quiz_id": 5101,
        "attempt_count": 3,
        "submitted_attempt_count": 2,
        "graded_attempt_count": 2,
        "average_score": "75.000",
        "passed_attempt_count": 1,
        "pass_rate_percent": "50.000",
    }
    assert payload["meta"] == {}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert captured == [(GET_ADMIN_QUIZ_STATISTICS, {"quiz_id": 5101})]
    assert "quiz.status" not in GET_ADMIN_QUIZ_STATISTICS
    assert "attempt.status" not in GET_ADMIN_QUIZ_STATISTICS
    assert "quiz_answers" not in GET_ADMIN_QUIZ_STATISTICS
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_statistics_keeps_empty_quiz_and_null_average(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Giữ Quiz không có attempt với count zero và average/rate null."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_statistics_query(
        monkeypatch,
        row={
            "quiz_id": 5101,
            "passing_score": 60,
            "attempt_count": 0,
            "submitted_attempt_count": 0,
            "graded_attempt_count": 0,
            "average_score": None,
            "passed_attempt_count": 0,
            "pass_rate_percent": None,
        },
    )

    response = statistics_request(client, "5101")

    assert response.status_code == 200
    assert response.json()["data"] == {
        "quiz_id": 5101,
        "attempt_count": 0,
        "submitted_attempt_count": 0,
        "graded_attempt_count": 0,
        "average_score": None,
        "passed_attempt_count": 0,
        "pass_rate_percent": None,
    }
    assert session.commit_count == 0


def test_statistics_keeps_submitted_but_ungraded_attempts_out_of_average(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Đếm submitted_at độc lập với score để giữ trạng thái chờ chấm."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_statistics_query(
        monkeypatch,
        row={
            "quiz_id": 5101,
            "passing_score": 60,
            "attempt_count": 2,
            "submitted_attempt_count": 2,
            "graded_attempt_count": 1,
            "average_score": "80.00",
            "passed_attempt_count": 1,
            "pass_rate_percent": "100.00",
        },
    )

    response = statistics_request(client, "5101")

    assert response.status_code == 200
    assert response.json()["data"]["submitted_attempt_count"] == 2
    assert response.json()["data"]["graded_attempt_count"] == 1
    assert response.json()["data"]["average_score"] == "80.00"


def test_statistics_null_threshold_returns_unknown_pass_metrics(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Không biến passing_score NULL thành passed count hoặc rate bằng zero."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_statistics_query(
        monkeypatch,
        row={
            "quiz_id": 5101,
            "passing_score": None,
            "attempt_count": 1,
            "submitted_attempt_count": 1,
            "graded_attempt_count": 1,
            "average_score": "40.00",
            "passed_attempt_count": None,
            "pass_rate_percent": None,
        },
    )

    response = statistics_request(client, "5101")

    assert response.status_code == 200
    assert response.json()["data"]["passed_attempt_count"] is None
    assert response.json()["data"]["pass_rate_percent"] is None


@pytest.mark.parametrize("quiz_id", ["0", "abc", "1.5", "+1", "-1", str(2**63)])
def test_statistics_maps_invalid_path_to_catalog_not_found_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    quiz_id: str,
) -> None:
    """Ánh xạ raw ID không hợp lệ sang 404 catalog trước query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_statistics_query(monkeypatch)

    response = statistics_request(client, quiz_id)

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert response.json()["data"] is None
    assert captured == []
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_statistics_authentication_precedes_invalid_path_and_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Yêu cầu Bearer token trước parse path và trước database query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_statistics_query(monkeypatch)

    response = statistics_request(client, "invalid", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert response.json()["data"] is None
    assert captured == []


def test_statistics_forbids_non_admin_before_database(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối token không có role ADMIN trước khi mở query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["MENTOR"])
    captured = install_statistics_query(monkeypatch)

    response = statistics_request(client, "5101")

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []


def test_statistics_returns_not_found_for_missing_quiz(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Map row vắng mặt sang 404 và rollback transaction đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_statistics_query(monkeypatch, row=None)

    response = statistics_request(client, "5101")

    assert response.status_code == 404
    assert response.json()["businessCode"] == "DESIGN_RESOURCE_NOT_FOUND"
    assert captured == [(GET_ADMIN_QUIZ_STATISTICS, {"quiz_id": 5101})]
    assert session.commit_count == 0
    assert session.rollback_count == 1


@pytest.mark.parametrize(
    "row",
    [
        "not-a-mapping",
        {
            "quiz_id": 5101,
            "passing_score": 60,
            "attempt_count": -1,
            "submitted_attempt_count": 0,
            "graded_attempt_count": 0,
            "average_score": None,
            "passed_attempt_count": 0,
            "pass_rate_percent": None,
        },
        {
            "quiz_id": 5101,
            "passing_score": 60,
            "attempt_count": 1,
            "submitted_attempt_count": 2,
            "graded_attempt_count": 0,
            "average_score": None,
            "passed_attempt_count": 0,
            "pass_rate_percent": None,
        },
        {
            "quiz_id": 5101,
            "passing_score": 60,
            "attempt_count": 1,
            "submitted_attempt_count": 1,
            "graded_attempt_count": 1,
            "average_score": "NaN",
            "passed_attempt_count": 1,
            "pass_rate_percent": "100",
        },
    ],
)
def test_statistics_rolls_back_invalid_aggregate_projection(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
    row: Any,
) -> None:
    """Không trả số liệu khi aggregate thiếu hoặc vi phạm bất biến."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_statistics_query(monkeypatch, row=row)

    response = statistics_request(client, "5101")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert response.json()["data"] is None
    assert session.commit_count == 0
    assert session.rollback_count == 1


def test_statistics_rolls_back_and_hides_query_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ẩn lỗi SQLAlchemy khỏi client và rollback transaction đọc."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_statistics_query(monkeypatch, fail_query=True)

    response = statistics_request(client, "5101")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private query detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0


def test_statistics_openapi_has_exact_path_errors_and_no_body_or_query(
    client: TestClient,
) -> None:
    """Khai báo path int64, Authorization và đúng error set catalog."""

    operation = client.app.openapi()["paths"]["/api/v1/admin/quizzes/{quiz_id}/statistics"]["get"]

    assert {item["name"] for item in operation["parameters"]} == {
        "quiz_id",
        "Authorization",
    }
    quiz_id = next(item for item in operation["parameters"] if item["name"] == "quiz_id")
    assert quiz_id["required"] is True
    assert quiz_id["schema"]["format"] == "int64"
    assert quiz_id["schema"]["minimum"] == 1
    response_schema = client.app.openapi()["components"]["schemas"]["AdminQuizStatistics"][
        "properties"
    ]
    assert response_schema["quiz_id"]["format"] == "int64"
    assert response_schema["attempt_count"]["format"] == "int64"
    assert response_schema["passed_attempt_count"]["format"] == "int64"
    assert "requestBody" not in operation
    assert set(operation["responses"]) == {"200", "401", "403", "404", "500"}
