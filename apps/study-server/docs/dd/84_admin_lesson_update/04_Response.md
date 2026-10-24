---
title: "Response"
order: 4
dd_id: "84"
api_name: "Cập nhật lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
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
| Direct response type | `ApiEnvelope<Lesson>` theo catalog #84. |
| Success business code | `DESIGN_RESOURCE_UPDATED` |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---|---|---|---|---|---|---|
| 1 | HTTP status | HTTP status | N/A | integer | No | Catalog | N/A | 5.1/5.2 | 200/401/403/404/422/500 theo nhánh | N/A | Exact catalog set. |
| 2 | `success` | Success flag | `success` | boolean | No | Envelope | N/A | 5.1/5.2 | true success; false error | Required | Reusable ApiEnvelope. |
| 3 | `businessCode` | Business code | `businessCode` | string | No | Catalog | N/A | 5.1/5.2 | Exact catalog code | Required | Không tạo code mới. |
| 4 | `message` | Message | `message` | string | No | Application | N/A | 5.1/5.2 | Safe message | Text chưa chốt | Không trả raw DB error. |
| 5 | `data` | Lesson | `data` | object | No | Legacy lessons candidate | N/A | 4.1 | Một Lesson trực tiếp | Required | Không bọc Page/array. |
| 5.1 | `data.id` | Lesson ID | `id` | int64 | No | Legacy lessons candidate | `id` | 4.1 | Copy returned row | Required | BIGINT candidate; live schema unknown. |
| 5.2 | `data.course_id` | Course ID | `course_id` | int64 | No | Legacy lessons candidate | `course_id` | 4.1 | Preserve existing relation | Required by contract | Nullable DDL discrepancy. |
| 5.3 | `data.title` | Lesson title | `title` | string | No | Legacy lessons candidate | `name` | 4.1 | Alias `name -> title` | Required | API #09 source alias precedent. |
| 5.4 | `data.content` | Lesson content | `content` | string? | Yes | Legacy lessons candidate | `content` | 4.1 | Copy returned value | Null/omit unresolved | Optional schema; DDL nullable. |
| 5.5 | `data.video_url` | Video URL | `video_url` | uri? | Yes | Legacy lessons candidate | `video_url` | 4.1 | Copy returned value | Null/omit unresolved | DDL TEXT candidate. |
| 5.6 | `data.order` | Lesson order | `order` | int32 | No | Legacy lessons candidate | `sort_order` | 4.1 | Alias `sort_order -> order` | Required | API #09 source alias precedent. |
| 5.7 | `data.status` | Lesson status | `status` | LessonStatus | No | Legacy lessons candidate | `status` | 4.1 | Return unchanged | Enum values/casing unresolved | #84 does not update status; #85 owns transition. |
| 6 | `meta` | Metadata | `meta` | object | No | Envelope convention | N/A | 5.1 | Empty object candidate | `{}` on success | No API-specific meta contract. |
| 7 | `traceId` | Trace ID | `traceId` | uuid | No | Trace middleware | `X-Trace-Id` or generated | 0/5 | Propagate or generate | Required | Current Study convention. |

## Ví dụ thành công — HTTP 200 — Candidate mapping

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_UPDATED",
  "message": "Đã cập nhật lesson.",
  "data": {
    "id": 501,
    "course_id": 42,
    "title": "Giới thiệu khóa học",
    "content": "Nội dung đã cập nhật",
    "video_url": "https://example.com/lesson-501.mp4",
    "order": 2,
    "status": "DRAFT"
  },
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000084"
}
```

Cấu trúc theo ApiEnvelope<Lesson>; mapping là legacy candidate. DRAFT chỉ là ví dụ từ legacy default, không định nghĩa toàn bộ enum.

## Ví dụ lỗi không tìm thấy — HTTP 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy lesson.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000084"
}
```

## Ví dụ validation — HTTP 422

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000084"
}
```

API guideline yêu cầu error data:null; current helper mặc định data:{} khi không truyền data. API #84 chưa được wire nên đây là integration discrepancy.

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
