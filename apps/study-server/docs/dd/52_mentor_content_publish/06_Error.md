---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "52"
api_name: "Publish/unpublish nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

API #52 giữ đúng năm lỗi trong catalog. Các điều kiện phụ thuộc body/state là proposal DERIVED; route chưa được triển khai.

## Error cases

| No | HTTP status | Business code | Điều kiện theo contract | Data Mapping reference | Response/source rule | Status |
|---:|---:|---|---|---:|---|---|
| 1 | 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT thiếu, sai hoặc hết hạn | 0 | Safe error envelope; không echo token/claims. | Code DIRECT; route absent |
| 2 | 403 | DESIGN_ACCESS_DENIED | Principal không có role Mentor hoặc không có quyền quản lý course chứa Content | 0 | Không tiết lộ owner/assignment internals. | Code DIRECT; access predicate SOURCE_REQUIRED |
| 3 | 404 | DESIGN_RESOURCE_NOT_FOUND | content_id không ánh xạ tới Content | 2 | Error envelope, không trả dữ liệu một phần. | Code DIRECT; physical lookup SOURCE_REQUIRED |
| 4 | 422 | DESIGN_VALIDATION_ERROR | Request target/body sai nếu proposal được duyệt, readiness không đạt, hoặc transition không hợp lệ theo policy được duyệt | 1, 2, 3 | Không echo payload nhạy cảm; catalog giữ nguyên code. | Code DIRECT; conditions DERIVED/SOURCE_REQUIRED |
| 5 | 500 | DESIGN_INTERNAL_ERROR | Lỗi bất ngờ khi load/readiness/update publication state | 2–4 | Safe error; không trả SQL, schema, stack/provider detail. | Code DIRECT; route absent |

## Nhánh cần xác nhận

| Tình huống | Code catalog hiện có | Cần chốt |
|---|---|---|
| APPROVED Content thiếu dữ liệu cần thiết | 422 candidate | Readiness criteria theo từng ContentType/payload chưa có nguồn. |
| PENDING_REVIEW hoặc REJECTED được yêu cầu publish | 422 candidate | State machine DERIVED; enum đầy đủ SOURCE_REQUIRED. |
| Unpublish Content đã PUBLISHED | 200 candidate | Đề xuất trở về APPROVED; cần xác nhận review semantics. |
| Request lặp lại target state | 200 candidate | No-op/idempotency là DERIVED proposal. |
| Content không tồn tại với Mentor không có quyền | 403 hoặc 404 | Thứ tự check/anti-enumeration cần policy; giữ nguyên code set. |
| Path int64 sai/overflow | Framework behavior chưa được xác nhận | Catalog không có 422 cho path riêng; kiểm tra khi runtime implementation được tạo. |

## Middleware integration discrepancy

API #52 chưa có route và /api/v1/mentor/content/{content_id}/publish không có trong DESIGN_CONTRACT_PATHS. Nếu route được wire mà allowlist/error mapping không đổi, framework validation/unhandled exceptions có thể trả generic VALIDATION_ERROR/INTERNAL_SERVER_ERROR thay cho DESIGN_VALIDATION_ERROR/DESIGN_INTERNAL_ERROR. Đây là discrepancy tích hợp tương lai, không phải current runtime behavior của API #52.

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
