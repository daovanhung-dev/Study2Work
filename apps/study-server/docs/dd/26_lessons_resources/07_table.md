---
title: "Định nghĩa table"
order: 7
dd_id: "26"
api_name: "Lấy tài nguyên đính kèm"
source_sheet: "table"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `resources` — candidate, DESIGN_ONLY |
| Logical table | Attached learning resource |
| Operation | READ / SELECT candidate; query chưa được xác nhận |
| Data Mapping step | 2 |

## Candidate read mapping

| No | Physical column | Logical name | Type | Required in ERD | Required in checked-in DDL | Key/relation | Candidate setting / response relation | Source | Data Mapping step | Remarks |
|---:|---|---|---|---|---|---|---|---|---:|---|
| 1 | `id` | Resource ID | `BIGSERIAL` | Yes | Yes | Primary key | Candidate `Resource.id`; API #26 does not declare Resource response. | ERD V1 / DB.sql | 2 | Design-only; query projection not confirmed. |
| 2 | `lesson_id` | Lesson ID | `BIGINT` | Yes | No — DDL omits `NOT NULL` | FK candidate → `lessons.id` | Candidate filter/source relationship; exact query not confirmed. | ERD V1 / DB.sql | 2 | ERD and DDL differ on nullability. |
| 3 | `name` | Resource name | `VARCHAR(200)` | Yes | Yes | N/A | Candidate `Resource.name`; not bound to API #26 response yet. | ERD V1 / DB.sql | 2 | Projection/cardinality unresolved. |
| 4 | `resource_type` | Resource type | `VARCHAR(20)` | Yes | Yes | N/A | Candidate alias to reusable `Resource.type`. | ERD V1 / DB.sql | 2 | Allowed enum values not specified. |
| 5 | `url` | Resource URL | `TEXT` | Yes | Yes | N/A | Candidate source for reusable `Resource.url`. | ERD V1 / DB.sql | 2 | Raw/stored/signed URL rule unresolved. |
| 6 | `created_at` | Creation time | `TIMESTAMP` | Yes | Yes | N/A | Not declared in reusable `Resource` response schema. | ERD V1 / DB.sql | 2 | No response mapping inferred. |

## Update mapping

**Áp dụng khi**

- `N/A — READ-ONLY API; không có UPDATE.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation mapping. |

## Insert mapping

**Áp dụng khi**

- `N/A — READ-ONLY API; không có INSERT.`

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A | No mutation mapping. |

## Delete mapping

**Áp dụng khi**

- `N/A — READ-ONLY API; không có DELETE.`

| No | Target column | Operator | Value source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---|
| N/A | N/A | N/A | N/A | N/A | No mutation mapping. |

## Source note

- `resources` fields above are design evidence from ERD V1 and checked-in `DB.sql`, not verified live schema or API #26 query.
- Reusable `Resource.visibility` has no corresponding column in the ERD/DDL.
- `resources.lesson_id` is nullable in checked-in DDL despite required relation in ERD.
- API #26 response type remains catalog `Lesson`; resource columns are not claimed as `data` fields.

