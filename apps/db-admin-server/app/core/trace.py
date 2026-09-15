"""Request trace ID middleware."""

from __future__ import annotations

from uuid import UUID, uuid4

from fastapi import Request

TRACE_HEADER = "X-Trace-Id"


def get_trace_id(request: Request) -> str:
    value = getattr(request.state, "trace_id", None)
    if isinstance(value, str) and value:
        return value
    trace_id = str(uuid4())
    request.state.trace_id = trace_id
    return trace_id


def normalize_trace_id(value: str | None) -> str:
    if value:
        try:
            return str(UUID(value))
        except ValueError:
            pass
    return str(uuid4())
