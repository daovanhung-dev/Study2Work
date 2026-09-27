import httpx
import pytest
from app.core import constants
from app.core.responses import ApiError
from app.service.ai import ollama_service
from app.service.ai.ollama_service import OllamaService


def test_ollama_defaults_ignore_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OLLAMA_BASE_URL", "http://environment-host:9999")
    monkeypatch.setenv("OLLAMA_MODEL", "environment-model")
    monkeypatch.setenv("OLLAMA_TIMEOUT", "1")

    service = OllamaService()

    assert service.base_url == constants.OLLAMA_BASE_URL
    assert service.model == constants.OLLAMA_MODEL
    assert service.timeout == constants.OLLAMA_TIMEOUT


def test_ollama_constructor_overrides_are_preserved() -> None:
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
    class FailingClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def request(self, **kwargs):
            raise httpx.ConnectError("private upstream address")

    monkeypatch.setattr(ollama_service.httpx, "AsyncClient", lambda **kwargs: FailingClient())

    with pytest.raises(ApiError) as error:
        await OllamaService()._request(method="GET", endpoint="/api/tags")

    assert error.value.status_code == 500
    assert error.value.business_code == "INTERNAL_SERVER_ERROR"
    assert error.value.message == "Đã xảy ra lỗi nội bộ hệ thống."
    assert "private upstream address" not in error.value.message
