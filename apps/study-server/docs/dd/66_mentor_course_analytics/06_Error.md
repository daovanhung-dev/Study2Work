---
title: "Error"
order: 6
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error codes trực tiếp từ catalog

| HTTP | Business code | Trigger trong local runtime | Status |
|---:|---|---|---|
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Thiếu hoặc không xác thực được Bearer JWT. | Code/status DIRECT; shared auth helper wired. |
| 403 | DESIGN_ACCESS_DENIED | Principal thiếu role MENTOR hoặc course do Mentor khác sở hữu. | Code DIRECT; owner policy DERIVED từ courses.mentor_id. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | course_id không parse được signed int64 hoặc course không tồn tại. | Code DIRECT; path mapping local runtime. |
| 500 | DESIGN_INTERNAL_ERROR | Query lỗi hoặc aggregate projection sai schema/value. | Code/status DIRECT; safe mapping local runtime. |

Không thêm error code vào direct contract.

## Error response mapping

| Điều kiện | HTTP | Business code | Data | Side effect |
|---|---:|---|---|---|
| Bearer thiếu/sai/hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | null | Không truy vấn DB. |
| JWT hợp lệ nhưng thiếu role Mentor | 403 | DESIGN_ACCESS_DENIED | null | Không truy vấn DB. |
| course_id malformed/out of int64 range | 404 | DESIGN_RESOURCE_NOT_FOUND | null | Không truy vấn DB. |
| Course không tồn tại | 404 | DESIGN_RESOURCE_NOT_FOUND | null | Rollback read transaction. |
| Course không do Mentor hiện tại sở hữu | 403 | DESIGN_ACCESS_DENIED | null | Không chạy aggregate; rollback read transaction. |
| SQL hoặc response mapping lỗi | 500 | DESIGN_INTERNAL_ERROR | null | Rollback read transaction; không lộ SQL/stack trace. |

Shared error_response mặc định data absent thành JSON null. Middleware design-contract allowlist hiện đã bao gồm path #66; endpoint không sinh framework 422 cho path ID vì view parse raw path string.

## Security handling

- Xác thực role Mentor trước mọi query.
- Kiểm tra course owner trước aggregate và lặp owner predicate trong aggregate SQL.
- Không trả learner IDs, raw activity rows, SQL hoặc stack trace.
- Course access policy này là DERIVED từ legacy courses.mentor_id; chưa xác nhận assignment model/live schema.

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
