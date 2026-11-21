---
title: "Error"
order: 6
dd_id: "102"
api_name: "Lấy dữ liệu tác động cộng đồng"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Catalog #102 định nghĩa đúng ba nhánh lỗi. AC-38 yêu cầu validate date range, nhưng endpoint row không khai báo 400/422; DD không tự thêm status hoặc business code. Trigger chi tiết của Admin/report permission và aggregate failure chưa có runtime source.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error Message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | N/A | Bearer JWT | Thiếu hoặc token không hợp lệ theo auth policy | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa nêu | Bước 0 | N/A | Status/code DIRECT; Admin guard chưa có |
| 2 | Authorization | N/A | Admin/report permission | Principal không có quyền xem báo cáo | 403 | `DESIGN_ACCESS_DENIED` | Chưa nêu | Bước 0 | N/A | DIRECT catalog/AC; claim policy SOURCE_REQUIRED |
| 3 | System error | N/A | Aggregate/query source | Lỗi nội bộ khi đọc/tổng hợp report | 500 | `DESIGN_INTERNAL_ERROR` | Chưa nêu | Bước 2–4 | N/A — read-only | Status/code DIRECT; exact infrastructure mapping chưa có |

## Input conditions chưa có mapping

- `from`/`to` có thể không parse thành ISO date hoặc `from > to`; AC-38 nói validate nhưng catalog không khai báo status/code cho các trường hợp này.
- `segment` ngoài `learning`/`community` hoặc chuỗi rỗng chưa có allowed-values/error rule.
- Không tự thêm 400/422, không mượn error code #103.
- Count rỗng đề xuất trả metric value `"0"`, không phải error.

## Error response convention

API guidelines mô tả envelope lỗi `success:false`, `data:null`, `businessCode`, `message`, `meta`, `traceId`. #102 chưa có route để xác minh current serializer/wiring.
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
