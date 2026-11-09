"""Điều phối truy vấn và dựng response kết quả attempt cho API #32."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_32_attempts_result.models import QuizAnswer, QuizAttempt
from app.modules.guest.api_32_attempts_result.query import (
    ATTEMPT_ANSWERS_BY_ID,
    ATTEMPT_RESULT_BY_ID,
)
from app.modules.guest.api_32_attempts_result.validate import (
    attempt_not_found,
    validate_attempt_result_request,
)
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_attempt_result(
    db: Session,
    *,
    attempt_id: int,
    user_id: int,
) -> dict[str, Any] | None:
    """Đọc attempt theo ID và user_id đã xác thực."""

    return query_one(
        db,
        ATTEMPT_RESULT_BY_ID,
        {"attempt_id": attempt_id, "user_id": user_id},
    )


def find_attempt_answers(
    db: Session,
    *,
    attempt_id: int,
    user_id: int,
) -> list[dict[str, Any]]:
    """Đọc các answer row thuộc attempt do Student hiện tại sở hữu."""

    return query_many(
        db,
        ATTEMPT_ANSWERS_BY_ID,
        {"attempt_id": attempt_id, "user_id": user_id},
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response 500 an toàn khi đọc hoặc ánh xạ kết quả attempt thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Attempt result could not be retrieved.",
        trace_id=trace_id,
        data=None,
    )


def _build_attempt_result(
    attempt_row: dict[str, Any],
    answer_rows: list[dict[str, Any]],
) -> QuizAttempt:
    """Ánh xạ dữ liệu sang model response, chỉ gồm field có căn cứ an toàn hiện tại."""

    raw_status = attempt_row["status"]
    status_value = getattr(raw_status, "value", raw_status)
    status_text = str(status_value)

    answers = [
        QuizAnswer(question_id=answer_row["question_id"])
        for answer_row in answer_rows
    ]

    # Việc chỉ trả score khi GRADED là cách xử lý tạm theo ví dụ DD;
    # chính sách score cho các trạng thái khác vẫn cần được xác nhận.
    score = (
        attempt_row.get("score")
        if status_text.upper() == "GRADED"
        else None
    )

    return QuizAttempt(
        id=attempt_row["id"],
        quiz_id=attempt_row["quiz_id"],
        status=status_text,
        started_at=attempt_row["started_at"],
        submitted_at=attempt_row.get("submitted_at"),
        score=score,
        answers=answers,
    )


# API #32 attempts_result
def get_attempt_result(
    *,
    authorization: str | None,
    attempt_id_raw: str,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, đọc attempt của họ và trả envelope kết quả theo API #32."""

    # Xác thực Student và kiểm tra path trước khi truy cập database.
    validated_request = validate_attempt_result_request(
        authorization,
        attempt_id_raw,
        trace_id=trace_id,
    )
    if isinstance(validated_request, JSONResponse):
        return validated_request

    user_id, attempt_id = validated_request

    # user_id lấy từ JWT; lookup không tìm thấy sẽ trả 404 theo quyết định tạm hiện tại.
    try:
        attempt_row = find_attempt_result(
            db,
            attempt_id=attempt_id,
            user_id=user_id,
        )
        if attempt_row is None:
            return attempt_not_found(trace_id)

        answer_rows = find_attempt_answers(
            db,
            attempt_id=attempt_id,
            user_id=user_id,
        )
    except SQLAlchemyError:
        db.rollback()
        logger.exception("Attempt result query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Mỗi answer row hiện được ánh xạ thành một phần tử có question_id.
    # Quy tắc gom nhiều row theo question và thứ tự answers chưa được DD chốt.
    try:
        attempt = _build_attempt_result(attempt_row, answer_rows)
    except:
        logger.exception("Attempt result mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # exclude_none=True chọn cách bỏ các field optional có giá trị None;
    # quy tắc omit/null của DD vẫn đang để mở.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Attempt result retrieved.",
        trace_id=trace_id,
        data=attempt.model_dump(mode="json", exclude_none=True),
    )