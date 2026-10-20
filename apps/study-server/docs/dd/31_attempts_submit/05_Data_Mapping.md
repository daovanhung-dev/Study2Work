---
title: "Data Mapping"
order: 5
dd_id: "31"
api_name: "Khóa attempt và bắt đầu chấm"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### 0. Authenticate and authorize

#### 0.1. Validate Bearer token and Student role

- The API catalog requires a Student Bearer JWT.
- Current Study auth helper validates the Bearer/JWT and Student role; API #31 is not wired to this helper.
- If authentication fails, return 401 DESIGN_AUTHENTICATION_REQUIRED.
- If role/access is denied, return 403 DESIGN_ACCESS_DENIED.

#### 0.2. Resolve Student identity and candidate attempt ownership

| Source | Field/condition | Evidence | Status |
|---|---|---|---|
| API catalog | Student Bearer JWT; no user ID request field. | API #31 row in list_api.md. | DIRECT contract. |
| Current Study auth helper | Current helper exposes the authenticated Student identity from JWT context. | apps/study-server/app/utils/auth.py. | CURRENT_BEHAVIOR; API #31 integration is not verified. |
| Candidate persistence | quiz_attempts.user_id. | DB table design, ERD and DDL. | DESIGN_ONLY; exact claim-to-column mapping and owner policy are SOURCE_REQUIRED. |

- Do not accept user_id from request data.
- Whether an attempt owned by another Student is denied as 403 or masked as 404 is unresolved.

#### 0.3. Check authorization result

- If the approved role/access check fails, return the catalog 403 code.
- The attempt ownership predicate and access-masking rule are recorded in [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-31-01-attempt-ownership).

### 1. Validate path parameter

- Read attempt_id from the required path parameter in [03_Request.md](./03_Request.md).
- The API catalog type is int64 and includes 422 DESIGN_VALIDATION_ERROR.
- Positive-value requirement, parse errors, overflow behavior and field-error metadata are SOURCE_REQUIRED.
- Do not add query parameters or request-body fields.

### 2. Load candidate attempt and grading context

#### 2.1. Candidate selected columns

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quiz_attempts AS a | a.id | Attempt ID | Candidate match for path attempt_id; no runtime query is verified. |
| ↑ | a.quiz_id | Parent quiz ID | Candidate relation for submitted attempt. |
| ↑ | a.user_id | Student owner | Candidate owner check; exact policy SOURCE_REQUIRED. |
| ↑ | a.status | Current attempt state | Candidate lifecycle check; accepted source states are not defined. |
| ↑ | a.started_at | Start time | Logical QuizAttempt field. |
| ↑ | a.submitted_at | Existing submission time | Candidate repeated-submit/state check. |
| ↑ | a.score | Aggregate score | Candidate update/result field; grading formula unresolved. |
| quiz_answers AS ans | ans.id | Answer row ID | Candidate row identity. |
| ↑ | ans.attempt_id | Parent attempt ID | Candidate filter for this attempt. |
| ↑ | ans.question_id | Answered question ID | Candidate join to quiz_questions. |
| ↑ | ans.choice_id | Selected choice ID | One-choice physical design candidate; API #30 representation differs. |
| ↑ | ans.is_correct | Stored correctness | Candidate update; DDL NOT NULL conflicts with pre-submit source gap. |
| ↑ | ans.score_received | Per-answer score | Candidate update; formula/scale unresolved. |
| quiz_questions AS q | q.id | Question ID | Candidate answer relationship. |
| ↑ | q.quiz_id | Parent quiz ID | Candidate consistency check against attempt quiz. |
| ↑ | q.score | Question points | Candidate grading input; weighting/rounding rule SOURCE_REQUIRED. |
| quiz_choices AS c | c.id | Choice ID | Candidate correctness lookup for choice answers. |
| ↑ | c.question_id | Parent question ID | Candidate relationship check. |
| ↑ | c.is_correct | Choice correctness | Candidate automatic-grading input; exact rule SOURCE_REQUIRED. |

#### 2.2. Candidate relationships

| Target table | Join condition | Join type |
|---|---|---|
| quiz_attempts AS a | N/A | BASE |
| quiz_answers AS ans | ans.attempt_id = a.id | LEFT JOIN candidate |
| quiz_questions AS q | q.id = ans.question_id AND q.quiz_id = a.quiz_id | LEFT JOIN candidate |
| quiz_choices AS c | c.id = ans.choice_id AND c.question_id = q.id | LEFT JOIN candidate |

These are candidate relationships from DB design/DDL. Query shape, missing-answer treatment and access filtering are not approved.

#### 2.3. Candidate lookup conditions

- Candidate attempt lookup: a.id = :attempt_id.
- Candidate answer set: ans.attempt_id = a.id.
- Candidate same-quiz consistency: q.quiz_id = a.quiz_id.
- Candidate choice relationship: c.question_id = q.id.
- Candidate owner comparison: a.user_id = authenticated Student ID; exact identity source and 403/404 behavior are SOURCE_REQUIRED.
- Candidate current-state check: a.status and a.submitted_at; allowed source state and repeat-submit behavior are SOURCE_REQUIRED.

#### 2.4. ORDER BY

N/A — API #31 returns one attempt; ordering of answer rows in QuizAttempt.answers is not defined.

### 3. Lock/submit the attempt

#### 3.1. Expected state transition

- AC-16 labels this action UPDATE Attempt = SUBMITTED.
- quiz_attempts is the candidate physical target.
- submitted_at is a candidate timestamp field set during submission.
- A conditional update from IN_PROGRESS, row lock, and exact conflict predicate are not specified; do not assert them as approved behavior.

#### 3.2. Candidate update matrix

| Operation | Target table | Condition | Values | Status |
|---|---|---|---|---|
| UPDATE | quiz_attempts | Candidate row selected by id = attempt_id; owner/state predicates remain open. | status = SUBMITTED per AC-16; submitted_at = timestamp source TBD; score = candidate aggregate after grading. | DESIGN_ONLY; exact update order, conditional predicate and transaction are SOURCE_REQUIRED. |

### 4. Grade submitted answers

#### 4.1. AC-16 grading branches

- AC-16 states that automatic grading occurs after submit.
- If any question requires manual grading, the attempt status is PENDING_GRADE.
- If no question requires manual grading, the attempt status is GRADED.
- The question-type field, manual-grade detection rule and behavior for unanswered questions are not defined.

#### 4.2. Candidate answer update matrix

| Operation | Target table | Condition | Values | Status |
|---|---|---|---|---|
| UPDATE candidate | quiz_answers | Candidate rows associated with the submitted attempt. | is_correct and score_received from approved grading rules, if available. | DB table map identifies API #31 grading updates; exact calculation and manual-answer values are SOURCE_REQUIRED. |

- quiz_choices.is_correct and quiz_questions.score are candidate grading inputs only.
- Do not create a grading formula, partial-credit rule, rounding rule or QuestionType enum.
- The DB DDL requires quiz_answers.is_correct NOT NULL, while API #30 does not define a pre-submit correctness value. Preserve this as a design/schema discrepancy.

### 5. Construct QuizAttempt response

- Return HTTP 200 and businessCode DESIGN_RESOURCE_UPDATED on success.
- Candidate response data follows the reusable QuizAttempt schema: id, quiz_id, status, started_at, optional submitted_at, optional score and answers[].
- AC-16 supplies PENDING_GRADE or GRADED as the submit outcome branches; other AttemptStatus values remain SOURCE_REQUIRED.
- Whether answers[].correct, answers[].score and aggregate score are returned before manual grading is complete is SOURCE_REQUIRED.
- Refer to [04_Response.md](./04_Response.md).

### 6. Error branches

- Use only the six error codes listed by API #31: 401, 403, 404, 422, 409 and 500.
- Missing attempt is a candidate 404 condition; owner masking and exact query semantics are unresolved.
- Invalid path/schema input maps to the catalog 422; exact parse/range mapping is unresolved.
- Attempt state conflict is a candidate 409 condition; exact states and repeated-submit behavior are unresolved.
- Error data is null per shared API guidelines; exact message and meta.fieldErrors are not specified.

### 7. Transaction and external calls

- Candidate database effects update quiz_attempts and, for automatic grading, quiz_answers.
- Atomicity across answer grading and attempt status/score, lock strategy, rollback and retry behavior are not defined.
- No external service or asynchronous operation is described by the API #31 contract or AC-16.
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
