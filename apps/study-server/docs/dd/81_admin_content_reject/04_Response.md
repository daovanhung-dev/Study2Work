---
title: "Response"
order: 4
dd_id: "81"
api_name: "Từ chối nội dung"
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

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTP status | HTTP Status | HTTP status | integer | No | N/A | N/A | Success/error branch | Catalog status | Success 200; errors 401, 403, 404, 422, 500 | Not a JSON body field. |
| 2 | success | Success | success | boolean | No | Envelope | N/A | Envelope build | true on success; false on error | Always present | Study helper convention; route absent. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog/envelope | N/A | Envelope build | Exact catalog literal | Always present | Success DESIGN_RESOURCE_UPDATED; errors in 06_Error.md. |
| 4 | message | Message | message | string | No | Application | N/A | Envelope build | Safe localized text | Always present | Exact success message unspecified. |
| 5 | data | Content | data | Content | No | Logical Content | SOURCE_REQUIRED | Step 7 | Project declared Content schema | One Content object | No Page/list wrapper. |
| 5.1 | data.id | Content ID | id | int64 | No | Logical Content | SOURCE_REQUIRED | Step 7 | Direct logical identity | Required | Physical key unresolved. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | Logical Content | SOURCE_REQUIRED | Step 7 | Stored relationship | Required | Physical relation unresolved. |
| 5.3 | data.content_type | Content type | content_type | ContentType | No | Logical Content | SOURCE_REQUIRED | Step 7 | Return stored value | Required | Enum members unresolved. |
| 5.4 | data.title | Title | title | string | No | Logical Content | SOURCE_REQUIRED | Step 7 | Return stored value | Required | Physical source unresolved. |
| 5.5 | data.payload | Payload | payload | object | No | Logical Content | SOURCE_REQUIRED | Step 7 | Return stored object | Required | Object keys/schema unresolved; do not invent. |
| 5.6 | data.status | Content status | status | ContentStatus | No | Logical Content | SOURCE_REQUIRED | Step 7 | Resulting logical status REJECTED | Required | Physical serialization/state owner unresolved. |
| 5.7 | data.parent_id | Parent Content ID | parent_id | int64? | Yes | Logical Content | SOURCE_REQUIRED | Step 7 | Return stored optional value | Null/omit rule unresolved | Optional per reusable schema. |
| 5.8 | data.order | Display order | order | int32 | No | Logical Content | SOURCE_REQUIRED | Step 7 | Return stored value | Required | Physical source unresolved. |
| 6 | meta | Metadata | meta | object | No | Envelope | N/A | Envelope build | Candidate empty object | No pagination metadata declared | Empty/null convention needs runtime alignment. |
| 7 | traceId | Trace ID | traceId | uuid | No | Request trace | N/A | Envelope build | Propagate request trace | Always present | Trace convention direct; route absent. |

Không có reason, reviewer, version, audit hoặc metadata field nào trong reusable Content response.

## Ví dụ thành công

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "<safe message>",
  "data": {
    "id": 123,
    "course_id": 456,
    "content_type": "<ContentType>",
    "title": "<title>",
    "payload": {},
    "status": "REJECTED",
    "parent_id": 789,
    "order": 1
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
~~~

ContentType và payload là placeholders vì enum members/payload schema chưa được xác nhận; payload:{} chỉ minh họa object shape. Status REJECTED phản ánh effect ở diagram, physical mapping chưa có.

## Ví dụ lỗi

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
~~~

data:null theo API guideline là expected error shape; current error_response() mặc định {} khi caller không truyền data. #81 chưa được wire.
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
