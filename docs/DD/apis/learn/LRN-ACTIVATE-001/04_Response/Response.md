# Response — LRN-ACTIVATE-001

## 1. Success response

HTTP `200 OK` cho read/update thành công; `201 Created` cho create; `202 Accepted` cho async job khi implementation áp dụng.

```json
{
  "success": true,
  "code": "LRN-ACTIVATE-SUCCESS",
  "message": "Thành công",
  "data": {
    "learnerPathId": "00000000-0000-4000-8000-000000000001",
    "status": "DRAFT",
    "activatedAt": "2026-07-05T12:00:00+07:00"
  },
  "traceId": "01JEXAMPLETRACEID"
}
```

## 2. Data contract

| Field | Type | Description |
| --- | --- | --- |
| learnerPathId | uuid | Giá trị trả về của contract |
| status | string | Giá trị trả về của contract |
| activatedAt | datetime | Giá trị trả về của contract |


## 3. Response guarantees

- `traceId` luôn có để truy vết.
- Timestamps theo ISO 8601 có timezone.
- Resource private được lọc theo scope và permission trước khi serialize.
- URL media/download (nếu có) là signed URL có hạn dùng, không phải URL storage gốc.
- `data` có thể có thêm field optional ở các version tương thích; client không dựa vào thứ tự field.
