---
title: "Data Mapping"
order: 5
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

### Mục lục

- [Step 0 — Authentication and authorization](#step-0-authentication-and-authorization)
- [Step 1 — Validate and parse body](#step-1-validate-and-parse-body)
- [Step 2 — Validate course reference](#step-2-validate-course-reference)
- [Step 3 — Insert Quiz parent](#step-3-insert-quiz-parent)
- [Step 4 — Insert question and choice children](#step-4-insert-question-and-choice-children)
- [Step 5 — Build response and commit](#step-5-build-response-and-commit)
- [Step 6 — Return success or error](#step-6-return-success-or-error)

<a id="step-0-authentication-and-authorization"></a>
## Step 0 — Authentication and authorization

- Nhận Authorization Bearer JWT theo catalog.
- Token thiếu/sai/hết hạn → HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Thiếu role Admin hoặc quiz-management permission → HTTP 403 DESIGN_ACCESS_DENIED.
- AC-35 xác định permission business; source chưa mô tả claim/policy mapping.
- Kiểm tra quyền trước khi đọc course hoặc ghi dữ liệu.
- Không nhận Admin ID từ body và không dùng Student guard thay cho Admin authorization.

| Item | Current evidence | Status |
|---|---|---|
| Admin Bearer guard | Study auth helper hiện kiểm tra Student; không có Admin helper | NOT_FOUND |
| Quiz-management permission | AC-35 precondition; source policy không có | SOURCE_REQUIRED |
| Route/API #88 | Không có route, module hoặc test | UNWIRED / NOT_FOUND |
| Middleware path | /api/v1/admin/quizzes chưa có trong DESIGN_CONTRACT_PATHS | Conditional future wiring gap |

<a id="step-1-validate-and-parse-body"></a>
## Step 1 — Validate and parse body

| Field | Direct rule | Proposed parse/use | Status |
|---|---|---|---|
| config | Required string | Parse JSON object | Direct type; embedded JSON DERIVED |
| questions | Required string | Parse JSON array | Direct type; embedded JSON DERIVED |

- Thiếu field, sai outer type hoặc body sai schema → HTTP 422 DESIGN_VALIDATION_ERROR theo catalog.
- Chỉ parse embedded JSON nếu owner duyệt cấu trúc string-encoded JSON.
- Không đổi outer contract thành config object hoặc questions array.

| Value | Proposed members | Mapping/status |
|---|---|---|
| config | course_id, title, duration_minutes?, passing_score | Logical Quiz fields; DERIVED |
| questions[] | text, type, choices[] | Logical QuizQuestion fields; DERIVED |
| choices[] | text, is_correct | Candidate create input từ legacy choice_text/is_correct; DERIVED, không phải output schema |

- Embedded JSON sai cú pháp hoặc member type sai → đề xuất 422 DESIGN_VALIDATION_ERROR.
- Không chốt enum, số question/choice, số đáp án đúng, range điểm hoặc payload limit.
- SINGLE_CHOICE trong ví dụ chỉ có trong V1-PILOT constraint, không được áp làm enum trực tiếp.
- Validate toàn bộ nested input trước transaction.

<a id="step-2-validate-course-reference"></a>
## Step 2 — Validate course reference

### Q0 — Candidate course existence read

| Target | Column | Predicate | Purpose | Status |
|---|---|---|---|---|
| courses AS c | c.id | c.id = config.course_id | Kiểm tra course trước insert | DERIVED; live schema chưa xác minh |

- Course không tồn tại → đề xuất HTTP 422 DESIGN_VALIDATION_ERROR vì API #88 không có 404.
- Không lọc course status, mentor owner hoặc publication state; AC-35 chỉ yêu cầu Admin quiz-management permission.
- Candidate precheck và DDL FK không chứng minh live DB constraint.

<a id="step-3-insert-quiz-parent"></a>
## Step 3 — Insert Quiz parent

### M1 — Candidate insert vào legacy quizzes

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| config.course_id | quizzes.course_id | Giữ int64 | DERIVED; DDL nullable, DB guide mô tả required |
| config.title | quizzes.name | Alias title → name | DERIVED; VARCHAR(200) NOT NULL candidate |
| config.passing_score | quizzes.passing_score | decimal-string → NUMERIC(5,2) | Candidate; range/scale open |
| config.duration_minutes | quizzes.time_limit_minutes | Alias trực tiếp; NULL nếu absent theo proposal | Candidate nullable |
| N/A | quizzes.description | Không ghi | Không có Quiz/config field |
| N/A | quizzes.status | DDL default DRAFT | Candidate default; lifecycle chưa chốt |
| Transaction time | quizzes.created_at | Thời điểm tạo | DDL NOT NULL, không có default |
| Same time | quizzes.updated_at | Cùng created_at khi tạo | DDL NOT NULL, không có default |
| Database | quizzes.id | BIGSERIAL generated ID | Legacy candidate |

- Generated Quiz ID được dùng cho question rows.
- Insert/ID retrieval lỗi → rollback transaction, 500 DESIGN_INTERNAL_ERROR.
- Không ghi description, status input, Admin ID hoặc audit row ngoài contract.

<a id="step-4-insert-question-and-choice-children"></a>
## Step 4 — Insert question and choice children

### M2 — Candidate insert vào legacy quiz_questions

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| Generated quiz ID | quiz_questions.quiz_id | Parent ID từ M1 | Legacy candidate |
| questions[i].text | quiz_questions.question_text | Alias text → question_text | Candidate |
| Input array index | quiz_questions.sort_order | Zero-based request index | DERIVED; DDL default 0 |
| N/A | quiz_questions.score | DDL default 1 | Candidate; không có score field trong API schema |
| Database | quiz_questions.id | BIGSERIAL generated ID | Legacy candidate |
| questions[i].type | SOURCE_REQUIRED | Legacy table không có cột type | DISCREPANCY với QuizQuestion |

- Tạo một row cho mỗi phần tử questions[] theo thứ tự array.
- Không thêm cột type hoặc map pilot question row vào legacy Quiz ID.

### M3 — Candidate insert vào legacy quiz_choices

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| Generated question ID | quiz_choices.question_id | Parent ID từ M2 | Legacy candidate |
| choices[j].text | quiz_choices.choice_text | Alias text → choice_text | DERIVED input mapping |
| choices[j].is_correct | quiz_choices.is_correct | Boolean answer key | DERIVED; QuizChoice chưa có contract |
| Database | quiz_choices.id | BIGSERIAL generated ID | Legacy candidate |
| Array order | N/A | Table không có sort_order | SOURCE_REQUIRED nếu order phải bền vững |

- Choice INSERT là DERIVED theo QuizQuestion.choices và candidate relation; AC-35 diagram chỉ ghi Quiz + Questions.
- Lưu cả lựa chọn đúng và sai; không bỏ các choice có is_correct=false.
- Không đưa is_correct vào response theo suy luận; QuizChoice output schema chưa định nghĩa.
- Bất kỳ lỗi child INSERT nào rollback cả Quiz và mọi child rows.

<a id="step-5-build-response-and-commit"></a>
## Step 5 — Build response and commit

- Dựng Quiz response từ config, parent ID và IDs của child rows trong transaction.
- data.id lấy từ quizzes.id; course_id/title/duration_minutes/passing_score map từ config/stored row.
- questions[].id/text/choices[] lấy từ các row vừa tạo theo input order proposal.
- questions[].type không thể đọc từ legacy question table; cần chốt persistence trước khi khẳng định response đầy đủ.
- QuizChoice field names, ID visibility, is_correct visibility và choice ordering chưa được định nghĩa.
- Nếu không dựng được đủ Quiz schema, không trả field giả/rỗng hoặc đổi response type; chốt schema/contract trước khi triển khai.
- Commit chỉ sau khi insert và response mapping hợp lệ; lỗi trước commit rollback toàn transaction.

| Boundary | Action | Failure behavior | Status |
|---|---|---|---|
| Before transaction | Parse outer/embedded input | 422; không có write | Outer direct; embedded DERIVED |
| Transaction body | Q0 course check → M1 parent → M2 questions → M3 choices | Không có course: không write; lỗi sau Q0 rollback toàn bộ | Q0+atomicity DERIVED |
| Commit | Sau insert và response mapping | 500 nếu DB commit lỗi | Candidate |
| External call | Không có | N/A | Theo diagram/contract |

<a id="step-6-return-success-or-error"></a>
## Step 6 — Return success or error

### 6.1. Thành công

- HTTP 201.
- businessCode = DESIGN_RESOURCE_CREATED.
- Direct response ApiEnvelope<Quiz>.
- Không thêm status, description, question score, answer key hoặc pagination metadata.

### 6.2. Authentication/authorization

- Token thiếu/sai: HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Role Admin/permission bị từ chối: HTTP 403 DESIGN_ACCESS_DENIED.

### 6.3. Validation

- Outer validation theo direct contract; embedded validation theo proposal: HTTP 422 DESIGN_VALIDATION_ERROR.
- Course ID không tồn tại dùng 422 chỉ là đề xuất vì catalog không khai báo 404.
- Không thêm 400, 404 hoặc 409.

### 6.4. System error

- Database, insert, ID retrieval, required mapping hoặc commit failure: HTTP 500 DESIGN_INTERNAL_ERROR.
- Nếu path chưa vào DESIGN_CONTRACT_PATHS, current middleware có thể trả INTERNAL_SERVER_ERROR.
- API Guidelines yêu cầu data=null; current helper serialize data=None thành {}.
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
