---
title: "Response"
order: 4
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
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
| Success business code | DESIGN_RESOURCE_UPDATED |
| Contract data type | ApiEnvelope<Submission> |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | N/A | N/A | 5 | Fixed by branch | Not a JSON field | Success is 200; error statuses are only 401/403/404/422/500. |
| 2 | success | Success flag | success | boolean | No | Envelope branch | N/A | 5 | true on success; false on error | Always present | Shared ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog | Catalog literal | 5 | Fixed by branch | Always present | Success DESIGN_RESOURCE_UPDATED; exact error codes are in 06_Error.md. |
| 4 | message | Message | message | string | No | Application message | N/A | 5 | Safe branch message | Always present | Exact message text is not specified. |
| 5 | data | Submission | data | Submission object or null | Yes | Candidate response mapping | N/A | 4, 5 | Updated Submission on success; null is API Guidelines error expectation | Success contains Submission; errors follow envelope contract | Current response helper serializes omitted error data as {}. |
| 5.1 | data.id | Submission ID | id | int64 | No | assignment_submissions candidate | id | 2, 4 | Direct candidate | Required by reusable Submission | Legacy DDL candidate; live schema unverified. |
| 5.2 | data.assignment_id | Assignment ID | assignment_id | int64 | No | assignment_submissions candidate | assignment_id | 2, 4 | Direct candidate | Required by reusable Submission | Legacy DDL allows NULL. |
| 5.3 | data.user_id | Student ID | user_id | int64 | No | assignment_submissions candidate | user_id | 2, 4 | Direct candidate | Required by reusable Submission | Do not accept this value from the Mentor request. |
| 5.4 | data.content | Submission content | content | string | Yes | assignment_submissions candidate | content | 2, 4 | Direct candidate | Optional; null/omit rule unresolved | Legacy DDL allows NULL. |
| 5.5 | data.files | Student-submitted files | files | UploadAsset[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | No approved asset resolver | Required array in reusable schema | Do not map feedback attachments or legacy file_url into this field. |
| 5.5.1 | data.files[].id | Asset ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Asset relation is not identified. |
| 5.5.2 | data.files[].name | File name | name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Metadata source is not identified. |
| 5.5.3 | data.files[].url | Asset URL | url | uri | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Public/signed URL and access rules are open. |
| 5.5.4 | data.files[].content_type | Content type | content_type | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Metadata source is not identified. |
| 5.5.5 | data.files[].size_bytes | File size | size_bytes | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Metadata source is not identified. |
| 5.5.6 | data.files[].status | Asset status | status | UploadStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4 | SOURCE_REQUIRED | Required by UploadAsset | Enum and lifecycle are open. |
| 5.6 | data.status | Submission status | status | SubmissionStatus | No | assignment_submissions candidate | status | 2, 4 | Preserve stored status | Required; enum members unresolved | AC-23 #56 sets candidate status GRADED; #57 does not update it. |
| 5.7 | data.submitted_at | Submission time | submitted_at | date-time | No | assignment_submissions candidate | submitted_at | 2, 4 | Serialize timestamp | Required | Legacy DDL uses TIMESTAMP; timezone policy is open. |
| 5.8 | data.score | Score | score | decimal-string | Yes | assignment_submissions candidate | score | 2, 4 | Preserve #56 value; do not recalculate | Optional; null/omit rule unresolved | Decimal conversion/rule remains open in #56. |
| 5.9 | data.feedback | Feedback text | feedback | string | Yes | assignment_submissions candidate | feedback | 3, 4 | Candidate value after update | Optional in reusable schema | Candidate source is nullable TEXT; feedback wire key and overwrite/history rule remain open. |
| 6 | meta | Metadata | meta | object | No | Envelope convention | N/A | 5 | Empty object candidate; no pagination | Always present | API #57 has no pagination or operation metadata. |
| 7 | traceId | Trace ID | traceId | uuid | No | Request trace context | N/A | 5 | Propagate request trace | Always present | API Guidelines defines X-Trace-Id propagation. |

## Ví dụ thành công

Các giá trị mang hậu tố PLACEHOLDER minh họa kiểu dữ liệu; chúng không công bố enum member, asset, user hay DB record thật. JSON này minh họa envelope/schema shape, không chứng minh có thể dựng đầy đủ Submission từ source hiện tại.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Feedback đã được lưu.",
  "data": {
    "id": 123,
    "assignment_id": 45,
    "user_id": 67,
    "content": "Nội dung bài làm minh họa.",
    "files": [
      {
        "id": 789,
        "name": "submission.pdf",
        "url": "https://example.invalid/submission.pdf",
        "content_type": "application/pdf",
        "size_bytes": 1024,
        "status": "UPLOAD_STATUS_PLACEHOLDER"
      }
    ],
    "status": "SUBMISSION_STATUS_PLACEHOLDER",
    "submitted_at": "2026-10-24T10:00:00Z",
    "score": "8.00",
    "feedback": "Giải thích rõ hơn cho kết luận ở phần hai."
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000057"
}
~~~

## Ví dụ lỗi

Theo API Guidelines, error data là null; current helper behavior khác như đã ghi ở Overview.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000057"
}
~~~

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
