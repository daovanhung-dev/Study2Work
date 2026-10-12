---
title: "Error"
order: 6
dd_id: "36"
api_name: "Xác nhận dữ liệu đã nộp"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các error cases giữ nguyên status/business code của API catalog #36. Điều kiện truy cập resource và một số mapping dữ liệu chưa được chốt; các điểm này được đánh dấu SOURCE_REQUIRED. Error envelope đặt data=null theo API Guidelines.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Required | Authorization | Bearer JWT thiếu hoặc không hợp lệ. | 401 | DESIGN_AUTHENTICATION_REQUIRED | SOURCE_REQUIRED | 0.1 / 4.2 | No | Catalog-confirmed status/code; no API #36 route is wired. |
| 2 | Authorization | Required | Student role / submission access | Role không phải Student hoặc predicate access đã được duyệt từ chối; predicate cụ thể SOURCE_REQUIRED. | 403 | DESIGN_ACCESS_DENIED | SOURCE_REQUIRED | 0.1 / 0.2 / 4.2 | No | Catalog includes 403; inaccessible-row masking as 404 is unresolved. |
| 3 | Resource lookup | Required | submission_id | Không tìm thấy submission theo candidate ID lookup. | 404 | DESIGN_RESOURCE_NOT_FOUND | SOURCE_REQUIRED | 2.2 / 2.3 / 4.3 | No | Catalog-confirmed status/code; relation to access denial must be decided. |
| 4 | System error | N/A | Internal operation | Lỗi database hoặc lỗi ứng dụng không dự kiến. | 500 | DESIGN_INTERNAL_ERROR | SOURCE_REQUIRED | 2 / 4.4 | No | Return a safe message; do not expose SQL or stack traces. |

> Không thêm 400, 409, 422 hoặc 503 ngoài error set của API #36. Parse-failure handling cho path int64 chưa được catalog định nghĩa; xem OPEN_QUESTIONS.md.

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
