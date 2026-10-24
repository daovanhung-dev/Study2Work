---
title: "Response"
order: 4
dd_id: "78"
api_name: "Lấy pending content"
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
| Success HTTP status | 200 `DESIGN_RESOURCE_RETRIEVED` |
| Direct response type | `ApiEnvelope<Content>` theo catalog. |
| Runtime status | API #78 chưa được wire; examples là expected design, không phải runtime output. |

## Direct contract fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | N/A | N/A | Branch | 200 success; 401/403/500 errors | N/A | Protocol status, không phải JSON field. |
| 2 | `success` | Success flag | `success` | boolean | No | Envelope | N/A | Branch | true success; false error | N/A | Envelope convention. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | N/A | Branch | `DESIGN_RESOURCE_RETRIEVED` hoặc exact catalog error code | N/A | Không tạo code mới. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | Branch | Safe localized message | Exact text chưa đặc tả | Không trả raw query/content details. |
| 5 | `data` | Content | `data` | object | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Một Content theo catalog | Required on success | Cardinality của queue/page chưa nhất quán. |
| 5.1 | `data.id` | Content ID | `id` | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Logical Content identifier | Required | Generic BIGINT Content persistence chưa có nguồn. |
| 5.2 | `data.course_id` | Course ID | `course_id` | int64 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Logical owning course | Required | Có thể là filter `course`; physical relation chưa xác nhận. |
| 5.3 | `data.content_type` | Content type | `content_type` | ContentType | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Serialize approved enum value | Required | Members/casing chưa được liệt kê. |
| 5.4 | `data.title` | Content title | `title` | string | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Preserve approved stored value | Required | Không suy ra table/column. |
| 5.5 | `data.payload` | Content payload | `payload` | object | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Preserve approved subtype object | Required object | Payload keys/default chưa xác nhận. |
| 5.6 | `data.status` | Content status | `status` | ContentStatus | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 2.1/3.1 | Row thỏa `PENDING_REVIEW` | Required | Filter DIRECT; enum/storage chưa xác nhận. |
| 5.7 | `data.parent_id` | Parent Content ID | `parent_id` | int64? | Yes | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Optional field | Null/omit rule unresolved | Không có generic parent relation. |
| 5.8 | `data.order` | Content order | `order` | int32 | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 3.1 | Preserve sibling order | Required | Không dùng làm queue sort mặc định. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope | N/A | Branch | `{}` candidate | Empty object candidate | Direct response không khai báo PageMeta. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Shared trace | `X-Trace-Id` | 0.1/Branch | Validate or generate | Required | Endpoint chưa wired. |
| E1 | Error `data` | Error payload | `data` | null by guideline | N/A | N/A | N/A | Error branch | API guideline yêu cầu `null` | Current helper default `{}` | Conditional source/contract discrepancy. |

## Ví dụ trực tiếp theo catalog — một Content object

Ví dụ giữ `ApiEnvelope<Content>` hiện tại. `content_type: "SOURCE_REQUIRED"` là placeholder có giải thích, không phải enum value hợp lệ; `payload: {}` chỉ minh họa JSON object, không phải payload mặc định. Example không giải quyết list/page cardinality.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã đọc nội dung chờ duyệt.",
  "data": {
    "id": 901,
    "course_id": 501,
    "content_type": "SOURCE_REQUIRED",
    "title": "Nội dung chờ duyệt",
    "payload": {},
    "status": "PENDING_REVIEW",
    "parent_id": null,
    "order": 1
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000078"
}
~~~

`PENDING_REVIEW` là predicate trực tiếp của AC-33; `content_type`, ID, payload và parent/order chỉ minh họa shape vì physical source/enum chưa được duyệt.

## Candidate response nếu catalog được sửa — DERIVED

Nếu API thực sự trả danh sách phân trang, phương án đề xuất là `ApiEnvelope<Page<Content>>`. Đây không phải response contract hiện tại; cần đổi catalog và xác nhận pagination trước implementation.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã đọc hàng đợi chờ duyệt.",
  "data": {
    "items": [
      {
        "id": 901,
        "course_id": 501,
        "content_type": "SOURCE_REQUIRED",
        "title": "Nội dung chờ duyệt",
        "payload": {},
        "status": "PENDING_REVIEW",
        "parent_id": null,
        "order": 1
      }
    ],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000078"
}
~~~

Giá trị type/payload tiếp tục là placeholders; empty-page behavior và page size 20 vẫn là proposals.

## Ví dụ lỗi authorization — HTTP 403

Ví dụ theo API guideline `data:null`; current helper phát `{}` khi `data` bị bỏ trống. Endpoint chưa wired nên không có runtime response.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Không có quyền truy cập hàng đợi duyệt.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000078"
}
~~~

Không trả author/reviewer metadata từ #79, decision reason từ #81, raw payload/schema errors hoặc database details ngoài direct Content contract.

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
