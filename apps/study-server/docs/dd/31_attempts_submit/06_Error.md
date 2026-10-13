---
title: "Error"
order: 6
dd_id: "31"
api_name: "Khóa attempt và bắt đầu chấm"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các error case giữ nguyên HTTP status và business code của API #31 trong API catalog. Những predicate hoặc code mapping chưa được nguồn chốt được ghi SOURCE_REQUIRED; không thêm code ngoài contract.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Business code | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Token thiếu, sai định dạng hoặc không hợp lệ theo authentication policy. | 401 | DESIGN_AUTHENTICATION_REQUIRED | [Step 0](./05_Data_Mapping.md) | No | API catalog. |
| 2 | Authorization | Yes | Student role / attempt access | Role khác Student hoặc access bị từ chối theo policy đã duyệt. | 403 | DESIGN_ACCESS_DENIED | [Step 0](./05_Data_Mapping.md) | No | Owner predicate và foreign-owner masking SOURCE_REQUIRED. |
| 3 | Resource lookup | Yes | attempt_id | Không tìm thấy attempt theo contract-level resource lookup. | 404 | DESIGN_RESOURCE_NOT_FOUND | [Step 2](./05_Data_Mapping.md) | No | Attempt của user khác có thể là 403 hoặc masked 404; chưa được chốt. |
| 4 | Validation | Yes | attempt_id | Path/schema validation không đạt theo policy được duyệt. | 422 | DESIGN_VALIDATION_ERROR | [Step 1](./05_Data_Mapping.md) | No | Positive/range, parse/overflow và field-error mapping SOURCE_REQUIRED. |
| 5 | State conflict | Yes | Attempt lifecycle / duplicate submit | Attempt không ở trạng thái cho phép submit hoặc request cạnh tranh tạo state conflict. | 409 | DESIGN_STATE_CONFLICT | [Steps 2–3](./05_Data_Mapping.md) | TBD | Trigger, repeat-submit response và lock behavior SOURCE_REQUIRED. |
| 6 | System error | No | Database / grading / internal processing | Lỗi nội bộ khi đọc attempt/answers, chấm hoặc lưu trạng thái/kết quả. | 500 | DESIGN_INTERNAL_ERROR | [Steps 2–5](./05_Data_Mapping.md) | TBD | Transaction and rollback behavior are unresolved. |

> API catalog does not define exact message text or field-error details. Error data is null per shared API guidelines. No 503 or other code is added.
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
