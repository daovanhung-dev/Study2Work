import pytest
from app.core import constants
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
