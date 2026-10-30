---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "41"
api_name: "Thêm bình luận/trả lời"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Giữ đúng HTTP/business code của API #41 trong approved catalog. Parent lookup, course access, content conversion và insert behavior được ghi ở [05_Data_Mapping.md](./05_Data_Mapping.md). Không thêm code không có trong catalog.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer JWT | Authorization | Token thiếu, không hợp lệ hoặc không xác thực được. | 401 | DESIGN_AUTHENTICATION_REQUIRED | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Catalog. |
| 2 | Authorization | Student role/course access | Principal / parent course | Caller không phải Student, thiếu enrollment ACTIVE trong course, hoặc topic không ACTIVE theo predicate DERIVED. | 403 | DESIGN_ACCESS_DENIED | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Active enrollment/topic gate cần được xác nhận. |
| 3 | Resource | Parent lookup | discussion_id | Không tìm thấy topic gốc hoặc ID trỏ tới comment thay vì topic. | 404 | DESIGN_RESOURCE_NOT_FOUND | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Root-only behavior là DERIVED; concealment khi không có quyền cần xác nhận. |
| 4 | Validation | Required/type | discussion_id | Thiếu hoặc không parse được kiểu int64. | 422 | DESIGN_VALIDATION_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Type theo catalog; không thêm range rule ngoài type. |
| 5 | Validation | Required/type | content | Thiếu hoặc không parse được kiểu int64. | 422 | DESIGN_VALIDATION_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Conversion tới TEXT/string chưa được xác nhận. |
| 6 | System error | Candidate insert | discussions | Internal/database failure không có mapping riêng trong catalog. | 500 | DESIGN_INTERNAL_ERROR | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | DERIVED rollback insert transaction | No runtime transaction behavior exists. |

## Error envelope

Error response dùng success=false, businessCode theo catalog, client-safe message, data=null, meta và traceId theo [API guidelines](../../../../../contracts/api-guidelines/README.md). Catalog không định nghĩa endpoint-specific message ID.

## Chưa có nguồn cho validation/access rule khác

| No | Field/condition | Status/code |
|---:|---|---|
| 1 | Content integer range, text length, blank/meaning and moderation rule | SOURCE_REQUIRED; contract chỉ nêu required/type. |
| 2 | Course participation predicate and allowed discussion status | DERIVED proposal: enrollment ACTIVE and parent topic ACTIVE; policy still needs confirmation. |
| 3 | Whether discussion_id must identify a root topic or may be a comment | DERIVED root-topic assumption; needs confirmation. |
| 4 | Counter mutation failure behavior | No counter column/table in current design evidence; do not introduce another error case. |

> Catalog không khai báo 409 hoặc 503 cho API #41; không tự thêm các HTTP/business code này.
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

