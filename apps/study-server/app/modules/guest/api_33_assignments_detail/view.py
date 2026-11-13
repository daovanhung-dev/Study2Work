"""Xử lý nghiệp vụ và điều phối dữ liệu cho API #33 chi tiết assignment."""

from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.guest.api_33_assignments_detail.models import AssignmentDetail
from app.modules.guest.api_33_assignments_detail.query import ASSIGNMENT_BY_ID
from app.modules.guest.api_33_assignments_detail.validate import (
    assignment_not_found,
    validate_assignment_id,
)

from app.utils.auth import validate_current_user_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def find_assignment(
    db: Session,
    *,
    assignment_id: int,
) -> dict[str, Any] | None:
    """Đọc một assignment theo ID, không thực hiện thay đổi dữ liệu."""

    return query_one(
        db,
        ASSIGNMENT_BY_ID,
        {"assignment_id": assignment_id},
    )


def _internal_error(trace_id: str) -> JSONResponse:
    """Tạo response 500 an toàn khi truy vấn hoặc ánh xạ assignment thất bại."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Assignment could not be retrieved.",
        trace_id=trace_id,
    )


# API #33 assignments_detail
def get_assignment_detail(
    *,
    assignment_id: str,
    authorization: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, đọc assignment và trả về chi tiết theo contract API #33."""

    # 1. Xác thực Bearer JWT và role Student trước khi truy cập database.
    auth_result = validate_current_user_request(
        authorization,
        trace_id=trace_id,
    )
    if isinstance(auth_result, JSONResponse):
        return auth_result

    # 2. Validate assignment_id trước khi truy vấn.
    validated_assignment_id = validate_assignment_id(
        assignment_id,
        trace_id=trace_id,
    )
    if isinstance(validated_assignment_id, JSONResponse):
        return validated_assignment_id

    # 3. Đọc assignment theo ID.
    try:
        assignment_row = find_assignment(
            db,
            assignment_id=validated_assignment_id,
        )
    except SQLAlchemyError:
        logger.exception(
            "Assignment detail lookup failed; trace_id=%s",
            trace_id,
        )
        return _internal_error(trace_id)

    # 4. Không tìm thấy assignment thì trả 404 theo API catalog.
    if assignment_row is None:
        return assignment_not_found(trace_id)

    # 5. Ánh xạ kết quả query sang schema response.
    try:
        assignment = AssignmentDetail.model_validate(assignment_row)
    except:
        logger.exception(
            "Assignment detail mapping failed; trace_id=%s",
            trace_id,
        )
        return _internal_error(trace_id)

    # 6. Trả envelope thành công theo contract API #33.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Assignment retrieved.",
        trace_id=trace_id,
        data=assignment.model_dump(mode="json"),
    )