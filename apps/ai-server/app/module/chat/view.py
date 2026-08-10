from app.service.ai.ollama_service import ai_service
from app.module.chat.model import ChatLogRequest

from typing import Any

async def chat_log_ai(
    chat_log_request: ChatLogRequest
) -> dict[str, Any]:

    result = await ai_service.generate(
        prompt=chat_log_request.prompt,
    )

    return {
        "response": result["answer"]
    }