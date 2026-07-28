from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.module.auth.model import RegisterRequest
from app.module.auth.query import CREATE_AUTH_CREDENTIAL, CREATE_USER
from app.module.auth.validate import validate_user_create


def _integrity_error_message(exc: IntegrityError) -> str:
    constraint_name = getattr(getattr(exc.orig, "diag", None), "constraint_name", "")

    if constraint_name in {
        "uq_users_email",
        "users_email_key",
        "ux_users_email_normalized",
    }:
        return "Email đã được sử dụng"

    if constraint_name in {
        "uq_users_phone",
        "users_phone_key",
        "ux_users_phone_normalized",
    }:
        return "Số điện thoại đã được sử dụng"

    return "Dữ liệu đăng ký vi phạm ràng buộc hệ thống"


def create_user(
    user_data: RegisterRequest,
    db: Session,
) -> dict[str, Any]:
    validation_error = validate_user_create(user_data)
    if validation_error is not None:
        return validation_error

    now = datetime.now(timezone.utc)
    user_id = uuid4()

    user_params = {
        "id": user_id,
        "display_name": user_data.display_name.strip(),
        "email": user_data.email.strip().lower(),
        "phone": user_data.phone.strip(),
        "created_at": now,
        "updated_at": now,
    }

    credential_params = {
        "user_id": user_id,
        "password_hash": hash_password(user_data.password),
        "password_algorithm": "BCRYPT",
        "password_login_enabled": True,
        "must_change_password": False,
        "failed_login_attempts": 0,
        "locked_until": None,
        "password_changed_at": now,
        "last_login_at": None,
        "created_at": now,
        "updated_at": now,
    }

    try:
        created_user_id = db.execute(
            text(CREATE_USER),
            user_params,
        ).scalar_one()

        credential_params["user_id"] = created_user_id
        db.execute(
            text(CREATE_AUTH_CREDENTIAL),
            credential_params,
        )

        db.commit()

        return {
            "success": True,
            "businessCode": "AUTH_000",
            "message": "Đăng ký tài khoản thành công",
            "data": {
                "userId": str(created_user_id),
                "displayName": user_params["display_name"],
                "email": user_params["email"],
                "phone": user_params["phone"],
            },
        }

    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=_integrity_error_message(exc),
        ) from exc

    except Exception:
        db.rollback()
        raise
