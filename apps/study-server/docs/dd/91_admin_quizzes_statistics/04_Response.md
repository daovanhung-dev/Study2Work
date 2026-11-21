---
title: "Response"
order: 4
dd_id: "91"
api_name: "Xem thống kê quiz"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields — direct catalog contract

| No | Path | Logical name | Physical name | Type | Nullable | Source table/column | Source step | Transform/null rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | Catalog | Branch | 200 or exact catalog errors | Không thêm status. |
| 2 | `success` | Success flag | `success` | boolean | No | ApiEnvelope | Envelope | true success, false error | Reusable schema. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | Branch | Exact catalog literal | DIRECT. |
| 4 | `message` | Message | `message` | string | No | Application | Branch | Nội dung an toàn; text cụ thể chưa chỉ định | DERIVED. |
| 5 | `data` | Quiz | `data` | object (Quiz) | No | Candidate quiz + question tables | Success | Direct schema | Không có statistics field. |
| 5.1 | `data.id` | Quiz ID | `id` | int64 | No | quizzes.id | Q1 | Direct candidate | BIGINT design only. |
| 5.2 | `data.course_id` | Course ID | `course_id` | int64 | No | quizzes.course_id | Q1 | Required logical field | Legacy DDL cho phép NULL. |
| 5.3 | `data.title` | Quiz title | `title` | string | No | quizzes.name | Q1 | name → title | Candidate. |
| 5.4 | `data.duration_minutes` | Duration | `duration_minutes` | int32 | Yes | quizzes.time_limit_minutes | Q1 | Alias; null/omit chưa chốt | Optional field. |
| 5.5 | `data.passing_score` | Passing score | `passing_score` | decimal-string | No | quizzes.passing_score | Q1 | Numeric → string | DDL allows NULL; discrepancy. |
| 5.6 | `data.questions[]` | Questions | `questions` | QuizQuestion[] | No | quiz_questions + choices | Q2 nếu direct Quiz phải được trả | Cần projection riêng | Không thuộc aggregate query. |
| 5.6.1 | `data.questions[].id` | Question ID | `id` | int64 | No | quiz_questions.id | Q2 | Direct candidate | Live schema chưa xác minh. |
| 5.6.2 | `data.questions[].text` | Question text | `text` | string | No | quiz_questions.question_text | Q2 | question_text → text | Candidate. |
| 5.6.3 | `data.questions[].type` | Question type | `type` | QuestionType | No | SOURCE_REQUIRED | N/A | Không có legacy column đã xác nhận | Required schema gap. |
| 5.6.4 | `data.questions[].choices[]` | Choices | `choices` | QuizChoice[] | No | SOURCE_REQUIRED | N/A | QuizChoice schema chưa có | Không tự thêm answer-key field. |
| 6 | `meta` | Metadata | `meta` | object | No | ApiEnvelope | Envelope | Không có pagination contract | Members chưa quy định. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Request context | Envelope | Propagate trace | Runtime giữ trace của request. |

## Response proposal — runtime fallback DERIVED, chưa được duyệt

AC-35 yêu cầu statistics nhưng reusable Quiz không có metric. Runtime dùng DTO riêng `ApiEnvelope<QuizStatistics>` theo phương án DERIVED; đây không phải schema catalog hiện tại và chưa được owner duyệt.

| Path | Type | Candidate source/expression | Null/transform rule | Status |
|---|---|---|---|---|
| `data.quiz_id` | int64 | quizzes.id | ID row được tìm thấy | DERIVED; runtime local |
| `data.attempt_count` | int64 | COUNT(quiz_attempts.id) | Tất cả attempt gắn với quiz | DERIVED; runtime local |
| `data.submitted_attempt_count` | int64 | COUNT(submitted_at) | submitted_at khác NULL | DERIVED; runtime local |
| `data.graded_attempt_count` | int64 | COUNT(score) | score khác NULL | DERIVED; runtime local |
| `data.average_score` | decimal-string? | AVG(score) | NULL khi không có scored attempt; scale/rounding mở | DERIVED; runtime local |
| `data.passed_attempt_count` | int64? | COUNT(score >= passing_score) | NULL nếu threshold NULL; 0 nếu threshold có giá trị nhưng không ai đạt | DERIVED; runtime local |
| `data.pass_rate_percent` | decimal-string? | passed / graded × 100 | NULL khi threshold NULL hoặc graded=0; không làm tròn trong app | DERIVED; runtime local |

## Ví dụ thành công — direct contract

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy quiz.",
  "data": {
    "id": 41,
    "course_id": 7,
    "title": "Kiểm tra cuối chương",
    "duration_minutes": 45,
    "passing_score": "60.00",
    "questions": []
  },
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

> Direct response này không chứa statistics, thể hiện rõ conflict với AC-35.

## Ví dụ thành công — QuizStatistics proposal

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy thống kê quiz.",
  "data": {
    "quiz_id": 41,
    "attempt_count": 120,
    "submitted_attempt_count": 110,
    "graded_attempt_count": 100,
    "average_score": "72.34",
    "passed_attempt_count": 78,
    "pass_rate_percent": "78.00"
  },
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

## Ví dụ rỗng — proposal

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy thống kê quiz.",
  "data": {
    "quiz_id": 41,
    "attempt_count": 0,
    "submitted_attempt_count": 0,
    "graded_attempt_count": 0,
    "average_score": null,
    "passed_attempt_count": 0,
    "pass_rate_percent": null
  },
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

## Ví dụ lỗi — 404

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy quiz.",
  "data": null,
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

> API Guidelines và current `error_response` đều tuần tự hóa error `data` thành `null`; route #91 dùng helper hiện hành.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `2.Response`
- Dimension: `A2:BR45`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `52`
- Số vùng merge: `15`

<details>
<summary>Danh sách vùng merge</summary>

- `B14:C15`
- `B16:C16`
- `B21:C21`
- `B22:BA22`
- `B23:C23`
- `B24:C24`
- `D14:S14`
- `T14:AK14`
- `AL14:BA15`
- `B20:C20`
- `B17:C17`
- `B18:C18`
- `T18:AB18`
- `AC18:AK18`
- `B19:BA19`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `B9` | Format |  |
| 9 | `L9` | JSON |  |
| 10 | `B10` | Code ký tự |  |
| 10 | `L10` | UTF-8 |  |
| 11 | `B11` | Content-Type |  |
| 11 | `L11` | application/json |  |
| 14 | `B14` | No |  |
| 14 | `D14` | Response item name |  |
| 14 | `T14` | Refer DB |  |
| 14 | `AL14` | Remarks |  |
| 15 | `D15` | Tên logic |  |
| 15 | `L15` | Tên vật lý |  |
| 15 | `T15` | Table nguồn get |  |
| 15 | `AC15` | Field nguồn get |  |
| 16 | `B16` | 1 |  |
| 16 | `D16` | HTTP Status |  |
| 16 | `L16` | HTTPStatus |  |
| 16 | `AL16` | Thành công: 200/ Phát sinh lỗi: 500/ Validate lỗi: 400 |  |
| 17 | `B17` | 2 |  |
| 17 | `D17` | Status |  |
| 17 | `L17` | status |  |
| 17 | `AL17` | Thành công: 1/phát sinh error: 2 |  |
| 18 | `B18` | 3 |  |
| 18 | `D18` | Nội dung response |  |
| 18 | `L18` | response |  |
| 19 | `B19` | Trường hợp thành công |  |
| 20 | `B20` | 3.1 |  |
| 21 | `B21` | 3.2 |  |
| 22 | `B22` | Các trường hợp lỗi của API |  |
| 23 | `B23` | 3.1 |  |
| 23 | `D23` | Error code |  |
| 23 | `M23` | error_code |  |
| 24 | `B24` | 3.2 |  |
| 24 | `D24` | Error Message id |  |
| 24 | `M24` | error_message_id |  |
| 26 | `B26` | Ví dụ |  |
| 27 | `M27` | Trường hợp thành công |  |
| 28 | `N28` | { |  |
| 29 | `O29` |   "status": 1, |  |
| 30 | `O30` |   "response":{ |  |
| 33 | `O33` | } |  |
| 34 | `N34` | } |  |
| 36 | `M36` | Trường hợp lỗi |  |
| 37 | `N37` | { |  |
| 38 | `O38` | "status" : 2 , |  |
| 39 | `O39` | "response" : {  |  |
| 40 | `P40` | "error_code" : "9999", |  |
| 41 | `P41` | "error_message_id" : "DLG000000" |  |
| 42 | `O42` |  } |  |
| 43 | `N43` |  } |  |

</details>
