---
title: "Response"
order: 4
dd_id: "30"
api_name: "Autosave/lưu câu trả lời"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json per shared API envelope convention. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4.1 | Fixed by response branch | N/A | Success is 200; errors follow API #30 catalog row. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4.1 | true on success | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 4.1 | DESIGN_RESOURCE_UPDATED | N/A | API catalog. |
| 4 | message | Message | message | string | No | N/A | N/A | 4.1 | Message policy | N/A | Exact text/localization is not defined in the API catalog. |
| 5 | data.id | Attempt ID | id | int64 | No | quiz_attempts | id | 3 | Candidate projection | N/A | Logical QuizAttempt; physical/runtime mapping is design-only. |
| 6 | data.quiz_id | Quiz ID | quiz_id | int64 | No | quiz_attempts | quiz_id | 3 | Candidate projection | N/A | Logical QuizAttempt; physical FK nullability differs between table design and DDL. |
| 7 | data.status | Attempt status | status | AttemptStatus | No | quiz_attempts | status | 3 | Candidate projection; API #30 state transition is not specified. | SOURCE_REQUIRED | Full enum and whether autosave requires IN_PROGRESS are unresolved. |
| 8 | data.started_at | Start time | started_at | date-time | No | quiz_attempts | started_at | 3 | Candidate projection | SOURCE_REQUIRED | Timestamp serialization policy is not defined in the API catalog. |
| 9 | data.submitted_at | Submission time | submitted_at | date-time | Yes | quiz_attempts | submitted_at | 3 | Candidate projection | Omit or null per approved response policy. | Optional in logical QuizAttempt; physical column nullable in DDL. |
| 10 | data.score | Attempt score | score | decimal-string | Yes | quiz_attempts | score | 3 | Candidate projection | Omit or null per approved response policy. | Optional logical field; API #30 does not define grading. |
| 11 | data.answers[] | Answers | answers | QuizAnswer[] | No | quiz_answers | N/A | 3 | Candidate projection of attempt answers. | Exact array contents SOURCE_REQUIRED. | Required by logical QuizAttempt; whether response returns all answers or a subset is open. |
| 12 | data.answers[].question_id | Question ID | question_id | int64 | No | quiz_answers | question_id | 3 | Candidate projection | N/A | Required in logical QuizAnswer; physical question relationship is design-only. |
| 13 | data.answers[].choice_ids[] | Selected choice IDs | choice_ids | int64[] | Yes | quiz_answers | choice_id | 3 | No confirmed conversion from one physical choice_id to logical array. | SOURCE_REQUIRED | Logical schema permits array; DDL stores one choice ID per row. |
| 14 | data.answers[].text_answer | Text answer | text_answer | string | Yes | N/A | N/A | 3 | No physical text answer column is defined. | SOURCE_REQUIRED | Logical schema allows this field; storage/schema mapping is absent. |
| 15 | data.answers[].correct | Correctness | correct | boolean | Yes | quiz_answers | is_correct | API #31 after autosave | Not calculated by API #30. | Do not include unless explicitly approved. | Logical field is optional; exposing correctness before submission is not specified. |
| 16 | data.answers[].score | Answer score | score | decimal-string | Yes | quiz_answers | score_received | API #31 after autosave | Not calculated by API #30. | Do not include unless explicitly approved. | Logical field is optional; autosave grading/value policy is not specified. |
| 17 | meta | Metadata | meta | object | No | N/A | N/A | 4.1 | Envelope metadata | {} when no metadata is supplied. | ApiEnvelope field. |
| 18 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4.1 | Generated/propagated according to common API contract. | N/A | ApiEnvelope field; API #30 route does not exist yet. |

## Ví dụ thành công

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Answer saved (illustrative text).",
  "data": {
    "id": 9001,
    "quiz_id": 501,
    "status": "IN_PROGRESS",
    "started_at": "2026-10-12T08:30:00Z",
    "answers": [
      {
        "question_id": 301
      }
    ]
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000030"
}
~~~

This example illustrates the envelope and a schema-compatible QuizAttempt shape only. The saved answer representation, status policy, full-versus-partial answer projection, and optional-field null behavior remain unresolved. correct and answer score are omitted.

## Ví dụ lỗi

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Resource not found (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000030"
}
~~~

The error envelope follows the API catalog and shared API guidelines. The exact resource lookup condition and message text are not defined.
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

