---
title: "Response"
order: 4
dd_id: "77"
api_name: "Xóa khóa học Admin theo policy AC-32"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success HTTP status | 200 `DESIGN_RESOURCE_DELETED` |
| Direct response type | `ApiEnvelope<DeleteResult>` theo catalog. |
| Runtime status | API #77 chưa được wire; examples là expected design, không phải runtime output. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | N/A | N/A | 5.1/6.1 | 200 success; 401/403/404/422/500 errors | N/A | Protocol status, không phải JSON field. |
| 2 | `success` | Success flag | `success` | boolean | No | Envelope | N/A | Branch | true success; false error | N/A | Direct envelope convention. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | N/A | Branch | `DESIGN_RESOURCE_DELETED` hoặc exact catalog error code | N/A | Không tạo code mới. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | Branch | Safe localized message | Exact text chưa đặc tả | Không trả raw database detail. |
| 5 | `data` | DeleteResult | `data` | object | No | Approved soft-delete target | N/A | 5.1 | Map theo reusable schema | Required on success; error data theo API guideline null | Physical mapping chưa có source. |
| 5.1 | `data.id` | Course ID | `id` | int64 | No | Course target candidate | `id` candidate | 5.1 | ID của course được đánh dấu xóa thành công | Required | Physical target schema/live mapping chưa xác nhận. |
| 5.2 | `data.status` | Delete status | `status` | literal `"deleted"` | No | DeleteResult schema | N/A | 5.1 | Literal `deleted` | Required | Direct reusable schema; không phải CourseStatus. |
| 5.3 | `data.deleted_at` | Deletion timestamp | `deleted_at` | date-time | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 5.1 | Timestamp do approved soft-delete persistence cung cấp | Required; không tự fallback sang request time | Legacy courses không có marker; pilot `archived_at` khác nghĩa/model. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope | N/A | Branch | `{}` candidate | Empty object candidate | Không có pagination. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Shared trace | `X-Trace-Id` | 0.1/Branch | Validate hoặc generate theo convention | Required trong envelope | Endpoint chưa wired. |
| E1 | Error `data` | Error payload | `data` | null by guideline | N/A | N/A | N/A | Error branch | API guideline yêu cầu `null` | Current helper default là `{}` | Conditional source/contract discrepancy. |

## Ví dụ thành công — HTTP 200

Ví dụ theo `DeleteResult` trực tiếp. `deleted_at` minh họa định dạng; nguồn persistable chưa được chọn nên không dùng giá trị ví dụ như implementation source.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_DELETED",
  "message": "Đã xóa khóa học theo policy.",
  "data": {
    "id": 101,
    "status": "deleted",
    "deleted_at": "2026-10-24T12:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000077"
}
~~~

## Ví dụ lỗi dependency — HTTP 422 — DERIVED

Ví dụ branch nếu policy được duyệt quy định enrollment/content hiện hữu chặn soft delete. Business code có trong catalog; điều kiện, field errors và message chưa được duyệt. `data:null` theo API guideline, khác helper hiện tại.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Không thể xóa khóa học do điều kiện policy.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000077"
}
~~~

Không trả enrollment IDs, learner data, content payload, raw SQL error hoặc `reason` chưa có trong `DeleteResult`.

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
