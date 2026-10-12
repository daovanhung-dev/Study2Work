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
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 5.1/5.2 | Fixed by response branch | N/A | Success 200; catalog errors 401, 403, 404 and 500 |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5.1/5.2 | true on success; false on error | N/A | ApiEnvelope field |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5.1/5.2 | Fixed by response branch | N/A | DESIGN_OPERATION_RETRIEVED on success; catalog-listed code on error |
| 4 | message | Message | message | string | No | N/A | N/A | 5.1/5.2 | Catalog does not define literal text | Message policy unspecified | ApiEnvelope field |
| 5 | data | Operation | data | object: Operation | No on success | Logical Operation | N/A | 4.1/5.1 | Map reusable Operation schema | Error representation unspecified | Physical source and error data shape are SOURCE_REQUIRED |
| 5.1 | data.id | Operation ID | id | UUID in reusable schema | No | Logical Operation | SOURCE_REQUIRED | 4.1 | Direct logical field | Required | API #18 row declares path ID int64; see Q-18-01 |
| 5.2 | data.kind | Operation kind | kind | OperationKind | No | Logical Operation | SOURCE_REQUIRED | 4.1 | Direct logical field | Required | Enum members are not defined |
| 5.3 | data.status | Operation status | status | OperationStatus | No | Logical Operation | SOURCE_REQUIRED | 4.1 | Direct logical field | Required | Enum members and lifecycle are not defined |
| 5.4 | data.owner_id | Owner ID | owner_id | int64 | No | Logical Operation | SOURCE_REQUIRED | 4.1 | Direct logical field | Required | Owner source and caller identity mapping are not defined |
| 5.5 | data.submitted_at | Submission time | submitted_at | date-time | No | Logical Operation | SOURCE_REQUIRED | 4.1 | ISO-8601 per catalog convention | Required | Source and precision are not defined |
| 5.6 | data.updated_at | Last update time | updated_at | date-time | No | Logical Operation | SOURCE_REQUIRED | 4.1 | ISO-8601 per catalog convention | Required | Update lifecycle and precision are not defined |
| 5.7 | data.completed_at | Completion time | completed_at | date-time | Yes — optional | Logical Operation | SOURCE_REQUIRED | 4.1 | Direct logical field | Optional; absent/null policy unspecified | Completion semantics are not defined |
| 5.8 | data.result | Operation result | result | Payment in reusable schema | Yes — optional | Logical Operation | SOURCE_REQUIRED | 4.1 | Direct logical field | Optional | Per-kind result contract is unresolved; see Q-18-04 |
| 5.8.1 | data.result.id | Payment ID | id | int64 | No when result is Payment | Logical Payment | SOURCE_REQUIRED | 4.1 | Direct logical field | Required if Payment result is present | Whether this result applies only to payment operations is unresolved |
| 5.8.2 | data.result.order_id | Order ID | order_id | int64 | No when result is Payment | Logical Payment | SOURCE_REQUIRED | 4.1 | Direct logical field | Required if Payment result is present | |
| 5.8.3 | data.result.provider | Payment provider | provider | PaymentProvider | No when result is Payment | Logical Payment | SOURCE_REQUIRED | 4.1 | Direct logical field | Required if Payment result is present | Enum members are not defined |
| 5.8.4 | data.result.amount | Payment amount | amount | decimal-string | No when result is Payment | Logical Payment | SOURCE_REQUIRED | 4.1 | Decimal serialized as string per catalog convention | Required if Payment result is present | |
| 5.8.5 | data.result.status | Payment status | status | PaymentStatus | No when result is Payment | Logical Payment | SOURCE_REQUIRED | 4.1 | Direct logical field | Required if Payment result is present | Enum members are not defined |
| 5.8.6 | data.result.transaction_code | Transaction code | transaction_code | string | Yes — optional | Logical Payment | SOURCE_REQUIRED | 4.1 | Direct logical field | Optional | |
| 5.8.7 | data.result.paid_at | Paid time | paid_at | date-time | Yes — optional | Logical Payment | SOURCE_REQUIRED | 4.1 | ISO-8601 per catalog convention | Optional | |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 5.1/5.2 | Shared envelope field | Object shape unspecified | Example uses an empty object only to illustrate envelope shape |
| 7 | traceId | Trace ID | traceId | UUID | No | N/A | N/A | 5.1/5.2 | Shared envelope field | Required by reusable schema | API-specific generation is not runtime-verified |

> The response example below follows the reusable Operation schema and deliberately uses enum placeholders. It illustrates shape only; it does not resolve the request path type, Operation persistence, result variants or message content.

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_OPERATION_RETRIEVED",
  "message": "<MESSAGE_TEXT_NOT_SPECIFIED>",
  "data": {
    "id": "00000000-0000-4000-8000-000000000018",
    "kind": "<OperationKind_SOURCE_REQUIRED>",
    "status": "<OperationStatus_SOURCE_REQUIRED>",
    "owner_id": 123,
    "submitted_at": "2026-10-11T00:00:00Z",
    "updated_at": "2026-10-11T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000019"
}
~~~

## Ví dụ lỗi — HTTP 403

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "<MESSAGE_TEXT_NOT_SPECIFIED>",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000020"
}
~~~

The error example uses the shared envelope shape for illustration. The catalog does not define literal message text or error data semantics for this endpoint.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/04_Response.md.
- Sheet logic: 2.Response.
