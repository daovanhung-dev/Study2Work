from app.service.ai import ai_service


async def chat_log_ai(prompt: str) -> dict[str, str]:
    result = await ai_service.generate(
        prompt=prompt,
    )

    return {
        "result": result,
    }
