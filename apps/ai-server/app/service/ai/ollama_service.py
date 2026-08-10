from __future__ import annotations

import os
from typing import Any, Literal

import httpx

MessageRole = Literal["system", "user", "assistant"]


class AIConnectionError(Exception):
    """Không thể kết nối tới Ollama AI Server."""


class AITimeoutError(Exception):
    """Ollama xử lý quá thời gian cho phép."""


class AIResponseError(Exception):
    """Ollama trả về HTTP hoặc JSON không hợp lệ."""


class OllamaService:
    """Đối tượng dùng chung để gọi Ollama từ service, use case hoặc API."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        configured_base_url = (
            base_url
            or os.getenv(
                "OLLAMA_BASE_URL",
                "http://127.0.0.1:11434",
            )
            or "http://127.0.0.1:11434"
        )
        self.base_url = configured_base_url.rstrip("/")

        self.model = model or os.getenv(
            "OLLAMA_MODEL",
            "qwen2.5-coder:1.5b",
        )

        self.timeout = timeout if timeout is not None else float(os.getenv("OLLAMA_TIMEOUT", "180"))

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
                raise AIResponseError(
                    "Ollama trả về JSON không đúng định dạng object.",
                )

            return data

        except httpx.ConnectError as exc:
            raise AIConnectionError(
                f"Không kết nối được tới Ollama tại {self.base_url}.",
            ) from exc

        except httpx.TimeoutException as exc:
            raise AITimeoutError(
                f"Ollama không phản hồi trong {self.timeout} giây.",
            ) from exc

        except httpx.HTTPStatusError as exc:
            raise AIResponseError(
                f"Ollama trả về HTTP {exc.response.status_code}: {exc.response.text}"
            ) from exc

        except ValueError as exc:
            raise AIResponseError(
                "Ollama trả về JSON không hợp lệ.",
            ) from exc


ai_service = OllamaService()
