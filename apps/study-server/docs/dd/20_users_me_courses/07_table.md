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
| Physical table | enrollments; courses |
| Logical table | Enrollment và Course |
| Operation | N/A — READ-ONLY API |
| Data Mapping step | 2.1/2.2 — SELECT only |

## Update mapping

**Áp dụng khi**

- N/A — API #20 không có UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo mapping UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- N/A — API #20 không có INSERT.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---:|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo mapping INSERT giả. |

## Delete mapping

**Áp dụng khi**

- N/A — API #20 không có DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Không tạo mapping DELETE giả. |

> AC-13 và DB docs hỗ trợ quan hệ đọc Enrollment/Course ở mức design. Query projection, filter, pagination và mapping UserProfile chưa được chốt. Không tạo mutation hoặc schema change.

---
## Phụ lục đối chiếu template Markdown

- Template: [07_table.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md).
- Sheet nguồn: table.
