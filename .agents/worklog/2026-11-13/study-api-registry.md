---
task_id: "2026-11-13-study-api-registry"
date: "2026-11-13"
primary_task_type: "coding"
secondary_task_types: ["test"]
project_scopes: ["web-work (Study Web)", "server-study"]
cross_scope_dependencies: ["Study API catalog ↔ active routes in apps/study-server/app/api/v1.py"]
status: "VERIFIED"
---

# Worklog: Register all Study Server APIs in Study Web core constants

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3` (Node was not on the default PATH; Deno compatibility invocation was used)
- selector_result: `READY`; 98 exact-type worklogs available; 3 selected and read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-12/ad01-screen-coding.md`
    - carry_forward: Study Web screens can remain presentation-only; do not invent API/auth behavior; the repository context validator had baseline structural/source-drift errors.
  - path: `.agents/worklog/2026-11-12/ad02-ui-only.md`
    - carry_forward: Generic `StudyApiService` exists without feature callers; preserve disconnected states and keep current-source/API evidence separate from DD design.
  - path: `.agents/worklog/2026-11-12/admin-system-route-wiring.md`
    - carry_forward: Current root/Admin routes are presentation navigation without auth/API integration; route work is outside this task.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Define the full 103-row Study API catalog in `apps/study-client/src/app/core/constants.ts`, with typed descriptors for API ID, method, relative path and current source status. Include source-only `POST /api/v1/auth/refresh` as `R-X01`, associated with API #3. Exclude `/api/v1/hello`, `/api/v1/test/db`, `/`, and `/health/*` from the client API registry.
- Study FE scope: `screens=none; APIs=#1–#103 plus source-only R-X01`. This is shared API infrastructure; no screen behavior/callsite is being added.
- Canonical contract/approved plan: User-approved descriptor + service plan; `apps/study-client/docs/list_endpoint.md` supplies the 103 catalog IDs/methods/paths; active `apps/study-server/app/api/v1.py` source determines `WIRED`/`STUB`/`UNWIRED`/`SOURCE_ONLY` status. `ApiEnvelope<T>` remains the response boundary.
- Consumer behavior: `StudyApiService` accepts a descriptor, resolves and URL-encodes named path parameters, preserves query params/body/headers and returns `Observable<ApiEnvelope<T>>`; it rejects `UNWIRED` descriptors before issuing HTTP.

## MILESTONES

Progress started at 0%. Context/source mapping reached 20%; registry, descriptor transport and seven focused cases passed, reaching 65%. Context synchronization, production build, exact registry audit and diff review are complete, reaching 100%. The required repository context validator still reports the previously observed repository-wide baseline findings.

| Weight | Cumulative progress when achieved | Objective / acceptance criterion | Status |
|---:|---:|---|---|
| 20% | 20% | Read three exact-type worklogs, scope rules and both catalogs; verify current client transport and exact catalog-to-server route mapping/status | DONE |
| 45% | 65% | Add typed descriptors for 103 catalog APIs plus R-X01, wire `StudyApiService` to descriptors and add coverage for registry, method/path, query/body/headers, path encoding and preflight rejection | DONE |
| 35% | 100% | Update Study Web context/manifest/worklog, run frontend tests/build, `git diff --check` and compare final context validation with the captured baseline | DONE |

## CURRENT_BEHAVIOR

- Source/config: `constants.ts` was an existing empty (0-byte) untracked target before implementation. `StudyApiService.request(path, options)` hardcodes `/api/v1`, defaults to GET and passes `HttpParams`, body and headers to `HttpClient`; there are no TypeScript feature callers. Angular 22 config provides a Vitest test target.
- Runnable tests: Angular TestBed/Vitest suite passed 4 files and 17/17 tests, including 7 new registry/transport cases. Production Angular build passed. Node `v22.23.4` and npm `10.9.9` are available via `/home/daovanhung/.local/opt/node-v22.23.4/bin`.
- Runtime wiring: `apps/study-server/app/main.py` composes the `/api/v1` router from `app/api/v1.py`. Static route comparison found 69 source operations, 66 exact catalog method/path matches, 37 unmatched catalog rows and 3 noncatalog `/api/v1` routes. Of the matches, #2 is an email-delivery stub; the other 65 are source-backed route declarations. The 37 unmatched IDs are `10, 11, 15–33, 35–45, 99–103`. `POST /api/v1/auth/refresh` is source-backed but outside the 103 catalog rows.

## SOURCE_TRACE

```text
Current: no feature caller -> StudyApiService.request(path, options) -> Angular HttpClient -> relative /api/v1 -> FastAPI app includes v1 router -> matching handler when one exists
Planned: feature data-access (future caller) -> StudyApiService.request(descriptor, options) -> descriptor method/path + encoded path params -> Angular HttpClient -> relative /api/v1 -> matching handler
API #2 -> verify-email route -> StubVerificationEmailProvider -> accepted result; no real email delivery
R-X01 -> refresh route in v1.py -> refresh view; source-only relative to the 103-row client catalog
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Catalog IDs #10, #11, #15–#33, #35–#45, #99–#103 | No exact method/path decorator match in the composed `app/api/v1.py` router | `UNWIRED` | Keep in registry for complete catalog coverage, but reject before HTTP. |
| API #2 | Matching `POST /auth/verify-email/send` route defaults to `StubVerificationEmailProvider`, whose source says it does not send email | `STUB` | Registry exposes route availability without implying email delivery. |
| API #3 refresh route | `POST /auth/refresh` exists under `app/api/v1.py` but not in `list_endpoint.md` rows #1–#103; server route context names it R-X01 | `SOURCE_ONLY` | Add one separate descriptor associated with API #3. |
| Other routes outside catalog | `/api/v1/hello` and `/api/v1/test/db` exist in `v1.py`; root and health routes exist in `main.py` | `OUT_OF_SCOPE` | Omit from client API registry. |
| Study Web context map | `.agents/context-map.md` says `SKELETON_ONLY`, while Study Web AGENTS/INDEX and manifest say `VERIFIED_WITH_UNWIRED_COMPONENTS` and current source contains readiness/Admin routes | `DISCREPANCY` | Update stale map status and registry description for the new shared constants entry. |
| Context validation | Pre-edit validator returned `AGENT_CONTEXT_INVALID`, including missing DB Admin context/source, orphan `create_dd_screen` resources and source drift across scopes | `BASELINE_INVALID` | Preserve unrelated findings; compare final output for new Study Web errors. |

## CHANGES

- Files changed: `apps/study-client/src/app/core/constants.ts`; `apps/study-client/src/app/core/http/study-api.service.ts`; `apps/study-client/src/app/core/http/study-api.service.spec.ts`; `.agents/web-work/study/AGENTS.md`; `.agents/web-work/study/INDEX.md`; `.agents/context-map.md`; `.agents/context-manifest.json`; this worklog.
- CONTEXT_UPDATES: Registered the API constants and service spec in the Study Web source list; documented descriptor/status semantics; corrected the stale Study Web context-map status to match the existing AGENTS/INDEX/manifest and current routes.
- Context pages changed: `.agents/web-work/study/AGENTS.md`; `.agents/web-work/study/INDEX.md`; `.agents/context-map.md`; `.agents/context-manifest.json`.
- Assumptions: API IDs are numeric for catalog entries; the refresh route uses its source/context ID `R-X01` and `relatedApiId: 3`. Status is source-route availability only, not live deployment or business-contract approval.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog preflight selector | Deno fallback `READY`; 3/98 exact-type `coding` logs selected and read; no shortage | VERIFIED_PREFLIGHT |
| `list_screen.md` and `list_endpoint.md` | 83 screens; 103 unique catalog API IDs; Study FE scope is screens none, API IDs #1–#103 | VERIFIED_STATIC |
| Catalog vs `app/api/v1.py` route parser | 69 source operations, 66 exact matches, 37 unmatched, 3 noncatalog source routes | VERIFIED_STATIC |
| API #2, R-X01 and client callsites source reads | #2 provider is a stub; refresh exists; no feature callers found | VERIFIED_STATIC |
| Node/npm | Node v22.23.4 and npm 10.9.9 available through local Node binary path | VERIFIED_RUNTIME |
| `node scripts/validate-agent-context.mjs` (pre-edit baseline) | Exit 1, `AGENT_CONTEXT_INVALID`; repository-wide DB Admin, orphan-resource and source-drift findings | BASELINE_INVALID |
| Catalog-to-registry-to-source audit | All 103 IDs, methods, relative paths and statuses match the catalog and active route source; 65 WIRED, 1 STUB, 37 UNWIRED; R-X01 matches separately | VERIFIED_STATIC |
| `npm install --no-audit --no-fund` | Installed 65 packages from the existing manifest/lock; no dependency declarations were requested | VERIFIED_LOCAL_SETUP |
| `npm ls vitest jsdom @angular/build --depth=0` | `vitest@4.1.12`, `jsdom@26.1.0`, and `@angular/build@22.2.6` resolve in Study client | VERIFIED |
| `npm test` | 4 test files passed; 17/17 tests passed, including 7 new registry/service cases | VERIFIED |
| `npm run build` | Exit 0; Angular production bundle generated | VERIFIED |
| Manifest JSON and required paths | Valid JSON; constants and service spec registered and present | VERIFIED |
| `git diff --check` | Exit 0 | VERIFIED |
| `node scripts/validate-agent-context.mjs` (final run after the completed worklog update) | Exit 1, `AGENT_CONTEXT_INVALID` (952 output lines); DB Admin/orphan/source-drift findings remain at baseline; no missing/unregistered finding for the new constants or service spec | BASELINE_INVALID |

## HANDOFF

- Remaining blockers: The repository-wide context validator remains invalid for baseline DB Admin, orphan-resource and cross-scope source-drift findings. This does not block the Study Web API registry; deployment and live API behavior remain outside source-route status evidence.
- Next owner/action: None for this task; the final context validator run follows this worklog update.
