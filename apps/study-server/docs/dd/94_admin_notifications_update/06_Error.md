---
title: "Error"
order: 6
dd_id: "94"
api_name: "Admin cập nhật notification"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases

| No | HTTP | Business code | Direct trigger/source | Handling/status |
|---:|---:|---|---|---|
| 1 | 401 | DESIGN_AUTHENTICATION_REQUIRED | Missing, invalid or expired Bearer JWT per catalog code | Direct code; token validation source is shared auth policy |
| 2 | 403 | DESIGN_ACCESS_DENIED | Authenticated caller lacks Admin/notification-management access | Admin permission requirement is direct in catalog/AC-36; claim and policy mapping SOURCE_REQUIRED |
| 3 | 404 | DESIGN_RESOURCE_NOT_FOUND | Target notification does not exist | Direct error code; lookup model and precedence vs permission SOURCE_REQUIRED |
| 4 | 422 | DESIGN_VALIDATION_ERROR | Catalog lists code; body field triggers are unspecified | Direct code; body validation and proposed ineligible-state handling are DERIVED, need owner approval |
| 5 | 500 | DESIGN_INTERNAL_ERROR | Unexpected internal failure | Direct code; transaction rollback, logging and safe message source SOURCE_REQUIRED |

## Error contract boundaries

- Preserve the exact five catalog error codes and HTTP statuses; do not invent 409, 503 or a scheduler error.
- Request body is absent from the direct catalog. A malformed proposal body maps to 422 only if the body proposal is approved and the shared contract confirms framework behavior.
- Draft/Scheduled eligibility is not defined as a direct condition. A 422 for already-dispatched/cancelled resources is only a DERIVED proposal.
- Error envelope data nullability follows API Guidelines/current helper boundary; this DD does not change shared serialization.
- Do not expose recipient IDs, provider details, SQL or stack traces.

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
