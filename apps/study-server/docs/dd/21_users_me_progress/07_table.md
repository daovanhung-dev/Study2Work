---
title: "Định nghĩa table"
order: 7
dd_id: "21"
api_name: "Lấy tiến độ tổng hợp"
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

- N/A — API #21 là GET và không có DB mutation.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Insert mapping

**Áp dụng khi**

- N/A — API #21 là GET và không có DB mutation.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Delete mapping

**Áp dụng khi**

- N/A — API #21 là GET và không có DB mutation.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Read-only API. |

## Read source note

DB design đánh dấu lesson_progress query cho API #21/#37 là DESIGN_ONLY. Query/API-specific projection không được định nghĩa tại sheet mutation template này; xem [05_Data_Mapping.md](./05_Data_Mapping.md).

---
## Phụ lục đối chiếu template Markdown

- Template: [07_table.md](../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md).
- Sheet nguồn: table.
