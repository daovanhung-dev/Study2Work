---
title: "Error"
order: 6
dd_id: "73"
api_name: "Lấy danh sách khóa học Admin"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu, sai hoặc hết hạn | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; Admin auth chưa wired. |
| 2 | Authorization | Role/permission | Admin course-management | Principal không có role Admin/quyền quản lý course | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; policy SOURCE_REQUIRED. |
| 3 | Validation | Query parsing | status/mentor/category/page | Query value không parse được theo kiểu catalog | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | No | Code/status DIRECT; middleware path allowlist chưa có. |
| 4 | Validation | Page range | page | Page nhỏ hơn 1 theo proposal | 422 | DESIGN_VALIDATION_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-1-validate-data-input) | No | Status/code DIRECT; minimum DERIVED. |
| 5 | System error | Database query | Q1/Q2 | DB/query/count failure | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua) | Candidate rollback khi cần; read-only | DIRECT code/status; không trả raw DB details. |
| 6 | System error | Course mapping | Course fields | Price NULL/invalid hoặc required Course field không map được | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua) | Candidate rollback khi cần; read-only | Mapping integrity candidate theo API #06. |
| 7 | System error | Mentor integrity | `Course.mentor` | Không tìm thấy mentor tương ứng trong `users` | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-2-get-thong-tin) | Candidate rollback khi cần; read-only | Theo #06 precedent; Admin recovery behavior cần xác nhận. |

## Candidate branches — không thêm HTTP contract

| Điều kiện | Candidate behavior | Trạng thái |
|---|---|---|
| Không có course phù hợp | 200, `items=[]`, total=0 | DERIVED theo API #06 precedent; collection rỗng không phải 404. |
| Page vượt phạm vi | 200, items rỗng, giữ total và total_pages | DERIVED theo API #06 test/source. |
| Status lạ | Exact filter trả 0 row nếu không có giá trị đó | DERIVED; không tạo enum whitelist. |
| Category được gửi | Không có predicate vật lý được phép hiện tại | SOURCE_REQUIRED; không bỏ qua filter, cũng không tự reject valid filter. |
| Course không có mentor | Safe 500 theo API #06 precedent | DERIVED; Admin recovery policy cần owner xác nhận. |

## Error envelope và wiring gap

- `error_response(...)` hiện dùng `data={}` khi không truyền data; API guideline yêu cầu `data=null` cho lỗi.
- Middleware `DESIGN_CONTRACT_PATHS` chưa có `/api/v1/admin/courses`; nếu route tương lai dựa vào exception handler trước khi cập nhật allowlist, có thể trả `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`.
- Đây là gap integration hiện tại/conditional future behavior; API #73 chưa tồn tại nên không phải quan sát runtime endpoint.
- Không trả SQL, stack trace, email hoặc thông tin mentor ngoài UserSummary.

## Không thêm

- Không thêm 404 cho empty list.
- Không thêm 409, 503 hoặc business code mới.
- Không biến category relation gap thành “category chưa hỗ trợ” response khi contract chưa cho behavior đó.

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
