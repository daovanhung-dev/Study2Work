---
title: "Overview"
order: 2
dd_id: "81"
api_name: "Từ chối nội dung"
source_workbook: "DD_API_Template(1).xlsx"
source_sheet: "Overview"
format: markdown
status: "Draft — Needs Confirmation"
---

# Overview

## Khái quát

| Thuộc tính | Giá trị |
|---|---|
| API ID | **#81** |
| Module | **ADMIN / SYSTEM MANAGEMENT — AC-33** |
| Method | **PATCH** |
| Endpoint | **/api/v1/admin/content/{content_id}/reject** |
| Purpose | Từ chối Content được chọn trong hàng đợi review và ghi nhận lý do theo AC-33. |
| Consumer/Actor | **Admin** |
| Authentication | **Bearer JWT** |
| Authorization | Shared Study guard requires role `ADMIN`; dedicated moderation permission remains unverified. |
| Basis | Method/path/auth/input/response/status/errors: **DIRECT**; `PENDING_REVIEW` eligibility, legacy reason mapping and atomicity: **DERIVED**. |
| Status | **Draft — Needs Confirmation**; implementation and HTTP tests exist locally, while business-rule owner approval and live DB remain unverified. |
| Transaction | Lock active Content, update status, insert one reason-bearing decision row, validate response, commit last. This transaction boundary is **DERIVED** from AC-33 and API #80/#76 patterns. |
| Side effects | Set active `contents.status` from `PENDING_REVIEW` to `REJECTED`; insert one `content_review_audit_logs` row carrying the submitted reason and actor. The same row persists the reason and records the decision; no second audit write is made. |

## Sources

- [API catalog và reusable Content schema](../../../../../docs/lists/list_api.md) — row #81, Content fields and exact errors.
- [AC/API index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) — AC-33 Admin actor, pending-review precondition and API sequence.
- [AC-33 moderation diagram](../../diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio) — #78 queue → #79 detail → reject branch with reason → #81 status/reason update → reload #78.
- [DD #78 queue](../78_admin_content_pending/02_Overview.md), [mapping](../78_admin_content_pending/05_Data_Mapping.md) and [open questions](../78_admin_content_pending/OPEN_QUESTIONS.md) — PENDING_REVIEW queue predicate, response cardinality and revision selection.
- [DD #79 detail](../79_admin_content_detail/02_Overview.md) and [open questions](../79_admin_content_detail/OPEN_QUESTIONS.md) — version/author read intent and stable revision identity gap.
- [DD #80 approve](../80_admin_content_approve/02_Overview.md) and [open questions](../80_admin_content_approve/OPEN_QUESTIONS.md) — separate approval status/audit effects and shared revision questions.
- [DD #52 publish/unpublish](../52_mentor_content_publish/02_Overview.md) and [DD #53 delete](../53_mentor_content_delete/02_Overview.md) — Content lifecycle interactions still proposed.
- [Legacy Study DDL](../../../../../infra/postgres/study-server/DB.sql) — legacy BIGINT `contents`; [migration 011](../../../../../infra/postgres/study-server/migrations/011_content_review_audit_logs.sql) adds the #80 DERIVED audit candidate with nullable reason. API #81 currently reuses this candidate locally as a DERIVED mapping; live deployment and owner approval remain unverified.
- [V1-PILOT Study DDL](../../../../../infra/postgres/02_study_db.sql) — UUID content/review artifacts; not direct mapping for catalog Content int64.
- [Current Study router](../../../app/api/v1.py), [API #81 module](../../../app/modules/admin/api_81_admin_content_reject/), [focused tests](../../../tests/modules/admin/api_81_admin_content_reject/test_admin_content_reject.py), [auth helper](../../../app/utils/auth.py), [middleware](../../../app/core/middleware.py), [response helper](../../../app/core/responses.py) — current route, ADMIN guard, middleware path entry, test evidence and error envelope behavior.
- [API guidelines](../../../../../contracts/api-guidelines/README.md) — common envelope and expected error data:null convention.

## Tables read

| Logical/physical source | Purpose | Basis/status |
|---|---|---|
| Logical Content | Resolve the path-selected item and response projection | Runtime maps to checked-in legacy `contents` BIGINT candidate; live schema unverified. |
| Logical Content review state | Determine whether the item is still eligible for rejection | AC-33/#78 pending precondition direct; recheck as `PENDING_REVIEW` is DERIVED. |
| Logical Content revision | Bind rejection to the revision Admin saw in #79 | Revision identity/selector SOURCE_REQUIRED; runtime acts on active row locked at call time. |
| `contents` | Current legacy Content response/state candidate used by APIs #49–#53, #78–#81 | Checked-in BIGINT source; live schema unverified. |
| `content_review_audit_logs` | Store actor, previous/new status and rejection reason in one decision row | Migration 011's nullable reason column reused as a DERIVED #81 mapping; no live deployment proof. |
| Admin principal | Authorize the caller and identify the reviewer | Shared guard requires role ADMIN and supplies numeric JWT `sub`; mapping to legacy BIGINT actor is DERIVED, live identity/FK state unverified. |
| V1-PILOT content_review_decisions | Compare existing pilot decision artifact | UUID revision/reviewer model; not selected as physical source for #81. |

## Tables write

| Logical target | Intended effect | Basis/status |
|---|---|---|
| `contents.status` | Set active row to `REJECTED` from `PENDING_REVIEW` | Logical effect direct; pending gate and legacy physical mapping are DERIVED. |
| `content_review_audit_logs` | Insert one decision row with actor, old/new status and request reason | Reusing migration 011's nullable reason slot is a DERIVED mapping; this is one row, not a second separate event. |

## Mục chú ý

- Catalog declares path content_id:int64! and body reason:string!; no query parameters.
- No reason maximum length, trim rule, blank-value rule, enum or reason code list is declared. Runtime accepts an empty string because the catalog only requires a string.
- Catalog response is one Content with eight fields. It has no review_reason, reviewer, version or audit field; do not add any.
- AC-33 queue filters PENDING_REVIEW. After status becomes REJECTED, the item no longer satisfies that logical predicate and should be absent from the reloaded queue; this outcome follows the two direct diagram steps.
- #80 says “+ audit”; #81 says “+ review reason”. Do not silently add a separate audit write to #81.

## Assumptions

- A request body object is sent as application/json, following the catalog body schema and existing Study API DD convention.
- A successful Content projection reports the resulting logical status REJECTED; legacy `contents` is the local physical candidate, while live schema remains unverified.
- The required marker means reason must be present; whitespace-only/length/content policy is not inferred.

## Conflicts

- AC-33 asks to store a review reason, but the reusable Content response has no reason field. Runtime stores it in the decision row and does not return it; retention/client visibility remain unresolved.
- #80 explicitly writes audit; #81 writes one reason-bearing decision row as the DERIVED physical store for its direct reason effect. Whether a separate additional audit event is desired remains open; none is written.
- #78/#79/#80/#81 identify the target only by content_id; AC-33 detail reads version, so a stale revision can be acted upon without a version selector in the request.
- Legacy candidate `contents` and migration 011 audit relation use BIGINT; V1-PILOT review decisions remain UUID-based and do not map directly to Content int64. Live schema is unverified.
- Route/path is now present in the router and middleware allowlist; shared validation/unhandled errors use DESIGN codes and `data:null`. Local fake-session tests do not imply live DB behavior.

## Security note

Require Bearer JWT and shared role `ADMIN` before exposing or changing Content. Resolve actor from the authenticated principal; do not accept it from request data. Dedicated moderation permission remains unverified; numeric JWT `sub` to BIGINT audit actor mapping is DERIVED. Restrict reason/audit data to approved persistence and response projections.

## Performance note

The local #81 path locks an active legacy Content row and writes the status/reason decision in one transaction using migration 011's candidate relation. Runtime performance and live database indexing are unverified; the revision shown in #79 still has no request selector.
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
