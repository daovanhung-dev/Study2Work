---
title: "Response"
order: 4
dd_id: "36"
api_name: "Xác nhận dữ liệu đã nộp"
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
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4 | Fixed by branch | N/A | Protocol status, not a JSON property. Success 200; catalog errors 401/403/404/500. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4 | true on success; false on error | Always present | Shared ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 4 | Fixed by catalog branch | Always present | Success: DESIGN_RESOURCE_RETRIEVED; errors use the exact catalog code for the branch. |
| 4 | message | Message | message | string | No | N/A | N/A | 4 | Safe branch message | Always present | Exact wording/localization is not defined. |
| 5 | data | Submission | data | object / null | Yes | N/A | N/A | 4 | ApiEnvelope<Submission> on success; null on error | null on error | Error envelope rule from API Guidelines. |
| 5.1 | data.id | Submission ID | id | int64 | No | assignment_submissions (candidate) | id | 3 | Candidate direct mapping | Required by logical schema | Physical source is design-only. |
| 5.2 | data.assignment_id | Assignment ID | assignment_id | int64 | No | assignment_submissions (candidate) | assignment_id | 3 | Candidate direct mapping | Required by logical schema | DDL permits NULL while DB table notes describe this FK as required. |
| 5.3 | data.user_id | Student ID | user_id | int64 | No | assignment_submissions (candidate) | user_id | 3 | Candidate direct mapping | Required by logical schema | Row access policy is unresolved; do not accept this value from the request. |
| 5.4 | data.content | Submission content | content | string | Yes | assignment_submissions (candidate) | content | 3 | Candidate direct mapping | Optional logical field; DDL NULL | Content may be absent; exact serialization rule is not further specified. |
| 5.5 | data.files | Submitted files | files | UploadAsset[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required logical collection; physical mapping unresolved | Logical schema requires the collection; candidate DDL has one file_url column only. |
| 5.5.1 | data.files[].id | Asset ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required by UploadAsset schema | API #34 asset identity and persistence are unresolved. |
| 5.5.2 | data.files[].name | File name | name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required by UploadAsset schema | Asset metadata source is unresolved. |
| 5.5.3 | data.files[].url | File URL | url | uri | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required by UploadAsset schema | Public/signed URL and access policy are unresolved. |
| 5.5.4 | data.files[].content_type | Content type | content_type | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required by UploadAsset schema | Asset metadata source is unresolved. |
| 5.5.5 | data.files[].size_bytes | File size | size_bytes | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required by UploadAsset schema | Asset metadata source is unresolved. |
| 5.5.6 | data.files[].status | Upload status | status | UploadStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | SOURCE_REQUIRED | Required by UploadAsset schema | UploadStatus values and lifecycle are undefined. |
| 5.6 | data.status | Submission status | status | SubmissionStatus | No | assignment_submissions (candidate) | status | 3 | Candidate direct mapping; AC-17 sets the initial state to SUBMITTED | Required by logical schema | Full enum and later lifecycle are not defined. |
| 5.7 | data.submitted_at | Submission time | submitted_at | date-time | No | assignment_submissions (candidate) | submitted_at | 3 | Candidate timestamp serialization | Required by logical schema | DDL uses TIMESTAMP; timezone and serialization policy are not defined. |
| 5.8 | data.score | Score | score | decimal-string | Yes | assignment_submissions (candidate) | score | 3 | Candidate decimal-to-string mapping | Optional logical field; DDL NULL | Visibility/release timing is unresolved; do not infer it from AC-23. |
| 5.9 | data.feedback | Grader feedback | feedback | string | Yes | assignment_submissions (candidate) | feedback | 3 | Candidate direct mapping | Optional logical field; DDL NULL | Visibility/release timing is unresolved; do not infer it from AC-23. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 4 | Empty object unless supported metadata applies | {} in example | No submission-specific metadata shape is defined. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4 | Request correlation UUID | Always present | Shared API Guidelines require trace propagation. |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Submission retrieved (illustrative text).",
  "data": {
    "id": 36001,
    "assignment_id": 35001,
    "user_id": 42,
    "content": "Illustrative submission text",
    "files": [],
    "status": "SUBMITTED",
    "submitted_at": "2026-10-12T05:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000036"
}
~~~

> Values are illustrative. files is shown as an empty array only to demonstrate the required logical shape; it does not assert that a stored submission has no file. Optional score and feedback are omitted as sample values; their response visibility remains unresolved.

## Ví dụ lỗi — HTTP 404

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Submission not found (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000037"
}
~~~

> The example uses the catalog error envelope. Exact message text and whether an inaccessible row is masked as not found are not specified.

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
