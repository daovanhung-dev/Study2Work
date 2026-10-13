---
title: "Error"
order: 6
dd_id: "34"
api_name: "Upload file"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các cases dưới đây giữ nguyên error status/business-code set của API #34 trong catalog. Điều kiện validation chi tiết và cách phân loại lỗi Object Storage còn cần xác nhận.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Required | Authorization | Bearer JWT thiếu, sai format, invalid hoặc expired. | 401 | DESIGN_AUTHENTICATION_REQUIRED | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#0-check-quyền) | N/A | Exact message and token failure detail are not defined in API #34 contract. |
| 2 | Authorization | Required | Role / upload scope | Authenticated principal không thuộc Student/Mentor hoặc không có quyền theo policy được duyệt. | 403 | DESIGN_ACCESS_DENIED | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#0-check-quyền) | N/A | Purpose/course ownership policy is SOURCE_REQUIRED. |
| 3 | Validation | Required | file | Required binary part is missing or request cannot be parsed as the declared multipart shape. | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#1-validate-request) | N/A | Exact parser errors, size and content checks are not specified. |
| 4 | Validation | Required | purpose | Required purpose field is missing or fails the eventual UploadPurpose contract. | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#1-validate-request) | N/A | Allowed values are not defined; do not invent them. |
| 5 | Validation | Conditional | course_id | Supplied course_id cannot be parsed as int64 under the eventual parser contract. | 422 | DESIGN_VALIDATION_ERROR | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#1-validate-request) | N/A | Positive range/existence semantics are not defined. |
| 6 | Dependency unavailable | Conditional | Object Storage | Storage dependency is unavailable under the eventual provider-failure classification. | 503 | DESIGN_DEPENDENCY_UNAVAILABLE | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#3-upload-to-object-storage) | N/A | Catalog permits 503; exact provider conditions and cleanup behavior are open. |
| 7 | System error | Conditional | Upload processing | Unexpected internal failure occurs outside the dependency-unavailable branch. | 500 | DESIGN_INTERNAL_ERROR | SOURCE_REQUIRED | [05_Data_Mapping.md](./05_Data_Mapping.md#3-upload-to-object-storage) | N/A | Do not expose credentials, storage details, raw provider body or stack trace. |

- The catalog defines only 401, 403, 422, 503 and 500 for API #34; no additional HTTP status or business code is added.
- API Guidelines require error data = null; safe field details, if approved, belong under meta.fieldErrors.
- There is no DB transaction or rollback mapping. Whether a partial/failed upload needs object cleanup is SOURCE_REQUIRED.
- API #13 maps its avatar-provider failures to 500; this separate endpoint does not establish API #34's 503/500 mapping.
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
