from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.core.trace import TRACE_HEADER, create_trace_id


class TraceIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        incoming_trace_id = request.headers.get(TRACE_HEADER)
        request.state.trace_id = incoming_trace_id or create_trace_id()

        response = await call_next(request)
        response.headers[TRACE_HEADER] = request.state.trace_id
        return response
