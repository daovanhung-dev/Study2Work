---
title: "Error"
order: 6
dd_id: "59"
api_name: "Lấy nội dung request/thread"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các lỗi giữ nguyên catalog API #59. Malformed/out-of-range `request_id` trả catalog 404 theo pattern API #48 vì #59 không khai báo 422. Error helper hiện tại trả `data:null` và trace ID.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Header thiếu, token invalid hoặc claim không hợp lệ | 401 | DESIGN_AUTHENTICATION_REQUIRED | Chưa quy định | [1.1](./05_Data_Mapping.md#11-xác-thực-bearer-jwt) | No | Shared auth guard. |
| 2 | Authorization | Role/scope | Mentor/request | Role không phải Mentor hoặc request hiện hữu thuộc course của Mentor khác | 403 | DESIGN_ACCESS_DENIED | Chưa quy định | [2.1](./05_Data_Mapping.md#21-đọc-request-và-owner) | Yes — rollback read transaction | Access predicate direct `courses.mentor_id`; owner mismatch follows #48/#55. |
| 3 | Not found | Path/query | `request_id` | Path sai định dạng/ngoài int64 hoặc request ID không tồn tại | 404 | DESIGN_RESOURCE_NOT_FOUND | Chưa quy định | [3.1](./05_Data_Mapping.md#31-path-parameter), [4.1](./05_Data_Mapping.md#41-q1--supportrequest-detail-và-student) | No | Không thêm 422 ngoài catalog. |
| 4 | System error | Query/projection | Request/thread/assets | DB lỗi hoặc required relation/asset projection không nhất quán | 500 | DESIGN_INTERNAL_ERROR | Chưa quy định | [4–6](./05_Data_Mapping.md#4-đọc-request-và-conversation) | Yes — best-effort rollback | Không trả stack trace hoặc partial thread. |

Error envelope dùng shared `error_response(...)`, bao gồm `data:null`, `meta` và `traceId` theo runtime hiện tại.

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
