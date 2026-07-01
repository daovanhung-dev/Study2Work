from __future__ import annotations

import logging
import time
from collections.abc import Awaitable, Callable
from uuid import UUID, uuid4

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger("study2work.api")


def _valid_or_new_trace_id(header_value: str | None) -> str:
    if header_value:
        try:
            return str(UUID(header_value))
        except ValueError:
            logger.warning("SYSTEM-TRACE-WARNING invalid upstream trace id")
    return str(uuid4())


class TraceMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        trace_id = _valid_or_new_trace_id(request.headers.get("X-Trace-Id"))
        request.state.trace_id = trace_id
        start = time.perf_counter()

        response = await call_next(request)
        response.headers["X-Trace-Id"] = trace_id
        response.headers["X-Process-Time-Ms"] = f"{(time.perf_counter() - start) * 1000:.2f}"
        return response
