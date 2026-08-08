# 06 — Core Contracts

## Config contract

`core/config.py` dùng field Python dạng `snake_case` và nhận các alias
environment hiện tại. Production settings gồm tối thiểu:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
DB_SCHEMA
```

JWT configuration phải cung cấp ES256 public key; HS256 chỉ là compatibility
mode và yêu cầu secret. Settings được load lazy qua:

```python
settings = get_settings()
```

Agent không hard-code các giá trị này vào module.

## Database contract mục tiêu

Một request nhận `Session` bằng:

```python
db: Session = Depends(get_db)
```

Business view nhận `db` qua parameter.

DB helper nếu được dùng phải nhận `Session` hoặc hoạt động trong request-scoped
lifecycle; không dựa vào global Session. `build_engine()` và
`build_session_factory()` là các factory công khai cho test/runtime.

## Security contract

```text
hash_password(password) -> str
verify_password(password, hashed_password) -> bool
needs_password_rehash(hash, algorithm) -> bool
generate_refresh_token() -> str
hash_refresh_token(token) -> str
```

Password mới dùng Argon2id. Bcrypt chỉ là legacy verify path. Refresh token
mới là opaque; core không sở hữu persistence/rotation session của Identity.
Password plaintext không được log hoặc đưa vào response.

## Response contract

Success:

```text
success
businessCode
message
data
meta
traceId
```

Validation/error utility hiện có `ErrorDetail` với:

```text
field
code
message
```

API mới dùng `success_response()` và `error_response()`. Field errors canonical
nằm trong `meta.fieldErrors`; `error_payload()` vẫn giữ top-level `errors` cho
caller cũ.

## Response design rule

Agent phải tránh tạo thêm response shape mới cho từng API.

Nếu source đã có canonical response utility sau này, dùng utility đó thay vì tự dựng dict.

## Trace contract

Một trace ID phải:

- Có một giá trị cho toàn request.
- Có trong response.
- Có trong log liên quan request đó.
- Được truyền vào error response.
- Không hard-code.
- Header chuẩn là `X-Trace-Id`; giá trị không phải UUID sẽ được thay mới.

## Exception contract mục tiêu

Business/validation errors phải được map sang contract có kiểm soát.

System error không expose:

- stack trace.
- raw SQL.
- DB credential.
- token.
- internal service secret.
