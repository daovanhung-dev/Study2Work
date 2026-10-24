---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "50"
api_name: "Tạo nội dung mới Conditional"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — Logical Content, physical mapping SOURCE_REQUIRED

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table/model | `SOURCE_REQUIRED`; chưa có generic Content table tương thích trong legacy DDL. |
| Logical entity | `Content` theo API catalog #50. |
| Operation | Một logical INSERT theo AC-22. |
| Data Mapping step | 5–7 |
| Evidence | Catalog row #50 + Content schema; AC-22 INSERT node; AC-33 pending queue; legacy/pilot DDL comparison. |
| Runtime | Route/service/test chưa được tìm thấy (`UNWIRED` / `NOT_FOUND`). |

## Insert mapping

| Logical field | Value source | Candidate rule | Evidence/status |
|---|---|---|---|
| `id` | Persistence layer | Generate BIGINT-compatible Content ID | `SOURCE_REQUIRED`; allocator/schema absent |
| `course_id` | Request body | Persist selected course after permission check | DIRECT logical input; physical FK SOURCE_REQUIRED |
| `content_type` | Request body | Persist approved enum member | DIRECT field; enum/type storage SOURCE_REQUIRED |
| `title` | Request body | Persist title | DIRECT field; length/normalization/schema SOURCE_REQUIRED |
| `payload` | Request body | Persist JSON object matching approved subtype schema | DIRECT field; payload/storage SOURCE_REQUIRED |
| `status` | Server lifecycle | `PENDING_REVIEW` candidate | DERIVED inference from AC-22 create + AC-33 pending queue; confirm transition and persistence |
| `parent_id` | Server default; not request | Candidate `NULL` for root Content | `DERIVED`; parent relationship and root creation policy need confirmation |
| `order` | Server allocator; not request | Candidate next order among root siblings of the course | `DERIVED`; scope, transaction/locking and uniqueness rule need confirmation |
| `created_by`/timestamps/audit | Not in contract | No value assigned here | `SOURCE_REQUIRED`; do not invent columns or payload fields |

## SQL mapping

No physical `INSERT` statement is approved. The target table, column names/types, constraints, ID strategy, transaction handling and returned row projection are unknown. Legacy `lessons` and V1-PILOT `content_blocks` are not substituted for generic Content.

### Legacy course access candidate only

~~~sql
SELECT c.id, c.mentor_id
FROM courses AS c
WHERE c.id = :course_id;
~~~

This is only a legacy-schema query candidate for course existence/direct owner. It is not the Content write target, does not resolve JWT-to-Mentor identity, and does not cover course assignment. Live schema is not verified.

## Cross-API lifecycle

- API #50 creates Content; AC-33 expects review queue items at `PENDING_REVIEW`.
- API #51 updates Content, #52 publishes/unpublishes and #53 deletes. Their interactions with pending/rejected/approved content and the physical model need the AC-22 macro-review after #51–#53 DDs are available.
- AC-33 approves/rejects and refers to audit/review data; that does not authorize adding audit columns to this API's table without schema evidence.

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
