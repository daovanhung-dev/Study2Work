---
title: "Định nghĩa table"
order: 7
dd_id: "22"
api_name: "Kiểm tra quyền truy cập lesson"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | N/A — READ-ONLY API |
| Logical table | N/A — READ-ONLY API |
| Operation | N/A — SELECT only; no INSERT/UPDATE/DELETE mapping |
| Data Mapping step | 2 |

## Update mapping

**Áp dụng khi**

- N/A — API #22 là GET và không có DB mutation được mô tả.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Insert mapping

**Áp dụng khi**

- N/A — API #22 là GET và không có DB mutation được mô tả.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Delete mapping

**Áp dụng khi**

- N/A — API #22 là GET và không có DB mutation được mô tả.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Read source note

Candidate design reads from `lessons` and `enrollments`; exact query and access predicate are unresolved. See [05_Data_Mapping.md](./05_Data_Mapping.md). This sheet documents mutation mapping only; it does not assert runtime table access.

---
## Phụ lục đối chiếu template Markdown

- Template: [07_table.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md).
- Sheet nguồn: table.
