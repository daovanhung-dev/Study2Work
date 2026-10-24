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

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 4 | Fixed by branch | Not a JSON field | Success 200; errors only 401/403/404/422/500 |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4 | true on success, false on error | Always present | Shared envelope |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | Catalog literal | 4 | Fixed by branch | Always present | Success DESIGN_RESOURCE_UPDATED; error uses exact catalog code |
| 4 | message | Message | message | string | No | N/A | N/A | 4 | Safe branch message | Always present | Wording/localization unspecified |
| 5 | data | Submission | data | object / null | Yes | N/A | N/A | 4 | Submission on success; null on error | API Guidelines expects null on error; current error_response() defaults None to {} | Envelope payload; API #56 route is absent |
| 5.1 | data.id | Submission ID | id | int64 | No | assignment_submissions candidate | id | 3 / 4 | Candidate direct mapping | Required by schema | Legacy DDL candidate; live schema unverified |
| 5.2 | data.assignment_id | Assignment ID | assignment_id | int64 | No | assignment_submissions candidate | assignment_id | 3 / 4 | Candidate direct mapping | Required by schema | DDL permits NULL |
| 5.3 | data.user_id | Student ID | user_id | int64 | No | assignment_submissions candidate | user_id | 3 / 4 | Candidate direct mapping | Required by schema | Do not accept from request |
| 5.4 | data.content | Submission content | content | string | Yes | assignment_submissions candidate | content | 3 / 4 | Candidate direct mapping | Optional; null/omit serialization unspecified | DDL permits NULL |
| 5.5 | data.files | Submitted files | files | UploadAsset[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | Asset resolver SOURCE_REQUIRED | Required collection; empty-array meaning is not established | Legacy DDL has one file_url only |
| 5.5.1 | data.files[].id | Asset ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Asset persistence/source unresolved |
| 5.5.2 | data.files[].name | File name | name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Asset metadata unresolved |
| 5.5.3 | data.files[].url | File URL | url | uri | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Public/signed URL and access policy unresolved |
| 5.5.4 | data.files[].content_type | Content type | content_type | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Asset metadata unresolved |
| 5.5.5 | data.files[].size_bytes | File size | size_bytes | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Asset metadata unresolved |
| 5.5.6 | data.files[].status | Upload status | status | UploadStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | UploadStatus values/lifecycle unresolved |
| 5.6 | data.status | Submission status | status | SubmissionStatus | No | assignment_submissions candidate | status | 3 / 4 | Candidate stored value; AC-23 target GRADED | Required by schema | Full enum and live status constraint unverified |
| 5.7 | data.submitted_at | Submission time | submitted_at | date-time | No | assignment_submissions candidate | submitted_at | 3 / 4 | Candidate timestamp serialization | Required by schema | Timezone/serialization policy unspecified |
| 5.8 | data.score | Score | score | decimal-string | Yes | assignment_submissions candidate | score | 3 / 4 | Numeric-to-string conversion SOURCE_REQUIRED | Optional logical field | Request score is int32; scale/format and DB conversion unresolved |
| 5.9 | data.feedback | Grader feedback | feedback | string | Yes | assignment_submissions candidate | feedback | 3 / 4 | Candidate direct mapping; API #56 does not update it | Optional; null/omit rule unresolved | Separate API #57 owns the feedback mutation |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 4 | Empty object unless shared runtime supplies metadata | {} in example | No API-specific meta shape |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4 | Request trace | Always present | Shared envelope convention |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Submission grade saved (illustrative text).",
  "data": {
    "id": 56001,
    "assignment_id": 35001,
    "user_id": 42001,
    "files": [],
    "status": "GRADED",
    "submitted_at": "2026-10-24T09:30:00Z",
    "score": "8"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000056"
}
~~~

> Values are illustrative. files is an empty array only to show the required logical collection shape; it does not assert that a stored submission has no file. The score string shows the response type only; the conversion rule is unresolved. Optional feedback is omitted and is not changed by API #56.

## Ví dụ lỗi — HTTP 404

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Submission not found (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000057"
}
~~~

> Error data and message follow the API Guidelines/catalog envelope; exact text is unspecified.

> Current-source discrepancy: app.core.responses.error_response() serializes data as {} when its data argument is None. The API #56 endpoint is not wired; resolve this helper/contract mismatch before claiming the error example as runtime behavior.
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
