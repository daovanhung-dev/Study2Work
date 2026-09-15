---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch: `201/422/500` | `N/A` | Protocol status; AC-02 alternative `200` is discrepancy |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `DESIGN_RESOURCE_CREATED`, `DESIGN_VALIDATION_ERROR` hoặc `DESIGN_INTERNAL_ERROR` | `N/A` | Normative list contract |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Fixed by branch | `TBD — message text chưa đặc tả` | Không trả raw credential/DB detail |
| 5 | `data` | User profile | `data` | `object` | `No` | `users` | `N/A` | `6.1` | Map `UserProfile`; `{}` on error | `{}` on error | `ApiEnvelope<UserProfile>` |
| 5.1 | `data.id` | User ID | `id` | `int64` | `No` | `users` | `id` | `6.1` | BIGSERIAL serialized as int64 | `N/A` | ERD primary key |
| 5.2 | `data.full_name` | Full name | `full_name` | `string` | `No` | `users` | `full_name` | `6.1` | Direct mapping | `N/A` | ERD NOT NULL |
| 5.3 | `data.email` | Email | `email` | `email` | `No` | `users` | `email` | `6.1` | Direct mapping | `N/A` | ERD UNIQUE, NOT NULL |
| 5.4 | `data.role` | Role | `role` | `string` | `No` | `users` | `role` | `6.1` | Direct mapping | `N/A` | Role values not enumerated here |
| 5.5 | `data.avatar_url` | Avatar URL | `avatar_url` | `uri` | `Yes` | `users` | `avatar_url` | `6.1` | Direct mapping | `TBD — null/omit rule` | ERD NULL |
| 5.6 | `data.bio` | Biography | `bio` | `string` | `Yes` | `N/A` | `N/A — no ERD column` | `6.1` | `DISCREPANCY/TBD` | `TBD — null/omit rule` | Contract field has no source column |
| 5.7 | `data.phone` | Phone | `phone` | `string` | `Yes` | `users` | `phone` | `6.1` | Direct mapping | `TBD — null/omit rule` | ERD NULL |
| 5.8 | `data.status` | Account status | `status` | `string` | `No` | `users` | `status` | `6.1` | Direct mapping | `N/A` | Status check performed before success |
| 5.9 | `data.created_at` | Created time | `created_at` | `date-time` | `No` | `users` | `created_at` | `6.1` | Direct mapping | `N/A` | ERD NOT NULL |
| 5.10 | `data.updated_at` | Updated time | `updated_at` | `date-time` | `No` | `users` | `updated_at` | `6.1` | Direct mapping | `N/A` | ERD NOT NULL |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | `{}` | `{}` | No operation metadata in contract |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `6.1/6.2/6.3` | Request correlation/generator | `TBD — exact generator` | `ApiEnvelope` field |

> Error response dùng cùng các field `success`, `businessCode`, `message`, `data`, `meta`, `traceId` của `ApiEnvelope`; không tạo `error_code` hoặc `error_message_id`.
>
> `HTTPStatus` trong bảng là protocol status, không phải property JSON.
>
> AC-02 nói client nhận token nhưng UserProfile contract không khai báo token; DD không thêm `access_token` hoặc field tương đương.

## Ví dụ thành công — HTTP 201

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Login accepted",
  "data": {
    "id": 1001,
    "full_name": "Nguyen Van A",
    "email": "student@example.com",
    "role": "STUDENT",
    "avatar_url": null,
    "phone": null,
    "status": "ACTIVE",
    "created_at": "2026-08-28T00:00:00Z",
    "updated_at": "2026-08-28T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

## Ví dụ lỗi — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Invalid request",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Login could not be processed",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```


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

