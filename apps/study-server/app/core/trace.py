"""Trace ID helpers."""

from contextvars import ContextVar, Token
from uuid import UUID, uuid4

from fastapi import Request


TRACE_HEADER = "X-Trace-Id"

_current_trace_id: ContextVar[str | None] = ContextVar(
    "current_trace_id",
    default=None,
)


def create_trace_id() -> str:
    """Create a new trace ID."""

    return str(uuid4())


def validate_trace_id(trace_id: str | None) -> str | None:
    """Return a valid UUID trace ID, otherwise None."""

    if not trace_id:
        return None

    try:
        return str(UUID(trace_id))
    except ValueError:
        return None


def get_trace_id(request: Request) -> str:
    """Get the trace ID of the current request."""

    trace_id = getattr(
        request.state,
        "trace_id",
        None,
    )

    trace_id = validate_trace_id(trace_id)

    if trace_id is None:
        trace_id = create_trace_id()
        request.state.trace_id = trace_id

    return trace_id


def set_trace_id(trace_id: str) -> Token:
    """Store the trace ID in the current execution context."""

    return _current_trace_id.set(trace_id)


def get_current_trace_id() -> str | None:
    """Get the trace ID without needing Request."""

    return _current_trace_id.get()


def reset_trace_id(token: Token) -> None:
    """Restore the previous trace context."""

    _current_trace_id.reset(token)