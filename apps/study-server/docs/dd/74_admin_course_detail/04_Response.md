---
title: "Response"
order: 4
dd_id: "74"
api_name: "Lấy chi tiết course quản trị"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |
| Success HTTP status | `200` |
| Direct response type | `ApiEnvelope<Page<Course>>` theo catalog/AC-32. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | N/A | N/A | 5.1/5.2 | 200 hoặc exact catalog error status | N/A | Protocol status; không phải JSON field. |
| 2 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 5.1/5.2 | true success; false error | N/A | Envelope field. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | N/A | 5.1/5.2 | Exact code theo nhánh | N/A | Không tạo code mới. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | 5.1/5.2 | Safe localized branch text | Text cụ thể chưa chốt | Không trả raw DB detail. |
| 5 | `data` | Page<Course> | `data` | object | No | `courses`/`users` candidate | N/A | 4.1 | Map singleton Page<Course> | Lỗi: guideline yêu cầu null; helper hiện tại mặc định `{}` | Direct success schema; conditional helper discrepancy. |
| 5.1 | `data.items` | Course items | `items` | array<Course> | No | Q1 result | N/A | 4.1 | Bọc đúng một course thành array | Một item khi thành công | Page contract; singleton behavior DERIVED. |
| 5.1.1 | `data.items[0].id` | Course ID | `id` | int64 | No | `courses` | `id` | 4.1 | Copy | N/A | Legacy query candidate. |
| 5.1.2 | `data.items[0].title` | Title | `title` | string | No | `courses` | `name` | 4.1 | `name → title` | N/A | Current #06/#08 mapping precedent. |
| 5.1.3 | `data.items[0].description` | Description | `description` | string | Yes | `courses` | `description` | 4.1 | Copy | Serialize `null` when source NULL per #08 model | Optional contract; null-vs-omit needs confirmation. |
| 5.1.4 | `data.items[0].thumbnail_url` | Thumbnail URL | `thumbnail_url` | uri | Yes | `courses` | `thumbnail_url` | 4.1 | Copy | Serialize `null` when source NULL per #08 model | Optional contract. |
| 5.1.5 | `data.items[0].price` | Price | `price` | decimal-string | No | `courses` | `price` | 4.1 | Decimal formatting without float conversion | NULL source is candidate 500 | Required by Course contract. |
| 5.1.6 | `data.items[0].status` | Course status | `status` | CourseStatus | No | `courses` | `status` | 4.1 | Preserve stored value | No status filter | Enum members/casing chưa chốt. |
| 5.1.7 | `data.items[0].mentor.id` | Mentor ID | `id` | int64 | No | `users` | `id` | 4.1 | LEFT JOIN by `courses.mentor_id` | Missing/orphan row → candidate 500 | UserSummary required. |
| 5.1.8 | `data.items[0].mentor.full_name` | Mentor name | `full_name` | string | No | `users` | `full_name` | 4.1 | Copy | Missing value → candidate 500 | UserSummary required. |
| 5.1.9 | `data.items[0].mentor.avatar_url` | Mentor avatar | `avatar_url` | uri | Yes | `users` | `avatar_url` | 4.1 | Copy | Serialize `null` when source NULL per #08 model | Optional contract. |
| 5.1.10 | `data.items[0].category` | Category | `category` | Category | Yes | No approved relation | N/A | N/A | Không map | Omit field vì optional | `SOURCE_REQUIRED`; không có course-category join source-backed. |
| 5.2 | `data.pagination.page` | Page number | `page` | int32 | No | Singleton page | N/A | 4.1 | Fixed `1` | `1` | DERIVED. |
| 5.2.1 | `data.pagination.size` | Page size | `size` | int32 | No | Singleton page | N/A | 4.1 | Fixed `1` | `1` | DERIVED. |
| 5.2.2 | `data.pagination.total` | Total items | `total` | int64 | No | Singleton page | N/A | 4.1 | Fixed `1` after row found | `1` | DERIVED. |
| 5.2.3 | `data.pagination.total_pages` | Total pages | `total_pages` | int32 | No | Singleton page | N/A | 4.1 | Fixed `1` after row found | `1` | DERIVED. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope convention | N/A | 5.1 | Empty object candidate | `{}` | No counters until contract defines them. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Middleware | N/A | 5.1/5.2 | Propagate/generate request trace | Valid UUID | Current Study trace convention. |

## Ví dụ thành công

Giá trị minh họa cho response Page singleton; chưa phải output runtime của API #74.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy chi tiết khóa học.",
  "data": {
    "items": [
      {
        "id": 101,
        "title": "Lập trình căn bản",
        "description": null,
        "thumbnail_url": null,
        "price": "49.90",
        "status": "DRAFT",
        "mentor": {
          "id": 7,
          "full_name": "Nguyễn Văn Mentor",
          "avatar_url": null
        }
      }
    ],
    "pagination": {
      "page": 1,
      "size": 1,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "7f66b991-ec10-4a14-b659-bc72c6f62d9d"
}
```

> `category` bị omit do optional và chưa có quan hệ dữ liệu được duyệt. Diagram đề cập counters nhưng schema không có trường tương ứng.

## Ví dụ lỗi

Theo API guideline. Current helper tạo `data:{}` khi không truyền data; #74 chưa wired nên đây là discrepancy tích hợp, không phải output hiện hành của endpoint.

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy khóa học.",
  "data": null,
  "meta": {},
  "traceId": "7f66b991-ec10-4a14-b659-bc72c6f62d9d"
}
```
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
