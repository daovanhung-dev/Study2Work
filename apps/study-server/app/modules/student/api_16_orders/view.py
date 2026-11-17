from __future__ import annotations

import logging
from decimal import Decimal, InvalidOperation
from typing import Any

from app.core.database import query_one
from app.core.responses import error_response, success_response
from app.modules.student.api_16_orders.models import Order
from app.modules.student.api_16_orders.query import FIND_ORDER_COURSE, INSERT_ORDER
from app.modules.student.api_16_orders.validate import validate_order_request
from pydantic import ValidationError
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


def create_order(*, authorization: str | None, payload: Any, db: Session, trace_id: str) -> dict[str, Any] | JSONResponse:
    validated = validate_order_request(authorization, payload, trace_id=trace_id)
    if isinstance(validated, JSONResponse):
        return validated
    user_id, body = validated
    try:
        course = query_one(db, FIND_ORDER_COURSE, {"course_id": body.course_id})
        if course is None or str(course.get("status", "")).upper() != "PUBLISHED":
            return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Course is not eligible for a paid order.", trace_id=trace_id)
        amount = Decimal(str(course.get("price", "0")))
        if not amount.is_finite() or amount <= 0:
            return error_response(status_code=422, business_code="DESIGN_VALIDATION_ERROR", message="Course is not eligible for a paid order.", trace_id=trace_id)
        row = query_one(db, INSERT_ORDER, {"user_id": user_id, "course_id": body.course_id, "amount": amount, "payment_provider": body.payment_provider})
        if row is None:
            db.rollback()
            return _internal_error(trace_id)
        order = Order.model_validate(row)
        db.commit()
    except (SQLAlchemyError, ValidationError, InvalidOperation, TypeError):
        db.rollback()
        logger.exception("Create Order failed; trace_id=%s", trace_id)
        return _internal_error(trace_id)
    return success_response(business_code="DESIGN_RESOURCE_CREATED", message="Order created.", trace_id=trace_id, data=order.model_dump(mode="json"))


def _internal_error(trace_id: str) -> JSONResponse:
    return error_response(status_code=500, business_code="DESIGN_INTERNAL_ERROR", message="Order could not be created.", trace_id=trace_id)
