---
title: "Định nghĩa table"
order: 7
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | SOURCE_REQUIRED — chưa chọn |
| Logical table | Content review outcome |
| Operation | UPDATE logical status and store review reason |
| Data Mapping step | Step 5; see [Step 3](./05_Data_Mapping.md#3-insertupdate-thong-tin) |

> Đây là logical mutation/gap register, chưa phải physical DB specification. Legacy DDL không có generic Content/review table. V1-PILOT content_review_decisions dùng UUID revision identity và không được map trực tiếp sang Content ID int64.

## Update mapping

**Áp dụng khi**

- AC-33 reject branch được thực hiện với target Content/revision đã được policy xác nhận.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | SOURCE_REQUIRED | Content status | ContentStatus | TBD | N/A | TBD | N/A | Set REJECTED theo AC-33 node n11 | AC-33 node n11 | Step 5 | Logical field; physical table/column and state ownership unresolved. |
| 2 | SOURCE_REQUIRED | Rejection reason value | string | TBD | N/A | Yes at request | N/A | Request body reason | API catalog #81 and AC-33 node n11 | Step 5 | Logical value only; physical column/relation and null/retention policy unresolved. |

## Insert mapping

**Áp dụng khi**

- Không có append/insert write được nêu rõ cho nhánh reject; audit parity với API #80 cần xác nhận.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | Separate audit/decision append | N/A | N/A | N/A | N/A | N/A | Not specified by reject diagram node | AC-33 node n11 | N/A | Do not infer an additional audit write; resolve with #80 before implementation. |

## Delete mapping

**Áp dụng khi**

- N/A — API #81 không khai báo delete.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE operation. |
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
