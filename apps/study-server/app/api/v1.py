from fastapi import APIRouter, Depends, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import engine, get_db
from app.core.trace import get_trace_id
from app.module.ai.log.view import chat_log_ai
from app.module.auth.model import LoginRequest, RefreshTokenRequest, RegisterRequest
from app.module.auth.view import (
    create_user,
    get_current_user,
    login_user,
    refresh_access_token,
)

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)


@router.get("/hello")
def hello_world():
    return {"message": "hello world!"}


@router.get("/test/db")
def test_db():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT NOW()"))
        return {"result": [row[0] for row in result]}


@router.post("/register")
def register(
    user_data: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    return create_user(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/login")
def login(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    return login_user(
        login_data=login_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/refresh")
def refresh_token(
    refresh_data: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db),
):
    return refresh_access_token(
        refresh_data=refresh_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.get("/auth/me")
def me(
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    return {
        "success": True,
        "businessCode": "AUTH_CURRENT_USER_FOUND",
        "message": "Lấy thông tin người dùng thành công",
        "data": current_user,
        "meta": {},
        "traceId": get_trace_id(request),
    }


@router.post("/chat_log_ai")
async def chat_log_ai_router(prompt: str):
    return await chat_log_ai(prompt=prompt)
