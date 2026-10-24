---
title: "Error"
order: 6
dd_id: "87"
api_name: "Lấy danh sách quiz"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các nhánh dưới đây giữ nguyên bộ lỗi API #87 trong catalog: 401, 403 và 500. Không thêm 404 hoặc 422. Điều kiện parse query lỗi và error-envelope integration cần được thống nhất trước khi wire route.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | SOURCE_REQUIRED | Authorization | Bearer token thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) | N/A | Code/status DIRECT; Admin guard chưa có. |
| 2 | Authorization | SOURCE_REQUIRED | Admin role/quiz-management permission | Principal không có role Admin hoặc permission | 403 | DESIGN_ACCESS_DENIED | N/A | [Step 0](./05_Data_Mapping.md#step-0-authentication-and-authorization) | N/A | Role DIRECT; AC-35 permission DIRECT; policy source chưa có. |
| 3 | System error | SOURCE_REQUIRED | Quiz/question query or mapping | DB/query hoặc required response mapping lỗi | 500 | DESIGN_INTERNAL_ERROR | N/A | [Step 5](./05_Data_Mapping.md#step-5-return-success-or-error) | N/A | Candidate data/schema; không lộ lỗi nội bộ. |

> Error message ID không có trong Study API contract; ghi N/A, không dùng mã từ template Excel.

## Query validation cases — contract chưa quy định

| Item | Condition | HTTP status | Business code | Status |
|---|---|---:|---|---|
| course | Query không parse được int64 | Chưa xác định | Catalog không khai báo | SOURCE_REQUIRED |
| page | Query không parse được int32 hoặc nhỏ hơn 1 theo proposal | Chưa xác định | Catalog không khai báo 400/422 | SOURCE_REQUIRED / DERIVED rule |
| status | Giá trị ngoài enum nếu enum được bổ sung | Chưa xác định | Catalog không khai báo 422 | SOURCE_REQUIRED |

Không tự gán HTTP 400/422 cho các nhánh trên.

## Error envelope

API Guidelines quy định data=null khi lỗi:

~~~json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Không thể truy vấn quiz.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-4000-8000-000000000089"
}
~~~

Current error_response thay data=None bằng {}. API #87 chưa có route; mismatch hiện tại là integration discrepancy phải xử lý khi wire endpoint.
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
