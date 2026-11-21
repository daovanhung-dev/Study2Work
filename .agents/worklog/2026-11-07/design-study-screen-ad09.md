---
task_id: "2026-11-07-design-study-screen-ad09"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-32 AD-06/AD-07 → AD-09; APIs #74/#76/#77; Admin confirmation, course status, delete dependencies and audit"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-09

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 214; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence distinct; do not infer APIs/data/actions from mockups; recheck Study Web wiring; preserve unverified runtime/schema/test status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Admin role is not proof of AC permission; retain PII/lifecycle/schema blockers; fake-session tests do not verify live deployment.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve numeric ID handoff; trace auth/path/query/effects/response/errors; do not infer audit behavior from mockups; distinguish API Draft from local source.
- additional_cross_screen_review: `.agents/worklog/2026-11-07/design-study-screen-ad08.md`
  - carry_forward: AD-08 confirms AC-32 permission mapping is open, API #75 DD/body is Draft/DERIVED, legacy BIGINT and V1-PILOT UUID schemas conflict, Study Web is UNWIRED, and historical fake DB test results do not establish live behavior. AD-09 should trace #76/#77 separately and preserve distinct status/delete policies.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-09 only in this session. Inspect its inventory and connected AD-06/AD-07/AC-32/API #74/#76/#77 behavior; write `AD-09_PLAN.md` before marker map, annotation or DD; preserve source assets; create ordered markers and annotated image; author A–F screen DD with event/API/state/navigation trace; update `list_screen.md`, global `dd_screens/PLAN.md`, and this worklog; distinguish DD readiness, implementation status and runtime verification.
- Inventory pointer: Admin course actions dialog at proposed `/admin/courses/:courseId/actions`; APIs #74/#76/#77; expected confirmation for status change/delete and warnings about enrollments/content dependencies; linked AD-06/AD-07; delete policy is currently marked unconfirmed. Verify against AC-32, API catalog and current source; do not assume soft/hard delete or status transitions.
- Objective pointer: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; goal is full 83-screen DD, one Screen ID per session.

## CURRENT_BEHAVIOR

- Assets: `screen.png` 1538×1600, SHA-256 `f37b4e028f71821c6995e1c92e296ef1f762ab76697329da250de3781e784978`; `code.html` SHA-256 `03525d51f30778c2bffd2b553d7e89864fd0e662aa3b03df68580080c4bfb4c7`. Preserve both.
- Prototype shows a page-style Admin action form (inventory calls it a Dialog), blank target/current-status cards, three radios `draft` (checked), `archive`, `delete`, disabled reason textarea, Cancel and disabled Confirm. The radio group is native/selectable; its `change` listener has an empty body and triggers no operation/API. No fetch/axios/XHR exists.
- Prototype claims archive semantics, permanent irreversible deletion, required ISO-27001 audit reason, automatic RBAC, enrollment checks, and lifetime record retention. These are display copy only. Back-to-AD-07 copy and Cancel both link to `/admin/courses` (AD-06); shell/footer links use `#`.
- Study Web recheck: no editable package/router/entrypoint/client source outside docs/assets, ignored `dist`, and `node_modules`; runtime remains `UNWIRED` / `NOT VERIFIED`.
- AC-32 actor is Admin with course-management permission. Sequence: GET #73 list → GET #74 detail/course+owner+counters → choose Update, Status, or Delete → status branch #76 updates status + audit; delete branch #77 soft-deletes by policy → reload course management. Permission and counters are not proven by local screen/API behavior.
- Catalog #76: `PATCH /api/v1/admin/courses/{course_id}/status`, Bearer JWT/Admin, int64 path, `ApiEnvelope<Page<Course>>`, 200 `DESIGN_RESOURCE_UPDATED`, errors 401/403/404/422/500. Body absent. API DD Draft.
- Local #76 route/module uses strict `{status}` body with uppercase `DRAFT|PUBLISHED|SUSPENDED` (`DERIVED`); no `ARCHIVED`, reason, transition/readiness gate, or enrollment/content side effect. Shared `ADMIN` guard precedes raw path/DB in the view; path is signed int64. It locks current status, same-status is a no-op without timestamp/audit duplicate, changed status updates row and writes `course_status_audit_logs` with actor/old/new status atomically, reads #74 projection, returns singleton Page, and commits after valid projection. Query/audit/projection/commit failures rollback to safe 500; absent course is 404.
- Catalog #77: `DELETE /api/v1/admin/courses/{course_id}`, Bearer JWT/Admin, int64 path, no body/query, `ApiEnvelope<DeleteResult>`, 200 `DESIGN_RESOURCE_DELETED`, errors 401/403/404/422/500. API DD Draft.
- Local #77 uses shared `ADMIN` guard before raw path/DB; locks a non-`DELETED` course; returns 404 if absent/already deleted; checks any enrollment and active generic Content, lesson, quiz, and assignment rows; dependency match rolls back with 422 `DESIGN_VALIDATION_ERROR`; otherwise sets `courses.status='DELETED'`, `updated_at=CURRENT_TIMESTAMP`, returns `{id,status:"deleted",deleted_at}` where timestamp maps from DB `updated_at`, and commits. It does not hard-delete, cascade, change children, or append audit. Dependency set, marker, timestamp alias, and repeat-delete semantics are DERIVED/open.
- Local #73/#74 do not filter `DELETED`; #76 also has no deleted-target filter, so local status update can replace the tombstone. Visibility/restore policy remains open. Legacy BIGINT DDL/migration 010 audit candidate differs from V1-PILOT UUID/versioned Course schema; deployment/live DB unverified.
- Historical source-context test checkpoint: #76 focused 18, linked regression 134, Study suite 890; #77 focused 20, linked regression 143, suite 910. Fake DB/session tests; not run in this screen session and do not verify live schema/deployment.

## SOURCE_TRACE

```text
Expected: AD-06/#73 → AD-07/#74 numeric Course.id and current Course → AD-09 user selects a contract-defined status action (#76) or delete (#77) → show result and reload course management per AC-32.
Current: Study Web is unwired. Prototype only changes native radio selection (default `draft`, other values `archive`/`delete`) with an empty listener; reason/Confirm are disabled. Local #76 accepts DERIVED status body DRAFT/PUBLISHED/SUSPENDED and writes status+audit for changes; local #77 soft-marks DELETED after DERIVED dependency checks. Back/Cancel route to AD-06. API DD/policy, permission, live schema and client reload route are unresolved.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Status options | Prototype radios are `draft/archive/delete`; catalog/AC omit #76 body, local candidate accepts DRAFT/PUBLISHED/SUSPENDED. | `DISCREPANCY` / `DERIVED` | Do not map `archive` to `SUSPENDED`, `delete`, or another state without owner decision. |
| Permanent delete vs #77 | Prototype says irreversible DB deletion; local #77 updates status to `DELETED` and returns DeleteResult. | `DISCREPANCY` | Do not promise hard deletion or data recovery behavior. |
| Audit reason | Prototype labels required ISO-27001 reason, textarea disabled; #76 body has only candidate status and audit row contains actor/old/new status, no reason; #77 writes no audit. | `UNSUPPORTED` | Do not send or persist a reason absent API/schema contract. |
| #77 dependency policy | Current source blocks any enrollment, active Content, lessons, quizzes, assignments with catalog 422; API DD lists coverage/history questions. | `DERIVED` / `OPEN` | Confirm which dependencies and historical records block deletion; server check remains authoritative. |
| Permission/schema/status lifecycle | AC-32 says course-management permission; local #76/#77 check role `ADMIN`; legacy BIGINT vs pilot UUID; deleted Courses remain visible and #76 can replace status. | `OPEN` / `DISCREPANCY` | Require owner approval for permission, live deployment, visibility and restore policy. |
| Route and runtime | Proposed action route; no Study Web app source; back/cancel point to list; native radio listener is no-op. | `UNWIRED` / `DISCREPANCY` | No mutation UI behavior is implemented or verified. |

## CHANGES

- Files changed: `AD-09_PLAN.md`, `AD-09.md`, `AD-09_markers.json`, `AD-09_markers.svg`, `screen_annotated.png`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, and this worklog.
- Tracker changes: AD-09 inventory/global-plan status records the DD and implementation blockers; API #076/#077 source classification updated from D to R because local route/module/test sources exist. API DDs remain Draft.
- Screen result: DD `BLOCKED`; implementation `BLOCKED`; Study Web runtime `NOT VERIFIED` (`UNWIRED`).
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`, 3/214 exact-type docs worklogs selected; all selected logs read in full. | VERIFIED |
| Scope and context preflight | `.agents/project/INDEX.md`, dependencies/contracts/workflows; web-work AGENTS/INDEX and Study subcontext; Study Web design guide; server-study AGENTS/INDEX/modules/database-security/tests context; registry confirms `createDD-markdown` excludes `web-ui-only-dd`; no canonical skill applies. | VERIFIED |
| AD-09 asset/HTML review | Source hashes recorded; controls include three radios, disabled reason and Confirm; native radio listener is no-op; no API transport call. | VERIFIED |
| AC/API/source review | AC-32 diagram, API catalog/DD/open questions, #76/#77 route/models/validators/queries/views and DB candidates reviewed. #76 body/status and #77 dependency/marker rules remain DERIVED; both API DDs Draft. | VERIFIED (source review only) |
| AD-09 artifact audit | DD A–F present; 38 ordered/unique JSON markers match exactly 38 section-C rows; SVG groups and coordinates match JSON; all stroked circles are in bounds; all local Markdown targets resolve. | VERIFIED |
| Image/source preservation | Original screenshot 1538×1600 and annotated image 3076×3200; source `screen.png` and `code.html` hashes unchanged; annotated image visually reviewed after moving top-row markers #2–#9 down 1 px. | VERIFIED |
| Catalog/tracker audit | Inventory IDs and screen folders match 83/83; core four-artifact count 62/83 (21 incomplete); AD-09 and #076/#077 index/global checkpoint updated. | VERIFIED |
| Whitespace/test scope | `git diff --check` passes for tracked changes; no application tests or runtime were run. | VERIFIED |

## HANDOFF

- Remaining work: none for AD-09 documentation in this session. Owner decisions, API DD approval, Study Web implementation, live schema/deployment, and runtime verification remain explicit blockers in the screen DD.
- Next owner/action: process AD-10 in a separate session; do not continue to another Screen ID in this session.
