---
title: "Response"
order: 4
dd_id: "28"
api_name: "Lấy metadata/câu hỏi được phép hiển thị"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | API catalog | N/A | 5.1–5.5 | Fixed by branch: 200/401/403/404/500 | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> schema | success | 5.1–5.5 | Envelope field | N/A | API #28 serialization chưa runtime-verified. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 5.1–5.5 | Fixed by branch | N/A | Chỉ dùng code API #28 ở bảng bên dưới. |
| 4 | message | Message | message | string | No | ApiEnvelope<T> schema | message | 5.1–5.5 | SOURCE_REQUIRED | Nội dung theo policy chưa đặc tả. | Catalog khai báo type string nhưng không định nghĩa text. |
| 5 | data | Quiz | data | object (Quiz) | Required on success | API catalog reusable schema | N/A | 3.1/5.1 | ApiEnvelope<Quiz> | Error response data=null theo API Guidelines. | Query/projection API #28 chưa được runtime xác nhận. |
| 5.1 | data.id | Quiz ID | id | int64 | No | quizzes — candidate | id | 3.1 | Candidate direct mapping | Required theo logical Quiz. | Query API #28 chưa xác nhận. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | quizzes — candidate | course_id | 3.1 | Candidate direct mapping | Required theo logical Quiz. | Checked-in DDL cho phép NULL; DB design mô tả required. |
| 5.3 | data.title | Quiz title | title | string | No | quizzes — candidate | name | 3.1 | Candidate alias name → title | Required theo logical Quiz. | Physical quizzes.name là candidate source. |
| 5.4 | data.duration_minutes | Time limit | duration_minutes | int32 | Optional | quizzes — candidate | time_limit_minutes | 3.1 | Candidate alias time_limit_minutes → duration_minutes | Null/omit rule chưa xác nhận. | Physical column nullable; mapping chưa runtime-verified. |
| 5.5 | data.passing_score | Passing score | passing_score | decimal-string | No | quizzes — candidate | passing_score | 3.1 | NUMERIC → decimal-string candidate | Required theo logical Quiz. | Serialization scale/rounding chưa được quy định. |
| 5.6 | data.questions | Question list | questions | QuizQuestion[] | No | quiz_questions — candidate | N/A | 3.2–3.4 | Candidate relation through quiz_id | Array required theo Quiz schema; empty behavior chưa đặc tả. | Question ordering uses sort_order only as candidate. |
| 5.6.1 | data.questions[].id | Question ID | id | int64 | No | quiz_questions — candidate | id | 3.2 | Candidate direct mapping | Required theo QuizQuestion. | Query chưa xác nhận. |
| 5.6.2 | data.questions[].text | Question text | text | string | No | quiz_questions — candidate | question_text | 3.2 | Candidate alias question_text → text | Required theo QuizQuestion. | Candidate column is TEXT NOT NULL in checked-in DDL. |
| 5.6.3 | data.questions[].type | Question type | type | QuestionType | No | SOURCE_REQUIRED | N/A | 3.2 | N/A | Required theo QuizQuestion nhưng values/mapping chưa có nguồn. | Không có QuestionType definition hoặc column trong DB design/DDL. |
| 5.6.4 | data.questions[].choices | Answer choices | choices | QuizChoice[] | No | quiz_choices — candidate | N/A | 3.3 | Candidate relation through question_id | Array required theo QuizQuestion; exact shape chưa định nghĩa. | Catalog không định nghĩa QuizChoice schema. |
| 5.6.4.1 | data.questions[].choices[] | Choice item | N/A | QuizChoice | SOURCE_REQUIRED | quiz_choices — candidate | N/A | 3.3 | Shape SOURCE_REQUIRED | Nullability/field set chưa được định nghĩa. | User requirement: không đưa is_correct vào response Student. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> schema | meta | 5.1–5.5 | Envelope field | Members unspecified. | API-specific metadata không được catalog khai báo. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> schema | traceId | 5.1–5.5 | Envelope field | Required theo reusable schema. | Runtime generation/propagation API #28 chưa xác minh. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Đọc Quiz theo API catalog; projection/query chưa được runtime xác nhận. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Authentication failure theo contract. |
| 403 | DESIGN_ACCESS_DENIED | Role/access bị từ chối theo contract; policy cụ thể chưa rõ. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource not found theo contract; condition cụ thể chưa được gắn. |
| 500 | DESIGN_INTERNAL_ERROR | Lỗi nội bộ theo contract. |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Message text is not specified by the contract.",
  "data": {
    "id": 501,
    "course_id": 9001,
    "title": "Example quiz",
    "duration_minutes": 30,
    "passing_score": "70.00",
    "questions": []
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

> ID và giá trị quiz chỉ để minh họa envelope. questions là danh sách rỗng trong ví dụ để không tự đặt QuestionType hoặc QuizChoice shape; điều này không khẳng định quiz thật không có câu hỏi. Không có is_correct trong response Student.

## Ví dụ lỗi — HTTP 404

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Not-found message text is not specified by the contract.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

> API Guidelines quy định error data là null. Catalog chưa xác định 404 áp dụng cho quiz không tồn tại, không truy cập được hay điều kiện nào khác.
