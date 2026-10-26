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
| Operation | INSERT lessons plus optional asset-link rows |
| Data Mapping step | 3.1–3.4, mutation M1 |

## Update mapping

**Áp dụng khi**

- N/A — API #47 chỉ tạo lecture mới.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- Course tồn tại và `courses.mentor_id` trùng Mentor hiện tại; transaction tạo một lessons row.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | id | Lecture ID | BIGSERIAL | N/A | N/A | Yes | ● | DB-generated sequence | DB | 3.3 | Legacy candidate; API response contract int64; pilot ID là UUID. |
| 2 | course_id | Course ID | BIGINT | N/A | N/A | Yes for this request |  | Path course_id | Request path | 3.3 | Legacy FK candidate to courses.id; physical DDL allows nullable but API path is required. |
| 3 | name | Lecture title | VARCHAR | 200 | N/A | Yes |  | Request title | Request body | 3.3 | Logical title → physical name; max 200 is DERIVED from candidate schema. |
| 4 | content | Lecture content | TEXT | N/A | N/A | No in DB; required in API |  | `str(request.content)` decimal representation | Request content | 3.3 | User decision: request remains signed int64; persisted/returned value is decimal string. |
| 5 | video_url | Lecture video URL | TEXT | N/A | N/A | No |  | Omitted | N/A | 3.3 | No request field; nullable legacy column remains NULL. |
| 6 | sort_order | Lecture order | INT | N/A | N/A | No in DB; required in API |  | Request order | Request body | 3.3 | Logical order → physical sort_order; no positivity rule inferred. |
| 7 | status | Lesson status | VARCHAR | 20 | N/A | No in DB; explicit value supplied |  | `PUBLISHED` | User decision | 3.3 | Explicit INSERT value; does not use legacy default DRAFT. |
| 8 | created_at | Creation time | TIMESTAMP | N/A | N/A | Yes |  | `CURRENT_TIMESTAMP` | Database clock | 3.3 | Legacy DDL has no default; live timezone/schema behavior is not verified. |
| 9 | updated_at | Update time | TIMESTAMP | N/A | N/A | Yes |  | `CURRENT_TIMESTAMP` | Database clock | 3.3 | Same database timestamp expression as created_at. |

## Ordered asset association mapping — lesson_uploads

**Áp dụng khi**

- `asset_refs` contains one or more unique UploadAsset IDs that were resolved for the same Mentor, `LECTURE` purpose and course.
- The association rows are inserted after the lesson row and before the transaction commits.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| 1 | lesson_id | Lecture ID | BIGINT | N/A | N/A | Yes | ● | ID returned by lessons INSERT | Database | 3.4 | FK to lessons.id; delete cascades with lesson. |
| 2 | upload_id | UploadAsset ID | BIGINT | N/A | N/A | Yes | ● | Validated asset_refs ID | Request after scoped uploads lookup | 3.4 | FK to uploads.id; unique per lesson. |
| 3 | asset_position | Asset position | BIGINT | N/A | N/A | Yes |  | Zero-based original array position | Request order | 3.4 | Nonnegative and unique per lesson; API #48 orders by this field. |

The insert is skipped for an empty asset_refs array. Any incomplete relation insert rolls back the lesson and all links. Migration availability on the live database is not verified.

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
