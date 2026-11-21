---
title: "Error"
order: 6
dd_id: "67"
api_name: "Lấy tiến độ Student"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu hoặc không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; shared Mentor guard hiện được gọi. |
| 2 | Authorization | Role/course scope | Mentor/course | Sai role Mentor hoặc không có quyền sở hữu course | 403 | `DESIGN_ACCESS_DENIED` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code; runtime fallback dùng direct owner `courses.mentor_id = sub`. |
| 3 | Not found | Resource/membership | Course/Student | Course không tồn tại hoặc Student không thuộc ACTIVE roster của course | 404 | `DESIGN_RESOURCE_NOT_FOUND` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-2-get-thong-tin) | No | DIRECT code; Student eligibility/404 privacy behavior là DERIVED fallback. |
| 4 | System error | Database/mapping | Progress query/result | Database failure hoặc không dựng được response | 500 | `DESIGN_INTERNAL_ERROR` | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-execute-query) | No | DIRECT code/status; không trả SQL/stack trace. |

Không thêm error code hoặc HTTP status ngoài catalog #67.

## Runtime fallback branch rules

| Điều kiện | Runtime fallback behavior | Trạng thái |
|---|---|---|
| Bearer thiếu/sai/hết hạn | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Shared guard hiện hành; verified bằng HTTP test. |
| Principal không có role Mentor | 403 `DESIGN_ACCESS_DENIED` | Shared MENTOR guard hiện hành; verified bằng HTTP test. |
| Course ngoài quyền Mentor | 403 `DESIGN_ACCESS_DENIED` | Runtime direct-owner fallback theo #65/#66. |
| Student không thuộc active learner set của course | 404 `DESIGN_RESOURCE_NOT_FOUND` | Runtime fallback dùng ACTIVE enrollment và STUDENT role như #65. |
| Student hợp lệ nhưng chưa có lesson progress row | 200; lesson state NOT_STARTED/0, timestamps null | DERIVED fallback được implement. |
| Course/Student không tồn tại hoặc signed-int64 path lỗi | 404 `DESIGN_RESOURCE_NOT_FOUND` | Code/status trực tiếp; path/resource mapping theo local #65/#66 pattern. |
| Query/projection error | 500 `DESIGN_INTERNAL_ERROR`, error `data:null` | Shared helper hiện hành; rollback và response an toàn. |

## Runtime error behavior

- Current `error_response` mặc định `data:null` và gắn trace ID/header.
- Middleware `DESIGN_CONTRACT_PATHS` đã chứa path #67.
- Catalog không khai báo 422 cho malformed path; API #67 ánh xạ path int64 lỗi sang 404 theo fallback #65/#66.
- Fake DB HTTP tests kiểm tra local response; không xác minh production DB/schema/deployment.

## Security handling

- Xác minh Mentor course scope và Student membership trước khi đọc/trả progress.
- Student ngoài ACTIVE roster trả 404 với message Student chung; policy privacy vẫn cần business approval.
- Không trả token, email, quiz answers, assignment submissions, raw SQL hoặc stack trace.

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
