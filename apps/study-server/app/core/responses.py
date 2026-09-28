"""Định nghĩa kiểu chi tiết lỗi, factory lỗi API và các hàm dựng envelope phản hồi của Study
API."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import status
from pydantic import BaseModel, ConfigDict

from app.core.trace import create_trace_id, get_current_trace_id

INTERNAL_ERROR_MESSAGE = "Đã xảy ra lỗi nội bộ hệ thống."


class ErrorDetail(BaseModel):
    """Mô tả một lỗi kiểm tra hoặc lỗi nghiệp vụ an toàn có thể trả cho client. Trường ngoài schema
    bị từ chối để tránh vô tình đưa dữ liệu không được hỗ trợ vào response."""

    field: str | None = None
    code: str
    message: str

    model_config = ConfigDict(extra="forbid")


class _ApiError(Exception):
    """Kiểu exception nội bộ mà factory ApiError tạo ra để mang HTTP status, business code, thông
    điệp an toàn, trace ID, dữ liệu, metadata, lỗi trường và header tùy chọn."""

    def __init__(
        self,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        business_code: str = "INTERNAL_SERVER_ERROR",
        message: str = INTERNAL_ERROR_MESSAGE,
        trace_id: str | None = None,
        data: Any = None,
        meta: Mapping[str, Any] | None = None,
        errors: Sequence[ErrorDetail] = (),
        headers: Mapping[str, str] | None = None,
    ) -> None:
        """Khởi tạo exception nội bộ với status, business code, message, data, metadata, field
        errors và header đã chuẩn hóa. Trace ID ưu tiên giá trị được truyền vào, sau đó lấy từ
        ContextVar hoặc tạo UUID mới; mapping được sao chép và errors được chuyển thành tuple để
        tránh caller sửa state nội bộ."""
        super().__init__(message)

        self.status_code = status_code
        self.business_code = business_code
        self.message = message
        self.trace_id = trace_id or get_current_trace_id() or create_trace_id()
        self.data = data
        self.meta = dict(meta or {})
        self.errors = tuple(errors)
        self.headers = dict(headers or {})

def ApiError(
    *,
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
    business_code: str = "INTERNAL_SERVER_ERROR",
    message: str = INTERNAL_ERROR_MESSAGE,
    trace_id: str | None = None,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
    errors: Sequence[ErrorDetail] = (),
    headers: Mapping[str, str] | None = None,
) -> _ApiError:
    """Tạo và trả về một _ApiError để caller có thể giữ cú pháp raise ApiError(...). Tham số mặc
    định tạo lỗi nội bộ HTTP 500 an toàn; factory chuyển nguyên các trường response, lỗi trường
    và header cho exception nội bộ."""

    return _ApiError(
        status_code=status_code,
        business_code=business_code,
        message=message,
        trace_id=trace_id,
        data=data,
        meta=meta,
        errors=errors,
        headers=headers,
    )


def success_response(
    *,
    business_code: str,
    message: str,
    trace_id: str,
    data: Any = None,
    meta: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Dựng dictionary envelope thành công với success, businessCode, message, data, meta và
    traceId. Hàm sao chép meta để không giữ mapping mutable của caller và không tạo response
    HTTP trực tiếp."""

    return {
        "success": True,
        "businessCode": business_code,
        "message": message,
        "data": data,
        "meta": dict(meta or {}),
        "traceId": trace_id,
    }


def error_response(
    error: _ApiError,
) -> dict[str, Any]:
    """Chuyển _ApiError thành dictionary envelope lỗi chuẩn. Hàm sao chép meta, thêm danh sách
    fieldErrors khi có lỗi trường, dùng data rỗng nếu exception không có data và giữ trace ID
    cùng business code đã gắn vào lỗi."""

    response_meta = dict(error.meta)
    if error.errors:
        response_meta["fieldErrors"] = [detail.model_dump() for detail in error.errors]

    return {
        "success": False,
        "businessCode": error.business_code,
        "message": error.message,
        "data": error.data if error.data is not None else {},
        "meta": response_meta,
        "traceId": error.trace_id,
    }
