---
title: "Error"
order: 6
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Nội dung check | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Status/code DIRECT; route chưa wired. |
| 2 | Authorization | Admin/user-management policy | Principal | Caller không có quyền Admin quản lý user | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Status/code DIRECT; policy SOURCE_REQUIRED. |
| 3 | Not found | User update result | user_id | Không tìm thấy user để update status | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-query) | Candidate rollback | Code/status DIRECT; zero-row condition DERIVED. |
| 4 | Validation | Request validation | Path/body status | Input sai schema/status policy được duyệt | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | Candidate rollback | Status/code DIRECT; exact body and validation rules chưa đặc tả. |
| 5 | System error | Database/session operation/mapping | Update pipeline | DB/query/mapping/transaction failure | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-query) | Candidate rollback | Status/code DIRECT; không trả raw SQL/token detail. |

Không thêm HTTP status, business code hoặc error-message ID ngoài catalog.

## Candidate branch questions — không phải HTTP contract

| Condition | Candidate or question | Status |
|---|---|---|
| user_id malformed/overflow | Behavior chưa được catalog nêu; không tự thêm status/code. | SOURCE_REQUIRED |
| Status field missing/null | Direct body schema không tồn tại trong catalog/diagram. | SOURCE_REQUIRED |
| Status value không thuộc enum đã duyệt | Catalog có 422, nhưng exact enum/rule/details cần contract owner xác nhận. | SOURCE_REQUIRED |
| User row không tồn tại | Zero-row UPDATE → 404 `DESIGN_RESOURCE_NOT_FOUND` là candidate. | DERIVED |
| Refresh-token revoke fails | Nếu conditional M2 được duyệt, transaction rollback và 500 là candidate. | DERIVED |
| Access JWT còn hạn sau khi khóa | Current guard không tra status/revocation; cần owner quyết định immediate-vs-expiry semantics. | SOURCE_REQUIRED |
| User đang ở target status | PATCH no-op behavior/updated_at behavior chưa định nghĩa; không thêm 409 vì catalog không có. | SOURCE_REQUIRED |

## Error envelope and routing discrepancy

- Shared `error_response` đổi data vắng mặt thành `{}`; server-study API guideline yêu cầu `data:null` cho error envelope.
- Current middleware `DESIGN_CONTRACT_PATHS` chưa chứa `/api/v1/admin/users/{user_id}/status`; future route phải cập nhật mapping để giữ business code `DESIGN_*`.
- API #71 chưa wired; các điểm trên là current infrastructure gaps, không phải runtime response hiện có của API #71.

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
