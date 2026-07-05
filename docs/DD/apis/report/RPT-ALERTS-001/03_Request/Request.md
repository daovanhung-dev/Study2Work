# Request — RPT-ALERTS-001

## 1. HTTP

| Item | Value |
| --- | --- |
| Method | `GET` |
| URL | `/api/v1/admin/reports/alerts` |
| Content-Type | `application/json` (không có body) |
| Authorization | `Bearer JWT` |
| Idempotency | `Idempotency-Key` khuyến nghị cho client retry khi có mutation |

## 2. Path parameters

_Không có dữ liệu._


## 3. Query parameters

| Name | Type | Required | Rule |
| --- | --- | --- | --- |
| page | integer | No | Default 1; min 1 |
| pageSize | integer | No | Default 20; max 100 |
| from | datetime | No | Start inclusive |
| to | datetime | No | End inclusive |


## 4. Body schema

_Không có dữ liệu._


## 5. Body example

```json
{}
```

## 6. Validation and security

- Chỉ chấp nhận JSON hợp lệ; field lạ phải bị bỏ qua có kiểm soát hoặc trả `VALIDATION_ERROR` theo implementation policy.
- Chuỗi phải trim, giới hạn độ dài, chống HTML/script injection và kiểm tra enum.
- Dữ liệu `PII`, `credential`, `audit`, `internal`, `external` không ghi nguyên văn vào application log.
- Backend tự lấy `actorId` từ token; client không được truyền quyền, điểm, completion hoặc trạng thái hệ thống tự quyết.
