---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | `JSON` |
| Character encoding | `UTF-8` |
| Content-Type | `application/json` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | `integer` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Fixed by branch: `200/404/500` | `N/A` | Protocol status; không phải property JSON |
| 2 | `success` | Success flag | `success` | `boolean` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | `true` on success; `false` on error | `N/A` | `ApiEnvelope` field |
| 3 | `businessCode` | Business code | `businessCode` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Fixed by branch | `N/A` | Uses `DESIGN_*` code from contract |
| 4 | `message` | Message | `message` | `string` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Fixed by branch | `TBD — message text chưa đặc tả` | Không trả raw SQL/stack trace |
| 5 | `data` | Curriculum page | `data` | `object` | `No` | `lessons` | `N/A` | `4.1/4.2` | Map `Page<Lesson>` | `{}` on error | `ApiEnvelope<Page<Lesson>>` |
| 5.1 | `data.items` | Lesson items | `items` | `array` | `No` | `lessons` | `N/A` | `4.1` | Map từng lesson public | `[]` khi không có lesson public | `Lesson[]` |
| 5.1.1 | `data.items[].id` | Lesson ID | `id` | `int64` | `No` | `lessons` | `id` | `3.1` | Direct mapping từ BIGSERIAL | `N/A` | |
| 5.1.2 | `data.items[].course_id` | Course ID | `course_id` | `int64` | `No` | `lessons` | `course_id` | `3.1` | Direct mapping | `N/A` | |
| 5.1.3 | `data.items[].title` | Lesson title | `title` | `string` | `No` | `lessons` | `name` | `3.1` | Alias `l.name` thành `title` | `N/A` | Physical/logical name discrepancy |
| 5.1.4 | `data.items[].content` | Lesson content | `content` | `string` | `Yes` | `lessons` | `content` | `3.1` | Direct mapping | `null` khi source là `NULL` | Optional contract field |
| 5.1.5 | `data.items[].video_url` | Video URL | `video_url` | `uri` | `Yes` | `lessons` | `video_url` | `3.1` | Direct mapping | `null` khi source là `NULL` | Optional contract field |
| 5.1.6 | `data.items[].order` | Lesson order | `order` | `int32` | `No` | `lessons` | `sort_order` | `3.1` | Alias `l.sort_order` thành `order` | `N/A` | Physical/logical name discrepancy |
| 5.1.7 | `data.items[].status` | Lesson status | `status` | `LessonStatus` | `No` | `lessons` | `status` | `3.1` | Filter `PUBLISHED`, direct mapping | `N/A` | Enum catalog chưa đầy đủ |
| 5.2 | `data.pagination` | Pagination metadata | `pagination` | `object` | `No` | `N/A` | `N/A` | `4.2` | One-page curriculum | `{}` on error | `PageMeta` |
| 5.2.1 | `data.pagination.page` | Page number | `page` | `int32` | `No` | `N/A` | `N/A` | `4.2` | Fixed `1` | `N/A` | Endpoint không nhận page |
| 5.2.2 | `data.pagination.size` | Page size | `size` | `int32` | `No` | `N/A` | `N/A` | `4.2` | `total` của lesson public | `0` khi empty | Design-only one-page convention |
| 5.2.3 | `data.pagination.total` | Total lessons | `total` | `int64` | `No` | `N/A` | `N/A` | `4.2` | `length(published_lessons)` | `0` khi empty | Không cần count query riêng |
| 5.2.4 | `data.pagination.total_pages` | Total pages | `total_pages` | `int32` | `No` | `N/A` | `N/A` | `4.2` | `1` khi total > 0, ngược lại `0` | `0` khi empty | Design-only one-page convention |
| 6 | `meta` | Metadata | `meta` | `object` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Empty object | `{}` | `ApiEnvelope` field |
| 7 | `traceId` | Trace ID | `traceId` | `uuid` | `No` | `N/A` | `N/A` | `5.1/5.2/5.3` | Request correlation/generator | `TBD — exact generator chưa đặc tả` | `ApiEnvelope` field |

> Error response dùng cùng các field `success`, `businessCode`, `message`, `data`, `meta`, `traceId` của `ApiEnvelope`; không tạo `error_code` hoặc `error_message_id` riêng.
>
> `HTTPStatus` trong bảng là protocol status, không phải property JSON.

## Ví dụ thành công — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Curriculum retrieved",
  "data": {
    "items": [
      {
        "id": 1001,
        "course_id": 101,
        "title": "Introduction",
        "content": "Overview of the course",
        "video_url": "https://cdn.example.test/lessons/1001.mp4",
        "order": 1,
        "status": "PUBLISHED"
      },
      {
        "id": 1002,
        "course_id": 101,
        "title": "Variables",
        "content": null,
        "video_url": null,
        "order": 2,
        "status": "PUBLISHED"
      }
    ],
    "pagination": {
      "page": 1,
      "size": 2,
      "total": 2,
      "total_pages": 1
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
```

## Ví dụ curriculum rỗng — HTTP 200

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "No published lessons",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 0,
      "total": 0,
      "total_pages": 0
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
```

## Ví dụ lỗi không tìm thấy — HTTP 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Published course not found",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
```

## Ví dụ lỗi hệ thống — HTTP 500

```json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Curriculum could not be retrieved",
  "data": {},
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000004"
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
<summary>Bản ghi đối chiếu</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 4 | `C4` | Giá trị trả về khi call API |  |
| 9 | `L9` | JSON |  |
| 14 | `D14` | Response item name |  |
| 26 | `B26` | Ví dụ |  |

</details>
