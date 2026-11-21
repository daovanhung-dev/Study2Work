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
| Physical table | payments |
| Logical table | Payment |
| Operation | INSERT — design-only per DB_UNICA_TABLES |
| Data Mapping step | 4 — initiate/confirm payment; physical execution not wired |

## Update mapping

**Áp dụng khi**

- N/A — API #17 catalog không khai báo UPDATE mapping; gateway confirmation/state update chưa có nguồn xác nhận.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | Không tạo mapping UPDATE giả | N/A | N/A | Payment lifecycle update policy SOURCE_REQUIRED |

## Insert mapping

**Áp dụng khi**

- DB_UNICA_TABLES đánh dấu API #17 là INSERT/external payment ở DESIGN_ONLY; đây không phải SQL runtime hoặc xác nhận bảng đang tồn tại live.
- Mỗi dòng dưới đây là cột có trong checked-in DB.sql. Mapping giá trị INSERT chỉ được chốt khi nguồn ghi rõ; cột không có mapping được đánh dấu SOURCE_REQUIRED.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---:|---|---|---|---|
| 1 | id | Payment ID | BIGSERIAL | N/A | N/A | Yes — primary key | ● | Generated value/source at runtime SOURCE_REQUIRED | DB.sql:192 | 4 | Checked-in schema/design only |
| 2 | user_id | Student ID | BIGINT | N/A | N/A | DISCREPANCY |  | SOURCE_REQUIRED — caller/order owner mapping | DB.sql:193; DB_UNICA_TABLES.md:613 | 4 | DB.sql permits NULL; table doc says required |
| 3 | course_id | Course ID | BIGINT | N/A | N/A | DISCREPANCY |  | SOURCE_REQUIRED — physical Order mapping | DB.sql:194; DB_UNICA_TABLES.md:614 | 4 | DB.sql permits NULL; table doc says required |
| 4 | amount | Payment amount | NUMERIC | 12 | 2 | Yes in DB.sql |  | SOURCE_REQUIRED — amount source/calculation | DB.sql:195; DB_UNICA_TABLES.md:615 | 4 | Currency is absent from payments table |
| 5 | provider | Payment provider | VARCHAR | 50 | N/A | Yes in DB.sql |  | SOURCE_REQUIRED — request value/adapter mapping | DB.sql:196; DB_UNICA_TABLES.md:616 | 4 | Provider allowlist not defined |
| 6 | transaction_code | Provider transaction code | VARCHAR | 100 | N/A | No — nullable, UNIQUE |  | SOURCE_REQUIRED — gateway response | DB.sql:197; DB_UNICA_TABLES.md:617 | 4 | Exact source/meaning not defined |
| 7 | status | Payment status | VARCHAR | 20 | N/A | No — nullable in DB.sql |  | SOURCE_REQUIRED — PaymentStatus and initial transition | DB.sql:198; DB_UNICA_TABLES.md:618 | 4 | DB default PENDING; enum/use of default not confirmed |
| 8 | paid_at | Payment completion time | TIMESTAMP | N/A | N/A | No — nullable |  | SOURCE_REQUIRED — success confirmation time | DB.sql:199; DB_UNICA_TABLES.md:619 | 4 | Optional logical Payment field |
| 9 | created_at | Creation time | TIMESTAMP | N/A | N/A | Yes in DB.sql |  | SOURCE_REQUIRED — timestamp source | DB.sql:200; DB_UNICA_TABLES.md:620 | 4 | NOT NULL; no default declared |

> Logical Payment.order_id is required by the reusable API schema, but there is no payments.order_id column in DB.sql/ERD V1 and no physical orders table. Do not treat this note as a physical column mapping. See [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).

## Delete mapping

**Áp dụng khi**

- N/A — API #17 catalog không khai báo DELETE.

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|
| N/A | N/A | N/A | N/A | N/A | Không tạo mapping DELETE giả. |

> DB.sql và ERD V1 là design/schema evidence; live metadata chưa được xác minh. DB.sql cho phép NULL ở user_id/course_id, trong khi DB_UNICA_TABLES mô tả hai quan hệ này là bắt buộc. Giữ discrepancy, không tự sửa một nguồn.

---
## Phụ lục đối chiếu template Markdown

- Template: ../../../../../.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/07_table.md.
- Sheet logic: table.
