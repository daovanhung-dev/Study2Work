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
Mentor Bearer principal -> xác thực role và course scope -> xác nhận student nằm trong learner set được phép của course -> đọc lesson PUBLISHED -> đọc current lesson progress của Student -> dựng summary và detail candidate -> trả contract trực tiếp hoặc contract đã được owner sửa.
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

- Xác thực Bearer JWT và yêu cầu role Mentor theo catalog; Study hiện chưa có Mentor guard.
- Kiểm tra quyền Mentor trên `course_id` trước khi truy vấn/serialize learner progress.
- Kiểm tra `student_id` thuộc cùng enrollment/roster scope mà #65 dùng sau khi policy được phê duyệt.
- Không trả dữ liệu Student chỉ dựa trên hai ID trong path.

### 0.2. Query/check quyền — candidate, chưa phải SQL được duyệt

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| JWT principal | `roles` | Phải có `MENTOR` | Role DIRECT; current helper chỉ yêu cầu STUDENT. |
| Legacy candidate `courses` | `id` | Khớp `course_id` | DDL BIGINT candidate; live schema chưa xác nhận. |
| Legacy candidate `courses` | `mentor_id` | So sánh principal Mentor khi identity mapping được duyệt | Candidate direct-owner; assignment chưa có mapping. |
| Legacy candidate `enrollments` | `course_id`, `user_id` | Student phải thuộc learner set của course | Enrollment status/eligibility giống policy #65, hiện SOURCE_REQUIRED. |
| Legacy candidate `users` | `id`, `role` | Xác minh learner là Student nếu schema được chọn | Candidate; role/identity projection chưa được duyệt. |

### 0.3. Check kết quả

- Nếu thiếu/sai Bearer credential: dùng 401 `DESIGN_AUTHENTICATION_REQUIRED` theo catalog.
- Nếu role hoặc course permission không hợp lệ: dùng 403 `DESIGN_ACCESS_DENIED` theo catalog; predicate cần xác nhận.
- Nếu course hoặc Student/course membership không tồn tại theo policy: 404 là candidate; privacy-aware 403/404 order SOURCE_REQUIRED.
- Không đọc progress cho Student ngoài scope Mentor/course.

<a id="step-1-validate-data-input"></a>

## 1. Validate data input

| Input | Validation trực tiếp | Candidate handling | Trạng thái |
|---|---|---|---|
| `course_id` | Required int64 path | Không thêm positivity/range constraint | DIRECT type; malformed-path behavior chưa xác định. |
| `student_id` | Required int64 path | Không thêm positivity/range constraint | DIRECT type; malformed-path behavior chưa xác định. |
| Query/body | Không khai báo | Không nhận page, size, filter hoặc mutation fields | DIRECT. |

Catalog không khai báo 422 cho API #67. Không tự thêm HTTP/business code cho path parse failure.

<a id="step-2-get-thong-tin"></a>

## 2. Get thông tin

### 2.1. Query candidate

Không có SQL runtime được duyệt. Bảng dưới chỉ nêu field hiện diện trong DDL/API #9; không chọn legacy DDL làm live schema.

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| Legacy `courses AS c` | `c.id` | Candidate course lookup | Course ID int64 trong legacy; pilot dùng UUID. |
| Legacy `courses AS c` | `c.mentor_id` | Candidate direct-owner check | Mentor claim mapping/assignment SOURCE_REQUIRED. |
| Legacy `enrollments AS e` | `e.course_id` | Candidate course membership scope | Status eligibility chưa được chọn. |
| Legacy `enrollments AS e` | `e.user_id` | Candidate Student membership | Không có unique `(course_id,user_id)` trong DDL đã rà soát. |
| Legacy `enrollments AS e` | `e.status` | Candidate membership state | Không tự lọc ACTIVE; cần cùng policy #65. |
| Legacy `users AS u` | `u.id` | Candidate Student identity | Legacy candidate; schema khác pilot. |
| Legacy `users AS u` | `u.full_name` | Candidate UserSummary field | Projection/privacy cần duyệt. |
| Legacy `users AS u` | `u.avatar_url` | Candidate optional UserSummary field | Null/omit policy chưa xác định. |
| API #9 source `lessons AS l` | `l.id` | Lesson ID | Current API #9 source, not #67 runtime. |
| API #9 source `lessons AS l` | `l.course_id` | Course relation | Candidate scope. |
| API #9 source `lessons AS l` | `l.name` | Map to candidate title | API #9 aliases name to title. |
| API #9 source `lessons AS l` | `l.sort_order` | Map to candidate order | API #9 sorts by sort_order then id. |
| API #9 source `lessons AS l` | `l.status` | Candidate PUBLISHED filter | Reuse to match #65 candidate denominator. |
| Legacy `lesson_progress AS lp` | `lp.user_id` | Candidate Student key | DDL nullable; token/path binding unresolved. |
| Legacy `lesson_progress AS lp` | `lp.lesson_id` | Candidate lesson key | DDL nullable; no declared unique user/lesson key. |
| Legacy `lesson_progress AS lp` | `lp.status` | Candidate progress status | Default NOT_STARTED; exhaustive enum unknown. |
| Legacy `lesson_progress AS lp` | `lp.progress_percent` | Candidate per-lesson percent | SMALLINT default 0; range/check not in DDL. |
| Legacy `lesson_progress AS lp` | `lp.last_accessed_at` | Candidate last access timestamp | Nullable in legacy DDL. |
| Legacy `lesson_progress AS lp` | `lp.completed_at` | Candidate completion timestamp | Nullable in legacy DDL. |

### 2.2. JOIN candidate

| Target table | Join condition | Join type | Evidence/status |
|---|---|---|---|
| `courses AS c` | `c.id = :course_id` | BASE/lookup | Legacy candidate only. |
| `enrollments AS e` | `e.course_id = c.id` | Candidate relation | Eligibility and status policy SOURCE_REQUIRED. |
| `users AS u` | `u.id = e.user_id` | Candidate relation | User role/visibility policy SOURCE_REQUIRED. |
| `lessons AS l` | `l.course_id = c.id AND l.status = 'PUBLISHED'` | Candidate lesson set | DIRECT in API #9 current source; DERIVED for #67/#65. |
| `lesson_progress AS lp` | `lp.lesson_id = l.id AND lp.user_id = :student_id` | LEFT JOIN candidate | Legacy relation; duplicate rows, nullable keys and live schema unresolved. |

V1-PILOT alternative uses UUID `course_enrollments` and `lesson_progress_facts`; it has no `progress_percent` in `lesson_progress_facts`. `progress_snapshots` stores aggregate facts but does not provide per-lesson detail. Do not mix these fields with legacy IDs.

### 2.3. WHERE / aggregate

- Candidate course predicate: `course_id` must match the requested course; Mentor authorization must pass first.
- Candidate Student predicate: `student_id` must match the requested learner and the same roster/eligibility policy selected for #65.
- Candidate lesson predicate: `lessons.course_id = course_id` and `lessons.status = 'PUBLISHED'`, matching current API #9 curriculum source.
- Candidate per-lesson progress predicate: `lesson_progress.user_id = student_id` and `lesson_progress.lesson_id = lessons.id`.
- Candidate missing-progress rule: no progress row maps to `NOT_STARTED` and 0 percent; this is DERIVED, not a database default guarantee for absent rows.
- Candidate duplicate-progress rule: SOURCE_REQUIRED; legacy DDL lacks a unique `(user_id, lesson_id)` constraint, so do not aggregate duplicate rows silently.

### 2.4. ORDER BY

- Candidate lesson order: `lessons.sort_order ASC, lessons.id ASC`, matching current API #9 source.
- API #67 does not declare client sort parameters; do not add them.

### 2.5. Summary formula — shared candidate with #65

- `total_lessons` = count of lessons in the PUBLISHED candidate lesson set.
- `completed_lessons` = count of those lessons whose candidate progress status is `COMPLETED`.
- `progress_percent` = floor of sum of per-lesson percent values, treating absent progress as zero, divided by `total_lessons`.
- If `total_lessons = 0`, candidate `completed_lessons = 0` and `progress_percent = 0`.
- This formula matches #65's candidate proposal only; exact state mapping, duplicate handling, denominator and rounding require owner confirmation.

<a id="step-3-insertupdate-thong-tin"></a>

## 3. Insert/Update thông tin

N/A — API #67 is GET/read-only. Không có INSERT/UPDATE/DELETE hoặc transaction được đặc tả.

<a id="step-4-check-ket-qua-execute-query"></a>

## 4. Check kết quả execute query

### 4.1. Thành công

- Direct response: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Page<Course>>`.
- Candidate response after contract approval: `StudentCourseProgress` with one summary and lesson detail list.
- Với Student hợp lệ nhưng chưa có progress state, candidate trả lesson list với 0/NOT_STARTED; không coi trường hợp này là resource không tồn tại.
- Map từng direct field ở [04_Response](./04_Response.md); candidate mapping chỉ áp dụng sau khi contract được sửa.

### 4.2. Lỗi hệ thống

- Lỗi database hoặc mapping ngoài nhánh đã biết: HTTP 500 `DESIGN_INTERNAL_ERROR` theo catalog.
- Không trả SQL, raw DB values hoặc stack trace.

### 4.3. Authentication / authorization / not found

- Giữ code 401/403/404 đúng catalog; trigger và privacy order cho course/student membership cần xác nhận tại [06_Error](./06_Error.md).
- Không thêm 422/409/503.

## Request Usage Matrix

| Request item | Source | Mapping step | Query use | Response use | Gap |
|---|---|---|---|---|---|
| Authorization | Bearer JWT | 0.1 | Mentor course permission | Không trả token/claims | Mentor guard và ID mapping SOURCE_REQUIRED. |
| `course_id` | Path int64 | 1, 2.1–2.3 | Q1/Q2/Q3 | Candidate `course_id` | Live schema/key binding unresolved. |
| `student_id` | Path int64 | 1, 2.1–2.3 | Q2/Q4 | Candidate `student.id` | Must be authorized within course roster. |
| Query/body | N/A | N/A | None | None | Catalog không khai báo. |

## Query Matrix

| Query ID | Mục đích | Type | Candidate source | Predicate/group/order | Status |
|---|---|---|---|---|---|
| Q1 | Kiểm tra course và Mentor scope | SELECT concept | Legacy `courses.id`, `mentor_id` | ID khớp path; owner/assignment rule chưa chốt | DERIVED candidate; live schema/identity SOURCE_REQUIRED. |
| Q2 | Kiểm tra Student thuộc course | SELECT concept | Legacy `enrollments`, `users` | Course + Student; cùng enrollment eligibility với #65 | Status, duplicate, privacy policy SOURCE_REQUIRED. |
| Q3 | Lấy curriculum làm denominator | SELECT concept | API #9 source `lessons` | Course + PUBLISHED; order `sort_order,id` | Current source for #9; DERIVED reuse in #65/#67. |
| Q4 | Đọc progress hiện trạng từng lesson | SELECT concept | Legacy `lesson_progress` | Student + lesson; resolve duplicate state before aggregate | DDL candidate only; not an approved query. |
| Q5 | Tính progress summary | Aggregate | Q3 + Q4 candidate rows | Count completed; floor average; zero on empty denominator | DERIVED, must match #65 if approved. |

## Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | Read-only GET | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## Response Source Matrix

| Response field | Contract/candidate type | Candidate source | Mapping rule | Evidence/status |
|---|---|---|---|---|
| `success` | boolean | ApiEnvelope<T> | Envelope success flag | DIRECT schema; endpoint unwired. |
| `businessCode` | string | Catalog | `DESIGN_RESOURCE_RETRIEVED` on success | DIRECT. |
| `message` | string | Application message | Exact text unspecified | SOURCE_REQUIRED. |
| `data.items[]` | Course[] | Catalog Course | Preserve direct type | DIRECT; no progress fields. |
| `data.pagination` | PageMeta | Catalog | page, size, total, total_pages | DIRECT; request lacks pagination inputs. |
| `meta` | object | ApiEnvelope<T> | Metadata object | DIRECT; fields unspecified. |
| `traceId` | uuid | Request trace | Per shared envelope contract | DIRECT schema; route absent. |
| Candidate `course_id` | int64 | Path/course relation | Echo requested authorized course | DERIVED; candidate shape only. |
| Candidate `student` | UserSummary | Enrolled Student row | Minimum identity fields only | DERIVED; projection/privacy SOURCE_REQUIRED. |
| Candidate `summary.completed_lessons` | int32 | Progress status rows | Count COMPLETED in same published denominator as #65 | DERIVED; enum/schema unresolved. |
| Candidate `summary.total_lessons` | int32 | PUBLISHED lesson rows | Count course curriculum rows | DERIVED from API #9 current source. |
| Candidate `summary.progress_percent` | int32 | Per-lesson percent state | Same floor-average proposal as #65 | DERIVED; rounding/range unresolved. |
| Candidate `lessons[].lesson_id` | int64 | Legacy `lessons.id` | One row per published lesson | Candidate; pilot UUID conflict. |
| Candidate `lessons[].title` | string | Legacy `lessons.name` | `name → title` | Candidate from API #9 source. |
| Candidate `lessons[].order` | int32 | Legacy `lessons.sort_order` | `sort_order → order` | Candidate from API #9 source. |
| Candidate `lessons[].progress_status` | string | Legacy `lesson_progress.status` | Missing row → NOT_STARTED proposal | DERIVED; enum and missing-row behavior unresolved. |
| Candidate `lessons[].progress_percent` | int32 | Legacy `lesson_progress.progress_percent` | Missing row → 0 proposal | DERIVED; DDL SMALLINT and no range check. |
| Candidate `lessons[].last_accessed_at` | date-time? | Legacy `lesson_progress.last_accessed_at` | Null when absent | DDL candidate; serialization unresolved. |
| Candidate `lessons[].completed_at` | date-time? | Legacy `lesson_progress.completed_at` | Null when absent | DDL candidate; serialization unresolved. |

## Mapping tables and relations

### Legacy BIGINT candidate

| Relation | Fields used | Status |
|---|---|---|
| `courses` | `id`, `mentor_id` | Checked-in DDL candidate; live schema/authorization unresolved. |
| `enrollments` | `course_id`, `user_id`, `status` | Checked-in DDL candidate; eligibility/uniqueness unresolved. |
| `users` | `id`, `full_name`, `avatar_url`, `role` | Checked-in DDL candidate; privacy/projection unresolved. |
| `lessons` | `id`, `course_id`, `name`, `sort_order`, `status` | Checked-in DDL candidate; API #9 source filters PUBLISHED. |
| `lesson_progress` | `user_id`, `lesson_id`, `status`, `progress_percent`, `last_accessed_at`, `completed_at` | Checked-in DDL candidate; no unique user/lesson key. |

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
