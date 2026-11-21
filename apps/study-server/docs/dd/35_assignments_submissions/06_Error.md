---
title: "Error"
order: 6
dd_id: "35"
api_name: "Tạo/nộp submission"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các error cases dưới đây giữ nguyên status/business code theo API catalog #35. Điều kiện chi tiết chỉ được nêu khi nguồn xác nhận; các predicate còn thiếu được đánh dấu SOURCE_REQUIRED. Error envelope đặt data=null theo API Guidelines.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Required | Authorization | Bearer JWT thiếu hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | SOURCE_REQUIRED | 0.1 / 6.2 | No | Catalog-confirmed status/code; no API #35 route is wired. |
| 2 | Authorization | Required | Student role / assignment access | Role không phải Student hoặc access predicate từ chối; predicate cụ thể SOURCE_REQUIRED | 403 | DESIGN_ACCESS_DENIED | SOURCE_REQUIRED | 0.1 / 2.2 | No | AC-17 requires permission; exact ownership/enrollment rule is not defined. |
| 3 | Resource lookup | Required | assignment_id | Không tìm thấy assignment theo candidate lookup | 404 | DESIGN_RESOURCE_NOT_FOUND | SOURCE_REQUIRED | 2.1 / 6.2 | No | Candidate lookup only; physical runtime source is absent. |
| 4 | Request validation | Required | assignment_id, text, file refs | Missing field, invalid declared type or parser validation failure; detailed rules SOURCE_REQUIRED | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | 1.2 / 6.2 | No | Preserve the catalog code; no length/empty/file-reference policy is invented. |
| 5 | State conflict | Conditional | Assignment/submission state | AC-17 shows a 403/409 branch for overdue or disallowed submission; exact 409 predicate and duplicate/resubmission mapping SOURCE_REQUIRED | 409 | DESIGN_STATE_CONFLICT | SOURCE_REQUIRED | 2.2 / 3 / 6.2 | SOURCE_REQUIRED | Catalog code exists; do not map every conflict or late request without policy. |
| 6 | System error | N/A | Internal operation | Unexpected database or application failure | 500 | DESIGN_INTERNAL_ERROR | SOURCE_REQUIRED | 4 / 6.2 | SOURCE_REQUIRED if a mutation/transaction has begun | Return safe message; do not expose SQL, stack traces or provider details. |

> Không thêm 400, 503 hoặc business code ngoài API #35 catalog. Exact localized message and field-error detail are not specified.
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
