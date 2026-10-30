"""Khai báo query và response models cho API #68."""

from __future__ import annotations

from typing import Annotated, Any

from app.modules.guest.api_04_users_me.models import UserProfile
from pydantic import BaseModel, ConfigDict, Field


class AdminUsersQuery(BaseModel):
    """Khai báo các filter và trang đã chuẩn hóa của API #68."""

    role: str | None = None
    status: str | None = None
    keyword: str | None = None
    page: Annotated[int, Field(strict=True, ge=1, le=2**31 - 1)] = 1

    model_config = ConfigDict(extra="forbid")


class AdminUsersPagination(BaseModel):
    """Metadata trang kết quả Admin có kích thước cố định."""

    page: Annotated[
        int,
        Field(strict=True, ge=1, le=2**31 - 1, json_schema_extra={"format": "int32"}),
    ]
    size: Annotated[int, Field(strict=True, ge=1, le=2**31 - 1)]
    total: Annotated[
        int,
        Field(strict=True, ge=0, le=2**63 - 1, json_schema_extra={"format": "int64"}),
    ]
    total_pages: Annotated[
        int,
        Field(strict=True, ge=0, le=2**31 - 1, json_schema_extra={"format": "int32"}),
    ]

    model_config = ConfigDict(extra="forbid")


class AdminUsersPage(BaseModel):
    """Gom profile an toàn và metadata phân trang cho màn hình AC-31."""

    items: list[UserProfile]
    pagination: AdminUsersPagination

    model_config = ConfigDict(extra="forbid")


class GetAdminUsersEnvelope(BaseModel):
    """Success envelope API #68 chứa một trang UserProfile."""

    success: bool
    businessCode: str
    message: str
    data: AdminUsersPage
    meta: dict[str, Any]
    traceId: str

    model_config = ConfigDict(extra="forbid")
