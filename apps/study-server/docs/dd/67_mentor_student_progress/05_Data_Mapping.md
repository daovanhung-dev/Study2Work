---
title: "Data Mapping"
order: 5
dd_id: "67"
api_name: "Lấy tiến độ Student"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

```text
Mentor Bearer principal -> shared MENTOR guard -> direct course-owner check -> active Student-roster check -> đọc lesson PUBLISHED và latest current progress -> dựng summary/detail response fallback -> trả envelope.
```

# Mục lục

- [0. Check quyền](#step-0-check-quyen)
- [1. Validate data input](#step-1-validate-data-input)
- [2. Get thông tin](#step-2-get-thong-tin)
- [3. Insert/Update thông tin](#step-3-insertupdate-thong-tin)
- [4. Check kết quả execute query](#step-4-check-ket-qua-execute-query)
- [Request Usage Matrix](#request-usage-matrix)
- [Query Matrix](#query-matrix)
- [Mutation Matrix](#mutation-matrix)
- [Response Source Matrix](#response-source-matrix)

<a id="step-0-check-quyen"></a>

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Xác thực Bearer/JWT và role Mentor bằng `validate_current_user_request(..., role="MENTOR")` trước mọi query.
- Kiểm tra `courses.mentor_id = principal sub` trước Student lookup theo local direct-owner pattern của #65/#66.
- Kiểm tra `student_id` có `enrollments.status = 'ACTIVE'` và `users.role = 'STUDENT'` trong course đó như roster #65.
- Không trả dữ liệu Student chỉ dựa trên hai ID trong path.

### 0.2. Query/check quyền — runtime SQL theo DERIVED fallback

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | `roles`, `sub` | Phải có `MENTOR`; `sub` dùng làm Mentor ID | Shared MENTOR guard là current source; `sub → courses.mentor_id` là DERIVED theo #65/#66. |
| Legacy `courses` | `id` | Khớp `course_id` | Current SQL source; live schema chưa xác nhận. |
| Legacy `courses` | `mentor_id` | So sánh với numeric principal `sub` | Runtime fallback direct-owner theo #65/#66; business approval chưa xác nhận. |
| Legacy `enrollments` | `course_id`, `user_id`, `status` | `course_id` và `user_id` khớp; `status = 'ACTIVE'` | Runtime dùng cùng roster predicate của #65; live schema chưa xác nhận. |
| Legacy `users` | `id`, `role`, `full_name`, `avatar_url` | `role = 'STUDENT'`; trả identity tối thiểu | Runtime projection; `avatar_url` nullable; privacy approval chưa xác nhận. |

### 0.3. Check kết quả

- Nếu thiếu/sai Bearer credential: dùng 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog.
- Nếu role sai hoặc Mentor không sở hữu course: trả 403 `DESIGN_ACCESS_DENIED` theo catalog.
- Nếu course không tồn tại hoặc Student không có trong active roster: trả 404 `DESIGN_RESOURCE_NOT_FOUND` theo fallback privacy hiện implement.
- Không đọc progress cho Student ngoài scope Mentor/course.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

| Input | Validation trực tiếp | Candidate handling | Trạng thái |
|---|---|---|---|
| `course_id` | Required int64 path | Raw signed-int64 parse; lỗi parse → 404 | DIRECT type; mapping 404 là runtime fallback theo #65. |
| `student_id` | Required int64 path | Raw signed-int64 parse; lỗi parse → 404 | DIRECT type; mapping 404 là runtime fallback theo #65/#66. |
| Query/body | Không khai báo | Không nhận page, size, filter hoặc mutation fields | DIRECT. |

Catalog không khai báo 422 cho API #67. Không tự thêm HTTP/business code cho path parse failure.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Query source hiện implement

`query.py` có SQL constants dùng legacy BIGINT field set giống #65/#66. Đây là current runtime source nhưng không chứng minh live schema/deployment.

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy `courses AS c` | `c.id` | Course lookup | Course ID int64 trong legacy; pilot dùng UUID. |
| Legacy `courses AS c` | `c.mentor_id` | Direct-owner check | Runtime so sánh numeric `sub`; mapping là DERIVED theo #65/#66. |
| Legacy `enrollments AS e` | `e.course_id` | Student membership scope | Runtime lọc theo course; DDL không có unique `(course_id,user_id)`. |
| Legacy `enrollments AS e` | `e.user_id` | Student membership | Runtime lọc theo `student_id` path. |
| Legacy `enrollments AS e` | `e.status` | Chỉ chọn membership `ACTIVE` | Cùng predicate runtime #65. |
| Legacy `users AS u` | `u.id` | Student identity | Legacy candidate; schema khác pilot. |
| Legacy `users AS u` | `u.full_name` | UserSummary field | Runtime projection; privacy approval pending. |
| Legacy `users AS u` | `u.avatar_url` | Optional UserSummary field | Runtime giữ JSON null; live privacy policy chưa xác nhận. |
| Legacy `lessons AS l` | `l.id` | Lesson ID | Current API #67 SQL source; API #9 uses same relation. |
| Legacy `lessons AS l` | `l.course_id` | Course relation | Runtime lesson scope. |
| Legacy `lessons AS l` | `l.name` | Map to `title` | Same alias as current API #9 source. |
| Legacy `lessons AS l` | `l.sort_order` | Map to `order` | API #67 orders by sort_order then id, as API #9. |
| Legacy `lessons AS l` | `l.status` | PUBLISHED filter | Same lesson eligibility source as #9/#65. |
| Legacy `lesson_progress AS lp` | `lp.user_id` | Lọc theo `student_id` path | Current query source; physical live schema unresolved. |
| Legacy `lesson_progress AS lp` | `lp.lesson_id` | Nối với `lessons.id` | DDL không khai báo unique user/lesson. |
| Legacy `lesson_progress AS lp` | `lp.status` | Trả current state; absent row thành `NOT_STARTED` | Enum được runtime giới hạn ở 3 trạng thái như #65. |
| Legacy `lesson_progress AS lp` | `lp.progress_percent` | Trả per-lesson percent; absent row thành 0 | Runtime kiểm tra 0–100 như #65. |
| Legacy `lesson_progress AS lp` | `lp.last_accessed_at` | Trả thời điểm truy cập cuối | Nullable; dùng tie-break row latest. |
| Legacy `lesson_progress AS lp` | `lp.completed_at` | Trả thời điểm hoàn thành | Nullable; giữ JSON null. |

### 2.2. JOIN candidate

| Target table | Join condition | Join type | Evidence/status |
|---|---|---|---|
| `courses AS c` | `c.id = :course_id` | BASE/lookup | Legacy candidate only. |
| `enrollments AS e` | `e.course_id = c.id` | Runtime relation | `ACTIVE` plus requested user. |
| `users AS u` | `u.id = e.user_id` | Runtime relation | `role='STUDENT'`; visibility policy beyond role is not modeled. |
| `lessons AS l` | `l.course_id = c.id AND l.status = 'PUBLISHED'` | Runtime lesson set | Current API #9 source also filters PUBLISHED; reuse in #67 is DERIVED. |
| `lesson_progress AS lp` | `lp.lesson_id = l.id AND lp.user_id = :student_id` | LEFT JOIN latest row | Runtime `DISTINCT ON`; sort timestamp desc nulls-last then ID desc, như #65. |

V1-PILOT alternative uses UUID `course_enrollments` and `lesson_progress_facts`; it has no `progress_percent` in `lesson_progress_facts`. `progress_snapshots` stores aggregate facts but does not provide per-lesson detail. Do not mix these fields with legacy IDs.

### 2.3. WHERE / aggregate

- Course predicate: `courses.id = course_id`; direct owner check runs before roster/progress access.
- Student predicate: requested user must have ACTIVE enrollment in the course and `users.role='STUDENT'`, following current #65.
- Lesson predicate: `lessons.course_id = course_id` and `lessons.status = 'PUBLISHED'`.
- Per-lesson progress predicate: `lesson_progress.user_id = student_id` and `lesson_progress.lesson_id = lessons.id`.
- Missing-progress rule: no progress row maps to `NOT_STARTED` and 0 percent; this is implemented DERIVED behavior, not a database default guarantee.
- Duplicate progress rule: choose latest `last_accessed_at DESC NULLS LAST`, then `id DESC`, matching the current #65 query; the DDL still lacks a unique `(user_id, lesson_id)` constraint.

### 2.4. ORDER BY

- Runtime lesson order: `lessons.sort_order ASC, lessons.id ASC`, matching current API #9 source.
- API #67 does not declare client sort parameters; do not add them.

### 2.5. Summary formula — shared DERIVED fallback with #65

- `total_lessons` = count of returned PUBLISHED lessons.
- `completed_lessons` = count of those lessons whose selected progress status is `COMPLETED`.
- `progress_percent` = floor of sum of per-lesson percent values, treating absent progress as zero, divided by `total_lessons`.
- If `total_lessons = 0`, runtime returns `completed_lessons = 0` and `progress_percent = 0`.
- Current #67 implementation matches current #65 source: COMPLETED count, per-lesson percent arithmetic mean, floor rounding and zero for an empty denominator. These remain DERIVED business rules pending owner approval.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

N/A — API #67 is GET/read-only. Không có INSERT/UPDATE/DELETE hoặc transaction được đặc tả.

<a id="step-4-check-ket-qua-execute-query"></a>

## 4. Check kết quả execute query

### 4.1. Thành công

- Direct diagram/catalog response: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Page<Course>>`.
- Current local fallback: `StudentCourseProgress` với identity, summary và ordered lesson detail.
- Với Student hợp lệ nhưng chưa có progress row, runtime trả `NOT_STARTED`/0 và hai timestamp null; không coi trường hợp này là resource không tồn tại.
- Map response theo [04_Response](./04_Response.md); singular shape là DERIVED và đang lệch direct diagram/catalog contract.

### 4.2. Lỗi hệ thống

- Lỗi database hoặc mapping ngoài nhánh đã biết: HTTP 500 `DESIGN_INTERNAL_ERROR` theo catalog.
- Không trả SQL, raw DB values hoặc stack trace.

### 4.3. Authentication / authorization / not found

- Giữ code 401/403/404 đúng catalog; fallback hiện trả 403 cho course khác owner và 404 cho course/Student không tìm thấy trong scope; xem [06_Error](./06_Error.md).
- Không thêm 422/409/503.

## Request Usage Matrix

| Request item | Source | Mapping step | Query use | Response use | Gap |
|---|---|---|---|---|---|
| Authorization | Bearer JWT | 0.1 | Shared role guard and direct owner check | Không trả token/claims | `MENTOR` helper current; owner predicate DERIVED from #65/#66. |
| `course_id` | Path int64 | 1, 2.1–2.3 | Q1/Q2/Q3 | Runtime `course_id` | Raw signed-int64; live schema unresolved. |
| `student_id` | Path int64 | 1, 2.1–2.3 | Q2/Q3 | Runtime `student.id` | ACTIVE roster membership required; live schema unresolved. |
| Query/body | N/A | N/A | None | None | Catalog không khai báo. |

## Query Matrix

| Query ID | Mục đích | Type | Candidate source | Predicate/group/order | Status |
|---|---|---|---|---|---|
| Q1 | Kiểm tra course và Mentor scope | SELECT runtime | Legacy `courses.id`, `mentor_id` | Course ID bằng path; owner lookup trước roster | Current source; live schema/identity policy unverified. |
| Q2 | Kiểm tra Student thuộc active roster | SELECT runtime | Legacy `enrollments`, `users` | Course + Student; ACTIVE + STUDENT | Current #65-compatible fallback; privacy approval pending. |
| Q3 | Lấy lesson set và current state | SELECT runtime | Legacy `lessons`, `lesson_progress` | PUBLISHED; progress theo Student; `sort_order,id`; latest timestamp/id | Current source; schema live unverified. |
| Q4 | Tính progress summary | Runtime aggregate in view | Q3 mapped lesson rows | Completed count; floor average; zero khi denominator rỗng | DERIVED; khớp #65 local source. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only GET | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract/candidate type | Candidate source | Mapping rule | Evidence/status |
|---|---|---|---|---|
| `success` | boolean | ApiEnvelope<T> | Envelope success flag | DIRECT schema; route is wired. |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` on success | DIRECT. |
| `message` | string | Application message | Runtime success: `Student progress retrieved.` | Direct catalog text unspecified; current local message is DERIVED. |
| `data.items[]` | Course[] | Catalog Course | Preserve direct type | DIRECT contract; not the current local response. |
| `data.pagination` | PageMeta | Catalog | page, size, total, total_pages | DIRECT contract; request lacks pagination inputs. |
| `meta` | object | ApiEnvelope<T> | Metadata object | DIRECT; fields unspecified. |
| `traceId` | uuid | Request trace | Per shared envelope contract | DIRECT schema; current route propagates trace ID. |
| Runtime `course_id` | int64 | Path | Echo authorized course path | DERIVED response shape; current module source. |
| Runtime `student` | UserSummary | Active Student row | id, full_name, nullable avatar_url | DERIVED projection; privacy approval pending. |
| Runtime `summary.completed_lessons` | int32 | Mapped progress states | Count COMPLETED in published lesson set | DERIVED; same local rule as #65. |
| Runtime `summary.total_lessons` | int32 | Published lesson rows | Number of returned lessons | DERIVED from API #9/current #65 source. |
| Runtime `summary.progress_percent` | int32 | Per-lesson percentages | Floor arithmetic mean; zero if no lessons | DERIVED; same local rule as #65. |
| Runtime `lessons[].lesson_id` | int64 | Legacy `lessons.id` | One row per PUBLISHED lesson | Current query source; live schema unverified. |
| Runtime `lessons[].title` | string | Legacy `lessons.name` | `name → title` | Current API #9 alias pattern. |
| Runtime `lessons[].order` | int | Legacy `lessons.sort_order` | `sort_order → order` | Current API #9 ordering field. |
| Runtime `lessons[].progress_status` | enum string | Legacy `lesson_progress.status` | Missing row → NOT_STARTED | DERIVED; runtime allows 3 states used by #65. |
| Runtime `lessons[].progress_percent` | int | Legacy `lesson_progress.progress_percent` | Missing row → 0; require 0–100 | DERIVED and checked by view. |
| Runtime `lessons[].last_accessed_at` | date-time? | Legacy `lesson_progress.last_accessed_at` | Null when absent | Current serialization keeps null; live schema unverified. |
| Runtime `lessons[].completed_at` | date-time? | Legacy `lesson_progress.completed_at` | Null when absent | Current serialization keeps null; live schema unverified. |

## Mapping tables and relations

### Legacy BIGINT candidate

| Relation | Fields used | Status |
|---|---|---|
| `courses` | `id`, `mentor_id` | Checked-in DDL candidate; live schema/authorization unresolved. |
| `enrollments` | `course_id`, `user_id`, `status` | Checked-in DDL candidate; eligibility/uniqueness unresolved. |
| `users` | `id`, `full_name`, `avatar_url`, `role` | Checked-in DDL candidate; privacy/projection unresolved. |
| `lessons` | `id`, `course_id`, `name`, `sort_order`, `status` | Checked-in DDL candidate; API #9 source filters PUBLISHED. |
| `lesson_progress` | `id`, `user_id`, `lesson_id`, `status`, `progress_percent`, `last_accessed_at`, `completed_at` | Current query source; checked-in DDL has no unique user/lesson key; latest timestamp/id is selected as in #65. |

### V1-PILOT UUID alternative

- `course_enrollments` keys learners to course versions with UUID IDs.
- `lesson_progress_facts` is per enrollment/lesson, has status/timestamps but no `progress_percent` column.
- `progress_snapshots` stores course-version aggregate counts/percent, not per-lesson detail.
- Do not combine the V1-PILOT facts with legacy BIGINT path IDs or columns; schema selection is SOURCE_REQUIRED.

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `3. Data mapping`
- Dimension: `B1:BB61`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `63`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Flow xử lý data |  |
| 4 | `D4` | 0. |  |
| 4 | `E4` | Check quyền |  |
| 5 | `E5` | ・ |  |
| 5 | `F5` | Thực hiện check quyền |  |
| 6 | `E6` | ・ |  |
| 6 | `F6` | Get count khi get data từ … |  |
| 7 | `G7` | Table get |  |
| 7 | `K7` | : |  |
| 8 | `G8` | Conditions |  |
| 8 | `K8` | : |  |
| 10 | `E10` | ・ |  |
| 10 | `F10` | Trường hợp giá trị get được lớn hơn 0, thực hiện các xử lý tiếp theo |  |
| 11 | `E11` | ・ |  |
| 11 | `F11` | Trường hợp giá trị get được bằng 0, trả về status 2 |  |
| 13 | `D13` | 1. |  |
| 13 | `E13` | validate data input |  |
| 14 | `F14` | refer sheet [４．Error] |  |
| 16 | `D16` | 2. |  |
| 16 | `E16` | Get thông tin… |  |
| 18 | `F18` | Table get |  |
| 18 | `K18` | Column get |  |
| 18 | `P18` | Chú thích |  |
| 18 | `U18` | Remarks |  |
| 29 | `F29` | Target table / join condition |  |
| 30 | `F30` | Target table |  |
| 30 | `N30` | Join condition |  |
| 30 | `AL30` | 結合種類 |  |
| 31 | `F31` | txn_ams_t0320 AS a |  |
| 32 | `F32` | txn_amm_v0002 AS b |  |
| 32 | `N32` | ON a . chy_typ = b . kbn_typ AND b . dmin_cd = A AND b . kbnknr_cd = 001 |  |
| 32 | `AL32` | LEFT JOIN |  |
| 33 | `F33` | txn_amm_v0002 AS c |  |
| 33 | `N33` | ON a . chy_typ = c . kbn_typ AND c . dmin_cd = A AND c . kbnknr_cd = Z02 |  |
| 33 | `AL33` | LEFT JOIN |  |
| 35 | `F35` | ・ |  |
| 35 | `G35` | Điều kiện get data |  |
| 37 | `F37` | ・ |  |
| 37 | `G37` | Điều kiện sort |  |
| 41 | `D41` | 3. |  |
| 41 | `E41` | Insert/Update thông tin … |  |
| 42 | `E42` | Update table…. |  |
| 43 | `E43` | ・ |  |
| 43 | `F43` | Items update |  |
| 44 | `F44` | ・ |  |
| 44 | `G44` | Refer sheet [xxxx] |  |
| 45 | `E45` | ・ |  |
| 45 | `F45` | Điều kiện get data |  |
| 46 | `F46` | ・ |  |
| 46 | `G46` | auth_user. id = user hiện tại theo token |  |
| 48 | `D48` | 4. |  |
| 48 | `E48` | check kết quả execute query  |  |
| 49 | `E49` | 1. Thành công |  |
| 50 | `F50` | HTTPStatus = 200 |  |
| 51 | `F51` | Trả về kết quả status = 1 |  |
| 52 | `E52` | 2. Lỗi hệ thống phát sinh |  |
| 53 | `F53` | HTTPStatus = 500 |  |
| 54 | `F54` | Trả về kết quả status = 2 |  |
| 55 | `E55` | 3. Validate lỗi |  |
| 56 | `F56` | HTTPStatus = 400 |  |
| 57 | `F57` | Trả về kết quả status = 2 |  |
| 58 | `E58` | 4. Ngoài trường hợp trên |  |
| 59 | `F59` | Trả về kết quả status = 2 |  |

</details>
