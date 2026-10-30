---
title: "Định nghĩa table"
order: 7
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical candidates | Legacy `contents`; `content_review_audit_logs` from migration 011 |
| Logical table | Content review state and decision |
| Operation | UPDATE status; INSERT one reason-bearing decision/audit row |
| Data Mapping step | [Step 3](./05_Data_Mapping.md#step-3-mutation) |

> AC-33 directly requires `REJECTED` plus review reason. The physical source below reuses checked-in legacy BIGINT candidates and is DERIVED; migration 011 is not proof of live deployment. V1-PILOT `content_review_decisions` uses UUID revision/reviewer IDs and is not selected for this int64 contract.

## Update mapping — `contents`

**Áp dụng khi** locked active Content currently has `PENDING_REVIEW`.

| No | Physical column | Logical name | Type | Length | Required | Key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|
| 1 | `status` | Content review status | TEXT | N/A | Yes | `contents.id` | Literal `REJECTED` | AC-33 node n11; legacy DDL candidate | Step 3.1 | `PENDING_REVIEW` predicate is DERIVED; no `updated_at` column exists in legacy `contents`. |

## Insert mapping — `content_review_audit_logs`

**Áp dụng khi** the conditional status update returns a valid Content projection. One row stores the decision and direct review reason; no separate second audit append is performed.

| No | Physical column | Logical name | Type | Length | Required | Key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---|
| 1 | `id` | Decision row ID | BIGSERIAL | N/A | Generated | PK | Database sequence/default | Migration 011 | Step 3.2 | Omitted from INSERT and response. |
| 2 | `content_id` | Content ID | BIGINT | N/A | Yes | FK → `contents.id` | Parsed path ID | Catalog #81 + migration 011 | Step 3.2 | Bound parameter. |
| 3 | `actor_user_id` | Admin actor | BIGINT | N/A | Yes | FK → `users.id` | Numeric JWT `sub` | Shared ADMIN guard + migration 011 | Step 3.2 | Never accepted from request. |
| 4 | `previous_status` | Previous Content status | TEXT | N/A | Yes | — | Locked value `PENDING_REVIEW` | Current locked row | Step 3.2 | Bound parameter. |
| 5 | `new_status` | Resulting Content status | TEXT | N/A | Yes | — | Literal `REJECTED` | AC-33 node n11 | Step 3.2 | Bound parameter. |
| 6 | `reason` | Review reason | TEXT NULL | N/A | Request required | — | Body `reason`, unchanged | Catalog #81; migration 011 candidate | Step 3.2 | Required in request; nullable column is shared with bodyless #80 approval. |
| 7 | `recorded_at` | Decision time | TIMESTAMPTZ | N/A | Generated | — | Database default `CURRENT_TIMESTAMP` | Migration 011 | Step 3.2 | Omitted from INSERT and response. |

## Transaction

`contents.status` update and the single decision-row INSERT run in the same caller-owned transaction. Validate the Content projection before commit. Query, insert, response mapping or commit failure rolls back both writes. This atomicity is a DERIVED local implementation choice; it does not prove live DB behavior.

## Unchanged mappings

- No `content_versions` insert/update is performed; #81 has no revision selector.
- No DELETE or second audit row is issued.
- `reason`, reviewer, version and audit columns are not added to the Content response.
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
