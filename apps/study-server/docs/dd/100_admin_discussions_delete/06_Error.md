---
title: "Error"
order: 6
dd_id: "100"
api_name: "Xóa discussion theo policy"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các mã HTTP và business code dưới đây lấy nguyên từ catalog #100. Điều kiện chi tiết chỉ được khẳng định khi có nguồn trực tiếp; các trigger chưa rõ được giữ là câu hỏi.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | N/A | Bearer JWT | Thiếu hoặc không hợp lệ theo auth convention | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa nêu | Bước 0 | N/A | Code/status DIRECT; exact auth behavior source chưa có |
| 2 | Authorization | N/A | Admin role | Principal không đạt quyền Admin | 403 | `DESIGN_ACCESS_DENIED` | Chưa nêu | Bước 0 | N/A | Code/status DIRECT; Admin guard SOURCE_REQUIRED |
| 3 | Target not found | N/A | `discussion_id` | Không tìm thấy target theo key | 404 | `DESIGN_RESOURCE_NOT_FOUND` | Chưa nêu | Bước 2 | N/A | Code/status DIRECT; already-deleted policy chưa rõ |
| 4 | Request validation | N/A | `discussion_id` | Candidate: path không parse được thành int64 hoặc ngoài miền int64 | 422 | `DESIGN_VALIDATION_ERROR` | Chưa nêu | Bước 1 | N/A | Status/code DIRECT; trigger cụ thể cần xác nhận |
| 5 | Internal error | N/A | Persistence/handler | Lỗi nội bộ không được xử lý thành error cụ thể khác | 500 | `DESIGN_INTERNAL_ERROR` | Chưa nêu | Bước 3–5 | TBD | Status/code DIRECT; exact exception mapping chưa có |

> 422 là contract trực tiếp; việc malformed path được map vào 422 là candidate, chưa được implementation hoặc catalog chi tiết xác nhận.

## Response convention

Error envelope theo API guideline dùng `success:false`, `data:null`, `businessCode`, `message`, `meta` và `traceId`. Field-level detail chỉ xuất hiện khi có lỗi validate và mapping được triển khai. Đây là convention chung; #100 chưa có runtime để xác minh.
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
