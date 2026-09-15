---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API #6 theo `list_api.md`. Danh sách rỗng là kết quả thành công `200`; không tạo `404`.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Validation error | `Yes` | `category` | Query `category` không parse được thành `int64` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`1.1`](./05_Data_Mapping.md#11-validate-category) | `No` | Category relation vẫn TBD; không tạo JOIN giả |
| 2 | Validation error | `Yes` | `page` | Query `page` không parse được thành `int32` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`1.2`](./05_Data_Mapping.md#12-validate-page) | `No` | Range/default chưa được contract xác nhận |
| 3 | Validation error | `Yes` | `size` | Query `size` không parse được thành `int32` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`1.3`](./05_Data_Mapping.md#13-validate-size) | `No` | Range/default chưa được contract xác nhận |
| 4 | Validation error | `Yes` | `sort` | Query `sort` không có kiểu `string` hoặc không khớp allow-list sau khi được xác nhận | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`1.4`](./05_Data_Mapping.md#14-validate-sort) | `No` | Allow-list chưa được contract đặc tả |
| 5 | System error | `No` | `courses/users` | Lỗi đọc query, count hoặc map response; hoặc thiếu mentor cho Course bắt buộc | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`4.3/6.3`](./05_Data_Mapping.md#43-lỗi-đọc-hoặc-map) | `No` | Không trả raw query, stack trace hoặc storage detail |

> Mỗi error case và mỗi field validation phải nằm trên một row riêng.

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
