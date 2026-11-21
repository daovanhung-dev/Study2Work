---
title: "Định nghĩa table"
order: 7
dd_id: "75"
api_name: "Cập nhật metadata khóa học Admin"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `courses` |
| Logical table | Course |
| Operation | `UPDATE` |
| Data Mapping step | `3. Insert/Update thông tin` |
| Schema status | Legacy BIGINT DDL candidate; live schema chưa xác minh. V1-PILOT dùng UUID/versioned model khác. |

## Update mapping

**Áp dụng khi**

- Q1 candidate update một course theo `courses.id = :course_id`.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `name` | Tiêu đề | `VARCHAR` | 200 | N/A | Yes in legacy DDL | No | `:title` | Request body proposal | 3.4 | Physical candidate; maps logical Course.title. |
| 2 | `description` | Mô tả | `TEXT` | N/A | N/A | No, nullable | No | `:description` or NULL | Request body proposal | 3.4 | Null-clearing proposal; legacy candidate. |
| 3 | `thumbnail_url` | URL thumbnail | `TEXT` | N/A | N/A | No, nullable | No | `:thumbnail_url` or NULL | Request body proposal | 3.4 | URI validation unresolved. |
| 4 | `price` | Giá | `NUMERIC` | 12 | 2 | No, nullable in DDL | No | `:price` decimal | Request body proposal | 3.4 | Contract response requires decimal-string; nullability discrepancy. |
| 5 | `updated_at` | Thời điểm cập nhật | `TIMESTAMP` | N/A | N/A | Yes in legacy DDL | No | Server current timestamp | Server | 3.4 | DERIVED update timestamp behavior. |

## Insert mapping

**Áp dụng khi**

- N/A — API #75 cập nhật resource hiện có; không tạo course mới.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No INSERT operation. |

## Delete mapping

**Áp dụng khi**

- N/A — course deletion thuộc API #77.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE operation. |

## WHERE mapping

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | `courses.id` | `=` | path `:course_id` | 3.2 | Candidate legacy primary key; schema/live status unresolved. |
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
