---
title: "Error"
order: 6
dd_id: "61"
api_name: "Đóng yêu cầu hỗ trợ"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng error set API #61: 401, 403, 404, 422, 500. Không thêm 409, 503 hoặc business code ngoài catalog.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---:|---|
| 1 | Authentication | Bearer/JWT | Authorization | Header thiếu, token invalid hoặc claims không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | [Data Mapping](./05_Data_Mapping.md) | No | Shared Mentor guard chạy trước DB. |
| 2 | Authorization | Role/scope | Mentor/SupportRequest | Role không phải Mentor hoặc request thuộc course của Mentor khác | 403 | `DESIGN_ACCESS_DENIED` | [Data Mapping](./05_Data_Mapping.md) | Yes for open transaction | Owner là `courses.mentor_id = JWT sub`. |
| 3 | Not found | Resource lookup | SupportRequest | Không có request với signed-int64 ID | 404 | `DESIGN_RESOURCE_NOT_FOUND` | [Data Mapping](./05_Data_Mapping.md) | Yes for open transaction | Missing được phân loại trước owner mismatch. |
| 4 | Request/state validation | Path/current status | `request_id` / status | Path sai int64 hoặc state `CANCELLED`/không hỗ trợ | 422 | `DESIGN_VALIDATION_ERROR` | [Data Mapping](./05_Data_Mapping.md) | Yes | State rejection là DERIVED; helper dùng `meta.fieldErrors` cho path. |
| 5 | System error | DB/update/projection/commit | SupportRequest | Query, update, thread mapping, envelope hoặc commit lỗi | 500 | `DESIGN_INTERNAL_ERROR` | [Data Mapping](./05_Data_Mapping.md) | Yes before successful commit | Safe message; không lộ SQL/stack trace. |

## Envelope and trace

- Lỗi dùng `error_response(...)`, `data: null`, `meta: {}`; validation details nằm trong `meta.fieldErrors`.
- `X-Trace-Id` được gắn vào response; `traceId` trong JSON dùng cùng giá trị.
- `/api/v1/mentor/support/{request_id}/resolve` nằm trong middleware design-contract allowlist để framework 422/500 dùng code catalog.

## Transaction notes

- Lỗi sau khi mở transaction và trước commit gọi rollback.
- Không commit request đã bị từ chối hoặc projection không hợp lệ.
- Commit failure trả 500 và thử rollback an toàn.
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
