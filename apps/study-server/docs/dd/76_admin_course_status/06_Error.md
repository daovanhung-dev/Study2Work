---
title: "Error"
order: 6
dd_id: "76"
api_name: "Thay đổi trạng thái khóa học Admin"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

- Danh sách dưới đây giữ nguyên HTTP status và business code của API catalog #76.
- Body/status validation mapping là candidate vì direct request schema bị bỏ trống.
- Admin guard, audit storage và route chưa tồn tại; bảng lỗi là design, không phải runtime evidence.
- Không thêm HTTP status hoặc business code ngoài tập đã khai báo trong catalog.

## Error cases

| No | HTTP | Business code | Điều kiện | Xử lý candidate | Source/status |
|---:|---:|---|---|---|---|
| 1 | 401 | DESIGN_AUTHENTICATION_REQUIRED | Thiếu, sai hoặc hết hạn Bearer JWT | Dừng trước course query; safe error envelope | Catalog DIRECT; route/auth chưa wire |
| 2 | 403 | DESIGN_ACCESS_DENIED | Principal hợp lệ nhưng không có Admin role/course-management permission | Dừng trước course query; không tiết lộ course existence | Catalog + AC-32 DIRECT |
| 3 | 404 | DESIGN_RESOURCE_NOT_FOUND | Không có course theo course_id | Rollback transaction; trả lỗi không kèm course data | Catalog DIRECT; Q1 branch DERIVED |
| 4 | 422 | DESIGN_VALIDATION_ERROR | course_id parse lỗi hoặc candidate body thiếu/không hợp lệ | Có thể thêm meta.fieldErrors theo guideline; cụ thể rule/status enum cần owner duyệt | Catalog code DIRECT; mapping DERIVED |
| 5 | 500 | DESIGN_INTERNAL_ERROR | DB read/update, required audit append, response mapping hoặc commit lỗi | Rollback; safe message; log nội bộ cùng trace ID | Catalog DIRECT; side-effect mapping theo diagram |
| 6 | 500 | DESIGN_INTERNAL_ERROR | Course projection thiếu required mentor/price hoặc sai dữ liệu | Không trả projection thiếu hợp đồng; rollback candidate | Candidate theo #06/#74/#75; owner policy cần duyệt |

## Error envelope

API guideline yêu cầu data:null, meta.fieldErrors cho lỗi field-level và X-Trace-Id. Current error_response() trả data:{} nếu không truyền data; đây là discrepancy tích hợp cần xử lý khi wire route.

Request-validation và unhandled-exception handlers chỉ chọn DESIGN_VALIDATION_ERROR/DESIGN_INTERNAL_ERROR cho path nằm trong DESIGN_CONTRACT_PATHS. Admin course status hiện chưa nằm trong allowlist; middleware dùng exact path membership, nên future route wiring phải hỗ trợ dynamic course_id qua route-aware/path-pattern mapping, không chỉ thêm path template có {course_id}.

## Branch ordering

1. Authentication và authorization trước mọi lookup.
2. Path/body validation trước mutation.
3. Q1 không thấy course → 404.
4. Status update + audit append cùng transaction candidate.
5. Audit/update/projection/commit lỗi → 500.
6. Thành công → 200 DESIGN_RESOURCE_UPDATED.
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
