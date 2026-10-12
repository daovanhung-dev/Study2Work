"""Điều phối xác thực, upload Object Storage và response cho API #13."""

from __future__ import annotations

import logging
from typing import Any

from app.core.responses import error_response, success_response
from app.modules.guest.api_13_users_me_avatar.models import (
    AvatarUploadRequest,
    AvatarUploadResult,
)
from app.modules.guest.api_13_users_me_avatar.validate import (
    validate_avatar_upload_request,
)
from app.service.object_storage.avatar import AvatarStorageProvider
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# API #13 users_me_avatar
def upload_avatar(
    *,
    authorization: str | None,
    user_data: AvatarUploadRequest,
    provider: AvatarStorageProvider,
    trace_id: str,
) -> dict[str, Any] | JSONResponse:
    """Xác thực Student, tải avatar lên storage và chỉ trả URL để API #14 cập nhật profile."""

    # Xác thực Student và kiểm tra ảnh trước khi tạo side effect ngoài hệ thống.
    validation = validate_avatar_upload_request(
        authorization,
        user_data,
        trace_id=trace_id,
    )
    if isinstance(validation, JSONResponse):
        return validation
    user_id, avatar_image = validation

    # Gửi bytes đã kiểm tra lên provider; mọi lỗi storage được ánh xạ thành 500 an toàn.
    try:
        avatar_url = provider.upload(
            user_id=user_id,
            content=avatar_image.content,
            content_type=avatar_image.content_type,
        )
        result = AvatarUploadResult(avatar_url=avatar_url)
    except Exception:
        logger.error("Avatar upload failed; trace_id=%s", trace_id)
        return error_response(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Avatar could not be uploaded.",
            trace_id=trace_id,
        )

    # Trả riêng public URL để API #14 lưu vào profile trong bước tiếp theo.
    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Avatar upload accepted",
        trace_id=trace_id,
        data=result.model_dump(mode="json"),
    )
