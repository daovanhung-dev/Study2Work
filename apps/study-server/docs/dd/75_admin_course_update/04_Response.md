---
title: "Response"
order: 4
dd_id: "75"
api_name: "Cập nhật metadata khóa học Admin"
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

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP status | `HTTPStatus` | integer | No | N/A | N/A | 6.1 | Fixed | N/A | Success is 200; error statuses follow catalog. |
| 2 | `success` | Thành công | `success` | boolean | No | N/A | N/A | 6.1 | `true` on success | N/A | Envelope field. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | 6.1 | Fixed by branch | N/A | Success `DESIGN_RESOURCE_UPDATED`. |
| 4 | `message` | Message | `message` | string | No | N/A | N/A | 6.1 | `Course updated.` | Fixed by local implementation | Do not expose DB/provider details. |
| 5 | `data.items[].id` | Course ID | `id` | int64 | No | `courses` | `id` | 5.1 | Copy | N/A | Legacy source candidate. |
| 6 | `data.items[].title` | Tiêu đề | `title` | string | No | `courses` | `name` | 5.1 | `name` → `title` | N/A | Legacy source candidate. |
| 7 | `data.items[].description` | Mô tả | `description` | string? | Yes | `courses` | `description` | 5.1 | Copy | Null or omit unresolved; proposal follows nullable source as null. | Legacy candidate. |
| 8 | `data.items[].thumbnail_url` | URL thumbnail | `thumbnail_url` | uri? | Yes | `courses` | `thumbnail_url` | 5.1 | Copy | Null or omit unresolved; proposal follows nullable source as null. | Legacy candidate. |
| 9 | `data.items[].price` | Giá | `price` | decimal-string | No | `courses` | `price` | 5.1 | Exact decimal serialization; avoid binary float | Contract requires value; DDL permits NULL | Legacy nullable discrepancy. |
| 10 | `data.items[].status` | Trạng thái | `status` | CourseStatus | No | `courses` | `status` | 5.1 | Preserve current value | N/A | #75 does not update status; enum members/casing unresolved. |
| 11 | `data.items[].mentor.id` | Mentor ID | `mentor.id` | int64 | No | `users` | `id` | 5.1 | Copy via course-owner join | Required contract; null owner unresolved | Candidate mapping only. |
| 12 | `data.items[].mentor.full_name` | Tên mentor | `mentor.full_name` | string | No | `users` | `full_name` | 5.1 | Copy via course-owner join | Required contract; null owner unresolved | Candidate mapping only. |
| 13 | `data.items[].mentor.avatar_url` | Avatar mentor | `mentor.avatar_url` | uri? | Yes | `users` | `avatar_url` | 5.1 | Copy | Null or omit unresolved; proposal uses null. | Candidate mapping only. |
| 14 | `data.items[].category` | Category | `category` | Category? | Yes | No approved relation | N/A | N/A | Omit proposal | Optional contract field; source unresolved | `SOURCE_REQUIRED`. |
| 15 | `data.pagination.page` | Page number | `page` | int32 | No | N/A | N/A | 5.2 | Fixed singleton | `1` | DERIVED from #74 precedent. |
| 16 | `data.pagination.size` | Page size | `size` | int32 | No | N/A | N/A | 5.2 | Fixed singleton | `1` | DERIVED from #74 precedent. |
| 17 | `data.pagination.total` | Total | `total` | int64 | No | N/A | N/A | 5.2 | One updated course | `1` | DERIVED. |
| 18 | `data.pagination.total_pages` | Total pages | `total_pages` | int32 | No | N/A | N/A | 5.2 | Fixed singleton | `1` | DERIVED. |
| 19 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 6.1 | Empty object candidate | `{}` | Current helper convention. |
| 20 | `traceId` | Trace ID | `traceId` | uuid | No | N/A | N/A | 6.1 | Current request trace | Generated if absent | Envelope trace convention. |

## Ví dụ thành công

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Đã cập nhật khóa học.",
  "data": {
    "items": [
      {
        "id": 75,
        "title": "Nhập môn thiết kế hệ thống",
        "description": null,
        "thumbnail_url": null,
        "price": "199.00",
        "status": "DRAFT",
        "mentor": {
          "id": 12,
          "full_name": "Nguyễn An",
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
  "traceId": "2ce82824-cf87-4f0a-8a13-bb781f82ad51"
}
```

> Ví dụ response là proposal `DERIVED` cho Page một phần tử; Category bị omit do chưa có relation source-backed. Runtime dùng shared `map_course`, giữ status/mentor từ projection và trả singleton pagination. Enum/casing và live data vẫn chưa được duyệt.

## Lỗi

| HTTP status | Business code | Điều kiện theo contract | Data hiện tại |
|---:|---|---|---|
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Thiếu/sai Bearer JWT | Current `error_response` trả `data:null`. |
| 403 | `DESIGN_ACCESS_DENIED` | Không có role `ADMIN` | Current runtime kiểm tra shared role; permission riêng chưa có source. `data:null`. |
| 404 | `DESIGN_RESOURCE_NOT_FOUND` | UPDATE không trả course row | Current handler rollback và trả `data:null`. |
| 422 | `DESIGN_VALIDATION_ERROR` | Signed-int64 path/body candidate không hợp lệ | Route template #75 được middleware nhận diện; field constraints vẫn là `DERIVED`. |
| 500 | `DESIGN_INTERNAL_ERROR` | Query, Course projection hoặc commit lỗi | Current handler rollback khi transaction đã bắt đầu. |

Chi tiết: [06_Error.md](./06_Error.md).
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
