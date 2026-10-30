---
title: "Overview"
order: 2
dd_id: "80"
api_name: "Phê duyệt nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | **#80** |
| Module | **ADMIN / SYSTEM MANAGEMENT — AC-33** |
| Method | **PATCH** |
| Endpoint | **/api/v1/admin/content/{content_id}/approve** |
| Purpose | Phê duyệt Content được chọn trong hàng đợi moderation theo AC-33. |
| Consumer/Actor | **Admin** |
| Authentication | **Bearer JWT** |
| Authorization | Shared role-aware guard yêu cầu `ADMIN`; dedicated moderation permission chưa được xác minh. |
| Basis | Endpoint, path, response, error codes và status/audit intent: **DIRECT**; `APPROVED`, pending check, BIGINT audit mapping và atomic transaction: **DERIVED**. |
| Status | **Draft — Needs Confirmation**; implementation local có source/test nhưng contract owner và live DB chưa xác nhận. |
| Transaction | Lock, update, audit và response validation nằm trong một transaction; commit sau cùng. Đây là **DERIVED** theo pattern API #76. |
| Side effects | Đổi active Content `PENDING_REVIEW` → `APPROVED` và append audit. API #52 tiếp tục sở hữu publication transition `APPROVED` ↔ `PUBLISHED`. |

## Sources

- [API catalog và reusable Content schema](../../../../../docs/lists/list_api.md) — row #80, response fields và exact error set.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 Admin actor, pending-review precondition và sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #78 queue → #79 detail → decision → #80 approve → update status plus audit → reload queue.
- [AC-22 Mentor content diagram](../../diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) — separate API #52 updates publication status.
- [DD #78 queue](../78_admin_content_pending/02_Overview.md), [DD #79 detail](../79_admin_content_detail/02_Overview.md) and [DD #79 open questions](../79_admin_content_detail/OPEN_QUESTIONS.md) — pending state and version/author identity gaps.
- [DD #52 publish/unpublish](../52_mentor_content_publish/02_Overview.md) and [open questions](../52_mentor_content_publish/OPEN_QUESTIONS.md) — separate publication operation and unresolved interaction with Admin approval.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) and [migration 011](../../../../../infra/postgres/study-server/migrations/011_content_review_audit_logs.sql) — checked-in BIGINT `contents` and a DERIVED review-audit candidate; live migration is unverified.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID content/version/decision artifacts; not a direct BIGINT Content mapping.
- [Current Study router](../../../app/api/v1.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py) and [response helper](../../../app/core/responses.py) — API #80 route, shared Admin guard, path allowlist and error envelope behavior.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope and expected error data=null convention.

## Tables read

| Logical/physical source | Purpose | Basis/status |
|---|---|---|
| `contents` | Resolve the active path-selected item and eight response fields | Checked-in legacy BIGINT candidate; live schema unverified. |
| Content review state | Check that the item is eligible for approval | AC-33/#78 pending precondition; require `PENDING_REVIEW` as a DERIVED check. |
| Logical Content revision | Keep the decision bound to the version shown in #79 | Revision identity and selector SOURCE_REQUIRED. |
| Admin principal | Determine role and audit actor | Shared `ADMIN` guard returns numeric JWT `sub`; legacy BIGINT FK mapping is DERIVED. |
| V1-PILOT content_review_decisions | Compare available pilot decision artifact | UUID revision/reviewer model; not selected as #80 physical source. |

## Tables write

| Logical target | Intended effect | Basis/status |
|---|---|---|
| `contents.status` | Set active row to `APPROVED` | Legacy candidate; target chosen as DERIVED intermediate before API #52 publication. |
| `content_review_audit_logs` | Append actor, old/new status, nullable reason and recorded time | Migration 011 is a DERIVED BIGINT candidate; append is atomic with the status write. |

## Mục chú ý

- Catalog #80 declares path content_id:int64! only; it has no body/query, revision ID or expected row version.
- AC-33 says APPROVED/PUBLISHED in one node; implementation selects `APPROVED` as the intermediate state because current API #52 publishes from `APPROVED`. The selection remains DERIVED.
- Catalog response is one Content with eight fields. AC-33 detail also reads version/author, but reusable Content schema contains neither; do not add fields.
- Catalog allows 422 DESIGN_VALIDATION_ERROR but does not define its trigger.
- Malformed/out-of-range signed-int64 path returns catalog 422; an active row outside `PENDING_REVIEW` also returns catalog 422.
- Study workflow delivers Markdown only; this package has no ZIP.

## Assumptions

- Use checked-in legacy `contents` with BIGINT ID and add migration 011 `content_review_audit_logs` as a DERIVED physical fallback; neither proves live availability.
- Use `PENDING_REVIEW` eligibility and target `APPROVED`; keep the status choice derived from AC-33 and current API #52 behavior.
- Response uses the current shared envelope (`meta: {}` on success, `data: null` on errors) and the direct eight-field Content schema.

## Conflicts

- AC-33 approve effect APPROVED/PUBLISHED is ambiguous beside AC-22 API #52 publication update.
- AC-33 reads version/author but #80 request and response do not identify or return a revision/author.
- V1-PILOT decision rows use UUID resource_version_id and cannot map directly to Content int64; the legacy BIGINT audit candidate is local DERIVED schema only.
- `contents` has no revision selector. API #80 acts on the active row locked at call time, which cannot prove continuity with the revision displayed by #79.

## Security note

Require Bearer JWT and shared `ADMIN` role before path validation or DB access. Bind the authenticated numeric JWT `sub` as audit actor; never accept actor identity from request data. Return only the reusable Content response allowlist, without audit or revision metadata.

## Performance note

The view locks one active Content row and updates/records one audit event. The audit indexes are DERIVED for Content/actor history lookups; they do not prove deployed performance. The exact revision shown earlier in #79 remains unbound.
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
