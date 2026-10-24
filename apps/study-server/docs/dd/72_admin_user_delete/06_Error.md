---
title: "Error"
order: 6
dd_id: "72"
api_name: "Xóa user theo policy AC-31"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | Status/code DIRECT; endpoint chưa wired. |
| 2 | Authorization | Admin policy | Admin/user-management permission | Principal không có quyền quản lý user | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | Status/code DIRECT; Admin guard SOURCE_REQUIRED. |
| 3 | Not found | Target lookup | user_id | Không tìm thấy target theo policy/schema được duyệt | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua) | No | Code/status DIRECT; no-row mapping DERIVED. |
| 4 | Validation/policy | Input or approved policy validation | Path/policy condition | Lỗi validation theo rule được duyệt | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | Candidate rollback only if mutation began | Code/status DIRECT; exact dependency conditions/mapping SOURCE_REQUIRED. |
| 5 | System error | Database/mutation/mapping | Delete pipeline | Lỗi nội bộ không xác định | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua) | Candidate rollback if policy transaction exists | Status/code DIRECT; do not return SQL or PII detail. |

Không thêm HTTP status, business code hoặc error-message ID ngoài catalog. 422 là response option trong catalog, không chứng minh mọi dependency phải map thành validation error.

## Candidate branch questions — không phải HTTP contract

| Condition | Candidate or question | Status |
|---|---|---|
| user_id malformed/overflow | Route/parser validation behavior chưa có source; catalog có 422 DESIGN_VALIDATION_ERROR. | SOURCE_REQUIRED |
| User không tồn tại | Candidate 404 DESIGN_RESOURCE_NOT_FOUND sau authorization. | DERIVED |
| User đã soft-delete/anonymized | Success lặp lại, 404 hay status khác chưa xác định. | SOURCE_REQUIRED |
| Dependency/policy không cho phép | Điều kiện, 422 mapping và response detail chưa được policy owner xác nhận. | SOURCE_REQUIRED |
| Mutation/query/commit failure | Catalog 500 DESIGN_INTERNAL_ERROR. | Code/status DIRECT; transaction rollback boundary tùy schema/policy chưa biết. |

## Error envelope discrepancy

- Study API guideline yêu cầu data:null cho error envelope.
- Current error_response helper thay data vắng mặt bằng {}.
- Middleware DESIGN_CONTRACT_PATHS chưa chứa /api/v1/admin/users/{user_id}; nếu route được wire sau này, mapping phải bổ sung để validation/unhandled errors dùng DESIGN_* catalog codes.
- Đây là hạ tầng hiện tại và discrepancy tích hợp có điều kiện; API #72 chưa wired nên chưa có endpoint runtime response.

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
