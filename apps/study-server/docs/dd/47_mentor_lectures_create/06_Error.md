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

Bộ lỗi giữ đúng catalog API #47. Các điều kiện quyền và candidate mapping được đánh dấu DERIVED; API #47 hiện chưa có handler runtime.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Thiếu, sai định dạng hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | 0 | N/A | Catalog direct; Mentor guard chưa có trong current Study source. |
| 2 | Authorization | Role | roles | Principal không có role Mentor | 403 | DESIGN_ACCESS_DENIED | N/A | 0 | N/A | Catalog direct. |
| 3 | Authorization | Course access | course_id | Course tồn tại nhưng Mentor không có quyền theo candidate direct-owner rule | 403 | DESIGN_ACCESS_DENIED | N/A | 0.3 | N/A | DERIVED; assignment access chưa có source. |
| 4 | Not found | Course lookup | course_id | Không có course theo path ID | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | 2.1 | N/A | Catalog direct; candidate legacy lookup. |
| 5 | Validation | Required/type/length | title | Thiếu/sai string hoặc vượt 200 theo legacy candidate | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Max 200 là DERIVED; không tự đặt min. |
| 6 | Validation | Required/type | content | Thiếu hoặc không parse thành int64 | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Catalog direct types. |
| 7 | Validation | Required/type | asset refs | Thiếu hoặc không phải string | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Không định nghĩa lỗi format cho chuỗi refs chưa có schema. |
| 8 | Validation | Required/type | order | Thiếu hoặc không parse thành int32 | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Không thêm rule không âm. |
| 9 | Validation | Path type | course_id | Không parse thành int64 | 422 | DESIGN_VALIDATION_ERROR | N/A | 1 | N/A | Error branch là DERIVED từ catalog 422. |
| 10 | System error | DB/transaction | M1 | Lỗi truy vấn hoặc INSERT không xử lý được | 500 | DESIGN_INTERNAL_ERROR | N/A | 3–4 | Yes | Catalog direct; rollback candidate. |

> Không thêm 409 hoặc 503: catalog API #47 không khai báo các status này. API #34 chịu trách nhiệm storage failure trước khi #47 được gọi.
>
> API guidelines đặt data:null ở error envelope; current error_response() mặc định {} khi không truyền data. API #47 chưa chạy nên không có current API response để đối chiếu.

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
