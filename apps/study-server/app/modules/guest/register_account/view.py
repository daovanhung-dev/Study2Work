from __future__ import annotations

import logging
from typing import Any

from app.core.responses import ApiError, success_response
from app.core.security.password import hash_password
from app.modules.guest.register_account.models import RegisterRequest
from app.modules.guest.register_account.query import find_user_by_email, insert_user
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)


def create_user(
    *,
    user_data: RegisterRequest,
    db: Session,
    trace_id: str,
) -> dict[str, Any]:
    """Create an account inside the caller-owned database session."""

    email = str(user_data.email)

    try:
        if find_user_by_email(db, email) is not None:
            db.rollback()
            raise ApiError(
                status_code=409,
                business_code="DESIGN_STATE_CONFLICT",
                message="Email đã tồn tại.",
                trace_id=trace_id,
            )

        created_user = insert_user(
            db,
            full_name=user_data.full_name,
            email=email,
            password_hash=hash_password(user_data.password),
        )
        if created_user is None:
            db.rollback()
            raise ApiError(
                status_code=500,
                business_code="DESIGN_INTERNAL_ERROR",
                message="Không thể tạo tài khoản.",
                trace_id=trace_id,
            )

        db.commit()
    except ApiError:
        raise
    except IntegrityError as exc:
        db.rollback()
        if _is_email_unique_violation(exc):
            raise ApiError(
                status_code=409,
                business_code="DESIGN_STATE_CONFLICT",
                message="Email đã tồn tại.",
                trace_id=trace_id,
            ) from exc
        logger.exception("Account insert integrity error; trace_id=%s", trace_id)
        raise ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Không thể tạo tài khoản.",
            trace_id=trace_id,
        ) from exc
    except SQLAlchemyError as exc:
        db.rollback()
        logger.exception("Account insert database error; trace_id=%s", trace_id)
        raise ApiError(
            status_code=500,
            business_code="DESIGN_INTERNAL_ERROR",
            message="Không thể tạo tài khoản.",
            trace_id=trace_id,
        ) from exc

    logger.info(
        "Verification dispatch deferred after account creation; trace_id=%s",
        trace_id,
        extra={"event": "verification_dispatch_pending", "user_id": created_user["id"]},
    )

    return success_response(
        business_code="DESIGN_RESOURCE_CREATED",
        message="Tạo tài khoản thành công.",
        trace_id=trace_id,
        data=created_user,
    )


def _is_email_unique_violation(exc: IntegrityError) -> bool:
    original = getattr(exc, "orig", None)
    diagnostic = getattr(original, "diag", None)
    return getattr(diagnostic, "constraint_name", None) == "users_email_key"
