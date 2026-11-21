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
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 6.1 | Fixed by accepted branch | N/A | HTTP 202 per API #17 contract |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 6.1 | ApiEnvelope field | Required by shared envelope schema | Contract schema only |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 6.1 | DESIGN_OPERATION_ACCEPTED | N/A | Design-only code from API catalog |
| 4 | message | Response message | message | string | No | N/A | N/A | 6.1 | SOURCE_REQUIRED | N/A | Message text/catalog not defined for API #17 |
| 5 | data | Operation | data | Operation | No | Logical Operation | N/A | 5.1 | Object mapping per reusable schema | Required on accepted response | Operation persistence/source fields not defined |
| 5.1 | data.id | Operation ID | id | uuid | No | Logical Operation | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Shared Operation schema says uuid; physical generator/storage SOURCE_REQUIRED |
| 5.2 | data.kind | Operation kind | kind | OperationKind | No | Logical Operation | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Enum members are not listed |
| 5.3 | data.status | Operation status | status | OperationStatus | No | Logical Operation | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Enum members and initial value are not listed |
| 5.4 | data.owner_id | Operation owner ID | owner_id | int64 | No | Logical Operation | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Owner identity/claim mapping and persistence are not defined |
| 5.5 | data.submitted_at | Submission time | submitted_at | date-time | No | Logical Operation | SOURCE_REQUIRED | 5.1 | ISO-8601 per API convention | Required | Clock/source and precision not defined |
| 5.6 | data.updated_at | Update time | updated_at | date-time | No | Logical Operation | SOURCE_REQUIRED | 5.1 | ISO-8601 per API convention | Required | Update lifecycle/precision not defined |
| 5.7 | data.completed_at | Completion time | completed_at | date-time | Yes — optional | Logical Operation | SOURCE_REQUIRED | 5.1 | Direct logical field | Optional field; absent/null policy not defined | Operation lifecycle not specified |
| 5.8 | data.result | Payment result | result | Payment | Yes — optional | Logical Payment | N/A | 5.1 | Object mapping per reusable schema | Optional field | Inclusion condition and source step not defined |
| 5.8.1 | data.result.id | Payment ID | id | int64 | No | Logical Payment / candidate payments | payments.id | 5.1 | Direct logical field | Required if result is present | Physical persistence is DESIGN_ONLY; not runtime verified |
| 5.8.2 | data.result.order_id | Order ID | order_id | int64 | No | Logical Payment | SOURCE_REQUIRED | 5.1 | Direct logical field | Required if result is present | No payments.order_id or physical orders table in DB.sql |
| 5.8.3 | data.result.provider | Payment provider | provider | PaymentProvider | No | Logical Payment / candidate payments | payments.provider | 5.1 | SOURCE_REQUIRED | Required if result is present | API request uses string; enum members/continuity unresolved |
| 5.8.4 | data.result.amount | Payment amount | amount | decimal-string | No | Logical Payment / candidate payments | payments.amount | 5.1 | Decimal value serialized as string per catalog convention | Required if result is present | Amount source/currency mapping unresolved |
| 5.8.5 | data.result.status | Payment status | status | PaymentStatus | No | Logical Payment / candidate payments | payments.status | 5.1 | SOURCE_REQUIRED | Required if result is present | Enum members and transition rules not listed |
| 5.8.6 | data.result.transaction_code | Provider transaction code | transaction_code | string | Yes — optional | Logical Payment / candidate payments | payments.transaction_code | 5.1 | SOURCE_REQUIRED | Optional field | Gateway response and absent/null policy not defined |
| 5.8.7 | data.result.paid_at | Payment time | paid_at | date-time | Yes — optional | Logical Payment / candidate payments | payments.paid_at | 5.1 | ISO-8601 per API convention | Optional field | Confirmation condition/time source not defined |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 6.1 | ApiEnvelope field | Object shape not defined | Shared envelope schema |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 6.1 | Direct envelope field | Required by shared envelope schema | API #17 runtime value generation not specified |

## Ví dụ thành công

Các giá trị mẫu chỉ minh họa JSON shape. OperationKind và OperationStatus là placeholder vì enum members chưa có nguồn; owner_id, timestamps và UUID không xác nhận cách sinh hoặc persistence. result được bỏ qua vì Payment là optional trong Operation schema.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_ACCEPTED",
  "message": "<MESSAGE>",
  "data": {
    "id": "00000000-0000-4000-8000-000000000017",
    "kind": "<OperationKind: SOURCE_REQUIRED>",
    "status": "<OperationStatus: SOURCE_REQUIRED>",
    "owner_id": 123,
    "submitted_at": "2026-10-11T00:00:00Z",
    "updated_at": "2026-10-11T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000018"
}
~~~

## Ví dụ lỗi

Ví dụ minh họa business code 503 đã khai báo trong catalog. Message literal và error envelope data/meta behavior chưa được định nghĩa riêng cho API #17; các placeholder không phải contract value.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "<MESSAGE>",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000018"
}
~~~

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md.
- Sheet logic: 2.Response.
