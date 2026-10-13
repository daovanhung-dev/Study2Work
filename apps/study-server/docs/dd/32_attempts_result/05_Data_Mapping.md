---
title: "Data Mapping"
order: 5
dd_id: "32"
api_name: "Lấy điểm/kết quả được phép xem"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### 0. Authentication and access

#### 0.1. Validate Student authentication and role

- Nhận Authorization Bearer JWT theo API catalog.
- Current helper validate_current_user_request() kiểm tra token và role Student cho các API Study hiện có; API #32 chưa được đăng ký hoặc gọi helper này.
- Nếu token thiếu hoặc không hợp lệ:
  - Trả HTTP 401 DESIGN_AUTHENTICATION_REQUIRED theo catalog.
- Nếu role không phải Student:
  - Trả HTTP 403 DESIGN_ACCESS_DENIED theo catalog và current helper behavior.
- Current helper trả user_id từ JWT subject; mapping đó là evidence của helper hiện tại, không phải integration đã xác minh cho API #32.

#### 0.2. Candidate attempt ownership check

| Source | Field/condition | Evidence | Status |
|---|---|---|---|
| API catalog | Student Bearer JWT; request không nhận user_id. | API #32 row in list_api.md. | DIRECT contract. |
| Current Study auth helper | JWT subject được chuyển thành numeric user_id dương; role STUDENT được xác nhận. | app/utils/auth.py. | CURRENT_BEHAVIOR; API #32 integration chưa verified. |
| Candidate persistence | quiz_attempts.user_id. | DB table map, ERD and checked-in DDL. | DESIGN_ONLY; owner policy và physical live schema SOURCE_REQUIRED. |

- Candidate comparison: quiz_attempts.user_id = authenticated user_id.
- Không chấp nhận user_id từ request.
- Không được trả attempt/result của Student khác; việc denied request là 403 hay 404 chưa được chốt.

#### 0.3. Check access result

- Nếu user role bị từ chối, trả 403 theo catalog.
- Attempt không tồn tại có thể trả 404 theo catalog.
- Predicate chính xác, owner masking và cách phân biệt 403/404 nằm trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

### 1. Request validation

- Đọc attempt_id từ required path parameter trong [03_Request.md](./03_Request.md).
- Contract xác định kiểu int64.
- Contract không quy định min/max, positivity, overflow hoặc parse-error status.
- Catalog API #32 không liệt kê 422; không thêm 400/422 hoặc business code cho path parse lỗi.
- API không có query parameter hoặc request body.

### 2. Read candidate attempt and answers

#### 2.1. Candidate selected columns

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quiz_attempts AS a | a.id | Attempt ID | Candidate match với path attempt_id; chưa có runtime query. |
| ↑ | a.quiz_id | Quiz ID | Logical QuizAttempt field; design-only. |
| ↑ | a.user_id | Student owner ID | Candidate access predicate; exact policy SOURCE_REQUIRED. |
| ↑ | a.status | Grading/attempt status | AC-16 names GRADED/PENDING_GRADE; full enum/source condition open. |
| ↑ | a.started_at | Start time | Candidate mapping from DB design. |
| ↑ | a.submitted_at | Submit time | Candidate mapping; nullable in checked-in DDL. |
| ↑ | a.score | Aggregate score | Candidate mapping; nullable; availability when pending is SOURCE_REQUIRED. |
| quiz_answers AS ans | ans.attempt_id | Parent attempt ID | Candidate collection relationship. |
| ↑ | ans.question_id | Question ID | Logical QuizAnswer field. |
| ↑ | ans.choice_id | Selected choice ID | Physical single-choice field; logical choice_ids array mismatch. |
| ↑ | ans.is_correct | Answer correctness | Candidate graded outcome; Student disclosure policy SOURCE_REQUIRED. |
| ↑ | ans.score_received | Per-answer score | Candidate graded outcome; Student disclosure/format unresolved. |

#### 2.2. Candidate relation

| Target table | Join condition | Join type |
|---|---|---|
| quiz_attempts AS a | N/A | BASE |
| quiz_answers AS ans | ans.attempt_id = a.id | Query shape and join type SOURCE_REQUIRED; preserve attempts that have zero answers only if approved. |

#### 2.3. Candidate conditions

- Candidate attempt key: a.id = path attempt_id.
- Candidate owner comparison: a.user_id = authenticated user_id.
- Status/eligibility predicate: SOURCE_REQUIRED; AC-16 calls this endpoint after AUTO GRADED and PENDING GRADE branches but does not define behavior for other statuses.
- No SQL statement or live schema is verified for API #32.
- Answer ordering is not defined by the API catalog or AC-16.

### 3. Interpret grading status

- AC-16 activity diagram routes both AUTO GRADED and PENDING GRADE branches to API #32.
- AC-16 labels the following action “Đọc score + feedback/status” and displays either a score or a pending-grade state.
- For GRADED, quiz_attempts.score is a candidate source for QuizAttempt.score.
- For PENDING_GRADE, AC-16 confirms the status branch but does not define whether score is absent, null, partial, or included.
- AC-16 does not define whether API #32 can be called before submission or after other attempt states.
- The only catalog success response is HTTP 200 DESIGN_RESOURCE_RETRIEVED; do not add 409 or another response status.

### 4. Map candidate QuizAttempt response

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| data.id | quiz_attempts.id | Direct candidate projection. | Design-only; runtime query not verified. |
| data.quiz_id | quiz_attempts.quiz_id | Direct candidate projection. | Design-only. |
| data.status | quiz_attempts.status | Candidate AttemptStatus value. | AC-16 provides GRADED/PENDING_GRADE for result branches; full enum is SOURCE_REQUIRED. |
| data.started_at | quiz_attempts.started_at | Candidate timestamp projection. | Timezone/serialization policy not defined. |
| data.submitted_at | quiz_attempts.submitted_at | Candidate timestamp projection. | Omit/null policy SOURCE_REQUIRED. |
| data.score | quiz_attempts.score | Candidate decimal-string projection after grading. | Pending/partial score behavior and formatting SOURCE_REQUIRED. |
| data.answers[] | quiz_answers rows by attempt_id | Candidate collection. | Exact join, empty-list behavior and ordering SOURCE_REQUIRED. |
| data.answers[].question_id | quiz_answers.question_id | Direct candidate projection. | Design-only. |
| data.answers[].choice_ids[] | quiz_answers.choice_id | Would require conversion from physical single-choice row(s) to logical array. | DISCREPANCY; cardinality and multi-select mapping unresolved. |
| data.answers[].text_answer | N/A | No physical text-answer column is defined. | SOURCE_REQUIRED. |
| data.answers[].correct | quiz_answers.is_correct | Candidate student-answer grading result, not quiz_choices answer key. | Include/omit policy SOURCE_REQUIRED. |
| data.answers[].score | quiz_answers.score_received | Candidate per-answer score. | Disclosure and decimal scale SOURCE_REQUIRED. |
| data.feedback | N/A | Not present in QuizAttempt schema or candidate tables. | DISCREPANCY; do not add to response. |
| meta / traceId | ApiEnvelope<T> schema | Standard response envelope. | Current API #32 runtime serialization is not verified. |

- Do not read or return quiz_choices.is_correct as an answer-key field to the Student.
- The previous API #28 DD excludes the answer key from quiz detail; this result endpoint still lacks an approved policy for disclosing per-answer correctness.
- Refer to [04_Response.md](./04_Response.md) for the contract fields and illustrative branches.

### 5. Mutation and external calls

#### 5.1. Database mutation

- N/A — API #32 is GET.
- No insert, update, delete, grading calculation or score persistence is assigned to API #32.
- Transaction: N/A.

#### 5.2. External calls

- No external provider, object storage or asynchronous operation is described by the API #32 contract or AC-16.

### 6. Error branches

- Use only the four error codes listed by API #32: 401, 403, 404 and 500.
- Missing/invalid authentication maps to 401 per catalog and current auth helper.
- Non-Student role maps to 403 per catalog and current auth helper.
- Missing attempt maps to catalog 404; whether another Student's attempt is masked as 404 or returns 403 is SOURCE_REQUIRED.
- Invalid attempt_id parse/range behavior has no catalog error mapping; do not add 422.
- Unexpected data-access/internal failures map to 500 DESIGN_INTERNAL_ERROR; do not expose SQL or stack traces.
- Error response uses data = null under the shared API Guidelines.

### 7. Return response

#### 7.1. Success

- HTTP 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Return ApiEnvelope<QuizAttempt>.
- Both GRADED and PENDING_GRADE paths are shown in [04_Response.md](./04_Response.md); optional result fields remain subject to the open questions.

#### 7.2. Error

- Use only the business codes in [06_Error.md](./06_Error.md).
- The example and status mapping do not determine owner masking or path parse behavior.
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
