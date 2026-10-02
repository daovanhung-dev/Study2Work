import httpx
import pytest
from app.core import constants
from app.service.ai import ollama_service
from app.service.ai.ollama_service import OllamaService
from starlette.responses import JSONResponse


def test_ollama_defaults_ignore_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """Kiểm tra OllamaService dùng constants mặc định thay vì tự đọc biến môi trường."""
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://environment-host:9999")
    monkeypatch.setenv("OLLAMA_MODEL", "environment-model")
    monkeypatch.setenv("OLLAMA_TIMEOUT", "1")

    service = OllamaService()

    assert service.base_url == constants.OLLAMA_BASE_URL
    assert service.model == constants.OLLAMA_MODEL
    assert service.timeout == constants.OLLAMA_TIMEOUT


def test_ollama_constructor_overrides_are_preserved() -> None:
    """Kiểm tra URL, model và timeout truyền vào constructor được giữ làm cấu hình service."""
    service = OllamaService(
        base_url="http://custom-host:11434/",
        model="custom-model",
        timeout=30,
    )

    assert service.base_url == "http://custom-host:11434"
    assert service.model == "custom-model"
    assert service.timeout == 30


@pytest.mark.asyncio
async def test_ollama_connection_failure_uses_safe_api_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Kiểm tra ConnectError từ upstream Ollama được chuyển thành ApiError an toàn."""
    class FailingClient:
        async def __aenter__(self):
            """Trả client giả khi mở async context để mô phỏng request Ollama."""
            return self

        async def __aexit__(self, *args):
            """Kết thúc context client giả mà không nuốt exception."""
            return None

        async def request(self, **kwargs):
            """Phát sinh ConnectError giả để kiểm tra chuyển lỗi kết nối upstream thành ApiError."""
            raise httpx.ConnectError("private upstream address")

    monkeypatch.setattr(ollama_service.httpx, "AsyncClient", lambda **kwargs: FailingClient())

    error = await OllamaService()._request(method="GET", endpoint="/api/tags")

    assert isinstance(error, JSONResponse)
    assert error.status_code == 500
    assert b"INTERNAL_SERVER_ERROR" in error.body
    assert b"private upstream address" not in error.body
