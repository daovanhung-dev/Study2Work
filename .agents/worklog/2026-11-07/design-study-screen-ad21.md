---
task_id: "2026-11-07-design-study-screen-ad21"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-36; API #18/#94/#95/#96; AD-21 notification status and delivery handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study AD-21

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; selected 3 exact-type docs logs of 226; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate; inspect Study Web routing every screen; trace authorization, query/effects, response and tests; static operational claims and absent routes must remain UNWIRED; do not claim live schema/runtime/tests.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep AC permission separate from shared ADMIN fallback; preserve PII/schema/lifecycle blockers; inspect API contract and current source separately; UI-only DD has no canonical skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not infer IDs/actions/privacy from mockups; distinguish catalog/AC from current response; fake DB test evidence does not establish live schema/deployment; preserve Study Web UNWIRED unless editable app source proves otherwise.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Complete AD-21 only; inspect inventory, AC-36, APIs #18/#94/#95/#96, related AD-19/20 and SH-07, plus current server source; save `AD-21_PLAN.md` before markers/annotation/DD; preserve assets; create ordered marker map, annotated image and A–F DD; update inventory/reverse API index/global plan/worklog; keep expected/current and DD/implementation/runtime states separate; do not continue to AD-22.
- Inventory row 79: AD-21 “Sửa/kiểm soát/đo trạng thái thông báo”, candidate `/admin/notifications/:notificationId`, AC-36, APIs #18/#94/#95/#96; related AD-19/SH-07; expected states draft/scheduled/sending/delivered/failed. GET #96 to view; PUT #94 to edit or DELETE #95; poll #18 if an operation_id exists. Existing blocker: no dedicated GET notification detail.
- AC-36 expects Admin with notification-management permission to manage notifications; operation references and status/delivery transitions must be compared with API catalog and backend source without inferring lifecycle.
- Current inventory/global tracker before this session: AD-21 status D / CHƯA_BẮT_ĐẦU. Folder contains only `screen.png` and `code.html`; no plan, DD, annotation or marker map. AD-20 is now complete as previous screen; core artifact coverage is 73/83.

## CURRENT_BEHAVIOR

- Study Web has no tracked `src/` files and no tracked router/package manifest; the top-level app tree has `dist/` and `docs/`. AD-21 therefore has no verified route, client, auth/session guard, or API binding. Its `code.html` is a 272-line static prototype. It contains five shell anchors, a Notifications icon button, a return-to-list anchor, and three footer anchors; all anchors use `href="#"`, the icon button has no handler, and no `fetch`, XHR, feature script, or input exists. The three feature actions (update draft, cancel release, SH-07 handoff) are statically disabled. Current technical IDs, status, RBAC, channel cards, counts, and pipeline copy are static claims, not live response data.
- Source assets before authoring: `screen.png` 1425×1600, SHA-256 `dc6863cb8033fb99adc21118823a5d72d739e2c2db83b13b2e3b39ba7d2dfa62`; `code.html` SHA-256 `5243c7a44d759c726a53fa035ace275ee354026f9e5ff8cd47aee37726cc363a`. Only these two files existed in the AD-21 directory.
- AC-36 and API catalog expect an Admin with notification-management permission, conditional update/delete/status operations, and a notification state handoff. Direct API rows: #94 PUT path-only→`ApiEnvelope<Notification>` (200/401/403/404/422/500); #95 DELETE path-only→`ApiEnvelope<DeleteResult>` (200/401/403/404/422/500); #96 GET status path-only→`ApiEnvelope<Notification>` (200/401/403/404/500). AC-36 describes #95 as delete/mark cancelled and #96 as delivery status; API #18 is the conditional generic Operation lookup.
- Current Study Server has registered #94/#95/#96 routes and local module/query/validator/model/test source. Shared auth guard requires `ADMIN`; this does not verify AC-36's finer notification-management permission. #94 locally requires strict JSON `{title, content}` (`title` max 200 and nonblank values), locks one notification and its delivery rows, and updates title/content only if there is at least one delivery and all delivery statuses are `QUEUED`; it preserves recipient, delivery, and creation time and returns a `Notification` projection. This body and eligibility are DERIVED because catalog/diagram declare path-only and do not define those rules.
- #95 locally locks one parent notification then deliveries and hard-deletes only that path-selected recipient-level legacy BIGINT row if at least one delivery exists and all are `QUEUED`; the candidate checked-in FK cascades delivery rows. Success returns `DeleteResult {id, status:"deleted", deleted_at}` after commit; repeat delete returns 404. It does not stop a provider/worker or establish cancellation. These row-grain, queued-only, hard-delete, cascade, and timestamp semantics are DERIVED; live schema is not verified.
- #96 locally reads a single notification joined to a delivery aggregate. It returns only Notification fields (`id`, `title`, `content`, sorted `channels`, aggregate `status`, `created_at`), with precedence `QUEUED` if any queued, else `FAILED` if any failed, else `SENT` if all sent. Invalid/malformed IDs and missing/no-delivery resources map to 404. It does not return delivery counts, per-channel status, `read_at`, or `scheduled_at`. Read-only; no commit/provider call.
- Checked-in Study DDL is a candidate legacy schema: `notifications.id`/recipient IDs are BIGINT, and `notification_deliveries` permits `PUSH|EMAIL` with `QUEUED|SENT|FAILED`; the delivery FK cascades on parent delete. It does not prove the live database/deployment. AC-36 uses a notification-management permission and described states; local source uses `ADMIN` and its QUEUED/SENT/FAILED fallback. The macro-review remains `VERIFIED_WITH_OPEN_QUESTIONS`; API DDs #94–#96 remain Draft.
- API #18 design is `GET /api/v1/operations/{operation_id}`, Bearer JWT, `ApiEnvelope<Operation>`, catalog int64 path but UUID in reusable schema/AC; no Study route/module/query/test or Study operations table is present. AD-20 #93 local source's UUID `meta.operation_id` therefore cannot be proven usable with #18. SH-07 must remain blocked; AD-21 must not navigate/poll it from an unverified ID.
- Application tests/runtime were not run during this screen task. Test source files exist for #94/#95/#96; prior worklog history reports fake-DB focused tests but is not a test run in this session or evidence of live schema/deployment.

## SOURCE_TRACE

Expected flow: AD-19/list hands off a contract-valid notification ID → AD-21 reads the notification/status through #96; optionally update via #94 or delete/cancel via #95 only under an approved lifecycle/policy; link to SH-07/#18 only if a producer supplies a compatible operation ID and the #18 contract is implemented. Expected inventory states `draft/scheduled/sending/delivered/failed` do not map directly to current local `QUEUED/SENT/FAILED`.

Current flow: no Study Web route exists, so no caller/event runs. The static prototype displays unresolved ID/operation/status placeholders and disabled controls. If invoked directly, registered API #96 first applies shared `ADMIN` auth, parses positive int64 (invalid → 404), runs a read-only notification/delivery aggregate query, validates a `Notification` envelope, and returns 401/403/404/500 catalog errors. API #94 applies shared ADMIN auth before strict local body/path validation, locks parent then delivery rows, returns 404 for missing row, 422 `NOTIFICATION_NOT_EDITABLE` unless deliveries exist and all are QUEUED, updates only title/content, validates response, commits, and returns 200/401/403/404/422/500. API #95 applies shared ADMIN auth, validates positive int64, locks parent then deliveries, returns 422 `NOTIFICATION_NOT_CANCELLABLE` unless nonempty deliveries are all QUEUED, deletes the selected row, validates/commits `DeleteResult`, and returns 200/401/403/404/422/500. These local behaviors are DERIVED over candidate legacy schema. #18 has no runtime route/query/test/store; no operation polling path exists.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Notification detail and ID | Inventory says no dedicated detail GET. #96 is the only notification-specific GET and returns limited `Notification` projection; all local notification IDs are positive int64 under candidate legacy model. | DISCREPANCY / BLOCKER | Do not add a detail API or map omitted recipient/per-channel/count fields. A route ID and #96 projection remain unapproved design inputs. |
| Lifecycle/edit/delete | Inventory expects draft/scheduled/sending/delivered/failed; AC-36 says #94 conditional update and #95 delete/mark cancelled. Catalog #94/#95 are path-only. Current #94 local body/QUEUED edit gate and #95 queued-only physical delete are DERIVED; local states are QUEUED/SENT/FAILED. | DISCREPANCY / DERIVED / BLOCKER | Do not equate SENT with delivered, QUEUED with draft/scheduled, or DELETE with provider cancellation. Owner must decide lifecycle, body, retention, race and delete/cancel policy. |
| Delivery detail | Mockup shows In-App/Email channel status, completion counts and SMTP pipeline. #96 returns channel names and aggregate status only; no counts or per-channel states. | SOURCE_REQUIRED / BLOCKER | Do not render mockup counters/status as response-backed facts; local channels PUSH/EMAIL differ from In-App/Email label mapping. |
| Admin permission | AC-36 precondition is notification-management permission; API catalog says role=Admin; current handlers use shared role `ADMIN`. | DISCREPANCY / SOURCE_REQUIRED | Do not claim least-privilege permission mapping or resource scope is verified. |
| Operation handoff | Inventory conditionally polls #18. API #18 row uses int64 but AC/reusable Operation and AD-20 #93 metadata use UUID; no Study #18 route/module/query/test/table. | DISCREPANCY / UNWIRED / BLOCKER | No SH-07 link/poll can be enabled until ID, ownership, producer mapping, lifecycle and runtime route/store are approved. |
| Schema/runtime | Checked-in legacy BIGINT tables support current module's query; macro-review says local fake-DB tests only, no live DB/deployment verification. | DERIVED / NOT VERIFIED | DD must label local response/effects as current source over candidate schema, never as deployed/live behavior. |
| Study Web route/runtime | Inventory candidate `/admin/notifications/:notificationId`; zero tracked `apps/study-client/src/` files, anchors are `#`, no feature API code. | UNWIRED | Do not call candidate route, auth shell or navigation wired. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-07/design-study-screen-ad21.md`; `apps/study-client/docs/screen_stitch/05_admin/AD-21_sua-kiem-soat-do-trang-thai-thong-bao/AD-21_PLAN.md`; `AD-21.md`; `AD-21_markers.json`; `AD-21_markers_overlay.svg`; `screen_annotated.png`; `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: no behavior inferred beyond source/catalog/AC. Current source is local route/module code over a candidate legacy schema; it is not proof of deployment/live DB/provider behavior.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Router/context/worklog preflight | `.agents/AGENTS.md`, `.agents/context-map.md`, worklog README/template read; exact docs selector READY 3/226; AD-01/02/03 reviewed in full. | VERIFIED_PREFLIGHT |
| AD-21 source/contract review | Source image/HTML hashes, static DOM/actions, Study Web tracked source absence, AC-36, API #94/#95/#96 catalog and route/validator/view/query/schema, API #18/SH-07, #92–#96 macro-review, related AD-19/AD-20 reviewed. | VERIFIED_SOURCE_REVIEW |
| AD-21 artifact audit | 47 sequential/unique/in-bounds markers; plan, JSON, SVG and DD rows align; A–F present; 15 Markdown links resolve; annotated image 2850×3200 visually reviewed. | PASS |
| Inventory/progress audit | Inventory/folders 83/83; core artifacts 74/83; AD-21 row and reverse APIs #094/#095/#096 show local source `R`; global plan remains DD/implementation blocked. | PASS |
| Source preservation and diff | Source image hash `dc6863cb8033fb99adc21118823a5d72d739e2c2db83b13b2e3b39ba7d2dfa62`; HTML hash `5243c7a44d759c726a53fa035ace275ee354026f9e5ff8cd47aee37726cc363a`; `git diff --check` clean. | PASS |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining work: none for this AD-21 session. Stop here; AD-22 is the next screen for a separate session.
- Remaining blockers: notification detail projection, Admin permission, API #94 body and lifecycle policy, #95 cancel-vs-delete/provider coordination, #96 per-channel/count data, operation ID/ownership/producer bridge, API #18 runtime/store, live schema/deployment, and Study Web route/auth/client remain unresolved. DD and implementation are blocked; runtime is not verified.
- Stop after AD-21; AD-22 is a separate-session screen.
