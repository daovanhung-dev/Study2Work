from __future__ import annotations

import os
import logging
from typing import Any, Literal

import httpx

MessageRole = Literal["system", "user", "assistant"]
logger = logging.getLogger(__name__)


class AIConnectionError(Exception):
    """Không thể kết nối tới Ollama AI Server."""


class AITimeoutError(Exception):
    """Ollama xử lý quá thời gian cho phép."""


class AIResponseError(Exception):
    """Ollama trả về HTTP hoặc JSON không hợp lệ."""


class AIBusyError(Exception):
    """Không lấy được kết nối từ HTTP pool trong thời gian cho phép."""


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
        self._client: httpx.AsyncClient | None = None

    async def start(self) -> None:
        """Mở một client cho vòng đời của service."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                limits=httpx.Limits(max_connections=100),
                timeout=httpx.Timeout(self.timeout, pool=5.0),
            )

    async def close(self) -> None:
        """Đóng client khi caller đã dùng xong service."""
        if self._client is not None:
            client, self._client = self._client, None
            await client.aclose()

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

        if not isinstance(data.get("response"), str):
            raise AIResponseError("Ollama trả về response không hợp lệ.")

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

        message = data.get("message")
        if not isinstance(message, dict) or not isinstance(message.get("content"), str):
            raise AIResponseError("Ollama trả về message không hợp lệ.")

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

        if not isinstance(data.get("models"), list):
            raise AIResponseError("Ollama trả về models không hợp lệ.")

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
        if self._client is None:
            raise RuntimeError("OllamaService chưa start(); hãy gọi start() trước khi sử dụng.")

        try:
            response = await self._client.request(
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

        except httpx.PoolTimeout as exc:
            logger.warning("Ollama HTTP pool timeout")
            raise AIBusyError("AI server đang bận.") from exc

        except (httpx.ConnectTimeout, httpx.NetworkError) as exc:
            logger.warning("Ollama connection failure: %s", type(exc).__name__)
            raise AIConnectionError(
                "Không kết nối được tới Ollama.",
            ) from exc

        except httpx.TimeoutException as exc:
            logger.warning("Ollama request timeout: %s", type(exc).__name__)
            raise AITimeoutError(
                "Ollama phản hồi quá thời gian.",
            ) from exc

        except httpx.HTTPStatusError as exc:
            logger.warning("Ollama HTTP status: %s", exc.response.status_code)
            raise AIResponseError(
                "Ollama trả về HTTP không hợp lệ."
            ) from exc

        except (httpx.ProtocolError, httpx.DecodingError) as exc:
            logger.warning("Ollama response failure: %s", type(exc).__name__)
            raise AIResponseError("Ollama trả về phản hồi không hợp lệ.") from exc

        except ValueError as exc:
            logger.warning("Ollama returned invalid JSON")
            raise AIResponseError(
                "Ollama trả về JSON không hợp lệ.",
            ) from exc


ai_service = OllamaService()
