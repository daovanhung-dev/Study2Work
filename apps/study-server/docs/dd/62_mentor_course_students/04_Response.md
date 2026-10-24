---
title: "Response"
order: 4
dd_id: "62"
api_name: "Lấy tập người nhận"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Format

| Thuộc tính | Giá trị |
|---|---|
| Format | JSON |
| Character encoding | UTF-8 |
| Content-Type | `application/json` |
| HTTP success | 200 `DESIGN_RESOURCE_RETRIEVED` |
| Contract type | `ApiEnvelope<Page<Course>>` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | `HTTPStatus` | HTTP Status | `HTTPStatus` | integer | No | N/A | N/A | 5 | Cố định theo catalog | N/A | DIRECT: 200. |
| 2 | `success` | Success | `success` | boolean | No | N/A | N/A | 5 | `true` | N/A | Theo quy ước envelope. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | N/A | N/A | 5 | Literal trong catalog | N/A | `DESIGN_RESOURCE_RETRIEVED`. |
| 4 | `message` | Message | `message` | string | No | N/A | N/A | 5 | Thông điệp an toàn | Chưa quy định câu chữ | Không lộ chi tiết nội bộ. |
| 5 | `data` | Payload | `data` | `Page<Course>` | No | N/A | N/A | 5 | Giữ schema catalog | Required | Lệch mục đích trả roster. |
| 5.1 | `data.items` | Items | `items` | `Course[]` | No | N/A | N/A | 4 | Generic type theo catalog | `[]` là DERIVED | Chưa có mapping người nhận. |
| 5.1.1 | `data.items[].id` | Course ID | `id` | int64 | No | `courses` candidate | `id` | 4 | Field Course trực tiếp | SOURCE_REQUIRED nếu dùng làm mục roster | Không phải learner ID. |
| 5.1.2 | `data.items[].title` | Course title | `title` | string | No | `courses` candidate | `name` candidate | 4 | Candidate `name → title` | SOURCE_REQUIRED nếu dùng làm mục roster | Không phải field người nhận. |
| 5.1.3 | `data.items[].description` | Course description | `description` | string? | Yes | `courses` candidate | `description` | 4 | Candidate trực tiếp | Quy tắc null/omit còn mở | Field Course optional. |
| 5.1.4 | `data.items[].thumbnail_url` | Thumbnail | `thumbnail_url` | uri? | Yes | `courses` candidate | `thumbnail_url` | 4 | Candidate trực tiếp | Quy tắc null/omit còn mở | Field Course optional. |
| 5.1.5 | `data.items[].price` | Price | `price` | decimal-string | No | `courses` candidate | `price` | 4 | Chuyển đổi decimal an toàn | NULL là lỗi toàn vẹn nguồn | Không phải field người nhận. |
| 5.1.6 | `data.items[].status` | Trạng thái course | `status` | CourseStatus | No | `courses` candidate | `status` | 4 | Chỉ dùng enum đã duyệt | Enum chưa xác định | Vòng đời course, không phải enrollment. |
| 5.1.7 | `data.items[].mentor.id` | Mentor ID | `id` | int64 | No | `users` candidate | `id` | 4 | Projection Mentor của Course | SOURCE_REQUIRED cho roster | Không phải learner đã ghi danh. |
| 5.1.8 | `data.items[].mentor.full_name` | Tên Mentor | `full_name` | string | No | `users` candidate | `full_name` | 4 | Projection Mentor của Course | SOURCE_REQUIRED cho roster | Không phải learner đã ghi danh. |
| 5.1.9 | `data.items[].mentor.avatar_url` | Mentor avatar | `avatar_url` | uri? | Yes | `users` candidate | `avatar_url` | 4 | Projection Mentor của Course | Quy tắc null/omit còn mở | Field UserSummary optional. |
| 5.1.10 | `data.items[].category.id` | Category ID | `id` | int64 | No when present | Chưa có relation được duyệt | N/A | 4 | None | Có thể bỏ object cha optional | Category là optional. |
| 5.1.11 | `data.items[].category.name` | Category name | `name` | string | No when present | Chưa có relation được duyệt | N/A | 4 | None | Có thể bỏ object cha optional | Field Category. |
| 5.1.12 | `data.items[].category.slug` | Category slug | `slug` | string | No when present | Chưa có relation được duyệt | N/A | 4 | None | Có thể bỏ object cha optional | Field Category. |
| 5.1.13 | `data.items[].category.description` | Category description | `description` | string? | Yes | Chưa có relation được duyệt | N/A | 4 | None | Optional/null policy open | Field Category. |
| 5.2 | `data.pagination` | Phân trang | `pagination` | PageMeta | No | N/A | N/A | 4 | Schema dùng chung | Required | #62 không có input page/size. |
| 5.2.1 | `data.pagination.page` | Trang hiện tại | `page` | int32 | No | N/A | N/A | 4 | SOURCE_REQUIRED | Chưa quy định default/range | Không sao chép từ #6/#46. |
| 5.2.2 | `data.pagination.size` | Kích thước trang | `size` | int32 | No | N/A | N/A | 4 | SOURCE_REQUIRED | Chưa quy định default/giới hạn | Request không có query. |
| 5.2.3 | `data.pagination.total` | Tổng số mục | `total` | int64 | No | Candidate count | N/A | 4 | Chưa rõ grain đếm | Empty→0 là DERIVED | Xung đột giữa số Course và số learner. |
| 5.2.4 | `data.pagination.total_pages` | Tổng số mục pages | `total_pages` | int32 | No | N/A | N/A | 4 | Cần tổng số và size | Quy tắc chưa xác định | SOURCE_REQUIRED. |
| 6 | `meta` | Metadata | `meta` | object | No | N/A | N/A | 5 | Theo quy ước envelope | Candidate `{}` | Catalog không khai báo metadata riêng cho #62. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | N/A | N/A | 5 | Quy ước trace dùng chung | Tạo/truyền tiếp khi wired | Chưa có runtime. |

## Ví dụ thành công — chỉ minh họa cấu trúc

JSON trang rỗng chỉ minh họa các kiểu dữ liệu trong catalog. Giá trị phân trang là ví dụ, chưa phải default được duyệt; #62 không có input phân trang. Ví dụ này không giải quyết xung đột Course/roster.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "<MESSAGE_TEXT>",
  "data": {
    "items": [],
    "pagination": {
      "page": 1,
      "size": 1,
      "total": 0,
      "total_pages": 0
    }
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000000"
}
```

## Ví dụ lỗi — envelope theo guideline

`data:null` theo API Guidelines. Helper hiện tại khác quy ước này và #62 chưa có route; đây không phải ví dụ runtime.

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "<SAFE_MESSAGE>",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000000"
}
```

## Khoảng trống trong response contract

- Giữ `Page<Course>` trong DD vì đây là type hiện tại của catalog.
- Không chép learner data vào Course fields hoặc tạo Course giả cho từng enrollment.
- `Page<UserSummary>` chỉ là đề xuất sửa contract; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-62-01-response-resource).
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
