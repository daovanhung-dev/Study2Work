---
title: "Error"
order: 6
dd_id: "99"
api_name: "Điều chỉnh trạng thái kiểm duyệt discussion"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4. Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Danh sách dưới đây giữ nguyên HTTP status và business code trong catalog #99. Condition cụ thể chỉ được mô tả khi catalog hoặc AC-37 hỗ trợ; validation details, path parsing và persistence behavior còn cần xác nhận.

## Error cases

| # | Condition | HTTP | Business code | Basis/status |
|---:|---|---:|---|---|
| 1 | Thiếu hoặc không xác thực được Bearer/JWT | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | DIRECT catalog; token/Admin guard chưa có trong Study source |
| 2 | Principal đã xác thực nhưng không có role Admin | 403 | `DESIGN_ACCESS_DENIED` | DIRECT catalog; role claim policy `SOURCE_REQUIRED` |
| 3 | Không tìm thấy Discussion theo path ID | 404 | `DESIGN_RESOURCE_NOT_FOUND` | DIRECT catalog code; row-missing condition là `DERIVED` candidate |
| 4 | Request body/field/action không hợp lệ theo rule được duyệt | 422 | `DESIGN_VALIDATION_ERROR` | DIRECT code; exact validation rules chưa được định nghĩa |
| 5 | Lỗi nội bộ khi đọc/cập nhật/audit hoặc dựng response | 500 | `DESIGN_INTERNAL_ERROR` | DIRECT catalog; transaction/audit failure mapping chi tiết chưa rõ |

## Điểm chưa được định nghĩa

- Catalog không nêu riêng malformed/overflow `discussion_id` mapping; không tự thêm business code.
- Catalog không định nghĩa mã riêng cho action token không hỗ trợ, state conflict, discussion reply/root, đã bị ẩn/khóa hoặc audit failure.
- Không diễn giải action “xóa” thành 422 của #99; quyết định delete đi qua API #100.
- Shared API guideline mong muốn `data:null` cho error. Current helper trả `{}` nếu caller không truyền `data`; endpoint chưa được wire.
- Middleware hiện dùng fallback `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` cho path không nằm trong `DESIGN_CONTRACT_PATHS`; #99 chưa nằm trong allowlist.

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
