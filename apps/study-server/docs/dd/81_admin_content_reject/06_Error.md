---
title: "Error"
order: 6
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các lỗi dưới đây giữ đúng HTTP status/business code catalog #81. State eligibility/path parsing are local DERIVED triggers because the catalog lists 422 but does not enumerate its conditions.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | DIRECT | Authorization | Bearer thiếu, sai chữ ký hoặc token không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Shared guard runs before path/DB. |
| 2 | Authorization | DIRECT role / DERIVED guard | Admin role/access | Role `ADMIN` không đạt | 403 | DESIGN_ACCESS_DENIED | N/A | [Step 0](./05_Data_Mapping.md#step-0-check-quyen) | N/A | Dedicated moderation permission remains unverified. |
| 3 | Path validation | DERIVED | content_id | Path không phải signed-int64 hoặc vượt miền | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 1](./05_Data_Mapping.md#step-1-validate) | N/A | No DB access. |
| 4 | Request validation | DIRECT required field | Body.reason | Body thiếu/sai schema, thiếu reason, non-string or extra field | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 1](./05_Data_Mapping.md#step-1-validate) | N/A | Blank, length and format rules are not imposed. |
| 5 | Resource lookup | DIRECT error set | content_id | Không có Content active; missing/deleted row | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | [Step 2](./05_Data_Mapping.md#step-2-get-thong-tin) | Yes | Transaction is rolled back after lock lookup. |
| 6 | Review eligibility | DERIVED | `contents.status` | Current state khác `PENDING_REVIEW` | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 2](./05_Data_Mapping.md#step-2-get-thong-tin) | Yes | No status or decision row is written. |
| 7 | System error | DIRECT error set | Status/reason transaction | Lock/update/decision insert/projection/commit fails | 500 | DESIGN_INTERNAL_ERROR | N/A | [Step 4](./05_Data_Mapping.md#step-4-result) | Yes | Roll back and do not expose raw DB/stack details. |

> Error message ID không có trong Study API contract; dùng N/A, không sao chép mã từ template Excel.

## Error envelope

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000000"
}
~~~

`error_response()` hiện mặc định `data:null`. Route #81 nằm trong `DESIGN_CONTRACT_PATHS`, nên framework request-validation và unhandled errors dùng DESIGN business codes.
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
