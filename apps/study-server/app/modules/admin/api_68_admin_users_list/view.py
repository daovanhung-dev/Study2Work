"""Điều phối xác thực, truy vấn và dựng response danh sách Admin user API #68."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from typing import Any

from app.core.database import query_many, query_one
from app.core.responses import error_response, success_response
from app.modules.admin.api_68_admin_users_list.models import (
    AdminUsersPage,
    AdminUsersPagination,
    AdminUsersQuery,
)
from app.modules.admin.api_68_admin_users_list.query import COUNT_ADMIN_USERS, LIST_ADMIN_USERS
from app.modules.admin.api_68_admin_users_list.validate import (
    validate_admin_request,
    validate_admin_users_query,
)
from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)
DEFAULT_PAGE_SIZE = 20
MAX_INT64 = 2**63 - 1


def _internal_error(trace_id: str) -> JSONResponse:
    """Dựng lỗi 500 an toàn cho query hoặc mapping danh sách user."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Users could not be retrieved.",
        trace_id=trace_id,
    )


def _rollback_safely(db: Session, *, trace_id: str) -> None:
    """Dọn transaction đọc lỗi mà không che response lỗi ban đầu."""

    try:
        db.rollback()
    except SQLAlchemyError:
        logger.error("Admin users rollback failed; trace_id=%s", trace_id)


def _map_user_profile(row: Mapping[str, Any]) -> UserProfile | None:
    """Kiểm tra projection user và dùng cùng safe model với API #04/#14."""

    if (
        type(row.get("id")) is not int
        or not 1 <= row["id"] <= MAX_INT64
        or not isinstance(row.get("full_name"), str)
        or not isinstance(row.get("email"), str)
        or not isinstance(row.get("role"), str)
        or not isinstance(row.get("status"), str)
        or (row.get("avatar_url") is not None and not isinstance(row.get("avatar_url"), str))
        or (row.get("phone") is not None and not isinstance(row.get("phone"), str))
    ):
        return None
    try:
        return UserProfile.model_validate(row)
    except (TypeError, ValidationError):
        return None


def _query_parameters(query: AdminUsersQuery) -> dict[str, Any]:
    """Gom bind values để count và page luôn dùng chung filter predicates."""

    return {
        "role": query.role,
        "status": query.status,
        "keyword": query.keyword,
    }


# API #68 admin_users_list
def get_admin_users(
    *,
    authorization: str | None,
    role: str | None,
    status: str | None,
    keyword: str | None,
    page_value: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Yêu cầu role ADMIN, lọc và phân trang safe UserProfile rows rồi trả Page envelope."""

    # Xác thực Bearer/JWT và role Admin trước mọi truy vấn người dùng.
    authentication = validate_admin_request(authorization, trace_id=trace_id)
    if isinstance(authentication, JSONResponse):
        return authentication

    # Kiểm tra page int32 và chuẩn hóa keyword theo helper dùng chung.
    validated_query = validate_admin_users_query(
        role=role,
        status=status,
        keyword=keyword,
        page_value=page_value,
        trace_id=trace_id,
    )
    if isinstance(validated_query, JSONResponse):
        return validated_query

    # Dùng cùng predicates cho count/page và chỉ bind các giá trị ngoài SQL.
    base_params = _query_parameters(validated_query)
    offset = (validated_query.page - 1) * DEFAULT_PAGE_SIZE
    page_params = {
        **base_params,
        "limit": DEFAULT_PAGE_SIZE,
        "offset": offset,
    }
    try:
        count_row = query_one(db, COUNT_ADMIN_USERS, base_params)
        rows = query_many(db, LIST_ADMIN_USERS, page_params)
    except SQLAlchemyError:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin users query failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Không chấp nhận count projection thiếu, âm hoặc không phải số nguyên.
    if not isinstance(count_row, Mapping):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin users count projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    total = count_row.get("total")
    if type(total) is not int or not 0 <= total <= MAX_INT64:
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin users total mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    if not isinstance(rows, list):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin users page projection failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Map từng row qua profile allowlist; response model loại bỏ mọi field thừa.
    items: list[UserProfile] = []
    for row in rows:
        if not isinstance(row, Mapping):
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin users row projection failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        profile = _map_user_profile(row)
        if profile is None:
            _rollback_safely(db, trace_id=trace_id)
            logger.error("Admin users profile mapping failed; trace_id=%s", trace_id)
            return _internal_error(trace_id)
        items.append(profile)

    # Tính số trang từ count cùng filter; danh sách rỗng hợp lệ với HTTP 200.
    try:
        total_pages = (total + DEFAULT_PAGE_SIZE - 1) // DEFAULT_PAGE_SIZE if total else 0
        page = AdminUsersPage(
            items=items,
            pagination=AdminUsersPagination(
                page=validated_query.page,
                size=DEFAULT_PAGE_SIZE,
                total=total,
                total_pages=total_pages,
            ),
        )
    except (TypeError, ValidationError):
        _rollback_safely(db, trace_id=trace_id)
        logger.error("Admin users pagination mapping failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)

    # Trả response chỉ đọc; Session do dependency sở hữu và không commit ở đây.
    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Users retrieved." if items else "No users found.",
        trace_id=trace_id,
        data=page.model_dump(mode="json"),
    )
