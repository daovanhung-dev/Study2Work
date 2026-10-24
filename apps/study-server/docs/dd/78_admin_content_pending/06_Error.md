---
title: "Error"
order: 6
dd_id: "78"
api_name: "Lấy pending content"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

- Giữ đúng 401/403/500 status và business codes của API catalog #78.
- Endpoint chưa có route/Admin guard; các hàng dưới là expected design branches, không phải runtime evidence.
- Catalog #78 không khai báo 404 hoặc 422; không thêm code/status cho queue rỗng hoặc invalid query.
- Query cardinality/page semantics và Content persistence vẫn là open questions; không ánh xạ chúng thành lỗi mới.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc hết hạn | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#0-check-quyen) | No | Status/code DIRECT; route/auth chưa wire. |
| 2 | Authorization | Admin role | Principal role | Principal hợp lệ nhưng không có role Admin | 403 | `DESIGN_ACCESS_DENIED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#0-check-quyen) | No | Code DIRECT; Admin claim/guard SOURCE_REQUIRED. |
| 3 | System error | Query/map response | Pending queue read | DB/query/content mapping failure | 500 | `DESIGN_INTERNAL_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#2-get-thong-tin) | No mutation | Code/status DIRECT; physical source/mapping chưa có. |

## Unresolved query parsing and result shape

- Unknown `type`, malformed/overflow `course`, `page<=0`, int32 overflow và empty queue behavior chưa được catalog quy định.
- API #78 không có 422/404; không tự ánh xạ những trường hợp này sang business code chưa khai báo.
- Catalog list/page mismatch phải được giải quyết trước khi chốt parser, pagination hoặc empty-result behavior.
- Candidate Page response có thể trả 200 với `items=[]`; candidate này là `DERIVED` và cần contract correction.

## Error envelope discrepancy

- API guideline yêu cầu error `data:null` và `meta.fieldErrors` cho validation error.
- Current `error_response()` đổi `data=None` thành `{}`.
- `DESIGN_CONTRACT_PATHS` hiện không có `/api/v1/admin/content/pending`; request-validation/unhandled-error fallback cho path chưa đăng ký dùng `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`, không khớp catalog.
- API #78 chưa wired; đây là conditional future-wiring discrepancy, không phải endpoint runtime behavior.

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
