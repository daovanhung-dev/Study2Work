---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
---

# Error

## Giải thích

Contract API #04 liệt kê `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED` và `500 DESIGN_INTERNAL_ERROR`. Các điều kiện bên dưới tách contract khỏi nhánh hiện có trong source. Source ánh xạ user row không tồn tại thành `401`; catalog chưa quy định riêng ngữ nghĩa này nên cần xác nhận.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication error | `Yes` | `Authorization/JWT` | Thiếu/sai Bearer header; JWT sai/hết hạn; thiếu/sai `sub` hoặc `roles`; hoặc current source không tìm thấy user theo JWT subject | `401` | `DESIGN_AUTHENTICATION_REQUIRED` | `N/A — envelope message` | [`0.1/0.2/2.3`](./05_Data_Mapping.md#01-get-request-header) | `No` | Không có `404` trong catalog; user-not-found là current-source mapping, semantics cần xác nhận |
| 2 | Authorization error | `Yes` | JWT `roles` | Token hợp lệ nhưng `roles` không chứa `STUDENT` sau chuẩn hóa uppercase | `403` | `DESIGN_ACCESS_DENIED` | `N/A — envelope message` | [`0.3`](./05_Data_Mapping.md#03-check-role) | `No` | Source không so role trong token với `users.role` |
| 3 | System error | `No` | JWT configuration | Decoder trả lỗi không phải `401`, ví dụ cấu hình verification key không dùng được; helper ánh xạ sang `500` | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`0.2/4.4`](./05_Data_Mapping.md#02-decode-token) | `No` | Không trả detail cấu hình hoặc secret |
| 4 | System error | `No` | `users` query | `SQLAlchemyError` khi đọc profile | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`2.1/2.3/4.4`](./05_Data_Mapping.md#23-check-result) | `Yes — rollback Session` | Không trả SQL/stack trace/credential detail |
| 5 | System error | `No` | `UserProfile` mapping | Hàng query không hợp lệ với model response, thiếu/sai trường bắt buộc | `500` | `DESIGN_INTERNAL_ERROR` | `N/A — envelope message` | [`3.1/4.4`](./05_Data_Mapping.md#31-map-userprofile) | `No` | Lỗi mapping được log theo trace ID; không có mutation cần rollback |

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
