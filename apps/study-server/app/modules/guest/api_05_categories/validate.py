"""Chuẩn hóa input cho API #5 đọc danh mục."""

from app.modules.guest.api_05_categories.models import DEFAULT_LOCALE


def resolve_category_locale(locale: str | None) -> str:
    """Dùng locale mặc định hiện tại khi query tùy chọn không được truyền."""

    return locale if locale is not None else DEFAULT_LOCALE
