---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | `integer` | No | N/A | N/A | 6.1 | Fixed by successful create branch | N/A | HTTP 201 per API #16 contract |
| 2 | `success` | Success flag | `success` | `boolean` | No | N/A | N/A | 6.1 | true on success | N/A | ApiEnvelope field |
| 3 | `businessCode` | Business code | `businessCode` | `string` | No | N/A | N/A | 6.1 | `DESIGN_RESOURCE_CREATED` | N/A | Design-only code from API catalog |
| 4 | `message` | Response message | `message` | `string` | No | N/A | N/A | 6.1 | Application message | SOURCE_REQUIRED | Message text/catalog not defined for API #16 |
| 5 | `data` | Order | `data` | `Order` | No | Logical Order | N/A | 5.1 | Object mapping per Order schema | Required on success | Physical mapping SOURCE_REQUIRED |
| 5.1 | `data.id` | Order ID | `id` | `int64` | No | Logical Order | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Physical key/generator not defined |
| 5.2 | `data.course_id` | Course ID | `course_id` | `int64` | No | Logical Order | SOURCE_REQUIRED | 5.1 | Association to requested course | Required | Contract relation is clear; persisted column is not |
| 5.3 | `data.user_id` | Student ID | `user_id` | `int64` | No | Logical Order | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Exact JWT identity mapping and physical column not defined |
| 5.4 | `data.amount` | Order amount | `amount` | `decimal-string` | No | Logical Order | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Amount source/calculation and currency association unresolved |
| 5.5 | `data.currency` | Currency | `currency` | `string` | No | Logical Order | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Currency source/value not defined |
| 5.6 | `data.status` | Order status | `status` | `OrderStatus` | No | Logical Order | SOURCE_REQUIRED | 5.1 | Initial value `PENDING` per AC-12 | Required | Other enum values and physical representation not defined |
| 5.7 | `data.created_at` | Creation time | `created_at` | `date-time` | No | Logical Order | SOURCE_REQUIRED | 5.1 | ISO-8601 per API convention | Required | Clock/DB source and precision not defined |
| 6 | `meta` | Metadata | `meta` | `object` | No | N/A | N/A | 6.1 | Envelope object | Object shape not defined | ApiEnvelope schema |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | No | N/A | N/A | 6.1 | Trace context | Required by ApiEnvelope schema | Runtime value generation is not specified for API #16 |

## Ví dụ thành công

Các giá trị mẫu chỉ minh họa kiểu và shape. `<MESSAGE>` và `<SOURCE_REQUIRED>` là placeholder, không phải giá trị response literal; ví dụ không xác nhận currency, ID generation, storage mapping hoặc Order enum ngoài trạng thái ban đầu `PENDING`.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "<MESSAGE>",
  "data": {
    "id": 0,
    "course_id": 123,
    "user_id": 0,
    "amount": "0",
    "currency": "<SOURCE_REQUIRED>",
    "status": "PENDING",
    "created_at": "1970-01-01T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000016"
}
```

## Ví dụ lỗi

Ví dụ dùng lỗi validation đã khai báo trong catalog; `message` là placeholder vì message catalog chưa có nguồn. `data: {}` và `meta: {}` theo default hiện tại của [responses.py](../../../app/core/responses.py); đây là current convention, chưa phải runtime proof cho API #16.

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "<MESSAGE>",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000016"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md.
- Sheet logic: 2.Response.

