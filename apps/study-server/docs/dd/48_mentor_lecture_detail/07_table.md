---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "48"
api_name: "Tải lại lecture vừa tạo"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — N/A — READ-ONLY API

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | lessons, courses — candidate legacy read source |
| Logical table | Một Lecture và course cha để kiểm tra quyền |
| Operation | SELECT only; design-only |
| Data Mapping step | 2 |
| Evidence | API #48 catalog, AC-21, DB guide/ERD, legacy DDL; live schema chưa xác minh |

## Update mapping

**Áp dụng khi**

- N/A — API #48 không cập nhật bảng.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có UPDATE. |

## Insert mapping

**Áp dụng khi**

- N/A — API #48 không tạo record; API #47 owns candidate insert.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không có INSERT. |

## Delete mapping

**Áp dụng khi**

- N/A — API #48 không xóa record.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | Không có DELETE. |

## Current checked-in read projection

> Runtime reads the checked-in legacy BIGINT schema; this does not prove the live database has migration 004/005 applied.

| No | Table | Candidate column | Type in checked-in DB.sql | DDL constraint | Data Mapping use | Source status |
|---:|---|---|---|---|---|---|
| 1 | lessons AS l | id | BIGSERIAL | PRIMARY KEY | Lecture.id | Checked-in legacy source |
| 2 | lessons AS l | course_id | BIGINT | FK; nullable trong DB.sql | Lecture.course_id và join parent | DDL/guide discrepancy; live unknown |
| 3 | lessons AS l | name | VARCHAR(200) | NOT NULL | Map sang Lecture.title | Checked-in legacy source |
| 4 | lessons AS l | content | TEXT | NULL | Map sang Lecture.content | SQL NULL serializes as JSON null |
| 5 | lessons AS l | sort_order | INT | DEFAULT 0 | Map sang Lecture.order | Checked-in legacy source |
| 6 | lessons AS l | status | VARCHAR(20) | DEFAULT DRAFT | Map sang Lecture.status tanpa filter | Enum members unspecified |
| 7 | courses AS c | id | BIGSERIAL | PRIMARY KEY | Kiểm tra parent course | Checked-in legacy source |
| 8 | courses AS c | mentor_id | BIGINT | Nullable FK to users.id | Direct-owner access | Assignment/identity unresolved |
| 9 | lesson_uploads AS lu | lesson_id | BIGINT | FK lessons.id; ON DELETE CASCADE | Resolve links for lecture | Migration 005; live schema unknown |
| 10 | lesson_uploads AS lu | upload_id | BIGINT | FK uploads.id | Resolve UploadAsset ID | Migration 005; live schema unknown |
| 11 | lesson_uploads AS lu | asset_position | BIGINT | Nonnegative; unique per lesson | Preserve asset order | Migration 005; live schema unknown |
| 12 | uploads AS u | id, file_name, url, content_type, size_bytes, status | BIGINT/TEXT/VARCHAR | Required metadata in migration 004 | UploadAsset projection | API #34 source; live schema unknown |

## Mapping gaps

| Contract item | Candidate source | Status | Impact |
|---|---|---|---|
| Lecture.assets[] | lesson_uploads + uploads | IMPLEMENTED_IN_CHECKED_IN_SOURCE | #47 writes links and #48 resolves ordered metadata locally; live migration not verified. |
| UploadAsset nested metadata | uploads metadata from API #34 | IMPLEMENTED_IN_CHECKED_IN_SOURCE | Not mapped from legacy resources or V1-PILOT file_objects. |
| Assigned Mentor course | No assignment relation in inspected legacy artifacts | SOURCE_REQUIRED | Candidate mentor_id không bao phủ AC-21 assigned-course case. |
| Live schema | Legacy and V1-PILOT differ; live metadata not verified | NOT_VERIFIED | Candidate SQL not implementation approval. |

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
