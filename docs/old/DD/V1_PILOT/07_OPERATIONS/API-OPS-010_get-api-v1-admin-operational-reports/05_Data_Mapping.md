---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: "markdown"
dd_id: "API-OPS-010"
api_name: "GET /api/v1/admin/operational-reports"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Traceability matrices

### Request Usage Matrix

| Request field/item | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| Authorization | BD global/endpoint convention | S01/S02 | As stated | Authentication/idempotency/concurrency | N/A | N/A | N/A |
| Mã báo cáo/ngày/bộ lọc | API catalog | S01/S03 | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | N/A | Not materialized as a physical key. |

### Query Matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Q01` | N/A — no source-confirmed physical query. | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | S04 |

### Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| N/A | N/A — READ-ONLY API | N/A | N/A | N/A | N/A | N/A | [07_table.md](./07_table.md) | N/A | N/A |

### Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| `success` | `boolean` | Fixed branch | N/A | S06 | Success/error branch | N/A | BD §2.1 |
| `businessCode` | `string` | Endpoint/global contract | N/A | S06 | DIRECT or SOURCE_REQUIRED | N/A | No new code. |
| `message` | `string` | Safe response text | N/A | S06 | Localized safe text | N/A | BD §2.1 |
| `data` | `object \| array \| null` | Endpoint output phrase | N/A | S06 | chỉ số tổng hợp + độ mới | SOURCE_REQUIRED for nested shape | API catalog |
| `meta` | `object` | Envelope metadata | N/A | S06 | Pagination/field errors only when applicable | {} | BD §2.1 |
| `traceId` | `string` | Trace propagation/generation | N/A | S06 | DIRECT global convention | N/A | BD §2.1 |

## Flow xử lý data

<a id="s01"></a>
### S01. Get request/protocol data

- Receive only items documented in [03_Request.md](./03_Request.md).
- Do not convert unnamed source phrases into JSON keys.

<a id="s02"></a>
### S02. Authentication and authorization

- Actor/authorization source: Quyền báo cáo theo miền.
- Apply public API authentication, account-state, permission, tenant and ownership rules from BD §2.2.

<a id="s03"></a>
### S03. Validate source-confirmed input

- Validate only constraints named by endpoint/global contract; absent physical schema remains `SOURCE_REQUIRED`.
- Endpoint input contract: Mã báo cáo/ngày/bộ lọc → chỉ số tổng hợp + độ mới.

<a id="s04"></a>
### S04. Execute source-defined processing

> Đọc chỉ số/bản chiếu hằng ngày; không có kho dữ liệu ở V1; trả định nghĩa/phiên bản báo cáo

- Operations/observability contract: Bộ nhớ đệm 5 phút; kiểm toán truy cập

<a id="s05"></a>
### S05. Idempotency, transaction and failure handling

- N/A — no source-confirmed business mutation.
- Refer to [06_Error.md](./06_Error.md); never return stack traces, SQL, secrets or tokens.

<a id="s06"></a>
### S06. Map response/protocol output

- Map the standard BD envelope in [04_Response.md](./04_Response.md); unnamed nested data remains SOURCE_REQUIRED.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `3. Data mapping`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
