---
title: "Data Mapping"
order: 5
dd_id: "23"
api_name: "Khởi tạo/lưu lần bắt đầu học"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Nhận Bearer JWT; catalog yêu cầu Student. API #23 chưa có runtime route/auth binding.
1. Đọc path lesson_id:int64!; request không khai báo query hoặc body.
2. AC-14 đặt API #22 access check trước API #23; direct-call entitlement check của API #23 chưa được định nghĩa.
3. Khi flow được phép tiếp tục, AC-14 mô tả UPSERT lesson progress = IN_PROGRESS.
4. Target table candidate là lesson_progress; conflict key, user identity source, update fields, timestamps, state preservation và transaction chưa xác nhận.
5. Catalog success contract là HTTP 201 DESIGN_RESOURCE_CREATED với ApiEnvelope<Lesson>; response projection/query chưa được xác nhận.
6. Ánh xạ lỗi theo catalog: 401/403/404/422/500; API-specific trigger/message/response shape chưa được định nghĩa.
~~~

<a id="0-authentication-and-authorization"></a>

## 0. Authentication and authorization

### 0.1. Thực hiện check quyền

- Design contract yêu cầu Bearer JWT và role Student.
- AC-14 precondition nói Student đã enrolled vào course chứa lesson; diagram đặt API #22 enrollment/prerequisite check trước API #23.
- Catalog cũng khai báo 403 cho API #23, nhưng không nêu có lặp lại entitlement check khi endpoint được gọi trực tiếp.
- Không có route API #23 hiện tại gọi shared auth helper hoặc bind token identity vào progress row.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer JWT | Required; actor role Student | Contract thiết kế; runtime API #23 chưa wired. |
| API #22 access | lesson_id | AC-14 đặt access check trước API #23 | Không chứng minh API #23 có thể tin cậy một lời gọi API khác làm ranh giới authorization. |
| JWT claims | user identity | SOURCE_REQUIRED | Không chốt claim hoặc cách map sang lesson_progress.user_id trong DD này. |
| lessons | id | Candidate lesson identity | Checked-in schema/design only; query API #23 chưa xác nhận. |

### 0.3. Check kết quả

- Contract liệt kê 403 DESIGN_ACCESS_DENIED; predicate và hành vi khi gọi API #23 độc lập cần xác nhận.
- AC-14 nhắc lý do ở nhánh 403 của bước API #22; wire shape lý do không được áp sang API #23.
- Không xác định resource condition cho 404 từ nguồn hiện có.

<a id="1-request-validation"></a>

## 1. Request validation

| Request field | Nguồn | Validate | Branch/Usage | Gap |
|---|---|---|---|---|
| Authorization | HTTP header | Bearer JWT, role Student theo catalog | Identity/authorization | Claim mapping và access policy chưa xác nhận. |
| lesson_id | Path parameter | int64 bắt buộc theo catalog | Lesson/progress lookup candidate | Range, non-positive IDs, invalid-path mapping và 422 trigger chưa được quy định. |
| Query parameters | N/A | N/A | N/A | Catalog không khai báo query parameters. |
| Request body | N/A | N/A | N/A | Catalog không khai báo body. |

## 2. Get thông tin

### 2.1. Query matrix

| Query ID | Mục đích | Type | Base table/view | Columns | JOIN/WHERE | Result variable | Status |
|---|---|---|---|---|---|---|---|
| Q1 | Resolve lesson/progress context before start | SOURCE_REQUIRED | Candidate: lessons, lesson_progress | SOURCE_REQUIRED | SOURCE_REQUIRED | start_context — logical placeholder | No API #23 query is present in current source or approved SQL contract. |

### 2.2. Candidate schema references

| Target table | Column/relationship | Evidence | Status |
|---|---|---|---|
| lessons | id, course_id, name, content, video_url, sort_order, status | Checked-in DB.sql and DB_UNICA_TABLES.md; reusable Lesson mapping is documented elsewhere. | DESIGN_ONLY; API #23 response query not confirmed. |
| lesson_progress | id, user_id, lesson_id, status, progress_percent, last_accessed_at, completed_at | Checked-in DB.sql and DB_UNICA_TABLES.md. | DESIGN_ONLY; no user/lesson unique key appears in checked-in DDL. |
| lesson_progress.user_id | Candidate identity relationship | DB design links progress row to users. | Token-to-user mapping for API #23 is SOURCE_REQUIRED. |
| lesson_progress.lesson_id | Candidate lesson relationship | DB design links progress row to lessons. | Candidate relationship only; API #23 query is not confirmed. |

### 2.3. Query rules

- Exact lookup query, selected fields, aliases, lock strategy and transaction isolation are SOURCE_REQUIRED.
- No unique constraint on (user_id, lesson_id) is declared in checked-in DDL; do not choose an UPSERT conflict target.
- No query is specified to return the Lesson response payload.
- Checked-in DDL/ERD are not live database metadata.

## 3. Insert/Update thông tin

### 3.1. Target table

- Candidate: lesson_progress (DESIGN_ONLY).
- AC-14 diagram directly states UPSERT lesson progress = IN_PROGRESS.

### 3.2. Conditions

- Candidate identity includes the authenticated Student and lesson_id; exact binding and conflict condition are SOURCE_REQUIRED.
- API #23 request has no client-supplied user_id or progress fields.

### 3.3. Items update/insert

- The only explicitly stated value is status = IN_PROGRESS in AC-14.
- Whether status is written on insert, update, or both is not detailed beyond the UPSERT label.
- Whether progress_percent, last_accessed_at, completed_at, or other fields are set/preserved is SOURCE_REQUIRED.
- Refer to [07_table.md](./07_table.md); it records the candidate write without inventing a SQL statement.

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| lesson_id | Path parameter | Required int64 per catalog; exact range/lookup predicate unresolved. |
| user_id | Authenticated identity | Candidate source from Student JWT; claim and binding unresolved. |
| status | IN_PROGRESS | Directly named by AC-14; persistence mapping is design-only. |

## 4. Check kết quả execute query

### 4.1. Thành công

- Catalog: HTTPStatus = 201; businessCode = DESIGN_RESOURCE_CREATED.
- Map data theo ApiEnvelope<Lesson> của catalog; Lesson projection/query chưa xác nhận.
- AC-14 chỉ xác nhận logical progress state IN_PROGRESS, không định nghĩa Lesson response assembly.

### 4.2. Lỗi hệ thống

- Catalog: HTTPStatus = 500; businessCode = DESIGN_INTERNAL_ERROR.
- Không có runtime API #23 để xác minh exception mapping, rollback hoặc error envelope.

### 4.3. Validate lỗi

- Catalog: HTTPStatus = 422; businessCode = DESIGN_VALIDATION_ERROR.
- Điều kiện validation ngoài path int64 bắt buộc chưa được xác định; không thêm rule.

### 4.4. Lỗi authentication/authorization/resource

- Giữ các mã 401/403/404 của catalog.
- Predicate, resource condition và error payload/message chưa được xác nhận.

### 4.5. Transaction and failure behavior

- API có write side effect theo AC-14, nhưng transaction boundary, atomicity với Lesson response và rollback khi lỗi chưa có nguồn.
- Ghi các quyết định này trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md); không mô tả rollback như hành vi hiện hành.

---
## Phụ lục đối chiếu template Markdown

- Template: [05_Data_Mapping.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md).
- Sheet nguồn: 3. Data mapping.
