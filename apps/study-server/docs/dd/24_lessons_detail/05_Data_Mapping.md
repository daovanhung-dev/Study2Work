---
title: "Data Mapping"
order: 5
dd_id: "24"
api_name: "Nạp nội dung bài học / Lấy nội dung chính"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Nhận Authorization Bearer JWT; catalog yêu cầu actor Student. API #24 chưa có runtime route/auth binding.
1. Nhận path lesson_id:int64!; catalog không khai báo query hoặc body.
2. AC-14 yêu cầu Student đã enrolled và đi qua API #22 access check trước API #23 start; AC-15 yêu cầu có access và diagram ghi kiểm tra access + publish status cho API #24.
3. Predicate entitlement, identity claim mapping, prerequisite và publish scope chưa được định nghĩa; không coi API #22 client call là authorization của lời gọi API #24 độc lập.
4. Candidate data source là lessons; API #24 query, selected columns, parent-course lookup và visibility filter chưa được xác nhận.
5. Map candidate Lesson theo catalog: lessons.id → id; course_id → course_id; name → title; content → content; video_url → video_url; sort_order → order; status → status.
6. Trả HTTP 200 DESIGN_RESOURCE_RETRIEVED với ApiEnvelope<Lesson> theo catalog; mapping runtime chưa xác minh.
7. Giữ 401/403/404/500 theo catalog; điều kiện cụ thể của 403/404 và error payload/message chưa được xác nhận.
8. API là GET read-only; không có write mapping hoặc transaction được mô tả.
~~~

## Request Usage Matrix

| Request field | Source | Validate | Query usage | Response usage | Gap |
|---|---|---|---|---|---|
| Authorization | HTTP header `Authorization` | Bearer JWT; actor role Student theo catalog | Entitlement lookup cần identity nếu policy yêu cầu | Không được trả trong response | API #24 không có auth binding; claim-to-user mapping cần xác nhận. |
| lesson_id | `path["lesson_id"]` | Required `int64` theo catalog | Candidate lookup `lessons.id` | Xác định Lesson cần trả | Range, positivity, parse error mapping và visibility semantics chưa xác nhận. |
| Query parameters | N/A | N/A | N/A | N/A | Catalog không khai báo query parameter. |
| Request body | N/A | N/A | N/A | N/A | Catalog không khai báo request body. |

## 0. Authentication and access

### 0.1. Thực hiện check quyền

- Design contract yêu cầu Bearer JWT và role Student.
- AC-14 precondition nói Student đã enrolled vào course chứa lesson; sequence có API #22 check enrollment/prerequisite trước API #23 và API #24.
- AC-15 precondition nói Student có quyền xem lesson; diagram ghi bước `Kiểm tra access + trạng thái publish` trước khi đọc lesson/content.
- Điều kiện enrollment hợp lệ, prerequisite, publish status/entity và lời gọi API #24 trực tiếp chưa được xác nhận.
- Shared auth helper hiện có trong Study source không chứng minh API #24 đã dùng helper hoặc entitlement policy.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer JWT | Required; actor role Student | Catalog contract; API #24 runtime chưa wired. |
| JWT claims | user identity | SOURCE_REQUIRED | Claim và cách bind sang enrollment chưa được API #24 contract xác nhận. |
| API #22 access check | `lesson_id` | AC-14 đặt trước API #23 và #24 trong client flow | Không chứng minh server có thể tin request trước đó cho direct call. |
| `enrollments` — candidate | `user_id`, `course_id`, `status` | Predicate/status eligibility SOURCE_REQUIRED | Checked-in DB design only; không chọn trạng thái được phép. |
| Publish state — candidate | `lessons.status` và/hoặc `courses.status` | Entity/status scope SOURCE_REQUIRED | AC-15 nói publish status nhưng không nêu check lesson, course hay cả hai. |
| Prerequisite source | SOURCE_REQUIRED | SOURCE_REQUIRED | AC-14 nêu prerequisite nhưng model/evaluation chưa được đặc tả. |

### 0.3. Check kết quả

- Nếu authentication thất bại, contract khai báo HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu role/access bị từ chối, contract khai báo HTTP 403 `DESIGN_ACCESS_DENIED`; API #24-specific predicate/reason field chưa được xác nhận.
- Catalog khai báo HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`; lesson-missing, parent-missing và unpublished-resource mapping cần xác nhận.
- Không kết luận API #24 đang thực thi checks này; endpoint hiện `UNWIRED / NOT_FOUND`.

## 1. Request validation

| Request field | Nguồn | Validate | Branch/Usage | Gap |
|---|---|---|---|---|
| Authorization | HTTP header | Bearer JWT, role Student theo catalog | Authentication/authorization | Claim, token policy và entitlement binding chưa được API #24 xác nhận. |
| lesson_id | Path parameter | Required `int64` theo catalog | Candidate lesson lookup | Min/max, positivity và invalid-path status chưa được quy định. |
| Query parameters | N/A | N/A | N/A | Catalog không khai báo. |
| Request body | N/A | N/A | N/A | Catalog không khai báo. |

> Catalog không liệt kê 422 cho API #24; không thêm validation code hoặc trigger. Hành vi framework khi path parse lỗi chưa thể xác nhận từ endpoint chưa tồn tại.

## 2. Read lesson data

### 2.1. Query Matrix

| Query ID | Mục đích | Type | Target table/API | Selected column | Condition | Result variable | Branch/status |
|---|---|---|---|---|---|---|---|
| Q1 | Resolve Lesson payload | READ candidate | `lessons AS l` — DESIGN_ONLY | Candidate: `l.id`, `l.course_id`, `l.name`, `l.content`, `l.video_url`, `l.sort_order`, `l.status` | Candidate identity: `l.id = :lesson_id`; publication/access filters SOURCE_REQUIRED | `lesson_row` — logical placeholder | Query/API #24 source not found; not an approved SQL statement. |
| Q2 | Resolve entitlement and publish decision | READ policy — SOURCE_REQUIRED | Candidate: `enrollments`, `courses`, `lessons`, or approved policy source | SOURCE_REQUIRED | SOURCE_REQUIRED | `access_decision` — logical placeholder | AC-14/15 state the check; data source and predicate are unspecified. |

### 2.2. Candidate schema references

| Target table | Column/relationship | Evidence | Status |
|---|---|---|---|
| `lessons` | `id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status` | Checked-in `DB.sql` and `DB_UNICA_TABLES.md`; reusable Lesson mapping documented by catalog/DB design. | DESIGN_ONLY; API #24 projection not confirmed. |
| `lessons.course_id` | FK candidate to `courses.id` | Checked-in DDL and DB design documentation. | DESIGN_ONLY; DDL omits `NOT NULL`, while DB design describes it as required. |
| `enrollments` | `user_id`, `course_id`, `status` | Checked-in DDL/DB design and AC-14 enrollment precondition. | Candidate only; eligibility and query not confirmed. |
| `courses.status` | Parent course publication state | Checked-in schema and adjacent public-course DD design. | Candidate only; AC-15 does not specify whether API #24 checks it. |

### 2.3. Query rules

- Exact query, joins, selected fields, access predicate and visibility filters are SOURCE_REQUIRED.
- Candidate Lesson identity is the requested `lesson_id`; this is not a verified query predicate.
- AC-15 publish check does not establish which entity status is checked or how unpublished content maps to 403 versus 404.
- Checked-in DDL and ERD are design evidence; live database metadata was not checked.

## 3. Response mapping

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| `data.id` | `lessons.id` | Direct candidate mapping to `Lesson.id:int64` | DESIGN_ONLY; query not confirmed. |
| `data.course_id` | `lessons.course_id` | Direct candidate mapping to `Lesson.course_id:int64` | DESIGN_ONLY; DDL nullability differs from design/catalog expectation. |
| `data.title` | `lessons.name` | `name` → logical `title:string` | Candidate mapping from DB design; query not confirmed. |
| `data.content` | `lessons.content` | Direct candidate mapping to optional `string` | Null versus omitted behavior SOURCE_REQUIRED. |
| `data.video_url` | `lessons.video_url` | Candidate `TEXT` → `uri` | Null/omit and URI serialization/validation SOURCE_REQUIRED. |
| `data.order` | `lessons.sort_order` | `sort_order` → logical `order:int32` | Candidate mapping from DB design; query not confirmed. |
| `data.status` | `lessons.status` | Candidate direct mapping to `LessonStatus` | Enum values and publish-state treatment SOURCE_REQUIRED. |
| `meta` | ApiEnvelope schema | Object per reusable envelope | API-specific members unspecified. |
| `traceId` | ApiEnvelope schema | UUID per reusable envelope | Runtime generation/propagation not verified for API #24. |

`created_at` and `updated_at` exist in checked-in DDL but are not fields in the reusable `Lesson` schema; this DD does not add them to the response.

## 4. Result and error mapping

### 4.1. Thành công

- Catalog: HTTPStatus = 200; businessCode = `DESIGN_RESOURCE_RETRIEVED`.
- Response contract: `ApiEnvelope<Lesson>`; candidate fields are listed in [04_Response.md](./04_Response.md).
- AC-14/15 describe reading Lesson/content; exact query and serializer are not present in current runtime.

### 4.2. Authentication/authorization/resource errors

- Preserve catalog HTTP/business codes 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED` and 404 `DESIGN_RESOURCE_NOT_FOUND`.
- API-specific access predicate, publish policy, 403 reason shape and 404 resource/visibility condition are SOURCE_REQUIRED.

### 4.3. System error

- Catalog: HTTPStatus = 500; businessCode = `DESIGN_INTERNAL_ERROR`.
- No runtime API #24 exists to verify exception mapping, error payload or trace behavior.

### 4.4. Mutation/transaction

- API #24 is GET and catalog/diagrams do not describe a write.
- No insert/update/delete mapping or transaction boundary is defined; see [07_table.md](./07_table.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [05_Data_Mapping.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md).
- Sheet nguồn: 3. Data mapping.
