---
title: "Table Update — quizzes"
order: 7
dd_id: "89"
api_name: "Cập nhật quiz"
source_sheet: "table mapping"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — quizzes UPDATE

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Logical table | Quiz |
| Physical table | legacy quizzes |
| Operation | UPDATE |
| Data Mapping step | [M1 — Step 4](./05_Data_Mapping.md#step-4-validate-course-and-update-quiz-parent) |
| Basis | Candidate từ infra/postgres/study-server/DB.sql; live schema chưa xác minh. |

## Điều kiện cập nhật

- quizzes.id = quiz_id từ path.
- `SELECT ... FOR UPDATE` khóa active Quiz trước child rows; `DELETED`/missing → 404.
- Chỉ cập nhật sau khi khóa child rows và history guard không thấy attempts/answers.

## Column mapping

| No | Physical column | Logical name | Type | Length | Scale | Required | PK | FK | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|---|
| 1 | id | Quiz ID | BIGSERIAL | N/A | N/A | Yes | Yes | No | <No change> | Path quiz_id | Step 4 | Candidate key; không đổi. |
| 2 | course_id | Course ID | BIGINT | N/A | N/A | DDL nullable | No | courses.id | config.course_id | DERIVED request body | Step 4 | Existing Course được khóa `FOR KEY SHARE`; move allowed. |
| 3 | name | Quiz title | VARCHAR | 200 | N/A | Yes | No | No | config.title | DERIVED request body | Step 4 | Alias title → name; #88 validator giới hạn 200 ký tự. |
| 4 | passing_score | Passing score | NUMERIC | 5 | 2 | DDL default 0 | No | No | config.passing_score | DERIVED request body | Step 4 | Validator #88 giới hạn exact decimal-string ±999.99. |
| 5 | time_limit_minutes | Duration | INT | N/A | N/A | Nullable | No | No | config.duration_minutes | DERIVED request body | Step 4 | Omit/null được ghi NULL. |
| 6 | updated_at | Update time | TIMESTAMP | N/A | N/A | Yes | No | No | CURRENT_TIMESTAMP | System/transaction | Step 4 | Legacy DDL NOT NULL/no default. |
| 7 | status | Quiz status | VARCHAR | 20 | N/A | DDL default DRAFT | No | No | <No change> | Existing row | Step 4 | Không có status trong request/response contract. |
| 8 | description | Description | TEXT | N/A | N/A | Nullable | No | No | <No change> | Existing row | Step 4 | Không có logical Quiz field. |

## Result handling

- UPDATE condition là `id = :quiz_id AND status IS DISTINCT FROM 'DELETED'`.
- Không set status, description hoặc created_at; không thay course status/enrollment state.
- `RETURNING` projection được kiểm tra trước khi delete/insert children và commit.
- Course target missing → 422; history found → 422 trước UPDATE.
- Database/write failure map 500 DESIGN_INTERNAL_ERROR theo catalog.
- Lỗi child-set operation hoặc response mapping rollback toàn transaction.
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
