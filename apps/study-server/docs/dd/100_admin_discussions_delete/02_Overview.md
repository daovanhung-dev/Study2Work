---
title: "Overview"
order: 2
dd_id: "100"
api_name: "Xóa discussion theo policy"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #100 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-37 |
| Method | DELETE |
| Endpoint | `/api/v1/admin/discussions/{discussion_id}` |
| Purpose | Soft-delete một discussion theo quyết định của Admin và giữ audit trail. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin là DIRECT theo catalog; guard/claim policy chưa có trong Study source. |
| Direct request | Path `discussion_id:int64!`; không body/query. |
| Direct response | HTTP 200 `ApiEnvelope<DeleteResult>`. |
| Direct errors | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 404 `DESIGN_RESOURCE_NOT_FOUND`; 422 `DESIGN_VALIDATION_ERROR`; 500 `DESIGN_INTERNAL_ERROR`. |
| AC-37 position | Sau #99 và quyết định “Cần xóa nội dung?”; sau đó reload moderation queue. |
| Runtime state | `UNWIRED / NOT_FOUND`; chưa có route/module/test #100. |
| Side effects | Soft delete + preserve audit trail là logical effect DIRECT; physical mapping và audit append policy chưa rõ. |
| Transaction | `TBD`; chưa có nguồn xác nhận update/audit atomicity. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — #100, `ApiEnvelope`, `DeleteResult`.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và AC-37 mapping.
- [AC-37 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — nhánh #97 → #98 → #99 → optional #100; soft delete + preserve audit trail.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) và [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate `discussions`; không chứng minh live schema.
- [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql) — UUID-based audit structures; không chứng minh mapping sang Discussion BIGINT.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py) — current route/auth/error boundary.
- DD [#97 queue](../97_admin_discussions_reported/00_Cover.md), [#98 detail](../98_admin_discussions_detail/00_Cover.md), [#99 moderation](../99_admin_discussions_moderate/00_Cover.md) — connected AC-37 contracts and unresolved fields.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope/error convention.

## Tables read

| Relation/source | Purpose | Basis/status |
|---|---|---|
| Legacy `discussions` | Candidate target lookup and soft-delete state | `id`, `status`, `updated_at` exist in legacy DDL; live schema unverified. |
| Logical audit trail | Preserve moderation history | AC-37 direct logical requirement; physical relation/key/source `SOURCE_REQUIRED`. |
| Pilot `admin_adjustments` / `audit_events` | Compare available audit design | UUID target/resource IDs; not mapped to legacy Discussion BIGINT. |
| Admin principal | Authorize deletion and identify actor | Role Admin direct from catalog; JWT claims and actor mapping unresolved. |

## Tables write

| Logical target | Intended effect | Basis/status |
|---|---|---|
| Discussion | Mark as deleted while retaining its row | AC-37 direct soft-delete behavior; physical marker/token `SOURCE_REQUIRED`. |
| Existing audit trail | Preserve existing records | AC-37 direct; retention/immutability source not identified for this entity. |
| Delete audit event | Whether to append a new event | Not stated by AC-37 #100; `SOURCE_REQUIRED`. |

## Mục chú ý

- `DeleteResult.status` is the literal `"deleted"`; it does not define the stored Discussion status token.
- Legacy `discussions.status` is nullable `VARCHAR(20)` with default `ACTIVE`; no approved `DELETED` token exists.
- `DeleteResult.deleted_at` is required, while legacy `discussions` has no dedicated delete timestamp. Mapping it from `updated_at` is only `DERIVED`.
- Diagram does not specify whether replies/reports are also hidden, whether deleting an already deleted row returns 404, or whether #99 moderation must precede #100.
- Catalog includes 422 but does not state which request condition produces it.

## Assumptions

- `status='DELETED'` and using `updated_at` as the response delete time are candidate `DERIVED` proposals only; neither is approved persistence behavior.
- Soft delete means no physical DELETE of the `discussions` row; no cascade is inferred.

## Conflicts

| Conflict | Expected behavior | Current/source evidence | Status |
|---|---|---|---|
| Soft-delete persistence | AC-37 says soft delete | Legacy status exists but approved token/transition is absent | `DISCREPANCY / SOURCE_REQUIRED` |
| Delete timestamp | Response requires `deleted_at` | Legacy DDL has `updated_at`, no `deleted_at` | `DISCREPANCY / DERIVED` |
| Audit mapping | Preserve audit trail | Legacy discussion DDL has no audit relation; pilot IDs are UUID | `DISCREPANCY / SOURCE_REQUIRED` |
| Admin authorization | Catalog requires Admin | Shared Study guard currently validates Student | `DISCREPANCY / SOURCE_REQUIRED` |
| Thread/report visibility | AC-37 says delete content | No cascade or queue predicate defined | `SOURCE_REQUIRED` |

## Security note

Only an authenticated Admin may perform the operation per catalog. Current Study source has no Admin guard or claim policy. Do not claim the actor is recorded until principal-to-audit identity mapping is approved.

## Performance note

Target lookup/update should be scoped by `discussion_id`; exact query, lock, retry and transaction rules are not established by source evidence.
---
## Phụ lục đối chiếu nguồn Excel
- Workbook nguồn: `DD_API_Template(1).xlsx`
- Sheet nguồn: `Overview`
- Dimension: `A1:BA10`
- Trạng thái: `visible`
- Số ô có dữ liệu/công thức: `4`
- Số vùng merge: `0`

<details>
<summary>Bản ghi từng ô có dữ liệu hoặc công thức</summary>

| Hàng | Ô | Giá trị nguồn | Công thức nguồn |
|---:|---|---|---|
| 1 | `A1` | 【Khái quát】 |  |
| 3 | `B3` | Get thông tin…. |  |
| 5 | `A5` | 【Mục chú ý】 |  |
| 7 | `B7` | Không có |  |

</details>
