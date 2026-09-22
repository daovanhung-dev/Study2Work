from typing import Any

# import framework
from fastapi import APIRouter, Depends, Header, Request, status
from sqlalchemy import text
from sqlalchemy.orm import Session

# import core's file
from app.core.database import get_db, get_engine
from app.core.trace import get_trace_id

# import folder's files
from app.modules.guest.auth_login.models import LoginRequest, RefreshRequest
from app.modules.guest.auth_login.view import login, refresh
from app.modules.guest.register_account.models import RegisterRequest
from app.modules.guest.register_account.view import create_user
from app.modules.guest.users_me.view import get_current_user

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)
db_dependency = Depends(get_db)


@router.get("/hello")
def hello_world() -> dict[str, str]:
    return {"message": "hello world!"}


@router.get("/test/db")
def test_db() -> dict[str, list[Any]]:
    with get_engine().connect() as connection:
        result = connection.execute(text("SELECT NOW()"))
        return {"result": [row[0] for row in result]}


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: RegisterRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return create_user(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/login", status_code=status.HTTP_200_OK)
def authenticate(
    user_data: LoginRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return login(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.post("/auth/refresh", status_code=status.HTTP_200_OK)
def refresh_access_token(
    user_data: RefreshRequest,
    request: Request,
    db: Session = db_dependency,
) -> dict[str, Any]:
    return refresh(
        user_data=user_data,
        db=db,
        trace_id=get_trace_id(request),
    )


@router.get("/users/me", status_code=status.HTTP_200_OK)
def current_user(
    request: Request,
    authorization: str | None = Header(default=None, alias="Authorization"),
    db: Session = db_dependency,
) -> dict[str, Any]:
    return get_current_user(
        authorization=authorization,
        db=db,
        trace_id=get_trace_id(request),
    )
