---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Required | `Required` | `email` | `email` là `NULL/BLANK` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — dùng businessCode/message` | [Step 2.1](./05_Data_Mapping.md#21-required) | `No` | |
| 2 | Required | `Required` | `password` | `password` là `NULL/BLANK` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — dùng businessCode/message` | [Step 2.1](./05_Data_Mapping.md#21-required) | `No` | |
| 3 | Required | `Required` | `full_name` | `full_name` là `NULL/BLANK` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — dùng businessCode/message` | [Step 2.1](./05_Data_Mapping.md#21-required) | `No` | |
| 4 | Format | `Format` | `email` | `email` không đúng format email | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — dùng businessCode/message` | [Step 2.2](./05_Data_Mapping.md#22-email-format) | `No` | |
| 5 | Validation | `Policy` | `password` | Vi phạm password policy đã phê duyệt; threshold TBD | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — dùng businessCode/message` | [Step 2.3](./05_Data_Mapping.md#23-password-policy) | `No` | |
| 6 | State conflict | `Duplicate` | `email` | Query `Q1` trả `count(existing_user) > 0` | `409` | `DESIGN_STATE_CONFLICT` | `N/A — dùng businessCode/message` | [Step 3.2](./05_Data_Mapping.md#32-check-result) | `No` | Email đã tồn tại |
| 7 | Database | `Execute` | `users` | INSERT `users` thất bại | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — dùng businessCode/message` | [Step 6.2](./05_Data_Mapping.md#62-check-insert-result) | `Yes` | Không trả raw DB error |
| 8 | Dependency side effect | `Dispatch` | `verification email` | Email Provider/verification dispatch thất bại sau COMMIT | `N/A — registration đã commit` | `N/A — log/retry` | `N/A` | [Step 7.2](./05_Data_Mapping.md#72-verification-dispatch) | `No` | Không rollback và không tạo account trùng |

> Mỗi error case và mỗi field validation phải nằm trên một row riêng.

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
