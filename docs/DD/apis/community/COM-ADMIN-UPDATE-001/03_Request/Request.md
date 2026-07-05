# Request — COM-ADMIN-UPDATE-001

## 1. HTTP

| Item | Value |
| --- | --- |
| Method | `PATCH` |
| URL | `/api/v1/admin/community-groups/{groupId}` |
| Content-Type | `application/json` |
| Authorization | `Bearer JWT` |
| Idempotency | `Idempotency-Key` khuyến nghị cho client retry khi có mutation |

## 2. Path parameters

| Name | Type | Required | Rule |
| --- | --- | --- | --- |
| groupId | uuid / slug | Yes | Phải tồn tại và caller có quyền truy cập |


## 3. Query parameters

_Không có dữ liệu._


## 4. Body schema

| Field | Type | Required | Classification | Validation / Note |
| --- | --- | --- | --- | --- |
| name | string | No | normal | Theo schema endpoint và rule nghiệp vụ |
| description | string | No | normal | Theo schema endpoint và rule nghiệp vụ |
| externalUrl | string | No | external | Theo schema endpoint và rule nghiệp vụ |
| scopeType | string | No | normal | Theo schema endpoint và rule nghiệp vụ |
| scopeId | uuid | No | normal | Theo schema endpoint và rule nghiệp vụ |
| status | string | No | normal | Theo schema endpoint và rule nghiệp vụ |
| reason | string | Yes | audit | Theo schema endpoint và rule nghiệp vụ |


## 5. Body example

```json
{
  "name": "example",
  "description": "example",
  "externalUrl": "example",
  "scopeType": "example",
  "scopeId": "00000000-0000-4000-8000-000000000001",
  "status": "DRAFT",
  "reason": "Nghiệp vụ đã được kiểm tra"
}
```

## 6. Validation and security

- Chỉ chấp nhận JSON hợp lệ; field lạ phải bị bỏ qua có kiểm soát hoặc trả `VALIDATION_ERROR` theo implementation policy.
- Chuỗi phải trim, giới hạn độ dài, chống HTML/script injection và kiểm tra enum.
- Dữ liệu `PII`, `credential`, `audit`, `internal`, `external` không ghi nguyên văn vào application log.
- Backend tự lấy `actorId` từ token; client không được truyền quyền, điểm, completion hoặc trạng thái hệ thống tự quyết.
