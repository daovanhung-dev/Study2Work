---
task_id: "2026-11-07-design-study-screen-ad11"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-33; AD-10 → AD-11; APIs #79–#81"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-11

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 216; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Separate expected/current behavior; preserve original assets; trace auth/data/errors; keep Study Web UNWIRED unless editable source proves wiring; do not claim tests/runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve Admin permission, PII, lifecycle and live-schema blockers; do not infer fields/actions from prototype; source and fake-DB evidence are distinct.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Keep identity handoff numeric and source-backed; do not infer privacy or identity policy from mockup; keep API-DD and runtime statuses distinct.
- additional_cross_screen_review: `.agents/worklog/2026-11-07/design-study-screen-ad10.md`
  - carry_forward: AD-10→AD-11 candidate handoff is `Content.id` to `content_id`; local #79 returns only eight Content fields and lacks author/version; #80/#81 revision identity, stale-item behavior, moderation permission and live schema remain open; Study Web is UNWIRED.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Objective: complete AD-11 only, preserving assets; create the per-screen plan before markers/annotation/DD; write A–F with one C row per marker; update inventory, reverse API source index, global checkpoint and this worklog; record blockers without inventing policy.
- Inventory row 69: route proposal `/admin/content/:contentId/review`, AC-33, APIs #79/#80/#81; expected detail, approve or reject with reason, then refresh #78; linked to AD-10. Current tracker had D and approval-vs-publish blocker.
- AC-33 expected flow: queue #78 → detail/content/version/author #79 → decision #80 or #81 → reload queue. Diagram node #9 says `APPROVED/PUBLISHED + audit`; preserve discrepancy against local #80 `APPROVED`.
- Catalog: #79 GET path int64 → `ApiEnvelope<Content>`; #80 PATCH path-only → `ApiEnvelope<Content>`; #81 PATCH path + `{reason:string!}` → `ApiEnvelope<Content>`. Bearer/Admin. #79 errors 401/403/404/500; #80/#81 additionally 422.

## CURRENT_BEHAVIOR

- Target folder has source `screen.png` (1566×1600) and `code.html`; hashes after authoring: PNG `3286eafc27d61cad5c1b7f09da9a55d7c5340d0ca6a91ea4cd1c20d11d962ee0`; HTML `200e72fc09e370b5735bfe53d33c40f2562543ceed0c682c9d0ef97c5fa761d9`.
- Prototype is static: hash anchors/no route, back-to-AD-10 anchor, no notification handler, disabled approve/reject, disabled reason textarea, no application fetch/XHR/API/media/timer handler. It shows empty preview, metadata placeholders, static lock/renderer/rubric claims, three checked criteria but `0/3 loaded` progress.
- Study Web editable source/package/router/client is absent from current checkout; runtime `UNWIRED` / `NOT VERIFIED`.
- Current route/source: `apps/study-server/app/api/v1.py` registers #79–#81; focused modules and tests exist. #79 reads one active Content row and returns direct eight-field projection; no author/version/course title/submission time, no revision selector, no status predicate. #80 locks active pending row and commits `PENDING_REVIEW→APPROVED` plus one audit candidate with actor/status and NULL reason. #81 strict required string body, locks pending row, commits `PENDING_REVIEW→REJECTED` plus one decision/audit candidate with the exact reason. Empty string is accepted. No revision token/idempotency key; current row is assessed when mutation executes.
- Current local error behavior: #79 malformed/overflow ID→404, missing/deleted→404, query/projection→safe 500/rollback. #80/#81 malformed/overflow path→422, missing/deleted→404, nonpending→422, transaction/projection failure→safe 500/rollback. #81 body validation occurs in FastAPI before view/auth. Shared role `ADMIN` does not prove fine-grained moderation permission.
- Migration 011 is a checked-in BIGINT audit schema candidate; local fake-DB tests do not prove PostgreSQL, migration deployment, grants or live behavior. Mentor #52 separately handles `APPROVED ↔ PUBLISHED`.

## SOURCE_TRACE

```text
Expected: AD-10/#78 selection → candidate Content.id to contentId → GET #79
          → PATCH #80 or #81(reason) → AC-33 reload #78.
Current: Study Web has no caller. #79 reads current active logical Content;
         #80 sets APPROVED; #81 sets REJECTED and stores reason. No revision
         identity ties the detail read to either mutation.
```

Reviewed direct evidence:
- Inventory: `apps/study-client/docs/list_screen.md` rows 68–69 and reverse API index rows 078–081.
- Design plan and adjacent screen: `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; AD-10 plan/DD/worklog.
- AC/catalog: `apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md`; `AC_04_ADMIN_MANAGEMENT.drawio`; `docs/lists/list_api.md` #79–#81.
- API DDs: `apps/study-server/docs/dd/79_admin_content_detail/`; `80_admin_content_approve/`; `81_admin_content_reject/` (all Draft, read for contract/source boundaries).
- Runtime/source: `apps/study-server/app/api/v1.py` lines 2054–2183; modules `api_79_admin_content_detail`, `api_80_admin_content_approve`, `api_81_admin_content_reject` (models/validate/query/view).
- Focused test source reviewed (not run): `apps/study-server/tests/modules/admin/api_79_admin_content_detail/test_admin_content_detail.py`; `.../api_80_admin_content_approve/test_admin_content_approve.py`; `.../api_81_admin_content_reject/test_admin_content_reject.py`.
- Adjacent publication/schema/security: `apps/study-server/app/modules/mentor/api_52_mentor_content_publish/{query.py,view.py}`; `.agents/server-study/core/database-security.md`; `infra/postgres/study-server/migrations/011_content_review_audit_logs.sql`.
- Router/context/registry: root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, project dependency/contracts pages, Web/Study Web context and Server Study scope pages. Registry has no canonical UI-only DD skill; `createDD-markdown` excludes web-UI-only DD.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Approval vs publish | AC diagram says `APPROVED/PUBLISHED`; #80 catalog/local source says `APPROVED`; Mentor #52 is separate publication transition. | `DISCREPANCY` | UI must not claim published after #80; semantics/CTA owner decision required. |
| Rejection reason | #81 catalog requires `reason`; prototype labels optional and disables field; local schema accepts empty string and preserves text. | `DISCREPANCY` | Form cannot fulfill API while disabled; blank/length/format rule open. |
| Metadata/preview | AC asks author/version; #79 returns only eight Content fields; no media locator/decoder or rubric API. | `BLOCKED` | Do not fabricate author/version/media/rubric results. |
| Revision/stale item | #79–#81 use logical ID only; no version/expected-row token; #79 can return any active status. | `OPEN` | Read/decision continuity and conflict policy unresolved. |
| Authorization/schema | Shared `ADMIN`, migration 011/legacy BIGINT checked in, tests fake DB. | `NOT_VERIFIED` | Dedicated moderation permission, live schema/deployment/grants/retention not established. |
| Frontend/runtime | No editable Study Web source/router/API client. | `UNWIRED` | All prototype behavior remains static. |

## CHANGES

- Added `apps/study-client/docs/screen_stitch/05_admin/AD-11_duyet-tu-choi-noi-dung/AD-11_PLAN.md` before markers and DD.
- Added `AD-11_markers.json` and `AD-11_markers.svg` with 48 numbered elements; rendered `screen_annotated.png` at 3132×3200 (2×). Original image/HTML preserved.
- Added `AD-11.md`, sections A–F, 48 element rows, EV-01…EV-08, API mapping/errors, state/navigation, acceptance and blockers.
- Updated AD-11 inventory and reverse API #079–#081 source status from D→R in `apps/study-client/docs/list_screen.md`; API DD statuses remain Draft.
- Updated AD-11 row and appended 64/83 checkpoint to `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- `CONTEXT_UPDATES`: none; no context page or contract source changed.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Goal/router/context/worklog preflight | Objective file, router, context map and worklog process reviewed; selector READY 3/216; AD-01/02/03 selected worklogs and adjacent AD-10 worklog read. | VERIFIED |
| Scope and registry | Project boundary, Web/Study Web and Server Study context reviewed; no canonical UI-only DD skill is wired. | VERIFIED |
| Contract/source review | AC-33, catalog #79–#81, API DDs, router/modules, focused test source, security context, migration and Mentor #52 source inspected. Tests/runtime not run. | VERIFIED (STATIC SOURCE REVIEW) |
| Source asset preservation | SHA-256 remained `3286eafc…d962ee0` PNG and `200e72fc…fa761d9` HTML; PNG 1566×1600. | VERIFIED |
| Markers/annotation | 48 sequential unique JSON/SVG groups; coordinates match; radius+stroke bounds in source; C rows 48/48; annotated image 3132×3200, visually inspected. | VERIFIED |
| Links/tracker/count | 12 local DD links resolve; 83 unique inventory IDs match 83 folders; 64/83 four-core-artifact sets; #079–#081 and AD-11 rows show R/source evidence. | VERIFIED |
| Whitespace | `git diff --check` on updated tracked trackers passes; new DD/plan/JSON/SVG trailing-whitespace/final-newline audit passes. | VERIFIED |
| Application tests/runtime | Not run by instruction. | NOT_RUN |

## HANDOFF

- AD-11 DD artifacts and tracker update are complete for this session. `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, `RUNTIME NOT VERIFIED` remain separate statuses.
- Remaining blockers: approval/publish semantics; required/blank reason policy; author/version/revision/media/rubric source; stale decision/permission policy; live schema/migration deployment; Study Web implementation.
- Next screen in the Admin sequence is AD-12, for a separate session. Overall 83-screen goal remains active.
