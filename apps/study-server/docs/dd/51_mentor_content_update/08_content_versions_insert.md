---
title: "Định nghĩa table"
order: 8
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "table"
format: markdown
dd_id: "51"
api_name: "Cập nhật nội dung Mentor"
status: "Draft — Needs Confirmation"
---

# Định nghĩa table — `content_versions` snapshot insert

## Table metadata

| Thuộc tính | Giá trị |
|---|---|
| Physical table | `content_versions` |
| Logical table | Legacy Content history snapshot |
| Operation | INSERT |
| Data Mapping step | 4 |
| Evidence | Migration 007 and legacy `DB.sql` added for API #51 fallback. |
| Status | DERIVED schema proposal; live migration is unverified. |

## Update mapping

- N/A — API #51 updates `contents` in a separate mapping sheet.

## Insert mapping

**Áp dụng khi**

- Direct-owner check passed and current `contents` row is locked.

| No | Item ID / Column | Item name | Type | Length | Scale | Required | Main key | Setting content | Source | Data Mapping step | Remarks |
|---:|---|---|---|---:|---:|---:|---|---|---|---|---|
| 1 | `content_id` | Content ID | BIGINT | N/A | N/A | Y | ● | Locked `contents.id` | Query Q1 | 4 | Composite primary key part. |
| 2 | `version_no` | Archived version number | BIGINT | N/A | N/A | Y | ● | `COALESCE(MAX(version_no), 0) + 1` for Content | Existing snapshots | 4 | Content row lock serializes API #51 writes. |
| 3 | `course_id` | Course ID | BIGINT | N/A | N/A | Y |  | Locked Content value | Query Q1 | 4 | Composite FK to current Content identity. |
| 4 | `content_type` | Content type | TEXT | N/A | N/A | Y |  | Locked current value | Query Q1 | 4 | Snapshot before replacement. |
| 5 | `title` | Title | TEXT | N/A | N/A | Y |  | Locked current value | Query Q1 | 4 | Snapshot before replacement. |
| 6 | `payload` | Content payload | JSONB object | N/A | N/A | Y |  | Locked current value | Query Q1 | 4 | Object check mirrors `contents`. |
| 7 | `status` | Prior status | TEXT | N/A | N/A | Y |  | Locked current value | Query Q1 | 4 | Snapshot only; current status later becomes PENDING_REVIEW. |
| 8 | `parent_id` | Parent ID | BIGINT | N/A | N/A | N |  | Locked current value | Query Q1 | 4 | Nullable; composite FK retains same-course relation. |
| 9 | `content_order` | Content order | INTEGER | N/A | N/A | Y |  | Locked current value | Query Q1 | 4 | Preserves prior tree placement. |
| 10 | `archived_by` | Superseding Mentor ID | BIGINT | N/A | N/A | Y |  | Numeric JWT subject | Auth guard | 4 | Actor performing next update; not original author. |
| 11 | `archived_at` | Snapshot record time | TIMESTAMPTZ | N/A | N/A | Y |  | Database `CURRENT_TIMESTAMP` default | DDL | 4 | Records archive time, not original version creation time. |

## Delete mapping

- N/A — API #51 does not delete snapshots.

## SQL mapping

The insert copies the locked row into a history snapshot and computes the next archive number while holding the Content row lock. The snapshot and the current `contents` UPDATE commit or roll back together. Existing pre-migration history is unavailable; the first successful API #51 update creates the first snapshot.

`archived_by` records the actor who superseded the snapshot. `contents` has no original-author field, so this column must not be interpreted as author provenance for AC-33.

