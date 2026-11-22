"""Xác thực Admin và chuẩn hóa kỳ báo cáo cho API #101."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.core.responses import ErrorDetail, error_response
from app.modules.admin.api_101_admin_reports_summary.models import AdminReportPeriod
from app.utils.auth import validate_current_user_request
from pydantic import TypeAdapter, ValidationError
from starlette.responses import JSONResponse

_DATE_ADAPTER = TypeAdapter(date)
_VIETNAM_TIMEZONE = ZoneInfo("Asia/Ho_Chi_Minh")


def vietnam_today() -> date:
    """Trả về ngày lịch hiện tại theo múi giờ Study Admin đã chốt."""

    return datetime.now(_VIETNAM_TIMEZONE).date()


def _invalid_date(field: str, *, trace_id: str) -> JSONResponse:
    """Dựng lỗi validation chuẩn cho một query date không hợp lệ."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field=field,
                code="DATE_PARSING",
                message="Input should be a valid date",
            )
        ],
    )


def _invalid_period(*, trace_id: str) -> JSONResponse:
    """Dựng lỗi validation chuẩn khi ngày bắt đầu sau ngày kết thúc."""

    return error_response(
        status_code=422,
        business_code="DESIGN_VALIDATION_ERROR",
        message="Dữ liệu đầu vào không hợp lệ.",
        trace_id=trace_id,
        errors=[
            ErrorDetail(
                field="from",
                code="DATE_RANGE",
                message="from must be on or before to",
            )
        ],
    )


def _parse_date(value: str | None, *, field: str, trace_id: str) -> date | None | JSONResponse:
    """Parse một ISO calendar date hoặc trả lỗi validation API hiện có."""

    if value is None:
        return None
    try:
        # TypeAdapter giữ parser date chuẩn của Pydantic mà không để lỗi lộ qua route.
        return _DATE_ADAPTER.validate_python(value)
    except ValidationError:
        # Gắn lỗi vào đúng query field để client nhận envelope thống nhất.
        return _invalid_date(field, trace_id=trace_id)


def validate_admin_report_summary_request(
    authorization: str | None,
    *,
    from_value: str | None,
    to_value: str | None,
    trace_id: str,
) -> AdminReportPeriod | JSONResponse:
    """Yêu cầu role ADMIN trước khi parse query rồi tạo kỳ inclusive mặc định 30 ngày."""

    # Dùng guard chung Study để xác thực Bearer/JWT và quyền ADMIN.
    authentication = validate_current_user_request(
        authorization,
        role="ADMIN",
        trace_id=trace_id,
        internal_error_message="Report summary could not be retrieved.",
    )
    if isinstance(authentication, JSONResponse):
        return authentication

    # Parse raw query sau auth để lỗi input không vượt trước quyền truy cập.
    parsed_from = _parse_date(from_value, field="from", trace_id=trace_id)
    if isinstance(parsed_from, JSONResponse):
        return parsed_from
    parsed_to = _parse_date(to_value, field="to", trace_id=trace_id)
    if isinstance(parsed_to, JSONResponse):
        return parsed_to

    # Chụp ngày hôm nay một lần để hai bound không lệch qua nửa đêm Việt Nam.
    today = vietnam_today()
    effective_to = parsed_to or today
    effective_from = parsed_from or (effective_to - timedelta(days=29))
    if effective_from > effective_to:
        return _invalid_period(trace_id=trace_id)

    # Trả period đã chuẩn hóa cho query và response dùng cùng hai bound.
    return AdminReportPeriod(from_date=effective_from, to_date=effective_to)
