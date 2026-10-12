---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

Luồng dưới đây là expected design từ API catalog và AC-12. API #17 chưa có runtime implementation; physical Order/payment mapping, gateway protocol và Operation lifecycle còn SOURCE_REQUIRED.

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Yêu cầu Bearer JWT theo contract API #17.
- Chỉ Student được gọi theo contract API #17.
- Chưa có nguồn xác nhận cách lấy owner_id hoặc kiểm tra Order thuộc Student hiện tại.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| N/A | N/A | N/A | Contract khai báo Student Bearer JWT; không chỉ định query quyền riêng. |

### 0.3. Check kết quả

- Thiếu hoặc JWT không hợp lệ: trả lỗi theo [06_Error.md](./06_Error.md), case 1.
- Role không phải Student: trả lỗi theo [06_Error.md](./06_Error.md), case 2.
- Direct-call ownership/eligibility policy cho order_id: SOURCE_REQUIRED; không thêm query hoặc error code.

## 1. Get request data

### 1.1. Get request header

- Authorization: Bearer JWT theo contract.
- Content-Type: application/json theo request body contract.

### 1.2. Get request data

- order_id: lấy từ body JSON; type int64; bắt buộc.
- provider: lấy từ body JSON; type string; bắt buộc.
- Allowed provider values và semantics: SOURCE_REQUIRED.
- Không lấy order_id, provider hoặc user identity từ field/body khác ngoài contract.

## 2. Validate data input

- Kiểm tra sự hiện diện và kiểu int64 của order_id theo request contract.
- Không tự thêm minimum/positive rule cho order_id.
- Kiểm tra sự hiện diện và kiểu string của provider theo request contract.
- Không thể chốt provider allowlist, max length, normalization hoặc API #16 continuity khi chưa có nguồn.
- Request validation failure dùng HTTP 422 DESIGN_VALIDATION_ERROR theo API catalog; điều kiện chi tiết và message còn SOURCE_REQUIRED.

## 3. Resolve Order context

### 3.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| SOURCE_REQUIRED — physical Order table chưa được xác định | SOURCE_REQUIRED | Logical Order từ API #16 | API catalog và AC-12 không chỉ rõ physical query cho API #17 |

### 3.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| N/A | N/A | N/A — không có physical Order schema để đặc tả JOIN |

### 3.3. WHERE

- order_id resolution/ownership condition: SOURCE_REQUIRED.
- Order status condition trước payment: SOURCE_REQUIRED.
- Order-to-Payment association: SOURCE_REQUIRED; DB.sql không khai báo payments.order_id.

### 3.4. ORDER BY

- N/A — thứ tự đọc không được đặc tả.

## 4. Initiate or confirm payment

- AC-12 đặt API #17 sau bước tạo logical Order của API #16 trong nhánh paid course.
- AC-12 mô tả Payment Gateway xử lý giao dịch; success đi tiếp tới bước xác nhận thanh toán và enrollment, failure/cancel dừng flow.
- DB_UNICA_TABLES đánh dấu API #17 là INSERT/external payment ở DESIGN_ONLY.
- Endpoint trả HTTP 202 DESIGN_OPERATION_ACCEPTED với ApiEnvelope<Operation> theo catalog.
- Gateway adapter, request/credential boundary, callback/webhook, retry, idempotency, duplicate handling và transaction/rollback behavior: SOURCE_REQUIRED.
- Operation storage, initial kind/status, progress, completion, result population và API #18 lookup source: SOURCE_REQUIRED.

## Query Matrix

| Step | Operation | Target table/API | Condition | Result | Evidence/status |
|---:|---|---|---|---|---|
| 3.1 | Resolve Order | Physical Order table SOURCE_REQUIRED | order_id; owner/status predicates SOURCE_REQUIRED | Logical Order context | API #16 schema exists; V1 physical mapping absent |
| 4.1 | Payment provider | External Payment Gateway | Protocol and request fields SOURCE_REQUIRED | External transaction outcome | AC-12 describes gateway and success/failure/cancel only |
| N/A | API #18 polling | GET /api/v1/operations/{operation_id} | Separate client call after accepted response | Operation status | Not invoked by API #17; operation_id type has catalog discrepancy |

## Mutation Matrix

| Mutation ID | Operation | Target table | Column/field | Record condition | Value source | Data Mapping step | Status/remarks |
|---|---|---|---|---|---|---|---|
| M1 | INSERT — design-only | payments | id | SOURCE_REQUIRED | BIGSERIAL in DB.sql; exact generated value source not runtime verified | 4 | Column exists in schema artifact |
| M1 | INSERT — design-only | payments | user_id | SOURCE_REQUIRED | Authenticated Student / Order ownership mapping SOURCE_REQUIRED | 4 | DB.sql permits NULL; DB_UNICA_TABLES marks required |
| M1 | INSERT — design-only | payments | course_id | SOURCE_REQUIRED | Order mapping SOURCE_REQUIRED | 4 | DB.sql permits NULL; DB_UNICA_TABLES marks required |
| M1 | INSERT — design-only | payments | amount | SOURCE_REQUIRED | Order amount/currency source SOURCE_REQUIRED | 4 | DB.sql NUMERIC(12,2); no approved amount rule |
| M1 | INSERT — design-only | payments | provider | SOURCE_REQUIRED | Request provider string; allowlist/adapter mapping SOURCE_REQUIRED | 4 | Column is VARCHAR(50) NOT NULL |
| M1 | INSERT — design-only | payments | transaction_code | SOURCE_REQUIRED | Gateway response SOURCE_REQUIRED | 4 | Column is unique and nullable in DB.sql |
| M1 | INSERT — design-only | payments | status | SOURCE_REQUIRED | PaymentStatus/initial transition SOURCE_REQUIRED | 4 | DB.sql default is PENDING; enum/use of default not confirmed |
| M1 | INSERT — design-only | payments | paid_at | SOURCE_REQUIRED | Gateway success confirmation time SOURCE_REQUIRED | 4 | Nullable timestamp in DB.sql |
| M1 | INSERT — design-only | payments | created_at | SOURCE_REQUIRED | Timestamp source SOURCE_REQUIRED | 4 | NOT NULL with no default in DB.sql |
| M2 | CREATE/queue | Operation store SOURCE_REQUIRED | id | SOURCE_REQUIRED | Operation schema requires uuid; generator/storage SOURCE_REQUIRED | 4 | No physical Operation table or service found |

## Response Source Matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| data.id | uuid | Operation schema | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Persistence/generator absent |
| data.kind | OperationKind | Operation schema | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Enum members absent |
| data.status | OperationStatus | Operation schema | SOURCE_REQUIRED | 5.1 | Direct logical field | Required | Enum members/initial state absent |
| data.owner_id | int64 | Operation schema | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | User identity source absent |
| data.submitted_at | date-time | Operation schema | SOURCE_REQUIRED | 5.1 | ISO-8601 | Required | Timestamp source absent |
| data.updated_at | date-time | Operation schema | SOURCE_REQUIRED | 5.1 | ISO-8601 | Required | Lifecycle/timestamp rule absent |
| data.completed_at | date-time | Operation schema | SOURCE_REQUIRED | 5.1 | Direct logical field | Optional | Completion rule absent |
| data.result.id | int64 | Payment schema | candidate payments.id | 5.1 | Direct logical field | Only if result present | DESIGN_ONLY physical persistence |
| data.result.order_id | int64 | Payment schema | SOURCE_REQUIRED — no payments.order_id | 5.1 | Direct logical field | Required if result present | Order association missing |
| data.result.provider | PaymentProvider | Payment schema | candidate payments.provider | 5.1 | SOURCE_REQUIRED | Required if result present | Request string/enum mapping absent |
| data.result.amount | decimal-string | Payment schema | candidate payments.amount | 5.1 | Decimal-string per API convention | Required if result present | Amount source unresolved |
| data.result.status | PaymentStatus | Payment schema | candidate payments.status | 5.1 | SOURCE_REQUIRED | Required if result present | Enum and state transitions absent |
| data.result.transaction_code | string | Payment schema | candidate payments.transaction_code | 5.1 | SOURCE_REQUIRED | Optional | Gateway mapping absent |
| data.result.paid_at | date-time | Payment schema | candidate payments.paid_at | 5.1 | ISO-8601 | Optional | Confirmation rule absent |
| businessCode | string | Contract constant | DESIGN_OPERATION_ACCEPTED | 6.1 | Fixed on accepted response | Required | Design-only code |
| traceId | uuid | ApiEnvelope schema | SOURCE_REQUIRED | 6.1 | Direct envelope field | Required | API #17 runtime source absent |

## 5. Map response

### 5.1. Map Operation

- Accepted response data uses the reusable Operation schema from [list_api.md](../../../../../docs/lists/list_api.md).
- Operation field shape and Payment result fields are listed in [04_Response.md](./04_Response.md).
- Payment is an optional Operation.result; no source defines whether it is populated in the initial 202 response or only after completion.
- Operation and Payment field values cannot be mapped to a current runtime table/service.

## 6. Return response

### 6.1. Accepted operation

- Return HTTP 202 and DESIGN_OPERATION_ACCEPTED according to API #17 contract.
- Use ApiEnvelope<Operation> shape; runtime serialization, message text, trace generation and error envelope behavior are not verified for this endpoint.
- Client operation tracking is a separate API #18 call; its contract type discrepancy is recorded in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md.
- Sheet logic: 3. Data mapping.
