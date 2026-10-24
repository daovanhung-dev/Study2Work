---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "43"
api_name: "Lấy notification list"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Danh sách dưới đây giữ nguyên các error case của API #43 trong catalog. Không thêm 404/409/422/503 ngoài contract. HTTP/business code theo catalog; error response envelope dùng guideline hiện có và cần lưu ý discrepancy của helper runtime.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP `status` | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/`JWT` validation | `Authorization` | Header thiếu, malformed, token không hợp lệ hoặc claim không hợp lệ. | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#0-lấy-principal](./05_Data_Mapping.md#0-lấy-principal) | N/A | Không trả chi tiết token/claim. |
| 2 | `Authorization` | `Student` role check | Role trong `JWT` | Token hợp lệ nhưng không có role `Student`. | 403 | `DESIGN_ACCESS_DENIED` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#0-lấy-principal](./05_Data_Mapping.md#0-lấy-principal) | N/A | Dùng principal từ `JWT`, không nhận `user_id` từ client. |
| 3 | System error | Query/mapping failure | notifications candidate query | Lỗi database hoặc lỗi nội bộ ngoài dự kiến trong Q1/Q2/mapping. | 500 | `DESIGN_INTERNAL_ERROR` | N/A — catalog không định nghĩa message ID. | [05_Data_Mapping.md#4-đọc-page-và-count](./05_Data_Mapping.md#4-đọc-page-và-count) | N/A | Không lộ raw SQL, stack trace hoặc secret. |

## Không thêm error ngoài catalog

- Empty list hoặc page vượt tổng số trang không phải 404 — đề xuất DERIVED.
- Query page < 1, page ngoài int32 hoặc boolean không parse được chưa có behavior được xác nhận; không tự thêm 422.
- SOURCE_REQUIRED mapping gap là blocker thiết kế/schema, không tự chuyển thành error code runtime mới.
- Lỗi envelope data giữa guideline và shared helper đang lệch; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
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
