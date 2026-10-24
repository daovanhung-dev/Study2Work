---
title: "Error"
order: 6
dd_id: "103"
api_name: "Xuất báo cáo tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP status và business codes dưới đây được khai báo trực tiếp trong row API #103. Điều kiện cụ thể ngoài mô tả dependency unavailable chưa được chốt; proposal được ghi rõ là DERIVED.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Yes | Bearer JWT | Thiếu hoặc credential không hợp lệ theo quy ước catalog. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — catalog không khai báo message ID | Step 2 | No | Nguồn kiểm tra token cho Admin chưa được xác nhận. |
| 2 | Authorization | Yes | Admin/report permission | Principal không có quyền xem report/analytics. | 403 | DESIGN_ACCESS_DENIED | N/A — catalog không khai báo message ID | Step 2 | No | Admin claim/permission policy chưa có trong current Study source. |
| 3 | Dependency unavailable | Yes | Export queue / file storage | DERIVED trigger: dependency từ chối trước khi job được chấp nhận. | 503 | DESIGN_DEPENDENCY_UNAVAILABLE | N/A — catalog không khai báo message ID | Step 4 | N/A | Dependency và acceptance boundary cụ thể là SOURCE_REQUIRED. |
| 4 | System error | No | Export request processing | Lỗi ngoài nhánh auth/access/dependency được duyệt. | 500 | DESIGN_INTERNAL_ERROR | N/A — catalog không khai báo message ID | Step 4/5 | N/A | Không trả raw SQL, storage key, stack trace hoặc provider detail. |

## Các lỗi chưa có mapping được duyệt

- Invalid filters JSON.
- Unsupported format.
- Format omitted.
- Failure sau khi HTTP 202 đã được gửi.
- Duplicate/retry GET request.
- Operation missing hoặc inaccessible trong API #18 poll.
- Không ánh xạ các case này sang HTTP 400/404/422 nếu contract chưa được cập nhật.

Chi tiết luồng: [05_Data_Mapping.md](./05_Data_Mapping.md#step-5-map-response-hoặc-lỗi).

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
