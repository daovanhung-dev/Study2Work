---
title: "Response"
order: 4
dd_id: "73"
api_name: "Lấy danh sách khóa học Admin"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | application/json |
| Success HTTP status | 200 |
| Direct response type | `ApiEnvelope<Page<Course>>` theo catalog. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP Status | HTTPStatus | integer | No | N/A | N/A | 6.1/6.2/6.3 | 200/401/403/422/500 theo nhánh | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | N/A | N/A | 6.1/6.2/6.3 | true khi success, false khi error | N/A | ApiEnvelope field. |
| 3 | businessCode | Business code | businessCode | string | No | Catalog | N/A | 6.1/6.2/6.3 | Exact catalog code theo nhánh | N/A | Không tạo code mới. |
| 4 | message | Message | message | string | No | Application | N/A | 6.1/6.2/6.3 | Safe localized branch message | Text chưa đặc tả | Không trả raw DB detail. |
| 5 | data | Page<Course> | data | object | No | courses/users candidate | N/A | 5.1/5.2 | Map Page<Course> | `{}` khi error theo helper hiện tại; guideline muốn null | Direct success schema. |
| 5.1 | data.items | Course items | items | array | No | courses/users candidate | N/A | 5.1 | Map từng Course | `[]` khi không có kết quả (DERIVED) | `Course[]`. |
| 5.1.1 | data.items[].id | Course ID | id | int64 | No | courses | id | 5.1 | Direct candidate | Bắt buộc | Legacy BIGSERIAL candidate. |
| 5.1.2 | data.items[].title | Course title | title | string | No | courses | name | 5.1 | Alias `name → title` | Bắt buộc | API #06 dùng cùng alias. |
| 5.1.3 | data.items[].description | Description | description | string? | Yes | courses | description | 5.1 | Direct candidate | null khi source NULL theo #06 | Optional schema field. |
| 5.1.4 | data.items[].thumbnail_url | Thumbnail | thumbnail_url | uri? | Yes | courses | thumbnail_url | 5.1 | Direct candidate | null khi source NULL theo #06 | Optional schema field. |
| 5.1.5 | data.items[].price | Price | price | decimal-string | No | courses | price | 5.1 | Serialize decimal chính xác thành string | Không nhận NULL; null là mapping error candidate | Không chuyển qua float. |
| 5.1.6 | data.items[].status | Course status | status | CourseStatus | No | courses | status | 5.1 | Giữ giá trị source | Bắt buộc | Enum members/casing chưa xác nhận. |
| 5.1.7 | data.items[].mentor | Mentor summary | mentor | object | No | users | N/A | 5.1 | Map UserSummary | Không dựng object giả | Course contract yêu cầu mentor. |
| 5.1.7.1 | data.items[].mentor.id | Mentor ID | id | int64 | No | users | id | 5.1 | Direct candidate qua mentor_id | Bắt buộc | Join candidate `users.id=courses.mentor_id`. |
| 5.1.7.2 | data.items[].mentor.full_name | Mentor name | full_name | string | No | users | full_name | 5.1 | Direct candidate | Bắt buộc | Không lấy email/phone. |
| 5.1.7.3 | data.items[].mentor.avatar_url | Mentor avatar | avatar_url | uri? | Yes | users | avatar_url | 5.1 | Direct candidate | null khi source NULL theo #06 | Optional UserSummary field. |
| 5.1.8 | data.items[].category | Category | category | Category? | Yes | SOURCE_REQUIRED | N/A | 5.1 | Omit tới khi có relation/source được duyệt | Omit — optional field | Không tạo category giả. |
| 5.2 | data.pagination | Pagination | pagination | object | No | N/A | N/A | 5.2 | Map PageMeta | Required | Reusable Page schema. |
| 5.2.1 | data.pagination.page | Current page | page | int32 | No | Query effective value | page | 5.2 | Default 1 nếu omitted | 1 khi omitted (DERIVED) | Page 1-based proposal. |
| 5.2.2 | data.pagination.size | Page size | size | int32 | No | Fixed setting | N/A | 5.2 | Fixed 20 | 20 | Không có request size field. |
| 5.2.3 | data.pagination.total | Total rows | total | int64 | No | courses | COUNT(*) | 4.3 | Count cùng predicates Q1 | 0 khi không có row | Category count chưa thể map nếu category query được dùng. |
| 5.2.4 | data.pagination.total_pages | Total pages | total_pages | int32 | No | Derived | total,size | 5.2 | `ceil(total/20)` | 0 khi total=0 | Fixed-size proposal. |
| 6 | meta | Metadata | meta | object | No | N/A | N/A | 6.1/6.2/6.3 | Empty object theo success helper | `{}` candidate | Error guideline null-data khác current helper. |
| 7 | traceId | Trace ID | traceId | uuid | No | Middleware | X-Trace-Id | 0.1/6.1/6.2/6.3 | Validate hoặc tạo UUID | Bắt buộc trong envelope | Current source convention. |

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy danh sách khóa học.",
  "data": {
    "items": [
      {
        "id": 101,
        "title": "Nhập môn lập trình",
        "description": "Kiến thức nền tảng về lập trình.",
        "thumbnail_url": "https://cdn.example.test/courses/101.png",
        "price": "49.90",
        "status": "PUBLISHED",
        "mentor": {
          "id": 7,
          "full_name": "Nguyễn Văn Mentor",
          "avatar_url": null
        }
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
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

Ví dụ theo Page<Course>; `category` bị omit vì optional và chưa có mapping source-backed. Giá `49.90` minh họa decimal-string theo API #06. Page size 20 là proposal `DERIVED`.

## Ví dụ danh sách rỗng — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Không tìm thấy khóa học phù hợp.",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 20,
      "total": 0,
      "total_pages": 0
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

Empty list trả 200 là proposal theo API #06; không dùng 404 cho collection rỗng.

## Ví dụ lỗi validation — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu query không hợp lệ.",
  "data": {},
  "meta": {
    "fieldErrors": [
      {
        "field": "page",
        "code": "GREATER_THAN_EQUAL",
        "message": "Page phải lớn hơn hoặc bằng 1."
      }
    ]
  },
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

Mã HTTP/business code trực tiếp từ catalog. Ví dụ page validation là `DERIVED`; path admin chưa có trong middleware allowlist. `data={}` phản ánh current helper, còn guideline yêu cầu `data=null`.

## Ví dụ lỗi quyền — HTTP 403

```json
{
  "success": false,
  "businessCode": "DESIGN_ACCESS_DENIED",
  "message": "Không có quyền quản lý khóa học.",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000004"
}
```

Role Admin và quyền course management là direct requirement; guard runtime chưa tồn tại.

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
