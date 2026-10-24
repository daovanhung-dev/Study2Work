---
title: "Định nghĩa table"
order: 7
dd_id: "85"
api_name: "Đổi trạng thái lesson"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | lessons (legacy candidate) |
| Logical table | Lesson |
| Operation | UPDATE + logical audit intent |
| Data Mapping step | [3. Update và audit](./05_Data_Mapping.md#step-3-update-audit) |
| Schema status | Legacy BIGINT DDL candidate; live schema chưa xác minh; V1-PILOT UUID/versioned Lesson khác. |

## Update mapping

**Áp dụng khi**

- Candidate lesson row có lessons.id = :lesson_id và Admin đã authorize.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | status | Lesson status | VARCHAR | 20 | N/A | Nullable/default DRAFT trong legacy DDL | No | :status | Body status proposal | 3.1 | Target values/transitions chưa được xác nhận. |
| 2 | updated_at | Updated timestamp | TIMESTAMP | N/A | N/A | Required in legacy DDL | No | CURRENT_TIMESTAMP candidate | Server clock unless another owner/trigger applies | 3.1 | DERIVED; timestamp ownership unresolved. |
| 3 | id | Lesson ID | BIGSERIAL | N/A | N/A | Primary key | Yes | :lesson_id predicate | Path lesson_id | 3.1 | Candidate WHERE key; live schema unknown. |

## Audit mapping

**Áp dụng khi**

- AC-34 yêu cầu audit sau thao tác đổi trạng thái.

| Logical item | Physical source | Status |
|---|---|---|
| Actor/Admin subject | Chưa có mapping được duyệt | SOURCE_REQUIRED |
| Lesson/resource ID | Legacy lesson ID BIGINT không map trực tiếp sang V1 audit_events.resource_id UUID | SOURCE_REQUIRED |
| Action/status before-after | Không có payload schema được chọn | SOURCE_REQUIRED |
| Trace/outcome | Chưa xác nhận relation và transaction policy | SOURCE_REQUIRED |

Không viết INSERT mapping cho tới khi schema owner xác nhận physical relation, key types, action, payload và transaction behavior.

## Insert mapping

**Áp dụng khi**

- N/A — API #85 không tạo lesson.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No INSERT into lessons. |

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
| 3 | name | data.title | Alias name → title. |
| 4 | content | data.content | Nullable source; null/omit unresolved. |
| 5 | video_url | data.video_url | TEXT source candidate; URI/null handling unresolved. |
| 6 | sort_order | data.order | Alias sort_order → order. |
| 7 | status | data.status | Updated target candidate; enum/casing unresolved. |

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
