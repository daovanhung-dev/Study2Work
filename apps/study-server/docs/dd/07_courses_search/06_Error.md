---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API #7 theo `list_api.md`. Empty result là kết quả thành công `200`; không tạo `404`.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Validation error | `Yes` | `q` | Query `q` không có kiểu string hoặc không thể normalize theo input contract | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.1`](./05_Data_Mapping.md#21-validate-q) | `No` | q optional; blank sau trim không phải lỗi |
| 2 | Validation error | `Yes` | `category` | Query `category` không parse được thành `int64` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.2`](./05_Data_Mapping.md#22-validate-category) | `No` | Category relation vẫn TBD; không tạo JOIN giả |
| 3 | Validation error | `Yes` | `page` | Query `page` không parse được thành `int32` hoặc nhỏ hơn `1` | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.3`](./05_Data_Mapping.md#23-validate-page) | `No` | Default page là `1` design-only |
| 4 | Validation error | `Yes` | `sort` | Query `sort` không có kiểu string hoặc không khớp allow-list đã được xác nhận | `422` | `DESIGN_VALIDATION_ERROR` | `N/A — envelope message` | [`2.4`](./05_Data_Mapping.md#24-validate-sort) | `No` | Allow-list/default order chưa được contract đặc tả |
| 5 | System error | `No` | `courses/users` | Lỗi query page, count, join hoặc map response; hoặc published course thiếu mentor bắt buộc | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`5.3`](./05_Data_Mapping.md#53-lỗi-đọc-hoặc-map) | `No` | Không trả raw query, stack trace hoặc storage detail |

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

</details>
