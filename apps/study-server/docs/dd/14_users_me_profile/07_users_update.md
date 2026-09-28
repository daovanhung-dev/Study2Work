---
title: "Định nghĩa table — users update"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `users` |
| Logical table | `Study user profile` |
| Operation | `UPDATE` |
| Data Mapping step | `3.2` |

## Update mapping

**Áp dụng khi**

- `users.id = user_id` lấy từ `JWT.sub`.
- JWT đã hợp lệ và chứa role `STUDENT`.
- Request validation đã hoàn tất.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | `full_name` | Full name | `VARCHAR` | `150` | `N/A` | `Y` | `blank` | `request["full_name"]` | Request body | `3.2` | Source-backed by `DB.sql`; blank normalization policy TBD. |
| 2 | `phone` | Phone | `VARCHAR` | `20` | `N/A` | `Y — contract` | `blank` | `request["phone"]` | Request body | `3.2` | Current schema allows `NULL`; contract requiredness is a discrepancy. |
| 3 | `avatar_url` | Avatar URL | `TEXT` | `N/A` | `N/A` | `TBD — contract literal avatar_url...:uri!` | `blank` | `request["avatar_url"]` | Request body | `3.2` | Current schema allows `NULL`; URI/requiredness semantics TBD. |
| 4 | `updated_at` | Updated time | `TIMESTAMP` | `N/A` | `N/A` | `Y` | `blank` | `current_timestamp` | Database clock/runtime | `3.2` | Must change with successful profile update. |

## Unmapped contract field

| Request field | Expected logical meaning | Physical column | Status | Decision required |
|---|---|---|---|---|
| `bio` | Biography | `N/A — users.bio absent from current DB.sql and ERD` | `SOURCE_REQUIRED` | Approve schema/contract mapping before adding SQL or migration. |

> Không đưa `bio` vào `UPDATE users` SQL. Không tự tạo column, migration, JSON fallback hoặc shadow storage.

## Insert mapping

**Áp dụng khi**

- `N/A — API #14 chỉ có UPDATE; không có INSERT được source xác nhận.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping INSERT giả. |

## Delete mapping

**Áp dụng khi**

- `N/A — API #14 không có DELETE được source xác nhận.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DELETE giả. |

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md`.
- Sheet logic: `table`.

