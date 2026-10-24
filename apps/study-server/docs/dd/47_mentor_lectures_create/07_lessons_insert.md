---
title: "Định nghĩa table — lessons INSERT"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "47"
api_name: "Tạo lecture"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | lessons |
| Logical table | Lecture — legacy mapping candidate |
| Operation | INSERT |
| Data Mapping step | 3.1–3.4, mutation M1 |

## Update mapping

**Áp dụng khi**

- N/A — API #47 chỉ tạo lecture mới.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- Q1 course tồn tại và candidate Mentor ownership check đạt; transaction M1 tạo một lessons row.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Lecture ID | BIGSERIAL | N/A | N/A | Yes | ● | DB-generated sequence | DB | 3.3 | Legacy candidate; API response contract int64; pilot ID là UUID. |
| 2 | course_id | Course ID | BIGINT | N/A | N/A | Yes for this request |  | Path course_id | Request path | 3.3 | Legacy FK candidate to courses.id; physical DDL allows nullable but API path is required. |
| 3 | name | Lecture title | VARCHAR | 200 | N/A | Yes |  | Request title | Request body | 3.3 | Logical title → physical name; max 200 is DERIVED from candidate schema. |
| 4 | content | Lecture content | TEXT | N/A | N/A | No in DB; required in API |  | Decimal-string representation candidate | Request content | 3.3 | DISCREPANCY: request int64 may be an ID; conversion is DERIVED and blocks confirmation. |
| 5 | video_url | Lecture video URL | TEXT | N/A | N/A | No |  | Omitted | N/A | 3.3 | No request field; nullable legacy column remains NULL. |
| 6 | sort_order | Lecture order | INT | N/A | N/A | No in DB; required in API |  | Request order | Request body | 3.3 | Logical order → physical sort_order; no positivity rule inferred. |
| 7 | status | Lesson status | VARCHAR | 20 | N/A | No in DB; default applies |  | Omit column; candidate default DRAFT | Legacy DDL | 3.3 | LessonStatus enum members are SOURCE_REQUIRED; pilot lifecycle differs. |
| 8 | created_at | Creation time | TIMESTAMP | N/A | N/A | Yes |  | CURRENT_TIMESTAMP | Database clock | 3.3 | Legacy DDL has no default; timezone semantics unresolved. |
| 9 | updated_at | Update time | TIMESTAMP | N/A | N/A | Yes |  | CURRENT_TIMESTAMP | Database clock | 3.3 | Same insert timestamp candidate; legacy DDL has no default. |

## Delete mapping

**Áp dụng khi**

- N/A — API #47 không xóa lecture.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Không tạo DELETE giả. |

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
