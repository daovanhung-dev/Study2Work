# Request — PRG-LESSON-UPDATE-001

## 1. HTTP

| Item | Value |
| --- | --- |
| Method | `PATCH` |
| URL | `/api/v1/lessons/{lessonId}/progress` |
| Content-Type | `application/json` |
| Authorization | `Bearer JWT; endpoint internal dùng service token` |
| Idempotency | `Idempotency-Key` khuyến nghị cho client retry khi có mutation |

## 2. Path parameters

| Name | Type | Required | Rule |
| --- | --- | --- | --- |
| lessonId | uuid / slug | Yes | Phải tồn tại và caller có quyền truy cập |


## 3. Query parameters

_Không có dữ liệu._


## 4. Body schema

| Field | Type | Required | Classification | Validation / Note |
| --- | --- | --- | --- | --- |
| eventType | string | Yes | normal | Theo schema endpoint và rule nghiệp vụ |
| positionSeconds | integer | No | normal | Theo schema endpoint và rule nghiệp vụ |
| durationSeconds | integer | No | normal | Theo schema endpoint và rule nghiệp vụ |
| clientEventId | string | Yes | normal | Theo schema endpoint và rule nghiệp vụ |
| occurredAt | datetime | No | normal | Theo schema endpoint và rule nghiệp vụ |


## 5. Body example

```json
{
  "eventType": "example",
  "positionSeconds": 1,
  "durationSeconds": 1,
  "clientEventId": "00000000-0000-4000-8000-000000000001",
  "occurredAt": "2026-07-05T12:00:00+07:00"
}
```

## 6. Validation and security

- Chỉ chấp nhận JSON hợp lệ; field lạ phải bị bỏ qua có kiểm soát hoặc trả `VALIDATION_ERROR` theo implementation policy.
- Chuỗi phải trim, giới hạn độ dài, chống HTML/script injection và kiểm tra enum.
- Dữ liệu `PII`, `credential`, `audit`, `internal`, `external` không ghi nguyên văn vào application log.
- Backend tự lấy `actorId` từ token; client không được truyền quyền, điểm, completion hoặc trạng thái hệ thống tự quyết.
