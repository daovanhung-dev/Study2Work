---
title: "Error"
order: 6
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "4.Error"
format: markdown
dd_id: "40"
api_name: "Tạo topic/câu hỏi mới"
status: "Draft — Needs Confirmation"
---

# Error

## Giải thích

Các trường hợp giữ đúng HTTP/business code của API #40 trong approved catalog. Predicate course access, field constraints ngoài required/type, insert defaults và transaction behavior chưa được chốt.

## Error cases

| No | Category | Verify check | Item | Condition | HTTP status | Error code | Error message ID | Data Mapping reference | Rollback | Remarks |
|---:|---|---|---|---|---:|---|---|---|---|---|
| 1 | Authentication | Bearer JWT | `Authorization` | Token thiếu, không hợp lệ hoặc không xác thực được. | 401 | `DESIGN_AUTHENTICATION_REQUIRED` | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Theo catalog và API guideline. |
| 2 | Authorization | Student role/course access | Principal / `course_id` | Role không phải Student hoặc access bị từ chối theo predicate sau khi được xác nhận. | 403 | `DESIGN_ACCESS_DENIED` | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Course participation predicate chưa có nguồn. |
| 3 | Validation | Required/type | `course_id` | Thiếu giá trị hoặc không theo kiểu `int64` đã khai báo. | 422 | `DESIGN_VALIDATION_ERROR` | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Không thêm range rule. |
| 4 | Validation | Required/type | `title` | Thiếu giá trị hoặc không theo kiểu `string` đã khai báo. | 422 | `DESIGN_VALIDATION_ERROR` | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Length/blank policy chưa có nguồn. |
| 5 | Validation | Required/type | `content` | Thiếu giá trị hoặc không theo kiểu request `int64` của catalog. | 422 | `DESIGN_VALIDATION_ERROR` | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | N/A | Request type không khớp Discussion/DDL; không tự sửa. |
| 6 | System error | Candidate insert | `discussions` | Internal/database failure không có error mapping riêng trong catalog. | 500 | `DESIGN_INTERNAL_ERROR` | N/A | [05_Data_Mapping.md](./05_Data_Mapping.md) | TBD | Transaction rollback behavior chưa được đặc tả. |

> Catalog không khai báo 404, 409 hoặc 503 cho API #40. Không thêm các status/business code này vào DD.

## Error envelope

Error response dùng `success=false`, `businessCode` theo catalog, client-safe `message`, `data=null`, `meta` và `traceId` theo [API guidelines](../../../../../contracts/api-guidelines/README.md). Catalog không quy định endpoint-specific message ID.

## Chưa có nguồn cho các validation rule khác

| No | Field/condition | Status/code |
|---:|---|---|
| 1 | `course_id` tồn tại, enrollment hoặc discussion access | `SOURCE_REQUIRED`; catalog chỉ có 403 access denied và không định nghĩa predicate. |
| 2 | `title` length, blank handling và normalization | `SOURCE_REQUIRED`; catalog chỉ định kiểu/required. |
| 3 | `content` conversion/meaning giữa request `int64`, logical `string` và DDL `TEXT` | `DISCREPANCY`; không thêm validation code hoặc conversion. |
| 4 | Insert defaults/timestamps và transaction rollback | `SOURCE_REQUIRED`; DDL là design evidence, không xác nhận runtime. |
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
