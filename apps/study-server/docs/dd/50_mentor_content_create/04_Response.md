---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| Success contract | HTTP 201 `DESIGN_RESOURCE_CREATED`; `ApiEnvelope<Content>`. |
| Error contract | HTTP 401/403/422/500; chỉ dùng code của API catalog. |
| Runtime status | API source-backed locally; TestClient/fake DB evidence không chứng minh live schema/deployment. |

## Response fields

| Field | Type | Required | Source/rule |
|---|---|---:|---|
| `success` | boolean | Có | Envelope success branch (`true`). |
| `businessCode` | string | Có | `DESIGN_RESOURCE_CREATED` cho success; error code theo catalog. |
| `message` | string | Có | Human-readable message; exact copy chưa quy định. |
| `data` | Content | Có | Một Content vừa tạo; response model/projection được dùng chung với API #49. |
| `data.id` | int64 | Có | ID allocation/storage type `SOURCE_REQUIRED`. |
| `data.course_id` | int64 | Có | Giá trị course được chấp nhận từ request; physical source chưa rõ. |
| `data.content_type` | ContentType | Có | Echo/project theo enum được duyệt; enum members `SOURCE_REQUIRED`. |
| `data.title` | string | Có | Giá trị đã lưu; trim/normalization chưa có rule. |
| `data.payload` | object | Có | JSON object đã lưu; subtype schema `SOURCE_REQUIRED`. |
| `data.status` | ContentStatus | Có | Implementation gán `PENDING_REVIEW`; DERIVED từ queue precondition AC-33, chưa là direct API rule. |
| `data.parent_id` | int64? | Không | Root `NULL`; response serialization bỏ field null, khớp API #49. DERIVED. |
| `data.order` | int32 | Có | Kế tiếp trong active root siblings, first order 0; DERIVED allocation. |
| `meta` | object | Có | Envelope metadata; pagination không được khai báo cho create. |
| `traceId` | uuid | Có | Request trace theo envelope convention; được xác minh qua TestClient. |

## Success example (illustrative only)

`content_type` placeholder không thuộc enum đã xác minh; ID và dữ liệu là minh họa. Ví dụ thể hiện implementation hiện tại: root `parent_id` null bị loại khỏi JSON, status `PENDING_REVIEW`, order bắt đầu từ 0.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Content created",
  "data": {
    "id": 9001,
    "course_id": 123,
    "content_type": "<SOURCE_REQUIRED: ContentType member>",
    "title": "Nội dung mẫu",
    "payload": {},
    "status": "PENDING_REVIEW",
    "order": 0
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000001"
}
~~~

`parent_id` bị lược khi null bởi response model; field vẫn được hỗ trợ trên Content tree khi node có parent. `order=0` là initial order implementation decision cho root đầu tiên.

## Error response code set

| HTTP | Business code | Tình huống ở mức contract |
|---:|---|---|
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | JWT thiếu/không hợp lệ. |
| 403 | `DESIGN_ACCESS_DENIED` | Role hoặc quyền quản lý course không đủ. |
| 422 | `DESIGN_VALIDATION_ERROR` | Request không thỏa validation được xác nhận. |
| 500 | `DESIGN_INTERNAL_ERROR` | Lỗi nội bộ không dự kiến; không lộ SQL/stack/provider detail. |

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
