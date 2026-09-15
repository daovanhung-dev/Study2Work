---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API #10 theo contract API V1. API chỉ khai báo `404 DESIGN_RESOURCE_NOT_FOUND` và `500 DESIGN_INTERNAL_ERROR`; không tự thêm `422` cho query malformed.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Not found | `Yes` | `course_id` | Path không parse được `int64`, hoặc Q1 không có course với `c.id = course_id AND c.status = 'PUBLISHED'` | `404` | `DESIGN_RESOURCE_NOT_FOUND` | `N/A — envelope message` | [`2.3`](./05_Data_Mapping.md#23-validate-course_id) / [`3.2`](./05_Data_Mapping.md#32-check-result) / [`6.2`](./05_Data_Mapping.md#62-not-found) | `No` | Không expose course draft/private |
| 2 | System error | `No` | `courses/discussions/users` | Lỗi Q1/Q2/Q3/Q4, lỗi join hoặc lỗi map `Page<Discussion>` | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`4.4`](./05_Data_Mapping.md#44-check-result) / [`6.3`](./05_Data_Mapping.md#63-system-error) | `No` | Không trả raw SQL, stack trace hoặc storage detail |

> Mỗi error case và mỗi field validation phải nằm trên một row riêng.

> `page` và `rating` malformed chưa có HTTP/business code tương ứng trong contract; giữ `TBD` trong Data Mapping, không tự tạo nhánh lỗi mới.

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
