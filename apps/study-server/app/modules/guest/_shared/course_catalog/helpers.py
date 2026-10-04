from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.core.responses import error_response
from app.modules.guest._shared.course_catalog.constants import SORT_COLUMNS, SORT_DIRECTIONS
from app.modules.guest._shared.course_catalog.models import Course, MentorSummary
from starlette.responses import JSONResponse


def build_order_by(sort: str | None) -> str:
    """Chuyển sort đã kiểm tra thành biểu thức ORDER BY lấy cột từ allowlist tĩnh. Khi không truyền
    sort, dùng thứ tự mặc định; với field khác id, thêm c.id làm khóa phụ ổn định. Dữ liệu sort
    không hợp lệ phát sinh ValueError để caller ánh xạ an toàn."""

    if sort is None:
        return "c.created_at DESC, c.id ASC"

    field, direction = sort.split(":")
    if field not in SORT_COLUMNS or direction not in SORT_DIRECTIONS:
        raise ValueError("sort field không được hỗ trợ.")

    column = SORT_COLUMNS[field]
    direction_sql = direction.upper()
    if field == "id":
        return f"{column} {direction_sql}"
    return f"{column} {direction_sql}, c.id ASC"


def map_course(row: dict[str, Any]) -> Course:
    """Ánh xạ một hàng SQL đã join thành model Course công khai, bao gồm mentor projection và giá
    được tuần tự hóa thành chuỗi thập phân. Thiếu mentor ID hoặc tên mentor phát sinh ValueError
    để caller xử lý lỗi toàn vẹn dữ liệu."""

    mentor_id = row.get("mentor_id")
    mentor_name = row.get("mentor_full_name")
    if mentor_id is None or mentor_name is None:
        raise ValueError("Course mentor information is incomplete.")

    return Course(
        id=row.get("id"),
        title=row.get("title"),
        description=row.get("description"),
        thumbnail_url=row.get("thumbnail_url"),
        price=decimal_string(row.get("price")),
        status=row.get("status"),
        mentor=MentorSummary(
            id=mentor_id,
            full_name=mentor_name,
            avatar_url=row.get("mentor_avatar_url"),
        ),
    )


def decimal_string(value: Any) -> str:
    """Chuyển giá khóa học sang chuỗi decimal mà không đưa qua phép tính floating point. Từ chối
    giá trị None bằng ValueError và giữ dạng thập phân chính xác theo giá trị nguồn."""

    if value is None:
        raise ValueError("Course price is missing.")
    return format(Decimal(str(value)), "f")


def course_internal_error(trace_id: str) -> JSONResponse:
    """Tạo JSONResponse HTTP 500 dùng chung cho lỗi đọc hoặc ánh xạ khóa học. Hàm gắn business code
    nội bộ, thông điệp an toàn và trace ID do caller cung cấp."""

    return error_response(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Courses could not be retrieved.",
        trace_id=trace_id,
    )
