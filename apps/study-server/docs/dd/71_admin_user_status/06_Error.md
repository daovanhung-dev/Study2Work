---
title: "Error"
order: 6
dd_id: "71"
api_name: "Khóa/mở khóa user Conditional"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog và runtime fallback

| No | Category | Verify check | Item | Nội dung check | HTTP status | Error code | Rollback | Runtime mapping |
|---:|---|---|---|---|---:|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | Shared ADMIN guard. |
| 2 | Authorization | Admin role | Principal | Caller không có ADMIN claim | 403 | DESIGN_ACCESS_DENIED | N/A | Shared role guard trước DB. Dedicated permission policy chưa source-backed. |
| 3 | Not found | User lock/update | user_id | Không có user row | 404 | DESIGN_RESOURCE_NOT_FOUND | Read transaction rollback | Zero-row Q0 hoặc Q1. |
| 4 | Validation | Path/body/current state | Request | Path sai int64, body sai schema/status hoặc current state không lockable | 422 | DESIGN_VALIDATION_ERROR | Read transaction rollback nếu đã lock | Invalid current state ngoài ACTIVE/SUSPENDED là DERIVED. |
| 5 | System error | DB/mapping/transaction | Update pipeline | Lock/update/revoke/projection/commit thất bại | 500 | DESIGN_INTERNAL_ERROR | Rollback toàn bộ mutation | Không trả SQL/token details. |

Không thêm HTTP status hoặc business code ngoài catalog.

## Runtime branch details

- Invalid raw signed-int64 `user_id`, missing/null/extra/unsupported body field → 422. Middleware route template map framework body validation thành `DESIGN_VALIDATION_ERROR`.
- Existing user status ngoài ACTIVE/SUSPENDED → 422; endpoint không chuyển pending/deletion lifecycle states.
- Status update không tìm thấy row → 404.
- Khi SUSPENDED, revoke query chạy cùng transaction; lỗi revoke hoặc commit rollback status mutation và trả 500.
- Query/projection/rollback failures chỉ trả safe message; không echo stack, SQL, password hash, refresh-token hash hoặc token.
- `error_response(...)` trả `data:null`, có `meta.fieldErrors` cho lỗi validation và `X-Trace-Id`.

## Discrepancies and limits

- Catalog/diagram không định nghĩa body, enum members, malformed-path mapping hoặc transition matrix. Required `{status}`, ACTIVE/SUSPENDED allowlist, current-state gate và 422 fallback đều `DERIVED`.
- Diagram nói “revoke session nếu cần”; runtime chọn revoke refresh rows chưa revoke/chưa hết hạn khi khóa. Access JWT hiện hữu không bị vô hiệu tức thời.
- Live legacy schema, dedicated Admin permission, audit/PII rules và self/last-admin policy chưa xác minh.

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
