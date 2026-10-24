---
title: "Response"
order: 4
dd_id: "54"
api_name: "Lấy submissions"
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
| Success business code | DESIGN_RESOURCE_RETRIEVED |
| Contract data type | ApiEnvelope<Submission> |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 4 | Fixed by branch | N/A | Success 200; error statuses exactly those in catalog. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 4 | true on success; false on error | Always present | Shared ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | Catalog literal | 4 | Fixed by branch | Always present | Keep exact DESIGN_* code. |
| 4 | message | Message | message | string | No | Application | Safe message | 4 | Branch message | Always present | Exact text/language unspecified. |
| 5 | data | Submission | data | object / null | Yes | N/A | N/A | 3/4 | ApiEnvelope<Submission> on success; null expected on error | Null on error per API Guidelines | Singular contract conflicts with list endpoint semantics. |
| 5.1 | data.id | Submission ID | id | int64 | No | assignment_submissions (candidate) | id | 2/3 | Candidate direct mapping | Required by logical schema | BIGSERIAL candidate; live schema not verified. |
| 5.2 | data.assignment_id | Assignment ID | assignment_id | int64 | No | assignment_submissions (candidate) | assignment_id | 2/3 | Candidate direct mapping | Required logically; DDL permits NULL | Guide/DDL nullability discrepancy. |
| 5.3 | data.user_id | Student ID | user_id | int64 | No | assignment_submissions (candidate) | user_id | 2/3 | Candidate direct mapping | Required logically; DDL permits NULL | Do not derive display name; schema has no student object. |
| 5.4 | data.content | Submission content | content | string | Yes | assignment_submissions (candidate) | content | 2/3 | Preserve candidate value | Null/omit serialization unspecified | Nullable in reusable schema and candidate DDL. |
| 5.5 | data.files | Submitted files | files | UploadAsset[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved mapping | Array/null/empty policy needs confirmation | Candidate file_url is not an UploadAsset array. |
| 5.5.1 | data.files[].id | Asset ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved lookup | Required by UploadAsset | No source-backed asset ID relation. |
| 5.5.2 | data.files[].name | File name | name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved lookup | Required by UploadAsset | No metadata source. |
| 5.5.3 | data.files[].url | Asset URL | url | uri | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | file_url is insufficient | Required by UploadAsset | Access/signing policy unresolved. |
| 5.5.4 | data.files[].content_type | Content type | content_type | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved lookup | Required by UploadAsset | No metadata source. |
| 5.5.5 | data.files[].size_bytes | File size | size_bytes | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved lookup | Required by UploadAsset | No metadata source. |
| 5.5.6 | data.files[].status | Upload status | status | UploadStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3 | No approved lookup | Required by UploadAsset | Enum and lifecycle not defined. |
| 5.6 | data.status | Submission status | status | SubmissionStatus | No | assignment_submissions (candidate) | status | 2/3 | Candidate stored value | Enum members/lifecycle unresolved | AC-17 states initial SUBMITTED only. |
| 5.7 | data.submitted_at | Submission time | submitted_at | date-time | No | assignment_submissions (candidate) | submitted_at | 2/3 | Candidate timestamp serialization | Zone/precision/format policy unresolved | DDL type is TIMESTAMP. |
| 5.8 | data.score | Score | score | decimal-string | Yes | assignment_submissions (candidate) | score | 2/3 | NUMERIC-to-decimal-string transform SOURCE_REQUIRED | Omit/null behavior not specified | Candidate NUMERIC(6,2), nullable. |
| 5.9 | data.feedback | Feedback | feedback | string | Yes | assignment_submissions (candidate) | feedback | 2/3 | Preserve candidate value | Null/omit policy not specified | Candidate nullable; disclosure policy not specified. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 4 | Empty object candidate | No pagination fields defined | Do not add page/count. |
| 7 | traceId | Trace ID | traceId | uuid | No | Trace context | Request trace ID | 4 | Propagate UUID | Always present by shared convention | Current route absent. |

### Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Submissions retrieved (illustrative text).",
  "data": {
    "id": 54001,
    "assignment_id": 1201,
    "user_id": 804,
    "content": "Illustrative submission text.",
    "files": [],
    "status": "SUBMITTED",
    "submitted_at": "2026-10-24T09:30:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000054"
}
~~~

IDs, content and timestamp are illustrative. `SUBMITTED` is evidenced as AC-17's initial state, not the full SubmissionStatus enum. The empty `files` array only demonstrates the declared array type; it does not decide when empty files are returned. `data` is shown as one object to preserve the catalog contract; list cardinality remains open.

### Ví dụ lỗi — HTTP 409

~~~json
{
  "success": false,
  "businessCode": "DESIGN_STATE_CONFLICT",
  "message": "State conflict (illustrative text).",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000055"
}
~~~

The catalog declares 409 but AC-23 does not define its trigger. `data: null` follows API Guidelines; current `error_response()` defaults omitted/None data to `{}`, so the future route needs an explicit compatibility decision.

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
