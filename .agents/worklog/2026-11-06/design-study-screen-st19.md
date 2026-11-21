---
task_id: "2026-11-06-design-study-screen-st19"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-17 and API #36; ST-18 → ST-19 handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-19

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 of 183 exact-type docs worklogs selected; all selected files were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected behavior separate from current assets/API; preserve originals; Study Web is UNWIRED; unsupported behavior remains a blocker.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not infer URL sync, cache, or runtime from a prototype; record screenshot/HTML and contract discrepancies; do not claim unrun tests.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Distinguish source-backed API operations from missing routes and design-only declarations; preserve unresolved AC/API orchestration rather than reconciling by assumption.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Process only ST-19 in this session; author its plan before marker/DD assets; preserve screen.png/code.html; map each numbered group one-to-one to DD; trace API/errors/states/navigation; update tracker/worklog.
- Inventory ST-19: GET #36 by submission owner, display submission time, files, grading state and score/feedback where available; do not show GRADED when source status is only SUBMITTED.
- API catalog #36: GET `/api/v1/submissions/{submission_id}`, Student Bearer, int64 path, `ApiEnvelope<Submission>`, 200 `DESIGN_RESOURCE_RETRIEVED`, exact errors 401/403/404/500.
- API #36 DD remains Draft — Needs Confirmation. Student access/403-vs-404, score/feedback release, `files[]` mapping, status/time semantics and invalid path handling are open.
- F06 handoff names `submission_id`; API #35 DD draft response uses `data.id`. Do not resolve this mismatch by assumption.
- UI-only DD skill routing: machine registry excludes `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only screen-DD skill applies.

## CURRENT_BEHAVIOR

- Source assets in `apps/study-client/docs/screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/`: source PNG is 1241×1600 RGB, SHA-256 `359e259cf97a8880009e8f9324466a3437f932f0a00dc80532d2d3aeffacca57`; HTML is 8,812 bytes, SHA-256 `142253c74400da2f37fb9832d6cefcf93d3f74c6dbb4802dfc575b2d2106cab2`.
- PNG is a loaded/graded sample with top receipt/status/score, rubric breakdown, mentor details/quote, three resource rows plus preview, skill-index trend, progress/next-assignment CTAs and footer. Names, score, dates, feedback, links and other visible values are sample content, not live data.
- `code.html` is a static Guest/unavailable fallback with “Chưa có thông tin bài nộp để hiển thị.” and `/student/courses` return link; no scripts, form, route binding or API. It does not represent the loaded PNG.
- Study Web has no editable source/package/router/Student route for ST-19; ignored dist contains only `/`. Runtime is not verified.
- API #36 has catalog/DD only; no Student route/module/query/test. Current Mentor API #55 is a different role/path and cannot serve Student ST-19.
- Candidate `assignment_submissions` DDL has scalar `file_url`, score/feedback/status/time fields; logical Submission requires `files:UploadAsset[]`. DDL is not live-schema evidence.

## SOURCE_TRACE

```text
Expected: ST-18 POST #35 success → submission ID handoff (inventory submission_id;
  API #35 draft data.id) → ST-19 GET #36 → approved Submission projection → receipt/grade UI.
Current: Study Web route absent; Student API #36 route/module/query/test absent.
  Mentor API #55 exists under a separate Mentor path/authorization. API #36 design
  lists the read-only contract but does not settle access, files, or disclosure policy.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| PNG vs HTML | PNG is loaded/graded Student mockup; HTML is Guest unavailable fallback. | `DISCREPANCY` | Preserve both; don't infer runtime from either asset. |
| Study Web route | No editable app/router/Student route; ignored dist only contains `/`. | `UNWIRED / NOT_FOUND` | No frontend action/navigation is current runtime. |
| API #36 | Catalog/DD exists; current Student route/module/query/test absent. | `DESIGN_ONLY / NOT_FOUND` | Cannot claim GET execution or data rendering is implemented. |
| Access policy | Student Bearer and 403/404 catalog codes exist; owner predicate and masking unresolved. | `SOURCE_REQUIRED` | No safe row-level response behavior can be specified yet. |
| Grade/feedback | Optional score/feedback in schema; release timing and omit/null rules unresolved. | `SOURCE_REQUIRED` | Do not infer display from mockup or Mentor workflow. |
| Files | Logical `files[]`; candidate DDL stores one `file_url`; #34 association and URL access open. | `DISCREPANCY / SOURCE_REQUIRED` | No asset reconstruction or external link is allowed by current evidence. |
| Status/time/schema | Status enum/transitions, timezone, candidate FK nullability and live schema unresolved. | `SOURCE_REQUIRED / NOT_VERIFIED` | No status promotion, format or data validation assumption. |
| Path / handoff | API #36 path is int64 with no malformed-ID mapping; #35 draft `data.id` differs from inventory `submission_id`. | `DISCREPANCY / OPEN` | Route key and invalid path behavior need owner decision. |
| Mockup-only features | Rubric rows, cohort stats, mentor profile, repository/demo/PR, booking, skill chart and next assignment lack #36 fields/contracts. | `DESIGN_ONLY / SOURCE_REQUIRED` | Do not add APIs or derive values from sample content. |

## CHANGES

- Files created: `apps/study-client/docs/screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19_PLAN.md`, `ST-19_markers.json`, `ST-19_markers_overlay.svg`, `screen_annotated.png`, `ST-19.md`; `.agents/worklog/2026-11-06/design-study-screen-st19.md`.
- Master tracker updated: `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; ST-19 status/blockers recorded and total advanced to 30/83 core bundles (53 incomplete).
- Original `screen.png` and `code.html` remain preserved.
- CONTEXT_UPDATES: none. No context pages changed.
- Tests/runtime: none run.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Source preservation | `screen.png` remains 1241×1600, SHA-256 `359e259cf97a8880009e8f9324466a3437f932f0a00dc80532d2d3aeffacca57`; `code.html` SHA-256 `142253c74400da2f37fb9832d6cefcf93d3f74c6dbb4802dfc575b2d2106cab2`. Both match the pre-authoring evidence. | VERIFIED |
| Plan ordering | `ST-19_PLAN.md` was authored before marker JSON/SVG, annotated PNG and the screen DD. | VERIFIED |
| Marker/DD mapping | 58 ordered unique marker IDs and in-bounds source coordinates; 58 ordered DD element rows; all gutter badges unique; 13 sequential event headings; required A–F sections present. | VERIFIED |
| Annotation image | `screen_annotated.png` is 1401×1600 sRGB with 80px gutters; reduced preview visually checked. Original screen content is preserved under the gutter overlay. | VERIFIED |
| Link/whitespace/static audit | All relative Markdown links in ST-19 DD resolve; new Markdown files have no trailing whitespace; `git diff --check` exited 0. | VERIFIED |
| Tracker | ST-19 row is BLOCKED with source blockers; progress now records 30/83 core bundles complete and 53 incomplete, W2 Student next ST-20, independent Mentor pointer ME-03 retained. | VERIFIED |
| Tests/runtime/context | No tests or runtime checks run. No `.agents/` context page changed; context validator not required. | NOT_RUN / N/A |

## HANDOFF

- Remaining blockers: API #36 and Study Web route not wired; access predicate/403-vs-404, score/feedback disclosure, status/time, files mapping/security, invalid path and ST-18 ID handoff unresolved.
- Next W2 Student screen: ST-20 in a separate session. Keep independent Mentor pointer ME-03.
