from __future__ import annotations

# import folder's files
from app.modules.guest.api_03_auth_login.validate import (
    normalize_login_email,
    validate_login_password,
    validate_refresh_token,
)

# import framework
from pydantic import BaseModel, EmailStr, Field, field_validator


class LoginRequest(BaseModel):
    """Public request body for authenticating a Study account."""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=1)

    _normalize_email = field_validator("email", mode="before")(normalize_login_email)
    _validate_password = field_validator("password", mode="before")(validate_login_password)


class RefreshRequest(BaseModel):
    """Public request body for rotating a refresh token."""

    refresh_token: str = Field(min_length=1)

    _validate_refresh_token = field_validator("refresh_token", mode="before")(
        validate_refresh_token
    )
