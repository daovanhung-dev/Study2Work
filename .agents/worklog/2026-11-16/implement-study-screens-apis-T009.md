---
task_id: "2026-11-16-implement-study-screens-apis-T009"
date: "2026-11-16"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["AD-20 Study Web caller -> Study Server API #93; consider API #18 handoff only if current contract/source supports it"]
status: "COMPLETE"
---

# Worklog: Continue Study Server + Study Web (T009)

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `node scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: `READY`; 118 available; 3 selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-16/implement-study-screens-apis-T004.md`
    - carry_forward: T004 completed the bounded GS-02/API #07 search slice; the full 83-screen/103-API objective remains active at 20%; preserve browser/live API/DB and unresolved DD gates.
  - path: `.agents/worklog/2026-11-16/implement-study-screens-apis-T005.md`
    - carry_forward: AD-16/#88/#89 documentation reflects current source but create/edit remain blocked by detail/body/question/schema/permission gaps; current tests used fake sessions and browser/live DB were unverified.
  - path: `.agents/worklog/2026-11-16/implement-study-screens-apis-T006.md`
    - carry_forward: AD-17/#91 source was wired and docs reconciled, while direct Quiz vs derived metrics, permission, schema and runtime gates remained open. Historical worklog frontmatter status may differ from the process tracker; use current source and tracker for current state.
- additional_carry_forward_read: `.agents/worklog/2026-11-16/implement-study-screens-apis-T008.md`
  - carry_forward: T008 completed AD-19/#92 as a source-supported slice, 6/6 Angular tests and 20/20 fake-session API tests passed, build and scoped docs checks passed; overall objective remained 20% ACTIVE. Its worktree changes must be preserved.
- shortage: `none`
- context_read: `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/project/INDEX.md`, `.agents/project/contracts.md`, `.agents/project/dependencies.md`, `.agents/project/agent-control.md`, `.agents/project/workflows.md`, `.agents/worklog/README.md`, `.agents/worklog/TEMPLATE.md`, `.agents/web-work/AGENTS.md`, `.agents/web-work/INDEX.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`, `.agents/web-work/study/workflows/screen-implementation.md`, `.agents/server-study/AGENTS.md`, `.agents/server-study/INDEX.md`, `.agents/server-study/modules/README.md`, `.agents/server-study/apis/declared-routes.md`, `.agents/server-study/tests.md`, `.agents/server-study/database.md`, and registry entries in `.agents/context-manifest.json`.
- baseline: branch `develop`, HEAD `dadc4860`, 563 `git status --short` entries, 0 staged before T009 edits. Preserve all dirty paths; do not stage, reset, clean, commit, merge, deploy or modify production data.

## EXPECTED_BEHAVIOR

- Requirement: continue the full objective to organize Study Server APIs by role and implement all 83 Study Web screens against DD/Stitch/catalogs; verify backend/API tests while coding and change API behavior only where DD/BD/current source supports it; keep progress current in `docs/tasks/process.md`.
- Candidate scope from the screen inventory: AD-20, Soạn/gửi thông báo hệ thống, route `/admin/notifications/new`, API #93. The source DD, matching API DD, current caller and tests still need verification before deciding what can be implemented.
- Canonical materials: `apps/study-client/docs/list_screen.md`, `list_endpoint.md`, `dd_screens/`, matching Stitch assets, `apps/study-server/docs/dd/`, diagrams, current source/tests/config. Keep expected behavior separate from current behavior and record discrepancies explicitly.
- Overall objective remains `20% ACTIVE`; T009 begins at `0%` and does not redefine overall progress.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 15% | 15% | Complete required worklog/context and both-catalog preflight; verify AD-20/#93 route/caller/test inventory; record exact scope and current dirty baseline. | `COMPLETE` |
| 65% | 80% | Read complete AD-20 DD/Stitch/image package and API #93 DD/diagram/source/tests; trace caller through backend side effects/response; make only a source/contract-supported bounded implementation and run focused tests, or document a concrete gate without inventing behavior. | `COMPLETE` |
| 20% | 100% | Reconcile docs only where current source warrants it; run applicable focused tests, scoped link/diff checks and final context validator; update worklog/process and state remaining contract/runtime gates. Build is not applicable because no application source changed. | `COMPLETE` |

- T009 progress: `100%`; broad objective remains `20% ACTIVE`.

## STUDY_FE_SCOPE

`Study FE scope: candidate screen=AD-20; candidate API=#93; possible API #18 handoff is conditional on current approved contract/source and is not assumed in scope.`

## PRE_IMPLEMENTATION_PLAN

**Decision after M1 source/DD trace:** make a docs-only current-state reconciliation; do not add a client request or enable draft/send controls. The existing AD-20 Angular route/page and local title/content preview are source-backed, while no API #93 caller exists in this page. API #93 only accepts explicit recipient IDs, `PUSH|EMAIL`, title and content, writes recipient-level legacy Notification rows plus `QUEUED` delivery rows, commits before 202, and does not invoke a provider/worker. Current API #18 has a UUID path and notification-only lookup over the same `operation_id`, bound to the authenticated sender; there is no generic Study `operations` table. The generic catalog/diagram ID, response, ownership, permission, audience, draft-vs-send and delivery questions remain unresolved.

Before editing, preserve the existing dirty worktree and limit documentation changes to AD-20 current-state surfaces (`screen-index.md`, `list_screen.md`, the AD-20 DD pages/source note) and API #93 DD statements that incorrectly say #18 has no handler/mapping. Keep expected behavior and source behavior separate; do not change canonical catalogs, API contracts, backend/frontend code or `.agents` context. Then run focused AD-20 frontend, API #93 and API #18 tests, scoped Markdown-link and diff checks, and the required context validator; record exact results and any pre-existing validator baseline.

## CURRENT_BEHAVIOR

- Preflight inventory: `list_screen.md` row 78 maps AD-20 to API #93 and lists recipient/channel/preview/confirm expectations; `list_endpoint.md` catalog #93 is `POST /api/v1/admin/notifications`, 202, request `{recipients?: int64[], segment?: AudienceSegment, title, content, channels[]}`, response `Notification`, with Operation handoff unresolved. Catalogs are design evidence, not runtime proof.
- Current Angular source maps `/admin/notifications/new` to `AD20Page`; title/content update local signals and preview. Recipient/channel/priority and Save Draft/Send controls are disabled. No API #93 caller or #18 client handoff exists; the page spec asserts no POST.
- Current API #93 authenticates shared role `ADMIN`, validates explicit unique positive int64 recipient IDs, rejects `segment`, accepts only unique `PUSH|EMAIL`, and requires nonblank title/content. It verifies IDs in `users`, writes one legacy candidate notification per recipient and one `QUEUED` delivery per notification/channel, commits before 202, and invokes no provider/worker. These are local source facts; DDL/migration are candidates, not live schema proof.
- Current API #18 route accepts UUID and the Shared query projects notification/outbox rows grouped by `notifications.operation_id`, bound to authenticated `sender_id`. No generic Study `operations` table exists. It is not called by AD-20.
- Expected/current discrepancies remain: direct #93/AC-36 `Notification` vs generic tracking prose `Operation`; catalog #18 `int64` vs current route/schema UUID; owner-only vs owner/Admin policy; explicit recipients vs unresolved segments; channel mapping; AC-36 fine-grained permission vs role-only `ADMIN`; draft/send/priority/scheduling; approved Admin data grain; live schema and provider delivery.
- Focused source verification: AD-20 Angular spec `2/2`; API #93 + #18 fake-DB HTTP suites `34 passed` (one upstream Starlette/httpx deprecation warning). Browser runtime, deployment, live DB and provider delivery remain `NOT_VERIFIED`.

## SOURCE_TRACE

```text
AD-20 DD/Stitch/catalog -> AD-19 CTA + Angular route/page/local preview (no API caller) -> #93 route/ADMIN guard/validator -> recipients query -> notification + delivery inserts/transaction -> direct Notification + derived UUID metadata -> #18 notification-only UUID/sender query -> client handoff still absent
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AD-20 Web wiring | Current router maps `/admin/notifications/new` to `AD20Page`; page spec confirms controls remain disabled and no POST #93 occurs. | `ROUTE_PAGE_SOURCE_WIRED; API_CALLER_UNWIRED` | Catalog `UNWIRED` is stale for route/page only; the screen is not an operational send flow. |
| API #93 contract | Catalog flags Notification vs Operation; runtime requires explicit recipients and returns direct Notification plus derived metadata. Audience/channel/permission/draft-send/provider decisions remain open. | `DRAFT / DERIVED_PENDING_DD_REVIEW` | Keep draft/send disabled and do not invent audience, operation or delivery behavior. |
| API #18 local source | Route and Shared module exist; UUID lookup reads notification/outbox candidate rows and binds authenticated sender. Generic Operation table/lifecycle and canonical int64-vs-UUID/owner policy remain unresolved. | `LOCAL_NOTIFICATION_POLL_SOURCE; CONTRACT_DISCREPANCY` | No AD-20 client handoff; source tests do not prove live schema/deployment. |
| Overall progress | `docs/tasks/process.md` records the 83-screen/Web and test/integration objectives at a coarse 20%. | `ACTIVE / COARSE_ESTIMATE` | Keep the overall value until a broad objective milestone is verified. |

## CHANGES

- Files changed: `docs/tasks/process.md`, this worklog, AD-20 screen index/inventory, eight AD-20 DD pages, AD-20 source DD/plan, and five API #93 DD pages. No frontend/backend application source was changed in T009.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: continue the existing broad objective; select the bounded next action only after source/contract preflight; preserve all prior dirty files.

## VERIFICATION

| Command / evidence | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type coding --limit 3` | `READY`; 118 available; T004/T005/T006 selected and read; no shortage. | `VERIFIED_PREFLIGHT` |
| Git baseline | `develop`, `dadc4860`, 563 short status entries, 0 staged before T009 edits. | `VERIFIED_BASELINE` |
| Both Study catalogs and target source inventory | `list_endpoint.md` #1–#103 read in current preflight; `list_screen.md` full 83-row inventory was previously read in T004 and current AD-20/#93 rows rechecked. Current route/page/API boundary and FE/BE test paths inventoried. | `VERIFIED_M0_SCOPE` |
| Angular current route/page/test inventory | `admin.routes.ts` and route spec register `notifications/new` → `AD20Page`; screen component, data-access boundary, and page spec exist; focused spec explicitly prevents a #93 request while controls are disabled. | `VERIFIED_SOURCE_INVENTORY` |
| Study Server API #93 route/module/test inventory | `app/api/v1.py` registers POST `/admin/notifications`, 202, `CreateAdminNotificationEnvelope`; API module and fake-session test file exist. | `VERIFIED_ROUTE_INVENTORY` |
| API #18 source trace | Current router uses Shared handler; query groups `notifications.operation_id`, aggregates `notification_deliveries`, and filters `sender_id` to authenticated caller. DD #18 records no generic Study `operations` table and the open ID/owner/lifecycle decisions. | `VERIFIED_WORKTREE_SOURCE` |
| Focused Angular test | `npm test -- --include=src/app/features/admin/AD20/pages/ad20-page.spec.ts` — 1 file, 2 tests passed. | `VERIFIED_TEST` |
| Focused Study Server tests | `uv run pytest -q tests/modules/admin/api_93_admin_notifications_create/test_admin_notifications_create.py tests/modules/shared/api_18_operations/test_operations.py` — 34 passed; one Starlette/httpx deprecation warning; fake DB only. | `VERIFIED_TEST` |
| Scoped documentation checks | 27 Markdown files, 282 relative links, 0 broken; stale-route/status scan returned no matches; `git diff --check` passed. | `VERIFIED_DOCS` |
| Agent context validator | Final post-log-close rerun during T010 of `node scripts/validate-agent-context.mjs` returned `AGENT_CONTEXT_INVALID`; 1,431 output lines match `/tmp/study2work-context-T008-baseline.log` byte-for-byte (0 added/removed findings). | `BASELINE_MATCH; FINAL_RERUN_COMPLETE` |

## HANDOFF

- Remaining blockers: canonical #93 response/operation semantics, recipients/segment resolver and eligibility, channel mapping, fine-grained permission, draft-vs-send/priority, approved Admin grain/live schema, provider/worker delivery, #18 catalog UUID/int64 and owner policy. AD-20 has no #93 caller; browser/runtime and live DB are unverified.
- Next continuation: select the next screen/API slice through the worklog preflight and keep overall objectives `20% ACTIVE` until broad acceptance evidence supports an increase.
