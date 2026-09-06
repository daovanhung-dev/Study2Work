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
| Physical table | `resources; lessons; courses` |
| Logical table | `Resource metadata, lesson relation và published-course visibility` |
| Operation | `N/A — no DB mutation` |
| Data Mapping step | `3.1/3.3 — SELECT only` |

## Update mapping

**Áp dụng khi**

- `N/A — API #12 là read-only.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- `N/A — API #12 là read-only.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping INSERT giả. |

## Delete mapping

**Áp dụng khi**

- `N/A — API #12 là read-only.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DELETE giả. |

> Các bảng trên chỉ được đọc. Object Storage signer là external read/capability và không tạo DB mapping.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/07_table.md`.
- Sheet logic: `table`.
