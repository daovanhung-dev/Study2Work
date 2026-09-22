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
| Physical table | `categories` |
| Logical table | `Category` |
| Operation | `READ ONLY` |
| Data Mapping step | `4.1–4.3 — category source read and mapping` |

## Read-only source mapping

| No | Physical column | Logical field | Type | Required | Default/condition | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|---|---|
| 1 | `id` | Category ID | `BIGSERIAL` | Yes | Primary key | `4.3` | Response `data.items[].id` |
| 2 | `name` | Category name | `VARCHAR(200)` | Yes | N/A | `4.3` | Response `data.items[].name` |
| 3 | `slug` | Category slug | `VARCHAR(200)` | Yes | N/A | `4.3` | Response `data.items[].slug` |
| 4 | `description` | Category description | `TEXT` | No | `NULL` allowed | `4.3` | Response `data.items[].description` |
| 5 | `locale` | Category locale | `VARCHAR(20)` | Yes | Default `vi-VN`; exact-match filter | `2.2/4.2` | Not returned directly |
| 6 | `status` | Category status | `VARCHAR(20)` | Yes | Default `ACTIVE`; query requires `ACTIVE` | `4.2` | Not returned directly |

## Update mapping

**Áp dụng khi**

- `N/A — API #5 không có UPDATE.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DB giả |

## Insert mapping

**Áp dụng khi**

- `N/A — API #5 không có INSERT.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DB giả |

## Delete mapping

**Áp dụng khi**

- `N/A — API #5 không có DELETE.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DB giả |


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
