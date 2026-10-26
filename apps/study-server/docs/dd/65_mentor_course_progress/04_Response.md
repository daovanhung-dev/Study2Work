---
title: "Response"
order: 4
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Contract trực tiếp từ catalog

HTTP 200, business code DESIGN_RESOURCE_RETRIEVED, body ApiEnvelope<Page<Course>>. Giữ nguyên schema này trong bảng contract dù nó chưa diễn tả learner progress của AC-26.

| Field | Type | Required | Description |
|---|---|---:|---|
| success | boolean | Có | Kết quả envelope. |
| businessCode | string | Có | DESIGN_RESOURCE_RETRIEVED khi đọc thành công. |
| message | string | Có | Thông điệp; nội dung cụ thể chưa được catalog chốt. |
| data.items | Course[] | Có | Items theo reusable schema Course. |
| data.pagination.page | int32 | Có | Trang hiện tại theo reusable schema PageMeta. |
| data.pagination.size | int32 | Có | Kích thước trang theo reusable schema PageMeta. |
| data.pagination.total | int64 | Có | Tổng số items. |
| data.pagination.total_pages | int32 | Có | Tổng số trang. |
| meta | object | Có | Metadata bổ sung của envelope. |
| traceId | uuid | Có | Trace identifier theo reusable schema. |

### Reusable Course fields trong response trực tiếp

| Field | Type | Required | Description |
|---|---|---:|---|
| id | int64 | Có | Course ID. |
| title | string | Có | Tiêu đề course. |
| description | string | Không | Mô tả tùy chọn. |
| thumbnail_url | uri | Không | URL ảnh tùy chọn. |
| price | decimal-string | Có | Giá theo decimal string. |
| status | CourseStatus | Có | Trạng thái course; enum members cần đối chiếu schema được chọn. |
| mentor | UserSummary | Có | Mentor summary của course. |
| category | Category | Không | Category tùy chọn; quan hệ nguồn chưa xác định cho #65. |

UserSummary: id:int64, full_name:string, avatar_url?:uri. Category: id:int64, name:string, slug:string, description?:string.

## Example theo direct contract

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Course retrieved",
  "data": {
    "items": [
      {
        "id": 321,
        "title": "Introduction to Biology",
        "description": "Course description",
        "thumbnail_url": "https://example.test/course.png",
        "price": "0.00",
        "status": "<CourseStatus>",
        "mentor": {
          "id": 22,
          "full_name": "Mentor Name"
        },
        "category": {
          "id": 5,
          "name": "Science",
          "slug": "science"
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
  "traceId": "00000000-0000-4000-8000-000000000001"
}
~~~

Đây là ví dụ shape theo schema catalog; các giá trị minh họa, CourseStatus là placeholder chứ không xác nhận enum member, và response không có learner/progress.

## Response local hiện tại — DERIVED, không phải contract catalog

AC-26 cần một row mỗi learner. Theo lựa chọn fallback được ủy quyền, route hiện trả Page<MentorStudentProgress> sau khi kiểm tra direct course owner:

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Course progress retrieved",
  "data": {
    "items": [
      {
        "student": {
          "id": 778,
          "full_name": "Student Name",
          "avatar_url": "https://example.test/student.png"
        },
        "completed_lessons": 3,
        "total_lessons": 12,
        "progress_percent": 25
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
  "traceId": "00000000-0000-4000-8000-000000000002"
}
~~~

Các field, phép tính và one-page behavior là DERIVED local fallback, được kiểm tra bằng focused HTTP tests. Catalog vẫn là nguồn contract trực tiếp `Page<Course>` cho tới khi owner phê duyệt thay đổi. No pagination limit exists.

## Error response note

The exact error business codes/statuses are listed in [Error](./06_Error.md). The shared `error_response` defaults `data=None`, serialized as JSON null and confirmed by local HTTP tests. OpenAPI declares 200/401/403/404/500; the route does not create a synthetic 422. Fake DB tests do not prove live schema/deployment behavior.

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
