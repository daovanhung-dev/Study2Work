---
task_id: "2026-11-06-design-study-screen-st18"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-17 and APIs #33–#35; ST-17 → ST-18 → ST-19 handoff"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-18

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs selected of 180 exact-type docs worklogs; all selected files were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected behavior separate from current assets/API; preserve originals; Study Web is UNWIRED; unsupported behavior remains a blocker.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Do not infer URL sync, cache, or runtime from a prototype; record screenshot/HTML and contract discrepancies; do not claim unrun tests.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Distinguish source-backed API operations from missing routes and design-only declarations; preserve unresolved AC/API orchestration rather than reconciling by assumption.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Process only ST-18 in this session; write its plan before marker/DD artifacts; preserve the PNG/HTML originals; map all markers to DD elements; trace events, API/error/state/navigation; update tracker and worklog.
- Canonical sources: ST-18 inventory and F06 describe GET #33 → optional per-file #34 upload → collect asset refs → POST #35 → submission ID; states are editing/uploading/submitting/failed/submitted. AC-17 requires an eligible Student and in-deadline assignment and continues to #36/ST-19 after submission. Current #35 wire/data policy remains Draft.
- UI-only DD skill routing: machine registry excludes `web-ui-only-dd` from `createDD-markdown`; no canonical screen-DD skill applies.

## CURRENT_BEHAVIOR

- Original source hashes/dimensions: `screen.png` is 826×1600 RGB, SHA-256 `be8b06a7f90dc5febab40aab9e50b3e3a81740fc599f26958c5d0fd433d5e940`; `code.html` is 8,726 bytes, SHA-256 `8c0a81d5fbd1b2907bd9fe8d8b358ab3c8026f1200519ae44f12cd5a8299491c`.
- PNG shows a loaded sample form: delivery URL fields, checklist, 50 MB text, two sample uploaded files, mentor/review details, draft history/autosave, Markdown editor, integrity checkbox and submit controls. These values and copy are design content, not live user/assignment data.
- HTML is a static Guest unavailable fallback with placeholder `#` links and a return-link fragment; it has no input/form/script/API behavior and does not represent the loaded screenshot.
- Current Study Web has no editable app source/package/Student route; ignored dist contains only `/`; serving/deployment unverified.
- API #34 has a current FastAPI route/module/provider and test source. It accepts Student `SUBMISSION` or Mentor `LECTURE`, optional `course_id` for Student (ACTIVE enrollment is checked only when supplied), arbitrary bytes/MIME without application size cap, and stores a public-base URL plus metadata after streaming the object. Test sources exist but were not run; live DB/object storage/deployment are not verified.
- Student APIs #33 and #35 have no current route/module/test. #33 DD remains Draft. #35 DD remains Draft with unresolved field names/file-reference encoding, text rules, access/deadline/409, INSERT/UPDATE/idempotency, schema and response mapping. Current mentor #54–#57 submission APIs are separate actor/operations.
- Candidate `assignment_submissions` DDL has one `file_url`; logical Submission has `files[]`; no submission-upload association table was found. DDL/migration is not live-schema evidence.
- Tests/runtime: #34 test source read/searchable; no tests run; no Study Web or production/storage runtime inspected.

## SOURCE_TRACE

```text
Expected: ST-17 → GET #33 → eligibility/deadline decision → edit text/choose file
  → each needed POST #34 → gather asset references → POST #35 → submission ID → ST-19 / GET #36
Current: no Study Web screen route; #33/#35/#36 Student routes/modules/tests not found;
  #34 POST /api/v1/uploads is registered → create_upload → auth/purpose/course check
  → S3-compatible object write → INSERT uploads → commit → UploadAsset envelope;
  on storage failure 503; on DB failure rollback + best-effort object cleanup + 500.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| ST-18 PNG/HTML | PNG is loaded Student form; HTML is Guest fallback with no submission form or runtime behavior. | `DISCREPANCY` | Preserve both; use screenshot as design source only. |
| Study Web route | Editable app/package/Student router absent; ignored dist only has `/`. | `UNWIRED / NOT_FOUND` | No frontend event or navigation is current runtime. |
| API #33 | Catalog/DD exists; Student route/module/test absent; access/deadline/submission-rule mapping is open. | `DESIGN_ONLY / NOT_FOUND` | Form initialization/eligibility cannot be claimed as implemented. |
| API #34 UI constraints | Screenshot says 50 MB and lists accepted formats; current source accepts any bytes/MIME with no application cap. | `DISCREPANCY` | Do not describe the screenshot restriction as server-enforced. |
| API #34 course scope | Student `course_id` is optional; omission skips enrollment query. | `SOURCE_BACKED / POLICY GAP` | Do not silently omit/pass course context; required source and client decision remain open. |
| API #35 | No route/module/test; file refs, text validation, access/deadline, duplicate policy and physical persistence are unresolved. | `DESIGN_ONLY / NOT_FOUND` | Submission must remain blocked in the DD; no request mapping is invented. |
| Upload-to-submission persistence | #34 returns an asset ID/public URL; #35 catalog requires an opaque string; candidate DB has one `file_url`, logical schema has files[]. | `DISCREPANCY / SOURCE_REQUIRED` | No reference encoding, list cardinality or orphan-cleanup policy can be assumed. |
| Duplicate assignment read | ST-17 and ST-18 inventory both reference GET #33; AC-17 depicts the read before the form. | `DISCREPANCY / OPEN` | Cache, refetch and stale-deadline revalidation ownership are not defined. |
| Draft/URL/checklist/consent fields | Screenshot shows server autosave, history, repo/deploy URLs, rubric checklist and integrity checkbox; no matching #35 contract fields/endpoints. | `DESIGN_ONLY / SOURCE_REQUIRED` | No persistence, validation or gating is claimed. |
| Screen handoff | Inventory expects `submission_id`; API #35 response DD names `data.id`; #36 current Student route absent. | `DISCREPANCY / NOT_FOUND` | ST-19 navigation key/API read sequence needs contract alignment. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-18_soan-va-nop-bai-tap/ST-18_PLAN.md`, `ST-18_markers.json`, `ST-18_markers_overlay.svg`, `screen_annotated.png`, `ST-18.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- Original `screen.png` and `code.html` were preserved.
- CONTEXT_UPDATES: none planned; no source contract or context page changed.
- Context pages changed: none.
- Assumptions: none; unresolved mappings remain explicit.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Docs preflight | Selector returned READY, 3/180 exact-type docs worklogs; all three selected files read. | VERIFIED |
| Current source trace | Inventory, AC-17, #33/#34/#35 DD/catalog, current #34 route/view/provider/test source, DDL and Study Web source status inspected. | VERIFIED |
| ST-18 plan and artifacts | Plan was written before marker/DD; completed 60 ordered marker entries, a matching 60-row DD table, SVG overlay and 2036×3200 annotated PNG. The rendered annotation was visually inspected; markers stay in gutters and do not cover content. | VERIFIED |
| Static artifact/tracker audit | Original hashes preserved; marker coordinates are in source bounds; badge columns are outside screenshot and non-overlapping; SVG parses; 13 event IDs are sequential; sections A–F and all relative links resolve. Inventory is 83 IDs, 29 complete core bundles and 54 incomplete; ST-18 tracker status and ST-19 next pointer agree. Separate mentor pointer ME-03 is preserved. | VERIFIED |
| `git diff --check` and whitespace | `git diff --check` exited 0; changed text artifacts have no trailing whitespace. | VERIFIED |
| Tests/runtime | No tests or runtime checks run. | NOT_RUN |

## HANDOFF

- Remaining blockers: #33 access/deadline/rule contract; #34 upload limit/MIME and course_id policy alignment; #35 wire format, persistence, duplicate/retry/deadline and response; Study Web route/runtime absent.
- Next owner/action: ST-19 — Bài đã nộp và phản hồi, in a separate session; retain ME-03 as the independent next screen in mentor scope.
