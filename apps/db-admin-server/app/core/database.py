"""SQLAlchemy engine and request-scoped connection helpers."""

from __future__ import annotations

from collections.abc import Iterator
from functools import lru_cache

from fastapi import Depends, Request
from sqlalchemy import Connection, Engine, create_engine, text
from sqlalchemy.engine import make_url

from app.core.config import Settings, get_settings


def build_engine(settings: Settings) -> Engine:
    url = make_url(settings.database_url.get_secret_value())
    if url.drivername == "postgresql":
        url = url.set(drivername="postgresql+psycopg")
    return create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        future=True,
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    return build_engine(get_settings())


def get_connection(request: Request) -> Iterator[Connection]:
    resources = getattr(request.app.state, "resources", None)
    if resources is None:
        from app.core.config import get_settings
        from app.core.runtime import build_resources

        resources = build_resources(get_settings())
        request.app.state.resources = resources
    with resources.engine.connect() as connection:
        yield connection


def configure_transaction_limits(connection: Connection, settings: Settings) -> None:
    """Apply bounded execution limits inside the current transaction."""

    connection.execute(
        text("SELECT set_config('statement_timeout', :timeout_value, true)"),
        {"timeout_value": f"{settings.statement_timeout_ms}ms"},
    )
    connection.execute(
        text("SELECT set_config('lock_timeout', :timeout_value, true)"),
        {"timeout_value": f"{settings.lock_timeout_ms}ms"},
    )


DbConnection = Depends(get_connection)
