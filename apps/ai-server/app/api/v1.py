from typing import Any
from app.module.chat.chat import chat_log_ai, ChatLogRequest
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/api/v1",
    tags=["api v1"],
)
@router.post("/chat_log_ai")
async def chat_log_ai_router(chat_log_request: ChatLogRequest) -> dict[str, Any]:
    return await chat_log_ai(chat_log_request=chat_log_request)
