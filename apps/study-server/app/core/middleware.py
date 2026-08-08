"""HTTP middleware for cross-cutting request concerns."""

from __future__ import annotations

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.exceptions import unhandled_exception_handler
from app.core.trace import (
    TRACE_HEADER,
    create_trace_id,
    normalize_trace_id,
    reset_current_trace_id,
    set_current_trace_id,
)


class TraceIdMiddleware(BaseHTTPMiddleware):
    """Propagate one valid trace ID through the complete request lifecycle."""

    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        trace_id = normalize_trace_id(request.headers.get(TRACE_HEADER)) or create_trace_id()
        request.state.trace_id = trace_id
        context_token = set_current_trace_id(trace_id)

        try:
            response = await call_next(request)
            response.headers[TRACE_HEADER] = trace_id
            return response
        except Exception as exc:
            response = await unhandled_exception_handler(request, exc)
            response.headers[TRACE_HEADER] = trace_id
            return response
        finally:
            reset_current_trace_id(context_token)
