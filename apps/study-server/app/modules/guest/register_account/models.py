from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.validate import strip_email,reject_blank_password


class RegisterRequest(BaseModel):
    """Public request body for creating a Study account."""

    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=1)
    full_name: str = Field(min_length=1, max_length=150)

    _strip_email = field_validator("email", mode="before")(strip_email)
    _reject_blank_password_ = field_validator("password", mode="before")(reject_blank_password)

    @field_validator("full_name", mode="before")
    @classmethod
    def strip_full_name(cls, value: object) -> object:
        if isinstance(value, str):
            return value.strip()
        return value
