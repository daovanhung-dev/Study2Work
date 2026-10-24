---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Bảng dưới đây giữ đúng error set của API #50 trong catalog: HTTP 401/403/422/500. Điều kiện nhánh ở mức contract; chi tiết schema, course lookup và middleware wiring chưa được runtime xác minh.

## Error cases

| No | HTTP status | Business code | Điều kiện theo contract | Data Mapping step | Response/source rule | Status |
|---:|---:|---|---|---:|---|---|
| 1 | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Bearer JWT thiếu hoặc không hợp lệ | 1–2 | Error envelope; không trả token/claims | Code DIRECT; endpoint UNWIRED |
| 2 | 403 | `DESIGN_ACCESS_DENIED` | Principal không có role Mentor hoặc Mentor không có quyền quản lý course | 2 | Error envelope; không lộ quyền/ID nội bộ | Code DIRECT; access implementation SOURCE_REQUIRED |
| 3 | 422 | `DESIGN_VALIDATION_ERROR` | Request không đạt validation được xác nhận: required field/type/body shape; enum/payload rules sau khi có schema | 3 | Error envelope; không echo payload nhạy cảm | Code DIRECT; điều kiện chi tiết một phần SOURCE_REQUIRED |
| 4 | 500 | `DESIGN_INTERNAL_ERROR` | Lỗi nội bộ/persistence/mapping không dự kiến | 5–8 | Error envelope; không trả SQL/stack/provider detail | Code DIRECT; route chưa có |

## Tình huống chưa được định nghĩa

| Tình huống | Catalog có code tương ứng? | Ghi chú |
|---|---|---|
| Course ID không tồn tại | Không có 404 trong API #50 | Cần quyết định trả 422, 403 hay hành vi khác trong giới hạn contract; không tự thêm status/code. |
| Mentor không được assign course nhưng có role Mentor | 403 được khai báo | Quy tắc direct ownership/assignment và principal mapping cần source/approval. |
| `content_type` không phải enum member | 422 có thể là validation branch | Enum member set và validation source chưa có. |
| `payload` sai schema của subtype | 422 có thể là validation branch | Schema theo loại Content chưa có. |
| Race khi cấp `order` hoặc lặp request | Không có 409/idempotency contract | Concurrency/retry policy cần xác nhận; không invent code. |

## Middleware integration discrepancy

Route API #50 chưa tồn tại. Nếu route được wire trong tương lai mà path chưa được thêm vào `DESIGN_CONTRACT_PATHS`, validation fallback có thể trả `VALIDATION_ERROR` và exception fallback `INTERNAL_SERVER_ERROR`, khác catalog `DESIGN_VALIDATION_ERROR` / `DESIGN_INTERNAL_ERROR`. Đây là điều kiện tích hợp cần xử lý khi triển khai, không phải behavior API #50 hiện tại.

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
