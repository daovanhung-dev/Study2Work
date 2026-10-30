from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.responses import ErrorDetail, error_response
from app.modules.guest._shared.course_catalog.constants import SORT_COLUMNS, SORT_DIRECTIONS
from app.modules.guest._shared.course_catalog.models import Course, MentorSummary
from app.utils.validate import parse_integer
from pydantic import ValidationError
from starlette.responses import JSONResponse


def build_order_by(sort: str | None) -> str | ErrorDetail:
    """Chuyển sort đã kiểm tra thành biểu thức ORDER BY lấy cột từ allowlist tĩnh. Khi không truyền
    sort, dùng thứ tự mặc định; với field khác id, thêm c.id làm khóa phụ ổn định. Sort không hợp
    lệ được trả dưới dạng ErrorDetail để caller ánh xạ an toàn."""

    if sort is None:
        return "c.created_at DESC, c.id ASC"

    parts = sort.split(":")
    if len(parts) != 2:
        return ErrorDetail(code="VALUE_ERROR", message="sort must use field:direction format.")
    field, direction = parts
    if field not in SORT_COLUMNS or direction not in SORT_DIRECTIONS:
        return ErrorDetail(code="VALUE_ERROR", message="sort field không được hỗ trợ.")

    column = SORT_COLUMNS[field]
    direction_sql = direction.upper()
    if field == "id":
        return f"{column} {direction_sql}"
    return f"{column} {direction_sql}, c.id ASC"


def map_course(row: dict[str, Any]) -> Course | ErrorDetail:
    """Ánh xạ một hàng SQL đã join thành model Course công khai, bao gồm mentor projection và giá
    được tuần tự hóa thành chuỗi thập phân. Dữ liệu thiếu hoặc sai được trả thành ErrorDetail để
    caller xử lý lỗi toàn vẹn."""

    mentor_id = row.get("mentor_id")
    mentor_name = row.get("mentor_full_name")
    if mentor_id is None or mentor_name is None:
        return ErrorDetail(
            code="COURSE_MAPPING_ERROR",
            message="Course mentor information is incomplete.",
        )

    price = decimal_string(row.get("price"))
    if isinstance(price, ErrorDetail):
        return price

    try:
        return Course(
            id=row.get("id"),
            title=row.get("title"),
            description=row.get("description"),
            thumbnail_url=row.get("thumbnail_url"),
            price=price,
            status=row.get("status"),
            mentor=MentorSummary(
                id=mentor_id,
                full_name=mentor_name,
                avatar_url=row.get("mentor_avatar_url"),
            ),
        )
    except ValidationError:
        return ErrorDetail(
            code="COURSE_MAPPING_ERROR",
            message="Course row is incomplete or invalid.",
        )


def decimal_string(value: Any) -> str | ErrorDetail:
    """Chuyển giá sang chuỗi decimal chính xác hoặc trả ErrorDetail nếu giá thiếu/sai."""

    if value is None:
        return ErrorDetail(code="COURSE_MAPPING_ERROR", message="Course price is missing.")
    try:
        return format(Decimal(str(value)), "f")
    except InvalidOperation:
        return ErrorDetail(code="COURSE_MAPPING_ERROR", message="Course price is invalid.")


def normalize_course_count(value: Any) -> int | ErrorDetail:
    """Chuẩn hóa count từ hàng SQL thành số nguyên không âm hoặc ErrorDetail an toàn."""

    if value is None:
        return 0
    if type(value) is int:
        count = value
    elif isinstance(value, str):
        count = parse_integer(value)
    else:
        count = None

    if count is None or count < 0:
        return ErrorDetail(
            code="COURSE_MAPPING_ERROR",
            message="Course count is invalid.",
        )
    return count


def course_internal_error(trace_id: str) -> JSONResponse:
    """Tạo JSONResponse HTTP 500 dùng chung cho lỗi đọc hoặc ánh xạ khóa học. Hàm gắn business code
    nội bộ, thông điệp an toàn và trace ID do caller cung cấp."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Courses could not be retrieved.",
        trace_id=trace_id,
    )
