---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
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
|---:|---|---|---|---|---:|---|---|---:|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 6 | 201 on success | N/A | Catalog direct. |
| 2 | success | Success | success | boolean | No | N/A | N/A | 6 | true on success | N/A | Standard envelope. |
| 3 | businessCode | Business code | businessCode | string | No | N/A | N/A | 6 | DESIGN_RESOURCE_CREATED | N/A | Catalog direct. |
| 4 | message | Message | message | string | No | N/A | N/A | 6 | Safe application message | Always present | Exact text is not specified. |
| 5 | data | Lecture | data | object | No | lessons | Returned row | 5 | Map Lecture fields | Required fields present | Local runtime source-backed; live schema remains unverified. |
| 5.1 | data.id | ID | id | int64 | No | lessons candidate | id | 5 | Direct generated identifier | Required | Legacy BIGSERIAL candidate. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | lessons candidate | course_id | 5 | Direct | Required | Legacy candidate. |
| 5.3 | data.title | Title | title | string | No | lessons candidate | name | 5 | name → title | Required | Legacy candidate. |
| 5.4 | data.content | Content | content | string | No | lessons | content | 5 | Return the persisted base-10 representation of request int64 | Required string, including values such as `"0"` | Null cannot occur through this required request path. |
| 5.5 | data.assets | Assets | assets | UploadAsset[] | No | uploads | matched metadata rows | 4 | Resolve IDs using same Mentor, LECTURE and request course; restore input order | Empty input returns `[]` | IDs not resolved within scope return generic 404. |
| 5.5.1 | data.assets[].id | Asset ID | id | int64 | No | uploads | id | 4 | Direct | Required | ID created by API #34. |
| 5.5.2 | data.assets[].name | Asset name | name | string | No | uploads | file_name | 4 | file_name → name | Required | Persisted API #34 metadata. |
| 5.5.3 | data.assets[].url | Asset URL | url | uri | No | uploads | url | 4 | Direct public URL | Required | Do not accept URL from #47 request. |
| 5.5.4 | data.assets[].content_type | Content type | content_type | string | No | uploads | content_type | 4 | Direct | Required | Persisted API #34 metadata. |
| 5.5.5 | data.assets[].size_bytes | Size | size_bytes | int64 | No | uploads | size_bytes | 4 | Direct | Required | Persisted API #34 metadata. |
| 5.5.6 | data.assets[].status | Asset status | status | UploadStatus | No | uploads | status | 4 | Direct | Required | Current value is `UPLOADED`. |
| 5.6 | data.order | Order | order | int32 | No | lessons candidate | sort_order | 5 | sort_order → order | Required | Legacy candidate. |
| 5.7 | data.status | Lesson status | status | status | No | lessons | status | 5 | Explicitly insert and return `PUBLISHED` | Required | Value fixed by user decision. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 6 | Empty object unless supported metadata exists | `{}` | Envelope. |
| 7 | traceId | Trace ID | traceId | uuid | No | Request context | Trace helper | 6 | Propagate request trace | Always present | API guidelines. |

## Ví dụ thành công

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_CREATED",
  "message": "Đã tạo lecture.",
  "data": {
    "id": 47001,
    "course_id": 1001,
    "title": "Bài học mở đầu",
    "content": "12345",
    "assets": [
      {
        "id": 34001,
        "name": "slide.pdf",
        "url": "https://cdn.example.test/uploads/123e4567-e89b-12d3-a456-426614174000",
        "content_type": "application/pdf",
        "size_bytes": 1024,
        "status": "UPLOADED"
      }
    ],
    "order": 1,
    "status": "PUBLISHED"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000047"
}
~~~

Response `content` là chuỗi thập phân được tạo từ request integer; `status` là `PUBLISHED`. Asset fields theo metadata API #34; `assets: []` là response hợp lệ khi request gửi `asset_refs: "[]"`.

## Ví dụ lỗi

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy course.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000048"
}
~~~

Ví dụ lỗi dùng current Study error helper với `data: null`.

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
