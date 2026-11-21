---
title: "Response"
order: 4
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
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
| Success HTTP status | 200 `DESIGN_RESOURCE_UPDATED` |
| Direct contract type | `ApiEnvelope<UserProfile>` theo catalog. |
| Runtime status | Route/module/test local đã wired; body/status/session decisions vẫn DERIVED. |

## Contract trực tiếp từ catalog và safe UserProfile source

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 200 success; error statuses theo catalog | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | true success, false error | N/A | ApiEnvelope. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | Exact catalog code | N/A | Không tạo code mới. |
| 4 | message | Message | message | string | No | N/A | N/A | Safe branch text | N/A | Exact message không được catalog định nghĩa. |
| 5 | data | Updated user | data | object | No | Legacy `users` candidate | Safe projection | `UserProfile` | Present on success | Local target mapping DERIVED; live schema chưa xác minh. |
| 5.1 | data.id | User ID | id | int64 | No | Legacy `users` candidate | id | Direct candidate mapping | Required | BIGINT candidate. |
| 5.2 | data.full_name | Full name | full_name | string | No | Legacy `users` candidate | full_name | Preserve | Required | API #71 không update. |
| 5.3 | data.email | Email | email | email | No | Legacy `users` candidate | email | Preserve | Required | PII/Admin policy open. |
| 5.4 | data.role | Role | role | string | No | Legacy `users` candidate | role | Preserve | Required | #71 không đổi role. |
| 5.5 | data.avatar_url | Avatar URL | avatar_url | string? | Yes | Legacy `users` candidate | avatar_url | Preserve | Null giữ null | Safe API #04 model. |
| 5.6 | data.phone | Phone | phone | string? | Yes | Legacy `users` candidate | phone | Preserve | Null giữ null | PII policy open. |
| 5.7 | data.status | Account status | status | string | No | Legacy `users` candidate | status | Target status sau UPDATE | Required | ACTIVE/SUSPENDED là DERIVED allowlist. |
| 5.8 | data.created_at | Created time | created_at | date-time | No | Legacy `users` candidate | created_at | ISO-8601 serialization | Required | Live schema/timezone chưa xác minh. |
| 5.9 | data.updated_at | Updated time | updated_at | date-time | No | Legacy `users` candidate | updated_at | Server `CURRENT_TIMESTAMP` | Required | No-op request cũng cập nhật timestamp theo fallback. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | `{}` | Empty object | Không có pagination/operation metadata. |
| 7 | traceId | Trace ID | traceId | uuid | No | Middleware | Request trace ID | Propagate | Required | `X-Trace-Id` response header cùng giá trị. |

`bio`, `password_hash`, refresh-token hashes và raw tokens không được chọn hoặc trả.

## Ví dụ success

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "User status updated.",
  "data": {
    "id": 1001,
    "full_name": "Nguyen Van A",
    "email": "user@example.test",
    "role": "STUDENT",
    "avatar_url": null,
    "phone": null,
    "status": "SUSPENDED",
    "created_at": "2026-09-15T12:00:00Z",
    "updated_at": "2026-10-25T09:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

`SUSPENDED` trong ví dụ là DERIVED; API runtime serialize `UserProfile` không có `bio`.

## Ví dụ lỗi theo current helper

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

`error_response(...)` hiện trả `data: null`; error body thật có thể có `meta.fieldErrors` khi input sai.

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
