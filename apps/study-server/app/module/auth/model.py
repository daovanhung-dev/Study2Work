from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    display_name: str
    email: str
    phone: str
    password: str


class LoginRequest(BaseModel):
    identifier: str = Field(min_length=1, max_length=320)
    password: str = Field(min_length=1, max_length=72)


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(min_length=1)
