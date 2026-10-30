---
title: "Error"
order: 6
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng error set API #60: 401, 403, 404, 422, 500. Không thêm 409, 503 hoặc 400 ngoài catalog.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Header thiếu hoặc token không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | No | Shared MENTOR guard. |
| 2 | Authorization | Role/scope | Mentor/request | Role sai hoặc request thuộc direct course owner khác | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | Yes after Q1 | Request exists before owner branch under API #59 pattern. |
| 3 | Not found | Request lookup | SupportRequest | Không có request ID tương ứng | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | Yes | Local BIGSERIAL lookup. |
| 4 | Not found | Asset scope | attachment_refs[] | ID hợp lệ cú pháp nhưng không resolve đúng owner/course/LECTURE/UPLOADED | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | Yes | Generic response; không lộ asset ngoài scope. |
| 5 | Request validation | Path/body/ref syntax | request_id, message, attachment_refs | Sai/overflow int64; field thiếu/sai kiểu; message blank; JSON refs sai shape/non-integer/duplicate | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | No before DB write | Nonblank and JSON-array policy are DERIVED. |
| 6 | System error | DB/projection/transaction | SupportRequest/SupportMessage | Query, parent integrity, insert/link, mapping, reload hoặc commit thất bại | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | Yes | Rollback before response; safe log by trace only. |

> Catalog không khai báo mã state-conflict HTTP 409. API #60 không sửa status; post-resolve reply policy vẫn cần business owner xác nhận.

> API Guidelines và current helper có khác biệt serialization error data; API #60 dùng shared error_response convention khi runtime được wiring.

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
