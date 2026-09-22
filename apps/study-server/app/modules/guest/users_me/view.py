"""Business orchestration for the current-user profile endpoint."""

from __future__ import annotations

import logging
from typing import Any

from app.core.responses import ApiError, success_response
from app.core.security import TokenError, decode_access_token
from app.modules.guest.users_me.models import UserProfile
from app.modules.guest.users_me.query import find_current_user
from app.modules.guest.users_me.validate import extract_bearer_token, validate_access_claims
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def get_current_user(
    *,
    authorization: str | None,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Authenticate the request and return the current Student profile."""

    try:
        token = extract_bearer_token(authorization)
        claims = decode_access_token(token)
        user_id, roles = validate_access_claims(claims)
    except (TokenError, ValueError) as exc:
        raise _authentication_error(trace_id) from exc

    if "STUDENT" not in roles:
        raise _authorization_error(trace_id)

    try:
        user = find_current_user(db, user_id=user_id)
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Current-user lookup failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    if user is None:
        raise _authentication_error(trace_id)

    try:
        profile = UserProfile.model_validate(user)
    except ValidationError as exc:
        logger.exception("Current-user profile mapping failed; trace_id=%s", trace_id)
        raise _internal_error(trace_id) from exc

    return success_response(
        business_code="DESIGN_RESOURCE_RETRIEVED",
        message="Profile retrieved.",
        trace_id=trace_id,
        data=profile.model_dump(mode="json"),
    )


def _authentication_error(trace_id: str) -> ApiError:
    return ApiError(
        status_code=401,
        business_code="DESIGN_AUTHENTICATION_REQUIRED",
        message="Authentication required.",
        trace_id=trace_id,
    )


def _authorization_error(trace_id: str) -> ApiError:
    return ApiError(
        status_code=403,
        business_code="DESIGN_ACCESS_DENIED",
        message="Access denied.",
        trace_id=trace_id,
    )


def _internal_error(trace_id: str) -> ApiError:
    return ApiError(
        status_code=500,
        business_code="DESIGN_INTERNAL_ERROR",
        message="Profile could not be retrieved.",
        trace_id=trace_id,
    )
