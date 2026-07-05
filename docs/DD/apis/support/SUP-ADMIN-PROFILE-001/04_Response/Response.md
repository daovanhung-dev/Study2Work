# Response — SUP-ADMIN-PROFILE-001

## 1. Success response

HTTP `200 OK` cho read/update thành công; `201 Created` cho create; `202 Accepted` cho async job khi implementation áp dụng.

```json
{
  "success": true,
  "code": "SUP-ADMIN-PROFILE-SUCCESS",
  "message": "Thành công",
  "data": {
    "learner": {},
    "activePath": {},
    "progress": {},
    "flags": [],
    "exceptions": []
  },
  "traceId": "01JEXAMPLETRACEID"
}
```

## 2. Data contract

| Field | Type | Description |
| --- | --- | --- |
| learner | object | Giá trị trả về của contract |
| activePath | object | Giá trị trả về của contract |
| progress | object | Giá trị trả về của contract |
| flags | array | Giá trị trả về của contract |
| exceptions | array | Giá trị trả về của contract |


## 3. Response guarantees

- `traceId` luôn có để truy vết.
- Timestamps theo ISO 8601 có timezone.
- Resource private được lọc theo scope và permission trước khi serialize.
- URL media/download (nếu có) là signed URL có hạn dùng, không phải URL storage gốc.
- `data` có thể có thêm field optional ở các version tương thích; client không dựa vào thứ tự field.
