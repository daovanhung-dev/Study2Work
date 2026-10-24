---
title: "Response"
order: 4
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json (`DERIVED`; catalog không nêu media type) |
| Success HTTP status | 200 |
| Success business code | DESIGN_RESOURCE_UPDATED |
| Contract data type | ApiEnvelope<SupportRequest> |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 8 | Fixed by branch | N/A | Success 200; errors đúng catalog. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 8 | true success; false error | Luôn có | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog | Literal catalog | 8 | Fixed by branch | Luôn có | Success `DESIGN_RESOURCE_UPDATED`; error code theo branch. |
| 4 | message | Message | message | string | No | Application | Safe message | 8 | Branch message | Luôn có | Wording chưa quy định. |
| 5 | data | Support request | data | SupportRequest | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7 | Object mapping | Không null khi success | Singleton object theo catalog. |
| 6 | data.id | Request ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | N/A | Không null | Pilot ticket ID UUID không khớp. |
| 7 | data.course_id | Course ID | course_id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | N/A | Không null | Pilot ticket không có course relation. |
| 8 | data.student | Student | student | UserSummary | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | Object mapping | Không null | Identity projection chưa được duyệt. |
| 9 | data.student.id | Student ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | N/A | Không null | Pilot profile ID UUID. |
| 10 | data.student.full_name | Student full name | full_name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | N/A | Không null | Pilot full_name nullable. |
| 11 | data.student.avatar_url | Student avatar URL | avatar_url | uri | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | Resolver chưa có | Optional theo schema | Null-versus-omit chưa rõ. |
| 12 | data.status | Request status | status | SupportStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | Giữ status hiện có | Không null | #60 không update status; enum/mapping chưa được xác nhận. |
| 13 | data.messages[] | Messages | messages | SupportMessage[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Thread projection | Array theo schema | Proposal response phải chứa reply mới; order/limit/visibility chưa chốt. |
| 14 | data.messages[].id | Message ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | N/A | Không null | Pilot message ID UUID; generator chưa rõ. |
| 15 | data.messages[].author | Author | author | UserSummary | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Object mapping | Không null | Mentor profile mapping chưa có. |
| 16 | data.messages[].author.id | Author ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | N/A | Không null | Mentor principal ID mapping chưa rõ. |
| 17 | data.messages[].author.full_name | Author full name | full_name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | N/A | Không null | Identity projection chưa có. |
| 18 | data.messages[].author.avatar_url | Author avatar URL | avatar_url | uri | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Resolver chưa có | Optional theo schema | Null/omit chưa chốt. |
| 19 | data.messages[].content | Message content | content | string | No | pilot candidate `support_messages` | body | 7.2 | `message` → `body` → `content` | Không null | Alias candidate; table chưa được duyệt. |
| 20 | data.messages[].attachments[] | Attachments | attachments | UploadAsset[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Resolve refs | Array theo schema | Reference format/resolver chưa có. |
| 21 | data.messages[].attachments[].id | Attachment ID | id | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | N/A | Không null | #34 ID unresolved; pilot file ID UUID. |
| 22 | data.messages[].attachments[].name | Attachment name | name | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Metadata resolver chưa có | Không null | Original filename policy chưa có. |
| 23 | data.messages[].attachments[].url | Attachment URL | url | uri | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Signed/public URL resolver chưa có | Không null | Không dùng storage_key làm URL. |
| 24 | data.messages[].attachments[].content_type | Content type | content_type | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | MIME source chưa chọn | Không null | Declared/detected MIME choice unresolved. |
| 25 | data.messages[].attachments[].size_bytes | Size in bytes | size_bytes | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Metadata resolver chưa có | Không null | Pilot candidate column size_bytes, model chưa duyệt. |
| 26 | data.messages[].attachments[].status | Upload status | status | UploadStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.2 | Enum mapping chưa có | Không null | Không map scan status theo suy đoán. |
| 27 | data.messages[].created_at | Message created time | created_at | date-time | No | pilot candidate `support_messages` | sent_at | 7.2 | `sent_at` → `created_at` | Không null | Candidate; clock/timezone unresolved. |
| 28 | data.created_at | Request created time | created_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | N/A | Không null | Request source chưa được duyệt. |
| 29 | data.resolved_at | Resolved time | resolved_at | date-time? | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | 7.1 | Không đổi ở #60 | Optional; null/omit chưa rõ | #61 là resolve API. |
| 30 | meta | Metadata | meta | object | No | Envelope convention | N/A | 8 | Empty object candidate | `{}` candidate | Không có pagination. |
| 31 | traceId | Trace ID | traceId | uuid | No | Request trace | X-Trace-Id/generated | 1.2/8 | Propagate/generate | Luôn có | Theo API Guidelines khi wired. |

## Ví dụ thành công

Ví dụ minh họa schema contract và reply mới trong `messages[]`. IDs/status placeholders không xác nhận persistence, enum hoặc ref lookup.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Đã gửi phản hồi.",
  "data": {
    "id": 60001,
    "course_id": 120,
    "student": {
      "id": 2042,
      "full_name": "Nguyễn An"
    },
    "status": "STATUS_VALUE_FROM_APPROVED_ENUM",
    "messages": [
      {
        "id": 90002,
        "author": {
          "id": 604,
          "full_name": "Trần Mentor"
        },
        "content": "Mình đã gửi hướng dẫn xử lý cho bạn.",
        "attachments": [
          {
            "id": 81001,
            "name": "huong-dan.pdf",
            "url": "https://example.invalid/assets/huong-dan.pdf",
            "content_type": "application/pdf",
            "size_bytes": 2048,
            "status": "STATUS_VALUE_FROM_APPROVED_ENUM"
          }
        ],
        "created_at": "2026-10-24T09:00:00Z"
      }
    ],
    "created_at": "2026-10-24T08:20:00Z"
  },
  "meta": {},
  "traceId": "123e4567-e89b-42d3-a456-426614174000"
}
```

## Ví dụ lỗi

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Nội dung phản hồi không hợp lệ.",
  "data": null,
  "meta": {},
  "traceId": "123e4567-e89b-42d3-a456-426614174000"
}
```

Error example follows API Guidelines `data=null`. Current helper defaults absent error data to `{}`; #60 is unwired, so this remains a conditional discrepancy.

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
