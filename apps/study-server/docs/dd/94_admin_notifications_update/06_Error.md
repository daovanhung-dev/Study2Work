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

| HTTP | Business code | Trigger | Status |
|---:|---|---|---|
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Missing, invalid or expired Bearer JWT | Direct catalog code; shared guard. |
| 403 | DESIGN_ACCESS_DENIED | Authenticated caller lacks ADMIN role | Direct catalog code; finer AC-36 permission remains unverified. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | No notification row for valid path ID | Direct code; lookup uses legacy candidate. |
| 422 | DESIGN_VALIDATION_ERROR | Invalid path/body; blank text; no delivery rows; any delivery is not QUEUED | Code is direct; precise body/state triggers are DERIVED fallback. |
| 500 | DESIGN_INTERNAL_ERROR | Query, projection or commit failure | Direct code; rollback and safe message implemented. |

## Error contract boundaries

- Preserve exactly the five catalog HTTP/business-code pairs; do not add 409/503 or scheduler errors.
- Shared ADMIN authentication/role errors are returned before path/body validation or DB query.
- 422 ineligible-state behavior is based on the candidate outbox; QUEUED is not treated as a Draft/Scheduled Notification enum.
- Fake-session tests verify error envelope and rollback path; live PostgreSQL constraints and deployment are unverified.
- Do not expose SQL, stack traces, recipient IDs, provider details, or queue internals.

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
