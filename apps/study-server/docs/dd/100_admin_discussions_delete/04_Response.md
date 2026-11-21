---
title: "Response"
order: 4
dd_id: "100"
api_name: "Xóa discussion theo policy"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |
| HTTP success | `200` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Thành công | `success` | boolean | No | N/A | N/A | 4.1 | Hằng `true` khi thành công | Không null | Shared envelope |
| 2 | `businessCode` | Mã nghiệp vụ | `businessCode` | string | No | N/A | N/A | 4.1 | Hằng `DESIGN_RESOURCE_DELETED` | Không null | DIRECT catalog |
| 3 | `message` | Thông báo | `message` | string | No | N/A | N/A | 4.1 | Nội dung do ứng dụng chọn | Exact message chưa nêu | Không suy ra literal |
| 4 | `data` | Kết quả xóa | `data` | object | No | N/A | N/A | 4.1 | Map `DeleteResult` | Không null theo schema | Reusable schema |
| 5 | `data.id` | Discussion ID | `id` | int64 | No | `discussions` candidate | `id` | 4.1 | ID của target/path | Giá trị phải là target đã xử lý | Physical lookup candidate |
| 6 | `data.status` | Trạng thái kết quả | `status` | string literal | No | N/A | N/A | 4.1 | Hằng `deleted` | Không null | DIRECT `DeleteResult`; không phải DB status token |
| 7 | `data.deleted_at` | Thời điểm xóa | `deleted_at` | date-time | No | Chưa chọn | Chưa chọn | 4.1 | Thời điểm soft-delete | Không null theo schema | Field/type DIRECT; source/persistence SOURCE_REQUIRED; `updated_at` mapping DERIVED |
| 8 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 4.1 | Object metadata chung | Chi tiết endpoint không nêu | Shared envelope |
| 9 | `traceId` | Trace ID | `traceId` | uuid | No | N/A | N/A | 4.1 | Request trace | Không null theo envelope | API guideline chung |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_DELETED",
  "message": "Discussion deleted.",
  "data": {
    "id": 123,
    "status": "deleted",
    "deleted_at": "2026-10-24T12:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
```

`message`, `id`, thời điểm và `traceId` trong ví dụ chỉ minh họa format; contract không chọn nội dung message, nguồn timestamp hoặc record ID cụ thể. `deleted_at` là ISO-8601 date-time theo convention catalog.

## Nguồn response

- `data.id` có thể lấy từ path hoặc target row; consistency rule cần source xác nhận.
- `data.status` lấy literal `"deleted"` từ reusable schema.
- Không có cột `deleted_at` trong legacy `discussions`; không tuyên bố `updated_at` là nguồn trực tiếp.
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
