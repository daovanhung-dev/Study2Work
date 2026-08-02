from typing import Any, Generator

from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings


DATABASE_URL = (
    f"postgresql+psycopg://"
    f"{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# Khởi tạo Session trước
db = SessionLocal()


def query_one(
    query: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """
    Thực thi truy vấn và trả về một bản ghi.
    """
    result = db.execute(
        text(query),
        params or {},
    )

    row = result.mappings().first()

    return dict(row) if row is not None else None


def query_many(
    query: str,
    params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """
    Thực thi truy vấn và trả về nhiều bản ghi.
    """
    result = db.execute(
        text(query),
        params or {},
    )

    rows = result.mappings().all()

    return [dict(row) for row in rows]


def close_db() -> None:
    """
    Đóng Session khi ứng dụng kết thúc.
    """
    db.close()