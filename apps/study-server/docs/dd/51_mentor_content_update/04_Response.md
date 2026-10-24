---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| Success contract | HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<Content>`. |
| Error contract | HTTP 401/403/404/422/500; đúng `DESIGN_*` code của catalog. |
| Runtime status | API #51 chưa có route/module/test; ví dụ là expected design, không phải observed response. |

## Response fields

| Field | Type | Required | Source/rule |
|---|---|---:|---|
| `success` | boolean | Có | true trên success. |
| `businessCode` | string | Có | `DESIGN_RESOURCE_UPDATED` trên success. |
| `message` | string | Có | Human-readable message; nội dung chính xác chưa có contract. |
| `data` | Content | Có | Logical Content sau update; mapping vật lý chưa xác định. |
| `data.id` | int64 | Có | Giữ nguyên `content_id`; stored projection SOURCE_REQUIRED. |
| `data.course_id` | int64 | Có | Giữ nguyên course của Content; physical mapping SOURCE_REQUIRED. |
| `data.content_type` | ContentType | Có | Trả giá trị đã lưu; body proposal DERIVED, enum SOURCE_REQUIRED. |
| `data.title` | string | Có | Trả giá trị đã lưu; normalization/column SOURCE_REQUIRED. |
| `data.payload` | object | Có | Trả payload của revision mới; subtype schema/storage SOURCE_REQUIRED. |
| `data.status` | ContentStatus | Có | Đề xuất `PENDING_REVIEW` cho revision mới; DERIVED, cần xác nhận. |
| `data.parent_id` | int64? | Không | Preserve placement; mapping/null omission SOURCE_REQUIRED. |
| `data.order` | int32 | Có | Preserve order trong đề xuất; physical mapping SOURCE_REQUIRED. |
| `meta` | object | Có | Không có pagination; serialization cần helper alignment. |
| `traceId` | uuid | Có | Current response convention; route behavior chưa được verify. |

Catalog Content không có field version. Không thêm `version`, `version_id` hoặc audit fields vào response của API #51 nếu chưa đổi contract.

## Ví dụ thành công (illustrative only)

`content_type` là placeholder không executable. Các ID/trường còn lại chỉ minh họa shape; status là lifecycle proposal DERIVED.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Content updated",
  "data": {
    "id": 9001,
    "course_id": 123,
    "content_type": "<SOURCE_REQUIRED: ContentType member>",
    "title": "Nội dung đã cập nhật",
    "payload": {},
    "status": "PENDING_REVIEW",
    "parent_id": null,
    "order": 1
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000001"
}
~~~

Giá trị `parent_id`, `order`, `status` trong ví dụ không phải default đã xác nhận. Response chỉ dùng schema `Content` hiện có.

## Ví dụ lỗi

Ví dụ contract-level 404 khi `content_id` không tồn tại; current API #51 runtime chưa được triển khai.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Content not found",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000001"
}
~~~

Khi wire route, cần giữ envelope hiện hành của `error_response`. Catalog chưa quy định nội dung thông báo tiếng Việt cụ thể.

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
