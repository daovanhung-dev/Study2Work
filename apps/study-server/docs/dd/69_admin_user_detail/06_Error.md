---
title: "Error"
order: 6
dd_id: "69"
api_name: "Lấy chi tiết user"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; route chưa wired. |
| 2 | Authorization | Role/policy | Admin user-management permission | Principal không có role/quyền Admin | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; Admin guard/policy SOURCE_REQUIRED. |
| 3 | Not found | User lookup | user_id | Không tìm thấy user theo candidate lookup | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-query) | No | Code/status DIRECT; điều kiện row-not-found là DERIVED. |
| 4 | System error | Database/profile mapping | Query or projection | Database/query/mapping failure | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-query) | No | DIRECT code/status; không trả raw SQL/stack trace. |

Không thêm HTTP 422 hoặc business code ngoài contract.

## Candidate branch questions — không phải HTTP contract

| Condition | Candidate or question | Status |
|---|---|---|
| user_id không parse được hoặc vượt miền int64 | HTTP behavior chưa được contract xác nhận; catalog không có 422 | SOURCE_REQUIRED |
| user_id là số hợp lệ nhưng không có row | 404 DESIGN_RESOURCE_NOT_FOUND | DERIVED theo detail resource semantics |
| User tồn tại nhưng caller không có Admin permission | 403; authorization phải chạy trước row lookup | Code/status DIRECT; policy implementation SOURCE_REQUIRED |
| Row bị xóa/ẩn/ẩn danh theo API #72 | Có trả 404, hồ sơ ẩn danh hay trạng thái khác | SOURCE_REQUIRED; policy còn mở sau document-level macro-review |

## Error envelope discrepancy

- Current error_response helper đổi data vắng mặt thành {}.
- API guideline yêu cầu data:null cho lỗi.
- Current middleware DESIGN_CONTRACT_PATHS chưa có /api/v1/admin/users/{user_id}; nếu route được nối mà allowlist không được cập nhật, request validation/unhandled exception có thể dùng fallback VALIDATION_ERROR/INTERNAL_SERVER_ERROR thay vì DESIGN_*.
- API #69 chưa wired; các điểm trên mô tả current infrastructure và conditional future integration, không phải endpoint runtime.

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
