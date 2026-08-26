# AI chat module

## `model.py:ChatLogRequest`
Pydantic model with one required field:

```text
prompt: str
```

No explicit min/max length/content validator exists.

## `chat.py`
Re-exports `ChatLogRequest` and `chat_log_ai`; contains no orchestration itself.

## `view.py:chat_log_ai(chat_log_request)`
- async function.
- Calls singleton `ai_service.generate(prompt=chat_log_request.prompt)`.
- Reads returned `result["answer"]`.
- Returns `{"response": answer}`.
- No DB write/logging, auth, business code, trace ID or standard envelope.
- Ollama adapter exceptions are not caught here.

## `query.py`
`EMPTY_PLACEHOLDER` (zero-byte at snapshot).

## `validate.py`
`EMPTY_PLACEHOLDER` (zero-byte at snapshot).

Do not claim chat history persistence or validation layer exists.
