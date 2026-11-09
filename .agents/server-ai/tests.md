# AI tests

```text
TEST_STATUS: VERIFIED_MOCK_TESTS
```

`apps/ai-server/tests/test_ollama_service.py` and `test_chat_api.py` run with
`& .venv/Scripts/python.exe -m unittest discover -s tests -v` from `apps/ai-server`.
They cover lifecycle, concurrent reuse, prompt boundaries, error mapping and
the existing success JSON using HTTPX mock transport. They do not measure live
Ollama throughput or deployment latency.

For an AI coding task, validation should at minimum target the exact changed layer:
- model validation for request changes;
- service tests mocking `httpx`/Ollama for adapter changes;
- FastAPI route tests for API behavior;
- explicit error mapping tests if custom handlers are introduced.

Do not claim runtime health solely because source imports look simple; Ollama availability is an external condition.
