---
title: "Error"
order: 6
dd_id: "66"
api_name: "Lấy analytics tổng hợp"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error codes trực tiếp từ catalog

| HTTP | Business code | Direct meaning | Candidate trigger | Status |
|---:|---|---|---|---|
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT thiếu hoặc không hợp lệ. | Không xác thực được principal. | Code/status DIRECT; endpoint chưa wired. |
| 403 | DESIGN_ACCESS_DENIED | Role hoặc quyền truy cập không hợp lệ. | Candidate: course ngoài scope Mentor. | Code DIRECT; quyền và predicate DERIVED/SOURCE_REQUIRED. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource không tồn tại. | Candidate: course không tồn tại. | Code DIRECT; object/authorization order chưa chốt. |
| 500 | DESIGN_INTERNAL_ERROR | Lỗi hệ thống không xác định. | Query/source/aggregation failure. | Code/status DIRECT; endpoint error mapping chưa chạy. |

Không thêm error code vào direct contract.

## Candidate branch rules

| Điều kiện | Candidate behavior | Trạng thái |
|---|---|---|
| Bearer thiếu/sai/hết hạn | 401 | Code DIRECT; auth helper hiện tại chỉ hỗ trợ Student guard. |
| Principal không có role Mentor | 403 | Code DIRECT; Mentor guard chưa có source. |
| Course không tồn tại | 404 | DERIVED mapping từ catalog error; query chưa tồn tại. |
| Course tồn tại nhưng ngoài scope Mentor | 403 hoặc privacy-preserving 404 | SOURCE_REQUIRED; policy chưa có. |
| Event source/query lỗi | 500 | Code DIRECT; physical source chưa được chọn. |

## Error envelope discrepancy

- API guidelines quy định data:null khi lỗi.
- Current error_response thay data absent thành {}.
- Middleware DESIGN_CONTRACT_PATHS chưa có path #66; nếu route được wire mà allowlist không cập nhật, request-validation/unhandled error có thể dùng fallback code.
- Đây là điều kiện tích hợp tương lai, không phải response đã quan sát của API #66.

## Security handling

- Không truy vấn/serialize analytics trước khi xác định Mentor và quyền course.
- Không trả raw event payload, nội dung nhạy cảm, SQL hoặc stack trace.
- Giữ tổng hợp ở mức course; metric theo learner không được thêm nếu chưa có contract/quyền rõ ràng.

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
