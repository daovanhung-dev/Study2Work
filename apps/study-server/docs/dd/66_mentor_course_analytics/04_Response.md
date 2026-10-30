---
title: "Response"
order: 4
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "2.Response"
status: "Draft — Needs Confirmation"
---

# Response

## Contract trực tiếp từ catalog

HTTP 200, business code DESIGN_RESOURCE_RETRIEVED, response ApiEnvelope<Page<Course>>. Bảng giữ nguyên direct schema. Course/PageMeta không chứa metric analytics; đây là discrepancy với AC-26 và local runtime.

| Field | Type | Required | Description |
|---|---|---:|---|
| success | boolean | Có | Kết quả envelope. |
| businessCode | string | Có | DESIGN_RESOURCE_RETRIEVED khi thành công. |
| message | string | Có | Thông điệp response. |
| data.items | Course[] | Có | Danh sách Course theo reusable schema. |
| data.pagination.page | int32 | Có | Trang hiện tại theo PageMeta. |
| data.pagination.size | int32 | Có | Kích thước trang. |
| data.pagination.total | int64 | Có | Tổng số items. |
| data.pagination.total_pages | int32 | Có | Tổng số trang. |
| meta | object | Có | Metadata envelope. |
| traceId | uuid | Có | Trace identifier. |

### Local runtime response — DERIVED

Runtime hiện trả một summary object vì catalog Page<Course> không thể biểu diễn mục tiêu AC-26. Không xem đây là contract đã được duyệt.

| Field | Type | Required | Mô tả |
|---|---|---:|---|
| tracked_lesson_accesses | int64, >= 0 | Có | Số cặp Student/lesson phân biệt có last_accessed_at trên lesson PUBLISHED. Đây là proxy, không phải số event. |
| students_with_activity | int64, >= 0 | Có | Số Student phân biệt trong các cặp proxy có activity. |
| last_activity_at | datetime hoặc null | Có | MAX last_accessed_at; null khi không có cặp activity. |

### Ví dụ local runtime

{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Course analytics retrieved.",
  "data": {
    "tracked_lesson_accesses": 405,
    "students_with_activity": 28,
    "last_activity_at": "2026-10-25T09:15:00"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000002"
}

405 là số cặp learner/lesson đang có dấu truy cập, không phải 405 lần truy cập. Khi không có dữ liệu, hai count là 0 và last_activity_at là null.

## Error response note

HTTP/business code giữ direct set 401/403/404/500. Shared error helper serializes error data as null when no data is supplied. Trace ID được phản hồi trong envelope và X-Trace-Id.

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
