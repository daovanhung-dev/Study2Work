from __future__ import annotations

from typing import Any, Literal

import httpx

from app.core import constants
from app.core.responses import ApiError, _ApiError

MessageRole = Literal["system", "user", "assistant"]


class OllamaService:
    """Đối tượng dùng chung để gọi Ollama từ service, use case hoặc API."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        configured_base_url = base_url or constants.OLLAMA_BASE_URL
        self.base_url = configured_base_url.rstrip("/")

        self.model = model or constants.OLLAMA_MODEL

        self.timeout = timeout if timeout is not None else constants.OLLAMA_TIMEOUT

    async def generate(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Gửi một prompt tới endpoint /api/generate."""

        payload: dict[str, Any] = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": False,
        }

        if system:
            payload["system"] = system

        if options:
            payload["options"] = options

        data = await self._request(
            method="POST",
            endpoint="/api/generate",
            json=payload,
        )

        return {
            "model": data.get("model", model or self.model),
            "answer": data.get("response", ""),
            "done": data.get("done", False),
            "raw": data,
        }

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        model: str | None = None,
        options: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Gửi danh sách messages tới endpoint /api/chat."""

        payload: dict[str, Any] = {
            "model": model or self.model,
            "messages": messages,
            "stream": False,
        }

        if options:
            payload["options"] = options

        data = await self._request(
            method="POST",
            endpoint="/api/chat",
            json=payload,
        )

        message = data.get("message") or {}

        return {
            "model": data.get("model", model or self.model),
            "role": message.get("role", "assistant"),
            "answer": message.get("content", ""),
            "done": data.get("done", False),
            "raw": data,
        }

    async def list_models(self) -> list[str]:
        """Lấy danh sách model đang có trên Ollama Server."""

        data = await self._request(
            method="GET",
            endpoint="/api/tags",
        )

        return [
            item["name"]
            for item in data.get("models", [])
            if isinstance(item, dict) and item.get("name")
        ]

    async def health_check(self) -> dict[str, Any]:
        """Kiểm tra kết nối và trả về danh sách model."""

        models = await self.list_models()

        return {
            "available": True,
            "base_url": self.base_url,
            "default_model": self.model,
            "models": models,
        }

    async def _request(
        self,
        *,
        method: str,
        endpoint: str,
        json: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(
                timeout=self.timeout,
            ) as client:
                response = await client.request(
                    method=method,
                    url=f"{self.base_url}{endpoint}",
                    json=json,
                )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):
                raise ApiError()

            return data

        except httpx.ConnectError as exc:
            raise ApiError() from exc

        except httpx.TimeoutException as exc:
            raise ApiError() from exc

        except httpx.HTTPStatusError as exc:
            raise ApiError() from exc

        except ValueError as exc:
            raise ApiError() from exc

        except _ApiError:
            raise

        except Exception as exc:
            raise ApiError() from exc


ai_service = OllamaService()
