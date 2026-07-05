# Request — SUP-ADMIN-RESOLVE-001

## 1. HTTP

| Item | Value |
| --- | --- |
| Method | `POST` |
| URL | `/api/v1/admin/support-requests/{requestId}/resolve` |
| Content-Type | `application/json` |
| Authorization | `Bearer JWT` |
| Idempotency | `Idempotency-Key` khuyến nghị cho client retry khi có mutation |

## 2. Path parameters

| Name | Type | Required | Rule |
| --- | --- | --- | --- |
| requestId | uuid / slug | Yes | Phải tồn tại và caller có quyền truy cập |


## 3. Query parameters

_Không có dữ liệu._


## 4. Body schema

| Field | Type | Required | Classification | Validation / Note |
| --- | --- | --- | --- | --- |
| resolution | string | Yes | PII | Theo schema endpoint và rule nghiệp vụ |
| resolutionCode | string | Yes | normal | Theo schema endpoint và rule nghiệp vụ |
| reason | string | Yes | audit | Theo schema endpoint và rule nghiệp vụ |


## 5. Body example

```json
{
  "resolution": "example",
  "resolutionCode": "example",
  "reason": "Nghiệp vụ đã được kiểm tra"
}
```

## 6. Validation and security

- Chỉ chấp nhận JSON hợp lệ; field lạ phải bị bỏ qua có kiểm soát hoặc trả `VALIDATION_ERROR` theo implementation policy.
- Chuỗi phải trim, giới hạn độ dài, chống HTML/script injection và kiểm tra enum.
- Dữ liệu `PII`, `credential`, `audit`, `internal`, `external` không ghi nguyên văn vào application log.
- Backend tự lấy `actorId` từ token; client không được truyền quyền, điểm, completion hoặc trạng thái hệ thống tự quyết.
