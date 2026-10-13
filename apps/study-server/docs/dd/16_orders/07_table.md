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
| Physical table | SOURCE_REQUIRED — chưa có bảng Order trong schema nguồn |
| Logical table | Order |
| Operation | INSERT — logical flow only |
| Data Mapping step | 4 — Create logical Order |

## Update mapping

**Áp dụng khi**

- N/A — API #16 là create operation; không khai báo UPDATE.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo mapping UPDATE giả. |

## Insert mapping

**Áp dụng khi**

- AC-12 yêu cầu tạo logical Order ở trạng thái PENDING; mapping physical bị chặn do chưa có schema Order.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| SOURCE_REQUIRED | SOURCE_REQUIRED — physical column chưa xác định | Logical Order fields | SOURCE_REQUIRED | N/A | N/A | SOURCE_REQUIRED | SOURCE_REQUIRED | Không chốt column hoặc giá trị insert khi chưa có schema | AC-12 xác nhận logical Order = PENDING; API catalog khai báo response Order | 4 | Đây là gap marker, không phải DB column; xem [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md#q-16-01-order-persistence-schema) |

## Delete mapping

**Áp dụng khi**

- N/A — API #16 không khai báo DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Không tạo mapping DELETE giả. |

> ERD V1 và checked-in DB.sql không có bảng `orders`. Bảng `payments` là đối tượng riêng trong API #17; không dùng làm physical target thay thế.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md.
- Sheet logic: table.

