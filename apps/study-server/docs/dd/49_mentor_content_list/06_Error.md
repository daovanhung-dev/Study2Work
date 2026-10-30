---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Error"
format: markdown
dd_id: "49"
api_name: "Lấy cây nội dung course"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Bảng dưới đây giữ đúng business-code/status trong catalog #49. Các nhánh được ánh xạ theo source hiện tại; các quy tắc owner/version vẫn cần owner confirmation.

## Error cases

| No | HTTP status | Business code | Điều kiện hiện tại | Data Mapping step | Response/source rule | Status |
|---:|---:|---|---|---:|---|---|
| 1 | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Bearer JWT thiếu hoặc không hợp lệ | 1 | Shared error envelope; không trả token/claims | Source-backed guard; catalog DIRECT |
| 2 | 403 | `DESIGN_ACCESS_DENIED` | Role không phải Mentor hoặc `courses.mentor_id` không khớp principal | 1–2 | Không tiết lộ nội dung/course owner | Direct-owner là implementation choice |
| 3 | 404 | `DESIGN_RESOURCE_NOT_FOUND` | Path ID sai format/out-of-range hoặc course không tồn tại | 2 | `data: null`; không có Content một phần | Catalog DIRECT; condition source-backed |
| 4 | 500 | `DESIGN_INTERNAL_ERROR` | Query, projection hoặc cây không nhất quán/có cycle | 3–4 | Message an toàn; rollback nếu DB transaction dở | Catalog DIRECT; source-backed handling |

## Error envelope boundary

`error_response` dựng envelope sáu khóa. Nếu caller không truyền data, JSON là `data: null`; `meta` mặc định `{}`. API #49 path template đã nằm trong `DESIGN_CONTRACT_PATHS`, nên middleware nhận design business-code dispatch.

## Input boundary

Route nhận `course_id` dưới dạng raw string và view tự parse signed int64. Vì vậy path lỗi/out-of-range trả API #49 404; request không đi qua FastAPI integer validation và không phát sinh 422 cho trường hợp này.

## Không khai báo

HTTP 422, 409 và 503 không nằm trong API #49 contract; implementation không thêm các business code đó.

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
