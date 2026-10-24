---
title: "Request"
order: 3
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "1.Request"
status: "Draft — Needs Confirmation"
---

# Request

## API endpoint

| Thuộc tính | Giá trị |
|---|---|
| HTTP method | PUT |
| URI | /api/v1/admin/notifications/{notification_id} |
| Character encoding | UTF-8 |
| Authentication | Bearer JWT |
| Role | Admin; AC-36 yêu cầu notification-management permission. |
| Content-Type | Catalog không khai báo body. application/json chỉ áp dụng nếu owner duyệt body proposal DERIVED. |

## Request header

| No | Logical name | Field name | Required | Value/Format | Description | Data Mapping reference |
|---:|---|---|---:|---|---|---|
| 1 | Authorization | Authorization | Yes | Bearer <token> | Direct auth contract; Admin permission theo AC-36. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-permission) |
| 2 | Content type | Content-Type | DERIVED | application/json | Chỉ cần nếu body proposal được duyệt; catalog không khai báo request body. | [Step 1](./05_Data_Mapping.md#step-1-read-request) |
| 3 | Trace ID | X-Trace-Id | No | UUID | Correlation theo convention hiện tại; không phải filter nghiệp vụ. | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-permission) |

## Path parameters

| No | Logical name | Physical name | Type | Required | Min | Max | Format | Valid values | Default | Description | Data Mapping reference |
|---:|---|---|---|---:|---|---|---|---|---|---|---|
| 1 | Notification ID | notification_id | int64 | Yes | N/A | N/A | Integer | N/A | N/A | Direct path parameter; physical ID model for Admin resource is unresolved. | [Step 1](./05_Data_Mapping.md#step-1-read-request) |

Catalog does not define positivity/range beyond int64 or a path parse-error rule.

## Query parameters

Không khai báo query parameter trong catalog hoặc AC-36 diagram.

## Request body

**Direct contract:** Catalog #94 and AC-36 diagram declare no request body. The fields below are a proposal DERIVED from the UPDATE intent and #93 create request. They are not an approved request contract.

| No | Logical name | Physical name | Type | Required | Basis | Description | Data Mapping reference |
|---:|---|---|---|---|---|---|---|
| 1 | Explicit recipients | recipients | int64[] | Exactly one audience selector, proposal | Reuse of #93 request | Replace audience with explicit recipient IDs. Empty/duplicate rules are unresolved. | [Recipient mapping](./08_notification_recipients_update.md) |
| 2 | Audience segment | segment | AudienceSegment | Exactly one audience selector, proposal | Reuse of #93 request | Replace audience using a segment; enum and expansion predicate are unresolved. | [Recipient mapping](./08_notification_recipients_update.md) |
| 3 | Title | title | string | Yes, proposal | Reuse of #93 request | Full replacement candidate; blank/length rules not sourced. | [07 table mapping](./07_table.md) |
| 4 | Content | content | string | Yes, proposal | Reuse of #93 request | Full replacement candidate; blank/length rules not sourced. | [07 table mapping](./07_table.md) |
| 5 | Channels | channels | NotificationChannel[] | Yes, proposal | Reuse of #93 request | Full replacement candidate; token set and empty/duplicate rules unknown. | [07 table mapping](./07_table.md) |
| 6 | Scheduled time | scheduled_at | date-time or null | Yes, proposal | Reusable Notification schema plus draft/scheduled purpose | Null is proposed to clear scheduling; a future timestamp is proposed to schedule. No scheduler effect is specified. | [07 table mapping](./07_table.md) |

> Full replacement, requiredness, exactly-one audience selection, null behavior, date-time timezone policy and lifecycle guard are all DERIVED. They require owner confirmation. No action, status, read state, sender ID or query field is added.

## Ví dụ Request data — proposal DERIVED

Illustrative JSON only. NotificationChannel and AudienceSegment placeholder values are not approved enum tokens.

~~~json
{
  "recipients": [12345],
  "title": "Lịch học đã cập nhật",
  "content": "Thời gian học đã được điều chỉnh.",
  "channels": ["<approved-NotificationChannel>"],
  "scheduled_at": "2026-10-25T09:00:00+07:00"
}
~~~

## Quy tắc input đang mở

- Catalog direct contract has no body. If body is approved, validation failure maps to the existing 422 code; field-level rules are not direct.
- notification_id lookup, positive range and 404 precedence relative to permission are unresolved.
- Audience selector, segment tokens, recipient eligibility, duplicate policy and whether previous deliveries can change are unresolved.
- Title/content trim and length limits are unresolved; legacy title VARCHAR(200) is only a schema candidate.
- Channel tokens and delivery constraints are unresolved.
- scheduled_at null/past/future behavior, timezone, precision and effect on existing queued work are unresolved.
- Whether a notification is editable after dispatch/cancel is unresolved; any Draft/Scheduled guard remains a proposal.

## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `1.Request`
- Dimension: `A1:BR34`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `62`
- Số vùng merge: `25`

<details>
<summary>Danh sách vùng merge</summary>

- `S16:T16`
- `U16:V16`
- `W18:X18`
- `W19:X19`
- `U19:V19`
- `S19:T19`
- `U18:V18`
- `S17:T17`
- `S18:T18`
- `AK18:BA18`
- `S15:T15`
- `U15:V15`
- `W15:X15`
- `U14:V14`
- `W14:X14`
- `W17:X17`
- `S13:T14`
- `U13:X13`
- `U17:V17`
- `W16:X16`
- `Y13:AA14`
- `AB14:AD14`
- `AE14:AG14`
- `AB13:AG13`
- `AH13:AJ14`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | HTTP method |  |
| 2 | `L2` | GET/POST |  |
| 3 | `B3` | URI |  |
| 4 | `B4` | Code ký tự |  |
| 4 | `L4` | UTF-8 |  |
| 6 | `B6` | Request header |  |
| 7 | `B7` | Name |  |
| 7 | `J7` | Field name |  |
| 7 | `V7` | Giá trị |  |
| 7 | `AK7` | Giải thích |  |
| 8 | `B8` | Contents type |  |
| 8 | `J8` | Content-Type |  |
| 8 | `V8` | application/json |  |
| 8 | `AK8` | Thực hiện request bằng json data |  |
| 9 | `B9` | Basic authen |  |
| 9 | `J9` | Authorization |  |
| 9 | `V9` | Token |  |
| 11 | `B11` | Request data |  |
| 12 | `B12` | No |  |
| 12 | `C12` | Key name |  |
| 12 | `S12` | Nội dung check |  |
| 12 | `AK12` | Giải thích |  |
| 13 | `S13` | Bắt buộc |  |
| 13 | `U13` | Số ký tự |  |
| 13 | `Y13` | Loại ký tự |  |
| 13 | `AB13` | Format |  |
| 13 | `AH13` | Giá trị hợp lệ |  |
| 14 | `C14` | Logic |  |
| 14 | `K14` | Vật lý |  |
| 14 | `U14` | Tối thiểu |  |
| 14 | `W14` | Tối đa |  |
| 15 | `B15` | 1 |  |
| 15 | `S15` | ○ |  |
| 15 | `U15` | 1 |  |
| 15 | `W15` | 20 |  |
| 15 | `Y15` | halfsize |  |
| 16 | `B16` | 2 |  |
| 16 | `S16` | ○ |  |
| 16 | `U16` | 1 |  |
| 16 | `W16` | 8 |  |
| 16 | `Y16` | halfsize |  |
| 16 | `AB16` | datetime |  |
| 16 | `AE16` | yyyyMMdd |  |
| 17 | `S17` | ○ |  |
| 17 | `U17` | 1 |  |
| 17 | `W17` | 1 |  |
| 17 | `Y17` | halfsize |  |
| 17 | `AB17` | numberic |  |
| 17 | `AH17` | 2,3,4 |  |
| 18 | `S18` | ○ |  |
| 18 | `U18` | 1 |  |
| 18 | `Y18` | fullsize |  |
| 19 | `S19` | ○ |  |
| 19 | `U19` | 1 |  |
| 25 | `B25` | Ví dụ về Request data |  |
| 26 | `L26` | { |  |
| 27 | `M27` | "tnorsh_pln_id" : "0000000001", |  |
| 28 | `M28` | "yt_ymd":" 20201001", |  |
| 29 | `M29` | "yt_hmi":" 0830", |  |
| 30 | `M30` | "excpt_id":" 001", |  |
| 31 | `M31` | "bik_desc":" 計画削除" |  |
| 32 | `L32` | } |  |

</details>
