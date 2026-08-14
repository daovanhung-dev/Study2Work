---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: "markdown"
dd_id: "API-IAM-007"
api_name: "POST /api/v1/auth/logout"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Traceability matrices

### Request Usage Matrix

| Request field/item | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| Authorization | BD global/endpoint convention | S01/S02 | As stated | Authentication/idempotency/concurrency | N/A | N/A | N/A |
| Phiên/mã làm mới hiện tại | API catalog | S01/S03 | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | N/A | Not materialized as a physical key. |

### Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Q01` | N/A — no source-confirmed physical query. | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | S04 |

### Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `M01` | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | [07_source_required_mutation.md](./07_source_required_mutation.md) | TBD | Mutation candidate lacks confirmed physical target. |

### Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| `success` | `boolean` | Fixed branch | N/A | S06 | Success/error branch | N/A | BD §2.1 |
| `businessCode` | `string` | Endpoint/global contract | N/A | S06 | DIRECT or SOURCE_REQUIRED | N/A | No new code. |
| `message` | `string` | Safe response text | N/A | S06 | Localized safe text | N/A | BD §2.1 |
| `data` | `object \| array \| null` | Endpoint output phrase | N/A | S06 | thành công | SOURCE_REQUIRED for nested shape | API catalog |
| `meta` | `object` | Envelope metadata | N/A | S06 | Pagination/field errors only when applicable | {} | BD §2.1 |
| `traceId` | `string` | Trace propagation/generation | N/A | S06 | DIRECT global convention | N/A | BD §2.1 |

## Flow xử lý data

<a id="s01"></a>
### S01. Get request/protocol data

- Receive only items documented in [03_Request.md](./03_Request.md).
- Do not convert unnamed source phrases into JSON keys.

<a id="s02"></a>
### S02. Authentication and authorization

- Actor/authorization source: Đã xác thực.
- Apply public API authentication, account-state, permission, tenant and ownership rules from BD §2.2.

<a id="s03"></a>
### S03. Validate source-confirmed input

- Validate only constraints named by endpoint/global contract; absent physical schema remains `SOURCE_REQUIRED`.
- Endpoint input contract: Phiên/mã làm mới hiện tại → thành công.

<a id="s04"></a>
### S04. Execute source-defined processing

> TX thu hồi phiên hiện tại + mọi hàng mã làm mới chưa dùng

- Operations/observability contract: Lặp an toàn; kiểm toán

<a id="s05"></a>
### S05. Idempotency, transaction and failure handling

- TBD — this mutation candidate lacks a complete transaction boundary at endpoint detail.
- Refer to [06_Error.md](./06_Error.md); never return stack traces, SQL, secrets or tokens.

<a id="s06"></a>
### S06. Map response/protocol output

- Map the standard BD envelope in [04_Response.md](./04_Response.md); unnamed nested data remains SOURCE_REQUIRED.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `3. Data mapping`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
