---
title: "Response"
order: 4
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "2.Response"
format: markdown
dd_id: "37"
api_name: "Lấy tiến độ chi tiết course"
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
| Contract type | ApiEnvelope<UserProfile> theo API catalog; contract design-only, chưa runtime-verified. |

## Response fields

| No | Path | Logical name | Physical name | Type | Nullable | Source table | Source column | Source step | Transform | Null/empty/omit rule | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|---|
| 1 | success | Success | success | boolean | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T>. | N/A | Field từ contract envelope. |
| 2 | businessCode | Business code | businessCode | string | No | N/A | N/A | 4.1 | DESIGN_RESOURCE_RETRIEVED khi thành công. | N/A | Field từ catalog/guideline. |
| 3 | message | Message | message | string | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T>. | N/A | Nội dung cụ thể chưa được chốt cho endpoint. |
| 4 | data | Data | data | UserProfile | No | Chưa xác định | Chưa xác định | 4.1 | Theo catalog; không map được payload tiến độ từ nguồn hiện có. | N/A | Discrepancy: UserProfile không có progress fields. |
| 5 | meta | Metadata | meta | object | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T>. | Có thể dùng object rỗng nếu không có metadata; endpoint rule chưa nêu. | N/A |
| 6 | traceId | Trace ID | traceId | uuid | No | N/A | N/A | 4.1 | Theo ApiEnvelope<T>/guideline. | N/A | Trace ID của request theo policy chung. |
| 7 | data.id | User ID | id | int64 | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Không có mapping riêng được xác nhận cho API #37. |
| 8 | data.full_name | Họ tên | full_name | string | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Nguồn projection của endpoint chưa xác nhận. |
| 9 | data.email | Email | email | email | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Nguồn projection của endpoint chưa xác nhận. |
| 10 | data.role | Vai trò | role | UserRole | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Giá trị enum không được API #37 đặc tả thêm. |
| 11 | data.avatar_url | URL avatar | avatar_url | uri | Yes | Chưa xác định | Chưa xác định | 4.1 | Field optional của UserProfile reusable schema. | Omit nếu không có; endpoint chưa xác nhận null policy. | Không suy ra từ API #37. |
| 12 | data.bio | Giới thiệu | bio | string | Yes | Chưa xác định | Chưa xác định | 4.1 | Field optional của UserProfile reusable schema. | Omit nếu không có; endpoint chưa xác nhận null policy. | users DB design không có cột bio. |
| 13 | data.phone | Điện thoại | phone | string | Yes | Chưa xác định | Chưa xác định | 4.1 | Field optional của UserProfile reusable schema. | Omit nếu không có; endpoint chưa xác nhận null policy. | Không suy ra từ API #37. |
| 14 | data.status | Trạng thái user | status | UserStatus | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Giá trị enum không được API #37 đặc tả thêm. |
| 15 | data.created_at | Thời điểm tạo | created_at | date-time | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Nguồn projection của endpoint chưa xác nhận. |
| 16 | data.updated_at | Thời điểm cập nhật | updated_at | date-time | No | Chưa xác định | Chưa xác định | 4.1 | Field của UserProfile reusable schema. | N/A | Nguồn projection của endpoint chưa xác nhận. |

## Ví dụ thành công

Đây là ví dụ cấu trúc theo contract ApiEnvelope<UserProfile> trong catalog. Giá trị role và status là placeholder theo kiểu dữ liệu; enum thực tế chưa được định nghĩa tại catalog. Ví dụ không mô tả payload tiến độ vì schema đó chưa được phê duyệt.

```json
{
  "success": true,
  "businessCode": "DESIGN_RESOURCE_RETRIEVED",
  "message": "Resource retrieved",
  "data": {
    "id": 123,
    "full_name": "Sample Student",
    "email": "student@example.invalid",
    "role": "<UserRole>",
    "status": "<UserStatus>",
    "created_at": "2026-10-12T00:00:00Z",
    "updated_at": "2026-10-12T00:00:00Z"
  },
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000037"
}
```

## Ví dụ lỗi

Ví dụ lỗi 404 theo ApiEnvelope/guideline; điều kiện nghiệp vụ cụ thể dẫn tới 404 còn mở trong [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Resource not found",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000037"
}
```

## Response gap

- Catalog đã phê duyệt ApiEnvelope<UserProfile>; DD này giữ nguyên kiểu đó.
- AC-18 cần một kết quả có thể hiển thị tiến độ lesson, quiz và assignment theo course, nhưng UserProfile không định nghĩa các field này.
- Không có response progress DTO, field mapping, unit, nullability hay empty-state contract trong các nguồn đã đọc.
- Không dùng dữ liệu user profile làm thay thế cho response tiến độ; cần quyết định schema qua cập nhật contract có thẩm quyền.

---
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
