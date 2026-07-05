# Error — SUP-ADMIN-LIST-001

## 1. Error envelope

```json
{
  "success": false,
  "code": "DOMAIN_RULE_VIOLATION",
  "message": "Thao tác không hợp lệ theo trạng thái hiện tại",
  "errors": [
    {
      "field": "pathId",
      "code": "ACTIVE_PATH_EXISTS",
      "message": "Learner đã có một lộ trình ACTIVE"
    }
  ],
  "traceId": "01JEXAMPLETRACEID"
}
```

## 2. Error matrix

| HTTP | Code | When |
| --- | --- | --- |
| 400 | VALIDATION_ERROR | Body, path hoặc query không đúng schema |
| 401 | UNAUTHENTICATED | Thiếu, hết hạn hoặc không hợp lệ token |
| 403 | FORBIDDEN | Caller không có role/permission hoặc không thuộc scope |
| 404 | RESOURCE_NOT_FOUND | Resource không tồn tại hoặc bị che theo quyền |
| 422 | DOMAIN_RULE_VIOLATION | Mọi quyết định ngoại lệ phải có lý do, người duyệt và audit trail; support agent chỉ truy cập dữ liệu trong phạm vi được cấp. |
| 429 | RATE_LIMITED | Vượt ngưỡng gọi API |
| 500 | INTERNAL_ERROR | Lỗi không mong muốn; dùng traceId để tra cứu |


## 3. Client handling

- `400/422`: hiển thị lỗi field hoặc nghiệp vụ, không retry tự động.
- `401`: refresh token một lần; nếu thất bại thì đăng xuất.
- `403`: ẩn hành động không có quyền; không cố gọi lại.
- `404`: hiển thị trạng thái không tìm thấy, không suy diễn resource có tồn tại hay không.
- `409`: tải lại dữ liệu hiện tại và yêu cầu người dùng xác nhận lại.
- `429/5xx`: retry có exponential backoff nếu endpoint idempotent; gửi `traceId` khi báo lỗi.
