"""Trace ID generation, validation and request-context access."""

from __future__ import annotations

from contextvars import ContextVar, Token
from uuid import UUID, uuid4

from fastapi import Request

TRACE_HEADER = "X-Trace-Id"
_trace_id_context: ContextVar[str | None] = ContextVar("trace_id", default=None)


def create_trace_id() -> str:
    """Create a new UUID trace identifier."""

    return str(uuid4())


def normalize_trace_id(value: str | None) -> str | None:
    """Return a canonical UUID string or ``None`` for an invalid value."""

    if not value:
        return None
    try:
        return str(UUID(value))
    except (ValueError, AttributeError):
        return None


def set_current_trace_id(trace_id: str) -> Token[str | None]:
    """Set the trace ID used by code that has no direct Request reference."""

    return _trace_id_context.set(trace_id)


def reset_current_trace_id(token: Token[str | None]) -> None:
    """Restore the previous trace context after a request finishes."""

    _trace_id_context.reset(token)


def get_current_trace_id() -> str | None:
    """Return the current context trace ID, if a request is active."""

    return _trace_id_context.get()


def get_trace_id(request: Request) -> str:
    """Return the request trace ID, creating one if middleware was bypassed."""

    trace_id = normalize_trace_id(getattr(request.state, "trace_id", None))
    if trace_id is None:
        trace_id = create_trace_id()
        request.state.trace_id = trace_id
    return trace_id
