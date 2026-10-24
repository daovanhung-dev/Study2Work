---
title: "Error"
order: 6
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

<a id="error-401"></a>

## Error cases

| No | Category | Verify check | Item/field | Condition | HTTP status | Business/Error code | Message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer JWT | Authorization | Missing or invalid token | 401 | DESIGN_AUTHENTICATION_REQUIRED | SOURCE_REQUIRED | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-permission) | N/A | Status/code direct; route absent |
| 2 | Authorization | Admin permission | Principal | Caller lacks Admin role/permission | 403 | DESIGN_ACCESS_DENIED | SOURCE_REQUIRED | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-permission) | N/A | Policy SOURCE_REQUIRED |
| 3 | Validation | Request body | recipients | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 1](./05_Data_Mapping.md#step-1-read-request) | Write behavior TBD | Field rule SOURCE_REQUIRED |
| 4 | Validation | Request body | recipients[] | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 2](./05_Data_Mapping.md#step-2-resolve-audience) | Write behavior TBD | Element rule SOURCE_REQUIRED |
| 5 | Validation | Request body | segment | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 2](./05_Data_Mapping.md#step-2-resolve-audience) | Write behavior TBD | Enum rule SOURCE_REQUIRED |
| 6 | Validation | Request body | title | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 1](./05_Data_Mapping.md#step-1-read-request) | Write behavior TBD | Direct field required; other rules unspecified |
| 7 | Validation | Request body | content | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 1](./05_Data_Mapping.md#step-1-read-request) | Write behavior TBD | Direct field required; other rules unspecified |
| 8 | Validation | Request body | channels | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 1](./05_Data_Mapping.md#step-1-read-request) | Write behavior TBD | Direct field required; array rules unspecified |
| 9 | Validation | Request body | channels[] | Approved schema validation fails; exact predicate TBD | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [Step 4](./05_Data_Mapping.md#step-4-accept-and-dispatch) | Write behavior TBD | Channel token rule SOURCE_REQUIRED |
| 10 | Dependency | Acceptance dependency | Queue/dispatch | Dependency unavailable before acceptance | 503 | DESIGN_DEPENDENCY_UNAVAILABLE | SOURCE_REQUIRED | [Step 4](./05_Data_Mapping.md#step-4-accept-and-dispatch) | Transaction boundary SOURCE_REQUIRED | Trigger is DERIVED |
| 11 | System | Internal processing | Persistence/processing | Unexpected internal failure | 500 | DESIGN_INTERNAL_ERROR | SOURCE_REQUIRED | [Step 3](./05_Data_Mapping.md#step-3-create-notification) | Rollback SOURCE_REQUIRED | Do not expose internals |

## Error contract boundaries

- Exact status/code set matches API #93.
- Do not add 400, 404, 409 or other codes absent from the catalog.
- Field messages and error-envelope details are not specified for #93.
- API Guidelines specify null error data; current helper/future middleware behavior is not verified.
- No runtime error branch exists for #93.
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
