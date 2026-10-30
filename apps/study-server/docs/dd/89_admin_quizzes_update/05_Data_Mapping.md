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
- [Step 2 — Lock target quiz and children](#step-2-lock-target-quiz-and-children)
- [Step 3 — Check attempt and answer history](#step-3-check-attempt-and-answer-history)
- [Step 4 — Validate course and update quiz parent](#step-4-validate-course-and-update-quiz-parent)
- [Step 5 — Delete old choices](#step-5-delete-old-choices)
- [Step 6 — Delete old questions](#step-6-delete-old-questions)
- [Step 7 — Insert replacement question set](#step-7-insert-replacement-question-set)
- [Step 8 — Build response and commit](#step-8-build-response-and-commit)
- [Step 9 — Return success or error](#step-9-return-success-or-error)

<a id="step-0-authentication-and-authorization"></a>
## Step 0 — Authentication and authorization

- Route nhận raw path, body bytes và Authorization; không parse JSON ở FastAPI.
- Shared `validate_current_user_request(..., role="ADMIN")` chạy trước path/body validation và mọi query.
- Token thiếu/sai/hết hạn → HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Principal không có role ADMIN → HTTP 403 `DESIGN_ACCESS_DENIED`.
- AC-35 fine-grained quiz-management permission chưa có claim/policy source; code chỉ thực thi role ADMIN.
- Dynamic path `/api/v1/admin/quizzes/{quiz_id}` đã được đăng ký trong `DESIGN_CONTRACT_PATHS`.

<a id="step-1-validate-request"></a>
## Step 1 — Validate request

| Input | Source | Runtime rule | Status |
|---|---|---|---|
| quiz_id | Required path `int64!` | Decimal digits; 1..9223372036854775807; invalid → 422 | Positive-only rule DERIVED |
| config | Outer body `string!` | Strict JSON string; inner config object theo validator #88 | Reused DERIVED proposal |
| questions | Outer body `string!` | Strict JSON string; inner array theo validator #88 | Reused DERIVED proposal |
| Query | Catalog/diagram | Không khai báo | DIRECT absence |

- Outer body chỉ nhận `config` và `questions`; field dư hoặc sai kiểu trả 422.
- `config.course_id` là signed int64; `title` tối đa 200; `duration_minutes` optional/null và int32; `passing_score` là decimal-string biểu diễn chính xác trong `NUMERIC(5,2)`.
- `questions[].type` theo ba giá trị validator #88: `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE`.
- `choices[].is_correct` optional; khi thiếu, validator #88 mặc định `false`.
- `questions=[]` và `choices=[]` được chấp nhận; không thêm answer-count rule.
- Các body/nested rules là DERIVED vì catalog #89 không khai báo body.

<a id="step-2-lock-target-quiz-and-children"></a>
## Step 2 — Lock target quiz and children

### Q1 — Lock active Quiz

| Target | Column | Predicate | Operation | Status |
|---|---|---|---|---|
| legacy quizzes AS q | q.id, q.status | q.id = :quiz_id AND status IS DISTINCT FROM 'DELETED' | `SELECT ... FOR UPDATE` | DERIVED; live schema chưa xác minh |

- Không có active row hoặc row đã tombstone → HTTP 404 `DESIGN_RESOURCE_NOT_FOUND`.
- Lock parent Quiz trước child rows để giữ thứ tự khóa thống nhất.
- Không đọc hoặc thay đổi `status`, `description`, `created_at` ngoài điều kiện tombstone.

### Q1.1 — Lock current Questions and Choices

| Target | Column | Predicate | Operation | Status |
|---|---|---|---|---|
| quiz_questions AS question | question.id | question.quiz_id = :quiz_id | `SELECT ... ORDER BY id FOR UPDATE` | Legacy candidate |
| quiz_choices AS choice | choice.id | choice.question_id = question.id AND question.quiz_id = :quiz_id | `SELECT ... ORDER BY id FOR UPDATE` | Legacy candidate |

- Xác thực ID rows là số dương, duy nhất; projection sai → rollback và HTTP 500.
- Lock child rows trước history check; sau DELETE, so sánh ID `RETURNING` với tập đã khóa.

<a id="step-3-check-attempt-and-answer-history"></a>
## Step 3 — Check attempt and answer history

### Q2 — Check history

| Target | Column | Predicate | Purpose | Status |
|---|---|---|---|---|
| quiz_attempts AS attempt | attempt.quiz_id | attempt.quiz_id = :quiz_id | Chặn mọi Quiz có attempt | DERIVED safety guard |
| quiz_answers AS answer | answer.question_id | answer.question_id thuộc quiz_questions.quiz_id = :quiz_id | Giữ answer FK history | Legacy candidate |
| quiz_answers AS answer | answer.choice_id | answer.choice_id thuộc quiz_choices của Quiz | Giữ choice FK history | Legacy candidate |

- Nếu `has_attempts=true` hoặc `has_answers=true`, trả 422 `DESIGN_VALIDATION_ERROR` trước mọi write.
- Không xóa attempt/answer rows; API #89 không version hoặc snapshot câu hỏi cũ.
- `FOR UPDATE` trên Quiz/Question/Choice là local locking proposal để ngăn candidate FK insert đồng thời; fake-session tests không xác minh PostgreSQL concurrency.

<a id="step-4-validate-course-and-update-quiz-parent"></a>
## Step 4 — Validate course and update quiz parent

### Q3 — Lock target Course

| Target | Column | Predicate | Operation | Status |
|---|---|---|---|---|
| courses AS course | course.id | course.id = :course_id | `SELECT ... FOR KEY SHARE` | Legacy BIGINT candidate |

- Course không tồn tại → rollback và HTTP 422 `DESIGN_VALIDATION_ERROR` tại `config.course_id`.
- Cho phép chuyển Course sang một Course khác đang tồn tại; không kiểm tra status, enrollment hoặc publish state.

### M1 — Update quizzes

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| path quiz_id | quizzes.id | WHERE id = :quiz_id; giữ PK | Direct path + candidate schema |
| config.course_id | quizzes.course_id | Gán target ID | DERIVED |
| config.title | quizzes.name | Alias title → name | DERIVED; VARCHAR(200) candidate |
| config.passing_score | quizzes.passing_score | decimal-string → NUMERIC(5,2) | DERIVED |
| config.duration_minutes | quizzes.time_limit_minutes | Giá trị hoặc NULL khi omit/null | DERIVED |
| Request timestamp | quizzes.updated_at | `CURRENT_TIMESTAMP` | DERIVED; legacy column NOT NULL |
| N/A | quizzes.status | Giữ nguyên | Not in request |
| N/A | quizzes.description | Giữ nguyên | Not in request |
| N/A | quizzes.created_at | Giữ nguyên | Not in request |

- UPDATE phải trả đúng quiz_id/course_id/title/duration/score; sai projection → rollback và HTTP 500.
- Tham chiếu [07_quizzes_update.md](./07_quizzes_update.md).

<a id="step-5-delete-old-choices"></a>
## Step 5 — Delete old choices

### M2 — Delete quiz_choices

- Delete qua join `quiz_questions` bằng `question.quiz_id = :quiz_id`.
- Xóa choices trước question rows để giữ thứ tự FK child-first.
- `RETURNING choice.id` phải khớp chính xác tập choice IDs đã khóa; mismatch → rollback và HTTP 500.
- Tham chiếu [08_quiz_choices_delete.md](./08_quiz_choices_delete.md).

<a id="step-6-delete-old-questions"></a>
## Step 6 — Delete old questions

### M3 — Delete quiz_questions

- Delete theo `quiz_questions.quiz_id = :quiz_id` sau khi choices cũ đã xóa.
- `RETURNING question.id` phải khớp tập question IDs đã khóa; mismatch → rollback và HTTP 500.
- Không xóa history; history guard phải chạy trước M1–M3.
- Tham chiếu [09_quiz_questions_delete.md](./09_quiz_questions_delete.md).

<a id="step-7-insert-replacement-question-set"></a>
## Step 7 — Insert replacement question set

### M4 — Insert quiz_questions

- Tạo row cho mỗi `questions[i]` theo input order.
- Map `questions[i].text` → `question_text`.
- Map `questions[i].type` → local migration-013 `question_type` candidate.
- Map `i` → `sort_order` zero-based.
- Bỏ `score` để dùng DDL default 1; không thêm score vào contract.
- Tham chiếu [10_quiz_questions_insert.md](./10_quiz_questions_insert.md).

### M5 — Insert quiz_choices

- Gắn choices bằng generated question ID từ M4.
- Map `choices[j].text` → `choice_text`.
- Map `choices[j].is_correct` → `is_correct`; absent được validator #88 chuẩn hóa thành false.
- Map `j` → migration-013 `sort_order` zero-based.
- Tham chiếu [11_quiz_choices_insert.md](./11_quiz_choices_insert.md).

<a id="step-8-build-response-and-commit"></a>
## Step 8 — Build response and commit

- Dựng `ApiEnvelope<Quiz>` từ parent `UPDATE ... RETURNING` và replacement rows.
- Map `data.id`, `course_id`, `title`, `duration_minutes`, `passing_score` từ row đã lưu.
- Map mỗi question/choice từ generated ID và projection `INSERT ... RETURNING`; input order được giữ trong response arrays.
- Admin choice response reuse #88 `{id,text,is_correct}`; Student API #28 không được trả `is_correct`.
- Null `duration_minutes` bị omit bởi response model `response_model_exclude_none=True`.
- Build và validate toàn response trước `db.commit()`; query, delete, insert, mapping hoặc commit failure đều rollback và trả 500.
- Shared error helper trả `data:null` và `meta.fieldErrors` khi lỗi validation.

<a id="step-9-return-success-or-error"></a>
## Step 9 — Return success or error

| Condition | HTTP | Business code | Transaction |
|---|---:|---|---|
| Quiz cập nhật thành công | 200 | `DESIGN_RESOURCE_UPDATED` | Commit sau mapping |
| Token không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa mở query |
| Thiếu role ADMIN | 403 | `DESIGN_ACCESS_DENIED` | Chưa mở query |
| Path/body lỗi, Course thiếu hoặc Quiz có history | 422 | `DESIGN_VALIDATION_ERROR` | Không có write; rollback nếu query đã chạy |
| Quiz thiếu hoặc status=`DELETED` | 404 | `DESIGN_RESOURCE_NOT_FOUND` | Rollback nếu query đã chạy |
| DB/query/projection/commit lỗi | 500 | `DESIGN_INTERNAL_ERROR` | Rollback toàn transaction |

- Không thêm 409 hoặc business code ngoài catalog.
- Không trả SQL, stack trace, hoặc dữ liệu nội bộ trong message.
- Request body, history guard, tombstone handling, Course move và lock semantics vẫn là DERIVED/open-owner choices.

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
