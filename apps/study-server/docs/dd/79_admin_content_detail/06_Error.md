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

- API #79 hiện wire tại `GET /api/v1/admin/content/{content_id}` và dùng shared ADMIN guard.
- Giữ đúng HTTP 401/403/404/500 và business codes API catalog #79.
- 404 áp dụng cho malformed/out-of-range int64 path theo fallback #69 và cho ID không có active row; malformed-path mapping là DERIVED.
- Query, projection hoặc payload-shape failure trả safe 500, không lộ chi tiết DB.
- Catalog không khai báo 409/422; không thêm code/status cho stale queue item, revision conflict hoặc path parse.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No query | Direct catalog; guard runs before path parse/DB. |
| 2 | Authorization | Admin role | Principal role | Principal hợp lệ nhưng không có role Admin | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No query | Direct catalog; shared ADMIN guard. |
| 3 | Resource not found | Parse/Content lookup | content_id | Malformed/out-of-range ID, no row, or soft-deleted row | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | Only if lookup started | Missing/deleted is derived; signed-int64 path fallback follows #69. |
| 4 | System error | Query/map response | Current Content projection | SQL, row identity, or Content payload projection fails | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-2-get-thong-tin) | Rollback | Safe error envelope; no raw database details. |

## Unresolved review-state behavior

- #78 queue filters `PENDING_REVIEW`; #79 returns current row status without re-filtering.
- Diagram does not define behavior if status changes between queue and detail. Catalog has no conflict code.
- Version selector or stale review has no catalog error 409/422; do not invent one.
- Moderation-specific permission and Content scope/concealment policy are not defined beyond shared ADMIN role.

## Error envelope

- Current `error_response()` default error `data` is JSON `null`, aligned with API guidelines.
- `/api/v1/admin/content/{content_id}` is registered in `DESIGN_CONTRACT_PATHS`, so shared contract middleware recognizes the dynamic route.
- Endpoint responses use the catalog business codes; generic framework fallback behavior remains governed by shared middleware.

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
