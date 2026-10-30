---
title: "Response"
order: 4
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
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
| Runtime status | Route/module/test có trong source; body/legacy mapping là fallback `DERIVED`, live schema chưa xác minh. |

## Contract trực tiếp từ catalog

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5.1/5.2 | 200 success; errors theo catalog | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | Envelope | true success; false error | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | Envelope | Exact catalog code theo branch | N/A | Không tạo code mới. |
| 4 | message | Message | message | string | No | N/A | N/A | Envelope | Message an toàn theo branch | SOURCE_REQUIRED | Message text chưa được contract định nghĩa. |
| 5 | data | Updated user | data | object | No | legacy users candidate | `UPDATE ... RETURNING` safe projection | 5.1 | `UserProfile` | UserProfile khi success; lỗi dùng `data:null` | Type trực tiếp; legacy mapping là fallback `DERIVED`. |
| 5.1 | data.id | User ID | id | int64 | No | legacy users candidate | id | 5.1 | Map ID user đã update | Required theo UserProfile | Live schema chưa xác minh. |
| 5.2 | data.full_name | Full name | full_name | string | No | legacy users candidate | full_name | 5.1 | Giá trị sau mutation candidate | Required theo UserProfile | API #14 precedent; body field candidate. |
| 5.3 | data.email | Email | email | email | No | legacy users candidate | email | 5.1 | Giữ giá trị hiện có | Required theo UserProfile | Không editable trong candidate body; PII. |
| 5.4 | data.role | Role | role | UserRole | No | legacy users candidate | role | 5.1 | Role sau mutation | Required theo UserProfile | Allowlist runtime là fallback DERIVED; policy còn mở. |
| 5.5 | data.avatar_url | Avatar URL | avatar_url | uri? | Optional | legacy users candidate | avatar_url | 5.1 | Map safe projection | JSON null khi nguồn null | API #04 model giữ null; URL format chưa được validate. |
| 5.6 | data.bio | Biography | bio | string? | Optional | SOURCE_REQUIRED | N/A | 5.1 | Không tạo hoặc trả giá trị giả | Omit | Không có legacy users column/API #04 mapping; model bỏ field. |
| 5.7 | data.phone | Phone | phone | string? | Optional | legacy users candidate | phone | 5.1 | Map safe projection | JSON null khi nguồn null | API #04 model giữ null; PII policy còn mở. |
| 5.8 | data.status | Account status | status | UserStatus | No | legacy users candidate | status | 5.1 | Giữ status hiện tại; không mutation ở #70 | Required theo UserProfile | Status update thuộc API #71; enum members chưa biết. |
| 5.9 | data.created_at | Created time | created_at | date-time | No | legacy users candidate | created_at | 5.1 | ISO-8601 candidate | Required theo UserProfile | Live schema/timezone chưa xác minh. |
| 5.10 | data.updated_at | Updated time | updated_at | date-time | No | legacy users candidate | updated_at | 5.1 | Server `CURRENT_TIMESTAMP` | Required theo UserProfile | Theo API #14 precedent; live DB timezone chưa xác minh. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | Envelope | `{}` | Current helper | Không có pagination metadata. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | Middleware | Envelope | Request correlation ID | Bắt buộc theo ApiEnvelope | Current middleware gắn trace ID. |

## Ví dụ success candidate

JSON hợp lệ theo runtime fallback. `bio` được omit vì model/source không có mapping; `phone` và `avatar_url` có thể null.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "User updated.",
  "data": {
    "id": 1001,
    "full_name": "Nguyen Van A",
    "email": "user@example.test",
    "role": "STUDENT",
    "avatar_url": null,
    "phone": null,
    "status": "ACTIVE",
    "created_at": "2026-09-15T12:00:00Z",
    "updated_at": "2026-10-25T08:30:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

## Ví dụ lỗi theo guideline

Ví dụ lỗi dùng `data:null`, đúng `error_response` hiện hành.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Access denied.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
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
