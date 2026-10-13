---
title: "Định nghĩa table"
order: 7
dd_id: "27"
api_name: "Tìm bài tiếp theo theo curriculum"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | lessons |
| Logical table | Lesson |
| Operation | READ ONLY |
| Data Mapping step | 2.2, 2.3, 3.1 |

Bảng dưới mô tả các cột candidate từ DB design/DDL được dùng trong Data Mapping. Đây không phải xác nhận query hoặc schema đang chạy. Cột được ánh xạ theo logical Lesson khi có căn cứ; các điểm chưa rõ được ghi rõ trong Remarks.

## Update mapping

**Áp dụng khi**

- N/A — API #27 là GET và không cập nhật lessons.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No update operation | N/A | N/A | Read-only contract. |

## Insert mapping

**Áp dụng khi**

- N/A — API #27 là GET và không tạo lessons.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No insert operation | N/A | N/A | Read-only contract. |

## Delete mapping

**Áp dụng khi**

- N/A — API #27 là GET và không xóa lessons.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | N/A | N/A | N/A | N/A | Read-only contract. |

## Read projection candidate

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Lesson ID | BIGSERIAL / int64 | N/A | N/A | Y | Primary key | Candidate response data.id | DB design and checked-in DDL | 2.2, 2.3, 3.1 | DB type is BIGSERIAL in checked-in DDL; live schema not verified. |
| 2 | course_id | Course ID | BIGINT / int64 | N/A | N/A | Y |  | Candidate response data.course_id | DB design, ERD and checked-in DDL | 2.2, 2.3, 3.1 | Logical Lesson/ERD treat it as required; checked-in DDL permits NULL. See OPEN_QUESTIONS Q-27-04. |
| 3 | name | Lesson title | VARCHAR | 200 | N/A | Y |  | Candidate response data.title | Checked-in DDL; API #9 mapping precedent | 2.3, 3.1 | Candidate alias name → title. Do not treat API #9 precedent as API #27 approval. |
| 4 | content | Lesson content | TEXT | N/A | N/A | N |  | Candidate response data.content | Checked-in DDL and Lesson contract | 2.3, 3.1 | Null/omit behavior is not specified. |
| 5 | video_url | Video URI | TEXT | N/A | N/A | N |  | Candidate response data.video_url | Checked-in DDL and Lesson contract | 2.3, 3.1 | URI conversion and null behavior are not specified. |
| 6 | sort_order | Curriculum order | INT | N/A | N/A | Y |  | Candidate response data.order | DB design and checked-in DDL | 2.2, 2.3, 3.1 | Default is 0 in checked-in DDL. Selection direction and tie-break are open. |
| 7 | status | Lesson status | VARCHAR | 20 | N/A | Y |  | Candidate response data.status | Checked-in DDL and Lesson contract | 2.2, 2.3, 3.1 | DDL default is DRAFT; enum values and publish visibility policy are not confirmed. |

### Read conditions

- Candidate current row key: lessons.id = path lesson_id. API #27 runtime query is not present to confirm this mapping.
- Candidate next-row scope/order/status conditions remain SOURCE_REQUIRED. See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-27-02-curriculum-order-and-duplicates) and [05_Data_Mapping.md](./05_Data_Mapping.md).
- Candidate cardinality and the meaning of HTTP 404 remain SOURCE_REQUIRED. See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-27-03-current-lesson-and-no-next-result).

---
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
