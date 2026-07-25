from sqlalchemy import text 

from fastapi import APIRouter
from app.core.database import engine

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