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

- Route nhận raw Request; không dùng typed body để FastAPI parse trước endpoint.
- View gọi `validate_current_user_request(..., role="ADMIN")` trước khi đọc/parse body hoặc truy cập DB.
- Token thiếu/sai/hết hạn trả 401; principal không có role ADMIN trả 403.
- AC-35 fine-grained quiz-management permission chưa có claim/policy source; shared ADMIN là local implementation boundary.
- Không nhận Admin ID từ body.

<a id="step-1-validate-and-parse-body"></a>
## Step 1 — Validate and parse body

| Field | Contract | Local parsing/mapping | Status |
|---|---|---|---|
| config | Required string | JSON object `{course_id,title,duration_minutes?,passing_score}` | Outer type DIRECT; members DERIVED. |
| questions | Required string | JSON array `{text,type,choices:[{text,is_correct?}]}` | Outer type DIRECT; members DERIVED. |
| type | QuestionType | Values `SINGLE_CHOICE`, `MULTIPLE_CHOICE`, `TRUE_FALSE` | DERIVED vocabulary from V1-PILOT; stored on legacy BIGINT row. |
| choices[].is_correct | Not defined by catalog | Optional boolean, default false | DERIVED from legacy column default. |

- Unknown fields, malformed outer/embedded JSON, invalid member types, unsupported type values and values outside physical int/numeric ranges return 422.
- Passing score must fit legacy `NUMERIC(5,2)` without a business range rule.
- Title must fit legacy `VARCHAR(200)`; no body-size or array-count limit is added.
- Validate every nested item before opening the write flow.

<a id="step-2-validate-course-reference"></a>
## Step 2 — Validate course reference

### Q0 — Candidate course existence read

| Target | Column | Predicate | Purpose | Status |
|---|---|---|---|---|
| courses AS c | c.id | c.id = :course_id | Ensure Quiz FK target is present | Legacy candidate; live schema unverified. |

- Course không tồn tại trả 422 `DESIGN_VALIDATION_ERROR`; catalog không có 404.
- Không lọc course status, Mentor owner hoặc publication state vì AC-35 không đặt các điều kiện này cho Admin.

<a id="step-3-insert-quiz-parent"></a>
## Step 3 — Insert Quiz parent

### M1 — Candidate insert vào legacy quizzes

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| config.course_id | quizzes.course_id | int64 direct | Required by logical Quiz; candidate DDL nullable. |
| config.title | quizzes.name | title → name | Required, max 200 by candidate DDL. |
| config.passing_score | quizzes.passing_score | decimal-string → NUMERIC(5,2) | Enforce physical representability; business range open. |
| config.duration_minutes | quizzes.time_limit_minutes | Direct or NULL | Optional. |
| N/A | quizzes.description | Leave NULL | Not in input/Quiz contract. |
| N/A | quizzes.status | Existing DDL default `DRAFT` | Lifecycle remains open. |
| Current transaction time | quizzes.created_at | Set explicitly | DDL NOT NULL, no default. |
| Same time | quizzes.updated_at | Set explicitly | DDL NOT NULL, no default. |
| Database | quizzes.id | BIGSERIAL generated | Used for all child rows. |

<a id="step-4-insert-question-and-choice-children"></a>
## Step 4 — Insert question and choice children

### M2 — Candidate insert vào legacy quiz_questions

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| Generated Quiz ID | quiz_questions.quiz_id | Parent ID from M1 | Legacy FK candidate. |
| questions[i].text | quiz_questions.question_text | Direct alias | Required by logical Question. |
| questions[i].type | quiz_questions.question_type | Persist one of three local values | Migration 013 adds nullable column + CHECK; API writes non-null. |
| Input array index | quiz_questions.sort_order | Zero-based | Existing legacy column; preserves question order. |
| N/A | quiz_questions.score | Omit; use DDL default 1 | No score input. |
| Database | quiz_questions.id | BIGSERIAL generated | Used for choices and response. |

### M3 — Candidate insert vào legacy quiz_choices

| Input/logical field | Candidate column | Transform/setting | Status |
|---|---|---|---|
| Generated Question ID | quiz_choices.question_id | Parent ID from M2 | Legacy FK candidate. |
| choices[j].text | quiz_choices.choice_text | Direct alias | Required by local request proposal. |
| choices[j].is_correct | quiz_choices.is_correct | bool; absent defaults false | Existing physical answer-key column. |
| Choice array index | quiz_choices.sort_order | Zero-based | Migration 013 adds order for stable local projection. |
| Database | quiz_choices.id | BIGSERIAL generated | Returned to Admin. |

- Insert all question and choice items in request order.
- No rule is imposed for number of correct answers per question type.
- Student-facing API #28 must omit the answer-key field even though this Admin create response includes it.
- A failure in any child insert rolls back Quiz and every previously inserted child.

<a id="step-5-build-response-and-commit"></a>
## Step 5 — Build response and commit

- Build direct `ApiEnvelope<Quiz>` from INSERT/RETURNING projections before commit.
- Quiz maps `id`, `course_id`, `title`, optional `duration_minutes`, `passing_score`, and `questions[]`.
- Each question maps `id`, `text`, and persisted `type`; each choice maps `{id,text,is_correct}`.
- Return choices in `sort_order ASC,id ASC`; input indices make order deterministic.
- Any missing/mismatched ID or projection field is internal mapping failure and rolls back.
- Commit only after the complete response projection validates.

| Boundary | Action | Failure behavior | Status |
|---|---|---|---|
| Before DB | Auth then outer/embedded validation | 401/403 or 422; no write | Auth helper direct runtime; embedded shape DERIVED. |
| Transaction body | Q0 → M1 → M2 → M3 | Missing course 422; DB/mapping error 500 + rollback | Atomicity DERIVED. |
| Commit | After response mapping | Commit error 500 + rollback | Current Study transaction pattern. |
| External call | None | N/A | Diagram/contract. |

<a id="step-6-return-success-or-error"></a>
## Step 6 — Return success or error

### 6.1 Success

- HTTP 201.
- `businessCode=DESIGN_RESOURCE_CREATED`.
- `data` is the newly persisted Quiz.
- `meta={}` and `traceId` follows shared Study envelope/middleware.

### 6.2 Authentication and authorization

- Missing/invalid/expired Bearer token: HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED`.
- Missing ADMIN role: HTTP 403 `DESIGN_ACCESS_DENIED`.
- Fine-grained quiz-management permission is not source-backed and remains an explicit gap.

### 6.3 Validation

- Outer/embedded JSON validation, unsupported QuestionType, physical type range, or missing course: HTTP 422 `DESIGN_VALIDATION_ERROR`.
- No 404/409 is added.

### 6.4 System error

- Query/insert/response mapping/commit failure: HTTP 500 `DESIGN_INTERNAL_ERROR`.
- Roll back all writes and return a safe message without SQL or stack details.
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
