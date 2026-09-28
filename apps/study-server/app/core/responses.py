"""Định nghĩa kiểu chi tiết lỗi, factory lỗi API và các hàm dựng envelope phản hồi của Study
API."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from fastapi import status
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ConfigDict
from starlette.responses import JSONResponse

from app.core.trace import create_trace_id, get_current_trace_id

INTERNAL_ERROR_MESSAGE = "Đã xảy ra lỗi nội bộ hệ thống."


class ErrorDetail(BaseModel):
    """Mô tả một lỗi kiểm tra hoặc lỗi nghiệp vụ an toàn có thể trả cho client. Trường ngoài schema
    bị từ chối để tránh vô tình đưa dữ liệu không được hỗ trợ vào response."""

    field: str | None = None
    code: str
    message: str

    model_config = ConfigDict(extra="forbid")


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
) -> JSONResponse:
    """Dựng và trả JSONResponse envelope lỗi chuẩn cùng HTTP status và trace header.

    Trace ID ưu tiên giá trị truyền vào, sau đó lấy từ ContextVar hoặc tạo UUID mới. Mapping được
    sao chép; ErrorDetail được tuần tự hóa dưới meta.fieldErrors.
    """
    resolved_trace_id = trace_id or get_current_trace_id() or create_trace_id()
    response_meta = dict(meta or {})
    if errors:
        response_meta["fieldErrors"] = [detail.model_dump() for detail in errors]

    response_headers = {
        key: value
        for key, value in (headers or {}).items()
        if key.lower() != "x-trace-id"
    }
    response_headers["X-Trace-Id"] = resolved_trace_id

    return JSONResponse(
        status_code=status_code,
        headers=response_headers,
        content=jsonable_encoder({
            "success": False,
            "businessCode": business_code,
            "message": message,
            "data": data if data is not None else {},
            "meta": response_meta,
            "traceId": resolved_trace_id,
        }),
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
