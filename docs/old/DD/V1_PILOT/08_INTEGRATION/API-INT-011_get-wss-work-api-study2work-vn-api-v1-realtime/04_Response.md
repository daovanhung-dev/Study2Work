---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: "markdown"
dd_id: "API-INT-011"
api_name: "GET wss://work-api.study2work.vn/api/v1/realtime"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
| ---: | --- |
| Transport | `WebSocket` |
| Endpoint | `wss://work-api.study2work.vn/api/v1/realtime` |
| REST envelope | N/A — WebSocket frames are not a REST envelope. |

## Server event fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `type` | Event type | `type` | `string` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | DIRECT protocol field | N/A | Server event category. |
| 2 | `eventId` | Event ID | `eventId` | `string` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | DIRECT protocol field | N/A | At-least-once delivery deduplication key. |
| 3 | `sequence` | Sequence | `sequence` | `integer` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | DIRECT protocol field | N/A | Gap detection / REST history reload. |
| 4 | `occurredAt` | Occurred at | `occurredAt` | `string` | No | N/A | N/A | [S06](./05_Data_Mapping.md#s06) | DIRECT protocol field | N/A | Event timestamp. |

## Server event types

- `message.created`.
- `message.tombstoned`.
- `receipt.updated`.
- `conversation.read_only`.
- `interview.changed`.
- `notification.created`.

## Ví dụ server event

```json
{
  "type": "message.created",
  "eventId": "0198a4c0-2d18-7a42-a82a-32f56e93bd10",
  "sequence": 1,
  "occurredAt": "2026-08-14T00:00:00Z"
}
```

---
## Phụ lục đối chiếu template Markdown

- Template Markdown: `.agent/docs/dd/DD_API_Template_MD/04_Response.md`.
- Workbook/sheet prototype: `DD_API_Template(1).xlsx` / `2.Response`.
- Nội dung nghiệp vụ được sinh từ Basic Design hiện hành; đây không phải khẳng định về chuyển đổi lossless từ Excel.
