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

Các nhánh lỗi dưới đây giữ đúng danh sách API #82 trong catalog. Không thêm 404, 422 hoặc business code khác. Điều kiện malformed query và error envelope cần owner/source xác nhận trước khi wire route.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | SOURCE_REQUIRED | Authorization | Bearer token thiếu, sai hoặc hết hạn | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A | [Step 0](./05_Data_Mapping.md#0-check-quyen) | N/A | Code/status DIRECT; guard hiện chưa có. |
| 2 | Authorization | SOURCE_REQUIRED | Admin role/lesson permission | Principal không có Admin role hoặc permission | 403 | `DESIGN_ACCESS_DENIED` | N/A | [Step 0](./05_Data_Mapping.md#0-check-quyen) | N/A | Role DIRECT; permission theo AC-34; policy source chưa có. |
| 3 | System error | SOURCE_REQUIRED | Lesson query/mapping | DB query hoặc required field mapping lỗi | 500 | `DESIGN_INTERNAL_ERROR` | N/A | [Step 3](./05_Data_Mapping.md#3-check-ket-qua-execute-query) | N/A | Candidate legacy `course_id=NULL` cũng không map được required field; behavior cần chốt. |
| 4 | Contract integration | SOURCE_REQUIRED | Query validation | `course` không parse được int64 hoặc query schema invalid | Chưa xác định | Chưa có trong catalog | N/A | [Step 1](./05_Data_Mapping.md#1-validate-data-input) | N/A | Không tự gán 400/422; direct error set chỉ có 401/403/500. |
| 5 | Contract integration | SOURCE_REQUIRED | Query `type` | Client gửi `type` nhưng không có Lesson field/predicate nguồn | Chưa xác định | Chưa có trong catalog | N/A | [Step 1](./05_Data_Mapping.md#1-validate-data-input) | N/A | Không bỏ qua filter; cần schema/contract resolution. |

> Error message ID không có trong Study API contract; dùng `N/A`, không sao chép mã từ template Excel.

## Error envelope

API guideline shape:

~~~json
{
  "success": false,
  "businessCode": "DESIGN_INTERNAL_ERROR",
  "message": "Không thể xử lý yêu cầu.",
  "data": null,
  "meta": {},
  "traceId": "00000000-0000-0000-0000-000000000003"
}
~~~

Current helper mặc định `data={}` nếu caller không truyền data; current middleware path chưa allowlist `/api/v1/admin/lessons`. API #82 chưa có route nên chưa có runtime error behavior để xác nhận. Xem [conflicts](./02_Overview.md#conflicts).

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
