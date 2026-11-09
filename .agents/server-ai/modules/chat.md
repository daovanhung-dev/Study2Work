# AI chat module

## `model.py:ChatLogRequest`
Pydantic model with one required field:

```text
prompt: str (strict, tối đa 8.000 ký tự; không rỗng/toàn khoảng trắng)
```

Validator chỉ dùng `strip()` để kiểm tra rỗng, không thay đổi prompt hợp lệ.

## `chat.py`
Re-exports `ChatLogRequest` and `chat_log_ai`; contains no orchestration itself.

## `view.py:chat_log_ai(chat_log_request)`
- async function.
- Calls singleton `ai_service.generate(prompt=chat_log_request.prompt)`.
- Reads returned `result["answer"]`.
- Returns `{"response": answer}`.
- No DB write/logging, auth, business code, trace ID or standard envelope.
- Ollama adapter exceptions are mapped by handlers in `app/main.py`, not by the view.

## `query.py`
`EMPTY_PLACEHOLDER` (zero-byte at snapshot).

## `validate.py`
`EMPTY_PLACEHOLDER` (zero-byte at snapshot).

Do not claim chat history persistence or validation layer exists.
