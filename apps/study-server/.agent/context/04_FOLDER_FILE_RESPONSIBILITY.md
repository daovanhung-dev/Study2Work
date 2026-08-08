# 04 — Folder & File Responsibility

## `app/main.py`

### Chịu trách nhiệm

- Tạo `FastAPI()`.
- Đăng ký router.
- Đăng ký middleware/exception handler khi core đã triển khai.
- Startup/shutdown hook nếu cần.

### Không chịu trách nhiệm

- Business logic.
- SQL.
- Validation nghiệp vụ.

---

## `app/api/`

### Chịu trách nhiệm

- HTTP method/path.
- Dependency injection.
- Binding Pydantic request.
- Gọi module view.

### Pattern

```python
@router.post("/resource")
def endpoint(
    payload: RequestModel,
    db: Session = Depends(get_db),
):
    return module_view(
        payload=payload,
        db=db,
    )
```

---

## `app/module/<feature>/model.py`

### Chịu trách nhiệm

- Pydantic request model.
- Pydantic response/data model khi cần.
- Enum/value object gắn trực tiếp với contract của module khi phù hợp.

### Không chịu trách nhiệm

- Query DB.
- HTTP orchestration.
- Hashing.

---

## `app/module/<feature>/validate.py`

### Chịu trách nhiệm

- Required.
- Length.
- Format.
- Range.
- Enum.
- Validation thuần không phụ thuộc infrastructure nếu có thể.

Business validation cần DB nên orchestration từ `view.py`.

---

## `app/module/<feature>/query.py`

### Chịu trách nhiệm

- SQL constant.
- Query text theo module.

### Quy tắc

- Dùng named parameter `:param`.
- Không nối raw user input vào SQL string.
- Không trả HTTP response.
- Không commit.

---

## `app/module/<feature>/view.py`

### Chịu trách nhiệm

- Business use-case flow.
- Gọi validate.
- Gọi query.
- Gọi security/service helper.
- Commit/rollback ở đúng boundary.
- Map response.

Đây là file developer tập trung nhiều nhất khi implement API.

---

## `app/core/config.py`

### Chịu trách nhiệm

- Typed environment settings.
- Config dùng chung.

Không hard-code secret trong source.

---

## `app/core/database.py`

### Chịu trách nhiệm

- SQLAlchemy engine.
- Session factory.
- `get_db()` dependency.
- DB primitives dùng chung nếu thiết kế thống nhất theo request-scoped Session.

Không dùng global mutable Session cho concurrent HTTP requests.

---

## `app/core/security.py`

### Hiện có

- bcrypt hash.
- bcrypt verify.

### Kiến trúc mục tiêu

Có thể mở rộng JWT/access token/refresh token khi task yêu cầu, nhưng phải giữ logic security tập trung ở core.

---

## `app/core/responses.py`

Chịu trách nhiệm response envelope thống nhất.

Contract đang xuất hiện trong source:

```json
{
  "success": true,
  "businessCode": "...",
  "message": "...",
  "data": {},
  "meta": {},
  "traceId": "..."
}
```

Error contract đang xuất hiện:

```json
{
  "success": false,
  "businessCode": "...",
  "message": "...",
  "errors": [],
  "traceId": "..."
}
```

Cần thống nhất một cơ chế response thay vì duy trì nhiều API tương đương lâu dài.

---

## `app/core/trace.py`

Mục tiêu:

- Generate trace ID.
- Get current trace ID.
- Không chứa business rule.

Hiện file đang rỗng.

---

## `app/core/middleware.py`

Mục tiêu:

- Trace middleware.
- Cross-cutting request/response concerns.

Hiện file đang rỗng.

---

## `app/core/exceptions.py`

Mục tiêu:

- Shared exception classes.
- Global exception mapping/handler khi thiết kế yêu cầu.

Hiện file đang rỗng.

---

## `app/service/`

Chịu trách nhiệm external integrations:

- AI.
- Email.
- Storage.
- Third-party APIs.

Service phải expose interface đơn giản để module gọi, che đi transport/protocol cụ thể.
