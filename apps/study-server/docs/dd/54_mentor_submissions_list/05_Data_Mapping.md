---
title: "Data Mapping"
order: 5
dd_id: "54"
api_name: "Lấy submissions"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
Mentor Bearer JWT
-> validate role MENTOR and numeric subject
-> if course_id supplied, check direct owner (courses.mentor_id)
-> COUNT submissions in Mentor-owned courses with supplied filters
-> SELECT one stable page (submitted_at DESC, id DESC; fixed size 20)
-> resolve at most one UploadAsset by exact file_url + owner + purpose + course
-> map each Submission and PageMeta
-> return ApiEnvelope<Page<Submission>>
~~~

Fallback pagination/cardinality and upload URL association are DERIVED; source artifacts and test DB do not establish live deployment.

## Request Usage Matrix

| Request field | Source | Step | Validation | Query/response use | Gap/status |
|---|---|---:|---|---|---|
| Authorization | Header | 0.1 | Shared JWT guard; role MENTOR | Numeric subject scopes every row | DIRECT guard shape; assigned Mentor SOURCE_REQUIRED |
| course_id | Optional query | 1/2 | Positive signed-int64 | Optional assignment course filter; direct-owner precheck | DERIVED direct owner; missing course returns empty page |
| status | Optional query | 1/2 | Raw optional string | Exact `s.status = :status` filter | No enum or normalization rule |
| page | Optional query | 1/4 | Positive int32 | OFFSET `(page-1)*20`; returned in pagination | Default 1 and size 20 are DERIVED from shared catalog convention |
| Request body | None | N/A | N/A | N/A | Catalog does not declare body |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Call `validate_current_user_request(..., role="MENTOR")` before reading submissions.
- JWT `sub` is numeric user ID per current shared helper.
- With `course_id`, query the course and compare `courses.mentor_id` to the authenticated ID; an existing owner mismatch returns 403.
- Without `course_id`, every data query scopes through `courses.mentor_id = :mentor_id`.
- Assigned-Mentor relationships are not represented and are not included.

### 0.2. Query/check quyền

| Target | Condition | Purpose | Status |
|---|---|---|---|
| `courses` | `id = :course_id` | Load an explicitly requested course | Direct source query pattern |
| `courses` | `mentor_id = :mentor_id` | Restrict course access | Existing API #46/#49 pattern; DERIVED for #54 |
| `assignments` | `a.course_id = c.id` | Find course scope from assignment | ERD relation; DDL allows NULL, inner join excludes it |
| `assignment_submissions` | `s.assignment_id = a.id` | Find submissions | ERD relation; DDL allows NULL, inner join excludes it |
| `users` | `student.id = s.user_id` | Require a valid Student FK for response | DDL FK candidate; null/orphan rows excluded |

### 0.3. Check result

- Missing/invalid Bearer or claims: 401.
- Non-Mentor role or existing course owned by another Mentor: 403.
- Missing `course_id` target and no matching submissions: 200 with empty `items` and zero totals; API #54 catalog has no 404.

## 1. Validate data input

- `course_id`: optional positive int64; malformed, zero, negative or overflow query value maps through the shared request-validation handler to 422 `DESIGN_VALIDATION_ERROR`.
- `status`: optional string matched exactly; no enum, casing, trimming or whitespace rule is added.
- `page`: optional positive int32, default 1; size is not client configurable and uses shared `DEFAULT_SIZE=20`.
- `page < 1` or values outside int32 map to 422 `DESIGN_VALIDATION_ERROR`; this is added to the catalog/diagram for the implemented query constraint.

## 2. Get thông tin

### 2.1. Q0 — course owner precheck

`FIND_MENTOR_COURSE` selects `id, mentor_id` by `course_id`. Existing course with another owner returns 403 before list data is read. Missing course continues to the count/list query and yields an empty page.

### 2.2. Q1 — COUNT

`COUNT_MENTOR_SUBMISSIONS` joins `assignment_submissions` → `assignments` → `courses` → `users`, scopes by `c.mentor_id`, and applies optional `course_id` and exact `status` filters. No upload join is used in the count.

### 2.3. Q2 — LIST

`LIST_MENTOR_SUBMISSIONS` uses the same base joins and predicates, orders by `s.submitted_at DESC, s.id DESC`, and binds `LIMIT 20` plus `OFFSET (page-1)*20`.

### 2.4. Q3 — asset projection

A lateral lookup matches `uploads.url = s.file_url`, `uploads.owner_id = s.user_id`, `uploads.purpose = 'SUBMISSION'` and `uploads.course_id = a.course_id`, ordered by upload ID and limited to one. This is a DERIVED association: `assignment_submissions.file_url` has no FK to `uploads` and API #35 file-ref encoding is unresolved. No match returns `files: []`; a partial projection is rejected as an internal mapping error.

### 2.5. Query matrix

| Query ID | Purpose | Type | Tables | Conditions | Order/pagination | Result |
|---|---|---|---|---|---|---|
| Q0 | Explicit course owner check | SELECT | courses | `id = :course_id` | LIMIT 1 | 403 if owner differs |
| Q1 | Count matching submissions | SELECT COUNT | assignment_submissions, assignments, courses, users | Mentor scope + optional course/status | None | `total` |
| Q2 | Read current page | SELECT | assignment_submissions, assignments, courses, users, uploads | Same as Q1; asset match is constrained | stable order; size 20 | Submission rows with 0/1 asset |

## Mutation Matrix

| Operation | Result |
|---|---|
| INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

## 3. Resolve response fields

- `id`, `assignment_id`, `user_id`, `content`, `status`, `submitted_at`, `score`, `feedback` come from `assignment_submissions`.
- `score` is converted to decimal string using `str(DB value)`.
- `files[]` comes only from the constrained API #34 upload match; one legacy `file_url` allows at most one asset.
- `items` contains the current page. `pagination` uses requested/default page, fixed size 20, count query total and ceiling division; `total_pages=0` when total=0.
- `meta` remains `{}`; page metadata is inside `data.pagination` per `Page<T>`.

## 4. Trả về response

### 4.1. Thành công

- HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<Page<Submission>>`.
- Empty results return a valid empty page, never a synthetic Submission or 404.

### 4.2. Business error

- 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- 403 `DESIGN_ACCESS_DENIED`.
- 409 `DESIGN_STATE_CONFLICT` remains listed but has no source-defined or implemented trigger.
- 422 `DESIGN_VALIDATION_ERROR` for invalid query types/ranges.

### 4.3. System error

- 500 `DESIGN_INTERNAL_ERROR` for SQL or response projection failure.
- Roll back a failed read transaction; never commit.
- Error envelope uses `data: null` through current `error_response()`.

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
