---
title: "Error"
order: 6
dd_id: "93"
api_name: "Tạo/phát notification"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

<a id="error-401"></a>

## Error cases

| No | Category | Verify check | Item/field | Condition | HTTP status | Business/Error code | Message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer JWT | Authorization | Missing/invalid token or failed auth | 401 | DESIGN_AUTHENTICATION_REQUIRED | Runtime envelope | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-permission) | N/A | Shared guard; checked before body and DB |
| 2 | Authorization | Role | Principal | Role is not `ADMIN` | 403 | DESIGN_ACCESS_DENIED | Runtime envelope | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-permission) | N/A | Fine-grained notification permission is not implemented |
| 3 | Validation | JSON/body schema | Body fields | Invalid JSON/type or unknown field | 422 | DESIGN_VALIDATION_ERROR | Runtime envelope | [Step 1](./05_Data_Mapping.md#step-1-read-request) | No writes have started | Direct error code; field predicates are DERIVED |
| 4 | Validation | Audience | recipients / segment | Missing, null, empty, non-positive, out-of-int64, duplicate recipient ID; segment supplied; one or more users missing | 422 | DESIGN_VALIDATION_ERROR | Runtime envelope | [Step 2](./05_Data_Mapping.md#step-2-resolve-audience) | Roll back if transaction was opened | Explicit recipient fallback; no missing ID is disclosed |
| 5 | Validation | Notification text | title / content | Blank title/content or title exceeds 200 characters | 422 | DESIGN_VALIDATION_ERROR | Runtime envelope | [Step 1](./05_Data_Mapping.md#step-1-read-request) | No notification writes | Title limit is from local DDL candidate |
| 6 | Validation | Delivery channels | channels | Empty, duplicate, or value other than `PUSH`/`EMAIL` | 422 | DESIGN_VALIDATION_ERROR | Runtime envelope | [Step 1](./05_Data_Mapping.md#step-1-read-request) | No notification writes | Channel values are DERIVED fallback |
| 7 | Dependency | DB acceptance dependency | Recipient/read/write/commit | SQL OperationalError or invalidated DB connection | 503 | DESIGN_DEPENDENCY_UNAVAILABLE | Runtime envelope | [Step 4](./05_Data_Mapping.md#step-4-accept-and-dispatch) | Attempt rollback after transaction begins | DB mapping is DERIVED; no live dependency was exercised |
| 8 | System | Persistence/projection | Insert/response/commit | Other SQLAlchemy error or invalid returned projection | 500 | DESIGN_INTERNAL_ERROR | Runtime envelope | [Step 3](./05_Data_Mapping.md#step-3-create-notification-and-delivery-rows) | Attempt rollback after transaction begins | Raw internals are not returned |

## Error contract boundaries

- Runtime uses only catalog statuses/codes: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 503 `DESIGN_DEPENDENCY_UNAVAILABLE`, and 500 `DESIGN_INTERNAL_ERROR`.
- Validation predicates and database failure classification are DERIVED implementation choices pending owner confirmation.
- The view rolls back failures during recipient lookup, notification insert, delivery insert, response mapping, and commit. Rollback failure is logged with trace ID and does not replace the response.
- No live database, deployment, or provider failure branch was verified.
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
