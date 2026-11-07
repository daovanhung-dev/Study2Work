---
task_id: "2026-11-07-design-study-screen-st08"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-08 Study Web /student/courses ↔ AC-13 and APIs #20/#21; ST-07 enrollment handoff and ST-09 course detail"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-08

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 235; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected behavior separate from current source; preserve original assets; trace caller, authorization, data effects, response and tests; keep Study Web `UNWIRED` unless current editable route/client code proves otherwise; do not claim tests/runtime/live schema verified.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer routes, filters, data mappings or actions from mockups; compare API catalog and AC with current backend; preserve unresolved contract and design-system discrepancies; UI-only DD has no canonical skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Treat local API source and draft contracts as distinct evidence; avoid inferred identity, policy, audit, or status semantics; preserve original assets; distinguish DD, implementation, and runtime status; finish one Screen ID only.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-08 only in this session. Inspect the canonical inventory, relevant AC/API/database contracts, original assets and current source. Write `ST-08_PLAN.md` before creating or updating marker maps, annotated image, or screen DD. Preserve usable source assets, create ordered one-to-one element markers, document sections A–F with traceable events/states/navigation/errors and explicit blockers, update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog. Do not infer API fields, progress math, status filters, retry rules, or behavior absent approved evidence.
- Canonical evidence: Inventory row 22 identifies ST-08 “Khóa học của tôi”, proposed route `/student/courses`, AC-13, APIs #20/#21, links ST-09/ST-20, states `loading/empty/partial-progress/error`, P1, gate D. AC-13 requires Student login and a course/progress list; API catalog and API DDs remain Draft. ST-07's expected handoff is enrollment-confirmed then reload #20; no runtime handoff is wired.

## CURRENT_BEHAVIOR

- Source/config: ST-08 artifacts already existed at session start: original `screen.png` (1280×1024, SHA-256 `665e39c4c1de2cbe417ce092b269aaaa4adc807fc0bb534c2714ab9f2213c21a`), `code.html` (SHA-256 `7b8effee5a5ee1dfd7a0ebb5a051af5710785ac0f0c452863fb2b9e057c2298f`), `screen_rendered.png` (1280×1024, SHA-256 `95d1f7bacd0ff05ebf9db81f970fc775afbdece30eb10d7374ecf2f551d12ab9`), and `screen_annotated.png` (2720×2048, SHA-256 `59ce04ce833c65db94fd0768b4a9c62acc8ae07a851952f28b3921c0fe564cdc`). Original PNG omits the header and has a black band below the footer; static HTML render is usable for annotation and is not a runtime capture. HTML contains a static empty state and anchors only; no API calls, client state, or route implementation. It imports Google Fonts/Tailwind CDN, uses Plus Jakarta Sans and 1440px content width, which differs from the Study Web guide's Inter/system stack, no remote import, and ~1120px width target.
- Runtime wiring: Current Study Web tree has docs and an ignored `dist/index.html`, with no editable source, package manifest, router or Student route; bundle has only `/`. Study Server router includes `/users/me` but no `/users/me/courses` or `/users/me/progress`; no API #20/#21 module/query/focused test exists. Current backend module/test inventory and source searches found no matching endpoint implementation. Serving, live DB schema and runtime remain unverified.
- Database evidence: Legacy `infra/postgres/study-server/DB.sql` describes BIGSERIAL `courses`/`enrollments` and `lesson_progress`; V1-PILOT `infra/postgres/02_study_db.sql` describes UUID course versions/enrollments and `lesson_progress_facts`/`progress_snapshots`. These are distinct checked-in design artifacts; neither proves the API #20/#21 live schema.
- Runnable tests: No API #20/#21 focused test source was found; no tests were run.

## SOURCE_TRACE

```text
Expected: ST-08 Student course list per inventory and AC-13; #20 courses then #21 progress and client merge; ST-07 enrollment handoff and ST-09/ST-20 destinations remain design-level.
Current: no Study Web caller/router; no Study Server #20/#21 route/module/query/test; API Drafts return ApiEnvelope<UserProfile>; static HTML has no request/event code. Catalog/AC, current runtime, and DDL artifacts do not establish the same list/progress payload or ID model.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #20 response and ST-08 course list | Catalog/API Draft declare `ApiEnvelope<UserProfile>`; AC-13 expects Enrollment + Course collection; endpoint is absent. | DISCREPANCY / BLOCKER | No course-row mapping, empty wire shape, page metadata or ST-09 course ID can be specified. |
| #21 query and progress response | Catalog says `course_id list hoặc aggregate?:string`; response is `ApiEnvelope<UserProfile>`; API Draft leaves schema/formula/identity/empty behavior open; endpoint is absent. | SOURCE_REQUIRED / BLOCKER | No merge key, progress percentage, missing-progress default or partial-failure policy can be specified. |
| AC-13 empty branch | Decision label says `NO → empty state; YES → render`, while both `EMPTY` and `HAS DATA` edges target the same “Hiển thị khóa học + % hoàn thành” node. | DISCREPANCY / BLOCKER | Owner must clarify the empty-state destination before final state transitions are implementable. |
| DDL identity/data model | Legacy BIGINT `enrollments`/`lesson_progress` differs from V1-PILOT UUID `course_enrollments`/`lesson_progress_facts`; live schema is not verified. | DISCREPANCY / BLOCKER | Do not infer course ID type, enrollment join, or progress source for #20/#21. |
| Loaded/filter UI and design alignment | HTML only shows empty state; no filter/cards/progress/loading/error; typography/import/content width diverge from intended guide. | DESIGN GAP / BLOCKER | Loaded-state and responsive implementation need an approved design aligned with Study Web guide. |
| Study Web and API runtime | Editable Study Web source/routes and #20/#21 route/module/query/tests are absent. | UNWIRED / NOT_FOUND | No implementation or runtime claims. |

## CHANGES

- Files changed: `ST-08_PLAN.md` (2026-11-07 re-audit/plan delta), `ST-08.md` (A–F structure and verified discrepancies), `apps/study-client/docs/list_screen.md` (ST-08 blocker row), `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (ST-08 row and checkpoint), this worklog.
- Existing source assets, marker JSON/SVG, HTML render and annotated PNG were retained; no image or source HTML was rewritten because marker and image audits passed.
- DD now makes the required sections A–F explicit; adds the AC-13 `EMPTY`/`HAS DATA` edge discrepancy, legacy BIGINT vs V1-PILOT UUID DDL discrepancy, and Study Web guide mismatch for remote fonts/CDN, type, primary color, blur and content width.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: None; unresolved product/API decisions remain explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective read; root router, global context map, worklog README/template, exact-type selector and all three selected AD-01/AD-02/AD-03 worklogs reviewed. | VERIFIED |
| Scoped context/registry review | Project INDEX, ownership/dependency/contracts/database/architecture pages, web-work and Study Web context, Study design guide, server-study AGENTS/INDEX/declared routes/database/tests/workflow pages reviewed. Manifest confirms Study OpenAPI NOT_FOUND and no canonical skill for web-UI-only DD; registered docs workflow loaded. | VERIFIED |
| ST-08 contract/source review | Inventory/global plan, AC-13 XML flow, API catalog and #20/#21 Draft DD/open questions, Study Server route/module/test inventory, Study Web tree/dist, both checked-in DDL generations and adjacent ST-07 handoff reviewed. No application tests run. | VERIFIED_STATIC_REVIEW |
| Artifact pre-audit | Existing PNG/HTML/render/annotation hashes and dimensions recorded; original and annotated images visually reviewed. | VERIFIED_STATIC_REVIEW |
| Plan/DD/tracker update | Re-audit plan updated before the DD; A–F sections and blockers updated; ST-08 inventory/global-plan entries updated; no source/API/context files changed. | VERIFIED |
| Marker/image/link static audit | Corrected audit path after the first script invocation used an incorrect scope directory; final Python static audit passed: source hashes match marker JSON; original/render/annotation dimensions match; 9 sequential unique markers map 1:1 to 9 DD rows and 9 SVG labels; targets/marker bounds and non-overlap pass; DD/plan local links resolve; annotation visually reviewed. | VERIFIED |
| Inventory and whitespace | 83 unique inventory IDs match 83 screen folders; 82/83 core artifact bundles present (only ST-01 incomplete); authored ST-08 text has no trailing whitespace. | VERIFIED |
| `git diff --check` | Scoped check of ST-08 trackers/artifact paths exited 0. | VERIFIED |
| Application tests/runtime | Not run; docs-only task. API #20/#21 and Study Web remain unwired; live DB schema/deployment were not inspected. | NOT_RUN |
| Context validator | Not run because no canonical context page or manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: #20/#21 response/query/merge/formula and identity semantics; AC-13 empty branch target; legacy BIGINT vs V1-PILOT UUID DDL; loaded/filter state and design-system alignment; Study Web and API #20/#21 runtime wiring; live DB state.
- Next owner/action: Complete ST-08 artifacts and static audit, then stop; next screen belongs in a separate session.
