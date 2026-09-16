"""SQLAlchemy engine and request-scoped connection helpers."""

from __future__ import annotations

from collections.abc import Iterator
from functools import lru_cache

from fastapi import Depends, Request
from sqlalchemy import Connection, Engine, create_engine, text
from sqlalchemy.engine import make_url

from app.core.config import Settings, get_settings
from app.core.responses import ApiError
from app.core.trace import get_trace_id
from app.services.identifiers import quote_identifier


def build_engine(settings: Settings) -> Engine:
    if settings.database_url is None:
        raise ValueError("A database URL is required to build an engine")
    url = make_url(settings.database_url.get_secret_value())
    if url.drivername == "postgresql":
        url = url.set(drivername="postgresql+psycopg")
    # Neon pooler URLs may include ``pgbouncer=true`` for clients that use it
    # as a connection hint. It is not a libpq/psycopg connection option, so
    # remove it before handing the URL to SQLAlchemy.
    if "pgbouncer" in url.query:
        url = url.set(query={key: value for key, value in url.query.items() if key != "pgbouncer"})
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


def get_connection(request: Request, database: str | None = None) -> Iterator[Connection]:
    resources = getattr(request.app.state, "resources", None)
    if resources is None:
        from app.core.config import get_settings
        from app.core.runtime import build_resources

        resources = build_resources(get_settings())
        request.app.state.resources = resources
    engine = resources.engine_for(database, get_trace_id(request)) if database else resources.engine
    with engine.connect() as connection:
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


def ensure_schema_exists(connection: Connection, schema_name: str, trace_id: str) -> None:
    schema = connection.execute(
        text("SELECT 1 FROM information_schema.schemata WHERE schema_name = :schema_name"),
        {"schema_name": schema_name},
    ).scalar_one_or_none()
    if schema is None:
        raise ApiError(
            status_code=422,
            business_code="DB_ADMIN_SCHEMA_NOT_FOUND",
            message="The selected schema does not exist in this database.",
            trace_id=trace_id,
        )


def configure_search_path(connection: Connection, schema_name: str, trace_id: str) -> None:
    search_path = quote_identifier(schema_name, "schema", trace_id)
    connection.execute(
        text("SELECT set_config('search_path', :search_path, true)"),
        {"search_path": search_path},
    )


DbConnection = Depends(get_connection)
