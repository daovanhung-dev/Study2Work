---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: "markdown"
dd_id: "API-INT-011"
api_name: "GET wss://work-api.study2work.vn/api/v1/realtime"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Traceability matrices

### Request Usage Matrix

| Request field/item | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
| ---: | --- | --- | --- | --- | --- | --- | --- |
| Handshake token transport | API catalog | S01/S02 | Secure subprotocol or first authentication frame | Authenticate connection | Connection establishment | N/A | Physical carrier remains SOURCE_REQUIRED. |
| `type` | API catalog | S01/S03 | DIRECT value subscribe | Subscription dispatch | Per client message | N/A | DIRECT named field/value. |
| `applicationId` | API catalog | S01/S03 | Authorization per application | Subscription lookup | Per client message | N/A | Type/requiredness remains SOURCE_REQUIRED. |
| `lastSequence` | API catalog | S01/S03 | Gap-detection input | Resume/reload decision | Per client message | N/A | Type/requiredness remains SOURCE_REQUIRED. |

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
| `type` | `string` | Protocol | N/A | S06 | DIRECT | N/A | API-INT-011 |
| `eventId` | `string` | Protocol | N/A | S06 | DIRECT | N/A | API-INT-011 |
| `sequence` | `integer` | Protocol | N/A | S06 | DIRECT | N/A | API-INT-011 |
| `occurredAt` | `string` | Protocol | N/A | S06 | DIRECT | N/A | API-INT-011 |

## Flow xử lý data

<a id="s01"></a>
### S01. Get request/protocol data

- Receive only items documented in [03_Request.md](./03_Request.md).
- Do not convert unnamed source phrases into JSON keys.

<a id="s02"></a>
### S02. Authentication and authorization

- Actor/authorization source: Ứng viên/thành viên Work đã xác thực.
- Apply WebSocket authentication and subscription authorization.

<a id="s03"></a>
### S03. Validate source-confirmed input

- Validate only constraints named by endpoint/global contract; absent physical schema remains `SOURCE_REQUIRED`.
- Endpoint input contract: N/A — WebSocket protocol is specified as one contract..

<a id="s04"></a>
### S04. Execute source-defined processing

> Ứng dụng khách gửi mã truy cập qua giao thức con bảo mật/khung xác thực đầu tiên; máy chủ kiểm đối tượng nhận/phiên/bản chiếu. Đăng ký theo dõi `{type:"subscribe", applicationId, lastSequence}`; máy chủ kiểm quyền cho từng đơn ứng tuyển và phân công nhà tuyển dụng. Sự kiện `message.created`, `message.tombstoned`, `receipt.updated`, `conversation.read_only`, `interview.changed`, `notification.created`. Có `eventId`, `sequence`, `occurredAt`; giao ít nhất một lần nên ứng dụng khách khử trùng lặp và phát hiện khoảng trống rồi gọi lịch sử REST. Gói kiểm tra sống mỗi 25 giây, hết thời gian 60 giây, kết nối lại theo cấp số nhân. Kết nối WebSocket không là nguồn dữ liệu và không nhận chuyển trạng thái ATS.

- Operations/observability contract: N/A — WebSocket lifecycle is part of the protocol contract.

<a id="s05"></a>
### S05. Idempotency, transaction and failure handling

- N/A — no source-confirmed business mutation.
- Refer to [06_Error.md](./06_Error.md); never return stack traces, SQL, secrets or tokens.

<a id="s06"></a>
### S06. Map response/protocol output

- Map only protocol fields and at-least-once delivery semantics; clients deduplicate and reload REST history after a sequence gap.

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/05_Data_Mapping.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `3. Data mapping`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
