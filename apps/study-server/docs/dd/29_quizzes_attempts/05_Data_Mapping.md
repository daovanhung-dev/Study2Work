---
title: "Data Mapping"
order: 5
dd_id: "29"
api_name: "Tạo attempt"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### 0. Authenticate and authorize

#### 0.1. Validate Bearer token and Student role

- Require Bearer JWT and role Student per the API catalog.
- If authentication fails, return 401 DESIGN_AUTHENTICATION_REQUIRED.
- If role/access is denied under the approved policy, return 403 DESIGN_ACCESS_DENIED.
- Current API #29 handler and token claim mapping are not found; do not infer a runtime implementation.

#### 0.2. Resolve authenticated Student identity

| Source | Field/condition | Evidence | Status |
|---|---|---|---|
| API catalog | Student Bearer JWT; no user_id request field | API #29 row | DIRECT contract; exact identity claim mapping SOURCE_REQUIRED. |
| Candidate persistence | quiz_attempts.user_id | DB table design and DDL | DESIGN_ONLY; FK is described as required in table design but nullable in checked-in DDL. |

- Do not accept user_id from the request.
- Do not name a JWT claim or user lookup query without an authoritative source.

### 1. Validate path parameter

- Read quiz_id from the required path parameter in [03_Request.md](./03_Request.md).
- Contract type is int64. Positive range, parse failure mapping and additional constraints are not defined.
- Catalog includes 422 DESIGN_VALIDATION_ERROR; exact path-validation cases are SOURCE_REQUIRED.

### 2. Resolve quiz and attempt eligibility

#### 2.1. Candidate quiz existence/read

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quizzes AS q | q.id | Candidate quiz ID | DB design/DDL evidence only; no API #29 runtime query. |
| ↑ | q.course_id | Candidate course scope | Physical nullability differs between table design and checked-in DDL. |
| ↑ | q.status | Candidate open-state input | Allowed status values and eligibility predicate are not defined. |
| ↑ | q.time_limit_minutes | Candidate time-limit input | Presence does not define attempt expiry behavior. |

- A missing quiz maps to the catalog's 404 DESIGN_RESOURCE_NOT_FOUND at the contract level.
- Exact lookup method and whether inaccessible quizzes are hidden as 404 are not specified.

#### 2.2. Eligibility decision

| Evidence | Rule | Status |
|---|---|---|
| AC-16 precondition | Student has permission to take the quiz. | Direct precondition; predicate SOURCE_REQUIRED. |
| AC-16 precondition | Quiz is open. | Direct precondition; allowed status values SOURCE_REQUIRED. |
| AC-16 activity | Eligibility decision follows the quiz/rules/question-set read; exhausted/expired branch is labeled 403/409. | Direct diagram branch; API ownership and code mapping unresolved. |
| API #29 catalog | 403 DESIGN_ACCESS_DENIED and 409 DESIGN_STATE_CONFLICT are both listed. | Approved design contract; branch predicates are not assigned. |

- API #28 OPEN_QUESTIONS.md also asks whether API #28 or API #29 owns this decision.
- Do not invent enrollment, publication, attempt-count, expiry, resume, concurrency or idempotency policy.
- See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-29-01-eligibility-owner) and [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-29-02-attempt-limit-expiry-and-conflict).

### 3. Insert attempt

#### 3.1. Candidate insert

- Target table: quiz_attempts.
- Candidate action: create one attempt row after eligibility is accepted.
- AC-16 labels the row status as IN_PROGRESS.
- The physical insert mapping is design-only; no query/repository implementation is verified.
- Candidate values are listed in [07_table.md](./07_table.md).

#### 3.2. Candidate mutation matrix

| Operation | Target table | Condition | Values | Status |
|---|---|---|---|---|
| INSERT | quiz_attempts | One new attempt for the requested quiz and authenticated Student. | quiz_id from path; user_id from authenticated principal; started_at source TBD; status IN_PROGRESS. | Table/diagram candidate; principal and timestamp source need confirmation. |

#### 3.3. Initial-state candidates

- id: generated key candidate based on DB BIGSERIAL design.
- quiz_id: request path value.
- user_id: authenticated Student identity; exact claim mapping SOURCE_REQUIRED.
- started_at: required by checked-in DDL; exact clock source, timezone and serialization policy SOURCE_REQUIRED.
- status: IN_PROGRESS per AC-16.
- submitted_at: candidate null before submission per DB table design.
- score: candidate null before grading per DB table design.
- No quiz_answers rows are described in the API #29 activity step.

### 4. Construct QuizAttempt response

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| data.id | quiz_attempts.id | Generated key candidate. | DB design only; runtime behavior not verified. |
| data.quiz_id | quiz_attempts.quiz_id | Candidate value from path. | Logical schema field; physical FK nullability discrepancy. |
| data.status | AC-16 / quiz_attempts.status | IN_PROGRESS. | AC-16 direct; full AttemptStatus enum SOURCE_REQUIRED. |
| data.started_at | quiz_attempts.started_at | Candidate persisted value. | Clock/timezone rule SOURCE_REQUIRED. |
| data.submitted_at | quiz_attempts.submitted_at | Optional logical field. | Initial null/omit behavior SOURCE_REQUIRED. |
| data.score | quiz_attempts.score | Optional decimal-string logical field. | Initial null/omit and serialization policy SOURCE_REQUIRED. |
| data.answers[] | QuizAttempt schema | No answer insert is described for API #29. | Required response property; initial value SOURCE_REQUIRED. |
| data.user_id | N/A | Not a field in logical QuizAttempt. | Do not add it to the response. |

- Error envelope follows [06_Error.md](./06_Error.md); error data is null per API guidelines.
- Do not expose raw SQL, stack trace, answer keys or internal details.

### 5. Return response

#### 5.1. Success

- HTTP 201.
- businessCode DESIGN_RESOURCE_CREATED.
- Return ApiEnvelope<QuizAttempt> according to the catalog.
- The sample in [04_Response.md](./04_Response.md) is illustrative where the source does not define initial optional values.

#### 5.2. Error branches

- Use only 401, 403, 404, 422, 409 and 500 business codes from API #29 catalog.
- Keep exact trigger mapping open where the API catalog/activity diagram is ambiguous.
- If a database mutation has begun, rollback behavior is SOURCE_REQUIRED until transaction ownership is approved.

### 6. Transaction and external calls

- Candidate flow writes one quiz_attempts row.
- Transaction ownership, retry behavior and concurrency handling are not defined.
- No external API, storage or asynchronous operation is described for API #29.

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
