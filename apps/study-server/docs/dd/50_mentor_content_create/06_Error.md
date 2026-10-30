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

Bảng dưới đây giữ đúng error set của API #50 trong catalog: HTTP 401/403/422/500. Local route/test hiện xác minh các nhánh; live schema/deployment chưa được xác minh.

## Error cases

| No | HTTP status | Business code | Điều kiện theo contract | Data Mapping step | Response/source rule | Status |
|---:|---:|---|---|---:|---|---|
| 1 | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Bearer JWT thiếu hoặc không hợp lệ | 1–2 | Error envelope; không trả token/claims | Code DIRECT; local route test verified |
| 2 | 403 | `DESIGN_ACCESS_DENIED` | JWT role không phải Mentor; course không tồn tại; hoặc Mentor không trực tiếp sở hữu course | 2–3 | Error envelope chung; không phân biệt course vắng và ngoài quyền | Code DIRECT; absent-course mapping DERIVED |
| 3 | 422 | `DESIGN_VALIDATION_ERROR` | Body thiếu/sai type, payload không phải object, hoặc có field ngoài request contract | 3 | Error envelope + field errors; không echo payload | Code DIRECT; local framework TestClient verified |
| 4 | 500 | `DESIGN_INTERNAL_ERROR` | Query/order/insert/commit failure hoặc invalid DB projection/order range | 4–8 | Rollback; error envelope không trả SQL/stack/provider detail | Code DIRECT; local view/TestClient verified |

## Tình huống chưa được định nghĩa

| Tình huống | Catalog có code tương ứng? | Ghi chú |
|---|---|---|
| Course ID không tồn tại | Không có 404 trong API #50 | Implementation map cùng 403 `DESIGN_ACCESS_DENIED` như owner mismatch; DERIVED để tránh ID enumeration. |
| Mentor được assign nhưng không trực tiếp sở hữu course | 403 được khai báo | Current source chỉ hỗ trợ direct `courses.mentor_id`; assignment relation/policy vẫn SOURCE_REQUIRED. |
| `content_type` không phải enum member | 422 được khai báo | Chưa có enum member set nên hiện chỉ validate strict string; enum validation chưa thực hiện. |
| `payload` sai schema của subtype | 422 được khai báo | Chưa có schema subtype; hiện chỉ yêu cầu JSON object. |
| Race khi cấp `order` hoặc lặp request | Không có 409/idempotency contract | Row lock tuần tự hóa order allocation của API #50 trên cùng course; idempotency/retry vẫn chưa được quy định. |

## Middleware integration discrepancy

Route API #50 đã được thêm vào `DESIGN_CONTRACT_PATHS`. TestClient xác minh validation framework trả `DESIGN_VALIDATION_ERROR`; view tự map persistence/integrity errors thành `DESIGN_INTERNAL_ERROR`.

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
