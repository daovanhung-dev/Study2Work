---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `users` |
| Logical table | `User account` |
| Operation | `INSERT` |
| Data Mapping step | `6. Insert users` |

## Update mapping

**Áp dụng khi**

- `N/A — API #1 không thực hiện UPDATE`.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| - | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | |

## Insert mapping

**Áp dụng khi**

- Sau khi validate thành công và `Q1` xác nhận email chưa tồn tại.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `id` | `User ID` | `BIGSERIAL` | `N/A` | `N/A` | `Y` | `●` | `DB-generated` | `ERD V1` | `6.1` | Serialize to contract `int64` |
| 2 | `full_name` | `Full name` | `VARCHAR` | `150` | `N/A` | `Y` | ` ` | `request["full_name"]` | `03_Request.md` | `6.1` | |
| 3 | `email` | `Email` | `VARCHAR` | `255` | `N/A` | `Y` | ` ` | `request["email"]` | `03_Request.md` | `6.1` | `UNIQUE, NOT NULL` |
| 4 | `password_hash` | `Password hash` | `VARCHAR` | `255` | `N/A` | `Y` | ` ` | `hash(request["password"])` | `05_Data_Mapping.md#41-hash-password` | `4.1/6.1` | Never return plaintext/hash |
| 5 | `role` | `Account role` | `VARCHAR` | `20` | `N/A` | `Y` | ` ` | `"STUDENT"` | `AC-01 + list_api.md` | `4.2/6.1` | Default role |
| 6 | `avatar_url` | `Avatar URL` | `TEXT` | `N/A` | `N/A` | `N` | ` ` | `NULL` when absent | `ERD V1` | `6.1` | Optional |
| 7 | `phone` | `Phone` | `VARCHAR` | `20` | `N/A` | `N` | ` ` | `NULL` when absent | `ERD V1` | `6.1` | Optional |
| 8 | `status` | `Account status` | `VARCHAR` | `20` | `N/A` | `N` | ` ` | `DB default ACTIVE` | `ERD V1` | `6.1` | |
| 9 | `created_at` | `Created time` | `TIMESTAMP` | `N/A` | `N/A` | `Y` | ` ` | `TBD — generator chưa đặc tả` | `ERD V1 (NOT NULL)` | `6.1` | |
| 10 | `updated_at` | `Updated time` | `TIMESTAMP` | `N/A` | `N/A` | `Y` | ` ` | `TBD — generator chưa đặc tả` | `ERD V1 (NOT NULL)` | `6.1` | |

## Delete mapping

**Áp dụng khi**

- `N/A — API #1 không thực hiện DELETE`.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| - | `N/A` | `N/A` | `N/A` | `N/A` | |

---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `table`
- Dimension: `A1:BA35`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `19`
- Số vùng merge: `5`

<details>
<summary>Danh sách vùng merge</summary>

- `W34:BA34`
- `W14:BA14`
- `W15:BA15`
- `W19:BA19`
- `W32:BA32`

</details>

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 2 | `A2` | № |  |
| 2 | `B2` | Tên table |  |
| 3 | `B3` | SB |  |
| 3 | `S3` | Độ dài |  |
| 3 | `T3` | Dấu phẩy thập phân |  |
| 3 | `U3` | Bắt buộc |  |
| 3 | `V3` | Main key |  |
| 3 | `W3` | Nội dung setting |  |
| 4 | `B4` | № |  |
| 4 | `C4` | Item ID |  |
| 4 | `I4` | Item name |  |
| 4 | `O4` | Kiểu |  |
| 5 | `A5` | 1 |  |
| 5 | `B5` | table id |  |
| 5 | `I5` | table name |  |
| 6 | `B6` | Update |  |
| 6 | `I6` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  > 0 |  |
| 21 | `B21` | Insert |  |
| 21 | `I21` | Trường hợp số record get được từ xử lý 3. của sheet [３．Data mapping]  = 0 |  |

</details>
