# 08 — Auth, Trace, Response & Error Rules

## Password

Source hiện tại dùng bcrypt.

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

Không lưu plaintext password.

## JWT

Source `app(5).zip` chưa có JWT implementation hoàn chỉnh.

Khi triển khai JWT sau này, giữ các phần dùng chung trong `core/security.py` hoặc file security core chuyên biệt.

Không đặt encode/decode JWT riêng trong từng module.

Phân biệt:

```text
Access token -> xác thực API ngắn hạn
Refresh token -> cấp access token mới theo contract hệ thống
```

Không tự chọn TTL/claim/rotation policy nếu task/tài liệu chưa quy định.

## Trace ID

Hiện `validate.py` đang dùng literal:

```text
trace-123
```

Đây chỉ là placeholder hiện trạng, không phải design chuẩn.

Design chuẩn:

```text
incoming request
 ↓
read X-Trace-ID nếu policy cho phép hoặc generate UUID
 ↓
stored request context
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
  "traceId": "..."
}
```

Error target:

```json
{
  "success": false,
  "businessCode": "...",
  "message": "...",
  "errors": [
    {
      "field": "...",
      "code": "...",
      "message": "..."
    }
  ],
  "traceId": "..."
}
```

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

Log nội bộ có thể giữ exception context nhưng phải gắn trace ID và tránh secret.
