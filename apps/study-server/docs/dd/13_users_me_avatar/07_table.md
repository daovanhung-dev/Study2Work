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

## External storage mapping

| Thuộc tính | Giá trị |
|---|---|
| Provider | `S3-compatible Object Storage` |
| Object key | `avatars/{user_id}` |
| Content-Type | MIME đã kiểm tra: `image/png`, `image/jpeg` hoặc `image/webp` |
| Public URL | `OBJECT_STORAGE_PUBLIC_BASE_URL + /avatars/{user_id}` |
| Overwrite | Upload mới của cùng user ghi đè object hiện tại |
| Retry | `N/A — tối đa một attempt` |
| Cleanup | `N/A — không có cleanup riêng` |

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

> Object Storage upload là external behavior; không tự chuyển thành DB table/column mapping.

---
## Phụ lục đối chiếu template Markdown

- Template: `../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md`.
- Sheet logic: `table`.
