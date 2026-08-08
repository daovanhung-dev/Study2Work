# 10 — Current Source Status

## Snapshot

Nguồn dùng để xây context: `app(5).zip`, đọc ngày 2026-08-08.

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

## File hiện rỗng

```text
app/core/exceptions.py
app/core/middleware.py
app/core/trace.py
app/module/auth/view.py
app/module/public/model.py
app/module/public/query.py
app/module/public/validate.py
app/module/public/view.py
app/module/ai/log/model.py
app/module/ai/log/validate.py
```

## Endpoint hiện khai báo

```text
GET  /api/v1/hello
GET  /api/v1/test/db
POST /api/v1/register
POST /api/v1/chat_log_ai
GET  /
```

## Blocking runtime issue hiện có

`api/v1.py` import:

```python
from app.module.auth.view import create_user
```

nhưng `app/module/auth/view.py` đang rỗng.

Do đó source snapshot này không phải implementation hoàn chỉnh cho `/register`.

## DB lifecycle issue

`database.py` đồng thời có request-scoped `get_db()` và global `db = SessionLocal()`.

Develop target của context này: giữ request-scoped Session, không dùng global shared Session cho HTTP concurrency.

## Trace status

`trace.py` rỗng và auth validation đang hard-code `trace_id="trace-123"`.

Đây là gap implementation.

## JWT status

`security.py` hiện chỉ có bcrypt hash/verify. Chưa có JWT code trong snapshot.

## Response status

`responses.py` hiện có hai hướng song song:

1. function `success_payload()` / `error_payload()`.
2. class `ApiResponse` có `success_payload()` / `raise_error()`.

Agent không nên tạo thêm hướng thứ ba. Khi task refactor response, nên thống nhất một canonical API.

## AI defect

`OllamaService.chat()` tham chiếu identifier không tồn tại `optionsclear`.

## Nguyên tắc khi dùng file này

Đây là factual snapshot của source tại thời điểm tạo context. Nếu source thay đổi, agent phải ưu tiên source mới và cập nhật context khi cần.
