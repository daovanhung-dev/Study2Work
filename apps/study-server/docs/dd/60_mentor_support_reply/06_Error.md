---
title: "Error"
order: 6
dd_id: "60"
api_name: "Gửi phản hồi"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng error set API #60: 401, 403, 404, 422, 500. Không thêm 409, 503 hoặc 400 ngoài catalog.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Header thiếu hoặc token không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | No | Catalog; Mentor claim validation chưa có source. |
| 2 | Authorization | Role/scope | Mentor/request/asset scope | Sai role, request ngoài phạm vi hoặc file ref không được phép dùng | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | No | Request scope direct từ AC-24; attachment ownership branch cần confirm. |
| 3 | Not found | Request lookup | Support request | Không tìm thấy request theo ID và access rule được duyệt | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | No | Catalog; physical lookup chưa có. |
| 4 | Request validation | Required/type/content | `request_id`, `message`, `attachment refs` | Thiếu/sai kiểu; hoặc proposal message rỗng/whitespace; ref format invalid nếu CSV proposal được duyệt | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | No | Nonblank/CSV checks là DERIVED; không thêm length limit. |
| 5 | System error | DB/asset projection/response mapping | SupportMessage/SupportRequest | Lỗi query, insert hoặc mapping ngoài dự kiến | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md) | Yes, candidate transaction rollback trước commit | Catalog; không trả stack trace/provider detail. |

> Catalog không khai báo mã state-conflict HTTP 409; post-resolution reply behavior chưa chốt và không tự thêm 409. Nếu API owner muốn chặn reply trên request đã resolved/cancelled, status branch phải được ánh xạ bằng error contract đã duyệt.

> API Guidelines yêu cầu error `data:null`; current helper mặc định `{}` khi caller bỏ qua data. API #60 chưa wired nên đây là conditional future discrepancy.

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
