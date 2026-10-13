---
title: "Data Mapping"
order: 5
dd_id: "30"
api_name: "Autosave/lưu câu trả lời"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### 0. Authenticate and authorize

#### 0.1. Validate Bearer token and Student role

- API catalog requires a Bearer JWT and Student role.
- Current helper validate_current_user_request validates Bearer/JWT and requires STUDENT role.
- Current helper maps JWT sub to a positive numeric user ID; this is source-backed auth behavior, not evidence that API #30 is wired to the helper.
- If authentication fails, return 401 DESIGN_AUTHENTICATION_REQUIRED.
- If role/access is denied under the API contract, return 403 DESIGN_ACCESS_DENIED.

#### 0.2. Resolve authenticated Student identity

| Source | Field/condition | Evidence | Status |
|---|---|---|---|
| API catalog | Student Bearer JWT; no user ID request field | API #30 row in list_api.md | DIRECT contract. |
| Current Study auth helper | JWT sub is parsed to positive integer user_id; roles are normalized and checked for STUDENT. | app/utils/auth.py | CURRENT_BEHAVIOR; reusable helper exists, API #30 integration is not verified. |
| Candidate persistence | quiz_attempts.user_id | DB tables/ERD/DDL | DESIGN_ONLY; ownership comparison policy for this API is SOURCE_REQUIRED. |

- Do not accept user_id from the request body.
- Whether an attempt owned by another Student maps to 403 or is masked as 404 is not specified.

### 1. Validate path and body

- Read attempt_id from the required path parameter in [03_Request.md](./03_Request.md).
- Read question_id from the required request body.
- Read answer(s) using the exact catalog notation pending confirmation of its physical JSON key.
- attempt_id and question_id are int64 in the API catalog.
- Positive/range constraints, malformed numeric parsing, and field-level validation rules are SOURCE_REQUIRED.
- The catalog declares answer(s) as string, but string encoding, maximum length, multiplicity, and answer type are SOURCE_REQUIRED.
- See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-30-01-answer-contract).

### 2. Get attempt and question context

#### 2.1. Candidate query information

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quiz_attempts AS a | a.id | Attempt ID | Candidate lookup by path attempt_id; no runtime query exists. |
| ↑ | a.quiz_id | Quiz ID | Candidate parent scope for checking question membership. |
| ↑ | a.user_id | Student owner | Candidate owner field; access predicate/403-versus-404 policy SOURCE_REQUIRED. |
| ↑ | a.status | Attempt status | Candidate state field; allowed autosave states SOURCE_REQUIRED. |
| quiz_questions AS q | q.id | Question ID | Candidate lookup by body question_id; schema is design-only. |
| ↑ | q.quiz_id | Question quiz ID | Candidate relation to a.quiz_id; enforcement and not-found behavior SOURCE_REQUIRED. |
| quiz_answers AS qa | qa.id | Existing answer row ID | Candidate lookup only; no unique upsert key is defined. |
| ↑ | qa.attempt_id | Existing answer attempt ID | Candidate association for the AC-16 upsert; DDL has no natural-key constraint. |
| ↑ | qa.question_id | Existing answer question ID | Candidate association for the AC-16 upsert; duplicate-row behavior is SOURCE_REQUIRED. |
| quiz_choices AS c | c.id | Choice ID | Candidate validation only if answer representation is choice-based. |
| ↑ | c.question_id | Choice question ID | Candidate relationship only if answer representation is choice-based. |

#### 2.2. JOIN and candidate relationships

| Target table | Join condition | Join type |
|---|---|---|
| quiz_questions AS q | q.quiz_id = a.quiz_id | Candidate relationship from DB design; exact query is not approved. |
| quiz_answers AS qa | qa.attempt_id = a.id AND qa.question_id = q.id | Candidate lookup for an existing answer; uniqueness is not defined. |
| quiz_choices AS c | c.question_id = q.id | Conditional candidate relationship if answer input contains choice IDs. |

- ERD connects quiz_attempts to quiz_answers by attempt_id.
- ERD connects quiz_questions to quiz_answers by question_id.
- ERD connects quiz_choices to quiz_answers by choice_id.
- Diagram/API catalog do not define whether nonexistent attempt/question or cross-quiz question maps to 404, 403, or 422.

#### 2.3. Candidate lookup conditions

- Candidate attempt identifier: a.id = :attempt_id.
- Candidate question identifier: q.id = :question_id.
- Candidate same-quiz relationship: q.quiz_id = a.quiz_id.
- Candidate existing-answer lookup: qa.attempt_id = :attempt_id AND qa.question_id = :question_id; no unique constraint confirms one matching row.
- Candidate owner check: a.user_id = :authenticated_user_id; exact behavior is SOURCE_REQUIRED.
- Attempt status restriction such as a.status = IN_PROGRESS is not asserted by API #30 catalog; confirm before treating it as a WHERE condition.

#### 2.4. ORDER BY

N/A — API #30 updates a single question answer; no ordering rule is defined.

### 3. Upsert candidate answer

#### 3.1. Candidate target table

- Target table: quiz_answers.
- AC-16 labels the action UPSERT AttemptAnswer.
- quiz_answers is the candidate physical table based on DB tables/ERD; no current runtime method is wired.
- The upsert identity/unique key, insert-versus-update branch and transaction behavior are SOURCE_REQUIRED.

#### 3.2. Candidate mutation matrix

| Operation | Target table | Condition | Values | Status |
|---|---|---|---|---|
| UPSERT (diagram label) | quiz_answers | Attempt/question association; exact natural key and owner/state predicates are unresolved. | attempt_id from path; question_id from body; answer storage fields unresolved. | DESIGN_ONLY; no query, unique constraint or runtime handler is verified. |

#### 3.3. Candidate stored fields and grading gap

- quiz_answers.attempt_id candidate value comes from attempt_id.
- quiz_answers.question_id candidate value comes from question_id.
- quiz_answers.choice_id has one physical column; source from answer(s) is unresolved.
- quiz_answers.is_correct is NOT NULL in checked-in DDL; API #30 input has no correctness field and AC-16 places grading after submit at API #31.
- quiz_answers.score_received has DEFAULT 0 in checked-in DDL; whether autosave inserts and uses that default is not specified.
- The DDL also permits NULL for quiz-answer foreign keys while the table design describes them as required.
- Refer to [07_table.md](./07_table.md) and [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-30-02-storage-and-grading).

#### 3.4. Parameters

| Param | Giá trị | Remarks |
|---|---|---|
| attempt_id | Required path parameter | int64 per API catalog; source route not wired. |
| question_id | Required body field | int64 per API catalog; membership in the attempt's quiz is unresolved. |
| answer(s) | Required body field as written | string per catalog; key and representation unresolved. |
| authenticated_user_id | Candidate current Student ID | Current auth helper maps numeric JWT sub; whether/how API #30 applies owner check is SOURCE_REQUIRED. |

### 4. Return response

#### 4.1. Success

- HTTP 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Return ApiEnvelope<QuizAttempt> per API catalog.
- The logical QuizAttempt includes id, quiz_id, status, started_at, optional submitted_at, optional score, and required answers[].
- Whether the response returns the full attempt, all answers, or a limited projection is SOURCE_REQUIRED.
- Do not infer or expose correct/score for the saved answer before the grading contract is confirmed.
- Refer to [04_Response.md](./04_Response.md).

#### 4.2. Error branches

- Use only 401, 403, 404, 422 and 500 codes listed for API #30.
- Do not add 409 for a submitted/expired attempt without changing the canonical contract.
- Exact trigger mapping for 403/404/422 and safe message text is unresolved.
- Error data is null per shared API guidelines; safe field errors may be represented in meta.fieldErrors when applicable.

### 5. Transaction and external calls

- Candidate operation writes one answer row through insert/update behavior.
- Transaction ownership, concurrent autosave handling, retry/idempotency, and rollback behavior are not defined.
- No external service or asynchronous operation is described for API #30.
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

