---
title: "Data Mapping"
order: 5
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Contract yêu cầu Student Bearer JWT; API #22 chưa có route gọi shared auth helper.
1. Đọc path lesson_id:int64!; không có query hoặc body được khai báo.
2. AC-14 yêu cầu kiểm tra enrollment/prerequisite; access predicate, identity binding và query chưa được định nghĩa.
3. Nếu bị từ chối, AC-14 ghi HTTP 403 + lý do; catalog code là DESIGN_ACCESS_DENIED, còn lý do chưa có wire schema.
4. Nếu được phép, catalog quy định HTTP 200 DESIGN_RESOURCE_RETRIEVED với ApiEnvelope<Lesson>.
5. Catalog khai báo HTTP 404 DESIGN_RESOURCE_NOT_FOUND; resource condition chưa được xác định.
6. Lỗi nội bộ dùng HTTP 500 DESIGN_INTERNAL_ERROR; không có runtime API #22 để xác minh mapping.
7. API #22 là GET; không có mutation/transaction nào được mô tả. API #23 start là endpoint riêng.
~~~

<a id="0-check-quyen"></a>

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Design contract yêu cầu Bearer JWT và role Student.
- AC-14 nêu kiểm tra enrollment/prerequisite trước khi tiếp tục luồng học.
- Current [auth.py](../../../app/utils/auth.py) có shared helper đọc Bearer/JWT, chuẩn hóa `sub` thành numeric user ID và yêu cầu role STUDENT; API #22 chưa gọi helper này.
- API-specific binding giữa JWT subject và `enrollments.user_id` chưa được xác nhận.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| Authorization header | Bearer JWT | Required; actor role Student | Design contract; API #22 runtime chưa wired. |
| JWT claims | `sub`, `roles` | Current helper parses numeric `sub` and requires STUDENT | Shared source behavior; endpoint-specific use is not verified. |
| `enrollments` — candidate | `user_id`, `course_id`, `status` | Predicate/status selection SOURCE_REQUIRED | Checked-in DB design only; do not infer active-state rule. |
| Prerequisite source | SOURCE_REQUIRED | SOURCE_REQUIRED | AC-14 names prerequisite but no model/rule is specified. |

### 0.3. Check kết quả

- Nếu authentication thất bại, contract khai báo HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Nếu role/access bị từ chối, contract khai báo HTTP 403 `DESIGN_ACCESS_DENIED`; AC-14 ghi thêm “lý do” chưa có wire definition.
- Không kết luận API #22 đang thực thi các checks này; endpoint hiện `UNWIRED / NOT_FOUND`.

<a id="1-request-usage-and-validation"></a>

## 1. Request usage and validation

| Request field | Nguồn | Data Mapping step | Validate | SQL/Mutation usage | Branch/Loop | Response usage | Gap |
|---|---|---|---|---|---|---|---|
| Authorization | HTTP header | 0 | Bearer JWT; role Student theo contract | Candidate identity input cho access check; API #22 chưa binding vào query | Authentication/authorization | N/A | Claim-to-enrollment binding SOURCE_REQUIRED. |
| lesson_id | Path parameter | 1 | int64 bắt buộc theo catalog; range thêm chưa được xác định | Candidate định danh lesson; exact query SOURCE_REQUIRED | Lesson lookup/access check | Lesson schema on success | 404 condition và invalid-path wire behavior chưa được quy định. |
| Query parameters | N/A | 1 | N/A | N/A | N/A | N/A | Catalog không khai báo query parameters. |
| Request body | N/A | 1 | N/A | N/A | N/A | N/A | Catalog không khai báo request body. |

## 2. Get thông tin

### 2.1. Query matrix

| Query ID | Mục đích | Type | Base table/view | Alias | Columns | JOIN | WHERE | GROUP/HAVING | ORDER | Pagination | Result variable | Branch |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Q1 | Kiểm tra access và cung cấp Lesson nếu được phép | SELECT — DESIGN_ONLY; exact query SOURCE_REQUIRED | Candidate: `lessons`, `enrollments` | SOURCE_REQUIRED | Lesson response schema fields; API #22 projection SOURCE_REQUIRED | SOURCE_REQUIRED | Enrollment/prerequisite predicate SOURCE_REQUIRED | N/A | N/A | N/A | `access_result` — logical placeholder | Allowed/denied/not found semantics require confirmation. |

### 2.2. Candidate schema references

| Target table | Column/relationship | Evidence | Status |
|---|---|---|---|
| `lessons` | `id`, `course_id`, `name`, `content`, `video_url`, `sort_order`, `status` | Checked-in `DB.sql` and `DB_UNICA_TABLES.md`; logical Lesson mapping is documented for API #9. | DESIGN_ONLY; API #22 query not confirmed. |
| `enrollments` | `user_id`, `course_id`, `status` | Checked-in `DB.sql` and `DB_UNICA_TABLES.md`; AC-14 precondition requires enrollment. | DESIGN_ONLY; status and selection predicates not confirmed. |
| `lessons.course_id` → `courses.id` | Parent-course relationship | Checked-in DDL/ERD. | Schema design relationship only; not a confirmed API #22 JOIN. |
| Prerequisite data | SOURCE_REQUIRED | AC-14 diagram names prerequisite but DB/API source does not define its model for API #22. | SOURCE_REQUIRED. |

### 2.3. Query rules

- Exact selected columns, table aliases and query ordering are SOURCE_REQUIRED for API #22.
- Enrollment status values and the status eligible for access are SOURCE_REQUIRED.
- Prerequisite model, lookup and evaluation rule are SOURCE_REQUIRED.
- `404 DESIGN_RESOURCE_NOT_FOUND` is declared, but the missing resource/visibility condition is SOURCE_REQUIRED.
- No SQL text or access predicate is specified in this draft.

## 3. Mutation matrix

| Mutation ID | Operation | Target table | Record condition | Fields | Value sources | Audit | Mapping file | Transaction | Failure behavior |
|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A — GET; no mutation is described | N/A | N/A | N/A | N/A | N/A | [07_table.md](./07_table.md) | N/A | API #23 lesson start is a separate endpoint. |

## 4. Response source matrix

| Response field | Type | Source type | Table/column or generator | Data Mapping step | Transform | Null/empty rule | Gap |
|---|---|---|---|---|---|---|---|
| success | boolean | ApiEnvelope schema | ApiEnvelope<T>.success | 4.1–4.4 | Per shared schema | N/A | API #22 runtime serialization not verified. |
| businessCode | string | API catalog | Contract code by branch | 4.1–4.4 | Fixed by branch | N/A | Preserve catalog codes. |
| message | string | Message source | SOURCE_REQUIRED | 4.1–4.4 | SOURCE_REQUIRED | N/A | Message text unspecified. |
| data | Lesson | API catalog schema | ApiEnvelope<Lesson> | 3/4.1 | Contract generic type | Error shape unspecified | No access decision field is declared. |
| data.id | int64 | Reusable Lesson schema | Candidate `lessons.id` | 3/4.1 | Direct candidate mapping | Required by schema | API #22 SELECT not confirmed. |
| data.course_id | int64 | Reusable Lesson schema | Candidate `lessons.course_id` | 3/4.1 | Direct candidate mapping | Required by schema | API #22 SELECT not confirmed. |
| data.title | string | Reusable Lesson schema | Candidate `lessons.name` | 3/4.1 | `name` → `title` per DB design | Required by schema | API #22 SELECT not confirmed. |
| data.content | string, optional | Reusable Lesson schema | Candidate `lessons.content` | 3/4.1 | Direct candidate mapping | Null/omit unspecified | Optional schema field. |
| data.video_url | uri, optional | Reusable Lesson schema | Candidate `lessons.video_url` | 3/4.1 | Direct candidate mapping | Null/omit unspecified | Optional schema field. |
| data.order | int32 | Reusable Lesson schema | Candidate `lessons.sort_order` | 3/4.1 | `sort_order` → `order` per DB design | Required by schema | API #22 SELECT not confirmed. |
| data.status | LessonStatus | Reusable Lesson schema | Candidate `lessons.status` | 3/4.1 | Direct candidate mapping | Required by schema | Enum values unspecified. |
| meta | object | ApiEnvelope schema | ApiEnvelope<T>.meta | 4.1–4.4 | Per shared schema | Members unspecified | No API #22 metadata fields declared. |
| traceId | uuid | ApiEnvelope schema | ApiEnvelope<T>.traceId | 4.1–4.4 | UUID per schema | Required by schema | API #22 runtime trace behavior not verified. |

## 5. Check result and return response

### 5.1. Thành công

- HTTP status = 200.
- businessCode = `DESIGN_RESOURCE_RETRIEVED`.
- Response type = `ApiEnvelope<Lesson>` per catalog.
- Candidate lesson-column mapping is design evidence only; API #22 query is unresolved.

### 5.2. Authentication/authorization errors

- HTTP status = 401; businessCode = `DESIGN_AUTHENTICATION_REQUIRED`.
- HTTP status = 403; businessCode = `DESIGN_ACCESS_DENIED`.
- AC-14 says denial includes a reason; response field/message location remains unresolved.

### 5.3. Not found and system error

- HTTP status = 404; businessCode = `DESIGN_RESOURCE_NOT_FOUND`; exact condition is unresolved.
- HTTP status = 500; businessCode = `DESIGN_INTERNAL_ERROR`.
- Do not return raw SQL errors, stack traces or internal details.

---
## Phụ lục đối chiếu template Markdown

- Template: [05_Data_Mapping.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/05_Data_Mapping.md).
- Sheet nguồn: 3. Data mapping.
