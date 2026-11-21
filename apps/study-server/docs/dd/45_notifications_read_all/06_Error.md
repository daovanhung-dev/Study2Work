---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "06 Error"
format: markdown
dd_id: "45"
api_name: "Đánh dấu tất cả đã đọc"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các error case dưới đây giữ nguyên status và business code được khai báo cho API #45 trong catalog. No unread row là thành công no-op; body validation details là proposal `DERIVED` dùng 422 có sẵn.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT validation | `Authorization` | Header thiếu/sai format, token không hợp lệ hoặc claim không hợp lệ. | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#0-lấy-principal](./05_Data_Mapping.md#0-lấy-principal) | N/A | Không lộ token/claim. |
| 2 | Authorization | Student role check | Role trong JWT | Token hợp lệ nhưng không có role Student. | 403 | `DESIGN_ACCESS_DENIED` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#0-lấy-principal](./05_Data_Mapping.md#0-lấy-principal) | N/A | Không truy vấn DB trước khi auth pass. |
| 3 | Validation | JSON parse/type check | Request body | JSON sai cú pháp hoặc body không phải object theo empty-body proposal. | 422 | `DESIGN_VALIDATION_ERROR` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#1-validate-body](./05_Data_Mapping.md#1-validate-body) | N/A | Trigger `DERIVED`; body omission rule cần xác nhận. |
| 4 | Validation | Empty-object check | Request body | JSON object có property theo empty-body proposal. | 422 | `DESIGN_VALIDATION_ERROR` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#1-validate-body](./05_Data_Mapping.md#1-validate-body) | N/A | Không tự thêm request field. |
| 5 | System error | M1 update/returning/mapping/commit | `notifications` candidate | Database, response mapping hoặc commit lỗi ngoài dự kiến. | 500 | `DESIGN_INTERNAL_ERROR` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#2-bulk-update](./05_Data_Mapping.md#2-bulk-update) | Yes — rollback caller-owned transaction when available | Không trả SQL/stack trace/secret. |

## Không thêm error ngoài catalog

- Không có unread row vẫn trả 200 success với empty Page — proposal `DERIVED`.
- Không thêm 404 vì request không nhắm một notification ID.
- Không thêm 409 cho request lặp lại; state assignment là idempotent.
- Không thêm 503; API catalog chỉ khai báo 500 cho dependency/internal failure.
- Envelope guideline yêu cầu `data:null`, current helper fallback là `{}`; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
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
