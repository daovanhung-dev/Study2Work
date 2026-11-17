task_id: "2026-11-16-load-study-server-web-context"
date: "2026-11-16"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study", "web-work"]
cross_scope_dependencies: ["Study Web -> relative /api/v1 -> Study Server via Angular dev proxy; Study OpenAPI contract is NOT_FOUND/placeholder and deployment is unverified."]
status: "PARTIAL"
---

# Worklog: Nạp context Study Server và Web

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 281 matching worklogs; selected and read all 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-13/load-project-context.md`
    - carry_forward: Prior broad context handoff says Study Server historical counts are not freshly verified and Study Web status metadata had a discrepancy; inspect current entry pages and preserve evidence/status boundaries.
  - path: `.agents/worklog/2026-11-12/add-study-web-screen-rules-workflow.md`
    - carry_forward: Study Web is Angular 22; screen/API catalogs are design references and feature API callers may be unwired; use frontend rules and implementation workflow for Study Web.
  - path: `.agents/worklog/2026-11-12/agent-context-improvements.md`
    - carry_forward: Agent Control is mandatory; context validator previously had a repository-wide invalid baseline, which must be checked afresh if run.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Load the relevant project context for Study Server and Web, identify the wired page graph and practical source boundaries, then provide a concise handoff. No application behavior or feature was requested.
- Canonical contract/approved DD: Root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/project/agent-control.md`, the context manifest, and the scope routers/indexes. No feature DD/API contract selected.

## MILESTONES

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 25% | 25% | Complete classification, global context read, exact-type worklog preflight and read all selected prior logs; record this audit entry. | `DONE` |
| 35% | 60% | Read the wired Study Server router/index and its principal architecture, API/runtime/database/module/service/test/workflow context pages; summarize status and source boundaries. | `DONE` |
| 40% | 100% | Read Web parent and Study Web subcontext pages needed for a scope handoff, inspect registered boundary/wiring, finalize this worklog, and run context validation. | `DONE` |

## CURRENT_BEHAVIOR

- Source/config: Read `.agents/server-study/AGENTS.md`, `INDEX.md`, all 10 pages wired in the manifest, with focused excerpts from the large pages. Context describes FastAPI composition `app/main.py -> app/api/v1.py` plus core settings, sync SQLAlchemy, middleware, response and trace helpers. It lists 58 `/api/v1` path templates / 69 operations. Study DB helper does not commit; caller owns transaction. Checked-in pilot DDL and migrations are source artifacts; live schema/deployment is `NOT_VERIFIED_HERE`. Readiness reports configured status without a DB probe. API #98 is source-wired while its DD remains `UNWIRED`; source omits report detail and derives title from discussion content.
- Web context/config: Read parent `web-work` router/index and architecture/conventions/dependencies/modules/workflow, plus Study Web `AGENTS.md`/`INDEX.md`, design, frontend rules and screen workflow. Parent context covers both Angular Study and React Work clients. Study Web subcontext describes AD-01–AD-25 routes and 19 screen-level callers to 14 source-backed Admin GET APIs through `AdminApiService`; login uses API #3, refresh uses source-only R-X01, and credentials remain in tab memory. Other feature groups and production routing/deployment remain unverified. Work Web is React 19/TypeScript/Vite with React Query, Zod and relative `/api/v1` to Work Express; keep the two client stacks separate. Study Web has a distinct ocean/light design guide and four-folder screen structure. Its individual screen workflow requires catalog/DD/image/source checks, tests/demo and cleanup of isolated fixtures.
- Contract boundary: Project architecture/dependencies say Study Web uses a generic relative `/api/v1` transport and Angular dev proxy to Study Server at `127.0.0.1:3003`; Work Web has a separate `/api/v1` boundary to Work Express. Project contracts and manifest both mark Study OpenAPI as `NOT_FOUND`/placeholder. No screen/API-specific Study contract was selected.
- Runnable tests: Not run in this task. Context page `tests.md` records 1,326 local Study tests passed at the 2026-11-01 checkpoint, 178 nullable-bind regression tests, and 20/20 branch-backed follow-up HTTP requests for ten repaired operations. These are dated context claims, not re-executed verification.
- Runtime wiring: Context says guest, mentor and admin route families are composed locally; `/api/v1/chat_log_ai` is unwired, real email delivery/token generation/retry is absent, and Ollama adapter has no verified Study caller. Admin/mentor pages often label physical mappings and policies `DERIVED`; preserve those labels and do not infer live DB behavior.

## SOURCE_TRACE

```text
root/global context -> exact-type worklog preflight -> project ownership/contracts -> server-study router/index/pages -> web-work parent + Study Web subcontext -> cross-scope handoff
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #98 expected/current | Scope pages say route is source-wired and characterized, while DD remains `UNWIRED`; current source derives title from discussion content and omits report detail. | `DISCREPANCY` | Keep DD/source gap explicit; do not infer report projection from route existence. |
| Live Study database | `.agents/server-study/database.md` labels pilot DDL checked in and live status not verified; fake DB tests do not establish deployment. | `NOT_VERIFIED_HERE` | Require current live metadata before relying on deployed tables or migrations for a feature. |
| Study Web wiring | `.agents/context-map.md` and project architecture/dependencies say feature routes/calls/auth are absent; current `.agents/web-work/study/{AGENTS,INDEX}.md` describes AD-01–AD-25, 19 callers and 14 source-backed Admin GET APIs. Current app source was not inspected in this handoff. | `DISCREPANCY` | For a screen/API task, complete the mandatory Study catalogs preflight, then inspect exact current source and preserve unresolved behavior separately. |
| Study Server route-count metadata | `.agents/project/source-status.md` records 57 templates/68 operations and 1,315 tests; `.agents/server-study/AGENTS.md`, `apis/declared-routes.md` and `tests.md` record 58/69 and 1,326 tests at a later checkpoint. | `DISCREPANCY / CONTEXT_STALE` | Treat these as dated context claims; recheck current source/test before relying on counts. |

## CHANGES

- Files changed: This worklog only.
- CONTEXT_UPDATES: None requested; this is a context-loading handoff.
- Context pages changed: None.
- Assumptions: “web” is routed through `web-work`; include the Study Web subcontext because the requested other scope is Study Server and the context map maps `apps/study-client/` there.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; 281 available; 3 selected and read. | `VERIFIED` |
| Study Server/Web/project context reads | Read manifest and scope routers/indexes; principal Study Server pages; Web parent pages and Study Web subcontext pages; Project INDEX and relevant architecture/dependency/contract/source-status excerpts. These are context-document claims, not a fresh source/runtime audit. | `VERIFIED_STATIC_ONLY` |
| `node scripts/validate-agent-context.mjs` | Exit 1, `AGENT_CONTEXT_INVALID`; 83 findings: 32 DB Admin, 1 contract, 33 orphan skill resources, 10 broken context links and 7 `CONTEXT_STALE` sections. Summary matches recorded prior baseline; no finding mentions this worklog. | `BASELINE_INVALID; NO_NEW_WORKLOG_FINDING` |
| Study Server app/test suite/live DB | Not requested or run. | `NOT_RUN` |
| Application tests/runtime | Not requested or run. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: Repository-wide context validator remains invalid with the existing 83-finding baseline described above. The Study Server/Web wiring and route-count documentation discrepancies remain unresolved because no feature-specific source audit was requested.
- Next owner/action: For a feature task, select the exact screen/API. If it touches Study Web, first read `apps/study-client/docs/list_screen.md` and `list_endpoint.md`, record screen/API IDs, then verify the current client and Study Server source/tests because the context pages disagree about feature wiring and route counts. No implementation action is in scope for this handoff.
