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
| Physical table | `N/A — upload-only; không có DB mutation` |
| Logical table | `N/A — Object Storage là external service, không phải DB table` |
| Operation | `N/A — không INSERT/UPDATE/DELETE/UPSERT` |
| Data Mapping step | `3.1 — external Object Storage upload` |

## Update mapping

**Áp dụng khi**

- `N/A — API #13 không cập nhật users.avatar_url hoặc bảng DB nào.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- `N/A — Object Storage upload không phải DB INSERT.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping INSERT giả. |

## Delete mapping

**Áp dụng khi**

- `N/A — API #13 không hard delete hoặc soft delete DB record.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| `N/A` | `N/A` | `N/A` | `N/A` | `N/A` | Không tạo mapping DELETE giả. |

> Object Storage upload, object key, cleanup và idempotency là external behavior; không tự chuyển thành DB table/column mapping.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../.agents/skills/create_dd/docs/dd/DD_API_Template_MD/07_table.md`.
- Sheet logic: `table`.
