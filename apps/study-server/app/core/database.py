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
    connect_args={
        "options": f"-csearch_path={settings.DB_SCHEMA},public",
    },
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


def query_one(
    db: Session,
    query: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Execute a query using the request-scoped session and return one row."""
    result = db.execute(text(query), params or {})
    row = result.mappings().first()
    return dict(row) if row is not None else None


def query_many(
    db: Session,
    query: str,
    params: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute a query using the request-scoped session and return all rows."""
    result = db.execute(text(query), params or {})
    rows = result.mappings().all()
    return [dict(row) for row in rows]
