"""Điều phối auth, bốn aggregate read-only và response API #101."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from datetime import UTC, datetime
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_101_admin_reports_summary.models import (
    AdminReportMetric,
    AdminReportSummary,
)
from app.modules.admin.api_101_admin_reports_summary.query import (
    COUNT_ADMIN_REPORT_COURSES,
    COUNT_ADMIN_REPORT_DISCUSSIONS,
    COUNT_ADMIN_REPORT_ENROLLMENTS,
    COUNT_ADMIN_REPORT_USERS,
)
from app.modules.admin.api_101_admin_reports_summary.validate import (
    validate_admin_report_summary_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc mapping report thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Report summary could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction đọc lỗi mà không che response lỗi ban đầu."""

    try:
        # Dọn transaction thất bại trước khi dependency đóng Session.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin report summary rollback failed; trace_id=%s", trace_id)


def _count_value(row: Any) -> int | None:
    """Chỉ nhận projection COUNT là mapping có số nguyên không âm trong miền int64."""

    if not isinstance(row, Mapping):
        return None
    total = row.get("total")
    if type(total) is not int or not 0 <= total <= MAX_INT64:
        return None
    return total


# API #101 admin_reports_summary
def get_admin_report_summary(
    *,
    authorization: str | None,
    from_value: str | None,
    to_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN rồi tổng hợp bốn count metric trong kỳ inclusive đã chọn."""

    # Xác thực role và chuẩn hóa date range trước mọi truy vấn.
    period = validate_admin_report_summary_request(
        authorization,
        from_value=from_value,
        to_value=to_value,
        trace_id=trace_id,
    )
    if isinstance(period, JSONResponse):
        return period

    # Dùng cùng bound cho bốn query độc lập để không nhân bản row giữa domain.
    params = {"from_date": period.from_date, "to_date": period.to_date}
    try:
        rows = [
            query_one(db, COUNT_ADMIN_REPORT_USERS, params),
            query_one(db, COUNT_ADMIN_REPORT_COURSES, params),
            query_one(db, COUNT_ADMIN_REPORT_ENROLLMENTS, params),
            query_one(db, COUNT_ADMIN_REPORT_DISCUSSIONS, params),
        ]
    except SQLAlchemyError:
        # Dọn transaction đọc lỗi và chỉ log trace ID, không lộ chi tiết SQL.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin report summary query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối projection lỗi để không trả metric thiếu hoặc sai kiểu.
    totals = [_count_value(row) for row in rows]
    if any(total is None for total in totals):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin report summary mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    try:
        # Giữ key/order ổn định và serialize COUNT đúng decimal-string contract.
        report = AdminReportSummary(
            period=period,
            metrics=[
                AdminReportMetric(
                    key="user_records_created",
                    value=str(totals[0]),
                    label="Tài khoản được tạo",
                ),
                AdminReportMetric(
                    key="course_records_created",
                    value=str(totals[1]),
                    label="Khóa học được tạo",
                ),
                AdminReportMetric(
                    key="enrollment_records_created",
                    value=str(totals[2]),
                    label="Lượt ghi danh được tạo",
                ),
                AdminReportMetric(
                    key="discussion_records_created",
                    value=str(totals[3]),
                    label="Bản ghi thảo luận được tạo",
                ),
            ],
            generated_at=datetime.now(UTC),
        )
    except (TypeError, ValidationError):
        # Map model failure thành lỗi nội bộ chuẩn thay vì trả DTO một phần.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin report summary response validation failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; không commit transaction và trả envelope Study chuẩn.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Report summary retrieved.",
        trace_id=trace_id,
        data=report.model_dump(mode="json", by_alias=True),
    )
