# AI API surface

## `GET /`
Source: `app/main.py:root`.
Returns raw JSON `{message: "Wellcome to AI server"}`. No envelope/trace/auth.

## `POST /api/v1/chat_log_ai`

Status: `VERIFIED` from current source wiring (subject to Ollama availability).

### Input
JSON body validated by Pydantic `ChatLogRequest`:

```json
{"prompt":"..."}
```

Only type/required-field validation is explicit; no custom length/content rules.

### Flow

```text
FastAPI validation
-> chat_log_ai_router
-> chat_log_ai(ChatLogRequest)
-> ai_service.generate(prompt)
-> Ollama POST /api/generate
-> result["answer"]
```

### Success output
Raw JSON:

```json
{"response":"<ollama answer>"}
```

### Errors
- FastAPI/Pydantic handles malformed request body with default validation response.
- Ollama connection/timeout/response errors are custom Python exceptions from service, but current view/main do not catch/map them.
- No declared business code, custom HTTP mapping, trace ID or standard API envelope.

Do not copy Study's declared `/chat_log_ai` semantics: Study route takes a plain `prompt` parameter and points to a missing log module; these are different implementations.
