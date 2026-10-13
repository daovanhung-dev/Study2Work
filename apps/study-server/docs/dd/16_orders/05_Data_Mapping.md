---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
---

# Data Mapping

## Flow xử lý data

Luồng bên dưới mô tả expected design theo API contract và AC-12. API #16 chưa có runtime implementation; các bước cần physical Order schema được giữ ở trạng thái `SOURCE_REQUIRED`.

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Yêu cầu Bearer JWT theo contract API #16.
- Chỉ Student được gọi theo contract API #16.
- Claim cụ thể dùng làm `user_id` chưa được chốt cho API #16.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| N/A | N/A | N/A | Contract khai báo Student Bearer JWT; không chỉ định query quyền riêng. |

### 0.3. Check kết quả

- Thiếu hoặc JWT không hợp lệ: trả lỗi theo [06_Error.md](./06_Error.md), case 1.
- Role không phải Student: trả lỗi theo [06_Error.md](./06_Error.md), case 2.
- Không tự thêm ownership query hoặc role khác.

## 1. Get request data

### 1.1. Get request header

- `Authorization`: lấy Bearer JWT theo contract.
- `Content-Type`: `application/json` cho request body.

### 1.2. Get request data

- `course_id`: lấy từ body JSON; type `int64`; bắt buộc.
- `payment_provider`: lấy từ body JSON; type `PaymentProvider`; bắt buộc.
- Danh sách member hợp lệ của `PaymentProvider`: `SOURCE_REQUIRED`.
- Không lấy `user_id` từ body, query hoặc header bổ sung; contract không khai báo các input này.

## 2. Validate data input

- Kiểm tra sự hiện diện và kiểu `int64` của `course_id` theo request contract.
- Không tự thêm minimum, maximum hoặc positive-number rule cho `course_id`.
- Kiểm tra sự hiện diện của `payment_provider` theo request contract.
- Không thể chốt enum membership validation cho `payment_provider` khi chưa có allowed values.
- Request validation failure dùng HTTP 422 `DESIGN_VALIDATION_ERROR` theo API catalog; chi tiết điều kiện/provider message còn SOURCE_REQUIRED.

## 3. Evaluate AC-12 entry context

- AC-12 đặt API #8 course detail trước API #15 enrollment-status trong flow đăng ký khóa học.
- AC-12 kiểm tra enrollment hiện có trước khi phân nhánh tiếp.
- AC-12 bỏ qua Order/Payment với khóa học miễn phí.
- AC-12 gọi API #16 trong nhánh paid course.
- Các bước trên là flow context; nguồn hiện có không xác nhận API #16 tự gọi API #8/#15 hoặc lặp lại các predicate.
- Hành vi của API #16 khi được gọi trực tiếp cho course không hợp lệ, miễn phí hoặc đã enrolled là `SOURCE_REQUIRED`.

## 4. Create logical Order

- AC-12 mô tả bước `INSERT Order = PENDING`.
- Logical status ban đầu là `PENDING` theo AC-12.
- Physical table/column mapping: `SOURCE_REQUIRED`; không có bảng `orders` trong ERD V1 hoặc checked-in DB.sql.
- Không dùng bảng `payments` thay cho Order; API #17 tạo/xử lý payment riêng sau bước này.
- Transaction boundary, rollback và idempotency chưa được xác định.
- Không thể lập SQL hoặc điều kiện uniqueness khi schema/policy chưa có nguồn.

## Query Matrix

| Step | Operation | Target table/API | Condition | Result | Evidence/status |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | API #16 query không được xác định trong contract hoặc AC-12 | N/A | `SOURCE_REQUIRED` nếu implementation cần đọc course price/eligibility trong endpoint này |
| Context | Prior API calls | API #8 và API #15 | N/A | Course detail và enrollment status trong flow AC-12 | Ngoài query matrix của endpoint #16; không giả định endpoint #16 gọi lại |

## Mutation Matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| M1 | INSERT logical Order | `SOURCE_REQUIRED` — physical table chưa xác định | `SOURCE_REQUIRED` — uniqueness/duplicate policy chưa có | Physical columns `SOURCE_REQUIRED` | AC-12 xác nhận logical state ban đầu `PENDING`; các field khác chưa có mapping đủ nguồn | SOURCE_REQUIRED | [07_table.md](./07_table.md) | SOURCE_REQUIRED | Contract có 500; rollback và persistence behavior chưa xác định |

## Response Source Matrix

| Response field | Type | Source type | Table/column hoặc generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| `data.id` | `int64` | Logical Order contract | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Physical key/generator chưa được xác nhận |
| `data.course_id` | `int64` | Request-to-Order association | `course_id` trong request; physical column SOURCE_REQUIRED | 5.1 | Direct logical association | Required | Physical persistence chưa được xác nhận |
| `data.user_id` | `int64` | Authenticated Student context | JWT claim/mapping SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Claim/physical column mapping chưa được xác nhận cho API #16 |
| `data.amount` | `decimal-string` | Logical Order contract | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Không có nguồn xác nhận tính amount từ course price hoặc rule khác |
| `data.currency` | `string` | Logical Order contract | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Không có currency source/value |
| `data.status` | `OrderStatus` | AC-12 logical initial state | SOURCE_REQUIRED | 5.1 | `PENDING` ở bước tạo | Required | Các enum value khác và physical mapping chưa xác nhận |
| `data.created_at` | `date-time` | Logical Order contract | SOURCE_REQUIRED | 5.1 | SOURCE_REQUIRED | Required | Time source/precision chưa được xác định |
| `businessCode` | `string` | Contract constant | `DESIGN_RESOURCE_CREATED` | 6.1 | Fixed on success | Required | Design-only business code |
| `traceId` | `uuid` | Envelope contract | Trace context/source generator SOURCE_REQUIRED | 6.1 | Per shared envelope contract | Required | API #16 runtime not wired |

## 5. Map response

### 5.1. Map Order

- Response schema là logical `Order` từ API catalog.
- Map `id`, `course_id`, `user_id`, `amount`, `currency`, `status`, `created_at` theo [04_Response.md](./04_Response.md).
- Không thể chốt physical mapping cho các field này cho đến khi có Order schema.
- Không trả `payment_provider` trong Order response vì field này không thuộc schema Order hiện tại.

## 6. Trả về response

### 6.1. Success response

- HTTPStatus = 201.
- `success = true`.
- `businessCode = DESIGN_RESOURCE_CREATED`.
- `data` có logical shape `Order`.
- `meta` có type object theo ApiEnvelope; shape cụ thể chưa khai báo.
- `traceId` có type UUID theo ApiEnvelope.

### 6.2. Error response

- HTTPStatus và business code chỉ dùng các lỗi đã liệt kê trong API catalog.
- Chi tiết refer [06_Error.md](./06_Error.md).
- Không thêm 404, 409 hoặc 503 cho API #16.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md.
- Sheet logic: 3. Data mapping.

