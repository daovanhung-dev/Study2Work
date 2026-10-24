---
title: "Data Mapping"
order: 5
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "3. Data mapping"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

~~~text
0. Authenticate Bearer JWT and require Mentor role
1. Read path submission_id and required body descriptors
2. Validate score:int32 and rubric-items:string presence/type; semantic rubric format remains SOURCE_REQUIRED
3. Candidate lookup submission and assignment/course scope
4. Missing submission -> catalog 404; Mentor scope denial -> catalog 403 (direct-owner policy is DERIVED)
5. Candidate update assignment_submissions.score and status=GRADED
6. Resolve the updated Submission response; files[] still requires an asset source
7. Return 200 DESIGN_RESOURCE_UPDATED
8. Client calls API #57 separately to write feedback, then shows success
~~~

API #56 has no current runtime route or DB query. SQL and table mapping below are design candidates only. Live schema is not verified.

## Request Usage Matrix

| Request item | Source | Step | Validation | Query/response use | Gap/status |
|---|---|---:|---|---|---|
| Authorization | Header | 0 | Bearer JWT; role Mentor | Principal for course access | Role DIRECT; Mentor guard and subject-to-user mapping SOURCE_REQUIRED |
| submission_id | Path | 1 / 3 | Required int64 | Candidate s.id lookup/update key | DIRECT type; malformed path mapping not specified |
| score | Body | 1 / 2 / 5 | Required int32 | Candidate score update and response | DIRECT type; min/max, scale and max_score rule SOURCE_REQUIRED |
| rubric items | Body descriptor | 1 / 2 | Required string | No approved persistence/response mapping | DIRECT required string; wire key, encoding and table SOURCE_REQUIRED |
| Query parameters | None | N/A | N/A | None | No catalog query fields |
| Additional body fields | None | N/A | Do not accept by contract unless contract changes | None | No extras defined |

## 0. Check quyền

### 0.1. Thực hiện check quyền

- Parse Bearer JWT using the shared Study token primitives.
- Require role Mentor because API catalog declares Mentor.
- Current shared request guard is Student-specific; a Mentor guard is not implemented.
- Convert authenticated subject into a Study numeric Mentor ID only after an approved mapping is available.
- Check the Mentor's permission for the course that owns the submission; AC-23 states this precondition.

### 0.2. Query/check quyền

| Target table/API | Column/Field | Condition/Value | Remarks |
|---|---|---|---|
| assignment_submissions AS s | s.id | s.id = :submission_id | Candidate submission lookup; legacy BIGSERIAL primary key |
| assignment_submissions AS s | s.assignment_id | a.id = s.assignment_id | Candidate relation; legacy DDL FK is nullable |
| assignments AS a | a.course_id | c.id = a.course_id | Candidate relation; legacy DDL FK is nullable |
| courses AS c | c.mentor_id | c.mentor_id = :mentor_id | Direct-owner access candidate DERIVED; assigned-Mentor relation absent |

### 0.3. Check kết quả

- If the candidate lookup returns no submission, map to 404 DESIGN_RESOURCE_NOT_FOUND.
- If the authenticated Mentor is not permitted for the submission course, map to 403 DESIGN_ACCESS_DENIED as a candidate interpretation of AC-23.
- Whether an existing but inaccessible submission must be masked as 404 is SOURCE_REQUIRED.
- Do not return submission fields before the access check succeeds.
- Broken or nullable assignment/course relations have no approved API mapping; do not infer an error code beyond the catalog.

## 1. Validate data input

- submission_id is required and has catalog type int64; path parse and overflow behavior is not specified.
- score is required and has catalog type int32.
- No score minimum, maximum, nonnegative rule, rounding rule or comparison against assignment.max_score is specified.
- rubric items is required string by the catalog descriptor; its physical key spelling and content format require confirmation.
- Invalid request shape/type maps to 422 DESIGN_VALIDATION_ERROR from the exact catalog set.
- No conflict or idempotency behavior is declared; do not add 409.

## 2. Get thông tin

### 2.1. Query

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| assignment_submissions AS s | s.id | Submission ID | Candidate PK and update key |
| ↑ | s.assignment_id | Assignment ID | Legacy DDL allows NULL |
| ↑ | s.user_id | Student ID | Legacy DDL allows NULL |
| ↑ | s.content | Text submission | Nullable candidate response field |
| ↑ | s.file_url | Legacy single file URL | Does not satisfy UploadAsset[] |
| ↑ | s.submitted_at | Submission time | Candidate response field |
| ↑ | s.score | Current score | Nullable numeric(6,2) candidate |
| ↑ | s.feedback | Current feedback | Nullable; not updated by API #56 |
| ↑ | s.status | Current status | VARCHAR(20), enum/constraints unresolved |
| assignments AS a | a.id | Assignment relation | Candidate authorization/read relation |
| ↑ | a.course_id | Course scope | Candidate relation |
| ↑ | a.max_score | Assignment maximum | Numeric(6,2); no approved validation rule |
| courses AS c | c.id | Course ID | Candidate owner relation |
| ↑ | c.mentor_id | Direct course owner | DERIVED access candidate only |

### 2.2. JOIN

| Target table | Join condition | Join type |
|---|---|---|
| assignment_submissions AS s | N/A | BASE |
| assignments AS a | a.id = s.assignment_id | LEFT JOIN candidate |
| courses AS c | c.id = a.course_id | LEFT JOIN candidate |

### 2.3. WHERE

- Candidate lookup condition: s.id = :submission_id.
- Candidate direct-owner condition: c.mentor_id = :mentor_id; DERIVED and depends on confirmed Mentor identity mapping.
- Do not use the UUID assessment rubric tables to join this BIGINT legacy candidate model.

### 2.4. ORDER BY

- N/A — primary-key lookup returns at most one candidate submission.

## 3. Insert/Update thông tin

### 3.1. Target table

- Candidate table: assignment_submissions.
- Rubric-item persistence target: SOURCE_REQUIRED; no approved assignment-rubric relation exists.

### 3.2. Conditions

- Candidate row key: assignment_submissions.id = :submission_id.
- Execute only after authenticated Mentor access has been checked.
- Update eligibility by current status and repeated grading behavior are SOURCE_REQUIRED.

### 3.3. Items update/insert

- Candidate UPDATE fields are assignment_submissions.score and assignment_submissions.status only.
- Set status to GRADED as stated by AC-23.
- Do not update feedback; API #57 is the separate feedback step.
- Do not write rubric items until a physical relation and item encoding are approved.
- Refer to [07_assignment_submissions_update.md](./07_assignment_submissions_update.md).

### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| submission_id | Path submission_id | Required int64; candidate row key |
| score | Body score | Required int32; database numeric conversion unresolved |
| status | Constant GRADED | AC-23 target state |
| rubric items | Required body string descriptor | No query/write parameter until target mapping is approved |
| mentor_id | Authenticated principal mapping | Required for direct-owner candidate; mapping SOURCE_REQUIRED |

## 4. Check kết quả execute query

### 4.1. Thành công

- HTTPStatus = 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Return ApiEnvelope<Submission> for the updated logical submission.
- Map every field in [04_Response.md](./04_Response.md); do not expose the row before authorization passes.
- Current score response format and files[] resolution remain SOURCE_REQUIRED.

### 4.2. Lỗi hệ thống

- HTTPStatus = 500.
- businessCode = DESIGN_INTERNAL_ERROR.
- Return a safe message; do not expose SQL, stack trace or internal provider details.
- Transaction and rollback behavior must be defined by the future implementation.
- Current middleware DESIGN_CONTRACT_PATHS uses exact path equality and does not include this dynamic route; generic system errors can fall back to INTERNAL_SERVER_ERROR unless future route/error mapping explicitly handles the catalog code.

### 4.3. Validate lỗi

- HTTPStatus = 422.
- businessCode = DESIGN_VALIDATION_ERROR.
- Refer to [06_Error.md](./06_Error.md) for the exact catalog validation cases.
- Current middleware DESIGN_CONTRACT_PATHS does not include API #56; generic request-validation handling can fall back to VALIDATION_ERROR.

### 4.4. Ngoài trường hợp trên

- Do not introduce status or business codes beyond the catalog.
- Recheck API #54 list cardinality and API #57 feedback sequencing during the AC-23 macro-review.
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
