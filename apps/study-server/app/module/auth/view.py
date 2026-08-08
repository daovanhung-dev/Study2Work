from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.database import get_db, query_many, query_one
from app.core.responses import ErrorDetail, error_payload, success_payload
from app.core.security import (
    TokenError,
    create_access_token,
    create_refresh_token,
    decode_access_token,
    decode_refresh_token,
    hash_password,
    verify_password,
)
from app.core.trace import get_trace_id
from app.module.auth.model import LoginRequest, RefreshTokenRequest, RegisterRequest
from app.module.auth.query import (
    CREATE_AUTH_CREDENTIAL,
    CREATE_USER,
    GET_LOGIN_USER,
    GET_USER_BY_ID,
    GET_USER_ROLES,
    MARK_LOGIN_SUCCESS,
)
from app.module.auth.validate import validate_user_create


bearer_scheme = HTTPBearer(auto_error=False)


def _roles_for_user(db: Session, user_id: str) -> list[str]:
    rows = query_many(db, GET_USER_ROLES, {"user_id": user_id})
    return [str(row["code"]) for row in rows]


def _next_action(account_status: str) -> str:
    mapping = {
        "REGISTERED_PENDING_VERIFICATION": "VERIFY_CONTACT",
        "VERIFIED": "START_ONBOARDING",
        "ONBOARDING_IN_PROGRESS": "CONTINUE_ONBOARDING",
        "READY_TO_LEARN": "ACTIVATE_LEARNING_PATH",
        "ACTIVE": "OPEN_DASHBOARD",
    }
    return mapping.get(account_status, "OPEN_DASHBOARD")


def _raise_auth_error(
    *,
    status_code: int,
    business_code: str,
    message: str,
    trace_id: str,
) -> None:
    raise HTTPException(
        status_code=status_code,
        detail={
            "success": False,
            "businessCode": business_code,
            "message": message,
            "traceId": trace_id,
        },
        headers={"WWW-Authenticate": "Bearer"}
        if status_code == status.HTTP_401_UNAUTHORIZED
        else None,
    )


def create_user(
    user_data: RegisterRequest,
    db: Session,
    trace_id: str = "",
):
    validation_error = validate_user_create(user_data)
    if validation_error:
        if trace_id:
            validation_error["traceId"] = trace_id
        return validation_error

    now = datetime.now(UTC)
    user_id = str(uuid4())

    try:
        db.execute(
            text(CREATE_USER),
            {
                "id": user_id,
                "display_name": user_data.display_name.strip(),
                "email": user_data.email.strip().lower(),
                "phone": user_data.phone.strip(),
                "created_at": now,
                "updated_at": now,
            },
        )

        db.execute(
            text(CREATE_AUTH_CREDENTIAL),
            {
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
            },
        )
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "businessCode": "ACCOUNT_ALREADY_EXISTS",
                "message": "Email hoặc số điện thoại đã được sử dụng",
                "traceId": trace_id,
            },
        )
    except Exception:
        db.rollback()
        raise

    return success_payload(
        business_code="ACCOUNT_REGISTERED_PENDING_VERIFICATION",
        message="Tạo tài khoản thành công. Cần xác thực thông tin liên hệ.",
        trace_id=trace_id,
        data={
            "userId": user_id,
            "accountStatus": "REGISTERED_PENDING_VERIFICATION",
            "nextAction": "VERIFY_CONTACT",
        },
    )


def login_user(
    login_data: LoginRequest,
    db: Session,
    trace_id: str,
):
    identifier = login_data.identifier.strip()
    user = query_one(db, GET_LOGIN_USER, {"identifier": identifier})

    if not user or not verify_password(
        login_data.password,
        str(user["password_hash"]),
        str(user["password_algorithm"]),
    ):
        _raise_auth_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            business_code="ACCOUNT_INVALID_CREDENTIALS",
            message="Thông tin đăng nhập không chính xác",
            trace_id=trace_id,
        )

    if not bool(user["password_login_enabled"]):
        _raise_auth_error(
            status_code=status.HTTP_403_FORBIDDEN,
            business_code="ACCOUNT_PASSWORD_LOGIN_DISABLED",
            message="Đăng nhập bằng mật khẩu đã bị vô hiệu hóa",
            trace_id=trace_id,
        )

    locked_until = user.get("locked_until")
    if locked_until is not None:
        now = datetime.now(UTC)
        if locked_until.tzinfo is None:
            locked_until = locked_until.replace(tzinfo=UTC)
        if locked_until > now:
            _raise_auth_error(
                status_code=status.HTTP_423_LOCKED,
                business_code="ACCOUNT_TEMPORARILY_LOCKED",
                message="Tài khoản đang bị khóa tạm thời",
                trace_id=trace_id,
            )

    account_status = str(user["account_status"])
    if account_status == "SUSPENDED":
        _raise_auth_error(
            status_code=status.HTTP_403_FORBIDDEN,
            business_code="ACCOUNT_SUSPENDED",
            message="Tài khoản đã bị tạm ngừng",
            trace_id=trace_id,
        )

    user_id = str(user["id"])
    roles = _roles_for_user(db, user_id)

    db.execute(text(MARK_LOGIN_SUCCESS), {"user_id": user_id})
    db.commit()

    access_token = create_access_token(user_id=user_id, roles=roles)
    refresh_token = create_refresh_token(user_id=user_id)

    next_action = (
        "CHANGE_PASSWORD"
        if bool(user["must_change_password"])
        else _next_action(account_status)
    )

    return success_payload(
        business_code="ACCOUNT_LOGIN_SUCCEEDED",
        message="Đăng nhập thành công",
        trace_id=trace_id,
        data={
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "tokenType": "Bearer",
            "user": {
                "id": user_id,
                "displayName": user["display_name"],
                "accountStatus": account_status,
                "roles": roles,
            },
            "nextAction": next_action,
        },
    )


def refresh_access_token(
    refresh_data: RefreshTokenRequest,
    db: Session,
    trace_id: str,
):
    try:
        claims = decode_refresh_token(refresh_data.refresh_token)
    except TokenError:
        _raise_auth_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            business_code="AUTH_REFRESH_TOKEN_INVALID",
            message="Refresh token không hợp lệ hoặc đã hết hạn",
            trace_id=trace_id,
        )

    user_id = str(claims["sub"])
    user = query_one(db, GET_USER_BY_ID, {"user_id": user_id})
    if not user:
        _raise_auth_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            business_code="AUTH_USER_NOT_FOUND",
            message="Người dùng của token không còn tồn tại",
            trace_id=trace_id,
        )

    if str(user["account_status"]) == "SUSPENDED":
        _raise_auth_error(
            status_code=status.HTTP_403_FORBIDDEN,
            business_code="ACCOUNT_SUSPENDED",
            message="Tài khoản đã bị tạm ngừng",
            trace_id=trace_id,
        )

    roles = _roles_for_user(db, user_id)
    access_token = create_access_token(user_id=user_id, roles=roles)

    return success_payload(
        business_code="AUTH_ACCESS_TOKEN_REFRESHED",
        message="Cấp access token mới thành công",
        trace_id=trace_id,
        data={
            "accessToken": access_token,
            "tokenType": "Bearer",
        },
    )


def get_current_user(
    request: Request,
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> dict:
    trace_id = get_trace_id(request)

    if credentials is None or credentials.scheme.lower() != "bearer":
        _raise_auth_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            business_code="AUTH_TOKEN_REQUIRED",
            message="Thiếu Bearer access token",
            trace_id=trace_id,
        )

    try:
        claims = decode_access_token(credentials.credentials)
    except TokenError:
        _raise_auth_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            business_code="AUTH_ACCESS_TOKEN_INVALID",
            message="Access token không hợp lệ hoặc đã hết hạn",
            trace_id=trace_id,
        )

    user_id = str(claims["sub"])
    user = query_one(db, GET_USER_BY_ID, {"user_id": user_id})
    if not user:
        _raise_auth_error(
            status_code=status.HTTP_401_UNAUTHORIZED,
            business_code="AUTH_USER_NOT_FOUND",
            message="Người dùng của token không còn tồn tại",
            trace_id=trace_id,
        )

    if str(user["account_status"]) == "SUSPENDED":
        _raise_auth_error(
            status_code=status.HTTP_403_FORBIDDEN,
            business_code="ACCOUNT_SUSPENDED",
            message="Tài khoản đã bị tạm ngừng",
            trace_id=trace_id,
        )

    user["roles"] = _roles_for_user(db, user_id)
    return user
