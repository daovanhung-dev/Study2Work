---
title: "Error"
order: 6
dd_id: "62"
api_name: "Lấy tập người nhận"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

API #62 chỉ dùng catalog error codes 401/403/404/500. Path ID sai format/range được map sang 404 để giữ error set; không thêm HTTP 422. Course có roster rỗng là thành công với `data: []`.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | `Authorization` | Header thiếu, sai scheme hoặc JWT/sub/roles không hợp lệ. | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A | [Data Mapping](./05_Data_Mapping.md#step-0-auth-va-nhan-request) | No DB transaction | Shared auth guard. |
| 2 | Authorization | Role | JWT roles | Token hợp lệ nhưng không có role `MENTOR`. | 403 | `DESIGN_ACCESS_DENIED` | N/A | [Data Mapping](./05_Data_Mapping.md#step-0-auth-va-nhan-request) | No DB transaction | Không đọc course/roster. |
| 3 | Authorization | Direct owner | `courses.mentor_id` | Course tồn tại nhưng owner khác principal. | 403 | `DESIGN_ACCESS_DENIED` | N/A | [Data Mapping](./05_Data_Mapping.md#step-2-check-course-scope) | Rollback read transaction | Roster query không chạy. |
| 4 | Not found | Path/course lookup | `course_id` / `courses.id` | Raw ID sai signed-int64 format/range hoặc course không tồn tại. | 404 | `DESIGN_RESOURCE_NOT_FOUND` | N/A | [Data Mapping](./05_Data_Mapping.md#step-1-parse-course-id) | Rollback if course lookup ran | Không thêm 422. |
| 5 | System error | DB/projection | `courses`, `enrollments`, `users` | Query lỗi hoặc response projection không hợp lệ. | 500 | `DESIGN_INTERNAL_ERROR` | N/A | [Data Mapping](./05_Data_Mapping.md#step-5-returnerror) | Rollback read transaction | Không lộ SQL, stack trace hoặc dữ liệu nội bộ. |

## Error envelope

`error_response` trả `data: null`, `meta: {}` và cùng trace ID trong body/header. Response không phản chiếu chi tiết lỗi database.

## Empty roster

Không phải error case. Course tồn tại, đúng owner nhưng không có enrollment đủ điều kiện trả HTTP 200 `DESIGN_RESOURCE_RETRIEVED` với `data: []`.
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
