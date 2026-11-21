---
title: "Error"
order: 6
dd_id: "74"
api_name: "Lấy chi tiết course quản trị"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Catalog #74 chỉ cho phép các business code dưới đây. Không thêm 422/409 hoặc code khác. Mapping role/path/DB hiện là local implementation; live deployment chưa xác minh.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Shared Bearer/JWT guard | `Authorization` | Header thiếu, token sai/hết hạn hoặc principal không hợp lệ | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-0-check-quyen](./05_Data_Mapping.md#step-0-check-quyen) | No | Catalog + shared guard; local source/test. |
| 2 | Authorization | Shared role guard | Principal | Principal không có role `ADMIN` | `403` | `DESIGN_ACCESS_DENIED` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-0-check-quyen](./05_Data_Mapping.md#step-0-check-quyen) | No | Shared `ADMIN` guard is implemented; dedicated course-management permission remains SOURCE_REQUIRED. |
| 3 | Not found | Signed-int64 parse / Q1 result | `course_id` | ID malformed/outside int64 hoặc Q1 không tìm thấy course | `404` | `DESIGN_RESOURCE_NOT_FOUND` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-1-validate-data-input](./05_Data_Mapping.md#step-1-validate-data-input) / [#step-2-get-thong-tin](./05_Data_Mapping.md#step-2-get-thong-tin) | No | Fallback `DERIVED`, covered by focused tests; no `PUBLISHED` filter. |
| 4 | System/data integrity | Query/mapping | Course/UserSummary | DB error, thiếu required price hoặc mentor projection không đầy đủ | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — Catalog không định nghĩa message ID riêng.` | [05_Data_Mapping.md#step-4-check-ket-qua-query](./05_Data_Mapping.md#step-4-check-ket-qua-query) | Rollback on missing row or query/projection failure; read path never commits | Safe message; orphan mentor behavior là candidate cần xác nhận. |

> Current `error_response` serializes omitted error data as `null`; this is local source behavior, with deployment unverified.
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
