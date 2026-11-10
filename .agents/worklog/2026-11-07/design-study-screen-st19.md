---
task_id: "2026-11-07-design-study-screen-st19"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-18 API #35 submission ID → ST-19 API #36 receipt; AC-17; Mentor API #55 is separate"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-19

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 246; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; verify current source each session; do not infer UI data from mockups or claim runtime from static design/API docs.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve original assets; current source and fake-DB tests do not prove live schema/deployment; keep UI source `UNWIRED` absent editable route/client code.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use exact current server fields/route evidence; retain authorization, privacy and schema policy as open where not approved; distinguish local source from runtime verification.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st18.md`
    - carry_forward: Keep API #34 upload success separate from #35 submission success; #35/#36 Student routes are absent; F06 does not decide draft retention; AC-17 places GET #36 before submitted-state display while inventory assigns receipt ownership to ST-19; `data.id` vs `submission_id` remains unresolved.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-19 only in this session; audit its existing plan, source assets, marker map and DD; preserve raw assets; document all visible elements/events with source trace; update the screen inventory, global tracker and worklog; distinguish DD, implementation and runtime statuses.
- Inventory row 33: Student receipt at proposed `/student/submissions/:submissionId`; API #36; show submission timestamp/files/status and score/feedback when available; do not infer `GRADED` from screenshot or `SUBMITTED`; links to ST-17/ST-20.
- F06/AC-17: ST-18 #35 creates the submission, then GET #36 reads the receipt; inventory calls the handoff `submission_id`, while #35 Draft response calls it `data.id`.
- API catalog #36: `GET /api/v1/submissions/{submission_id}`, Student Bearer, path `submission_id:int64!`, `ApiEnvelope<Submission>`, 200 `DESIGN_RESOURCE_RETRIEVED`, exact errors 401/403/404/500.
- UI-only Study Web DD has no canonical skill in the registered skill manifest; no API DD or implementation change is authorized by this screen task.

## CURRENT_BEHAVIOR

- Study Web root has `dist/`, `docs/`, `node_modules/` and build metadata; editable `src/`, root `package.json`, Student route and ST-19 runtime are absent. The compiled dist contains index/CSS/JS but no `student/submissions` route string in the inspected output.
- Student API #36 has catalog and Draft DD only; no Student route/module/query/test was found in current Study Server source. Mentor API #55 is a distinct `/mentor/submissions/{submission_id}` endpoint with Mentor auth and course-owner checks.
- Logical `Submission.files` is `UploadAsset[]`; checked-in legacy `assignment_submissions` has one nullable `file_url`, nullable assignment/user FKs, nullable score/feedback and `submitted_at TIMESTAMP`. V1-PILOT `02_study_db.sql` has no business assignment/submission/upload tables; live schema/deployment remain unverified.
- ST-19 original PNG is 1241×1600; HTML fallback is Guest/unavailable with `/student/courses`. HTML includes Tailwind CDN/config scripts and remote Google Fonts, but no form, ST-19 API call or event handler. The visual typography/width/CDN choices differ from the Study Web guide.
- Existing screen DD/plan/marker JSON/SVG/annotation were drafts. DD was corrected for HTML script facts, design target gap, event type/trigger mapping, and element-to-event references for header/footer/skill index.

## SOURCE_TRACE

```text
Expected: ST-18 API #35 success → submission identifier → ST-19 GET #36 → approved Submission projection → receipt/grade fields permitted by status and disclosure policy.
Current: Study Web route/client absent → Student API #36 route/module/query/test absent. Mentor #55 has a separate role/path/query and is not the Student consumer. Catalog/API DD remain design-only; no current #36 DB effect or response exists.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #36 wiring and row access | Current route/module/test search finds no Student #36; API DD Q-36-01 leaves owner predicate and 403/404 masking open. | `NOT_FOUND / UNWIRED / BLOCKER` | DD cannot define access query or inaccessible-row behavior. |
| Score/feedback and status | Logical schema fields are optional; AC-17 doesn't define release timing; full SubmissionStatus and timestamp serialization are open. | `DESIGN_ONLY / BLOCKER` | UI must not infer grade state, scale, visibility or timestamp conversion. |
| Files and schema | Logical `files[]` differs from legacy scalar `file_url`; V1-PILOT has no business tables and live metadata was not queried. | `DISCREPANCY / BLOCKER` | No asset link, URL policy or persistence mapping can be finalized. |
| ST-18 handoff | API #35 Draft response uses `data.id`; inventory names `submission_id`. | `DISCREPANCY / BLOCKER` | Route param/refresh/direct-entry ID mapping remains unresolved. |
| Prototype and intended design | Loaded graded PNG differs from Guest fallback HTML; HTML has Tailwind CDN/config and remote fonts, width 1440 vs guide ~1120/Inter-system/no remote font. | `DESIGN DISCREPANCY` | Preserve assets; align implementation to the guide before frontend work. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-19_bai-da-nop-va-phan-hoi/ST-19_PLAN.md`, `ST-19.md`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog.
- Existing `ST-19_markers.json`, `ST-19_markers_overlay.svg`, `screen_annotated.png`, `screen.png` and `code.html` are retained; annotation assets were checked, not regenerated.
- CONTEXT_UPDATES: none; no API/source/schema contract changed.
- Context pages changed: none.
- Assumptions: none; unresolved access/disclosure/asset/route choices remain blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective read first; exact docs selector `READY` 3/246; AD-01, AD-02, AD-03 selected worklogs and ST-18 dependency worklog read. | VERIFIED |
| API/UI/source trace | Inventory/F06, AC-17, API catalog and #36 DD, #35 response DD, Mentor #55 current source, route inventory, DDL and Study Web tree inspected. | VERIFIED_SOURCE_REVIEW |
| Asset/marker/DD static audit | Original PNG 1241×1600/hash retained; HTML 8,812 bytes/hash retained; annotated PNG 1401×1600 reviewed. 58 sequential unique markers = 58 DD rows = 58 SVG groups; labels/badge coordinates match, unique target points are in bounds, minimum badge-center spacing 25px. DD A–F and 13 sequential events have explicit element/type/precondition and valid event references. | VERIFIED |
| Local links and inventory coverage | DD links 18/18; plan links 12/12. Inventory has 83 unique IDs matching 83 folders; 82/83 folders have six core artifacts (ST-01 is the sole incomplete bundle); ST-19 has all six. | VERIFIED |
| Inventory/global plan and whitespace checks | ST-19 inventory row and global tracker row/checkpoint updated with blockers and three separate statuses. Scoped `git diff --check` passed; authored ST-19 files have no trailing whitespace. Repository scan found four pre-existing trailing spaces in `list_screen.md` lines 3–6, outside changed hunks. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 `AGENT_CONTEXT_INVALID`: `.agents/db-admin` context and source roots are missing, broken db-admin context links, and stale manifests for server-study/server-work/web-work/mobile-work/db-admin. No ST-19-specific validation issue appeared. | FAILED_REPOSITORY_WIDE |
| Application tests/runtime/live DB | Not run; no behavior test or live-state claim is made. | NOT_RUN |

## HANDOFF

- Remaining blockers: #36 access and disclosure policy; Student routes/source; asset mapping; status/time semantics; #35 ID handoff; mockup-only data/actions; live schema/deployment; Study Web route and visual alignment.
- Next owner/action: ST-20, in a separate session; do not process another Screen ID in this session.
