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
| Physical tables | `lessons` and `lesson_status_audit_logs` legacy candidates |
| Logical table | Lesson |
| Operation | SELECT FOR UPDATE + UPDATE + INSERT audit on change |
| Data Mapping step | [3. Update và audit](./05_Data_Mapping.md#step-3-update-audit) |
| Schema status | Legacy BIGINT DDL/runtime candidate; migration 012 is DERIVED source only. Live schema/deployment chưa xác minh; V1-PILOT UUID/versioned Lesson khác. |

## Update mapping

**Áp dụng khi**

- Legacy candidate row `lessons.id = :lesson_id` được tìm thấy sau ADMIN auth.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|---|
| 1 | status | Lesson status | VARCHAR | 20 | N/A | Nullable/default DRAFT in legacy DDL | No | `:status` | Strict body enum `DRAFT/PUBLISHED/SUSPENDED` | 3.2 | Enum is DERIVED from API #76; no transition matrix. |
| 2 | updated_at | Updated timestamp | TIMESTAMP | N/A | N/A | Required in legacy DDL | No | `CURRENT_TIMESTAMP` | Database clock | 3.2 | DERIVED, following adjacent legacy update APIs. |
| 3 | id | Lesson ID | BIGSERIAL | N/A | N/A | Primary key | Yes | `:lesson_id` predicate | Path lesson_id | 3.1 | Runtime candidate key; live schema unknown. |

## Audit mapping — migration 012 DERIVED

**Áp dụng khi**

- AC-34 status changes from its locked previous value.

| Logical item | Physical column | Type/relationship | Source/status |
|---|---|---|---|
| Lesson | `lesson_id` | BIGINT FK → `lessons.id` | Migration 012 DERIVED |
| Admin actor | `actor_user_id` | BIGINT FK → `users.id` | Numeric JWT `sub` from current shared guard; legacy key DERIVED |
| Previous status | `previous_status` | VARCHAR(20) NULL | DERIVED; allows legacy nullable source status |
| New status | `new_status` | VARCHAR(20) NOT NULL | Validated request status |
| Audit time | `changed_at` | TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP | DERIVED DB timestamp |

Migration 012 declares indexes on `(lesson_id, changed_at DESC, id DESC)` and `(actor_user_id, changed_at DESC, id DESC)`. The checked-in migration does not prove it is applied to a live database. Same-status requests do not insert an audit row.

## Insert mapping

**Áp dụng khi**

- N/A — API #85 does not create a lesson.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---|---|---|---|---|---|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No INSERT into lessons. |

## Delete mapping

**Áp dụng khi**

- N/A — delete belongs to API #86.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | No DELETE operation. |

## WHERE mapping

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| 1 | `lessons.id` | = | Path `lesson_id` | 3.1 | Candidate primary-key predicate from legacy DDL. |

## Response columns

| No | Column/source | Response path | Transform/status |
|---:|---|---|---|
| 1 | id | data.id | Copy and validate identity. |
| 2 | course_id | data.course_id | Copy; required Lesson vs nullable legacy DDL discrepancy. |
| 3 | name | data.title | SQL alias; reusable API #09 mapping. |
| 4 | content | data.content | Nullable source; JSON null preserved. |
| 5 | video_url | data.video_url | Nullable text source; JSON null preserved. |
| 6 | sort_order | data.order | SQL alias; reusable API #09 mapping. |
| 7 | status | data.status | Updated/current value; response model validates string. |
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
