---
title: "Data Mapping"
order: 5
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

- [Step 0 — Authentication and authorization](#step-0-authentication-and-authorization)
- [Step 1 — Validate request](#step-1-validate-request)
- [Step 2 — Load target quiz](#step-2-load-target-quiz)
- [Step 3 — Check attempt and answer history](#step-3-check-attempt-and-answer-history)
- [Step 4 — Update quiz parent](#step-4-update-quiz-parent)
- [Step 5 — Delete old choices](#step-5-delete-old-choices)
- [Step 6 — Delete old questions](#step-6-delete-old-questions)
- [Step 7 — Insert replacement question set](#step-7-insert-replacement-question-set)
- [Step 8 — Build response and commit](#step-8-build-response-and-commit)
- [Step 9 — Return success or error](#step-9-return-success-or-error)

## Step 0 — Authentication and authorization

- Nhận Authorization Bearer JWT theo catalog.
- Token thiếu/sai/hết hạn → HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Principal không có Admin role hoặc quiz-management permission → HTTP 403 DESIGN_ACCESS_DENIED.
- AC-35 xác nhận permission nghiệp vụ; Study chưa có policy/claim mapping tương ứng.
- Hoàn tất authorization trước khi đọc Quiz, attempts hoặc answers.
- Không dùng Student guard để thay thế Admin guard.

| Item | Current evidence | Status |
|---|---|---|
| Admin Bearer guard | Current Study auth helper chỉ kiểm tra Student | NOT_FOUND |
| Quiz-management permission | AC-35 precondition; source policy chưa có | SOURCE_REQUIRED |
| API #89 route | Không có route/module/test | UNWIRED / NOT_FOUND |
| Middleware path | Dynamic Admin quiz path chưa có trong DESIGN_CONTRACT_PATHS | Conditional future wiring gap |

## Step 1 — Validate request

### Direct input

| Field | Source | Rule | Status |
|---|---|---|---|
| quiz_id | Required path | int64; min/max chưa có nguồn | DIRECT |
| Query | Catalog/diagram | Không khai báo | DIRECT |
| Body | Catalog | Không khai báo | DIRECT absence |

### Candidate body — chỉ sau khi được duyệt

| Field | Candidate type | Candidate use | Status |
|---|---|---|---|
| config | string | Parse như #88 proposed JSON object | DERIVED |
| questions | string | Parse như #88 proposed JSON array | DERIVED |

- Nếu owner duyệt body proposal, kiểm tra field presence/type và parse trước khi mở transaction.
- Embedded JSON sai cú pháp/shape theo proposal → candidate HTTP 422 DESIGN_VALIDATION_ERROR.
- Candidate config fields: course_id, title, duration_minutes?, passing_score.
- Candidate questions fields: text, type, choices[{text,is_correct}].
- Không thêm status, description, question score, query hoặc request field khác.
- Rule trim, length, answer-count, enum, numeric range và payload-size chưa có nguồn.
- Inner rules tiếp tục là proposal cho tới khi được xác nhận.

## Step 2 — Load target quiz

### Q1 — Candidate target read

| Target | Column | Predicate | Purpose | Status |
|---|---|---|---|---|
| legacy quizzes AS q | q.id | q.id = :quiz_id | Kiểm tra Quiz tồn tại và nạp metadata hiện tại | DERIVED; live schema chưa xác minh |
| legacy quizzes AS q | q.course_id | Cùng row | Candidate current course context | Legacy nullable discrepancy |
| legacy quizzes AS q | q.status | Cùng row | Chỉ đọc để bảo toàn; không cập nhật | Enum/lifecycle SOURCE_REQUIRED |

- Không có row → candidate HTTP 404 DESIGN_RESOURCE_NOT_FOUND theo code catalog.
- Không lấy Quiz ID từ body; path parameter là key.
- Transaction isolation/row-lock policy cần phối hợp API tạo attempt; source chưa xác nhận.

## Step 3 — Check attempt and answer history

### Q2 — Candidate attempt existence

| Target | Column | Predicate | Purpose | Status |
|---|---|---|---|---|
| legacy quiz_attempts AS qa | qa.id | qa.quiz_id = :quiz_id | Phát hiện attempt gắn với Quiz | DERIVED safety proposal |

### Q3 — Candidate answer references

| Target | Column | Predicate | Purpose | Status |
|---|---|---|---|---|
| legacy quiz_questions AS qq | qq.id | qq.quiz_id = :quiz_id | Khoanh vùng question cũ | Candidate relation |
| legacy quiz_answers AS ans | ans.question_id | ans.question_id = qq.id | Tìm answer history theo question | DERIVED safety proposal |
| legacy quiz_choices AS qc | qc.id | qc.question_id = qq.id | Khoanh vùng choice cũ | Candidate relation |
| legacy quiz_answers AS ans | ans.choice_id | ans.choice_id = qc.id | Tìm answer history theo choice | DERIVED safety proposal |

- Nếu Q2 hoặc Q3 có history, candidate dừng trước mutation và trả 422 DESIGN_VALIDATION_ERROR.
- Proposal bảo vệ IDs mà APIs #29–#32/ERD dùng; policy chưa được duyệt.
- Precheck không chứng minh race-safety. Lock/isolation phải thống nhất với API #29/#30 trước triển khai.

## Step 4 — Update quiz parent

### M1 — Candidate UPDATE legacy quizzes

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| path quiz_id | quizzes.id | WHERE id = :quiz_id; giữ PK | Direct path + candidate schema |
| config.course_id | quizzes.course_id | Gán giá trị candidate | DERIVED; course-move policy open |
| config.title | quizzes.name | Alias title → name | DERIVED; VARCHAR(200) candidate |
| config.passing_score | quizzes.passing_score | decimal-string → NUMERIC candidate | Scale/range open |
| config.duration_minutes | quizzes.time_limit_minutes | Alias trực tiếp | Null/omission open |
| Transaction timestamp | quizzes.updated_at | Candidate transaction time | DDL NOT NULL/no default; clock owner open |
| N/A | quizzes.status | Không cập nhật | Không có status trong candidate body |
| N/A | quizzes.description | Không cập nhật | Không có logical Quiz field |

- Tham chiếu [07_quizzes_update.md](./07_quizzes_update.md).
- Q1 no-row sau SELECT nhưng UPDATE không thấy row là integrity/concurrency failure; candidate 500.

## Step 5 — Delete old choices

### M2 — Candidate DELETE legacy quiz_choices

- Xóa choices thuộc questions hiện tại của Quiz.
- Candidate scope: question_id thuộc quiz_questions có quiz_id = :quiz_id.
- Xóa choices trước question rows để tôn trọng quan hệ 1:N.
- Chỉ chạy sau Q2/Q3 không thấy history và proposal được duyệt.
- Tham chiếu [08_quiz_choices_delete.md](./08_quiz_choices_delete.md).
- FK/cascade behavior live chưa xác minh.

## Step 6 — Delete old questions

### M3 — Candidate DELETE legacy quiz_questions

- Candidate predicate: quiz_questions.quiz_id = :quiz_id.
- Xóa sau khi choices cũ được xử lý.
- Tham chiếu [09_quiz_questions_delete.md](./09_quiz_questions_delete.md).
- Không xóa history khi chưa có chính sách/version model.

## Step 7 — Insert replacement question set

### M4 — Candidate INSERT legacy quiz_questions

- Tạo một row cho mỗi phần tử questions[] theo request order.
- Map text → question_text; index → sort_order zero-based là proposal từ #88.
- Dùng score default 1 trong legacy DDL chỉ làm candidate; không thêm score vào contract.
- Lấy generated question ID để gắn choices.
- Legacy table không có type; không thể khẳng định QuestionType được lưu.
- Tham chiếu [10_quiz_questions_insert.md](./10_quiz_questions_insert.md).

### M5 — Candidate INSERT legacy quiz_choices

- Tạo choices dưới question ID mới từ M4.
- Candidate map text → choice_text và is_correct → is_correct.
- Legacy table không có choice order.
- Không trả answer key is_correct theo suy luận.
- Tham chiếu [11_quiz_choices_insert.md](./11_quiz_choices_insert.md).

## Step 8 — Build response and commit

- Dựng ApiEnvelope<Quiz> từ parent và replacement rows theo logical response.
- data.id lấy từ quizzes.id; data.title map từ quizzes.name.
- course_id, duration_minutes, passing_score map theo updated row/candidate config.
- data.questions[].id lấy generated question IDs; text map từ question_text.
- data.questions[].type không có legacy column; QuizChoice output shape/order chưa chốt.
- Không tuyên bố response đầy đủ nếu QuestionType/QuizChoice chưa được persistence.
- Commit sau khi mutation và response mapping hợp lệ; lỗi trước commit rollback toàn transaction.
- API Guidelines yêu cầu error data=null; current helper serialize data=None thành {}.
- Dynamic path chưa có allowlist mapping; lỗi framework có thể dùng generic business code.

## Step 9 — Return success or error

### 9.1. Thành công

- HTTP 200.
- businessCode = DESIGN_RESOURCE_UPDATED.
- Direct response type = ApiEnvelope<Quiz>.
- Không thêm status, description, question score hoặc answer key.

### 9.2. Authentication/authorization

- Token thiếu/sai: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Admin/quiz-management permission bị từ chối: HTTP 403 DESIGN_ACCESS_DENIED.

### 9.3. Resource not found

- quiz_id không tồn tại → candidate HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
- Visibility sau soft delete phụ thuộc policy #90 chưa được chốt.

### 9.4. Validation

- Nếu body proposal được duyệt, schema lỗi → candidate 422 DESIGN_VALIDATION_ERROR.
- Nếu owner duyệt history guard, Quiz có attempt/answer → candidate 422 DESIGN_VALIDATION_ERROR.
- Không thêm 409, 400 hoặc business code khác.

### 9.5. System error

- Query/write/ID retrieval/mapping/commit failure → HTTP 500 DESIGN_INTERNAL_ERROR theo catalog.
- Nếu route được wire mà middleware không nhận dynamic path, business code có thể lệch catalog.
- Không trả raw SQL, stack trace hoặc answer key.
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
