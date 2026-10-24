---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Error

## Quy ước

Các mã dưới đây là error contract trực tiếp của catalog #96. Trạng thái/trigger chi tiết, error envelope runtime và thứ tự quyền/resource chưa được xác nhận vì endpoint chưa có source.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP | Business code | Data Mapping reference | Remarks |
|---:|---|---|---|---|---:|---|---|---|
| 1 | Authentication | Có | Bearer JWT | Token thiếu/không hợp lệ theo contract | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | 0 | Claim/parser hiện tại cho Admin chưa được xác minh. |
| 2 | Authorization | Có | Admin permission | Sai role hoặc không có permission được cấp | 403 | `DESIGN_ACCESS_DENIED` | 0 | Permission key/scope và precedence chưa có nguồn. |
| 3 | Resource lookup | Có | `notification_id` | Notification không tồn tại theo lookup được owner duyệt | 404 | `DESIGN_RESOURCE_NOT_FOUND` | 2 | Exact not-found/tombstone semantics chưa rõ. |
| 4 | System error | Có | Read/aggregate | Lỗi nội bộ khi đọc source đã được duyệt | 500 | `DESIGN_INTERNAL_ERROR` | 2 | Không trả SQL, provider detail hoặc stack trace. |

## Không tự thêm error

- Catalog #96 không khai báo 422, 409 hoặc 503; không thêm các status này trong DD.
- Malformed/overflow `notification_id` không có mapping riêng trong catalog; cần xác nhận trước khi thay đổi error contract.
- Lỗi delivery dependency hiện chưa có 503 ở #96, dù API #92 có 503; không sao chép code giữa endpoint.
- 404, 403 precedence và error `data` shape cần owner/runtime convention review.
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

