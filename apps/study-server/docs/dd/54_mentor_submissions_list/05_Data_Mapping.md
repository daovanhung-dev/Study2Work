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
-> parse optional course_id/status/page
-> check Mentor access to courses with submissions
-> read candidate assignment_submissions through assignments/course
-> apply supplied filters only
-> resolve UploadAsset[] (SOURCE_REQUIRED)
-> map one Submission per catalog response contract
-> return ApiEnvelope
-> UI selects one row and calls API #55
~~~

API #54 chưa có runtime implementation. Các bảng và điều kiện bên dưới là design candidates, không phải SQL đã được xác nhận.

## Request Usage Matrix

| Request field | Source | Step | Validation | Query/response use | Gap |
|---|---|---:|---|---|---|
| Authorization | Header | 0.1 | Bearer JWT; role Mentor theo catalog | Xác định principal và course scope | Mentor guard/identity SOURCE_REQUIRED |
| course_id | Optional query | 1/2.1 | Optional int64; range chưa rõ | Filter candidate assignments.course_id | Không có default/range |
| status | Optional query | 1/2.1 | Optional string; enum chưa rõ | Filter candidate assignment_submissions.status | Blank/case policy chưa rõ |
| page | Optional query | 1/2.5 | Optional int32; range/default chưa rõ | Pagination chưa thể xác định | Không có page size hoặc response metadata |
| Request body | None | N/A | N/A | N/A | Catalog không khai báo body |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Catalog yêu cầu Bearer JWT và role Mentor.
- AC-23 yêu cầu Mentor có quyền chấm submission của course.
- Current Study shared guard chỉ kiểm tra Student; không có Mentor guard cho API #54.
- JWT subject-to-user mapping cho Mentor chưa được xác nhận trong route hiện tại.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| courses (candidate) | mentor_id | mentor_id = authenticated Mentor ID | DERIVED direct-owner candidate; assigned-course relation chưa có nguồn. |
| assignments (candidate) | course_id | assignments.course_id = courses.id | ERD relation; DDL permits NULL. |
| assignment_submissions (candidate) | assignment_id | assignment_submissions.assignment_id = assignments.id | ERD relation; DDL permits NULL. |

### 0.3. Check kết quả

- Nếu Bearer/JWT thiếu hoặc không hợp lệ: catalog 401; route guard chưa tồn tại.
- Nếu actor không phải Mentor hoặc không có quyền course: catalog 403; exact assignment predicate SOURCE_REQUIRED.
- Nếu course_id không được gửi: phạm vi tất cả courses Mentor được phép chấm là DERIVED; cần xác nhận ownership/assignment coverage.
- Nếu không có quyền theo candidate: không trả Submission rows; chính sách mask/not-found chưa được định nghĩa.

## 1. Validate data input

- course_id: nhận optional int64; positivity/range/malformed behavior không được catalog nêu.
- status: nhận optional string; không trim, lowercase hay validate enum khi chưa có rule.
- page: nhận optional int32; default, minimum, maximum và page-size behavior không được nêu.
- Catalog không có lỗi 422/404 cho API #54; không thêm error code.
- Pydantic/FastAPI path behavior hiện tại không phải API #54 behavior vì route chưa được đăng ký.

## 2. Get thông tin

### 2.1. Query

**Q1 — Candidate SELECT.** Logical base là assignment_submissions; quan hệ tới course đi qua assignments. courses.mentor_id chỉ là candidate access source.

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| assignment_submissions AS s | s.id | Submission ID | Candidate từ checked-in DDL. |
| ↑ | s.assignment_id | Assignment ID | Nullable trong DDL, bắt buộc theo guide/ERD. |
| ↑ | s.user_id | Student ID | Nullable trong DDL, bắt buộc theo guide/ERD. |
| ↑ | s.content | Submission text | Nullable candidate. |
| ↑ | s.file_url | Legacy single-file URL | Không đủ tạo UploadAsset[]. |
| ↑ | s.submitted_at | Submission time | TIMESTAMP candidate; timezone policy mở. |
| ↑ | s.score | Graded score | NUMERIC(6,2) candidate; format transform mở. |
| ↑ | s.feedback | Grader feedback | Nullable candidate. |
| ↑ | s.status | Submission status | VARCHAR(20) candidate; enum đầy đủ chưa có. |
| assignments AS a | a.id | Assignment relation | Candidate join key. |
| ↑ | a.course_id | Course scope | Optional course filter đi qua field này. |
| courses AS c | c.id | Course relation | Candidate access context. |
| ↑ | c.mentor_id | Direct course owner | DERIVED candidate; Mentor identity/assignment mapping chưa có. |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| assignment_submissions AS s | N/A | BASE candidate |
| assignments AS a | a.id = s.assignment_id | SOURCE_REQUIRED join behavior due nullable DDL |
| courses AS c | c.id = a.course_id | SOURCE_REQUIRED join behavior due nullable DDL |

ERD/table guide model the foreign keys as required; checked-in DDL allows NULL on s.assignment_id and a.course_id. This DD does not choose how orphan/null rows are handled.

### 2.3. WHERE

- Apply a.course_id = :course_id only if optional query course_id is supplied.
- Apply s.status = :status only if optional query status is supplied.
- Restrict every returned course to the authenticated Mentor's approved authorization scope; physical predicate SOURCE_REQUIRED.
- c.mentor_id = :mentor_id is a DERIVED direct-owner candidate only.
- No status default, allowed-value list, hidden/deleted filter or course lifecycle filter is defined.

### 2.4. ORDER BY

- N/A — Catalog and AC-23 do not define a stable sort order.

### 2.5. Pagination

- page is declared optional.
- No page size, default, minimum/maximum, offset rule or pagination metadata is declared.
- Do not specify LIMIT/OFFSET or reuse another endpoint's page-size convention.
- Whether a supplied page is ignored, rejected or applied under an external fixed size is SOURCE_REQUIRED.

### Query Matrix

| Query ID | Purpose | Type | Candidate base | Candidate joins | Filters | Order/pagination | Result |
|---|---|---|---|---|---|---|---|
| Q1 | Read submissions in Mentor scope | SELECT | assignment_submissions AS s | assignments AS a; courses AS c | Optional course_id/status plus approved Mentor scope | SOURCE_REQUIRED | Submission candidate rows |
| Q2 | Count matching submissions | N/A | N/A | N/A | No count contract | N/A | Do not invent PageMeta |

## Mutation Matrix

| Mutation ID | Operation | Target | Condition | Result |
|---|---|---|---|---|
| N/A | N/A | N/A | API is read-only | N/A — READ-ONLY API |

## 3. Resolve response fields

### 3.1. Candidate Submission mapping

| Response field | Candidate source | Transform/null handling | Status |
|---|---|---|---|
| data.id | s.id | Direct candidate | Live schema unverified |
| data.assignment_id | s.assignment_id | Direct candidate | DDL nullability conflict |
| data.user_id | s.user_id | Direct candidate | DDL nullability conflict |
| data.content | s.content | Preserve value; null/omit policy open | Nullable candidate |
| data.status | s.status | Preserve candidate value | Enum/lifecycle open |
| data.submitted_at | s.submitted_at | Serialize date-time | Zone/precision open |
| data.score | s.score | NUMERIC(6,2) to decimal-string | Rounding/serialization open |
| data.feedback | s.feedback | Preserve value | Null/disclosure policy open |
| data.files[] | No approved source | Do not map one file_url into UploadAsset[] | SOURCE_REQUIRED |

### Response Source Matrix

| Response path | Candidate source | Transform | Gap |
|---|---|---|---|
| data.id | assignment_submissions.id | Direct candidate | Live schema unverified |
| data.assignment_id | assignment_submissions.assignment_id | Direct candidate | DDL permits NULL |
| data.user_id | assignment_submissions.user_id | Direct candidate | DDL permits NULL |
| data.content | assignment_submissions.content | Preserve nullable value | Null/omit rule open |
| data.files[] and nested UploadAsset fields | No approved source | No transform approved | SOURCE_REQUIRED |
| data.status | assignment_submissions.status | Preserve candidate value | Enum/lifecycle open |
| data.submitted_at | assignment_submissions.submitted_at | Serialize date-time | Zone/precision open |
| data.score | assignment_submissions.score | NUMERIC to decimal-string | Serialization rule open |
| data.feedback | assignment_submissions.feedback | Preserve nullable value | Disclosure/null rule open |
| meta | Envelope convention | Empty object candidate | No page metadata |
| traceId | Request trace context | UUID propagation | Route absent |

### 3.2. Resolve files

- API #35 records the candidate mismatch between files:UploadAsset[] and one file_url.
- No approved asset table, association, ID, name, content type, size, status or URL policy was found.
- Do not synthesize asset objects or assert files: [] for real results.
- This blocks a complete response projection until the asset contract is supplied.

### 3.3. List/cardinality branch

- Catalog success schema is one Submission.
- AC-23 says “Đọc submissions” and the endpoint name is plural.
- Empty-result semantics and collection wrapper are not defined.
- Preserve singular schema in this draft; do not infer array, Page, 404 or a synthetic empty Submission.

## 4. Trả về response

### 4.1. Thành công

- HTTPStatus = 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Map data to exactly the catalog Submission type pending resolution of its list/cardinality mismatch.
- Return shared ApiEnvelope fields success, message, meta and traceId.
- Do not add items, count or pagination properties to meta.

### 4.2. Business error

- 401 → DESIGN_AUTHENTICATION_REQUIRED.
- 403 → DESIGN_ACCESS_DENIED.
- 409 → DESIGN_STATE_CONFLICT; trigger SOURCE_REQUIRED because AC-23 has no conflict branch.
- Keep error data behavior aligned after resolving the API Guidelines versus current helper discrepancy.

### 4.3. System error

- 500 → DESIGN_INTERNAL_ERROR.
- Do not expose raw database errors, SQL, token values or stack traces.
- No rollback applies; API is read-only.

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
