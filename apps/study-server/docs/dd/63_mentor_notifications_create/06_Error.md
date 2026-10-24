---
title: "Error"
order: 6
dd_id: "63"
api_name: "Tạo và phát thông báo"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng catalog error set API #63: 401, 403, 422, 503, 500. Không thêm 404, 409 hoặc mã nghiệp vụ mới. Các nhánh về course/recipient là khuyến nghị DERIVED và chỉ thực hiện sau khi contract được sửa.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu hoặc không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-auth) | No | Mentor guard chưa wired. |
| 2 | Authorization | Role/scope | Mentor/course/recipient | Sai role hoặc Mentor không có quyền với course/recipient | 403 | `DESIGN_ACCESS_DENIED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-2-recipient-scope) | No | Course ID vắng trong direct body; scope branch chưa thể hoàn thiện. |
| 3 | Validation | Required/type/encoding | Request body | Thiếu field, sai kiểu hoặc encoding không hợp lệ sau khi được duyệt | 422 | `DESIGN_VALIDATION_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-request) | Rollback logical writes | Không tự thêm length/enum/batch limit. |
| 4 | Dependency | Queue/provider | Operation dispatch | Queue/provider không thể nhận yêu cầu trước khi API chấp nhận | 503 | `DESIGN_DEPENDENCY_UNAVAILABLE` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-operation-queue) | Rollback chưa chốt | Sau 202, lỗi delivery thuộc status lifecycle; không đổi response đã trả. |
| 5 | System error | Persistence/runtime | Notification/recipient/Operation | Lỗi nội bộ ngoài dự kiến khi lưu hoặc dựng response | 500 | `DESIGN_INTERNAL_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-6-response-errors) | Theo transaction được duyệt | Không trả SQL, provider detail hoặc stack trace. |

> Error envelope theo API Guidelines dùng `data:null`; current helper mặc định `{}`. Route #63 chưa wired nên chưa có behavior runtime.
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
