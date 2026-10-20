---
title: "Định nghĩa table"
order: 7
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | quizzes, quiz_questions, quiz_choices |
| Logical table | Quiz, QuizQuestion, QuizChoice — QuizChoice shape chưa được định nghĩa |
| Operation | READ ONLY |
| Data Mapping step | 2.1–2.3, 3 |

Các cột dưới đây là candidate projection từ DB design/checked-in DDL. Chúng không xác nhận SQL hoặc schema đang chạy. Chỉ các field có trong logical response schema mới được ánh xạ; đáp án đúng không được đưa vào response Student.

## Update mapping

**Áp dụng khi**

- N/A — API #28 là GET và không cập nhật quiz data.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No update operation | N/A | N/A | Read-only contract. |

## Insert mapping

**Áp dụng khi**

- N/A — API #28 là GET và không tạo quiz data.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No insert operation | N/A | N/A | Read-only contract. |

## Delete mapping

**Áp dụng khi**

- N/A — API #28 là GET và không xóa quiz data.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | Read-only contract. |

## Read projection candidate

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | quizzes.id | Quiz ID | BIGSERIAL / int64 | N/A | N/A | Y | Primary key | Candidate response data.id | DB design and checked-in DDL | 2.1, 3 | Live schema/query chưa xác minh. |
| 2 | quizzes.course_id | Course ID | BIGINT / int64 | N/A | N/A | Y | FK candidate | Candidate response data.course_id | DB design and checked-in DDL | 2.1, 3 | DB table design says required; checked-in DDL permits NULL. |
| 3 | quizzes.name | Quiz title | VARCHAR | 200 | N/A | Y |  | Candidate response data.title | Checked-in DDL and logical Quiz schema | 2.1, 3 | Candidate alias name → title. |
| 4 | quizzes.passing_score | Passing score | NUMERIC | 5 | 2 | SOURCE_REQUIRED |  | Candidate response data.passing_score | DB design and logical Quiz schema | 2.1, 3 | DDL default 0; exact decimal-string serialization chưa xác nhận. |
| 5 | quizzes.time_limit_minutes | Duration in minutes | INT / int32 | N/A | N/A | N |  | Candidate response data.duration_minutes | DB design and logical Quiz schema | 2.1, 3 | Nullable; null/omit rule chưa xác nhận. |
| 6 | quizzes.status | Quiz state | VARCHAR | 20 | N/A | N |  | Candidate eligibility input; not in Quiz response schema | DB design and checked-in DDL | 2.1 | Default DRAFT; enum and allowed/open predicate SOURCE_REQUIRED. |
| 7 | quiz_questions.id | Question ID | BIGSERIAL / int64 | N/A | N/A | Y | Primary key | Candidate response data.questions[].id | DB design and checked-in DDL | 2.2, 3 | Live schema/query chưa xác minh. |
| 8 | quiz_questions.quiz_id | Quiz ID | BIGINT / int64 | N/A | N/A | Y | FK candidate | Candidate relation to quizzes.id | DB design and checked-in DDL | 2.2 | Design docs say required; checked-in DDL permits NULL. |
| 9 | quiz_questions.question_text | Question text | TEXT / string | N/A | N/A | Y |  | Candidate response data.questions[].text | DB design, checked-in DDL and logical schema | 2.2, 3 | Candidate alias question_text → text. |
| 10 | quiz_questions.sort_order | Question order | INT / int32 | N/A | N/A | N |  | Candidate ORDER BY source; not response field | DB design and checked-in DDL | 2.2 | Default 0; duplicate tie-break SOURCE_REQUIRED. |
| 11 | quiz_questions.score | Question score | NUMERIC | 5 | 2 | N |  | Not included in logical QuizQuestion | DB design and checked-in DDL | 2.2 | Do not add to response without contract change. |
| 12 | quiz_choices.id | Choice ID | BIGSERIAL / int64 | N/A | N/A | Y | Primary key | Candidate QuizChoice field; not confirmed | DB design and checked-in DDL | 2.3 | QuizChoice logical fields are undefined. |
| 13 | quiz_choices.question_id | Question ID | BIGINT / int64 | N/A | N/A | Y | FK candidate | Candidate relation to quiz_questions.id | DB design and checked-in DDL | 2.3 | DDL permits NULL; live schema/query not verified. |
| 14 | quiz_choices.choice_text | Choice text | TEXT / string | N/A | N/A | Y |  | Candidate QuizChoice field; not confirmed | DB design and checked-in DDL | 2.3 | Exact response property name/shape SOURCE_REQUIRED. |

### Excluded source field

| Physical column | Type | Source | Reason excluded | Data Mapping step |
|---|---|---|---|---|
| quiz_choices.is_correct | BOOLEAN | DB design and checked-in DDL | Answer key must not be exposed by Student quiz-read response. | 2.3 |

### Read conditions

- Candidate quiz key: quizzes.id = path quiz_id; exact query is not present in runtime.
- Candidate question relation: quiz_questions.quiz_id = quizzes.id.
- Candidate question ordering: quiz_questions.sort_order ASC; stable tie-break is not defined.
- Candidate choice relation: quiz_choices.question_id = quiz_questions.id.
- Choice ordering has no source column or contract rule.
- Student entitlement, quiz open-state, attempt limit and expiry predicates are not specified.
- DB_UNICA_TABLES.md marks quiz foreign-key relations required, while checked-in DB.sql does not declare NOT NULL for quizzes.course_id, quiz_questions.quiz_id or quiz_choices.question_id.
- No live database metadata was inspected; checked-in DDL remains design evidence only.
