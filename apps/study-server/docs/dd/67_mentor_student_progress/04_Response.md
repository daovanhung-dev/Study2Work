---
title: "Response"
order: 4
dd_id: "67"
api_name: "Lấy tiến độ Student"
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
| HTTP status | 200 |
| Contract trực tiếp | ApiEnvelope<Page<Course>> theo diagram/catalog. |
| Runtime fallback | ApiEnvelope<StudentCourseProgress> theo mục đích AC-26; DERIVED và chưa được contract owner phê duyệt. |

## Contract trực tiếp từ catalog

HTTP 200, business code `DESIGN_RESOURCE_RETRIEVED`. Giữ nguyên schema trực tiếp dù schema Course không biểu diễn tiến độ Student theo AC-26.

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `success` | Success flag | `success` | boolean | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T> | N/A | DIRECT reusable schema. |
| 2 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | 4.1 | DESIGN_RESOURCE_RETRIEVED khi thành công | N/A | DIRECT từ catalog. |
| 3 | `message` | Message | `message` | string | No | N/A | N/A | 4.1 | Text cụ thể chưa được catalog chốt | Chưa đặc tả | DIRECT field, message SOURCE_REQUIRED. |
| 4 | `data.items[]` | Course list | `items` | Course[] | No | SOURCE_REQUIRED | SOURCE_REQUIRED | 4.1 | Theo Page<Course> | Empty rule chưa đặc tả | DIRECT type; không có progress field. |
| 5 | `data.pagination.page` | Current page | `page` | int32 | No | N/A | N/A | 4.1 | Theo PageMeta | DIRECT schema | PageMeta schema có field này; request không có page input. |
| 6 | `data.pagination.size` | Page size | `size` | int32 | No | N/A | N/A | 4.1 | Theo PageMeta | DIRECT schema | Request không có size input/default. |
| 7 | `data.pagination.total` | Total items | `total` | int64 | No | N/A | N/A | 4.1 | Theo PageMeta | DIRECT schema | Semantics chưa rõ nếu direct response giữ Course. |
| 8 | `data.pagination.total_pages` | Total pages | `total_pages` | int32 | No | N/A | N/A | 4.1 | Theo PageMeta | DIRECT schema | Pagination policy chưa chốt. |
| 9 | `meta` | Envelope metadata | `meta` | object | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T> | Object fields chưa đặc tả | DIRECT schema. |
| 10 | `traceId` | Trace ID | `traceId` | uuid | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T> | N/A | DIRECT schema; route hiện truyền trace ID. |

### Reusable Course fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | int64 | Có | Course ID. |
| `title` | string | Có | Tiêu đề course. |
| `description` | string | Không | Mô tả tùy chọn. |
| `thumbnail_url` | uri | Không | URL ảnh tùy chọn. |
| `price` | decimal-string | Có | Giá theo decimal string. |
| `status` | CourseStatus | Có | Enum members chưa được catalog định nghĩa. |
| `mentor` | UserSummary | Có | Mentor gồm id, full_name, avatar_url tùy chọn. |
| `category` | Category | Không | Category tùy chọn; mapping cho #67 chưa xác định. |

Category gồm `id:int64`, `name:string`, `slug:string`, `description?:string`. UserSummary gồm `id:int64`, `full_name:string`, `avatar_url?:uri`.

## Ví dụ theo direct contract

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Course retrieved",
  "data": {
    "items": [
      {
        "id": 321,
        "title": "Example course",
        "description": "Example description",
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
      "size": 1,
      "total": 1,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000001"
}
```

`CourseStatus` là placeholder minh họa, không xác nhận enum member. Ví dụ không chứa tiến độ Student.

## Runtime response fallback — DERIVED, chưa phải contract catalog đã duyệt

Runtime dùng singular `StudentCourseProgress` vì path xác định đúng một course và một Student. Shape là DERIVED fallback cho AC-26; chỉ gồm lesson progress để đồng bộ với #65, không gồm learning events của #66, quiz hoặc assignment progress.

| Runtime field | Type | Null/empty rule | Basis/status |
|---|---|---|---|
| `course_id` | int64 | Bằng course path đã được xác thực | DERIVED; cần sửa response contract. |
| `student` | UserSummary | `avatar_url` hiện có thể là JSON null | DERIVED; chỉ trả sau khi Student thuộc active roster. |
| `summary.completed_lessons` | int32 | 0 nếu không có completed lesson | DERIVED runtime; đếm trạng thái COMPLETED. |
| `summary.total_lessons` | int32 | 0 nếu course không có lesson PUBLISHED | DERIVED từ API #9/#65. |
| `summary.progress_percent` | int32 | 0 nếu total_lessons = 0 | DERIVED runtime; cùng formula floor-average #65. |
| `lessons[]` | LessonProgress[] | Một item mỗi lesson PUBLISHED theo sort_order, id | DERIVED; unbounded, request không có pagination. |
| `lessons[].lesson_id` | int64 | Required | Legacy query source; live schema chưa xác nhận. |
| `lessons[].title` | string | Tên lesson theo API #9 projection | Runtime map `lessons.name → title`. |
| `lessons[].order` | int32 | Theo API #9 projection | Runtime map `lessons.sort_order → order`. |
| `lessons[].progress_status` | string | NOT_STARTED khi không có progress row | DERIVED runtime; allowed state set vẫn cần phê duyệt. |
| `lessons[].progress_percent` | int32 | 0 khi không có progress row | DERIVED runtime; kiểm tra range 0–100. |
| `lessons[].last_accessed_at` | date-time? | JSON null nếu không có progress row/timestamp | Runtime giữ null; field source vẫn là legacy DDL candidate. |
| `lessons[].completed_at` | date-time? | JSON null nếu chưa hoàn thành | Runtime giữ null; field source vẫn là legacy DDL candidate. |

### Runtime JSON fallback — DERIVED, không phải contract catalog

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Student progress retrieved.",
  "data": {
    "course_id": 321,
    "student": {
      "id": 778,
      "full_name": "Student Name",
      "avatar_url": "https://example.test/student.png"
    },
    "summary": {
      "completed_lessons": 1,
      "total_lessons": 4,
      "progress_percent": 37
    },
    "lessons": [
      {
        "lesson_id": 9001,
        "title": "Introduction",
        "order": 1,
        "progress_status": "COMPLETED",
        "progress_percent": 100,
        "last_accessed_at": "2026-10-23T09:00:00",
        "completed_at": "2026-10-23T09:20:00"
      },
      {
        "lesson_id": 9002,
        "title": "Core concepts",
        "order": 2,
        "progress_status": "IN_PROGRESS",
        "progress_percent": 50,
        "last_accessed_at": "2026-10-24T09:00:00",
        "completed_at": null
      },
      {
        "lesson_id": 9003,
        "title": "Practice",
        "order": 3,
        "progress_status": "NOT_STARTED",
        "progress_percent": 0,
        "last_accessed_at": null,
        "completed_at": null
      },
      {
        "lesson_id": 9004,
        "title": "Review",
        "order": 4,
        "progress_status": "NOT_STARTED",
        "progress_percent": 0,
        "last_accessed_at": null,
        "completed_at": null
      }
    ]
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000067"
}
```

Runtime fallback summary: `floor((100 + 50 + 0 + 0) / 4) = 37`; 1 of 4 lessons is COMPLETED. Đây là DERIVED behavior; không sửa contract catalog.

## Error response note

Catalog chỉ liệt kê 401/403/404/500; xem [06_Error](./06_Error.md). API guideline và current `error_response` thống nhất error `data:null`; middleware design-code allowlist đã gồm path #67. Malformed signed-int64 path được view ánh xạ 404 theo fallback cùng nhóm #65/#66.

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
