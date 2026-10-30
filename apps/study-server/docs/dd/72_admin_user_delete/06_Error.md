---
title: "Error"
order: 6
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

| No | Category | Verify check | Item/field | Condition | HTTP status | Business/Error code | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Missing, malformed or invalid token | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | [0.1](./05_Data_Mapping.md#0-check-quyen) | No DB transaction | Shared guard. |
| 2 | Authorization | Role | ADMIN | Valid JWT lacks ADMIN role | 403 | `DESIGN_ACCESS_DENIED` | [0.1](./05_Data_Mapping.md#0-check-quyen) | No DB transaction | Dedicated permission policy is not source-backed. |
| 3 | Range/format | Path parse | user_id | Raw path is not signed int64 or overflows | 422 | `DESIGN_VALIDATION_ERROR` | [1](./05_Data_Mapping.md#1-validate-data-input) | No DB transaction | DERIVED mapping using direct catalog code. |
| 4 | Not found | Mutation result | users.id | No row returned: target absent or already DELETED | 404 | `DESIGN_RESOURCE_NOT_FOUND` | [4.4](./05_Data_Mapping.md#44-ngoai-truong-hop-tren) | Rollback | No additional 409. |
| 5 | Database | UPDATE | users | SQL execution failure | 500 | `DESIGN_INTERNAL_ERROR` | [3](./05_Data_Mapping.md#3-insertupdate-thong-tin) | Rollback | Do not expose SQL details. |
| 6 | Mapping | RETURNING | id/deleted_at | ID mismatch or timestamp is not datetime | 500 | `DESIGN_INTERNAL_ERROR` | [4.1](./05_Data_Mapping.md#41-thanh-cong) | Rollback | No commit on invalid projection. |
| 7 | Transaction | COMMIT | users | Commit failure | 500 | `DESIGN_INTERNAL_ERROR` | [4.2](./05_Data_Mapping.md#42-loi-he-thong) | Rollback attempt | Safe response only. |

Error envelopes use `data: null` from the current shared `error_response(...)`. No policy-specific 422 dependency branch is implemented: selected fallback preserves all relation rows and does not break FK references. No 409 code is added.

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
