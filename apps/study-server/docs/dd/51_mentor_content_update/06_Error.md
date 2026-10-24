---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

API #51 giữ nguyên 5 lỗi trong catalog. Body-validation conditions dưới đây chỉ áp dụng nếu proposed body được chấp thuận; route hiện chưa tồn tại.

## Error cases

| No | HTTP status | Business code | Điều kiện theo contract | Data Mapping step | Response/source rule | Status |
|---:|---:|---|---|---:|---|---|
| 1 | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Bearer JWT thiếu/không hợp lệ | 1 | Error envelope; không trả token/claims | Code DIRECT; runtime route absent |
| 2 | 403 | `DESIGN_ACCESS_DENIED` | Không phải Mentor hoặc không có quyền quản lý course chứa Content | 2–4 | Error envelope; không tiết lộ thông tin quyền nội bộ | Code DIRECT; exact access predicate SOURCE_REQUIRED |
| 3 | 404 | `DESIGN_RESOURCE_NOT_FOUND` | `content_id` không tồn tại | 4 | Error envelope; không trả dữ liệu một phần | Code DIRECT; physical lookup SOURCE_REQUIRED |
| 4 | 422 | `DESIGN_VALIDATION_ERROR` | Validation không đạt theo contract; field-specific conditions của proposed body cần duyệt | 2–3 | Error envelope; không echo payload nhạy cảm | Code DIRECT; body proposal DERIVED |
| 5 | 500 | `DESIGN_INTERNAL_ERROR` | Lỗi bất ngờ khi đọc/cập nhật Content hoặc version | 4–8 | Safe error envelope; không trả SQL/stack/provider detail | Code DIRECT; route absent |

## Các nhánh cần xác nhận

| Tình huống | Contract code hiện có | Ghi chú |
|---|---|---|
| Content tồn tại nhưng Mentor không có quyền quản lý course | 403 | AC-22 permission direct; identity/assignment query chưa có nguồn. |
| Content ở trạng thái không cho phép sửa | 422 candidate only | AC-22 không chỉ rõ editable statuses; không thêm 409. |
| ContentType không hợp lệ hoặc payload sai subtype | 422 nếu proposed body được duyệt | Enum/payload schema chưa có. |
| Hai PUT đồng thời hoặc revision race | Không có 409 | Cần concurrency/version policy; không tự thêm code/status. |
| Body thiếu/không hợp lệ | 422 nếu body proposal được duyệt | Catalog hiện không khai báo body; phải chốt contract trước implementation. |

## Middleware integration discrepancy

API #51 chưa được wire và path hiện không nằm trong `DESIGN_CONTRACT_PATHS`. Nếu thêm route mà không cập nhật allowlist, validation/unhandled fallback có thể trả `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` thay vì `DESIGN_VALIDATION_ERROR`/`DESIGN_INTERNAL_ERROR`. Đây là integration requirement tương lai, không phải current API behavior.

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
