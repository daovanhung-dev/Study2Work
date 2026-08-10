"""Synchronous SQLAlchemy setup and small, request-scoped query helpers."""

from __future__ import annotations

from collections.abc import Generator, Mapping
from functools import lru_cache
from typing import Any

from sqlalchemy import URL, Engine, create_engine, text
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import Settings, get_settings


def build_database_url(config: Settings) -> URL:
    """Build a PostgreSQL URL without exposing or mis-escaping credentials."""

    return URL.create(
        drivername="postgresql+psycopg",
        username=config.db_user,
        password=config.db_password.get_secret_value(),
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
    )


def build_engine(config: Settings) -> Engine:
    """Create an engine for the supplied application settings."""

    return create_engine(
        build_database_url(config),
        pool_pre_ping=True,
        pool_size=config.database_pool_size,
        max_overflow=config.database_max_overflow,
        connect_args={
            "options": f"-csearch_path={config.db_schema},public",
        },
    )


def build_session_factory(database_engine: Engine) -> sessionmaker[Session]:
    """Create the factory used to open one Session per request."""

    return sessionmaker(
        bind=database_engine,
        autoflush=False,
        expire_on_commit=False,
        class_=Session,
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Return the lazily-created process engine for the default settings."""

    return build_engine(get_settings())


@lru_cache(maxsize=1)
def get_session_factory() -> sessionmaker[Session]:
    """Return the lazily-created process session factory."""

    return build_session_factory(get_engine())


def SessionLocal() -> Session:
    """Compatibility wrapper for legacy callers; returns a new Session."""

    return get_session_factory()()


def get_db_from_factory(
    session_factory: sessionmaker[Session],
) -> Generator[Session, None, None]:
    """Yield one request-scoped session and always close it afterwards."""

    db = session_factory()
    try:
        yield db
    finally:
        db.close()


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that uses the lazily-created default factory."""

    yield from get_db_from_factory(get_session_factory())


def execute_query(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> Result[Any]:
    """Execute parameterized SQL inside the caller-owned transaction."""

    return db.execute(text(query), dict(params or {}))


def query_one(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> dict[str, Any] | None:
    """Execute a query and return the first row as a plain dictionary."""

    row = execute_query(db, query, params).mappings().first()
    return dict(row) if row is not None else None


def query_many(
    db: Session,
    query: str,
    params: Mapping[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Execute a query and return all rows as plain dictionaries."""

    rows = execute_query(db, query, params).mappings().all()
    return [dict(row) for row in rows]
