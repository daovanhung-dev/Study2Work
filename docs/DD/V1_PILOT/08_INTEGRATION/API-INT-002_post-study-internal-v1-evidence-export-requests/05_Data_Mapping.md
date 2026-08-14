---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: "markdown"
dd_id: "API-INT-002"
api_name: "POST study /internal/v1/evidence-export-requests"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Traceability matrices

### Request Usage Matrix

| Request field/item | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| SOURCE_REQUIRED | BD global/endpoint convention | S01/S02 | As stated | Authentication/idempotency/concurrency | N/A | N/A | N/A |
| `evidenceId` | API catalog | S01/S03 | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | N/A | Physical key direct; location/type not locked. |
| `expectedVersion` | API catalog | S01/S03 | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | N/A | Physical key direct; location/type not locked. |
| ID yêu cầu, ID đơn ứng tuyển, chủ thể nền tảng,  đã chọn, phiên bản/hàm băm đồng ý | API catalog | S01/S03 | SOURCE_REQUIRED | SOURCE_REQUIRED | N/A | N/A | Not materialized as a physical key. |

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
| `data` | `object \| array \| null` | Endpoint output phrase | N/A | S06 | `202` | SOURCE_REQUIRED for nested shape | API catalog |
| `meta` | `object` | Envelope metadata | N/A | S06 | Pagination/field errors only when applicable | {} | BD §2.1 |
| `traceId` | `string` | Trace propagation/generation | N/A | S06 | DIRECT global convention | N/A | BD §2.1 |

## Flow xử lý data

<a id="s01"></a>
### S01. Get request/protocol data

- Receive only items documented in [03_Request.md](./03_Request.md).
- Do not convert unnamed source phrases into JSON keys.

<a id="s02"></a>
### S02. Authentication and authorization

- Actor/authorization source: JWT dịch vụ Work + chữ ký phần thân tách rời, `aud=study-internal`.
- Apply mTLS, service JWT audience/signature and replay protection.

<a id="s03"></a>
### S03. Validate source-confirmed input

- Validate only constraints named by endpoint/global contract; absent physical schema remains `SOURCE_REQUIRED`.
- Endpoint input contract: ID yêu cầu, ID đơn ứng tuyển, chủ thể nền tảng, `{evidenceId,expectedVersion}` đã chọn, phiên bản/hàm băm đồng ý → `202`.

<a id="s04"></a>
### S04. Execute source-defined processing

> ID yêu cầu duy nhất; kiểm thời điểm/nonce <=5 phút; lưu yêu cầu/hộp thư đi. Tiến trình nền kiểm chủ sở hữu Study, `ISSUED`, đúng phiên bản, chưa thu hồi; tạo kết quả tối thiểu đã ký. Không chấp nhận ID ứng viên được khẳng định nếu không ánh xạ chủ thể mã thông báo

- Operations/observability contract: N/A — internal endpoint table has no separate operations column.

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
