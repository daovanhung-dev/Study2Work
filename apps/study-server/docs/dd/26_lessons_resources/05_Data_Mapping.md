---
title: "Data Mapping"
order: 5
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

1. Nhận `Authorization` và `lesson_id` theo [03_Request.md](./03_Request.md).
2. Áp dụng authentication/role theo contract; entitlement và publish predicate cho lời gọi API #26 còn SOURCE_REQUIRED.
3. Candidate source đọc là `resources`, với relation `resources.lesson_id → lessons.id` theo DB design. Không có API #26 query runtime để xác nhận điều kiện, join hoặc projection.
4. Catalog yêu cầu `ApiEnvelope<Lesson>`. Không có field `Resource[]` được khai báo cho response; giữ mâu thuẫn này ở [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-26-01-response-type-và-resource-payload).
5. Map business code theo [04_Response.md](./04_Response.md#business-code-by-status) và [06_Error.md](./06_Error.md).

## Request Usage Matrix

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| `Authorization` | Request header | Bearer JWT theo catalog; token/claim behavior chưa được API #26 xác minh. | Student identity/access check chưa đặc tả. | Không map vào response. | JWT identity claim và direct-call entitlement policy SOURCE_REQUIRED. |
| `lesson_id` | Path `/api/v1/lessons/{lesson_id}/resources` | Required `int64` theo catalog. | Candidate relation `resources.lesson_id = lesson_id`; chưa phải approved SQL. | Không map trực tiếp vào `Lesson` fields. | Min/max/positive rule, invalid path mapping, response/resource projection SOURCE_REQUIRED. |

## 0. Authentication and access

### 0.1. Contract

- API catalog yêu cầu Bearer JWT và role `Student`.
- AC-15 precondition ghi Student có quyền xem lesson.
- AC-15 diagram ghi “Kiểm tra access + trạng thái publish” trong lesson flow, nhưng không nêu predicate hoặc xác nhận API #26 có tự thực hiện check khi gọi độc lập.

### 0.2. Access source matrix

| Source | Data/condition | Status | Remarks |
|---|---|---|---|
| Bearer JWT | Student role | Contract | Runtime API #26 chưa tồn tại để xác minh enforcement. |
| Enrollment/access policy | User-to-course/lesson entitlement | SOURCE_REQUIRED | Không chọn claim, trạng thái enrollment hoặc prerequisite rule. |
| Publish state | Lesson/course status | SOURCE_REQUIRED | Không xác định entity, allowed state hoặc filter. |

### 0.3. Decision

- Nếu authentication/authorization thất bại theo contract, trả code tương ứng ở [06_Error.md](./06_Error.md).
- Không tự thiết kế JWT claim binding hoặc access SQL.

## 1. Request validation

- `lesson_id`: catalog yêu cầu `int64` và bắt buộc.
- `lesson_id` minimum, maximum, positivity và parse-error mapping: SOURCE_REQUIRED.
- Catalog không khai báo HTTP 422 cho API #26; không thêm 422 business code.

## 2. Read lesson resources

### 2.1. Request-to-query intent

| Query ID | Mục đích | Type | Target table | Selected columns | Candidate condition | Result variable | Branch |
|---|---|---|---|---|---|---|---|
| Q1 | Đọc resource metadata gắn với lesson | READ — DESIGN_ONLY | `resources AS r` | Candidate columns trong [07_table.md](./07_table.md#candidate-read-mapping) | Candidate `r.lesson_id = :lesson_id` từ ERD relation; chưa được runtime/API #26 xác nhận. | `resource_rows` — logical placeholder | Query/cardinality/empty behavior SOURCE_REQUIRED. |
| Q2 | Xác định access/publish eligibility | READ policy — SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | SOURCE_REQUIRED | `access_decision` — logical placeholder | AC-15 precondition/diagram không đủ chốt predicate. |

### 2.2. Join, ordering and cardinality

- ERD khai báo relation `resources.lesson_id → lessons.id`.
- API #26 không có query source/runtime để xác nhận join thực tế.
- Không có sort key, pagination hoặc max result trong API contract.
- Không chọn một row, array, page, thứ tự, hoặc empty-result behavior; xem [Q-26-02](./OPEN_QUESTIONS.md#q-26-02-cardinality-ordering-and-empty-result).

## 3. Response mapping

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| `success` | `ApiEnvelope<T>` schema | Envelope field | Contract schema; runtime serialization chưa xác minh. |
| `businessCode` | API #26 catalog | Fixed by branch | Direct contract. |
| `message` | `ApiEnvelope<T>` schema | Envelope field | Text policy SOURCE_REQUIRED. |
| `data` | API #26 catalog | `Lesson` theo catalog | DISCREPANCY với endpoint resource intent; payload projection SOURCE_REQUIRED. |
| `data.id` | `lessons.id` | Candidate mapping theo reusable `Lesson`. | DESIGN_ONLY; API #26 query chưa xác nhận. |
| `data.course_id` | `lessons.course_id` | Candidate direct mapping. | DESIGN_ONLY; DDL nullable mismatch cần xác nhận. |
| `data.title` | `lessons.name` | Candidate alias `name` → `title`. | DESIGN_ONLY; API #26 projection chưa xác nhận. |
| `data.content` | `lessons.content` | Candidate direct mapping. | Null/omit behavior SOURCE_REQUIRED. |
| `data.video_url` | `lessons.video_url` | Candidate TEXT → URI. | Null/omit/conversion SOURCE_REQUIRED. |
| `data.order` | `lessons.sort_order` | Candidate alias `sort_order` → `order`. | DESIGN_ONLY; API #26 projection chưa xác nhận. |
| `data.status` | `lessons.status` | Candidate direct mapping to `LessonStatus`. | Enum/filter semantics SOURCE_REQUIRED. |
| Resource item fields | `resources` | Candidate `id`, `name`, `resource_type`, `url`, `lesson_id`. | Not added to response contract; `Resource` payload/cardinality and visibility unresolved. |
| `meta` | `ApiEnvelope<T>` schema | Envelope field | Member set unspecified. |
| `traceId` | `ApiEnvelope<T>` schema | Envelope field | Runtime generator/propagation chưa xác minh. |

## 4. Mutation and external calls

### 4.1. Database mutation

- API #26 là GET theo catalog.
- Mutation: `N/A — READ-ONLY API`.
- Transaction: `N/A — không có mutation được khai báo`.

### 4.2. External resource access

- API #12 adjacent design có signed URL flow cho private resource.
- API #26 source/diagram không xác nhận resolve signed URL, gọi API #12, hoặc trả stored URL trực tiếp.
- Không tạo external call, URL transform hoặc storage policy trong DD này.

## 5. Result and error mapping

### 5.1. Success

- HTTP `200`; business code `DESIGN_RESOURCE_RETRIEVED`.
- Payload type giữ theo catalog là `ApiEnvelope<Lesson>`; response projection vẫn open.

### 5.2. Authentication/authorization/access errors

- Giữ HTTP `401 DESIGN_AUTHENTICATION_REQUIRED` và `403 DESIGN_ACCESS_DENIED`.
- Trigger cụ thể, entitlement, publish policy và error payload là SOURCE_REQUIRED.

### 5.3. Not found

- Giữ HTTP `404 DESIGN_RESOURCE_NOT_FOUND`.
- Chưa chốt lesson missing, không có resource, resource visibility hay access masking; không phân loại empty list thành 404.

### 5.4. System error

- Giữ HTTP `500 DESIGN_INTERNAL_ERROR`.
- Không suy ra exception mapping hoặc error payload từ API #12.

### 5.5. Links

- Error cases: [06_Error.md](./06_Error.md).
- Unresolved response/access/schema decisions: [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

