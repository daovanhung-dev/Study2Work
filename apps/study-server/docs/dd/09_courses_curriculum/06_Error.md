---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Các trường hợp lỗi của API #9 theo contract API V1. API chỉ khai báo `404 DESIGN_RESOURCE_NOT_FOUND` và `500 DESIGN_INTERNAL_ERROR`; không tạo thêm `403` hoặc `422`.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Not found | `Yes` | `course_id` | Path không parse được `int64`, hoặc Q1 không có course với `c.id = course_id AND c.status = 'PUBLISHED'` | `404` | `DESIGN_RESOURCE_NOT_FOUND` | `N/A — envelope message` | [`1.2`](./05_Data_Mapping.md#12-validate-course_id) / [`2.2`](./05_Data_Mapping.md#22-check-result) / [`5.2`](./05_Data_Mapping.md#52-not-found-response) | `No` | Gom path type mismatch, course không tồn tại và course draft/private theo contract status 404 |
| 2 | System error | `No` | `courses/lessons` | Lỗi Q1/Q2, lỗi mapping `Page<Lesson>` hoặc lỗi tạo envelope | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.2`](./05_Data_Mapping.md#32-check-result) / [`5.3`](./05_Data_Mapping.md#53-system-error-response) | `No` | Không trả raw SQL, stack trace hoặc storage detail |

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
<summary>Bản ghi đối chiếu</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `B2` | Giải thích |  |
| 4 | `C4` | Các trường hợp lỗi của API |  |
| 10 | `C10` | Category |  |
| 10 | `J10` | Tên item |  |

</details>
