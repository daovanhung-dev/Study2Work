---
title: "Error"
order: 6
dd_id: "84"
api_name: "Cập nhật lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ nguyên error set và mã từ catalog #84. Request conditions cụ thể chưa được phê duyệt.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Credential thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | DIRECT business code; Study contract không có message ID riêng. |
| 2 | Authorization | Admin role/permission | Principal | Không có Admin role hoặc lesson-management permission | 403 | DESIGN_ACCESS_DENIED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | DIRECT requirement; policy implementation SOURCE_REQUIRED. |
| 3 | Not found | UPDATE RETURNING | lesson_id | Không có row lesson được cập nhật | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | [Step 4](./05_Data_Mapping.md#step-4-check-ket-qua-va-map-response) | Rollback nếu transaction bắt đầu | No-row -> 404 là candidate branch. |
| 4 | Validation | Request validation | Path/body candidate | Request sai schema/rules sau khi được duyệt | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 1](./05_Data_Mapping.md#step-1-nhan-request) / [Step 2](./05_Data_Mapping.md#step-2-check-body-proposal) | N/A trước mutation | Status/code DIRECT; exact fields/conditions SOURCE_REQUIRED. |
| 5 | System error | DB/update/response mapping | N/A | Database hoặc mapping failure không xử lý được | 500 | DESIGN_INTERNAL_ERROR | N/A | [Step 4](./05_Data_Mapping.md#step-4-check-ket-qua-va-map-response) | Rollback theo transaction owner | DIRECT business code; Study contract không có message ID riêng. |

## Error envelope

- API guidelines quy định top-level data:null; field-level details nằm trong meta.fieldErrors.
- Current error_response(...) chuyển absent data=None thành {}.
- API #84 chưa có route, nên chưa có endpoint runtime behavior.
- Không có business code mới cho API #84.

## Error response example — 404

```json
{
  "success": false,
  "businessCode": "DESIGN_RESOURCE_NOT_FOUND",
  "message": "Không tìm thấy lesson.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000084"
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
