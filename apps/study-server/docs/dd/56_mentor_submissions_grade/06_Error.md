---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Only the API catalog error set is permitted. Conditions below distinguish direct contract evidence from candidate interpretation and unresolved rules.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer JWT check | Authorization | Missing, invalid or expired authentication | 401 | DESIGN_AUTHENTICATION_REQUIRED | Catalog code | 0.1 | N/A before mutation | Direct catalog case; exact token errors use shared auth mapping when implemented |
| 2 | Authorization | Mentor role and course scope | Mentor access | Authenticated principal lacks Mentor role or course permission | 403 | DESIGN_ACCESS_DENIED | Catalog code | 0.3 | N/A before mutation | Mentor role is DIRECT; course predicate and inaccessible-row masking need confirmation |
| 3 | Resource existence | Submission lookup | submission_id | No candidate submission row exists | 404 | DESIGN_RESOURCE_NOT_FOUND | Catalog code | 0.3 | N/A before mutation | Missing-resource mapping is catalog-backed |
| 4 | Validation | Request parse/type | score | Required score is missing or is not an int32 value | 422 | DESIGN_VALIDATION_ERROR | Catalog code | 1 | N/A before mutation | Required field/type DIRECT; range rules unspecified |
| 5 | Validation | Request parse/type | rubric items | Required string descriptor is absent or wrong type | 422 | DESIGN_VALIDATION_ERROR | Catalog code | 1 | N/A before mutation | Exact wire key spelling and semantic validation SOURCE_REQUIRED |
| 6 | System | Persistence/mapping | Database or response mapping | Unexpected database or internal mapping failure | 500 | DESIGN_INTERNAL_ERROR | Catalog code | 4.2 | Transaction policy SOURCE_REQUIRED | Do not expose internal details; middleware allowlist does not include the dynamic API #56 route |

> No 409, 400, 503 or additional business code is added. Error messages are illustrative; exact text is not in the catalog.

> Current-source discrepancy: generic validation/system handlers use fallback VALIDATION_ERROR/INTERNAL_SERVER_ERROR when the request path is not in DESIGN_CONTRACT_PATHS. API #56 is absent from the current allowlist. Current error_response() also emits data={} when no error data is passed, while API Guidelines specifies data=null. These are conditional integration gaps because the route is unwired.
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
