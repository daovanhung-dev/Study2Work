from __future__ import annotations

from typing import Any, Literal

import httpx
from starlette.responses import JSONResponse

from app.core import constants
from app.core.responses import ApiError

MessageRole = Literal["system", "user", "assistant"]


class OllamaService:
    """Đóng gói lời gọi HTTP bất đồng bộ tới Ollama cho các service hoặc API. Service dùng cấu hình
    mặc định khi không có override và trả JSONResponse an toàn khi upstream lỗi."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        timeout: float | None = None,
    ) -> None:
        """Khởi tạo client Ollama bằng giá trị override nếu được truyền, nếu không thì dùng hằng số
        mặc định. URL được bỏ dấu gạch chéo cuối để ghép endpoint chính xác; model và timeout
        được lưu để dùng ở các request sau."""
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
    ) -> dict[str, Any] | JSONResponse:
        """Gửi prompt cùng model, system tùy chọn và options tới endpoint /api/generate với stream
        tắt. Trả model, câu trả lời, trạng thái hoàn tất và payload upstream thô; lỗi được
        _request trả thành JSONResponse an toàn."""

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
        if isinstance(data, JSONResponse):
            return data

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
    ) -> dict[str, Any] | JSONResponse:
        """Gửi danh sách messages cùng model và options tùy chọn tới endpoint /api/chat với stream
        tắt. Trả model, role, nội dung câu trả lời, trạng thái hoàn tất và payload upstream thô."""

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
        if isinstance(data, JSONResponse):
            return data

        message = data.get("message") or {}

        return {
            "model": data.get("model", model or self.model),
            "role": message.get("role", "assistant"),
            "answer": message.get("content", ""),
            "done": data.get("done", False),
            "raw": data,
        }

    async def list_models(self) -> list[str] | JSONResponse:
        """Gọi endpoint /api/tags rồi lấy tên từ các phần tử model hợp lệ. Trả danh sách tên model;
        lỗi kết nối hoặc response được xử lý bởi _request."""

        data = await self._request(
            method="GET",
            endpoint="/api/tags",
        )
        if isinstance(data, JSONResponse):
            return data

        return [
            item["name"]
            for item in data.get("models", [])
            if isinstance(item, dict) and item.get("name")
        ]

    async def health_check(self) -> dict[str, Any] | JSONResponse:
        """Gọi list_models để xác nhận Ollama phản hồi, sau đó trả trạng thái available cùng URL,
        model mặc định và danh sách model hiện có."""

        models = await self.list_models()
        if isinstance(models, JSONResponse):
            return models

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
    ) -> dict[str, Any] | JSONResponse:
        """Gửi request HTTP bất đồng bộ tới endpoint tương đối của Ollama bằng timeout đã cấu hình,
        kiểm tra status và giải mã JSON object. Lỗi kết nối, timeout, HTTP, JSON hoặc response
        sai dạng được chuyển thành JSONResponse an toàn qua ApiError()."""
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
                return ApiError()

            return data

        except httpx.ConnectError:
            return ApiError()

        except httpx.TimeoutException:
            return ApiError()

        except httpx.HTTPStatusError:
            return ApiError()

        except ValueError:
            return ApiError()

        except Exception:
            return ApiError()


ai_service = OllamaService()
