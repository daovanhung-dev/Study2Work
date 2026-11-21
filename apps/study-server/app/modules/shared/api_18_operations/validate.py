from __future__ import annotations

import re
from uuid import UUID

from app.core.responses import error_response
from app.utils.auth import validate_current_user_request
from starlette.responses import JSONResponse

_UUID_PATTERN = re.compile(
    r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
)


def validate_operation_request(
    authorization: str | None,
    operation_id_raw: str,
    *,
    trace_id: str,
) -> tuple[int, UUID] | JSONResponse:
    auth = validate_current_user_request(
        authorization,
        role=("STUDENT", "MENTOR", "ADMIN"),
        trace_id=trace_id,
    )
    if isinstance(auth, JSONResponse):
        return auth
    if not isinstance(operation_id_raw, str) or not _UUID_PATTERN.fullmatch(operation_id_raw):
        return error_response(
            status_code=404,
            business_code="DESIGN_RESOURCE_NOT_FOUND",
            message="Operation not found.",
            trace_id=trace_id,
        )
    operation_id = UUID(operation_id_raw)
    return auth[0], operation_id
