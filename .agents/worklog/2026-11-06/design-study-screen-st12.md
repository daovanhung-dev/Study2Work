---
task_id: "2026-11-06-design-study-screen-st12"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-11 → ST-12 lesson context; API #26 lesson resources; API #12 resource metadata/access; ST-12 → GS-07 resource view/return context"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-12

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 of 173 exact-type `docs` worklogs; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve source assets; separate API catalog/design from current source; Study Web is UNWIRED; keep API discrepancies and data/source gaps explicit.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not infer UI route/cache/search behavior from prototype; trace backend contract and source independently; keep hashes and expected/current separation.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: One Screen ID per session; source-backed API does not prove UI/runtime wiring; preserve API #12 current direct-URL behavior and unresolved resource access policy.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Objective file `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` was read before continuing. This session handles ST-12 only, plans before DD/annotation, preserves source assets, and distinguishes DD readiness, implementation status and runtime verification.
- Inventory ST-12: Student, proposed `/student/lessons/:lessonId/resources`, AC-15, API #26/#12, linked ST-11 and GS-07. Expected: request #26 by `lessonId`; if a valid `resource_id` is available, request #12; do not open an unapproved URL.
- API catalog #26 declares Student Bearer, `lesson_id:int64!`, `ApiEnvelope<Lesson>`, 200/401/403/404/500. API #26 DD remains Draft and lists unresolved payload/cardinality/access/visibility/URL/error questions.
- API catalog #12 declares public GET `/api/v1/resources/{resource_id}`, `ApiEnvelope<Resource>`, 200/404/500. AC-06 describes public-or-authorized access and a private-resource signer; this conflicts with current API #12 source.

## CURRENT_BEHAVIOR

- `screen.png` is 1600×1504 and `code.html` is static HTML. Both source hashes are recorded in `ST-12_PLAN.md` and `ST-12_markers.json`; originals remain unmodified.
- HTML contains no page fetch/listener/timer/router handler. Anchors use `href="#"`; `data-path` is inert in this file. The 30-second refresh, auth/security and compliance claims are static copy.
- Study Web editable source/package/router is absent in this checkout; the Study Web context is `UNWIRED`.
- API #26 route/module/query/test was not found in current Study Server source/tests. API #12 is registered and implemented. It validates positive signed-int64 ID, reads `resources`, and when `lesson_id` is non-null requires a non-DELETED lesson and PUBLISHED parent course; it returns stored URL with id/name/type/url/lesson_id. It has no auth, visibility check, enrollment check or signer. `lesson_id=null` skips parent check. Source tests exist and were not run.
- Candidate `DB.sql` `resources` has `id`, nullable `lesson_id`, `name`, `resource_type`, `url`, `created_at`; no `visibility`. The checked-in DDL is not live-schema evidence.

## SOURCE_TRACE

- Router: `apps/study-server/app/api/v1.py` imports API #12 and registers `GET /resources/{resource_id}` under `/api/v1`; no Student resources-by-lesson route was found.
- API #12 caller/callee: route → `get_resource_detail` → `validate_resource_id` → `find_resource` (`RESOURCE_BY_ID`) → optional `find_published_parent_course` (`PUBLISHED_PARENT_COURSE`) → `ResourceDetail.model_validate` → `success_response`.
- API #12 effects/responses: GET is read-only. Invalid/nonpositive/overflow ID and absent resource or failing parent gate return 404 `DESIGN_RESOURCE_NOT_FOUND`. SQLAlchemy errors rollback and return 500 `DESIGN_INTERNAL_ERROR`; mapping failure returns 500. Success is 200 `DESIGN_RESOURCE_RETRIEVED`. It returns direct stored `url`; it does not call storage or sign URLs. `ResourceDetail` ignores extra values and does not return `visibility`.
- API #26: catalog/AC diagram/API DD only. `rg` over current Study Server `app` and `tests` found no `api_26`, Student `/lessons/{lesson_id}/resources` route, or corresponding module/test.
- AC-15 requires lesson entitlement but does not settle #26 direct-call predicate. API #26 DD Q-26-01..07 explicitly leaves response shape/cardinality/order/empty, auth/visibility, URL signer, error semantics and path/schema decisions open.
- ST-11 DD records no resource control in its fallback; GS-07 DD records #12 public/direct URL and unresolved entry/return context. Neither is runtime navigation evidence.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #26 response | Catalog and AC diagram say `ApiEnvelope<Lesson>`; screen purpose expects resources; no source route/module/test. | `DISCREPANCY` / `NOT_FOUND` | Cannot map a Resource collection, item ID or empty response. |
| #26 access and list behavior | API DD questions Q-26-02..07 open ordering, empty, entitlement, visibility, URL and errors. | `Draft — Needs Confirmation` | Blocks data/state implementation. |
| #12 auth and URL | Current route is public/no Bearer and returns stored URL; screen badge says Pending Auth and API DD title mentions signed URL. | `DISCREPANCY`; source `SOURCE_BACKED` | Do not claim auth, signed URL, visibility or private-resource protection. |
| Fallback/security labels | Screenshot says no available resources, zero disclosure, E2E, one-time token, refresh 30s and WCAG valid. No response/timer/accessibility runtime backs these claims. | `DESIGN_ONLY` | Do not map static copy to API state or implemented policy. |
| Study Web route | No editable app source/package/router; anchors are `#`. | `UNWIRED` | No UI/API/navigation runtime verification. |
| DDL | Candidate resources table has no visibility and nullable `lesson_id`; no live metadata check. | `NOT_VERIFIED` | Do not infer production constraints. |

## CHANGES

- Created `ST-12_PLAN.md` before DD/annotation.
- Created `ST-12.md` with 27 marker-mapped elements, five events, #26/#12 trace, state/navigation matrices, security/accessibility, blockers and source links.
- Created `ST-12_markers.json`, `ST-12_markers_overlay.svg` and `screen_annotated.png` (3200×3008, 2× source scale). Original `screen.png` and `code.html` were preserved.
- Updated `dd_screens/PLAN.md`: ST-12 blockers/status, complete-bundle count 21/83, 62 incomplete, and next pointer ST-13.
- CONTEXT_UPDATES: none. No API contract, implementation, database or runtime behavior was changed; repository-wide context pages do not need alteration for this screen DD.
- Skill routing: `.agents/context-manifest.json` registers `createDD-markdown` for Web/API DD and explicitly excludes `web-ui-only-dd`; no canonical skill was invoked for this UI-only DD.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Goal objective, router/context and docs worklog preflight | Objective read; global context map and both scope contexts reloaded; 3 selected exact-type docs worklogs read. | `VERIFIED` |
| ST-12 source/API trace | Inventory, API catalog, AC-15, API #12 route/module/query/model/test source, API #26 DD/open questions, candidate DDL, ST-11/GS-07 DD and assets read. Tests not run. | `VERIFIED` (source trace only) |
| Annotation visual review | Final 3200×3008 render reviewed; marker placement/leader lines adjusted to preserve legibility and source content. | `VERIFIED` |
| Artifact static audit | Original PNG/HTML hashes unchanged; 27 ordered unique markers map one-to-one to 27 DD IDs; all marker bounds valid; annotated ratio matches 1600×1504 source at 2×; SVG embeds exact source PNG and contains 27 numbered labels; 5 event sections; all local DD links resolve. | `VERIFIED` |
| Tracker/artifact inventory | 83 screen folders; 21 complete required bundles; 62 incomplete; ST-12 row is BLOCKED on DD/implementation/runtime axes; next pointer ST-13. | `VERIFIED` |
| `git diff --check` | No whitespace errors. | `VERIFIED` |
| Context validator | Not run: no registered `.agents/` context page or manifest changed; only per-screen design assets, tracker and worklog changed. | `NOT_REQUIRED` |
| Tests/browser/runtime | Not run; this task documents source and static assets only. | `NOT_RUN` |

## HANDOFF

- ST-12 remains `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` while #26 payload/access/empty behavior and #12 URL policy remain unresolved, and Study Web is unwired.
- Next screen after this single-screen session: ST-13, in a separate session.
