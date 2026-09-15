from typing import Any

from fastapi import APIRouter, Depends, Request, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db, get_engine
from app.core.trace import get_trace_id
from app.modules.auth.models import RegisterRequest
from app.modules.auth.view import create_user

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
