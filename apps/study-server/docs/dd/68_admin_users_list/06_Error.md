---
title: "Error"
order: 6
dd_id: "68"
api_name: "Lấy danh sách user"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error cases trực tiếp từ catalog

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Token thiếu hoặc không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; endpoint chưa wired. |
| 2 | Authorization | Role/policy | Admin user-management permission | Principal không có role/quyền Admin | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-0-check-quyen) | No | DIRECT code/status; guard/policy SOURCE_REQUIRED. |
| 3 | System error | Database/profile mapping | Query hoặc response projection | Database/query/mapping failure | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [Data Mapping](./05_Data_Mapping.md#step-4-check-ket-qua-execute-query) | No | DIRECT code/status; không trả raw SQL/stack trace. |

Không thêm 404 hoặc 422 vào direct error set. Empty results là candidate 200, nhưng response list cần contract correction.

## Candidate branch questions — không phải HTTP contract

| Điều kiện | Candidate hoặc câu hỏi | Trạng thái |
|---|---|---|
| Role/status không có trong dữ liệu | Exact-match filter cho zero rows; candidate empty list 200 | DERIVED; cần chốt semantics response list. |
| Keyword rỗng sau trim | Bỏ keyword predicate | DERIVED; cần xác nhận trim/normalization. |
| Page không truyền | Proposal dùng page 1 | DERIVED; catalog chưa ghi default. |
| Page bằng 0/âm | Không tự chọn clamp, reject hay code lỗi | SOURCE_REQUIRED; catalog không liệt kê 422. |
| Không có user khớp | Proposal trả items=[]/total=0 trong HTTP 200 | DERIVED; direct UserProfile không biểu diễn empty list. |
| DB query hoặc mapping lỗi | 500 DESIGN_INTERNAL_ERROR | Code/status DIRECT; #68 chưa wired. |

## Error envelope discrepancy

- Current error_response helper thay data bị lược bằng {}.
- API guideline quy định data:null cho lỗi.
- Middleware DESIGN_CONTRACT_PATHS chưa có /api/v1/admin/users; nếu wire sau này, phải cập nhật allowlist để không rơi về fallback VALIDATION_ERROR/INTERNAL_SERVER_ERROR.
- Đây là current infrastructure và conditional future wiring; không phải quan sát runtime API #68.

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
