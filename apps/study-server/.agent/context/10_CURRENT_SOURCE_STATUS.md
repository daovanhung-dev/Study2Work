# 10 — Current Source Status

## Snapshot

Source đã được tối ưu theo core plan ngày 2026-08-08. Source hiện tại là
baseline ưu tiên khi context cũ khác với code.

## File có implementation đáng kể

- `app/main.py`
- `app/api/v1.py`
- `app/core/config.py`
- `app/core/database.py`
- `app/core/responses.py`
- `app/core/security.py`
- `app/module/auth/model.py`
- `app/module/auth/query.py`
- `app/module/auth/validate.py`
- `app/module/ai/log/view.py`
- `app/service/ai/ollama_service.py`

## File còn để dành cho module sau

```text
app/module/public/model.py
app/module/public/query.py
app/module/public/validate.py
app/module/public/view.py
app/module/ai/log/model.py
app/module/ai/log/validate.py
```

Các file `core/exceptions.py`, `core/middleware.py`, `core/trace.py` và
`module/auth/view.py` hiện đã có implementation.

## Endpoint hiện khai báo

```text
GET  /api/v1/hello
GET  /api/v1/test/db
POST /api/v1/register
POST /api/v1/chat_log_ai
GET  /
```

## Runtime baseline

`app.main` export cả `app` và `create_app(settings)`. Health routes, trace
middleware, validation error handler và database factory có thể chạy mà không
cần mở kết nối PostgreSQL trong lúc import.

## DB lifecycle issue

`database.py` giữ request-scoped `get_db()` và các lazy default factory. Không
dùng global shared Session cho HTTP concurrency.

## Trace status

Trace middleware đọc/validate `X-Trace-Id`, tạo UUID khi thiếu/sai và gắn
cùng giá trị vào request state, response header và response body.

## JWT status

`security.py` dùng Argon2id cho hash mới, verify bcrypt legacy, JWT ES256 với
issuer/audience validation, interface key provider và opaque refresh-token
helpers. Persistence/rotation refresh vẫn thuộc Identity và chưa nằm trong
Study server.

## Response status

`responses.py` có canonical factories:

1. `success_response()` / `error_response()`.
2. Compatibility adapters `success_payload()` / `error_payload()` và `ApiResponse`.

Code mới không tạo thêm response shape thứ ba.

## Quality baseline

Ruff, mypy và pytest hiện chạy pass trong `.venv`. Test suite bao phủ config,
trace, health, response, DB URL/query helpers, Argon2id/bcrypt legacy, JWT và
opaque refresh token.

## Nguyên tắc khi dùng file này

Đây là factual snapshot của source tại thời điểm tạo context. Nếu source thay đổi, agent phải ưu tiên source mới và cập nhật context khi cần.
