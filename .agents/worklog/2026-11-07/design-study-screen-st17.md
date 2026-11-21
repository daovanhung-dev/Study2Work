---
task_id: "2026-11-07-design-study-screen-st17"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-17 assignment brief/API #33 → ST-18 upload/API #34 → ST-19 submit/receipt APIs #35–#36; AC-17"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-17

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 244; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; do not infer UI behavior from a mockup; inspect Study Web routing and source; trace server authorization, query/effects, response and tests; distinguish contract from runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve source assets and explicit static-only claims; do not invent filters/actions or map prototype vocabulary to API values; fake DB tests do not establish live schema/runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use exact current source and approved fields; keep permission/privacy/model discrepancies open; local source-backed behavior is not runtime proof.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st16.md`
    - carry_forward: Finish one Screen ID per session; preserve expected/current split; use AC/API/DD as design evidence only; Study Web remains UNWIRED unless editable source proves otherwise; do not infer route/fields from a prototype; no application tests/runtime/live DB unless requested.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-17 only this session; re-audit its plan before DD/tracker changes; preserve source assets; verify the 49 marker-to-element mappings; maintain a traceable A–F screen DD; update only ST-17 in the inventory/global tracker plus the directly related F06 flow and this worklog; distinguish design, implementation and runtime status.
- Canonical inventory: `apps/study-client/docs/list_screen.md` row 31 lists Student assignment detail at `/student/assignments/:assignmentId`, AC-17, API #33, linked ST-18/ST-09, and loading/open/closed/not-found states. F06 flow is #33 → optional #34 upload → #35 submission → #36 receipt.
- AC-17: Student must have assignment access and the assignment must be in deadline; diagram reads Assignment + submission rule and has a 403/409 overdue/no-permission branch. Its ordered API list is #33 GET, #34 upload, #35 POST submission, #36 GET receipt.
- API catalog #33: `GET /api/v1/assignments/{assignment_id}`, Student Bearer, required int64 path only, `ApiEnvelope<Assignment>`, success 200 `DESIGN_RESOURCE_RETRIEVED`, errors 401/403/404/500. Reusable `Assignment` has `id`, `course_id`, `title`, optional `description`, optional `due_at`, `max_score`. API #33 DD is `Draft — Needs Confirmation`; Q-33-01…05 remain open for access, deadline/error mapping, submission-rule shape, nullability/timezone/decimal serialization, and path validation.
- Canonical UI target: `.agents/web-study/design.md` calls for no remote font imports, content width around 1120px, responsive reflow below 768px, and controls at least 44px high. This is intended design, not runtime evidence.
- Skill routing: `.agents/skills/INDEX.md` and `.agents/context-manifest.json` exclude `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only screen DD skill applies.

## CURRENT_BEHAVIOR

- Current Study Server source has no Student #33 GET route, #33 module, or #33 test. The Student module/test tree has only API #34 uploads; APIs #54–#57 are separate Mentor submission flows. Student #35/#36 route/module/test source is absent. API #34 is a source-backed local multipart `POST /api/v1/uploads`; `purpose=SUBMISSION` returns an UploadAsset reference. This does not establish live storage/schema/deployment.
- Study Web remains `UNWIRED`: editable `src/`, package manifest and Student routes are absent; the ignored `dist` search has no `/student/assignments` route.
- Legacy Study Server DDL and table notes contain BIGINT `assignments`/`assignment_submissions` candidates. The V1-PILOT `02_study_db.sql` contains no business assignment/submission tables; `service_role_assignments` is unrelated. There is no verified live schema or API #33 adapter.
- `screen.png` is a loaded Student assignment-detail mockup. `code.html` is a Guest/unavailable composition with login/register and a course link, not an assignment route view; no API/request or form behavior is present. Screenshot values for status, score weight, deadline, rubric, resources, mentor, SLA, checklist and submission history lack #33 fields.
- At 667px source width the PNG is dense and retains two-column content. The HTML loads remote Plus Jakarta Sans/Material Symbols and Tailwind CDN and uses a 1440px maximum width; these differ from the Study Web design target.

## SOURCE_TRACE

```text
Expected: list_screen.md ST-17 / F06 → AC-17 Student precondition → GET #33 Assignment + rule → server access/deadline decision → eligible CTA may hand off assignmentId to ST-18 → optional #34 UploadAsset → #35 creates Submission → #36 reads the submission receipt.
Current: no Study Web caller/route → no Student #33 route/module/query/test → no #33 response or access side effect. Current #34 is a multipart upload route/module/test that authenticates Student for purpose=SUBMISSION and returns an UploadAsset ID; it does not fetch an assignment or create a submission. Student #35/#36 route/module/test are absent; Mentor #54–#57 are distinct. Candidate `assignments` DDL is legacy BIGINT; V1-PILOT has no business assignment/submission tables; no live schema verification.
Assets: `screen.png` 667×1600, SHA-256 7ac187345ca89ef08462767a6269e91af888944d4a8b76494896596e1f6c7c86; `code.html` 9,745 bytes, SHA-256 82de50d864c0be013a198358a1f41de72acf032d18add1107114eb07c76580f6. Existing annotated PNG is 1718×3200.
Static: 49 sequential markers / 49 DD element rows / 49 SVG groups; all targets and badge centers unique and in bounds; SVG centers match JSON; final DD/plan links are checked after edits.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #33 expected contract vs current source | Catalog/API #33 DD Draft and AC-17 exist; no current Student #33 route/module/test; Study Web is UNWIRED. | UNWIRED / NOT_FOUND | No current result can be claimed; keep API and screen blocked. |
| Access, deadline and submission rule | AC-17 says assignment in time/authorized and reads an unspecified submission rule; diagram says 403/409, catalog #33 has no 409; Q-33-01/02/03 open. | DISCREPANCY / BLOCKER | Do not derive open/closed or CTA eligibility from client clock, mockup or unapproved fields. |
| Logical Assignment vs database artifacts | Legacy BIGINT assignments/submissions differ from V1-PILOT, which has no business assignment/submission tables; nullable legacy columns conflict with required logical fields. | DISCREPANCY | Source schema/adapter and live state remain unresolved. |
| Loaded design vs HTML and UI target | Student loaded PNG conflicts with Guest/unavailable HTML; dense 667px PNG and remote-font/CDN, 1440px HTML target differ from Study Web guide. | DESIGN DISCREPANCY | Preserve assets; approve canonical states and align final design before implementation. |
| Downstream AC-17 handoff | API #34 upload source exists; #35/#36 Student source absent; #34 does not create submissions or provide resource downloads. | PARTIAL / NOT_FOUND | ST-17 must hand off only `assignmentId`; later upload/submit/receipt contracts remain separate. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-17_chi-tiet-bai-tap/ST-17_PLAN.md` (re-audit, V1-PILOT source, post-edit audit); `ST-17.md` (schema/design/current handoff discrepancies); `apps/study-client/docs/list_screen.md` (ST-17 row and F06 handoff status); `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (ST-17 row and checkpoint); this worklog.
- ST-17 plan re-audit was saved before editing the DD, inventory or global tracker.
- Existing `screen.png`, `code.html`, `ST-17_markers.json`, `ST-17_markers_overlay.svg`, and `screen_annotated.png` were preserved; annotation files were inspected and statically checked. No ST-18/ST-19 screen DD/tracker row, API DD, DDL, or other Screen ID was edited.
- CONTEXT_UPDATES: none; no source/contract/global context page changed.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; 3 exact-type docs worklogs selected of 244; AD-01, AD-02, AD-03 fully read; ST-16 dependency worklog also read. | VERIFIED |
| Inventory / AC / catalog / API #33 DD review | ST-17–ST-19 rows, F06, AC-17 index and diagram, API #33 catalog plus Overview/Request/Response/Mapping/Error/Open Questions/Verification Report reviewed. | VERIFIED |
| Current source trace | No Student #33/#35/#36 route/module/test; API #34 route/module/test is current and scoped to upload. Study Web source/package absent; ignored dist has no assignment route. | VERIFIED_SOURCE_REVIEW |
| Database source review | Legacy assignment/submission DDL and table notes compared with V1-PILOT `02_study_db.sql`; no V1-PILOT business assignment/submission table; no live DB check. | VERIFIED |
| Asset and marker audit | Original PNG hash/dimensions match plan; HTML hash/size match plan; annotated PNG 1718×3200. 49 JSON markers, 49 SVG groups and 49 DD rows; unique/in-bounds targets and badge centers; SVG badge mapping matches JSON; raw and annotated images visually reviewed. | VERIFIED |
| Local Markdown links | Final DD 25 links and plan 18 links all resolve; no missing local targets. | VERIFIED |
| `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` | No whitespace errors in changed tracked files; separate authored-file scan found no trailing spaces in ST-17 DD, plan or worklog. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 / `AGENT_CONTEXT_INVALID`: missing db-admin context/source roots and stale manifests for db-admin, mobile-work, server-study, server-work, web-work and web-work/work-web. No ST-17 reference in validator output. | FAILED (repository-wide) |
| Application tests/runtime/live DB | Not run; this is a static screen-DD task and the per-screen plan does not authorize runtime/live DB claims. | NOT RUN |

## HANDOFF

- Remaining blockers: API #33 route/auth/access/deadline/rule/error behavior; legacy-to-V1-PILOT schema mapping and live schema; missing data for rubric/resources/status/mentor/history; loaded-vs-unavailable state and design-system mismatch; ST-17→ST-18 eligibility route; #35/#36 Student source.
- Status: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next owner/action: ST-18 in a separate session after ST-17; do not begin another Screen ID in this session.
