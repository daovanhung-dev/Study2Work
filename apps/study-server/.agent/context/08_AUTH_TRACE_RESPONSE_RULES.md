# 08 — Auth, Trace, Response & Error Rules

## Password

Source hiện tại dùng Argon2id cho hash mới và chỉ verify bcrypt legacy.

Flow đăng ký:

```text
plaintext password
 ↓
hash_password()
 ↓
password_hash
 ↓
auth_credentials
```

Không lưu plaintext password hoặc password hash trong response/log.

## JWT

`core/security.py` tập trung JWT signing/verification, issuer/audience/type
validation và interface key provider cho static key hoặc JWKS adapter.

Phân biệt:

```text
Access token -> xác thực API ngắn hạn
Refresh token -> opaque token, chỉ lưu hash ở Identity
```

Persistence, rotation và reuse detection của refresh token thuộc Identity;
Study server chỉ cung cấp primitive và legacy adapter, không tự tạo schema.

## Trace ID

Design chuẩn:

```text
incoming request
 ↓
validate X-Trace-Id hoặc generate UUID
 ↓
request state + context
 ↓
all logs/errors/responses reuse same traceId
```

## Response

Không trả mỗi endpoint một shape tùy ý.

Success target:

```json
{
  "success": true,
  "businessCode": "...",
  "message": "...",
  "data": {},
  "meta": {},
  "traceId": "uuid"
}
```

Canonical error target:

```json
{
  "success": false,
  "businessCode": "...",
  "message": "...",
  "data": null,
  "meta": {"fieldErrors": []},
  "traceId": "uuid"
}
```

`error_payload()` vẫn có adapter `errors` ở top-level cho caller cũ.

## HTTP status vs business code

Không trộn hai khái niệm:

- HTTP status mô tả kết quả HTTP/protocol.
- businessCode mô tả lỗi/trạng thái nghiệp vụ của S2W.

## Error handling

Không expose:

- exception repr trực tiếp.
- raw PostgreSQL detail.
- password/token.
- stack trace.

Log nội bộ có thể giữ exception context nhưng phải gắn trace ID và tránh
secret.
