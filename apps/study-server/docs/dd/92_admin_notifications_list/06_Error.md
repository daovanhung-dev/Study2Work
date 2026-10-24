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
| E1 | Bearer token thiếu/sai theo Admin auth policy | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Thông điệp xác thực an toàn | Code DIRECT; guard/claim chưa có source |
| E2 | Token hợp lệ nhưng không có Admin role hoặc notification-management permission | 403 | `DESIGN_ACCESS_DENIED` | Không có quyền quản lý thông báo | Code DIRECT; policy SOURCE_REQUIRED |
| E3 | Dependency không khả dụng | 503 | `DESIGN_DEPENDENCY_UNAVAILABLE` | Dịch vụ phụ thuộc hiện không khả dụng | Code DIRECT; trigger cụ thể chưa có trong #92 diagram |
| E4 | Query/mapping/internal failure không được xử lý riêng | 500 | `DESIGN_INTERNAL_ERROR` | Đã xảy ra lỗi nội bộ hệ thống. | Code DIRECT; endpoint chưa được wire |

## Nguyên tắc lỗi

- Direct error set chỉ gồm 401, 403, 503 và 500; không thêm 404 hoặc 422.
- #92 diagram chỉ nêu “Query notifications”; không chỉ rõ external dependency nên không gán DB outage, delivery provider hoặc operation service thành trigger 503.
- Query trả rỗng chưa có semantics được duyệt; catalog không khai báo 404 cho API list.
- API Guidelines yêu cầu error `data=null`; current `error_response` chuẩn hóa `None` thành `{}`. Đây là discrepancy có điều kiện khi API được wire, không phải behavior #92 hiện tại.
- `/api/v1/admin/notifications` chưa thuộc `DESIGN_CONTRACT_PATHS`; cập nhật allowlist và mapping khi implementation được phê duyệt, không coi DD là evidence runtime.

## Ví dụ lỗi — 503

Code/HTTP dưới đây trực tiếp theo catalog. Message là placeholder an toàn; điều kiện dependency chưa được nguồn chốt.

~~~json
{
  "success": false,
  "businessCode": "DESIGN_DEPENDENCY_UNAVAILABLE",
  "message": "Dịch vụ phụ thuộc hiện không khả dụng.",
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
