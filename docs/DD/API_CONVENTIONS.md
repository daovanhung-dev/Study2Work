# API Conventions

## Envelope thành công

```json
{
  "success": true,
  "code": "MODULE-ACTION-SUCCESS",
  "message": "Thành công",
  "data": {},
  "traceId": "01J..."
}
```

## Envelope lỗi

```json
{
  "success": false,
  "code": "VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ",
  "errors": [
    {
      "field": "email",
      "code": "INVALID_FORMAT",
      "message": "Email không hợp lệ"
    }
  ],
  "traceId": "01J..."
}
```

## Quy ước bắt buộc

- `Content-Type: application/json` cho request có body JSON.
- `Authorization: Bearer <accessToken>` cho endpoint private.
- `Idempotency-Key` bắt buộc cho nộp bài, gửi notification hoặc lệnh tạo có khả năng retry.
- Pagination: `page` bắt đầu từ 1, `pageSize` mặc định 20, tối đa 100.
- Optimistic concurrency: request chỉnh sửa admin dùng `version` khi API yêu cầu.
- Time: ISO 8601 kèm timezone, ví dụ `2026-07-05T12:00:00+07:00`.
- Không trả password hash, refresh token database record, secret hay URL storage gốc.
- Ảnh và tài liệu private dùng signed URL ngắn hạn.
