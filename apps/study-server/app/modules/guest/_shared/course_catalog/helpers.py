from __future__ import annotations

from decimal import Decimal
from typing import Any

from app.core.responses import ApiError, _ApiError
from app.modules.guest._shared.course_catalog.constants import (
    SORT_COLUMNS,
    SORT_DIRECTIONS,
    SORT_FIELDS,
)
from app.modules.guest._shared.course_catalog.models import Course, MentorSummary


def normalize_sort(value: str | None) -> str | None:
    """Kiểm tra biểu thức sort tùy chọn theo dạng field:direction. Trả None nếu không truyền; nếu
    có, chỉ chấp nhận field và direction trong allowlist, còn định dạng hoặc giá trị không hỗ
    trợ sẽ phát sinh ValueError."""

    if value is None:
        return None

    parts = value.split(":")
    if len(parts) != 2:
        raise ValueError("sort phải có định dạng field:direction.")

    field, direction = parts
    if field not in SORT_FIELDS:
        raise ValueError("sort field không được hỗ trợ.")
    if direction not in SORT_DIRECTIONS:
        raise ValueError("sort direction không được hỗ trợ.")
    return f"{field}:{direction}"


def build_order_by(sort: str | None) -> str:
    """Chuyển sort đã kiểm tra thành biểu thức ORDER BY lấy cột từ allowlist tĩnh. Khi không truyền
    sort, dùng thứ tự mặc định; với field khác id, thêm c.id làm khóa phụ ổn định. Dữ liệu sort
    không hợp lệ phát sinh ApiError 422."""

    if sort is None:
        return "c.created_at DESC, c.id ASC"

    field, direction = sort.split(":")
    if field not in SORT_FIELDS or field not in SORT_COLUMNS:
        raise ApiError(
            status_code=422,
            business_code="DESIGN_VALIDATION_ERROR",
            message="sort field không được hỗ trợ.",
        )

    column = SORT_COLUMNS[field]
    direction_sql = direction.upper()
    if field == "id":
        return f"{column} {direction_sql}"
    return f"{column} {direction_sql}, c.id ASC"


def map_course(row: dict[str, Any]) -> Course:
    """Ánh xạ một hàng SQL đã join thành model Course công khai, bao gồm mentor projection và giá
    được tuần tự hóa thành chuỗi thập phân. Thiếu mentor ID hoặc tên mentor phát sinh ApiError
    để caller xử lý lỗi toàn vẹn dữ liệu."""

    mentor_id = row.get("mentor_id")
    mentor_name = row.get("mentor_full_name")
    if mentor_id is None or mentor_name is None:
        raise ApiError()

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
    giá trị None bằng ApiError và giữ dạng thập phân chính xác theo giá trị nguồn."""

    if value is None:
        raise ApiError()
    return format(Decimal(str(value)), "f")


def course_internal_error(trace_id: str) -> _ApiError:
    """Tạo _ApiError HTTP 500 dùng chung cho lỗi đọc hoặc ánh xạ khóa học. Hàm gắn business code
    nội bộ, thông điệp an toàn và trace ID do caller cung cấp."""

    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Courses could not be retrieved.",
        trace_id=trace_id,
    )
