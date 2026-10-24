---
title: "Định nghĩa table"
order: 7
dd_id: "84"
api_name: "Cập nhật lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | lessons |
| Logical table | Lesson |
| Operation | UPDATE |
| Data Mapping step | [3. Update lesson](./05_Data_Mapping.md#step-3-update-lesson) |
| Schema status | Legacy BIGINT DDL candidate; live schema chưa xác minh; V1-PILOT UUID/versioned model khác. |

## Update mapping

**Áp dụng khi**

- Candidate lesson row có lessons.id = :lesson_id và Admin đã authorize.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | name | Lesson title | VARCHAR | 200 | N/A | Yes in legacy DDL | No | :title | Body proposal title | 3.1 | Candidate legacy column; live schema/title rules unresolved. |
| 2 | content | Lesson content | TEXT | N/A | N/A | No, nullable in legacy DDL | No | :content or NULL candidate | Body proposal content | 3.1 | Null/omit behavior needs confirmation. |
| 3 | video_url | Video URL | TEXT | N/A | N/A | No, nullable in legacy DDL | No | :video_url or NULL candidate | Body proposal video_url | 3.1 | URI policy needs confirmation. |
| 4 | sort_order | Lesson order | INT | N/A | N/A | Nullable/default 0 in legacy DDL | No | :order | Body proposal order | 3.1 | Range/uniqueness unresolved. |
| 5 | updated_at | Updated timestamp | TIMESTAMP | N/A | N/A | Yes in legacy DDL | No | CURRENT_TIMESTAMP candidate | Server clock unless another owner/trigger applies | 3.1 | DERIVED; timestamp ownership unresolved. |

## Insert mapping

**Áp dụng khi**

- N/A — API #84 chỉ mô tả UPDATE lesson; create không thuộc nhánh này.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No INSERT operation. |

## Delete mapping

**Áp dụng khi**

- N/A — delete lesson thuộc API #86.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE operation. |

## WHERE mapping

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | lessons.id | = | Path lesson_id | 3.1 | Candidate primary-key predicate from legacy DDL. |

## Response columns

| No | Column/source | Response path | Transform/status |
|---:|---|---|---|
| 1 | id | data.id | Copy candidate. |
| 2 | course_id | data.course_id | Required response vs nullable legacy DDL discrepancy. |
| 3 | name | data.title | Alias name -> title. |
| 4 | content | data.content | Null/omit unresolved. |
| 5 | video_url | data.video_url | URI/null handling unresolved. |
| 6 | sort_order | data.order | Alias sort_order -> order. |
| 7 | status | data.status | Return unchanged; enum/casing unresolved; #84 does not update it. |

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
