---
title: "Response"
order: 4
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
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
| Success business code | `DESIGN_RESOURCE_UPDATED` |
| Contract data type | `ApiEnvelope<SupportRequest>` |

## Response fields

| No | Path | Logical name | Physical source | Type | Nullable | Mapping/rule | Remarks |
|---:|---|---|---|---|---:|---|---|
| 1 | `HTTPStatus` | HTTP Status | Route | integer | No | Success fixed at 200 | Errors use catalog status. |
| 2 | `success` | Success flag | Envelope | boolean | No | `true` on success | Always present. |
| 3 | `businessCode` | Business code | Catalog | string | No | `DESIGN_RESOURCE_UPDATED` | Error branch uses exact catalog code. |
| 4 | `message` | Message | Application | string | No | Safe fixed text | No contract-specific message ID. |
| 5 | `data` | Support request | Reusable model | SupportRequest | No | One mapped request | Catalog declares singleton object. |
| 6 | `data.id` | Request ID | `support_requests.id` | int64 | No | BIGINT → int64 | Local migration 008; live schema unverified. |
| 7 | `data.course_id` | Course ID | `support_requests.course_id` | int64 | No | BIGINT → int64 | Course owner scope uses `courses.mentor_id`. |
| 8 | `data.student` | Student | `users` | UserSummary | No | Project `id`, `full_name`, `avatar_url` | Required parent projection. |
| 9 | `data.student.id` | Student ID | `support_requests.student_id` / `users.id` | int64 | No | FK must match public user row | Numeric local fallback. |
| 10 | `data.student.full_name` | Student name | `users.full_name` | string | No | Direct projection | Required by response model. |
| 11 | `data.student.avatar_url` | Student avatar | `users.avatar_url` | uri? | Yes | Direct projection | `null` omitted by route serializer. |
| 12 | `data.status` | Request status | `support_requests.status` | string | No | Active state → `RESOLVED`; resolved retry unchanged | Transition matrix is DERIVED. |
| 13 | `data.messages[]` | Thread | `support_messages` | SupportMessage[] | No | API #59 owner-scoped read, chronological order | #61 does not mutate messages. |
| 14 | `data.messages[].id` | Message ID | `support_messages.id` | int64 | No | BIGINT → int64 | Local migration 008. |
| 15 | `data.messages[].author` | Author | `users` | UserSummary | No | Public author projection | Author must map to numeric user ID. |
| 16 | `data.messages[].author.id` | Author ID | `support_messages.author_id` / `users.id` | int64 | No | FK must match public user row | No JWT subject is emitted. |
| 17 | `data.messages[].author.full_name` | Author name | `users.full_name` | string | No | Direct projection | Required by response model. |
| 18 | `data.messages[].author.avatar_url` | Author avatar | `users.avatar_url` | uri? | Yes | Direct projection | `null` omitted by route serializer. |
| 19 | `data.messages[].content` | Message content | `support_messages.content` | string | No | Direct projection | #61 preserves current thread. |
| 20 | `data.messages[].attachments[]` | Attachments | `support_message_uploads` + `uploads` | UploadAsset[] | No | Reuse API #59 scoped resolver | Empty list when no links. |
| 21 | `data.messages[].attachments[].id` | Attachment ID | `uploads.id` | int64 | No | BIGINT → int64 | Only matching link/upload rows are included. |
| 22 | `data.messages[].attachments[].name` | Attachment name | `uploads.file_name` | string | No | Map to `name` | Existing UploadAsset response model. |
| 23 | `data.messages[].attachments[].url` | Attachment URL | `uploads.url` | uri | No | Direct local metadata projection | No new signed URL generation. |
| 24 | `data.messages[].attachments[].content_type` | Content type | `uploads.content_type` | string | No | Direct projection | Existing local resolver. |
| 25 | `data.messages[].attachments[].size_bytes` | Attachment size | `uploads.size_bytes` | int64 | No | BIGINT → int64 | Existing local resolver. |
| 26 | `data.messages[].attachments[].status` | Upload status | `uploads.status` | string | No | Existing scoped resolver requires `UPLOADED` | No status conversion. |
| 27 | `data.messages[].created_at` | Message creation time | `support_messages.created_at` | date-time | No | Direct projection; order by timestamp then ID | Local migration 008. |
| 28 | `data.created_at` | Request creation time | `support_requests.created_at` | date-time | No | Direct projection | Required by response model. |
| 29 | `data.resolved_at` | Resolution time | `support_requests.resolved_at` | date-time | Yes in shared model | DB `CURRENT_TIMESTAMP` on first transition | New transitions return a timestamp; a pre-existing resolved row may remain null and is preserved on retry. |
| 30 | `meta` | Metadata | Envelope | object | No | `{}` | No pagination metadata. |
| 31 | `traceId` | Trace ID | Trace middleware | uuid | No | Propagate or generate | Also returned in `X-Trace-Id`. |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Support request resolved.",
  "data": {
    "id": 59001,
    "course_id": 120,
    "student": {
      "id": 2042,
      "full_name": "Nguyễn An"
    },
    "status": "RESOLVED",
    "messages": [
      {
        "id": 90001,
        "author": {
          "id": 604,
          "full_name": "Trần Mentor"
        },
        "content": "Mình đã gửi hướng dẫn xử lý cho bạn.",
        "attachments": [],
        "created_at": "2026-10-24T08:30:00Z"
      }
    ],
    "created_at": "2026-10-24T08:20:00Z",
    "resolved_at": "2026-10-25T08:40:00Z"
  },
  "meta": {},
  "traceId": "123e4567-e89b-42d3-a456-426614174000"
}
```

Shape theo catalog và reusable model #58–#60. Giá trị cụ thể chỉ minh họa; local mapping là fallback DERIVED và chưa chứng minh live data.

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Support request cannot be resolved in its current state.",
  "data": null,
  "meta": {},
  "traceId": "123e4567-e89b-42d3-a456-426614174000"
}
```

422 dùng catalog code cho path/state validation; current `error_response` serialize `data: null` và chi tiết field validation dưới `meta.fieldErrors`.
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
