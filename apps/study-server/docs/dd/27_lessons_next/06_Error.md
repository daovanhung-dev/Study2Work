---
title: "Error"
order: 6
dd_id: "27"
api_name: "Tìm bài tiếp theo theo curriculum"
source_sheet: "4.Error"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các HTTP/business codes bên dưới được giữ đúng API #27 trong catalog. Contract không gắn điều kiện cụ thể cho access denial hoặc not-found. Shared API Guidelines quy định error response dùng data=null; error message và từng condition vẫn cần nguồn xác nhận.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Yes | Bearer JWT | Authentication failure theo contract; runtime trigger chưa xác minh. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only. | Không suy diễn JWT claim hoặc payload riêng. |
| 2 | Authorization | Yes | Student role / lesson access | Role/access bị từ chối theo contract; entitlement/publish predicate chưa rõ. | 403 | DESIGN_ACCESS_DENIED | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#0-authentication-and-access) | N/A — GET read-only. | Không tự đặt 403/404 masking. |
| 3 | Not found | Yes | Current or next Lesson | DESIGN_RESOURCE_NOT_FOUND có trong contract; current-lesson missing và terminal curriculum chưa phân biệt. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#2-read-current-curriculum-position-and-candidate-next-lesson) | N/A — GET read-only. | Không gán no-next thành 404 nếu chưa được xác nhận. |
| 4 | System error | No | Read/mapping processing | Lỗi nội bộ theo contract; exception mapping chưa xác minh. | 500 | DESIGN_INTERNAL_ERROR | N/A — catalog không có message ID. | [05_Data_Mapping.md](./05_Data_Mapping.md#5-return-response) | N/A — GET read-only. | Error data=null theo API Guidelines; không trả raw SQL/stack trace. |

> Catalog không khai báo 422 cho API #27. Không thêm validation error code hoặc error branch ngoài contract.

## Error response envelope

- success = false.
- businessCode = code tương ứng trong bảng Error cases.
- message = safe client message; nội dung cụ thể SOURCE_REQUIRED.
- data = null theo API Guidelines.
- meta = object theo reusable ApiEnvelope schema; API-specific members chưa khai báo.
- traceId = UUID theo reusable ApiEnvelope schema.
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
