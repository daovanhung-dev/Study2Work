---
title: "Error"
order: 6
dd_id: "65"
api_name: "Lấy tiến độ toàn lớp"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Error code trực tiếp từ catalog

| HTTP | Business code | Direct meaning | Candidate trigger | Status |
|---:|---|---|---|---|
| 401 | DESIGN_AUTHENTICATION_REQUIRED | Bearer JWT thiếu/không hợp lệ. | Guard không xác thực được principal. | Code/status DIRECT; local route tested. |
| 403 | DESIGN_ACCESS_DENIED | Không đủ role hoặc quyền truy cập. | Role không phải Mentor hoặc course thuộc Mentor khác. | Code DIRECT; direct-owner rule DERIVED, local route tested. |
| 404 | DESIGN_RESOURCE_NOT_FOUND | Resource không tồn tại. | Malformed/overflow course ID hoặc course không tồn tại. | Code DIRECT; local mapping DERIVED and tested. |
| 500 | DESIGN_INTERNAL_ERROR | Lỗi nội bộ không xác định. | Query hoặc projection/aggregate mapping failure. | Code/status DIRECT; safe local mapping tested. |

Không thêm 422, 409 hoặc 503 vì catalog #65 không khai báo các lỗi này.

## Branch rules cần xác nhận

| Điều kiện | Candidate behavior | Trạng thái |
|---|---|---|
| Bearer absent/invalid | 401 | Shared guard local behavior; HTTP tested. |
| Principal không có role Mentor | 403 | Shared guard local behavior; HTTP tested. |
| Course không tồn tại | 404 | Direct catalog code; local lookup behavior DERIVED and tested. |
| Course có nhưng không thuộc scope Mentor | 403 | Direct catalog code; direct-owner fallback DERIVED and tested. |
| Schema/query/aggregation failure | 500 | Direct catalog code; safe error behavior tested with fake DB. |

## Error envelope discrepancy

- API guideline quy định error response với data:null; shared `error_response` mặc định `data=None`, HTTP test xác nhận 401 trả null.
- Route template đã được thêm vào `DESIGN_CONTRACT_PATHS`, giữ các DESIGN_* mappings cho handler.
- HTTP tests xác minh 401/403/404/500 local; không xác minh live DB errors hoặc deployment config.

## Security handling

- Không trả thông tin roster trước khi xác định role, course access và 403/404 privacy policy.
- Không đưa SQL, stack trace, raw DB values hoặc token vào message/details.
- Audit event, rate limit và masking behavior chưa được đặc tả cho API #65.

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
