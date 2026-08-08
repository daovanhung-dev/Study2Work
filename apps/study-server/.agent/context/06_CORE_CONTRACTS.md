# 06 — Core Contracts

## Config contract

`core/config.py` hiện yêu cầu:

```text
DB_HOST
DB_PORT
DB_NAME
DB_USER
DB_PASSWORD
DB_SCHEMA
```

Agent không hard-code các giá trị này vào module.

## Database contract mục tiêu

Một request nhận `Session` bằng:

```python
db: Session = Depends(get_db)
```

Business view nhận `db` qua parameter.

DB helper nếu được dùng phải nhận `Session` hoặc hoạt động trong request-scoped lifecycle; không dựa vào global Session.

## Security contract hiện có

```text
hash_password(password) -> str
verify_password(password, hashed_password) -> bool
```

Password plaintext không được log hoặc đưa vào response.

## Response contract hiện có

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

## Response design rule

Agent phải tránh tạo thêm response shape mới cho từng API.

Nếu source đã có canonical response utility sau này, dùng utility đó thay vì tự dựng dict.

## Trace contract mục tiêu

Một trace ID phải:

- Có một giá trị cho toàn request.
- Có trong response.
- Có trong log liên quan request đó.
- Được truyền vào error response.
- Không hard-code.

## Exception contract mục tiêu

Business/validation errors phải được map sang contract có kiểm soát.

System error không expose:

- stack trace.
- raw SQL.
- DB credential.
- token.
- internal service secret.
