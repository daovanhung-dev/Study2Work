# Request — EXE-SUBMIT-001

## 1. HTTP

| Item | Value |
| --- | --- |
| Method | `POST` |
| URL | `/api/v1/exercises/{exerciseId}/submissions` |
| Content-Type | `application/json` |
| Authorization | `Bearer JWT` |
| Idempotency | `Idempotency-Key` bắt buộc |

## 2. Path parameters

| Name | Type | Required | Rule |
| --- | --- | --- | --- |
| exerciseId | uuid / slug | Yes | Phải tồn tại và caller có quyền truy cập |


## 3. Query parameters

_Không có dữ liệu._


## 4. Body schema

| Field | Type | Required | Classification | Validation / Note |
| --- | --- | --- | --- | --- |
| attemptId | uuid | Yes | normal | Theo schema endpoint và rule nghiệp vụ |
| answers | array | Yes | PII | Theo schema endpoint và rule nghiệp vụ |
| submittedAt | datetime | No | normal | Theo schema endpoint và rule nghiệp vụ |


## 5. Body example

```json
{
  "attemptId": "00000000-0000-4000-8000-000000000001",
  "answers": [],
  "submittedAt": "2026-07-05T12:00:00+07:00"
}
```

## 6. Validation and security

- Chỉ chấp nhận JSON hợp lệ; field lạ phải bị bỏ qua có kiểm soát hoặc trả `VALIDATION_ERROR` theo implementation policy.
- Chuỗi phải trim, giới hạn độ dài, chống HTML/script injection và kiểm tra enum.
- Dữ liệu `PII`, `credential`, `audit`, `internal`, `external` không ghi nguyên văn vào application log.
- Backend tự lấy `actorId` từ token; client không được truyền quyền, điểm, completion hoặc trạng thái hệ thống tự quyết.
