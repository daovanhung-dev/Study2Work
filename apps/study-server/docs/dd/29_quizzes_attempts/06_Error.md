---
title: "Error"
order: 6
dd_id: "29"
api_name: "Tạo attempt"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các trường hợp lỗi trong bảng giữ nguyên business code và HTTP status của API #29 trong API catalog. Predicate cụ thể chưa được nguồn chốt sẽ được ghi SOURCE_REQUIRED, không tự gán thêm mã lỗi.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Token thiếu hoặc không hợp lệ theo authentication policy. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — envelope uses message/businessCode | [Step 0](./05_Data_Mapping.md) | No | API catalog. |
| 2 | Authorization | Yes | Student role/access | Role không phải Student hoặc access bị từ chối theo policy đã duyệt. | 403 | DESIGN_ACCESS_DENIED | N/A — envelope uses message/businessCode | [Step 0](./05_Data_Mapping.md) | No | Exact entitlement predicate SOURCE_REQUIRED. |
| 3 | Resource lookup | Yes | quiz_id | Quiz không tồn tại theo contract-level resource lookup. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — envelope uses message/businessCode | [Step 2](./05_Data_Mapping.md) | No | Access masking policy is unresolved. |
| 4 | Validation | Yes | quiz_id | Path/schema validation fails under the approved policy. | 422 | DESIGN_VALIDATION_ERROR | N/A — envelope uses message/businessCode | [Step 1](./05_Data_Mapping.md) | No | Exact range and parse-error mapping SOURCE_REQUIRED. |
| 5 | State conflict | Yes | Attempt eligibility/state | Attempt cannot be created due to a state-conflict condition. | 409 | DESIGN_STATE_CONFLICT | N/A — envelope uses message/businessCode | [Step 2](./05_Data_Mapping.md) | TBD | AC-16 mentions exhausted/expired → 403/409 but does not map the branch. |
| 6 | System error | No | Database/internal processing | Unhandled internal error during lookup or candidate insert. | 500 | DESIGN_INTERNAL_ERROR | N/A — envelope uses message/businessCode | [Steps 2–5](./05_Data_Mapping.md) | TBD | Rollback depends on approved transaction boundary/runtime implementation. |

> Error messages are not defined by the API catalog. Error response data is null per API guidelines. No HTTP/business code outside the API #29 catalog is added.

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
