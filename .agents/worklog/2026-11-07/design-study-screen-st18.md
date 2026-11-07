---
task_id: "2026-11-07-design-study-screen-st18"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-17 assignment detail → ST-18 upload/API #34 → ST-19 submission receipt/API #36; AC-17; API #35"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-18

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 245; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current source evidence separate; don't infer UI behavior from mockups; trace authorization, query/effects, response and tests; distinguish source from runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Preserve original assets; do not invent API fields/actions; fake DB tests do not prove live schema/deployment; keep Study Web `UNWIRED` until editable route/client source exists.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use current source-backed fields; keep role/privacy/API discrepancies open; distinguish local API source from runtime verification.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st17.md`
    - carry_forward: ST-17 remains DD/implementation blocked; only `assignmentId` may be carried forward pending eligibility contract; #34 is upload only, #35/#36 Student routes are absent; preserve upload-success vs submission-success boundary.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-18 only in this session; re-audit its existing plan before editing DD/trackers; preserve source assets; verify marker-to-element map; maintain traceable A–F DD; update ST-18 inventory/global tracker and F06 only where directly related; distinguish DD, implementation and runtime status.
- Inventory row 32 and F06: ST-17 #33 → per-file #34 upload if needed → collect asset references → #35 submission → ST-19 #36 receipt. F06 explicitly separates upload success from submission success and leaves retry/orphan/size/MIME/draft-preservation decisions open.
- AC-17: Student with permission and assignment in time; load Assignment/rule, check eligibility, upload via #34, create SUBMITTED submission via #35, then #36 receipt. Diagram shows #36 before the “submitted” display, while inventory assigns #36 to ST-19; preserve the owner/order discrepancy.
- Catalog #34: `POST /api/v1/uploads`, Bearer; multipart `file` and `purpose`, optional `course_id`; 201 `ApiEnvelope<UploadAsset>` with `id,name,url,content_type,size_bytes,status`; errors 401/403/422/503/500. Current API #34 DD is `Draft — Ready for Review`.
- Catalog/API #35: Student Bearer, `POST /api/v1/assignments/{assignment_id}/submissions`, required `text:string` and catalog token `file refs:string`, 201 `ApiEnvelope<Submission>`, errors 401/403/404/409/422/500. API #35 DD is Draft; Q-35-01…08 retain wire-format, validation, eligibility/deadline, resubmission, file-persistence, status/time/schema and idempotency questions.
- Current screen contract remains design evidence; no new API, validation, upload cap, MIME rule, retry/idempotency behavior or draft retention may be inferred.

## CURRENT_BEHAVIOR

- API #34 is registered as `POST /api/v1/uploads`; `api_34_uploads` has models/validator/view/query plus an S3-compatible storage provider. `create_upload` validates Student/Mentor Bearer roles and matches role to `SUBMISSION`/`LECTURE`; supplied Student `course_id` checks ACTIVE enrollment, while omitted `course_id` skips that lookup. The source measures byte size, resets stream, uploads a server UUID key, inserts `uploads` metadata, commits and returns `UploadAsset(status=UPLOADED)`. It accepts any bytes/MIME and has no application size cap; missing filename/MIME use `upload`/`application/octet-stream`. Storage failure maps to 503; metadata/size errors map to 500 with rollback/best-effort object deletion. Test source covers role, scope, parsing, fallback, storage and DB failure paths but was not run this session.
- API #34 DDL/migration 004 use legacy BIGINT `uploads`; V1-PILOT `infra/postgres/02_study_db.sql` has no business `uploads`, `assignments` or `assignment_submissions` tables (`service_role_assignments` is unrelated). Legacy candidate `assignment_submissions` contains one nullable `file_url`, unlike logical `Submission.files[]`; no submission-upload association was found. Live database/schema, migration deployment, credentials, object-storage connectivity and runtime are not verified.
- Current source search finds no Student #33/#35/#36 routes, modules or tests; Mentor `/mentor/submissions*` routes are distinct. Study Web has no editable `src/`, package manifest or Student route; ignored `dist/` contains only `index.html` with `/`. Serving/deployment remains unverified.
- Assets rechecked: `screen.png` is 826×1600, hash `be8b06a7f90dc5febab40aab9e50b3e3a81740fc599f26958c5d0fd433d5e940`; `code.html` is 8,726 bytes, hash `8c0a81d5fbd1b2907bd9fe8d8b358ab3c8026f1200519ae44f12cd5a8299491c`. PNG is a loaded Student form; HTML is a Guest/unavailable fallback with a hash assignment-detail link, no form/API/screen-specific interaction, plus Tailwind config/CDN and remote Google Fonts. Sample fields/values are not runtime data.
- Plan/DD review found one incorrect requirement statement: F06 does not require keeping form data on error. It requires upload/submission success to remain separate and lists draft preservation as unresolved. The plan and DD now keep retention unresolved.

## SOURCE_TRACE

```text
Expected: ST-17 assignment context → ST-18 uploads each needed file with API #34 → collect confirmed asset reference(s) → API #35 creates submission → ST-19 reads receipt via #36.
Current: Student/API #34 route → `create_upload` → shared Bearer guard + purpose/supplied-course policy → optional ACTIVE-enrollment query → S3-compatible object upload → legacy BIGINT `uploads` INSERT/commit → `ApiEnvelope<UploadAsset>`; no Student #33/#35/#36 or Study Web caller/route. Fake-provider/session test source exists; live DB/storage and deployment are unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| F06 form retention | `list_screen.md` F06 separates upload/submission success and says draft-preservation decisions need confirmation; it does not mandate retaining the form after errors. | DISCREPANCY (previous plan/DD wording) | Correct the unsupported requirement and keep retention policy open. |
| API #34 current source vs screen design | Local route/module/provider/test source; no application size/MIME cap; optional `course_id`; public-base URL. PNG claims 50 MB and formats. | SOURCE-BACKED LOCALLY / DESIGN DISCREPANCY | Document source behavior only; do not promote mockup limits or expose preview without access policy. |
| API #35 submission contract | Catalog and Draft DD only; no Student route/module/test; file-reference key/encoding/cardinality, `data.id` vs `submission_id`, persistence and retry remain open. | DESIGN ONLY / NOT_FOUND | Do not build request mapping, save-draft behavior or success state from assumptions. |
| AC-17 #36 ownership/order | AC diagram reads #36 after #35 before “submitted”; inventory assigns #36 to ST-19. | DISCREPANCY | Keep the call/screen boundary open; do not silently call #36 from ST-18. |
| Study DB candidate vs V1-PILOT | Legacy BIGINT DDL/migration has uploads/assignment candidates; V1-PILOT has no business equivalents; live schema is unverified. | DISCREPANCY | No adapter, association or runtime persistence claim. |
| Design assets and Study Web | Loaded Student PNG vs Guest/unavailable HTML/hash target; remote fonts/CDN and 1440px HTML width differ from Study Web design target; app source/router absent. | DESIGN DISCREPANCY / UNWIRED | Preserve assets; no route/runtime claim; align approved design before implementation. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18_PLAN.md` (pre-edit re-audit and final source references); `ST-18.md` (F06 correction, current #34 trace, asset/route/design discrepancy, event and state handling, checklist); `apps/study-client/docs/list_screen.md` (ST-18/F06 row and #034 D→R status); `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (ST-18 row/checkpoint); this worklog.
- Existing `screen.png`, `code.html`, `ST-18_markers.json`, `ST-18_markers_overlay.svg`, and `screen_annotated.png` were preserved; original PNG/HTML hashes are unchanged. Marker JSON/SVG/annotated PNG existed before this session and were verified, not edited. No other Screen ID, API DD, code or schema was changed.
- CONTEXT_UPDATES: none; no source/API/schema contract changed.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Objective read first; root router, context-map, worklog contract/template read; exact docs selector `READY`, 3/245 selected and fully read (AD-01/02/03); ST-17 dependency worklog fully read; no shortage. Registry confirms UI-only DD has no canonical skill. | VERIFIED |
| Inventory/AC/catalog/API DD review | ST-18 row, F06, AC-17 diagram, API #34 catalog/DD and API #35 request/response/open questions reviewed. AC-17 #36 call position differs from inventory's ST-19 ownership. | VERIFIED |
| Current source trace | #34 route/module/provider and test source present; Student #33/#35/#36 routes/modules/tests absent; Mentor submission routes are distinct; Study Web editable source/package/Student route absent and ignored dist only has `/`. Test source was read, not run. | VERIFIED_SOURCE_REVIEW |
| Database/storage source review | Legacy BIGINT uploads/assignments/submissions artifacts and upload migration 004 compared with V1-PILOT `02_study_db.sql`; V1-PILOT has no business assignment/upload/submission tables. No live DB/storage check. | VERIFIED |
| Asset and marker audit | `screen.png` 826×1600/hash unchanged; `code.html` 8,726 bytes/hash unchanged; annotated PNG 2036×3200. 60 sequential unique markers = 60 DD rows = 60 SVG groups; JSON/SVG badges match; targets unique/in bounds; badges remain in side gutters and minimum center spacing is 25px. Raw and annotated PNG visually reviewed. | VERIFIED |
| Markdown links / DD structure | DD has A–F and 13 sequential events; all event refs resolve; DD has 19 local links and plan has 15, with no missing targets. | VERIFIED |
| Inventory artifact scope | 83 unique IDs match 83 folders; 82/83 have the six required core artifacts (ST-01 is the only incomplete bundle); ST-18 is complete. | VERIFIED |
| `git diff --check` / authored whitespace | Scoped check for changed tracked inventory/tracker passed; authored ST-18 DD/plan/worklog and global tracker have no trailing whitespace. | VERIFIED |
| `node scripts/validate-agent-context.mjs` | Exit 1 / `AGENT_CONTEXT_INVALID`: db-admin context/source roots are missing, with broken db-admin context links; scope manifests are stale for server-study, server-work, web-work, web-work/work-web, mobile-work and db-admin. Validator output contains no ST-18 reference. | FAILED (repository-wide) |
| Application tests/runtime/live DB | Not run; this is a screen-DD documentation task and the request requires static verification, not application behavior tests. | NOT_RUN |

## HANDOFF

- Remaining blockers: #33/#35 Student source and eligibility/schema contracts; #34 optional course scoping, public URL policy and no limits; #35 file-reference and submission lifecycle/idempotency/ID mapping; AC-17 #36 ownership; draft retention; legacy/V1 schema mismatch; Study Web route and visual design discrepancy.
- Next owner/action: ST-19 in a separate session; do not begin another Screen ID in this session.
