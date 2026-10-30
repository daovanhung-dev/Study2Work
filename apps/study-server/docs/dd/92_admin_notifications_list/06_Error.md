---
title: "Error"
order: 6
dd_id: "92"
api_name: "Lấy notification list"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Error mapping

| No | Trigger | HTTP status | Business code | Message | Basis/status |
|---:|---|---:|---|---|---|
| E1 | Bearer token thiếu/sai | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Thông điệp xác thực an toàn | Code DIRECT; current shared guard |
| E2 | Token hợp lệ nhưng role không phải Admin | 403 | `DESIGN_ACCESS_DENIED` | Không có quyền quản lý thông báo | Code DIRECT; role guard current; permission chuyên biệt chưa có |
| E3 | Database operational/connection-invalidated error | 503 | `DESIGN_DEPENDENCY_UNAVAILABLE` | Notifications are temporarily unavailable. | Code DIRECT; DB trigger DERIVED |
| E4 | SQL error khác, count/row malformed hoặc projection failure | 500 | `DESIGN_INTERNAL_ERROR` | Notifications could not be retrieved. | Code DIRECT; mapping current source |
| E5 | `page` không phải int32 dương | 422 | `DESIGN_VALIDATION_ERROR` | Dữ liệu đầu vào không hợp lệ. | DERIVED; catalog không liệt kê 422 |

## Nguyên tắc lỗi

- Direct error set chỉ gồm 401, 403, 503 và 500; E5 là local fallback ngoài catalog.
- 503 chỉ dành cho SQLAlchemy `OperationalError` hoặc `DBAPIError.connection_invalidated`; không suy provider failure vì GET không gọi provider.
- Query trả rỗng hoặc page vượt trang cuối là 200 Page rỗng; không trả 404.
- Current `error_response` tạo envelope chuẩn; không trả raw SQL, stack trace hoặc thông tin nội bộ.
- `/api/v1/admin/notifications` hiện thuộc `DESIGN_CONTRACT_PATHS`; validation exception handler nhận diện path này.

## Ví dụ lỗi — 503

~~~json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "Notifications are temporarily unavailable.",
  "data": null,
  "meta": {},
  "traceId": "550e8400-e29b-41d4-a716-446655440000"
}
~~~

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `4.Error`
- Dimension: `A1:BR13`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `30`
- Số vùng merge: `10`

<details>
<summary>Danh sách vùng merge</summary>

- `C10:F10`
- `G10:I10`
- `J10:N10`
- `O10:X10`
- `Y10:AA10`
- `G11:I11`
- `G12:I12`
- `G13:I13`
- `AB10:AF10`
- `AG10:BA10`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Các trường hợp lỗi của API |  |
| 10 | `B10` | № |  |
| 10 | `C10` | Category |  |
| 10 | `G10` | Verify check |  |
| 10 | `J10` | Tên item |  |
| 10 | `O10` | Nội dung check |  |
| 10 | `Y10` | Error code |  |
| 10 | `AB10` | Error message ID |  |
| 10 | `AG10` | Remarks |  |
| 11 | `B11` | 1 |  |
| 11 | `C11` | system error |  |
| 11 | `G11` | - |  |
| 11 | `J11` | - |  |
| 11 | `O11` | Trường hợp lỗi truy cập DB |  |
| 11 | `Y11` | 9999 |  |
| 11 | `AB11` | DLG000000 |  |
| 12 | `B12` | 2 |  |
| 12 | `C12` | Check quyền |  |
| 12 | `G12` | - |  |
| 12 | `O12` | Trường hợp không có thông tin quyền tương ứng với user_id trong token |  |
| 12 | `Y12` | 1000 |  |
| 12 | `AB12` | STOCKERR1 |  |
| 12 | `AG12` | Trường hợp số record get được từ xử lý 0. của sheet [3.Data mapping] = 0 |  |
| 13 | `B13` | 3 |  |
| 13 | `C13` | check tồn tại |  |
| 13 | `G13` | 〇 |  |
| 13 | `O13` | Trường hợp không có thông tin parameter trong request data |  |
| 13 | `Y13` | 1001 |  |
| 13 | `AB13` | DLG000093 |  |

</details>
