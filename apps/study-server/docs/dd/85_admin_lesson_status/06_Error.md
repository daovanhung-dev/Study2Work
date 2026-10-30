---
title: "Error"
order: 6
dd_id: "85"
api_name: "Đổi trạng thái lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ nguyên error set/catalog code của API #85. Body/status enum, legacy audit table và atomicity là fallback DERIVED; live schema và fine-grained lesson-management permission chưa xác minh.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Credential thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Shared ADMIN auth. |
| 2 | Authorization | Role check | Principal | Không có role ADMIN | 403 | DESIGN_ACCESS_DENIED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | AC-34 fine-grained lesson permission remains unsupported. |
| 3 | Not found | SELECT FOR UPDATE | lesson_id | Không có row lesson khớp ID | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | [Step 3](./05_Data_Mapping.md#step-3-update-audit) | Rollback read transaction | Soft-delete visibility remains linked to #86. |
| 4 | Validation | FastAPI/Pydantic and path parser | Path/body | Invalid int64, missing/extra/wrong field, or status outside DERIVED enum | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) / [Step 2](./05_Data_Mapping.md#step-2-check-status-proposal) | Before mutation | Catalog status/code; exact conditions follow local DERIVED model. |
| 5 | System error | DB/lock/update/audit/mapping/commit | N/A | Query, audit insert, response mapping or commit fails | 500 | DESIGN_INTERNAL_ERROR | N/A | [Step 3](./05_Data_Mapping.md#step-3-update-audit) / [Step 4](./05_Data_Mapping.md#step-4-check-ket-qua-va-map-response) | Roll back transaction | Audit update and status change share one Session transaction. |

## Error envelope

- Current `error_response(...)` returns top-level `data: null`; field details use `meta.fieldErrors`.
- Focused HTTP tests verify 401/403/404/422/500 envelopes and safe messages.
- Local fake DB tests do not verify live database behavior or migration deployment.
- Không thêm business code hoặc HTTP status ngoài tập catalog #85.

## Error response example — 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Lesson not found.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000085"
}
```
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
