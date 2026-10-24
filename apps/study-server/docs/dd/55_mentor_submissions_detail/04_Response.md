---
title: "Response"
order: 4
dd_id: "55"
api_name: "Lấy bài làm và rubric Mentor"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---:|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | integer | No | N/A | N/A | 5 | Fixed by branch | N/A | Success HTTP 200; errors 401/403/404/500 per catalog. |
| 2 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 5 | `true` success; `false` error | Always present | Shared `ApiEnvelope`. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | API catalog | N/A | 5 | Fixed by branch | Always present | Exact catalog code. |
| 4 | `message` | Message | `message` | string | No | Application message | N/A | 5 | Safe branch message | Always present | Wording/localization not specified. |
| 5 | `data` | Submission | `data` | object / null | Error: null theo guideline | N/A | N/A | 5 | `ApiEnvelope<Submission>` on success | Null on error per guideline | Current helper emits `{}` for absent data; discrepancy. |
| 5.1 | `data.id` | Submission ID | `id` | int64 | No | `assignment_submissions` (candidate) | `id` | 4 | Direct candidate mapping | Required | Legacy DDL primary key; live schema unverified. |
| 5.2 | `data.assignment_id` | Assignment ID | `assignment_id` | int64 | No | `assignment_submissions` (candidate) | `assignment_id` | 4 | Direct candidate mapping | Required; DDL permits NULL | Orphan/null handling is open. |
| 5.3 | `data.user_id` | Student ID | `user_id` | int64 | No | `assignment_submissions` (candidate) | `user_id` | 4 | Direct candidate mapping | Required; DDL permits NULL | Do not join/return unrelated student profile fields. |
| 5.4 | `data.content` | Bài làm dạng text | `content` | string | Optional | `assignment_submissions` (candidate) | `content` | 4 | Preserve stored text | Null-versus-omit unspecified | Optional in reusable `Submission`; candidate column nullable. |
| 5.5 | `data.files` | Tệp đính kèm | `files` | `UploadAsset[]` | No | No approved relation | N/A | 4 / SOURCE_REQUIRED | No approved transform | Do not fabricate assets or force `[]` for real data | Contract field; candidate DDL has one `file_url` only. |
| 5.5.1 | `data.files[].id` | Asset ID | `id` | int64 | No | No approved relation | N/A | 4 / SOURCE_REQUIRED | None approved | SOURCE_REQUIRED | No asset identity source. |
| 5.5.2 | `data.files[].name` | Tên tệp | `name` | string | No | No approved relation | N/A | 4 / SOURCE_REQUIRED | None approved | SOURCE_REQUIRED | No persisted name source. |
| 5.5.3 | `data.files[].url` | URL tệp | `url` | uri | No | `assignment_submissions` (candidate) | `file_url` | 4 / SOURCE_REQUIRED | Do not treat URL as complete asset record | URL access policy unspecified | A single URL cannot define an `UploadAsset[]`. |
| 5.5.4 | `data.files[].content_type` | MIME type | `content_type` | string | No | No approved relation | N/A | 4 / SOURCE_REQUIRED | None approved | SOURCE_REQUIRED | Not present in candidate submission DDL. |
| 5.5.5 | `data.files[].size_bytes` | Kích thước byte | `size_bytes` | int64 | No | No approved relation | N/A | 4 / SOURCE_REQUIRED | None approved | SOURCE_REQUIRED | Not present in candidate submission DDL. |
| 5.5.6 | `data.files[].status` | Trạng thái asset | `status` | UploadStatus | No | No approved relation | N/A | 4 / SOURCE_REQUIRED | None approved | SOURCE_REQUIRED | Enum/lifecycle source absent for this relation. |
| 5.6 | `data.status` | Trạng thái submission | `status` | SubmissionStatus | No | `assignment_submissions` (candidate) | `status` | 4 | Preserve candidate value | Required; legacy column permits NULL | AC-17 names `SUBMITTED`; complete enum is unspecified. |
| 5.7 | `data.submitted_at` | Thời điểm nộp | `submitted_at` | date-time | No | `assignment_submissions` (candidate) | `submitted_at` | 4 | Serialize timestamp as ISO-8601 candidate | Required | Legacy TIMESTAMP lacks zone/precision policy. |
| 5.8 | `data.score` | Điểm | `score` | decimal-string | Optional | `assignment_submissions` (candidate) | `score` | 4 | Candidate NUMERIC(6,2) to decimal-string | Omit/null policy unspecified | API #56 input uses `int32`; range/scale alignment unresolved. |
| 5.9 | `data.feedback` | Feedback | `feedback` | string | Optional | `assignment_submissions` (candidate) | `feedback` | 4 | Preserve stored text | Omit/null and Student disclosure timing unspecified | Candidate nullable column. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope convention | N/A | 5 | Empty object candidate | `{}` if no metadata | No pagination/extra metadata contract. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Request trace | N/A | 5 | Propagate validated/generated trace ID | Always present | API Guidelines use `X-Trace-Id`. |

> AC-23 node says đọc rubric, nhưng reusable `Submission` không khai báo `rubric`. DD này giữ nguyên `ApiEnvelope<Submission>` và không thêm field; contract cần được sửa đồng bộ trước khi client có thể nhận rubric từ API #55.

## Ví dụ thành công

Payload minh họa shape contract cho một submission chưa chấm. `files: []` chỉ minh họa kiểu array; khả năng trả array rỗng và asset lookup thật chưa được nguồn xác nhận. Không có `score`/`feedback` vì hai field optional; đây không xác nhận null/omit policy.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Lấy bài làm thành công.",
  "data": {
    "id": 7301,
    "assignment_id": 120,
    "user_id": 8802,
    "content": "Nội dung bài làm minh họa.",
    "files": [],
    "status": "SUBMITTED",
    "submitted_at": "2026-10-24T09:30:00Z"
  },
  "meta": {},
  "traceId": "4fbb48a1-ccaa-4719-a8de-4a75439d0a6f"
}
~~~

`SUBMITTED` được AC-17 nêu làm trạng thái sau khi nộp; enum đầy đủ của `SubmissionStatus` vẫn chưa có. `rubric` không xuất hiện vì không thuộc reusable schema.

## Ví dụ lỗi

Ví dụ theo API Guidelines (`data:null`). Current Study helper serialize absent error data thành `{}`; endpoint #55 chưa được wiring nên đây là expected/current discrepancy, không phải runtime result của API #55.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy bài nộp.",
  "data": null,
  "meta": {},
  "traceId": "4fbb48a1-ccaa-4719-a8de-4a75439d0a6f"
}
~~~

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
