# Request — ONB-DRAFT-001

## 1. HTTP

| Item | Value |
| --- | --- |
| Method | `PATCH` |
| URL | `/api/v1/onboarding/draft` |
| Content-Type | `application/json` |
| Authorization | `Bearer JWT` |
| Idempotency | `Idempotency-Key` khuyến nghị cho client retry khi có mutation |

## 2. Path parameters

_Không có dữ liệu._


## 3. Query parameters

_Không có dữ liệu._


## 4. Body schema

| Field | Type | Required | Classification | Validation / Note |
| --- | --- | --- | --- | --- |
| step | string | Yes | normal | Theo schema endpoint và rule nghiệp vụ |
| answers | object | Yes | PII | Theo schema endpoint và rule nghiệp vụ |


## 5. Body example

```json
{
  "step": "example",
  "answers": {}
}
```

## 6. Validation and security

- Chỉ chấp nhận JSON hợp lệ; field lạ phải bị bỏ qua có kiểm soát hoặc trả `VALIDATION_ERROR` theo implementation policy.
- Chuỗi phải trim, giới hạn độ dài, chống HTML/script injection và kiểm tra enum.
- Dữ liệu `PII`, `credential`, `audit`, `internal`, `external` không ghi nguyên văn vào application log.
- Backend tự lấy `actorId` từ token; client không được truyền quyền, điểm, completion hoặc trạng thái hệ thống tự quyết.
