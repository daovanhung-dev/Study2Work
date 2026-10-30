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
| Error contract | HTTP 401/403/404/422/500; catalog `DESIGN_*` codes. |
| Runtime status | Route/view and focused TestClient tests pass locally; tests fake DB and do not verify live schema. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `success` | Success | `success` | boolean | No | N/A | N/A | R1 | Fixed `true` | N/A | Success envelope. |
| 2 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | R1 | Fixed `DESIGN_RESOURCE_UPDATED` | N/A | Catalog #51. |
| 3 | `message` | Message | `message` | string | No | N/A | N/A | R1 | Fixed `Content updated.` | N/A | Current implementation text; not separately fixed by catalog. |
| 4 | `data` | Content | `data` | object | No | `contents` | projection | R1 | Shared `ContentResponse` | N/A | Reusable Content contract. |
| 4.1 | `data.id` | Content identifier | `id` | int64 | No | `contents` | `id` | R1 | Return path target | N/A | Mapped from locked and updated row. |
| 4.2 | `data.course_id` | Course identifier | `course_id` | int64 | No | `contents` | `course_id` | R1 | Preserve existing | N/A | Course does not come from body. |
| 4.3 | `data.content_type` | Content type | `content_type` | string | No | `contents` | `content_type` | R1 | Return replacement string | N/A | Open string in current model; enum unresolved. |
| 4.4 | `data.title` | Title | `title` | string | No | `contents` | `title` | R1 | Return replacement string | N/A | No normalization added. |
| 4.5 | `data.payload` | Payload | `payload` | object | No | `contents` | `payload` | R1 | Return JSONB object | N/A | Subtype keys are not validated. |
| 4.6 | `data.status` | Status | `status` | string | No | `contents` | `status` | R1 | Set `PENDING_REVIEW` | N/A | DERIVED lifecycle rule. |
| 4.7 | `data.parent_id` | Parent Content identifier | `parent_id` | int64? | Yes | `contents` | `parent_id` | R1 | Preserve existing | Null value omitted | Shared model excludes none. |
| 4.8 | `data.order` | Content order | `order` | int32 | No | `contents` | `content_order` | R1 | Preserve existing | N/A | Alias mapping. |
| 5 | `meta` | Metadata | `meta` | object | No | N/A | N/A | R1 | Empty object | `{}` | No pagination. |
| 6 | `traceId` | Trace identifier | `traceId` | uuid | No | N/A | N/A | R1 | Request trace ID | N/A | Shared response helper. |

Không thêm version/audit fields vào response. Catalog không định nghĩa chúng.

## Ví dụ thành công

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Content updated.",
  "data": {
    "id": 50001,
    "course_id": 101,
    "content_type": "lesson-node-v2",
    "title": "Nội dung đã cập nhật",
    "payload": {"body": "Nội dung mới"},
    "status": "PENDING_REVIEW",
    "parent_id": 42001,
    "order": 3
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000001"
}
~~~

Shape khớp current local response; IDs và lifecycle field chỉ là ví dụ, lifecycle vẫn DERIVED.

## Ví dụ lỗi

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Content not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000001"
}
~~~

Error data là `null` theo `error_response`; field errors của body 422 được đặt trong `meta.fieldErrors`.

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
