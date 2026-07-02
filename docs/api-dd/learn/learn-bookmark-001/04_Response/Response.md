# Response - LEARN-BOOKMARK-001

## Response Matrix

| Scenario | HTTP | Business code | Data/errors | Client behavior |
|---|---:|---|---|---|
| Success | `200` | `LEARN-BOOKMARK-001-SUCCESS` | `data` | Cập nhật UI/cache theo payload và traceId. |
| Validation failed | `422` | `LEARN-BOOKMARK-001-INVALID_INPUT` | `errors[]` | Hiển thị field error an toàn. |
| Unauthorized | `401` | `AUTH-RESP-UNAUTHORIZED` | `errors[]` | Yêu cầu login lại hoặc refresh token. |
| Forbidden | `403` | `LEARN-BOOKMARK-001-FORBIDDEN` | `errors[]` | Ẩn hoặc khóa hành động không đủ quyền. |
| Not found | `404` | `LEARN-BOOKMARK-001-NOT_FOUND` | `errors[]` | Hiển thị trạng thái không tìm thấy. |
| Conflict | `409` | `LEARN-BOOKMARK-001-CONFLICT` | `errors[]` | Refresh dữ liệu hoặc xử lý state conflict. |
| Dependency unavailable | `502/503/504` | `LEARN-BOOKMARK-001-DEPENDENCY_UNAVAILABLE` | `errors[]` | Retry chỉ với thao tác an toàn/idempotent. |
| Internal error | `500` | `SYSTEM-RESP-INTERNAL_ERROR` | `errors[]` | Hiển thị thông báo hỗ trợ an toàn. |

## Success Envelope

```json
{
  "businessCode": "LEARN-BOOKMARK-001-SUCCESS",
  "message": "Xử lý thành công API LEARN-BOOKMARK-001.",
  "timestamp": "2026-07-02T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "data": {
    "id": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
    "status": "example"
  }
}
```

## Error Envelope

```json
{
  "businessCode": "LEARN-BOOKMARK-001-INVALID_INPUT",
  "message": "Dữ liệu yêu cầu không hợp lệ.",
  "timestamp": "2026-07-02T10:00:00Z",
  "traceId": "7c3a2f1b-31c5-4a21-9b3e-7d1745c4748a",
  "errors": [
    {
      "field": "request",
      "code": "E422",
      "message": "Kiểm tra lại dữ liệu đầu vào."
    }
  ]
}
```

## Data Fields

| Field | Type | Required | Nullable | Source | Sensitive | Note |
|---|---|---:|---:|---|---:|---|
| `id` | `UUID/string` | Y | N | bookmark | Y/N theo resource | ID resource chính khi có. |
| `status` | `string` | N | Y | bookmark | N | Trạng thái sau xử lý hoặc projection status. |
| `items` | `array` | N | Y | read model | N | Chỉ dùng cho list endpoint. |

## Pagination

- Bắt buộc với list endpoint.
- Không áp dụng với single-resource hoặc mutation endpoint trừ khi response data có `items`.

```json
{
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 0,
    "totalPages": 0
  }
}
```
