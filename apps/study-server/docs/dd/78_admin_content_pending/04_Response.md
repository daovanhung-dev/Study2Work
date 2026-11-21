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
| Local runtime response | `ApiEnvelope<Page<Content>>` — `DERIVED` queue/cardinality fallback. |
| Runtime status | Route/module/shared ADMIN guard và focused HTTP tests đã wire; tests dùng fake DB session. |

## Runtime Content projection

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | N/A | N/A | Branch | 200 success; 401/403/422/500 errors | N/A | 422 là derived query validation; không phải catalog #78 direct error. |
| 2 | `success` | Success flag | `success` | boolean | No | Envelope | N/A | Branch | true success; false error | N/A | Shared response helper. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog/helper | N/A | Branch | `DESIGN_RESOURCE_RETRIEVED` hoặc error code | N/A | Không tạo code khác. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | Branch | Safe localized message | Exact text chưa đặc tả | Không trả raw database detail. |
| 5 | `data.items[]` | Content list | reusable Content | object[] | No | `contents` | `id`, `course_id`, `content_type`, `title`, `payload`, `status`, `parent_id`, `content_order` | Q1 page | `content_order AS order`; map bằng API #49 `ContentResponse` | `parent_id` có thể null | Page shape DERIVED; only current active logical rows. |
| 5.1 | `data.items[].id` | Content ID | `id` | int64 | No | `contents` | `id` | Q1 | Preserve | Required | Checked-in BIGINT candidate; live schema chưa xác nhận. |
| 5.2 | `data.items[].course_id` | Course ID | `course_id` | int64 | No | `contents` | `course_id` | Q1 | Preserve | Required | Filter target for `course`. |
| 5.3 | `data.items[].content_type` | Content type | `content_type` | ContentType/string | No | `contents` | `content_type` | Q1 | Preserve exact stored value | Required | No enum whitelist. |
| 5.4 | `data.items[].title` | Content title | `title` | string | No | `contents` | `title` | Q1 | Preserve | Required | Required by DDL candidate. |
| 5.5 | `data.items[].payload` | Content payload | `payload` | object | No | `contents` | `payload` | Q1 | JSON object to mapping | Required object | DDL requires JSONB object. |
| 5.6 | `data.items[].status` | Content status | `status` | ContentStatus/string | No | `contents` | `status` | Q1 | Fixed predicate `PENDING_REVIEW` | Required | Direct AC-33 predicate. |
| 5.7 | `data.items[].parent_id` | Parent Content ID | `parent_id` | int64? | Yes | `contents` | `parent_id` | Q1 | Preserve nullable parent | Null serializes as null | Reusable field optional. |
| 5.8 | `data.items[].order` | Content order | `order` | int32 | No | `contents` | `content_order` | Q1 | Alias physical column | Required | Not queue ordering. |
| 6 | `data.pagination` | Page metadata | PageMeta | object | No | Derived query/page | `page`, fixed `size`, count | Q1/Q2 | page 1/default; size 20; total; ceil total/size | total_pages 0 when empty | DERIVED; absent from direct Content response. |
| 7 | `meta` | Metadata | `meta` | object | No | Envelope | N/A | Branch | `{}` | Empty object | No separate pagination in meta. |
| 8 | `traceId` | Trace ID | `traceId` | uuid | No | Shared middleware | `X-Trace-Id` | Branch | Validate or generate | Required | Current route is registered. |
| E1 | Error `data` | Error payload | `data` | null | Yes | Shared helper | N/A | Error branch | Current `error_response()` default | JSON null | Matches current runtime/helper, not old DD `{}` claim. |

## Contract discrepancy

Catalog #78 directly declares a single `Content` under `data`, while this queue endpoint has a `page` query and AC-33 requires opening a queue. The local implementation returns `Page<Content>` so it can represent zero or many pending rows. This is `DERIVED`; the catalog/diagram were not changed and the DD remains Draft for owner correction.

## Ví dụ direct theo catalog — một Content object

Ví dụ này giữ shape direct hiện tại của catalog; nó không phải response runtime sau fallback Page.

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã đọc nội dung chờ duyệt.",
  "data": {
    "id": 901,
    "course_id": 501,
    "content_type": "QUIZ",
    "title": "Nội dung chờ duyệt",
    "payload": {"question_count": 4},
    "status": "PENDING_REVIEW",
    "parent_id": null,
    "order": 1
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000078"
}
~~~

`QUIZ`/payload chỉ minh họa kiểu; enum member và payload schema chưa được định nghĩa. Predicate `PENDING_REVIEW` là direct từ AC-33.

## Ví dụ local runtime — DERIVED Page<Content>

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Pending content retrieved.",
  "data": {
    "items": [{
      "id": 901,
      "course_id": 501,
      "content_type": "QUIZ",
      "title": "Nội dung chờ duyệt",
      "payload": {"question_count": 4},
      "status": "PENDING_REVIEW",
      "parent_id": null,
      "order": 1
    }],
    "pagination": {"page": 1, "size": 20, "total": 1, "total_pages": 1}
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000078"
}
~~~

Queue rỗng hoặc page vượt cuối dùng HTTP 200 với `items:[]`; `total_pages=0` khi `total=0`.

## Ví dụ lỗi authorization — HTTP 403

Current helper trả error `data:null`.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Access denied.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000078"
}
~~~

Không trả author/version metadata của #79, reviewer/decision history của #80/#81 hoặc raw database exception.

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
