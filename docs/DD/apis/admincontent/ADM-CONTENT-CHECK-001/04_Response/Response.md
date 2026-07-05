# Response — ADM-CONTENT-CHECK-001

## 1. Success response

HTTP `200 OK` cho read/update thành công; `201 Created` cho create; `202 Accepted` cho async job khi implementation áp dụng.

```json
{
  "success": true,
  "code": "ADM-CONTENT-CHECK-SUCCESS",
  "message": "Thành công",
  "data": {
    "passed": true,
    "checks": [],
    "blockingIssues": []
  },
  "traceId": "01JEXAMPLETRACEID"
}
```

## 2. Data contract

| Field | Type | Description |
| --- | --- | --- |
| passed | boolean | Giá trị trả về của contract |
| checks | array | Giá trị trả về của contract |
| blockingIssues | array | Giá trị trả về của contract |


## 3. Response guarantees

- `traceId` luôn có để truy vết.
- Timestamps theo ISO 8601 có timezone.
- Resource private được lọc theo scope và permission trước khi serialize.
- URL media/download (nếu có) là signed URL có hạn dùng, không phải URL storage gốc.
- `data` có thể có thêm field optional ở các version tương thích; client không dựa vào thứ tự field.
