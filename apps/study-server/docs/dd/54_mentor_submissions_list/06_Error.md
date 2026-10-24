---
title: "Error"
order: 6
dd_id: "54"
api_name: "Lấy submissions"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Bộ lỗi giữ nguyên chính xác theo API catalog #54. Điều kiện của 409 và cách xử lý input sai kiểu chưa được AC-23 định nghĩa.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Authorization | Bearer token thiếu, sai định dạng hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | SOURCE_REQUIRED | 0.1 | No | Current API #54 route/guard absent. |
| 2 | Authorization | Yes | Mentor course access | Actor không phải Mentor hoặc không có quyền chấm course | 403 | DESIGN_ACCESS_DENIED | SOURCE_REQUIRED | 0.3 | No | Role DIRECT; exact identity/assignment predicate SOURCE_REQUIRED. |
| 3 | State conflict | SOURCE_REQUIRED | SOURCE_REQUIRED | Catalog khai báo 409 nhưng AC-23 không nêu điều kiện trigger | 409 | DESIGN_STATE_CONFLICT | SOURCE_REQUIRED | 4.2 | No | Do not derive from empty results, status filter or page. |
| 4 | System error | Yes | Query/data mapping | Database, asset lookup or response mapping fails | 500 | DESIGN_INTERNAL_ERROR | SOURCE_REQUIRED | 4.3 | No | Safe message only; exact message text unspecified. |

## Input validation and empty result

- Catalog #54 does not include 422 DESIGN_VALIDATION_ERROR; malformed/overflow query handling is not defined.
- Catalog #54 does not include 404; missing course or no matching submissions must not be mapped to 404 without a contract update.
- Empty list/singular data behavior is unresolved because the endpoint is plural but response type is singular.
- No error branch performs rollback because API #54 is read-only.

> Error message IDs are SOURCE_REQUIRED; the catalog defines business codes and HTTP statuses, not separate message identifiers.

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
