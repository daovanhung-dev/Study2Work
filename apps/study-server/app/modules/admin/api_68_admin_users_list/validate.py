"""Xác thực Admin và chuẩn hóa filter query cho API #68."""

from __future__ import annotations

import app.utils.auth as auth_utils
from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_68_admin_users_list.models import AdminUsersQuery
from app.utils.validate import normalize_search_query, parse_integer
from starlette.responses import JSONResponse

MAX_PAGE = 2**31 - 1


def validate_admin_request(
    authorization: str | None,
    *,
    trace_id: str,
) -> int | JSONResponse:
    """Dùng shared JWT guard với role ADMIN trước khi đọc dữ liệu người dùng."""

    authentication = auth_utils.validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Users could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication
    admin_id, _roles = authentication
    return admin_id


def validate_admin_users_query(
    *,
    role: str | None,
    status: str | None,
    keyword: str | None,
    page_value: str | None,
    trace_id: str,
) -> AdminUsersQuery | JSONResponse:
    """Kiểm tra int32 page, chuẩn hóa keyword và giữ role/status exact-match."""

    page = 1 if page_value is None else parse_integer(page_value)
    if page is None:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="page",
                    code="INT_PARSING",
                    message="Input should be a valid integer",
                )
            ],
        )
    if page < 1:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="page",
                    code="GREATER_THAN_EQUAL",
                    message="Input should be greater than or equal to 1",
                )
            ],
        )
    if page > MAX_PAGE:
        return error_response(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="Dữ liệu đầu vào không hợp lệ.",
            trace_id=trace_id,
            errors=[
                ErrorDetail(
                    field="page",
                    code="LESS_THAN_EQUAL",
                    message="Input should be less than or equal to 2147483647",
                )
            ],
        )

    return AdminUsersQuery(
        role=role,
        status=status,
        keyword=normalize_search_query(keyword),
        page=page,
    )
