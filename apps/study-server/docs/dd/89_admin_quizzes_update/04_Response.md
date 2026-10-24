---
title: "Response"
order: 4
dd_id: "89"
api_name: "Cập nhật quiz"
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
| Success HTTP status | 200 |
| Direct response type | ApiEnvelope<Quiz> theo catalog #89. |
| Success business code | DESIGN_RESOURCE_UPDATED |

## Response fields — direct contract

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | API catalog | N/A | Step 9 | 200 success; lỗi theo catalog | N/A | Không thêm HTTP status. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> | success | Step 9 | true success, false error | Required | Reusable envelope. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | Step 9 | Exact branch code | Required | Success DESIGN_RESOURCE_UPDATED. |
| 4 | message | Message | message | string | No | Application | N/A | Step 9 | Safe message | Text chưa chuẩn hóa | Không lộ dữ liệu nội bộ. |
| 5 | data | Quiz | data | object (Quiz) | No | Candidate updated rows | N/A | Step 8 | ApiEnvelope<Quiz> | Required success | Nested persistence chưa đủ để hoàn thiện projection. |
| 5.1 | data.id | Quiz ID | id | int64 | No | Legacy quizzes candidate | id | Step 2 | Existing BIGSERIAL key | Required | Live schema chưa xác minh. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | quizzes/config | course_id | Step 4 | Updated candidate value | Required | Legacy nullable; course-move policy open. |
| 5.3 | data.title | Quiz title | title | string | No | config/quizzes | name | Step 4 | Alias title → name | Required | Request field is DERIVED. |
| 5.4 | data.duration_minutes | Duration | duration_minutes | int32 | Yes | config/quizzes | time_limit_minutes | Step 4 | Alias trực tiếp | Null/omit unresolved | Optional in Quiz schema. |
| 5.5 | data.passing_score | Passing score | passing_score | decimal-string | No | config/quizzes | passing_score | Step 4 | NUMERIC → decimal-string candidate | Required | Precision/scale open. |
| 5.6 | data.questions[] | Questions | questions | QuizQuestion[] | No | Candidate replacement rows | N/A | Steps 6–8 | Replacement rows in proposed order | Required array | Strategy DERIVED. |
| 5.6.1 | data.questions[].id | Question ID | id | int64 | No | quiz_questions candidate | id | Step 7 | Generated ID | Required | Legacy BIGSERIAL candidate. |
| 5.6.2 | data.questions[].text | Question text | text | string | No | quiz_questions candidate | question_text | Step 7 | Alias question_text → text | Required | Candidate physical mapping. |
| 5.6.3 | data.questions[].type | Question type | type | QuestionType | No | SOURCE_REQUIRED | N/A | Step 8 | No legacy column | Required | Blocks complete legacy response projection. |
| 5.6.4 | data.questions[].choices[] | Choices | choices | QuizChoice[] | No | quiz_choices candidate | N/A | Step 8 | Relation by question_id | Required array | Shape/order unresolved. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> | meta | Step 9 | Empty object candidate | Members unspecified | Current envelope convention. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> | traceId | Step 9 | Request trace | Required | Middleware generates/propagates current trace. |

## Business code theo status

| HTTP status | Business code | Basis |
|---:|---|---|
| 200 | DESIGN_RESOURCE_UPDATED | Direct catalog #89. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Direct catalog. |
| 403 | DESIGN_ACCESS_DENIED | Direct catalog. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Direct code; missing quiz mapping DERIVED. |
| 422 | DESIGN_VALIDATION_ERROR | Direct code; body/history semantics DERIVED. |
| 500 | DESIGN_INTERNAL_ERROR | Direct catalog. |

## Ví dụ thành công — HTTP 200, shape minh họa

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Quiz update message text is not specified by the contract.",
  "data": {
    "id": 501,
    "course_id": 9001,
    "title": "Quiz đã cập nhật",
    "duration_minutes": 30,
    "passing_score": "70.00",
    "questions": []
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000089"
}
~~~

questions: [] chỉ làm ví dụ envelope hợp lệ; không khẳng định update xóa hết câu hỏi. Logical response yêu cầu QuizQuestion nhưng QuestionType/QuizChoice chưa thể biểu diễn đầy đủ bằng legacy mapping hiện tại.

## Ví dụ lỗi — HTTP 404

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Quiz not-found message text is not specified by the contract.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000090"
}
~~~

API Guidelines yêu cầu error data=null. Current helper đổi data=None thành {}; integration cần thống nhất trước khi wire API #89.
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
