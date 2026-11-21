---
title: "Error"
order: 6
dd_id: "34"
api_name: "Upload file"
source_sheet: "4.Error"
status: "Draft — Ready for Review"
---

# Error

## Giải thích

API #34 chỉ dùng status/business-code trong catalog. Error response không đưa raw exception hoặc thông tin cấu hình storage ra client.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Required | Authorization | Bearer thiếu, sai format, token invalid hoặc expired. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#0-check-quyền) | N/A | Shared auth helper. |
| 2 | Authorization | Required | Role/purpose | Role không thuộc Student/Mentor hoặc Student dùng LECTURE/Mentor dùng SUBMISSION. | 403 | DESIGN_ACCESS_DENIED | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#0-check-quyền) | N/A | Chặn trước DB/storage. |
| 3 | Authorization | Conditional | course_id | Student không có enrollment ACTIVE hoặc Mentor không phải direct owner theo courses.mentor_id. | 403 | DESIGN_ACCESS_DENIED | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#2-permission-queries) | Rollback read transaction | Không thêm 404 theo error set #34. |
| 4 | Validation | Required/type | file | Thiếu binary part hoặc multipart không parse được. | 422 | DESIGN_VALIDATION_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#1-validate-request) | N/A | Không đặt MIME/size allowlist. |
| 5 | Validation | Required/enum | purpose | Thiếu purpose hoặc giá trị không phải SUBMISSION/LECTURE. | 422 | DESIGN_VALIDATION_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#1-validate-request) | N/A | Valid purpose nhưng role không tương ứng là 403. |
| 6 | Validation | Conditional | course_id | Không parse được int64, ngoài signed int64 range, hoặc thiếu với LECTURE. | 422 | DESIGN_VALIDATION_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#1-validate-request) | N/A | Không thêm positive-only rule. |
| 7 | Dependency unavailable | Conditional | Object Storage | Cấu hình thiếu/không hợp lệ hoặc S3 upload thất bại. | 503 | DESIGN_DEPENDENCY_UNAVAILABLE | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#3-object-storage-mutation) | Rollback; best-effort delete UUID key | Cleanup lỗi không đổi response 503. |
| 8 | System error | Conditional | Database metadata | Query scope, INSERT, commit hoặc metadata mapping gặp lỗi. | 500 | DESIGN_INTERNAL_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md#4-metadata-mutation) | Rollback; best-effort delete nếu object đã upload | Raw DB/provider details không trả client. |

- Error envelope dùng `data: null`; `meta.fieldErrors` chứa lỗi field khi framework cung cấp validation details.
- Migration là source artifact; lỗi live database không chứng minh migration đã deploy.

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
