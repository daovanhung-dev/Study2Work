# AI tests

```text
TEST_STATUS: NOT_FOUND
```

No AI-server test directory/files are present at tracked source snapshot.

For an AI coding task, validation should at minimum target the exact changed layer:
- model validation for request changes;
- service tests mocking `httpx`/Ollama for adapter changes;
- FastAPI route tests for API behavior;
- explicit error mapping tests if custom handlers are introduced.

Do not claim runtime health solely because source imports look simple; Ollama availability is an external condition.
