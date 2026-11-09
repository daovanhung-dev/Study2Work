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

`prompt` phải là chuỗi, không rỗng hoặc toàn khoảng trắng, tối đa 8.000 ký tự.
Nội dung hợp lệ được chuyển nguyên văn; lỗi đầu vào trả FastAPI HTTP 422.

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
- `app/main.py` ánh xạ lỗi pool sang 503 `AI_BUSY`, kết nối sang 503 `OLLAMA_UNAVAILABLE`, timeout sang 504 `OLLAMA_TIMEOUT`, HTTP/JSON/response Ollama sai sang 502 `OLLAMA_BAD_RESPONSE`. JSON lỗi là `{error:{code,message}}`, không chứa nội dung thô từ Ollama.
- No declared business code, trace ID or standard API envelope.

Do not copy Study's declared `/chat_log_ai` semantics: Study route takes a plain `prompt` parameter and points to a missing log module; these are different implementations.
