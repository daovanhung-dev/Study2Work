---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "46"
api_name: "Lấy course Mentor được quản lý"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các lỗi dưới đây giữ đúng HTTP status và business code của API #46 trong API catalog. Điều kiện role/range/query là dự thảo; current Study source chưa có handler API #46.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Thiếu, sai định dạng hoặc không hợp lệ | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | N/A | 0 | N/A | Catalog direct. |
| 2 | Authorization | Role | `roles` | Principal không có role Mentor | `403` | `DESIGN_ACCESS_DENIED` | N/A | 0 | N/A | Catalog direct; guard cần định nghĩa. |
| 3 | Validation | Query type/value | `status` | Giá trị không thuộc CourseStatus được phê duyệt | `422` | `DESIGN_VALIDATION_ERROR` | N/A | 1.1 | N/A | Enum member list `SOURCE_REQUIRED`. |
| 4 | Validation | Query range | `page` | Không phải int32 hoặc nhỏ hơn 1 theo đề xuất | `422` | `DESIGN_VALIDATION_ERROR` | N/A | 1.2 | N/A | Range `DERIVED`, cần duyệt. |
| 5 | Validation | Query range | `size` | Không phải int32 hoặc ngoài 1..100 theo đề xuất | `422` | `DESIGN_VALIDATION_ERROR` | N/A | 1.3 | N/A | Max 100 `DERIVED` từ API #6. |
| 6 | System/integrity | Query/mapping | Course projection | DB lỗi hoặc field bắt buộc không map được | `500` | `DESIGN_INTERNAL_ERROR` | N/A | 2–3 | N/A | Không trả raw DB detail. |

> Catalog không khai báo 404 cho list API. Không ánh xạ danh sách rỗng thành lỗi.
>
> Error guideline yêu cầu `data: null`; current `error_response()` dùng `{}` khi không có data. Đây là `DISCREPANCY`, chưa có runtime API #46 để xác nhận.
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
