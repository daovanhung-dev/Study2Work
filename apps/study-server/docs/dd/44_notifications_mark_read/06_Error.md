---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "44"
api_name: "Đánh dấu một thông báo đã đọc"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Mỗi error case dưới đây giữ nguyên `HTTP` `status` và business code đã khai báo riêng cho API #44 trong catalog. Không thêm lỗi ngoài contract.

## Error cases

| No | Category | Verify check | Item | Condition | `HTTP` `status` | Error code | Error `message` ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | `Bearer`/`JWT` validation | `Authorization` | Header thiếu/sai format, token không hợp lệ hoặc claim không hợp lệ. | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A — catalog không khai báo `message` ID. | [05_Data_Mapping.md#0-check-quyền](./05_Data_Mapping.md#0-check-quyền) | N/A | Không tiết lộ token/claim. |
| 2 | `Authorization` | `Student` role check | Role trong `JWT` | Token hợp lệ nhưng không có role `Student`. | 403 | `DESIGN_ACCESS_DENIED` | N/A — catalog không khai báo `message` ID. | [05_Data_Mapping.md#0-check-quyền](./05_Data_Mapping.md#0-check-quyền) | N/A | Không truy cập DB trước khi auth pass. |
| 3 | Not found / ownership | M1 `RETURNING` row count | `notification_id` | Không có row thỏa ID và principal; gồm nonexistent, user khác hoặc `user_id` IS NULL. | 404 | `DESIGN_RESOURCE_NOT_FOUND` | N/A — catalog không khai báo `message` ID. | [05_Data_Mapping.md#3-update-read-state](./05_Data_Mapping.md#3-update-read-state) | No change | Cùng `status` để không xác nhận sự tồn tại của row user khác. |
| 4 | Validation | `int64` path parse | `notification_id` | Path không parse được thành `int64` hoặc nằm ngoài miền `int64`. | 422 | `DESIGN_VALIDATION_ERROR` | N/A — catalog không khai báo `message` ID. | [05_Data_Mapping.md#1-validate-data-input](./05_Data_Mapping.md#1-validate-data-input) | N/A | Giá trị `int64` hợp lệ nhưng không có row trả 404; không thêm positivity rule. |
| 5 | System error | `UPDATE`/`RETURNING`/commit/response mapping | `notifications` candidate | Lỗi database hoặc lỗi nội bộ ngoài dự kiến. | 500 | `DESIGN_INTERNAL_ERROR` | N/A — catalog không khai báo `message` ID. | [05_Data_Mapping.md#3-update-read-state](./05_Data_Mapping.md#3-update-read-state) | Yes — rollback transaction | Không trả SQL, stack trace, token hoặc secret. |

## Không thêm error ngoài catalog

- Không thêm 409 cho request lặp lại; gán state `TRUE` là idempotent candidate.
- Không thêm lỗi riêng cho notification đã đọc.
- Không thêm lỗi 404 riêng để phân biệt notification user khác/broadcast.
- Error body theo API guideline là `data`:null, nhưng current helper khác; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

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
