---
title: "Response"
order: 4
dd_id: "88"
api_name: "Tạo quiz mới"
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
| Success HTTP status | 201 |
| Direct response type | ApiEnvelope<Quiz> theo catalog #88. |
| Success business code | DESIGN_RESOURCE_CREATED |

## Response fields — direct contract

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | API catalog | N/A | 6.1/6.2 | 201 success; errors theo catalog | N/A | Không thêm HTTP status. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> | N/A | 6.1/6.2 | true success, false error | Required | Reusable envelope. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 6.1/6.2 | Exact code theo nhánh | Required | Giữ code catalog. |
| 4 | message | Message | message | string | No | Application | N/A | 6.1/6.2 | Safe message | Nội dung chưa chuẩn hóa | Không lộ thông tin nội bộ. |
| 5 | data | Quiz | data | object (Quiz) | No | Candidate insert results | N/A | 5.1 | ApiEnvelope<Quiz> | Required on success | Cần IDs đã sinh và nested fields theo Quiz schema. |
| 5.1 | data.id | Quiz ID | id | int64 | No | Legacy quizzes candidate | id | 3.1 | Generated BIGSERIAL → int64 | Required | Live model chưa xác minh. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | config.course_id / quizzes | course_id | 3.1 | Candidate direct mapping | Required | Embedded field DERIVED; physical column nullable trong DDL. |
| 5.3 | data.title | Quiz title | title | string | No | config.title / quizzes | name | 3.1 | Alias title → name | Required | Candidate alias. |
| 5.4 | data.duration_minutes | Duration | duration_minutes | int32 | Yes | config / quizzes | time_limit_minutes | 3.1 | Alias duration_minutes → time_limit_minutes | Optional | Null/omit rule chưa xác nhận. |
| 5.5 | data.passing_score | Passing score | passing_score | decimal-string | No | config / quizzes | passing_score | 3.1 | Candidate NUMERIC → decimal-string | Required | Scale policy chưa xác nhận. |
| 5.6 | data.questions[] | Questions | questions | QuizQuestion[] | No | Inserted question/choice candidates | N/A | 4.1–4.2 | Preserve request order proposal | Required array | AC-35 says insert Quiz + Questions; nested projection follows Quiz schema. |
| 5.6.1 | data.questions[].id | Question ID | id | int64 | No | Legacy quiz_questions candidate | id | 4.1 | Generated BIGSERIAL → int64 | Required | Legacy candidate. |
| 5.6.2 | data.questions[].text | Question text | text | string | No | questions input | question_text | 4.1 | Candidate alias | Required | Candidate column NOT NULL. |
| 5.6.3 | data.questions[].type | Question type | type | QuestionType | No | SOURCE_REQUIRED | N/A | 4.1 | No legacy column | Required by schema | Pilot field belongs to separate UUID model. |
| 5.6.4 | data.questions[].choices[] | Choice list | choices | QuizChoice[] | No | Legacy quiz_choices candidate | N/A | 4.2 | Output shape not defined | Required by QuizQuestion | Contract omits QuizChoice fields. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> | N/A | 6.1/6.2 | Envelope metadata | Members unspecified | No create metadata declared. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> | N/A | 6.1/6.2 | Request trace | Required | API Guidelines convention. |

## Business code theo status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 201 | DESIGN_RESOURCE_CREATED | Quiz được tạo theo catalog; embedded questions shape còn proposal. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Authentication failure theo contract. |
| 403 | DESIGN_ACCESS_DENIED | Admin role/permission bị từ chối theo contract. |
| 422 | DESIGN_VALIDATION_ERROR | Request validation failure theo contract. |
| 500 | DESIGN_INTERNAL_ERROR | Lỗi nội bộ theo contract. |

## Ví dụ thành công — HTTP 201

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Quiz created.",
  "data": {
    "id": 5101,
    "course_id": 9001,
    "title": "Quiz minh họa",
    "duration_minutes": 30,
    "passing_score": "70.00",
    "questions": []
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000088"
}
~~~

> Ví dụ tập trung vào direct envelope/Quiz fields. questions rỗng minh họa kiểu mảng, không khẳng định API chấp nhận tạo Quiz không có câu hỏi. Question type và QuizChoice output phải được chốt trước khi dùng ví dụ làm implementation fixture.

## Ví dụ lỗi — HTTP 422

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {
    "fieldErrors": [
      {
        "field": "config",
        "code": "INVALID_JSON",
        "message": "config phải chứa JSON hợp lệ."
      }
    ]
  },
  "traceId": "00000000-0000-4000-8000-000000000089"
}
~~~

> API Guidelines yêu cầu fieldErrors trong meta và data=null. Current helper đổi data=None thành {}. Middleware chỉ phát DESIGN_VALIDATION_ERROR khi path nằm trong allowlist; API #88 chưa được wire.
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
