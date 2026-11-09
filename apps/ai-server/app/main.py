from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.v1 import router
from app.service.ai import (
    AIBusyError,
    AIConnectionError,
    AIResponseError,
    AITimeoutError,
    ai_service,
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await ai_service.start()
    try:
        yield
    finally:
        await ai_service.close()


app = FastAPI(lifespan=lifespan)


def _error_response(code: str, message: str, status: int) -> JSONResponse:
    return JSONResponse(status_code=status, content={"error": {"code": code, "message": message}})


@app.exception_handler(AIBusyError)
async def busy_handler(request: Request, exc: AIBusyError) -> JSONResponse:
    logger.warning("AI client pool is busy")
    return _error_response("AI_BUSY", "Dịch vụ AI đang bận, vui lòng thử lại", 503)


@app.exception_handler(AIConnectionError)
async def connection_handler(request: Request, exc: AIConnectionError) -> JSONResponse:
    logger.warning("Ollama is unavailable")
    return _error_response("OLLAMA_UNAVAILABLE", "Dịch vụ AI tạm thời không khả dụng", 503)


@app.exception_handler(AITimeoutError)
async def timeout_handler(request: Request, exc: AITimeoutError) -> JSONResponse:
    logger.warning("Ollama request timed out")
    return _error_response("OLLAMA_TIMEOUT", "Dịch vụ AI phản hồi quá lâu", 504)


@app.exception_handler(AIResponseError)
async def response_handler(request: Request, exc: AIResponseError) -> JSONResponse:
    logger.warning("Ollama returned an invalid response")
    return _error_response("OLLAMA_BAD_RESPONSE", "Dịch vụ AI trả về phản hồi không hợp lệ", 502)


@app.get("/")
def root():
    return {
        "message": "Wellcome to AI server"
    }

app.include_router(router)
