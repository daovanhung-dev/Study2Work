"""Cung cấp các hàm tạo, kiểm tra và quản lý trace ID trong request cùng ContextVar của tiến
trình."""

from contextvars import ContextVar, Token
from uuid import UUID, uuid4

from fastapi import Request

TRACE_HEADER = "X-Trace-Id"

_current_trace_id: ContextVar[str | None] = ContextVar(
    "current_trace_id",
    default=None,
)


def create_trace_id() -> str:
    """Tạo UUID phiên bản 4 và trả về dạng chuỗi canonical dùng làm mã theo dõi request."""

    return str(uuid4())


def validate_trace_id(trace_id: str | None) -> str | None:
    """Kiểm tra chuỗi đầu vào có phải UUID hợp lệ hay không và chuẩn hóa UUID về dạng chuỗi chuẩn.
    Trả None khi giá trị vắng mặt hoặc không phân tích được."""

    if not trace_id:
        return None

    try:
        return str(UUID(trace_id))
    except ValueError:
        return None


def get_trace_id(request: Request) -> str:
    """Đọc trace ID từ request.state, kiểm tra định dạng UUID rồi trả giá trị đã chuẩn hóa. Nếu
    state thiếu hoặc không hợp lệ, tạo UUID mới, ghi lại vào request.state và trả về."""

    trace_id = getattr(
        request.state,
        "trace_id",
        None,
    )

    trace_id = validate_trace_id(trace_id)

    if trace_id is None:
        trace_id = create_trace_id()
        request.state.trace_id = trace_id

    return trace_id


def set_trace_id(trace_id: str) -> Token[str | None]:
    """Đặt trace ID vào ContextVar của luồng thực thi hiện tại. Trả về Token để reset_trace_id có
    thể khôi phục context trước đó sau khi request kết thúc."""

    return _current_trace_id.set(trace_id)


def get_current_trace_id() -> str | None:
    """Đọc trace ID từ ContextVar mà không cần truyền Request. Trả None nếu chưa có trace context
    trong luồng hiện tại."""

    return _current_trace_id.get()


def reset_trace_id(token: Token[str | None]) -> None:
    """Khôi phục giá trị ContextVar trước lần set_trace_id tương ứng bằng Token đã nhận. Middleware
    gọi hàm này trong finally để không rò trace giữa các request."""

    _current_trace_id.reset(token)
