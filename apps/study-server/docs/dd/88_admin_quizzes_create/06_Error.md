---
title: "Error"
order: 6
dd_id: "88"
api_name: "Tạo quiz mới"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng error set API #88: 401, 403, 422, 500. Embedded JSON structure là proposal DERIVED; không thêm 404/409.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | SOURCE_REQUIRED | Authorization | Bearer token thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) | Không mở transaction | Code/status DIRECT; Admin guard chưa có. |
| 2 | Authorization | SOURCE_REQUIRED | Admin role/permission | Principal không có Admin role hoặc quiz-management permission | 403 | DESIGN_ACCESS_DENIED | N/A | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) | Không mở transaction | Role catalog DIRECT; policy chưa có source. |
| 3 | Validation | DERIVED | config/questions | Outer field thiếu/sai type; embedded JSON sai cú pháp/shape sau khi proposal được duyệt | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 1](./05_Data_Mapping.md#step-1-validate-and-parse-body) | Không có write | HTTP/code DIRECT; inner rules DERIVED. |
| 4 | Validation | DERIVED | config.course_id | Course không tồn tại theo candidate Q0 | 422 | DESIGN_VALIDATION_ERROR | N/A | [Step 2](./05_Data_Mapping.md#step-2-validate-course-reference) | Không có write | DERIVED vì catalog không có 404. |
| 5 | System error | SOURCE_REQUIRED | Parent/child insert or commit | DB/ID retrieval/response mapping/commit lỗi | 500 | DESIGN_INTERNAL_ERROR | N/A | [Step 3](./05_Data_Mapping.md#step-3-insert-quiz-parent) | Rollback cả transaction | Không lộ lỗi nội bộ. |

Error message ID không có trong Study API contract; ghi N/A, không dùng mã từ template Excel.

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
        "field": "questions",
        "code": "INVALID_JSON",
        "message": "questions phải chứa JSON hợp lệ."
      }
    ]
  },
  "traceId": "00000000-0000-4000-8000-000000000088"
}
~~~

API Guidelines quy định data=null và fieldErrors trong meta. Current helper serialize data=None thành {}; middleware chỉ phát DESIGN_VALIDATION_ERROR khi path thuộc allowlist. API #88 hiện chưa có route.
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
