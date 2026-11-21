---
title: "Error"
order: 6
dd_id: "82"
api_name: "Lấy danh sách lesson"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---
# Error

## Giải thích

Các lỗi authentication/authorization/system giữ mã catalog API #82. Local implementation bổ sung 422 `DESIGN_VALIDATION_ERROR` làm fallback DERIVED cho input không parse được hoặc filter `type` chưa có source mapping; do đó DD vẫn Draft.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error Message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | VERIFIED by local HTTP tests | Authorization | Bearer token thiếu, sai hoặc hết hạn | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A | [Step 0](./05_Data_Mapping.md#0-check-quyen) | N/A | Code/status DIRECT; shared guard. |
| 2 | Authorization | VERIFIED by local HTTP tests | Admin role | Principal không có role `ADMIN` | 403 | `DESIGN_ACCESS_DENIED` | N/A | [Step 0](./05_Data_Mapping.md#0-check-quyen) | N/A | Role DIRECT; fine-grained lesson permission chưa có check. |
| 3 | Validation | DERIVED/local behavior | Query `course` | Không parse được signed int64 hoặc vượt range | 422 | `DESIGN_VALIDATION_ERROR` | N/A | [Step 1](./05_Data_Mapping.md#1-validate-data-input) | N/A | `meta.fieldErrors`: field `course`, code `INT_PARSING`; DB chưa được gọi. |
| 4 | Validation | DERIVED/local behavior | Query `type` | Client gửi type khi không có Lesson type mapping | 422 | `DESIGN_VALIDATION_ERROR` | N/A | [Step 1](./05_Data_Mapping.md#1-validate-data-input) | N/A | `meta.fieldErrors`: field `type`, code `UNSUPPORTED_FILTER`; không âm thầm bỏ filter. |
| 5 | System error | VERIFIED by local HTTP tests | Lesson query/mapping | DB query lỗi hoặc projection không map được reusable Lesson | 500 | `DESIGN_INTERNAL_ERROR` | N/A | [Step 3](./05_Data_Mapping.md#3-check-ket-qua-execute-query) | Best-effort | Legacy nullable required fields nếu NULL làm mapping thất bại. |

> Error message ID không có trong Study API contract; dùng `N/A`, không sao chép mã từ template Excel.

## Error envelope

~~~json
{
  "success": false,
  "businessCode": "DESIGN_VALIDATION_ERROR",
  "message": "Dữ liệu đầu vào không hợp lệ.",
  "data": null,
  "meta": {
    "fieldErrors": [
      {
        "field": "type",
        "code": "UNSUPPORTED_FILTER",
        "message": "Lesson type filter is not supported by the available schema."
      }
    ]
  },
  "traceId": "00000000-0000-0000-0000-000000000003"
}
~~~

`error_response(...)` trả `data: null`; validation error giữ field error trong `meta.fieldErrors`. Query/projection 500 rollback best-effort. Local HTTP tests không xác minh live DB/schema.

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
