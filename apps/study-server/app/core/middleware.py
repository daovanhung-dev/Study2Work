"""Cung cấp middleware trace ID và các handler chuyển lỗi của FastAPI thành phản hồi an toàn,
thống nhất."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import Any

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from app.core.responses import ApiError, ErrorDetail
from app.core.trace import (
    TRACE_HEADER,
    create_trace_id,
    get_trace_id,
    reset_trace_id,
    set_trace_id,
    validate_trace_id,
)

logger = logging.getLogger(__name__)

DESIGN_CONTRACT_PATHS = {
    "/api/v1/auth/register",
    "/api/v1/auth/login",
    "/api/v1/auth/refresh",
    "/api/v1/auth/verify-email/send",
    "/api/v1/categories",
    "/api/v1/courses",
    "/api/v1/courses/search",
}


def _validation_field(location: Sequence[Any]) -> str | None:
    """Chuyển vị trí lỗi Pydantic thành tên trường dễ đọc bằng cách bỏ các tiền tố giao thức như
    body, query, path, header và cookie. Các phần còn lại được nối bằng dấu chấm; nếu không còn
    phần nào thì trả về None."""
    ignored_locations = {"body", "query", "path", "header", "cookie"}
    parts = [str(part) for part in location if str(part) not in ignored_locations]
    return ".".join(parts) or None


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    """Chuyển HTTPException thành JSONResponse an toàn, giữ status code và header gốc. Chỉ dùng
    business code, message, data và meta từ detail khi detail đã có dạng error envelope; các
    detail tùy ý khác không được phản chiếu ra client."""

    detail: dict[str, Any] = exc.detail if isinstance(exc.detail, dict) else {}
    has_error_envelope = detail.get("success") is False
    meta = detail.get("meta") if has_error_envelope else None
    return ApiError(
        status_code=exc.status_code,
        business_code=(
            str(detail["businessCode"])
            if has_error_envelope and detail.get("businessCode")
            else "HTTP_ERROR"
        ),
        message=(
            str(detail["message"])
            if has_error_envelope and detail.get("message")
            else "Yêu cầu không thể được xử lý."
        ),
        trace_id=get_trace_id(request),
        data=detail.get("data") if has_error_envelope else None,
        meta=meta if isinstance(meta, dict) else None,
        headers=exc.headers,
    )


async def request_validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Chuyển từng lỗi RequestValidationError thành ErrorDetail, chuẩn hóa vị trí trường rồi dựng
    ApiError HTTP 422. Endpoint thuộc DESIGN_CONTRACT_PATHS dùng business code thiết kế tương
    ứng; endpoint khác dùng VALIDATION_ERROR."""

    errors = [
        ErrorDetail(
            field=_validation_field(error.get("loc", ())),
            code=str(error.get("type", "INVALID_FIELD")).upper().replace(".", "_"),
            message=str(error.get("msg", "Giá trị không hợp lệ.")),
        )
        for error in exc.errors()
    ]
    return ApiError(
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
        business_code=(
            "DESIGN_VALIDATION_ERROR"
            if request.url.path in DESIGN_CONTRACT_PATHS
            else "VALIDATION_ERROR"
        ),
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=get_trace_id(request),
        errors=errors,
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Ghi exception nội bộ cùng trace ID vào log nhưng chỉ trả message an toàn cho client.
    Business code được chọn theo endpoint và ApiError dựng trực tiếp envelope cùng header trace."""

    trace_id = get_trace_id(request)
    logger.exception("Unhandled API error; trace_id=%s", trace_id, exc_info=exc)
    business_code = (
        "DESIGN_INTERNAL_ERROR"
        if request.url.path in DESIGN_CONTRACT_PATHS
        else "INTERNAL_SERVER_ERROR"
    )
    return ApiError(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        business_code=business_code,
        message="Đã xảy ra lỗi nội bộ hệ thống.",
        trace_id=trace_id,
    )


class TraceIdMiddleware(BaseHTTPMiddleware):
    """Middleware gắn một trace ID hợp lệ vào request, context hiện tại và response. Middleware
    chuyển các lỗi thoát khỏi route qua handler dùng chung rồi luôn khôi phục context trước khi
    kết thúc request."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        """Thiết lập trace ID hợp lệ từ header hoặc tạo UUID mới, lưu vào request và ContextVar rồi
        gọi middleware kế tiếp. Hàm gắn trace ID vào response; nếu exception thoát ra, chuyển
        lỗi qua handler dùng chung và luôn khôi phục ContextVar trong finally."""
        trace_id = validate_trace_id(request.headers.get(TRACE_HEADER)) or create_trace_id()
        request.state.trace_id = trace_id
        context_token = set_trace_id(trace_id)

        try:
            response = await call_next(request)
            response.headers[TRACE_HEADER] = trace_id
            return response
        except Exception as exc:
            response = await unhandled_exception_handler(request, exc)
            response.headers[TRACE_HEADER] = trace_id
            return response
        finally:
            reset_trace_id(context_token)
