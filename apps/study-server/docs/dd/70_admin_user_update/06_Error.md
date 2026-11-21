---
title: "Error"
order: 6
dd_id: "70"
api_name: "Cập nhật thông tin/role Conditional"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Nội dung check | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Direct status/code; shared ADMIN guard hiện wired. |
| 2 | Authorization | ADMIN claim | Principal | Caller không có role ADMIN | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Direct status/code; permission/tenant/MFA mapping riêng chưa xác minh. |
| 3 | Not found | UPDATE RETURNING | user_id | Không có user row được cập nhật | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-query) | Rollback | Direct code/status; zero-row mapping DERIVED. |
| 4 | Validation | Path/body | Request input | Path sai int64 hoặc body vi phạm schema fallback | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | N/A | Direct code/status; full-replacement body/rules DERIVED. |
| 5 | System error | Database/mapping/transaction | Update pipeline | Query, projection hoặc commit thất bại | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-query) | Rollback | Direct status/code; response không lộ SQL/stack. |

Không thêm HTTP status, business code hoặc error-message ID ngoài catalog.

## Runtime branch mapping — một phần DERIVED

| Condition | Candidate or question | Status |
|---|---|---|
| user_id malformed/overflow | Trả 422 `DESIGN_VALIDATION_ERROR` trước query. | Runtime behavior; path mapping DERIVED. |
| Body thiếu field/extra field/invalid role | Framework validation trả 422 `DESIGN_VALIDATION_ERROR`. | Runtime behavior; body schema/allowlist DERIVED. |
| User row không tồn tại | UPDATE RETURNING không có row; rollback và trả 404. | Runtime behavior; no-row mapping DERIVED. |
| Role ngoài allowlist | `STUDENT`, `MENTOR`, `ADMIN` là các role labels hiện có; giá trị khác trả 422. | Allowlist DERIVED; transition policy SOURCE_REQUIRED. |
| Session token có role cũ sau update role | #70 không revoke refresh token; access JWT guard hiện kiểm tra role từ claim. | No side effect implemented; token policy SOURCE_REQUIRED. |
| Error data null hay empty object | Current `error_response` serializes omitted data as JSON null. | Resolved by current source; no helper change. |

## Error envelope và middleware hiện hành

- Current `error_response` serializes omitted error data as `null`; tests assert this behavior.
- Middleware already matches `/api/v1/admin/users/{user_id}` from API #69 and maps API #70 framework validation failures to `DESIGN_VALIDATION_ERROR`.
- Shared error helper/middleware were not changed for API #70.

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
