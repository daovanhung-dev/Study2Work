"""Điều phối aggregate, kiểm tra projection và dựng response API #91."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_91_admin_quizzes_statistics.models import AdminQuizStatistics
from app.modules.admin.api_91_admin_quizzes_statistics.query import GET_ADMIN_QUIZ_STATISTICS
from app.modules.admin.api_91_admin_quizzes_statistics.validate import (
    validate_admin_quiz_statistics_request,
)
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn khi truy vấn hoặc ánh xạ statistics thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Quiz statistics could not be retrieved.",
        trace_id=trace_id,
    )


def _not_found(trace_id: str) -> JSONResponse:
    """Dựng lỗi 404 catalog khi Quiz không còn row để tổng hợp."""

    return error_response(
        status_code=404,
        business_code="DESIGN_RESOURCE_NOT_FOUND",
        message="Quiz not found.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Rollback transaction lỗi đọc mà không che response lỗi ban đầu."""

    try:
        # Hoàn tác transaction đọc lỗi; không để lỗi rollback lộ ra HTTP response.
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin quiz statistics rollback failed; trace_id=%s", trace_id)


def _decimal_string(value: Any) -> str | None:
    """Chuyển số hữu hạn thành chuỗi thập phân không dùng exponent."""

    # Từ chối NULL/boolean và chuẩn hóa DB numeric qua Decimal.
    if value is None or isinstance(value, bool):
        return None
    try:
        decimal_value = Decimal(str(value))
    except (InvalidOperation, TypeError):
        return None
    # Chỉ giữ giá trị hữu hạn và không làm tròn ở tầng ứng dụng.
    if not decimal_value.is_finite():
        return None
    return format(decimal_value, "f")


def _valid_count(value: Any) -> bool:
    """Kiểm tra COUNT projection là số nguyên không âm thuộc int64."""

    return type(value) is int and 0 <= value <= MAX_INT64


def _map_statistics(
    row: Mapping[str, Any],
    *,
    requested_quiz_id: int,
) -> AdminQuizStatistics | None:
    """Xác thực aggregate row và ánh xạ các metric của DD proposal."""

    quiz_id = row.get("quiz_id")
    attempt_count = row.get("attempt_count")
    submitted_count = row.get("submitted_attempt_count")
    graded_count = row.get("graded_attempt_count")
    passed_count = row.get("passed_attempt_count")
    average_source = row.get("average_score")
    rate_source = row.get("pass_rate_percent")
    threshold = row.get("passing_score")

    # Kiểm tra identity, kiểu count và quan hệ số lượng trước khi ánh xạ.
    if (
        type(quiz_id) is not int
        or quiz_id != requested_quiz_id
        or not _valid_count(attempt_count)
        or not _valid_count(submitted_count)
        or not _valid_count(graded_count)
        or submitted_count > attempt_count
        or graded_count > attempt_count
    ):
        return None

    # Chuyển average/rate nhưng từ chối chuỗi lỗi thay vì che bằng NULL.
    average_score = _decimal_string(average_source)
    pass_rate_percent = _decimal_string(rate_source)
    if (average_source is not None and average_score is None) or (
        rate_source is not None and pass_rate_percent is None
    ):
        return None
    if (graded_count == 0) != (average_score is None):
        return None

    # Giữ metric pass là NULL khi threshold không được lưu.
    if threshold is None:
        if passed_count is not None or pass_rate_percent is not None:
            return None
    else:
        threshold_value = _decimal_string(threshold)
        if threshold_value is None or not _valid_count(passed_count):
            return None
        if passed_count > graded_count:
            return None
        if graded_count == 0:
            if pass_rate_percent is not None:
                return None
        else:
            if pass_rate_percent is None:
                return None
            rate_value = Decimal(pass_rate_percent)
            if not rate_value.is_finite() or not Decimal(0) <= rate_value <= Decimal(100):
                return None

    try:
        # Tạo DTO chặt sau khi mọi aggregate invariant đã hợp lệ.
        return AdminQuizStatistics(
            quiz_id=quiz_id,
            attempt_count=attempt_count,
            submitted_attempt_count=submitted_count,
            graded_attempt_count=graded_count,
            average_score=average_score,
            passed_attempt_count=passed_count,
            pass_rate_percent=pass_rate_percent,
        )
    except (TypeError, ValidationError):
        return None


# API #91 admin_quizzes_statistics
def get_admin_quiz_statistics(
    *,
    authorization: str | None,
    quiz_id_value: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực ADMIN rồi trả aggregate read-only cho một Quiz."""

    # Xác thực role ADMIN trước khi parse Quiz ID hoặc truy cập database.
    quiz_id = validate_admin_quiz_statistics_request(
        authorization,
        quiz_id_value,
        trace_id=trace_id,
    )
    if isinstance(quiz_id, JSONResponse):
        return quiz_id

    try:
        # LEFT JOIN giữ quiz không có attempt và query không loại tombstone.
        row = query_one(db, GET_ADMIN_QUIZ_STATISTICS, {"quiz_id": quiz_id})
    except SQLAlchemyError:
        # Rollback transaction đọc lỗi và không trả chi tiết database cho client.
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz statistics query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    if row is None:
        # Quiz đã hard-delete hoặc không tồn tại trả đúng catalog 404.
        _rollback_safely(db, trace_id=trace_id)
        return _not_found(trace_id)
    if not isinstance(row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz statistics projection is not a mapping; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Từ chối aggregate thiếu hoặc mâu thuẫn để không trả thống kê sai.
    statistics = _map_statistics(row, requested_quiz_id=quiz_id)
    if statistics is None:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin quiz statistics mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # GET chỉ đọc; serialize DTO proposal như JSON và không commit transaction.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Quiz statistics retrieved.",
        trace_id=trace_id,
        data=statistics.model_dump(mode="json"),
    )
