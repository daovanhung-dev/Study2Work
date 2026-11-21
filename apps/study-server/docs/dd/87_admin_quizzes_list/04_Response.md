---
title: "Response"
order: 4
dd_id: "87"
api_name: "Lấy danh sách quiz"
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
| Direct response type | ApiEnvelope<Quiz> theo catalog #87. |
| Local list response | ApiEnvelope<Page<Quiz>>; DERIVED runtime fallback for list intent and query `page`, not owner-approved and not the direct catalog schema. |

## Response fields — contract trực tiếp

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | API catalog/runtime validation | N/A | 5.1/5.2 | 200, 401, 403 hoặc 500 theo direct catalog; local invalid-query fallback also returns 422 | N/A | 422 is a DERIVED local discrepancy. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> | N/A | 5.1/5.2 | true khi thành công, false khi lỗi | Bắt buộc | Reusable envelope. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 5.1/5.2 | Exact code theo nhánh | Bắt buộc | Giữ code catalog. |
| 4 | message | Message | message | string | No | Application | N/A | 5.1/5.2 | Thông điệp an toàn | Nội dung chưa chuẩn hóa | Không lộ thông tin nội bộ. |
| 5 | data | Quiz | data | object (Quiz) | No | Legacy quizzes candidate | N/A | 4.1 | Direct catalog contract only | Required theo contract | Runtime instead returns Page<Quiz> as a DERIVED list fallback. |
| 5.1 | data.id | Quiz ID | id | int64 | No | Legacy quizzes candidate | id | 4.1 | Candidate direct mapping | Bắt buộc theo Quiz | BIGSERIAL candidate; live schema chưa xác minh. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | Legacy quizzes candidate | course_id | 4.1 | Candidate direct mapping | Required theo Quiz | Legacy DDL cho phép NULL; discrepancy. |
| 5.3 | data.title | Quiz title | title | string | No | Legacy quizzes candidate | name | 4.1 | Alias name → title | Bắt buộc theo Quiz | Candidate logical/physical mapping. |
| 5.4 | data.duration_minutes | Thời lượng | duration_minutes | int32 | Yes | Legacy quizzes candidate | time_limit_minutes | 4.1 | Alias time_limit_minutes → duration_minutes | Null hay omit chưa xác nhận | Optional trong Quiz; physical column nullable. |
| 5.5 | data.passing_score | Điểm đạt | passing_score | decimal-string | No | Legacy quizzes candidate | passing_score | 4.1 | NUMERIC(5,2) → decimal-string candidate | Bắt buộc theo Quiz | Scale/rounding chưa được runtime xác nhận. |
| 5.6 | data.questions[] | Danh sách câu hỏi | questions | QuizQuestion[] | No | SOURCE_REQUIRED for full tree | N/A | 4.2 | Direct Quiz schema requires it; local list item returns `[]` | Required theo Quiz schema | Does not assert that source Quiz has no questions; nested data is not queried. |
| 5.6.1 | data.questions[].id | Question ID | id | int64 | No | Legacy quiz_questions candidate | id | 4.2 | Candidate direct mapping | Bắt buộc theo QuizQuestion | BIGSERIAL candidate. |
| 5.6.2 | data.questions[].text | Question text | text | string | No | Legacy quiz_questions candidate | question_text | 4.2 | Alias question_text → text | Bắt buộc theo QuizQuestion | Candidate mapping. |
| 5.6.3 | data.questions[].type | Question type | type | QuestionType | No | Not loaded by API #87 | question_type | 4.2 | Local schema candidate from API #88 migration 013 | Not present because list projection returns `questions=[]` | Values remain DERIVED. |
| 5.6.4 | data.questions[].choices[] | Choice list | choices | QuizChoice[] | No | Not loaded by API #87 | N/A | 4.3 | Local #88 Admin shape is DERIVED | Not present because list projection uses `questions=[]` | Catalog fields remain undefined. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> | N/A | 5.1/5.2 | Envelope metadata | Members chưa khai báo | Current route returns empty meta unless helper adds data. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> | N/A | 5.1/5.2 | Trace từ request middleware | Bắt buộc theo schema | Route is locally wired and tested. |

## Local response — implemented DERIVED fallback

| Path | Type | Proposed source/rule | Status |
|---|---|---|---|
| data.items[] | Quiz[] | Q1 page result; metadata projection plus `questions=[]` | DERIVED; direct catalog returns one Quiz |
| data.pagination.page | int32 | Query page; default 1 | DERIVED and implemented |
| data.pagination.size | int32 | Fixed size 20; no request `size` parameter | DERIVED by #07/#78 precedent |
| data.pagination.total | int64 | Q1C count with identical filters | DERIVED and implemented |
| data.pagination.total_pages | int32 | ceil(total / 20); 0 when total=0 | DERIVED and implemented |

## Business code theo status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Truy vấn quiz theo API catalog; cardinality/page payload chưa được chốt. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Authentication failure theo contract. |
| 403 | DESIGN_ACCESS_DENIED | Role hoặc quiz-management access bị từ chối theo contract. |
| 500 | DESIGN_INTERNAL_ERROR | Lỗi nội bộ theo contract. |
| 422 | DESIGN_VALIDATION_ERROR | Local validation for malformed/out-of-range `course` or `page`; not listed in catalog. |

## Ví dụ thành công — direct catalog Quiz schema (not runtime cardinality)

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Message text is not specified by the contract.",
  "data": {
    "id": 501,
    "course_id": 9001,
    "title": "Quiz minh họa",
    "duration_minutes": 30,
    "passing_score": "70.00",
    "questions": []
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000087"
}
~~~

> Ví dụ này giữ direct catalog schema; route hiện trả Page. `questions: []` không khẳng định Quiz thực không có câu hỏi.

## Ví dụ thành công — local Page<Quiz> runtime fallback

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Quizzes retrieved.",
  "data": {
    "items": [
      {
        "id": 501,
        "course_id": 9001,
        "title": "Quiz minh họa",
        "duration_minutes": 30,
        "passing_score": "70.00",
        "questions": []
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000088"
}
~~~

> This is the implemented DERIVED fallback, not an owner-approved catalog change. `questions=[]` means nested question data is not loaded by this list route.

## Ví dụ lỗi — HTTP 500

~~~json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Không thể truy vấn quiz.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000089"
}
~~~

> Current `error_response` returns `data: null`; focused tests verify the safe envelope. Live SQL/schema behavior remains unverified.
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
