from __future__ import annotations

from pydantic import BaseModel, EmailStr, StrictInt


class VerifyEmailSendRequest(BaseModel):
    """Public request body for accepting a verification-email dispatch."""

    user_id: StrictInt
    email: EmailStr
