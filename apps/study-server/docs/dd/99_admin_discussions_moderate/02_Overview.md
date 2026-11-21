---
title: "Overview"
order: 2
dd_id: "99"
api_name: "Điều chỉnh trạng thái kiểm duyệt discussion"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | #99 |
| Module | ADMIN / SYSTEM MANAGEMENT — AC-37 |
| Method | PATCH |
| Endpoint | `/api/v1/admin/discussions/{discussion_id}/moderate` |
| Purpose | Cập nhật quyết định moderation cho một discussion do Admin chọn. |
| Consumer/Actor | Admin |
| Authentication | Bearer JWT |
| Authorization | Role Admin là DIRECT theo catalog; Admin guard, claims và permission policy chưa có trong Study source. |
| Direct path | `discussion_id:int64!`. |
| Direct body field | `action:string!`. |
| Direct body field | `reason:string!`. |
| Query | Không khai báo. |
| Direct response | HTTP 200 `ApiEnvelope<Page<Discussion>>`. |
| Direct errors | 5 catalogued; xem [06_Error.md](./06_Error.md). |
| AC-37 step | Sau #98, Admin đánh giá vi phạm → #99 cập nhật moderation state + audit → quyết định có chuyển sang #100 xóa hay kết thúc. |
| Runtime state | `UNWIRED / NOT_FOUND`; chưa có route/module/test #99. |
| Side effects | AC-37 yêu cầu cập nhật moderation state và audit; physical mapping, atomicity và transition chưa được xác nhận. #99 không xóa discussion. |
| Transaction | TBD; chưa có nguồn xác nhận state update và audit append phải atomic hay cách rollback. |

## Sources

- [API catalog và reusable schemas](../../../../../docs/lists/list_api.md) — row #99 và `Page`, `PageMeta`, `Discussion`, `DiscussionComment`, `UserSummary`.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — actor, precondition, postcondition và mapping AC-37.
- [AC-37 activity diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #97 queue → #98 detail → decision → #99 state + audit → optional #100 delete.
- [DD #97 reported queue](../97_admin_discussions_reported/02_Overview.md) and [request](../97_admin_discussions_reported/03_Request.md) — query `reason` is a report filter and differs from the #99 action reason.
- [DD #98 detail](../98_admin_discussions_detail/00_Cover.md) and [open questions](../98_admin_discussions_detail/OPEN_QUESTIONS.md) — report relation/response, path grain, Discussion projection and Page gaps.
- [API #42 discussion detail](../42_discussions_detail/00_Cover.md) — one-item Page precedent; proposal only for #99.
- [DB table guide](../../diagrams/DB_UNICA_TABLES.md) and [legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — candidate Discussion columns; not live-schema evidence.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID-based `admin_adjustments` and `audit_events`; not selected as #99 physical persistence.
- [Current router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), and [response helper](../../../app/core/responses.py) — current route/auth/error boundary.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope and expected error-data convention.

## Tables read

| Relation/source | Purpose | Basis/status |
|---|---|---|
| Logical discussion moderation state | Apply Admin decision to selected target | AC-37 logical update; physical relation/column/enum/transition `SOURCE_REQUIRED`. |
| `discussions` | Candidate Discussion lookup and response projection | Legacy DDL candidate; BIGINT IDs, nullable course/user FKs, no title; live schema unverified. |
| Logical moderation audit | Preserve actor/action/reason and decision history | AC-37 audit requirement; physical relation/keys/fields `SOURCE_REQUIRED`. |
| Pilot `admin_adjustments` / `audit_events` | Compare available design artifacts | UUID/versioned subject/resource identifiers; not compatible by evidence with legacy BIGINT Discussion ID. |
| Admin principal | Determine role and audit actor | Admin role direct from catalog; JWT claims and identity mapping unresolved. |

## Tables write

| Logical target | Intended effect | Basis/status |
|---|---|---|
| Discussion moderation state | Update according to selected action | AC-37 direct logical effect; physical column and allowed transition unresolved. |
| Moderation audit | Record the action and reason | AC-37 direct logical effect; physical table/fields and atomicity `SOURCE_REQUIRED`. |
| Discussion deletion | None in #99 | Separate decision and API #100 in AC-37. |

## Mục chú ý

- Body `action` and `reason` are required strings. Catalog does not state enum tokens, case, blank handling, lengths, or taxonomy.
- AC-37 labels the logical choices ẩn/khóa/cảnh báo; proposal tokens such as `hide`, `lock`, `warn` remain `DERIVED`, not accepted values.
- `reason` in #99 explains a moderation action; it is not the #97 optional report-reason query filter.
- Catalog response is `Page<Discussion>` although request has no page/size. A one-item page can be proposed from #42/#98 precedent but needs confirmation.
- Reusable `Discussion.title` is required but legacy DB guide/DDL has no `title`. `course_id` and `user_id` are nullable in legacy DDL.
- Current shared auth helper requires Student, and the middleware design-code path allowlist excludes #99. These are current-source integration gaps, not #99 runtime behavior.
- The report details requested by AC-37 elsewhere do not appear in #99 response schema; do not add fields.
- Study API DD output is Markdown-only; no ZIP is part of this deliverable.

## Assumptions

- Treat state update and audit as logical operations from AC-37, without selecting physical targets.
- Retain `Page<Discussion>` exactly. Any one-item pagination values are `DERIVED` and unresolved.
- No new business code, field, table, column, state, validation constraint, DELETE, or transaction guarantee is introduced.

## Conflicts

| Conflict | Expected behavior | Current/source evidence | Status |
|---|---|---|---|
| Moderation state persistence | AC-37 requires state update | Legacy `discussions.status` is VARCHAR(20) default ACTIVE; exact action mapping absent | `DISCREPANCY / SOURCE_REQUIRED` |
| Audit persistence | AC-37 requires audit | No legacy audit table; pilot audit schemas use UUID/versioned identifiers | `DISCREPANCY / SOURCE_REQUIRED` |
| Discussion response completeness | Catalog requires Discussion | Legacy schema lacks required title and has nullable course/user IDs | `DISCREPANCY` |
| Admin authentication | Catalog requires Admin | Shared Study guard only accepts Student | `DISCREPANCY / SOURCE_REQUIRED` |

## Security note

Only an authenticated Admin may perform the moderation action per catalog. The current Study source does not provide an Admin guard or claim policy. Audit must not be claimed complete until actor identity, reason handling, retention and physical persistence are approved.

## Performance note

Target lookup and mutation should be scoped to `discussion_id`; exact query, locking, idempotency and audit transaction behavior are unresolved. No performance target is specified.

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
