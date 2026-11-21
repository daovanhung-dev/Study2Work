---
task_id: "2026-11-06-design-study-screen-sh06"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-06 resource-not-found state maps API #08 course-detail outcomes and links GS-01/SH-01; Study Web routing is not source-backed in this checkout"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-06

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selected 3 of 158 docs worklogs; all selected logs read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: Preserve originals; verify marker-to-element mapping and source/API discrepancies; distinguish DD, implementation and runtime status.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh02.md`
    - carry_forward: Study Web source/router is absent; do not infer runtime from mock assets; source and approved catalog can conflict and must remain separate.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh03.md`
    - carry_forward: API source and static tests do not prove runtime/live DB; route proposals and links require source or explicit blocker.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete SH-06 only in this session; review/update its plan before editing DD or image/marker assets; preserve `screen.png` and `code.html`; verify annotation and marker map against stable Element IDs; trace API #08, AC-05, error mapping and linked routes; update global tracker and this worklog.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md` SH-06, AC-05, API #08 and shared route/state rules; `docs/lists/list_api.md`; current Study Server source/tests; `.agents/web-study/design.md` is the UI target, not runtime evidence.

## CURRENT_BEHAVIOR

- Source/config: SH-06 PNG/HTML and route proposals exist; there is no `apps/study-client/src/` or package manifest. Study Server #08 route, validation, query, model/helper, error mapping, and test source exist. Catalog labels #08 `D`; deployment/live DB not verified.
- Runnable tests: Read `apps/study-server/tests/modules/guest/api_08_courses_detail/test_courses_detail.py`; it covers invalid ID, missing row, SQL failure/rollback, success mapping and route success. Tests not run.
- Runtime wiring: Study Web route/UI not source-backed; #08 server source does not prove deployed runtime. No tests or browser/runtime verification performed.

## SOURCE_TRACE

- API #08 route: `apps/study-server/app/api/v1.py` maps `GET /courses/{course_id}` to `get_course_detail` and passes raw path ID, DB session, and trace ID.
- Validation/query: `validate_course_id` uses `parse_integer`; invalid IDs return 404 `DESIGN_RESOURCE_NOT_FOUND`. `FIND_PUBLISHED_COURSE_DETAIL` selects one row only where `courses.status='PUBLISHED'`, left-joins `users` for mentor projection.
- Response/mapping: 200 `DESIGN_RESOURCE_RETRIEVED` with shared envelope and singleton `data: Page<Course>`; invalid/missing/unpublished → 404 generic `Published course not found.`; SQL/mapping/model failure → 500 `DESIGN_INTERNAL_ERROR`; no #08 403 branch. Shared error helper includes `traceId` and `X-Trace-Id`.
- Contract comparison: API catalog #08 is `D`, response `ApiEnvelope<Page<Course>>`, 404/500; AC-05 diagram branch says `404/403` for not-found/unpublished. Keep discrepancy explicit. API #06 is a public list endpoint but no approved recommendation dependency/semantics in SH-06.
- Visual/static artifacts: source and HTML hashes match the plan (`screen.png` `b6a423005ea008e9f00de6f2328f182c6256e7ae647575f55dfa8c4ae05ecf0a`, `code.html` `ce3c9bff0e9d24630172230f2b28e3a533ad4e2be1daecfe71f3bf1db4649ce7`); original and annotated images are 1600×1425. Visual review and static checks confirm 22 ordered unique markers map one-to-one to 22 DD elements; 10 event sections; 25 local Markdown links resolve; marker coordinates stay inside the canvas.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Plan-first/source audit | Re-reviewed SH-06 plan, then updated it before DD; source trace above. | VERIFIED | The plan records `DD BLOCKED` for undecided surfaces and AC-05 status conflict. |
| Study Web not-found route | `src/` and package manifest absent; HTML anchors are placeholders; inventory provides route proposals. | UNWIRED | Do not infer route/runtime from design-only files or stale dist bundle. |
| API #08 and error contract | Catalog/source/test evidence shows D-vs-source discrepancy and AC-05 404/403 mismatch. | DISCREPANCY | Preserve expected/current separation; #08 invalid/missing/unpublished is 404, internal failure 500. |
| Recommendation/support/footer | Mock data has no ID/source; contact/footer destinations unresolved. | BLOCKER | Do not invent API, copy, route, or production disposition. |

## CHANGES

- Files changed: SH-06 plan and DD; this worklog; global tracker updated to `DD BLOCKED` and next handoff SH-07. `screen.png`, `code.html`, marker JSON, and annotated PNG are preserved unchanged.
- CONTEXT_UPDATES: None anticipated; this task documents current behavior and blockers.
- Context pages changed: None anticipated.
- Skill routing: Registry/context review found no canonical authoring skill for Web UI-only DD; no skill was invoked.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected-file review | Selected and read 3 exact-type docs worklogs of 158; no shortage. | VERIFIED |
| SH-06 plan and API #08 source trace | Plan updated before DD; route/module/query/response/model/test source read. | VERIFIED |
| Artifact/static audit | 22/22 markers/elements ordered and unique; 10 events; 25 local links resolve; both images 1600×1425; source hashes unchanged; coordinate bounds valid; tracker status/handoff consistent; trailing whitespace scan and `git diff --check` pass. | VERIFIED |
| Tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: Product/UX disposition for recommendation/contact/footer/legal surfaces; owner resolution of AC-05 404/403 vs API #08 source; Study Web router/source remains absent. DD BLOCKED, implementation blocked, runtime not verified.
- Next owner/action: Start SH-07 in a separate session; do not process another Screen ID in this session.
