---
title: "Error"
order: 6
dd_id: "64"
api_name: "Theo dõi trạng thái gửi"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---


# Error

## Giải thích

Giữ đúng error set catalog #64: 401, 403, 404 và 500. Không thêm 400, 422, 409 hoặc 503. Các mapping path/scope/status resource dưới đây là local DERIVED fallback và DD vẫn Draft.

## Error cases

| No | Category | Check | Item | Condition | HTTP status | Error code | Message | Data Mapping reference | Transaction | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer/JWT | Authorization | Header thiếu hoặc token không hợp lệ | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Safe authentication message | [0. Auth](./05_Data_Mapping.md#step-0-auth) | N/A — read-only | Shared MENTOR guard. |
| 2 | Authorization | Role/owner | Mentor/notification | Sai role hoặc notification thuộc sender Mentor khác | 403 | `DESIGN_ACCESS_DENIED` | Safe access-denied message | [0. Auth](./05_Data_Mapping.md#step-0-auth), [2. Scope](./05_Data_Mapping.md#step-2-access) | N/A — read-only | Owner predicate từ `sender_id` là DERIVED. |
| 3 | Not found | Parse/resource/status resource | `notification_id` | Path sai/out-of-range; notification không tồn tại; không có Operation ID hoặc delivery rows | 404 | `DESIGN_RESOURCE_NOT_FOUND` | Safe not-found message | [1. Parse](./05_Data_Mapping.md#step-1-request), [2. Scope](./05_Data_Mapping.md#step-2-access) | N/A — read-only | No extra 400/422; older non-dispatch notifications have no status resource. |
| 4 | System error | DB/projection/model | Notification/outbox/Operation projection | Query fails, status counts contradict total, or required UUID/owner/timestamps are malformed | 500 | `DESIGN_INTERNAL_ERROR` | Safe internal-error message | [3. Aggregate](./05_Data_Mapping.md#step-3-read-delivery), [4. Map](./05_Data_Mapping.md#step-4-map-response) | Rollback failed read transaction; no mutation | Never expose SQL, provider details or stack trace. |

Error envelope uses `data:null`, `meta:{}` or safe field metadata as supplied by shared `error_response(...)`; trace ID is kept in body/header.

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
