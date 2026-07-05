# Response — SUP-DETAIL-001

## 1. Success response

HTTP `200 OK` cho read/update thành công; `201 Created` cho create; `202 Accepted` cho async job khi implementation áp dụng.

```json
{
  "success": true,
  "code": "SUP-DETAIL-SUCCESS",
  "message": "Thành công",
  "data": {
    "request": {},
    "comments": [],
    "statusHistory": []
  },
  "traceId": "01JEXAMPLETRACEID"
}
```

## 2. Data contract

| Field | Type | Description |
| --- | --- | --- |
| request | object | Giá trị trả về của contract |
| comments | array | Giá trị trả về của contract |
| statusHistory | array | Giá trị trả về của contract |


## 3. Response guarantees

- `traceId` luôn có để truy vết.
- Timestamps theo ISO 8601 có timezone.
- Resource private được lọc theo scope và permission trước khi serialize.
- URL media/download (nếu có) là signed URL có hạn dùng, không phải URL storage gốc.
- `data` có thể có thêm field optional ở các version tương thích; client không dựa vào thứ tự field.
