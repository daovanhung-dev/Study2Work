---
title: "Response"
order: 4
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
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
| HTTP status thành công | 200 DESIGN_RESOURCE_DELETED |
| Direct contract type | ApiEnvelope<DeleteResult> theo catalog. |
| Runtime status | API #72 chưa có route/view; ví dụ chỉ minh họa contract. |

## Contract trực tiếp từ catalog

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 5.1/5.2/5.3/5.4 | 200 hoặc catalog error status | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | Envelope | true khi thành công; false khi lỗi | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | Envelope | Chính xác code theo catalog | N/A | Không tạo code mới. |
| 4 | message | Message | message | string | No | N/A | N/A | Envelope | Thông điệp an toàn theo branch | Chưa đặc tả | Exact text chưa được catalog định nghĩa. |
| 5 | data | Delete result | data | object | No | Chưa xác định | Chưa xác định | 5.1 | DeleteResult | Bắt buộc khi success theo response schema | Physical mapping unresolved. |
| 5.1 | data.id | User ID | id | int64 | No | User target chưa xác định | N/A | 5.1 | ID của user được xử lý thành công | Bắt buộc | Type DIRECT; candidate lấy từ user row/path cần xác nhận policy. |
| 5.2 | data.status | Delete status | status | literal string "deleted" | No | N/A | N/A | 5.1 | Hằng literal theo reusable schema | Bắt buộc | DIRECT; exact lowercase string. |
| 5.3 | data.deleted_at | Deletion time | deleted_at | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 5.1 | Từ timestamp được policy/schema phê duyệt | Bắt buộc | Contract DIRECT; legacy users không có source column. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | Envelope | {} candidate khi không có metadata | {} | No pagination contract. |
| 7 | traceId | Trace ID | traceId | uuid | No | N/A | Middleware | Envelope | UUID được validate/tạo theo middleware | Bắt buộc theo envelope | Endpoint chưa wired. |

## Ví dụ success theo contract

Ví dụ minh họa shape DeleteResult; timestamp không khẳng định physical source hay runtime response.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_DELETED",
  "message": "User deleted.",
  "data": {
    "id": 1001,
    "status": "deleted",
    "deleted_at": "2026-10-24T10:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

## Ví dụ lỗi theo guideline

Guideline Study yêu cầu data null cho error envelope. Current error_response helper mặc định data thành {}; API #72 chưa wired nên chưa có endpoint runtime để xác nhận.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Access denied.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

Không trả full UserProfile, email, phone, password_hash, token hoặc token hash trong DeleteResult.

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
