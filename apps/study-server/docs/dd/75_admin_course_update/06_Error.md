---
title: "Error"
order: 6
dd_id: "75"
api_name: "Cập nhật metadata khóa học Admin"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các nhánh bên dưới giữ nguyên HTTP status và business code của catalog #75. Điều kiện chi tiết cho body, authorization policy và database vẫn cần được chủ sở hữu contract xác nhận.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Authorization | Bearer JWT thiếu/sai hoặc không xác thực được | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A — catalog chỉ định business code | [05_Data_Mapping.md](./05_Data_Mapping.md) | No transaction | Direct code; auth behavior by current source is absent for Admin. |
| 2 | Authorization | Yes | Admin permission | Principal không có role Admin hoặc course-management permission | 403 | `DESIGN_ACCESS_DENIED` | N/A — catalog chỉ định business code | [05_Data_Mapping.md](./05_Data_Mapping.md) | No transaction | Permission policy `SOURCE_REQUIRED`. |
| 3 | Not found | Yes | `course_id` | Không có course row sau Q1 update predicate | 404 | `DESIGN_RESOURCE_NOT_FOUND` | N/A — catalog chỉ định business code | [05_Data_Mapping.md](./05_Data_Mapping.md) | Rollback candidate transaction | Condition is `DERIVED` from update-by-ID. |
| 4 | Validation | Yes | Path/body | Path parse hoặc body field không hợp lệ theo rules đã được duyệt | 422 | `DESIGN_VALIDATION_ERROR` | N/A — catalog chỉ định business code | [05_Data_Mapping.md](./05_Data_Mapping.md) | No transaction | Field-level constraints not defined by catalog. |
| 5 | System error | Yes | Database/response mapping | Query, required mentor mapping or commit fails | 500 | `DESIGN_INTERNAL_ERROR` | N/A — catalog chỉ định business code | [05_Data_Mapping.md](./05_Data_Mapping.md) | Rollback if transaction started | Internal details must not leak. |

> Current middleware emits `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR` for paths outside `DESIGN_CONTRACT_PATHS`; API #75 is absent from that allowlist. Current `error_response` uses `data:{}` when omitted, while API guidelines specify `data:null`. These are current-source discrepancies for future wiring.

## Liên kết

- [03_Request.md](./03_Request.md) — direct path and proposed body fields.
- [05_Data_Mapping.md](./05_Data_Mapping.md) — validation, query, update and rollback steps.
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
