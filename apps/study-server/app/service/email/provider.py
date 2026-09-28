from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class VerificationDispatchResult:
    """Chứa kết quả provider trả về khi tiếp nhận yêu cầu gửi email, gồm trạng thái và lý do tùy
    chọn."""

    status: str
    reason: str | None = None


class VerificationEmailProvider(Protocol):
    """Định nghĩa giao diện provider cần có để tiếp nhận yêu cầu gửi email xác minh hoặc báo lỗi."""

    def dispatch(
        self,
        *,
        user_id: int,
        email: str,
        trace_id: str,
    ) -> VerificationDispatchResult:
        """Cài đặt giao diện provider để tiếp nhận một yêu cầu gửi email xác minh với user ID,
        email và trace ID. Provider mặc định là stub phát triển: bỏ qua dữ liệu đầu vào và trả
        trạng thái accepted mà không gửi email thật."""


class StubVerificationEmailProvider:
    """Provider phát triển chỉ xác nhận đã tiếp nhận yêu cầu; không gửi email thật và không tạo
    token xác minh."""

    def dispatch(
        self,
        *,
        user_id: int,
        email: str,
        trace_id: str,
    ) -> VerificationDispatchResult:
        """Cài đặt giao diện provider để tiếp nhận một yêu cầu gửi email xác minh với user ID,
        email và trace ID. Provider mặc định là stub phát triển: bỏ qua dữ liệu đầu vào và trả
        trạng thái accepted mà không gửi email thật."""
        del user_id, email, trace_id
        return VerificationDispatchResult(status="accepted")


def get_verification_email_provider() -> VerificationEmailProvider:
    """Tạo và trả provider mặc định cho runtime Study hiện tại. Giá trị trả về là
    StubVerificationEmailProvider; caller có thể thay bằng dependency override khi cần provider
    khác."""

    return StubVerificationEmailProvider()
