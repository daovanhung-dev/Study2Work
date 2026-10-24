---
title: "Response"
order: 4
dd_id: "82"
api_name: "Lấy danh sách lesson"
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
| Direct response type | `ApiEnvelope<Lesson>` theo catalog #82. |
| List proposal | `ApiEnvelope<Lesson[]>` để phản ánh AC-34; proposal chưa được duyệt và mâu thuẫn với direct schema. |

## Response fields — contract trực tiếp

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | N/A | N/A | 5.1/5.2 | 200, 401, 403 hoặc 500 theo catalog | N/A | Không thêm HTTP status. |
| 2 | `success` | Success flag | `success` | boolean | No | Envelope | N/A | 5.1/5.2 | true khi thành công, false khi lỗi | Bắt buộc | ApiEnvelope field. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | N/A | 5.1/5.2 | Exact code theo nhánh | Bắt buộc | Giữ code được catalog khai báo. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | 5.1/5.2 | Thông điệp an toàn | Nội dung chưa chuẩn hóa | Không lộ SQL/stack trace. |
| 5 | `data` | Lesson | `data` | object | No | Candidate `lessons` | N/A | 4.1 | Map một reusable Lesson theo direct schema | Required theo catalog | Mâu thuẫn với danh sách; giữ như contract hiện tại. |
| 5.1 | `data.id` | Lesson ID | `id` | int64 | No | Legacy `lessons` candidate | `id` | 4.1 | Direct candidate | Bắt buộc | BIGSERIAL candidate; live DB chưa xác minh. |
| 5.2 | `data.course_id` | Course ID | `course_id` | int64 | No | Legacy `lessons` candidate | `course_id` | 4.1 | Direct candidate | Required trong contract | Legacy DDL nullable; NULL source không map được. |
| 5.3 | `data.title` | Lesson title | `title` | string | No | Legacy `lessons` candidate | `name` | 4.1 | Alias `name -> title` | Bắt buộc | API #09 dùng cùng alias. |
| 5.4 | `data.content` | Lesson content | `content` | string? | Yes | Legacy `lessons` candidate | `content` | 4.1 | Direct candidate | Optional; null/omit convention cần chốt | Không bịa nội dung. |
| 5.5 | `data.video_url` | Video URL | `video_url` | uri? | Yes | Legacy `lessons` candidate | `video_url` | 4.1 | Direct candidate | Optional; null/omit convention cần chốt | URI validity convention chưa xác minh. |
| 5.6 | `data.order` | Lesson order | `order` | int32 | No | Legacy `lessons` candidate | `sort_order` | 4.1 | Alias `sort_order -> order` | Bắt buộc | API #09 dùng cùng alias. |
| 5.7 | `data.status` | Lesson status | `status` | LessonStatus | No | Legacy `lessons` candidate | `status` | 4.1 | Giữ source value | Bắt buộc | Enum members/casing chưa đầy đủ. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope | N/A | 5.1/5.2 | Empty object candidate | `{}` candidate | API guideline envelope; current behavior chưa chứng minh cho #82. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Middleware | `X-Trace-Id` or generated | 0/5 | Validate or create UUID theo middleware convention | Bắt buộc theo envelope schema | Route hiện không có. |

## Ví dụ trực tiếp theo catalog — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy thông tin lesson.",
  "data": {
    "id": 501,
    "course_id": 42,
    "title": "Giới thiệu khóa học",
    "content": "Nội dung bài học",
    "video_url": "https://cdn.example.test/lessons/501.mp4",
    "order": 1,
    "status": "DRAFT"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

Đây là ví dụ hình dạng singleton theo `ApiEnvelope<Lesson>`; không giải quyết được plural/list intent.

## Phương án collection cần xác nhận

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Đã lấy danh sách lesson.",
  "data": [
    {
      "id": 501,
      "course_id": 42,
      "title": "Giới thiệu khóa học",
      "content": "Nội dung bài học",
      "video_url": "https://cdn.example.test/lessons/501.mp4",
      "order": 1,
      "status": "DRAFT"
    }
  ],
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

Đây là đề xuất `ApiEnvelope<Lesson[]>`, không phải contract đã duyệt. Nếu chọn collection, cần quyết định empty result `data: []`, maximum response size và có cần đổi catalog hay không. Không đề xuất `Page<Lesson>` vì catalog không có page query hoặc Page response.

## Error response

Catalog liệt kê đúng ba nhánh: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. Cấu trúc error envelope theo API guideline là `data:null`; helper hiện có default `{}` khi không truyền data. Route chưa tồn tại nên cách tích hợp phải xác nhận.

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
