---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Bộ lỗi giữ đúng catalog API #47. Route source-backed trả lỗi asset thiếu hoặc ngoài owner/purpose/course scope bằng cùng một 404 `DESIGN_RESOURCE_NOT_FOUND`.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Thiếu, sai định dạng hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | 0 | N/A | Catalog direct. |
| 2 | Authorization | Role | roles | Principal không có role Mentor | 403 | DESIGN_ACCESS_DENIED | N/A | 0 | N/A | Catalog direct. |
| 3 | Authorization | Course access | course_id | `courses.mentor_id` không bằng Mentor hiện tại | 403 | DESIGN_ACCESS_DENIED | N/A | 0.3 | Yes | Chỉ direct owner; mọi course status được nhận. |
| 4 | Not found | Course lookup | course_id | Course không tồn tại | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | 2.1 | Yes | Direct query result. |
| 5 | Not found | Asset resolution | asset_refs | Ít nhất một ID không resolve trong cùng Mentor, purpose LECTURE và course_id | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | 2.2 | Yes | Cùng response cho ID thiếu và ngoài scope. |
| 6 | Validation | Required/type/length | title | Thiếu/sai string hoặc dài hơn 200 ký tự | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Max 200 theo legacy `lessons.name VARCHAR(200)`. |
| 7 | Validation | Required/type/range | content | Thiếu, sai kiểu hoặc ngoài signed int64 | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Lưu/response bằng chuỗi thập phân. |
| 8 | Validation | JSON/array/int64/duplicates | asset_refs | JSON sai, không phải array, ID sai kiểu/ngoài int64 hoặc bị trùng | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Empty array is valid. |
| 9 | Validation | Required/type/range | order | Thiếu, sai kiểu hoặc ngoài signed int32 | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Không thêm rule không âm. |
| 10 | Validation | Path type/range | course_id | Không parse được hoặc ngoài signed int64 | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Path validation trước query. |
| 11 | System error | DB/transaction | Q1/Q2/M1 | Query, INSERT hoặc commit phát sinh SQLAlchemy error | 500 | DESIGN_INTERNAL_ERROR | N/A | 2–4 | Yes | Rollback; chi tiết DB không trả về client. |

> Không thêm 409 hoặc 503: catalog API #47 không khai báo các status này. API #34 chịu trách nhiệm storage upload trước đó.
>
> Với ID không tồn tại hoặc không thuộc cùng Mentor/purpose/course, resolver không trả metadata và dùng cùng 404 response.

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
