---
title: "Data Mapping"
order: 5
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "3. Data mapping"
status: "Draft — Needs Confirmation"
---

# Data Mapping

## Flow xử lý data

## 0. Authentication and access

### 0.1. Validate authentication and role

- Nhận Authorization Bearer JWT theo API catalog.
- Nếu token thiếu hoặc không hợp lệ:
  - Trả HTTP 401 DESIGN_AUTHENTICATION_REQUIRED.
- Nếu role không phải Student hoặc access bị từ chối theo policy đã xác nhận:
  - Catalog cho phép HTTP 403 DESIGN_ACCESS_DENIED.
- Runtime handler, claim name và policy API #28 chưa được tìm thấy; không suy ra implementation từ API khác.

### 0.2. Check quiz eligibility

| Source | Field/condition | Evidence | Status |
|---|---|---|---|
| AC-16 precondition | Student có quyền làm quiz | AC API index | Direct business precondition; predicate SOURCE_REQUIRED. |
| AC-16 precondition | Quiz đang mở | AC API index | Direct business precondition; allowed status values SOURCE_REQUIRED. |
| AC-16 activity | Hết lượt/hết hạn → 403/409 | AC-16 diagram | Diagram branch conflicts with API #28 catalog error set. |
| API #28 catalog | 401/403/404/500 | Approved design contract | Keep these codes in this DD; do not add 409. |

- Không tự tạo enrollment query, attempt-count policy, deadline rule hoặc status enum.
- Owner cần chốt API #28 có tự kiểm tra eligibility hay chỉ trả metadata/question set; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-28-01-student-quiz-state) và [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-28-02-attempt-expiry-http-409).

## 1. Request validation

- Đọc quiz_id từ required path parameter theo [03_Request.md](./03_Request.md).
- Contract type là int64; positivity, min/max và path parse-error mapping chưa được quy định.
- Không có query parameter hoặc request body theo API catalog.
- Không gán thêm 400/422 cho path parse lỗi vì API #28 catalog không liệt kê các status này.

## 2. Read Quiz and question set

### 2.1. Candidate Quiz metadata read

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quizzes AS q | q.id | Candidate Quiz ID | Checked-in DDL uses BIGSERIAL; query runtime chưa tồn tại. |
| ↑ | q.course_id | Candidate course scope | DDL nullable; DB design mô tả relation required. |
| ↑ | q.name | Candidate title source | Candidate alias name → Quiz.title. |
| ↑ | q.passing_score | Candidate passing score | NUMERIC(5,2); decimal-string serialization chưa được runtime xác nhận. |
| ↑ | q.time_limit_minutes | Candidate duration source | Candidate alias time_limit_minutes → duration_minutes; nullable. |
| ↑ | q.status | Candidate eligibility input | DB design default DRAFT; allowed/open values chưa được định nghĩa. |

**Candidate condition**

- q.id = path quiz_id.
- Đây là candidate predicate suy ra từ resource path và table key, không phải SQL runtime đã xác minh.

### 2.2. Candidate question read

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quiz_questions AS qq | qq.id | Candidate question ID | DB design and checked-in DDL. |
| ↑ | qq.quiz_id | Relation to Quiz | Candidate join/filter key; DDL nullable. |
| ↑ | qq.question_text | Candidate question text | Candidate alias question_text → QuizQuestion.text. |
| ↑ | qq.sort_order | Candidate display order | DB design mô tả thứ tự câu hỏi; tie-break chưa xác nhận. |
| ↑ | qq.score | Question score | Có trong DB design nhưng không có trong logical QuizQuestion response. |
| ↑ | SOURCE_REQUIRED | QuestionType source | Không có type column hoặc mapping trong DB design/DDL. |

**Candidate relation and ordering**

- Candidate relation: qq.quiz_id = q.id.
- Candidate ordering: qq.sort_order ASC dựa theo ý nghĩa field trong DB design.
- Unique tie-break khi trùng sort_order chưa được định nghĩa.
- Không lọc theo trạng thái hoặc publication vì không có rule/field question status được xác nhận.

### 2.3. Candidate choice read

| Target table | Column get | Chú thích | Remarks |
|---|---|---|---|
| quiz_choices AS qc | qc.id | Candidate choice ID | DB design; output property chưa được QuizChoice contract chốt. |
| ↑ | qc.question_id | Relation to question | Candidate relation key. |
| ↑ | qc.choice_text | Candidate choice text | DB design; output property chưa được QuizChoice contract chốt. |

**Answer-key restriction**

- Không đọc hoặc trả qc.is_correct trong response Student theo yêu cầu hiện tại.
- Catalog chưa định nghĩa QuizChoice fields; id/text chỉ là candidate mapping từ DB, chưa phải response contract đã duyệt.
- DB design không có choice sort_order; thứ tự choices SOURCE_REQUIRED.

### 2.4. Read-result handling

- Nếu không tìm thấy quiz:
  - Catalog có HTTP 404 DESIGN_RESOURCE_NOT_FOUND.
  - Exact not-found condition và access masking chưa được chốt.
- Quiz tồn tại nhưng đóng, Student không đủ quyền, hết lượt hoặc hết hạn:
  - AC-16 có nhánh 403/409.
  - API #28 catalog không khai báo 409; không thêm status/code vào contract của DD.
- Database, mapping hoặc internal error:
  - Catalog có HTTP 500 DESIGN_INTERNAL_ERROR.
  - Error response không chứa SQL, stack trace hoặc nội dung nội bộ.

## 3. Response mapping

| Response field | Candidate source | Mapping | Status / gap |
|---|---|---|---|
| data.id | quizzes.id | Direct candidate mapping. | Design-only; query chưa runtime-verified. |
| data.course_id | quizzes.course_id | Direct candidate mapping. | Logical field required; checked-in DDL nullable. |
| data.title | quizzes.name | Candidate alias name → title. | Description/status không thuộc logical Quiz schema. |
| data.duration_minutes | quizzes.time_limit_minutes | Candidate alias time_limit_minutes → duration_minutes. | Nullable/omit rule chưa xác nhận. |
| data.passing_score | quizzes.passing_score | NUMERIC → decimal-string candidate. | Serialization scale/rounding chưa được chốt. |
| data.questions[].id | quiz_questions.id | Direct candidate mapping. | Design-only. |
| data.questions[].text | quiz_questions.question_text | Candidate alias question_text → text. | Design-only. |
| data.questions[].type | N/A | No source mapping. | SOURCE_REQUIRED; enum/column absent. |
| data.questions[].choices[] | quiz_choices | Candidate relation via question_id. | QuizChoice shape chưa định nghĩa; không include is_correct. |
| meta / traceId | ApiEnvelope<T> schema | Envelope fields. | Runtime serialization chưa xác minh. |

- Không thêm quizzes.description, quizzes.status, created_at, updated_at hoặc quiz_questions.score vào response khi logical schema không khai báo chúng.
- Error mapping tham chiếu [06_Error.md](./06_Error.md); các field/schema chưa chốt nằm trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## 4. Mutation and external calls

### 4.1. Database mutation

- N/A — API #28 là GET theo catalog.
- Không insert/update/delete quizzes, quiz_questions hoặc quiz_choices.
- Transaction: N/A.

### 4.2. External calls

- Không có external API, storage hoặc signed URL call được API #28 sources mô tả.

## 5. Return response

### 5.1. Success

- HTTP 200.
- businessCode = DESIGN_RESOURCE_RETRIEVED.
- Return ApiEnvelope<Quiz> theo API catalog.
- Response mẫu chỉ minh họa envelope; nested QuizChoice shape chưa được chốt.

### 5.2. Authentication and access errors

- HTTP 401 DESIGN_AUTHENTICATION_REQUIRED theo API catalog.
- HTTP 403 DESIGN_ACCESS_DENIED theo API catalog.
- Exact trigger, role source và access policy còn SOURCE_REQUIRED.

### 5.3. Not found

- HTTP 404 DESIGN_RESOURCE_NOT_FOUND theo API catalog.
- Catalog không phân biệt quiz không tồn tại với quiz không được phép xem.

### 5.4. System error

- HTTP 500 DESIGN_INTERNAL_ERROR.
- Error data=null theo API Guidelines.
- Không trả raw SQL, stack trace hoặc internal detail.

### 5.5. Links

- Request: [03_Request.md](./03_Request.md).
- Response: [04_Response.md](./04_Response.md).
- Errors: [06_Error.md](./06_Error.md).
- Open decisions: [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
