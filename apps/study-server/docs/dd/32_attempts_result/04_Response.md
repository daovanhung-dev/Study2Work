---
title: "Response"
order: 4
dd_id: "32"
api_name: "Lấy điểm/kết quả được phép xem"
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
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5.1 | Fixed by response branch. | N/A | Success 200; error statuses follow API #32 catalog. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 5.1 | true on success; false on error. | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 5.1 | DESIGN_RESOURCE_RETRIEVED on success. | N/A | API catalog. |
| 4 | message | Message | message | string | No | N/A | N/A | 5.1 | Safe client message. | Exact message/localization SOURCE_REQUIRED. | ApiEnvelope field. |
| 5 | data.id | Attempt ID | id | int64 | No | quiz_attempts | id | 4 | Candidate projection. | N/A | Logical QuizAttempt field; design-only mapping. |
| 6 | data.quiz_id | Quiz ID | quiz_id | int64 | No | quiz_attempts | quiz_id | 4 | Candidate projection. | N/A | Logical QuizAttempt field; design-only mapping. |
| 7 | data.status | Attempt status | status | AttemptStatus | No | quiz_attempts | status | 3 | AC-16 result branches name GRADED and PENDING_GRADE. | N/A | Other values and full enum are SOURCE_REQUIRED. |
| 8 | data.started_at | Start time | started_at | date-time | No | quiz_attempts | started_at | 4 | Candidate timestamp projection. | N/A | Serialization and timezone policy not defined. |
| 9 | data.submitted_at | Submission time | submitted_at | date-time | Yes | quiz_attempts | submitted_at | 4 | Candidate timestamp projection. | Omit/null policy SOURCE_REQUIRED. | Nullable in DB design. |
| 10 | data.score | Attempt score | score | decimal-string | Yes | quiz_attempts | score | 3 | Candidate aggregate score for a graded result. | Omit/null/partial policy for PENDING_GRADE SOURCE_REQUIRED. | AC-16 says read score; formula is owned by grading flow/API #31. |
| 11 | data.answers[] | Answers | answers | QuizAnswer[] | No | quiz_answers | N/A | 4 | Candidate collection for the attempt. | Empty array or populated collection; exact projection SOURCE_REQUIRED. | Required by reusable QuizAttempt schema. |
| 12 | data.answers[].question_id | Question ID | question_id | int64 | No | quiz_answers | question_id | 4 | Candidate projection per answer. | N/A | Logical QuizAnswer field. |
| 13 | data.answers[].choice_ids[] | Selected choice IDs | choice_ids | int64[] | Yes | quiz_answers | choice_id | 4 | No approved conversion from physical one-choice rows to logical array. | SOURCE_REQUIRED | Logical schema versus physical design discrepancy. |
| 14 | data.answers[].text_answer | Text answer | text_answer | string | Yes | N/A | N/A | 4 | No physical text-answer column is defined. | SOURCE_REQUIRED | Logical field has no candidate persistence column. |
| 15 | data.answers[].correct | Answer correctness | correct | boolean | Yes | quiz_answers | is_correct | 4 | Candidate projection only after grading, if allowed. | Disclosure policy SOURCE_REQUIRED. | Do not expose answer key from quiz_choices. |
| 16 | data.answers[].score | Per-answer score | score | decimal-string | Yes | quiz_answers | score_received | 4 | Candidate projection if allowed. | Disclosure and numeric formatting SOURCE_REQUIRED. | DB design precision differs from attempt score. |
| 17 | meta | Metadata | meta | object | No | N/A | N/A | 5.1 | Envelope metadata. | Empty object when no metadata is supplied. | ApiEnvelope field. |
| 18 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 5.1 | Propagated/generated under shared API convention. | N/A | Runtime serialization is not verified. |

### Nhánh GRADED — ví dụ minh họa

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Result retrieved (illustrative text).",
  "data": {
    "id": 9001,
    "quiz_id": 501,
    "status": "GRADED",
    "started_at": "2026-10-12T08:30:00Z",
    "submitted_at": "2026-10-12T09:00:00Z",
    "score": "8.50",
    "answers": [
      {
        "question_id": 301
      }
    ]
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000032"
}
~~~

### Nhánh PENDING_GRADE — ví dụ minh họa

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Result retrieved (illustrative text).",
  "data": {
    "id": 9001,
    "quiz_id": 501,
    "status": "PENDING_GRADE",
    "started_at": "2026-10-12T08:30:00Z",
    "submitted_at": "2026-10-12T09:00:00Z",
    "answers": [
      {
        "question_id": 301
      }
    ]
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000032"
}
~~~

The examples show the documented status branches and required envelope/QuizAttempt fields only. They do not settle whether score, correctness, per-answer score, selected answer values or feedback are returned while grading is pending or complete.

## Ví dụ lỗi

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Attempt not found (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000032"
}
~~~

The error example illustrates the envelope. It does not decide whether an attempt owned by another Student maps to 403 or is masked as 404.
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
