---
title: "Định nghĩa table"
order: 7
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | courses; enrollments |
| Logical table | Course và enrollment status lookup |
| Operation | N/A — read-only API |
| Data Mapping step | 2.1/2.2 — SELECT only |

## Update mapping

**Áp dụng khi**

- N/A — API #15 không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo mapping UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- N/A — API #15 không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo mapping INSERT giả. |

## Delete mapping

**Áp dụng khi**

- N/A — API #15 không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Không tạo mapping DELETE giả. |

> Hai bảng chỉ được đọc. Identity selection gap không được giải quyết bằng cách tạo column, index, view hoặc mutation mới.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md.
- Sheet logic: table.
