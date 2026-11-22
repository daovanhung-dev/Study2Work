from __future__ import annotations

from datetime import date
from typing import Any

import app.modules.admin.api_101_admin_reports_summary.validate as report_validate
import app.modules.admin.api_101_admin_reports_summary.view as report_view
import app.utils.auth as auth_utils
import pytest
from app.core.database import get_db
from app.modules.admin.api_101_admin_reports_summary.query import (
    COUNT_ADMIN_REPORT_COURSES,
    COUNT_ADMIN_REPORT_DISCUSSIONS,
    COUNT_ADMIN_REPORT_ENROLLMENTS,
    COUNT_ADMIN_REPORT_USERS,
)
from fastapi.testclient import TestClient
from sqlalchemy.exc import SQLAlchemyError


class FakeSession:
    """Session giả ghi nhận transaction của API #101."""

    def __init__(self) -> None:
        """Khởi tạo bộ đếm commit và rollback cho request test."""

        self.commit_count = 0
        self.rollback_count = 0

    def commit(self) -> None:
        """Ghi nhận nếu API đọc vô tình commit transaction."""

        self.commit_count += 1

    def rollback(self) -> None:
        """Ghi nhận rollback khi query hoặc mapping thất bại."""

        self.rollback_count += 1


def override_db(session: FakeSession):
    """Tạo dependency override trả về một Session giả."""

    def dependency():
        """Cung cấp Session giả trong vòng đời request."""

        yield session

    return dependency


def allow_admin_token(
    monkeypatch: pytest.MonkeyPatch,
    *,
    roles: list[str] | None = None,
) -> None:
    """Cấp token giả có role được chọn để kiểm tra guard."""

    monkeypatch.setattr(
        auth_utils,
        "decode_access_token",
        lambda _token: {"sub": "9001", "roles": roles or ["ADMIN"]},
    )


def install_report_queries(
    monkeypatch: pytest.MonkeyPatch,
    *,
    totals: tuple[int, int, int, int] = (12, 4, 3, 6),
    fail_query: bool = False,
) -> list[tuple[str, dict[str, Any]]]:
    """Ghi nhận bốn query và trả COUNT projection giả theo thứ tự API."""

    captured: list[tuple[str, dict[str, Any]]] = []
    expected_queries = (
        COUNT_ADMIN_REPORT_USERS,
        COUNT_ADMIN_REPORT_COURSES,
        COUNT_ADMIN_REPORT_ENROLLMENTS,
        COUNT_ADMIN_REPORT_DISCUSSIONS,
    )

    def query_one(_db: Any, query: str, params: dict[str, Any]) -> Any:
        """Trả count tương ứng hoặc tạo lỗi database giả."""

        captured.append((query, dict(params)))
        if fail_query:
            raise SQLAlchemyError("private query detail")
        return {"total": totals[expected_queries.index(query)]}

    monkeypatch.setattr(report_view, "query_one", query_one)
    return captured


def report_request(
    client: TestClient,
    *,
    from_value: str | None = None,
    to_value: str | None = None,
    authorization: str | None = "Bearer valid-admin-token",
):
    """Gửi GET summary với raw query dates và Authorization tùy chọn."""

    params = {}
    if from_value is not None:
        params["from"] = from_value
    if to_value is not None:
        params["to"] = to_value
    headers = {"Authorization": authorization} if authorization is not None else {}
    return client.get("/api/v1/admin/reports/summary", params=params, headers=headers)


def test_summary_returns_four_date_counts_and_does_not_write(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả bốn KPI theo bound truyền vào với envelope chuẩn và không commit GET."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_report_queries(monkeypatch)

    response = report_request(client, from_value="2026-11-01", to_value="2026-11-07")

    assert response.status_code == 200
    payload = response.json()
    assert payload["businessCode"] == "DESIGN_RESOURCE_RETRIEVED"
    assert payload["data"]["period"] == {"from": "2026-11-01", "to": "2026-11-07"}
    assert payload["data"]["metrics"] == [
        {"key": "user_records_created", "value": "12", "label": "Tài khoản được tạo"},
        {"key": "course_records_created", "value": "4", "label": "Khóa học được tạo"},
        {"key": "enrollment_records_created", "value": "3", "label": "Lượt ghi danh được tạo"},
        {"key": "discussion_records_created", "value": "6", "label": "Bản ghi thảo luận được tạo"},
    ]
    assert payload["data"]["generated_at"].endswith("Z")
    assert payload["meta"] == {}
    assert response.headers["X-Trace-Id"] == payload["traceId"]
    assert [query for query, _params in captured] == [
        COUNT_ADMIN_REPORT_USERS,
        COUNT_ADMIN_REPORT_COURSES,
        COUNT_ADMIN_REPORT_ENROLLMENTS,
        COUNT_ADMIN_REPORT_DISCUSSIONS,
    ]
    assert all(
        params == {"from_date": date(2026, 11, 1), "to_date": date(2026, 11, 7)}
        for _, params in captured
    )
    assert "status" not in COUNT_ADMIN_REPORT_USERS
    assert "role" not in COUNT_ADMIN_REPORT_USERS
    assert "status" not in COUNT_ADMIN_REPORT_COURSES
    assert "parent_id" not in COUNT_ADMIN_REPORT_DISCUSSIONS
    assert session.commit_count == 0
    assert session.rollback_count == 0


def test_summary_uses_thirty_inclusive_vietnam_calendar_days_by_default(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Tạo default period gồm hôm nay và 29 ngày lịch trước theo Vietnam time."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(report_validate, "vietnam_today", lambda: date(2026, 11, 22))
    captured = install_report_queries(monkeypatch)

    response = report_request(client)

    assert response.status_code == 200
    assert response.json()["data"]["period"] == {"from": "2026-10-24", "to": "2026-11-22"}
    assert captured[0][1] == {"from_date": date(2026, 10, 24), "to_date": date(2026, 11, 22)}


def test_summary_supports_one_sided_bounds_using_draft_window_rules(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Dùng hôm nay cho from-only và 30 ngày kết thúc tại to-only."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    monkeypatch.setattr(report_validate, "vietnam_today", lambda: date(2026, 11, 22))
    install_report_queries(monkeypatch)

    from_only = report_request(client, from_value="2026-11-20")
    to_only = report_request(client, to_value="2026-11-10")

    assert from_only.status_code == 200
    assert from_only.json()["data"]["period"] == {"from": "2026-11-20", "to": "2026-11-22"}
    assert to_only.status_code == 200
    assert to_only.json()["data"]["period"] == {"from": "2026-10-12", "to": "2026-11-10"}


def test_summary_rejects_invalid_calendar_date_with_shared_validation_error(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Ánh xạ ngày sai định dạng vào business code validation đang dùng."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_report_queries(monkeypatch)

    response = report_request(client, from_value="2026-02-30", to_value="2026-03-01")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["field"] == "from"
    assert captured == []
    assert session.commit_count == 0


def test_summary_rejects_reversed_range(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Từ chối kỳ có ngày bắt đầu sau ngày kết thúc trước khi query."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    captured = install_report_queries(monkeypatch)

    response = report_request(client, from_value="2026-11-08", to_value="2026-11-07")

    assert response.status_code == 422
    assert response.json()["businessCode"] == "DESIGN_VALIDATION_ERROR"
    assert response.json()["meta"]["fieldErrors"][0]["code"] == "DATE_RANGE"
    assert captured == []


def test_summary_checks_admin_before_parsing_or_querying(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 401 trước lỗi date và không truy cập database khi thiếu Bearer."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    captured = install_report_queries(monkeypatch)

    response = report_request(client, from_value="not-a-date", authorization=None)

    assert response.status_code == 401
    assert response.json()["businessCode"] == "DESIGN_AUTHENTICATION_REQUIRED"
    assert captured == []
    assert session.commit_count == 0


def test_summary_rejects_non_admin_role_before_query(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Trả 403 cho token Student và không chạy aggregate."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch, roles=["STUDENT"])
    captured = install_report_queries(monkeypatch)

    response = report_request(client)

    assert response.status_code == 403
    assert response.json()["businessCode"] == "DESIGN_ACCESS_DENIED"
    assert captured == []


def test_summary_returns_zero_values_for_empty_sources(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Serialize bốn count bằng chuỗi zero khi mọi nguồn không có bản ghi."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_report_queries(monkeypatch, totals=(0, 0, 0, 0))

    response = report_request(client, from_value="2026-11-01", to_value="2026-11-01")

    assert response.status_code == 200
    assert [metric["value"] for metric in response.json()["data"]["metrics"]] == [
        "0",
        "0",
        "0",
        "0",
    ]


def test_summary_maps_database_failure_to_safe_500_and_rolls_back(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Rollback transaction query lỗi và không trả chi tiết database."""

    session = FakeSession()
    client.app.dependency_overrides[get_db] = override_db(session)
    allow_admin_token(monkeypatch)
    install_report_queries(monkeypatch, fail_query=True)

    response = report_request(client, from_value="2026-11-01", to_value="2026-11-07")

    assert response.status_code == 500
    assert response.json()["businessCode"] == "DESIGN_INTERNAL_ERROR"
    assert "private query detail" not in response.text
    assert session.rollback_count == 1
    assert session.commit_count == 0
