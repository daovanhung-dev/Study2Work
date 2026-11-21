---
title: "Response"
order: 4
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
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
| HTTP success | 200 `DESIGN_RESOURCE_RETRIEVED` |
| Contract type | `ApiEnvelope<Operation>` — giữ nguyên catalog DIRECT |

## Response fields

| No | Path | Logical name | Physical/local source | Type | Nullable | Transform/null rule | Remarks |
|---:|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | Route | integer | Không | Cố định 200 | `DESIGN_RESOURCE_RETRIEVED`. |
| 2 | `success` | Cờ thành công | Envelope | boolean | Không | `true` khi đọc được status resource | Không khẳng định Push/Email đã gửi thành công. |
| 3 | `businessCode` | Business code | Catalog | string | Không | `DESIGN_RESOURCE_RETRIEVED` | DIRECT. |
| 4 | `message` | Message | Application | string | Không | Safe static message | Nội dung cụ thể chưa được contract quy định. |
| 5 | `data` | Operation | Reconstructed from #63 local rows | Operation | Không | Mapped below | No Study Operation table. |
| 5.1 | `data.id` | Operation ID | `notifications.operation_id` | uuid | Không | Preserve shared UUID from #63 | Different from path notification ID. |
| 5.2 | `data.kind` | Operation kind | API #63 local response mapping | OperationKind | Không | `NOTIFICATION_DISPATCH` | DERIVED; kind enum members are not catalog-defined. |
| 5.3 | `data.status` | Operation status | Aggregated `notification_deliveries.status` | OperationStatus | Không | `QUEUED`, `FAILED`, or `SENT` by local precedence | DERIVED; no partial-success enum or counts in direct response. |
| 5.4 | `data.owner_id` | Operation owner | `notifications.sender_id` | int64 | Không | Preserve sender ID | Bound to JWT `sub` by API #63. |
| 5.5 | `data.submitted_at` | Submit time | `notifications.created_at` | date-time | Không | ISO-8601 serialization | Local DB timestamp. |
| 5.6 | `data.updated_at` | Last update time | `MAX(notification_deliveries.updated_at)` | date-time | Không | ISO-8601 serialization | Latest channel row update for this notification. |
| 5.7 | `data.completed_at` | Completion time | No source | date-time? | Tùy chọn | Omitted | Retry/terminal completion semantics are unspecified. |
| 5.8 | `data.result` | Operation result | No notification result source | Payment? | Tùy chọn | Omitted | Do not fabricate a Payment result. |
| 6 | `meta` | Metadata | Envelope | object | Không | `{}` | No extra response field is added. |
| 7 | `traceId` | Trace ID | Request trace | uuid | Không | Current trace UUID | Mirrored to `X-Trace-Id`. |

### Local status aggregation

| Outbox aggregate | `data.status` | Meaning/limit |
|---|---|---|
| `queued_count > 0` | `QUEUED` | At least one channel remains queued. |
| No queued row and `failed_count > 0` | `FAILED` | At least one channel failed; successful channels are not separately exposed. |
| `sent_count = delivery_count > 0` | `SENT` | All channel rows for this notification are sent. |
| Counts inconsistent or no supported status rows | Error mapping | 500 for inconsistent projection; 404 when no dispatch status resource exists. |

The reusable `NotificationDelivery` has delivery counts, but #64's direct response is Operation. Counts remain internal to the aggregate and are not added to `data`/`meta`.

## Ví dụ thành công — local queued status

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Notification status was retrieved.",
  "data": {
    "id": "00000000-0000-4000-8000-000000000063",
    "kind": "NOTIFICATION_DISPATCH",
    "status": "QUEUED",
    "owner_id": 1001,
    "submitted_at": "2026-10-25T10:30:00Z",
    "updated_at": "2026-10-25T10:30:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000064"
}
```

## Ví dụ lỗi — resource không tìm thấy

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Notification status was not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000065"
}
```

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
