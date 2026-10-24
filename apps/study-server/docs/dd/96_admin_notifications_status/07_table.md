---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "96"
api_name: "Xem trạng thái delivery notification Admin"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — API read-only

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | N/A — chưa có Admin relation được duyệt |
| Logical table | Admin Notification và delivery aggregate (logical only) |
| Operation | SELECT / read-only |
| Data Mapping step | 2 |

## Update mapping

**Áp dụng khi**

- N/A — API #96 không cập nhật dữ liệu.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | — | — | — | — | Không có UPDATE | N/A | N/A | Read-only API. |

## Insert mapping

**Áp dụng khi**

- N/A — API #96 không tạo dữ liệu.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | — | — | — | — | Không có INSERT | N/A | N/A | Read-only API. |

## Delete mapping

**Áp dụng khi**

- N/A — API #96 không xóa dữ liệu.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| — | N/A | N/A | N/A | N/A | Read-only API. |

## Query/source boundary

Các bảng legacy/pilot được ghi trong [05_Data_Mapping.md](./05_Data_Mapping.md) chỉ là evidence/candidate. Không có physical SELECT mapping nào được chốt cho đến khi owner chọn Admin model, grain và delivery aggregate source.
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

