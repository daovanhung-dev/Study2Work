---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
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

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Transform / null rule |
|---:|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | HTTP 200 success; catalog errors 401/403/404/422/500 |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | true on success, false on error |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | Catalog literal | DESIGN_RESOURCE_UPDATED on success; exact catalog code on error |
| 4 | message | Message | message | string | No | N/A | N/A | Safe branch message |
| 5 | data | Submission | data | object / null | Yes | N/A | N/A | Submission on success; null on error |
| 5.1 | data.id | Submission ID | id | int64 | No | assignment_submissions candidate | id | Direct mapping; required by response model |
| 5.2 | data.assignment_id | Assignment ID | assignment_id | int64 | No | assignment_submissions candidate | assignment_id | Direct mapping; required |
| 5.3 | data.user_id | Student ID | user_id | int64 | No | assignment_submissions candidate | user_id | Direct mapping; never request-controlled |
| 5.4 | data.content | Submission content | content | string | Yes | assignment_submissions candidate | content | Null omitted in success response |
| 5.5 | data.files | Submitted files | files | UploadAsset[] | No | uploads candidate | id, file_name, url, content_type, size_bytes, status | Scoped exact URL/owner/purpose/course lookup; zero or one asset, otherwise [] |
| 5.6 | data.status | Submission status | status | SubmissionStatus | No | assignment_submissions candidate | status | Updated to GRADED |
| 5.7 | data.submitted_at | Submission time | submitted_at | date-time | No | assignment_submissions candidate | submitted_at | Shared Submission mapping |
| 5.8 | data.score | Score | score | decimal-string | Yes | assignment_submissions candidate | score | Decimal returned by DB is serialized as string; null omitted |
| 5.9 | data.feedback | Grader feedback | feedback | string | Yes | assignment_submissions candidate | feedback | Preserved from the locked row; null omitted; not updated by #56 |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | Shared envelope metadata |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | Request trace |

rubric_items is not part of the Submission response and is not persisted. The legacy DDL contains no rubric target or approved relation.

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Submission grade saved.",
  "data": {
    "id": 56001,
    "assignment_id": 35001,
    "user_id": 42001,
    "files": [],
    "status": "GRADED",
    "submitted_at": "2026-10-24T09:30:00Z",
    "score": "8.00"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000056"
}
~~~

Values are illustrative. The database driver may represent the NUMERIC score with a different equivalent scale; the application serializes its returned value as a decimal string. files=[] means no matching UploadAsset metadata row was returned for this illustrative response.

## Ví dụ lỗi — HTTP 422

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Score is outside the assignment range.",
  "data": null,
  "meta": {
    "fieldErrors": [
      {
        "field": "score",
        "code": "VALUE_OUT_OF_RANGE",
        "message": "Score must be between zero and the assignment maximum."
      }
    ]
  },
  "traceId": "00000000-0000-4000-8000-000000000057"
}
~~~

The numeric range rule is DERIVED. The response helper emits data=null when error data is omitted, consistent with the API Guidelines.
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
