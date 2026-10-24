---
title: "Error"
order: 6
dd_id: "79"
api_name: "Lấy chi tiết content và metadata review"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

- Giữ đúng HTTP 401/403/404/500 và business codes API catalog #79.
- API #79 chưa có route/Admin guard; các cases là expected design, không phải runtime evidence.
- 404 cho Content không tồn tại là mapping candidate theo detail resource; status/version mismatch chưa được quy định thành error.
- Catalog không khai báo 409 hoặc 422; không thêm code/status cho stale queue item, revision conflict hoặc path parse.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#0-check-quyen) | No | Status/code DIRECT; route/auth chưa wire. |
| 2 | Authorization | Admin role | Principal role | Principal hợp lệ nhưng không có role Admin | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#0-check-quyen) | No | Code DIRECT; Admin claim/guard SOURCE_REQUIRED. |
| 3 | Resource not found | Content lookup | content_id | Q1 không có logical Content tương ứng | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#2-get-thong-tin) | No mutation | Catalog code DIRECT; missing-row mapping DERIVED. |
| 4 | System error | Query/map response | Content/version/author read | Query hoặc mapping failure | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#2-get-thong-tin) | No mutation | Code/status DIRECT; physical source/mapping chưa có. |

## Unresolved path and review-state behavior

- Malformed/overflow content_id và framework path parsing không được catalog #79 đặc tả.
- AC-33 queue #78 lọc PENDING_REVIEW; diagram không quy định #79 có trả 404 khi item đã đổi trạng thái hay trả Content với status hiện tại.
- Version selector hoặc stale review không có catalog error 409/422; không ánh xạ sang code chưa khai báo.
- Chưa xác định concealment policy khi Admin có quyền nhưng Content bị giới hạn scope.

## Error envelope discrepancy

- API guideline yêu cầu error data:null.
- Current error_response() dùng {} khi caller không truyền data.
- DESIGN_CONTRACT_PATHS hiện không có /api/v1/admin/content/{content_id}; route #79 chưa wired. Future request-validation/unhandled-error fallback có thể dùng VALIDATION_ERROR/INTERNAL_SERVER_ERROR, lệch catalog.
- Đây là discrepancy tích hợp có điều kiện, không phải runtime behavior endpoint #79.

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
