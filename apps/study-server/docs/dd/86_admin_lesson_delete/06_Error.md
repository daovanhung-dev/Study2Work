---
title: "Error"
order: 6
dd_id: "86"
api_name: "Xóa lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ nguyên error set và mã từ catalog #86. Dependency-blocker behavior là proposal; không bổ sung business code hoặc HTTP status.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Credential thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | DIRECT code; message ID không được catalog cung cấp. |
| 2 | Authorization | Admin role/permission | Principal | Không có Admin role hoặc lesson-management permission | 403 | DESIGN_ACCESS_DENIED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | DIRECT requirement; policy source absent. |
| 3 | Not found | Q1 target lookup | lesson_id | Không có lesson khớp path ID | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | [Step 2](./05_Data_Mapping.md#step-2-tim-lesson) | N/A | No-row → 404 là candidate semantics. |
| 4 | Validation/policy | Path/dependency check | lesson_id/reference/progress | Path invalid theo parser được duyệt hoặc dependency policy chặn soft-delete | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) / [Step 3](./05_Data_Mapping.md#step-3-check-dependency-va-policy) | N/A trước mutation | Catalog code DIRECT; dependency branch DERIVED. |
| 5 | System error | Query/persistence/mapping/commit | N/A | Database hoặc response mapping failure không xử lý được | 500 | DESIGN_INTERNAL_ERROR | N/A | [Step 4](./05_Data_Mapping.md#step-4-soft-delete-theo-policy) / [Step 5](./05_Data_Mapping.md#step-5-map-deleteresult) | Rollback theo approved transaction | DIRECT code; transaction owner unresolved. |

## Error envelope

- API guideline yêu cầu error data:null; field detail nằm trong meta.fieldErrors.
- Current error_response(...) đổi absent data thành {}; endpoint #86 chưa có route để chứng minh behavior riêng.
- Không thêm 409 hoặc code khác ngoài error set catalog #86.

## Error response example — dependency blocker 422 — DERIVED

```json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Không thể xóa lesson do policy dependency.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000086"
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
