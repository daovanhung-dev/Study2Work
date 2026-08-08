from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse

from app.core.trace import get_trace_id


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
) -> JSONResponse:
    if isinstance(exc.detail, dict) and "success" in exc.detail:
        content = exc.detail
    else:
        content = {
            "success": False,
            "businessCode": "HTTP_ERROR",
            "message": str(exc.detail),
            "traceId": get_trace_id(request),
        }

    return JSONResponse(
        status_code=exc.status_code,
        content=content,
        headers=exc.headers,
    )
