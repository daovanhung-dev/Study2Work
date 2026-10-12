---
title: "Error"
order: 6
dd_id: "30"
api_name: "Autosave/lưu câu trả lời"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các trường hợp lỗi dưới đây giữ nguyên status và business code của API #30 trong API catalog. Predicate hoặc code mapping chưa được nguồn chốt được ghi SOURCE_REQUIRED; không thêm mã lỗi ngoài contract.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Business code | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Token thiếu, sai định dạng hoặc không hợp lệ theo authentication policy. | 401 | DESIGN_AUTHENTICATION_REQUIRED | [Step 0](./05_Data_Mapping.md) | No | API catalog. |
| 2 | Authorization | Yes | Student role / attempt access | Role không phải Student hoặc access bị từ chối theo policy đã duyệt. | 403 | DESIGN_ACCESS_DENIED | [Step 0](./05_Data_Mapping.md) | No | Ownership predicate và cách xử lý attempt của user khác SOURCE_REQUIRED. |
| 3 | Resource lookup | Yes | Attempt / question | Resource lookup không tìm thấy attempt hoặc question theo contract-level mapping. | 404 | DESIGN_RESOURCE_NOT_FOUND | [Step 2](./05_Data_Mapping.md) | No | Phân biệt absent/cross-quiz/foreign-owner cases chưa được chốt. |
| 4 | Validation | Yes | attempt_id, question_id, answer(s) | Required/type/schema validation fails under the approved policy. | 422 | DESIGN_VALIDATION_ERROR | [Step 1](./05_Data_Mapping.md) | No | Exact limits, answer shape and parse behavior SOURCE_REQUIRED. |
| 5 | System error | No | Database / internal processing | Unhandled internal error while reading candidate records or applying the answer upsert. | 500 | DESIGN_INTERNAL_ERROR | [Steps 2–4](./05_Data_Mapping.md) | TBD | Rollback depends on approved transaction boundary and runtime implementation. |

> API #30 catalog does not list 409. Error data is null per shared API guidelines. Exact message and field-error details are not defined.
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

