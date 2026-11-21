---
title: "Response"
order: 4
dd_id: "58"
api_name: "Lấy support requests"
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
| Contract data type | ApiEnvelope<SupportRequest[]> |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 6 | Fixed by branch | N/A | Success 200; error statuses đúng catalog. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 6 | true success; false error | Luôn có | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog | Literal catalog | 6 | Fixed by branch | Luôn có | Giữ nguyên DESIGN_* code. |
| 4 | message | Message | message | string | No | Application | Safe message | 6 | Branch message | Luôn có | `Support requests retrieved.` hoặc `No support requests found.` |
| 5 | data | Support requests | data | SupportRequest[] | No | support_requests | Selected rows | 5 | Mảng ordered SupportRequest | Rỗng khi không có kết quả | Collection fallback; không phân trang. |
| 6 | data[].id | Request ID | id | int64 | No | support_requests | id | 5.1 | Direct BIGINT → int64 | Không null | Legacy BIGINT fallback; live schema chưa xác minh. |
| 7 | data[].course_id | Course ID | course_id | int64 | No | support_requests | course_id | 5.1 | Direct BIGINT → int64 | Không null | FK tới courses.id. |
| 8 | data[].student | Student | student | UserSummary | No | users | Joined by student_id | 5.1 | Object projection | Không null | INNER JOIN users theo schema FK. |
| 9 | data[].student.id | Student ID | id | int64 | No | users | id | 5.1 | Direct BIGINT → int64 | Không null | Numeric Study identity. |
| 10 | data[].student.full_name | Student name | full_name | string | No | users | full_name | 5.1 | Direct | Không null | users.full_name là NOT NULL trong legacy DDL. |
| 11 | data[].student.avatar_url | Student avatar URL | avatar_url | uri | Yes | users | avatar_url | 5.1 | Direct | Omit nếu NULL | Route response model loại field None. |
| 12 | data[].status | Request status | status | SupportStatus | No | support_requests | status | 5.1 | Direct exact string | Không null | DDL check: OPEN, IN_PROGRESS, WAITING_LEARNER, RESOLVED, CANCELLED. |
| 13 | data[].messages[] | Messages | messages | SupportMessage[] | No | support_messages | request_id | 5.2 | Chronological array | Rỗng nếu request chưa có message | #58 loads full thread per reusable schema. |
| 14 | data[].messages[].id | Message ID | id | int64 | No | support_messages | id | 5.2 | Direct BIGINT → int64 | Không null | Stable within request ordering. |
| 15 | data[].messages[].author | Author | author | UserSummary | No | users | Joined by author_id | 5.2 | Object projection | Không null | Required author FK. |
| 16 | data[].messages[].author.id | Author ID | id | int64 | No | users | id | 5.2 | Direct BIGINT → int64 | Không null | Numeric Study identity. |
| 17 | data[].messages[].author.full_name | Author name | full_name | string | No | users | full_name | 5.2 | Direct | Không null | Legacy DDL requires value. |
| 18 | data[].messages[].author.avatar_url | Author avatar URL | avatar_url | uri | Yes | users | avatar_url | 5.2 | Direct | Omit nếu NULL | Route response model loại field None. |
| 19 | data[].messages[].content | Message content | content | string | No | support_messages | content | 5.2 | Direct | Không null | Message text. |
| 20 | data[].messages[].attachments[] | Attachments | attachments | UploadAsset[] | No | support_message_uploads | upload_id, asset_position | 5.2 | Ordered asset projection | Rỗng nếu không có link | Broken or out-of-scope link causes safe 500. |
| 21 | data[].messages[].attachments[].id | Attachment ID | id | int64 | No | uploads | id | 5.2 | Direct BIGINT → int64 | Không null | Must match author/course/purpose/status. |
| 22 | data[].messages[].attachments[].name | Attachment name | name | string | No | uploads | file_name | 5.2 | file_name → name | Không null | Legacy UploadAsset column. |
| 23 | data[].messages[].attachments[].url | Attachment URL | url | uri | No | uploads | url | 5.2 | Direct | Không null | Existing API #34 stores public URL. |
| 24 | data[].messages[].attachments[].content_type | Content type | content_type | string | No | uploads | content_type | 5.2 | Direct | Không null | Existing API #34 metadata. |
| 25 | data[].messages[].attachments[].size_bytes | Size in bytes | size_bytes | int64 | No | uploads | size_bytes | 5.2 | Direct BIGINT → int64 | Không null | Existing API #34 metadata. |
| 26 | data[].messages[].attachments[].status | Upload status | status | UploadStatus | No | uploads | status | 5.2 | Direct | `UPLOADED` | API #34 DDL permits only UPLOADED. |
| 27 | data[].messages[].created_at | Message creation time | created_at | date-time | No | support_messages | created_at | 5.2 | ISO date-time serialization | Không null | Order ASC, id ASC. |
| 28 | data[].created_at | Request creation time | created_at | date-time | No | support_requests | created_at | 5.1 | ISO date-time serialization | Không null | Request order DESC, id DESC. |
| 29 | data[].resolved_at | Resolved time | resolved_at | date-time | Yes | support_requests | resolved_at | 5.1 | ISO date-time serialization | Omit nếu NULL | Follows current exclude-none convention. |
| 30 | meta | Metadata | meta | object | No | Envelope convention | N/A | 6 | Empty object | `{}` | No pagination contract. |
| 31 | traceId | Trace ID | traceId | uuid | No | Request trace | X-Trace-Id/generated | 1.2/6 | Propagate/generate | Luôn có | Theo API Guidelines. |

## Ví dụ thành công

Danh sách rỗng trả `data: []`. Ví dụ dưới đây có một request để minh họa projection và thread:

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Support requests retrieved.",
  "data": [
    {
      "id": 58001,
      "course_id": 120,
      "student": {
        "id": 2042,
        "full_name": "Nguyễn An",
        "avatar_url": "https://example.invalid/assets/student.png"
      },
      "status": "OPEN",
      "messages": [
        {
          "id": 90001,
          "author": {
            "id": 604,
            "full_name": "Trần Mentor"
          },
          "content": "Học viên cần hỗ trợ.",
          "attachments": [],
          "created_at": "2026-10-24T08:30:00Z"
        }
      ],
      "created_at": "2026-10-24T08:20:00Z"
    }
  ],
  "meta": {},
  "traceId": "123e4567-e89b-42d3-a456-426614174000"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Không có quyền truy cập yêu cầu hỗ trợ.",
  "data": null,
  "meta": {},
  "traceId": "123e4567-e89b-42d3-a456-426614174000"
}
```

Error example follows API Guidelines. The shared error helper serializes omitted error data as JSON `null`.
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
