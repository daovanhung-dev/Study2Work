from __future__ import annotations

import logging
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.shared.api_18_operations.models import Operation
from app.modules.shared.api_18_operations.query import FIND_NOTIFICATION_OPERATION
from app.modules.shared.api_18_operations.validate import validate_operation_request
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def get_operation(*, authorization: str | None, operation_id_raw: str, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_operation_request(authorization, operation_id_raw, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    owner_id, operation_id = validated
    try:
        row = query_one(db, FIND_NOTIFICATION_OPERATION, {"operation_id": operation_id, "owner_id": owner_id})
        if row is None:
            return error_response(status_code=404, business_code="DESIGN_RESOURCE_NOT_FOUND", message="Operation not found.", trace_id=trace_id)
        operation = Operation.model_validate({**row, "kind": "NOTIFICATION_DISPATCH"})
    except (SQLAlchemyError, ValidationError, TypeError):
        db.rollback()
        logger.exception("Operation lookup failed; trace_id=%s", trace_id)
        return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Operation could not be retrieved.", trace_id=trace_id)
    return success_response(business_code="DESIGN_OPERATION_RETRIEVED", message="Operation retrieved.", trace_id=trace_id, data=operation.model_dump(mode="json", exclude_none=True))
