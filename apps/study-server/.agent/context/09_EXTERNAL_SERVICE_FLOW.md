# 09 — External Service Flow

## Pattern

Module gọi interface service; service xử lý transport.

```text
API Router
 ↓
module/.../view.py
 ↓
service/<name>/
 ↓
external system
```

## AI hiện tại

```text
POST /api/v1/chat_log_ai
 ↓
module/ai/log/view.py
 ↓
service/ai/ai_service.generate()
 ↓
Ollama /api/generate
```

## `service/ai/` chịu trách nhiệm

- Base URL.
- Model mặc định.
- Timeout.
- `httpx` request.
- Parse response.
- Mapping lỗi connection/timeout/HTTP/JSON.

## Module không nên chịu trách nhiệm

- Tự tạo `httpx.AsyncClient` cho Ollama.
- Hard-code Ollama URL.
- Parse raw Ollama response ở router.

## Service exception hiện có

```text
AIConnectionError
AITimeoutError
AIResponseError
```

Module/core exception layer có thể map chúng thành response hệ thống theo contract khi được triển khai.

## Async rule

Nếu service method là async, call chain phải await đúng cách.

Router hiện có async cho `/chat_log_ai`, đây là phù hợp với `ai_service.generate()` async.

## Known source defect

Trong `OllamaService.chat()` hiện có:

```python
payload["options"] = optionsclear
```

`optionsclear` không được định nghĩa. Đây là bug source hiện tại; giá trị có chủ đích nhiều khả năng là `options`, nhưng agent chỉ sửa khi task liên quan hoặc người dùng yêu cầu sửa source.
