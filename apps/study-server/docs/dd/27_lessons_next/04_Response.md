---
title: "Response"
order: 4
dd_id: "27"
api_name: "Tìm bài tiếp theo theo curriculum"
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

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTPStatus | HTTP status | HTTPStatus | integer | No | API catalog | N/A | 4.1–4.4 | Fixed by branch: 200/401/403/404/500 | N/A | Protocol status, không phải JSON property. |
| 2 | success | Success flag | success | boolean | No | ApiEnvelope<T> schema | success | 4.1–4.4 | Envelope field | N/A | Serialization API #27 chưa runtime-verified. |
| 3 | businessCode | Business code | businessCode | string | No | API catalog | N/A | 4.1–4.4 | Fixed by branch | N/A | Chỉ dùng code API #27 ở bảng bên dưới. |
| 4 | message | Message | message | string | SOURCE_REQUIRED | ApiEnvelope<T> schema | message | 4.1–4.4 | SOURCE_REQUIRED | Text policy chưa đặc tả. | Catalog nêu field nhưng không định nghĩa nội dung. |
| 5 | data | Next lesson | data | object (Lesson) | Required on success | API catalog reusable schema | N/A | 3.1/4.1 | ApiEnvelope<Lesson> | Error response data=null theo API Guidelines. | No-next behavior chưa được gán cho 404 hay nullable result. |
| 5.1 | data.id | Lesson ID | id | int64 | No | lessons — candidate | id | 3.1 | Candidate direct mapping | Required theo Lesson schema. | Query API #27 chưa xác nhận. |
| 5.2 | data.course_id | Course ID | course_id | int64 | No | lessons — candidate | course_id | 3.1 | Candidate direct mapping | Required theo Lesson schema. | Checked-in DDL cho phép NULL; xem conflict trong Overview. |
| 5.3 | data.title | Lesson title | title | string | No | lessons — candidate | name | 3.1 | name → title | Required theo Lesson schema. | Candidate alias theo API #9 curriculum mapping. |
| 5.4 | data.content | Lesson content | content | string | Optional | lessons — candidate | content | 3.1 | Candidate direct mapping | Null/omit rule chưa xác nhận. | Logical Lesson field optional; DDL column nullable. |
| 5.5 | data.video_url | Lesson video URL | video_url | uri | Optional | lessons — candidate | video_url | 3.1 | Candidate TEXT → URI | Null/omit/conversion chưa xác nhận. | Logical Lesson field optional; DDL column nullable. |
| 5.6 | data.order | Curriculum order | order | int32 | No | lessons — candidate | sort_order | 3.1 | sort_order → order | Required theo Lesson schema. | DDL default 0; API #27 ordering rule chưa xác nhận. |
| 5.7 | data.status | Lesson status | status | LessonStatus | No | lessons — candidate | status | 3.1 | Candidate direct mapping | Enum values chưa được liệt kê. | Không khẳng định API #27 chỉ trả PUBLISHED lesson. |
| 6 | meta | Metadata | meta | object | No | ApiEnvelope<T> schema | meta | 4.1–4.4 | Envelope field | Members unspecified. | API-specific metadata không được catalog khai báo. |
| 7 | traceId | Trace ID | traceId | uuid | No | ApiEnvelope<T> schema | traceId | 4.1–4.4 | Envelope field | Required theo reusable schema. | Runtime generation/propagation API #27 chưa xác minh. |

## Business code by status

| HTTP status | Business code | Contract meaning |
|---:|---|---|
| 200 | DESIGN_RESOURCE_RETRIEVED | Đọc Lesson theo API catalog; selection/projection chưa được runtime xác nhận. |
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Authentication failure theo contract. |
| 403 | DESIGN_ACCESS_DENIED | Role/access bị từ chối theo contract; policy cụ thể chưa rõ. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource not found theo contract; current lesson và no-next conditions chưa phân biệt. |
| 500 | DESIGN_INTERNAL_ERROR | Lỗi nội bộ theo contract. |

## Ví dụ thành công — HTTP 200

~~~json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Message text is not specified by the contract.",
  "data": {
    "id": 102,
    "course_id": 9001,
    "title": "Example next lesson",
    "content": "Illustrative lesson content",
    "order": 2,
    "status": "<LessonStatus>"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000001"
}
~~~

> Các giá trị ID/nội dung chỉ để minh họa schema. Chuỗi <LessonStatus> là placeholder cho enum chưa được catalog liệt kê; ví dụ không xác nhận bài kế phải có trạng thái cụ thể.

## Ví dụ lỗi — HTTP 404

~~~json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Not-found message text is not specified by the contract.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000002"
}
~~~

> API Guidelines quy định error data là null. Ví dụ chỉ minh họa envelope/code; catalog chưa xác định 404 có áp dụng khi không có bài tiếp theo hay không.
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
