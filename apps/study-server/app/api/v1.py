from sqlalchemy import text
from sqlalchemy.orm import Session

from fastapi import APIRouter, Depends

from app.core.database import engine, get_db
from app.module.auth.model import RegisterRequest
from app.module.auth.view import create_user
from app.module.ai.log.view import chat_log_ai

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
    db: Session = Depends(get_db),
):
    return create_user(
        user_data=user_data,
        db=db,
    )


@router.post("/chat_log_ai")
async def chat_log_ai_router(prompt: str):
    return await chat_log_ai(prompt=prompt)
