---
task_id: "2026-11-06-design-study-screen-me04"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: ["test"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ME-04 takes courseId from ME-03/#46, uploads through API #34, creates via API #47 and hands lectureId to ME-05/API #48"]
status: "VERIFIED"
---

# Worklog: Detailed Design Study ME-04 — Tải lên và tạo bài giảng

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; selector returned 3 exact-type docs logs of 184; all were read.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep expected/current separated, preserve original screen/HTML, no Study Web runtime inference, and trace category/client interactions to current source.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Keep unsupported prototype fields/routes explicit; a source-backed API does not prove UI wiring or deployment; one Screen ID per session; no tests/runtime claim without execution.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Distinguish route/source/tests/runtime, respect API catalog vs current backend discrepancies, preserve image and HTML, and do not apply `createDD-markdown` to UI-only DD.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ME-04 only in this session; plan before marker map, annotation and DD; preserve original PNG/HTML; map every numbered element; detail every event/API/state/route; update global `dd_screens/PLAN.md` and this worklog; separate `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED` statuses.
- Canonical inventory: `apps/study-client/docs/list_screen.md` row ME-04 proposes `/mentor/courses/:courseId/lectures/new`, AC-21, API #46 context → #34 uploads → #47 create; links ME-05/ME-03; expected states `draft/uploading/creating/422/error` and explicitly warns against mapping `content:int64` to rich-text without confirmation.
- Goal objective attachment read: `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md`; scope is all 83 screens, one Screen ID per session, static source trace, annotation/marker/DD and status tracking.
- Skill boundary: `.agents/context-manifest.json` and `.agents/skills/INDEX.md` exclude `web-ui-only-dd` from `createDD-markdown`; no canonical UI-only DD skill applies.

## CURRENT_BEHAVIOR

- Assets: `screen.png` is 1175×1600, SHA-256 `5c95672f8912580f0dc932bccb233075cab6a29f5ea1ff789c93ea03abb960eb`; `code.html` is 42,754 bytes, SHA-256 `489fb9dae33dc172d2d11375ac60da2a2f5341fe4cabb11a622729ba26f5f925`. Image was visually inspected. The HTML is a static mockup with 7 `#` anchors, 22 buttons, 11 inputs, one select; no form, file input, textarea, `contenteditable`, fetch/XHR or API request. Its one submit handler fakes a success message after 900 ms; auto-save is static copy. Original assets remain unchanged.
- Study Web root was rechecked; `src/`, root `package.json` and router are absent. `dist/` is ignored and does not prove feature route or serving/runtime.
- API #46 route is registered: MENTOR Bearer JWT, optional DRAFT/PUBLISHED status, `page=1`, `size=20` max 100; current query only direct `courses.mentor_id` owner and returns paginated `Course` fields. It has no per-course detail lookup or module hierarchy.
- API #34 route is registered: `POST /api/v1/uploads`, multipart `file`, `purpose`, optional `course_id`. Mentor must use `LECTURE` and a directly owned course. Current source accepts arbitrary bytes/MIME without an application size cap, writes an S3-compatible UUID object then commits legacy BIGINT `uploads` metadata; returns UploadAsset ID/name/url/content_type/size_bytes/UPLOADED. Storage failure maps 503; DB failure rolls back metadata and attempts object cleanup. Real storage, live DB and deployment were not checked.
- API #47 route/module is now registered/source-backed locally, despite stale API #34 `PLAN_RESULT.md` saying #47 is UNWIRED. Current strict body is `{title<=200, content:int64, asset_refs:string(JSON array of unique signed-int64 IDs), order:int32}`. It checks MENTOR auth and direct course owner, resolves assets for same owner + `LECTURE` + same course, inserts lesson with `content=str(int64)`, fixed `PUBLISHED`, `order -> sort_order`, and ordered `lesson_uploads` links in one transaction. Success is 201 `DESIGN_RESOURCE_CREATED`; errors 401/403/404/422/500. Current local #47 DD remains Draft due unverified live schema/migrations.
- API #48 is registered and source-backed locally: MENTOR auth, direct owner check, then lecture + ordered upload details; 200 success, 401/403/404/500. It is the ME-05 handoff, not a create API.
- AC-21 precondition allows owner/assigned course while #46/#34/#47 require direct owner. Screenshot uses a sample course code, module picker, order, duration, difficulty, rich-text/code editor, media URL, type, preview/prerequisite flags, draft/publish and QA data. Those fields are absent from #47 request/response; API #47 creates PUBLISHED immediately. Screenshot's 2 GB/type policy also differs from #34 source. No upload deletion endpoint was found; #34 upload commits before #47, so a later cancel/failure cannot roll back uploaded assets.
- Checked-in DB.sql/migrations are legacy schema artifacts (`lessons`, `uploads`, `lesson_uploads` BIGINT); live schema/deployment is not verified. Focused #34/#46/#47/#48 test modules and coverage summaries were inspected; tests were not run in this docs-only session.

## SOURCE_TRACE

```text
ME-03 / direct route entry
  -> proposed /mentor/courses/:courseId/lectures/new
  -> API #46 GET /mentor/courses (MENTOR; paged direct-owner Course list)
  -> UI course selection/context remains blocked for assigned-course and detail lookup
  -> API #34 POST /uploads multipart(file, purpose=LECTURE, course_id)
  -> direct-owner check -> Object Storage UUID object -> INSERT uploads -> commit
  -> UploadAsset{id,...,status=UPLOADED}; object/meta persist independently
  -> API #47 POST /mentor/courses/{course_id}/lectures JSON strict body
  -> MENTOR/direct-owner check -> resolve same-owner/course LECTURE assets
  -> INSERT lessons(content=str(int64), status=PUBLISHED) + ordered lesson_uploads
  -> commit -> 201 Lecture{id,...}; safe 401/403/404/422/500
  -> proposed ME-05 route /mentor/lectures/:lectureId -> API #48 GET detail
  -> local route/source/tests exist; browser wiring, live DB and runtime unverified
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-21 course access | AC allows owned/assigned; current #46/#34/#47 query/check direct owner only. | DISCREPANCY / BLOCKER | Assigned Mentor access cannot be specified as current behavior. |
| Rich-text/editor vs #47 | UI edits Markdown/WYSIWYG/code; #47 accepts int64 and stores decimal string. | DISCREPANCY / BLOCKER | No content mapping is approved for this editor. |
| Draft/review vs #47 | UI offers Draft and review; #47 creates PUBLISHED only. | DISCREPANCY / BLOCKER | Cannot implement displayed lifecycle from current API. |
| Module/order/duration/type/URL/preview/prerequisite/QA | Screen contains fields; #47 schema and #46 projection do not. | SOURCE_GAP / BLOCKER | Do not invent fields, policy, validation or persistence. |
| Upload acceptance/lifecycle | UI shows type/size constraints and remove; #34 source has no app cap/allowlist and no delete route; upload commits before #47. | DISCREPANCY / BLOCKER | File policy, orphan cleanup and cancel/retry behavior need approval. |
| Study Web route/runtime | No editable app source/package/router; HTML only simulates CTA success. | UNWIRED | No current browser behavior or runtime verification. |
| API #47 documentation | Current registered source/tests vs old #34 Plan_Result “UNWIRED”; current #47 DD remains Draft for live schema. | DOC/SOURCE DISCREPANCY | Prefer current source for local behavior; do not treat local DD as deployed contract. |
| Schema/deployment | Legacy DDL/migrations are checked-in artifacts; no live metadata queried. | NOT_VERIFIED | Backend runtime/database behavior remains outside this session's evidence. |

## CHANGES

- Files changed: ME-04 `ME-04_PLAN.md`, `ME-04_markers.json`, `ME-04_markers_overlay.svg`, `screen_annotated.png`, `ME-04.md`; global `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog. Original `screen.png` and `code.html` are unchanged.
- CONTEXT_UPDATES: None; no API implementation, contract or context convention was changed. UI-only DD has no wired canonical authoring skill.
- Context pages changed: None.
- Assumptions: None. Mockup content without a source is marked unsupported or blocked.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + selected log review | Selected 3 exact-type logs; all reviewed; no shortage. | VERIFIED |
| ME-04 expected/current source review | Inventory, AC-21, API #34/#46/#47/#48 route/module/contract/DD/test sources, Study Web source presence and checked-in DDL/migrations reviewed. Tests not executed. | VERIFIED_SOURCE_REVIEW |
| Final plan-first order | Original plan was written before artifact creation; final marker coordinates were saved before regenerated JSON/SVG/PNG and the final DD update. | VERIFIED |
| Static marker/artifact audit | 60 ordered unique marker rows match JSON coordinates, SVG groups and 60 DD element IDs; 21 sequential events; coordinates in 1175×1600 bounds; annotated PNG 2350×3200; closest marker centers 26 px; final image visually reviewed after regeneration; original asset hashes unchanged. | VERIFIED_STATIC |
| Link/format/tracker audit | Local Markdown links resolve; no trailing whitespace; focused `git diff --check` clean; tracker row/status and 32/83 progress updated. | VERIFIED_STATIC |
| Context validation | No `.agents/` page or manifest was changed. | NOT_REQUIRED |
| Tests/runtime | Tests and Study Web runtime were not run. | NOT_RUN |

## HANDOFF

- Screen statuses: `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Worklog `VERIFIED` means source/artifact static audit is complete; it does not mean DD READY or runtime verification.
- Remaining blockers: ME04-B01–B11 in `ME-04_PLAN.md` / `ME-04.md`, especially owner vs assignment access, rich-text content mismatch, immediate PUBLISHED lifecycle, unsupported metadata, upload cleanup/idempotency, and unverified live schema/storage.
- Next Screen ID: ME-05 in a separate session; no second Screen ID was authored here. Global tracker is 32/83; ST-20 stays a separate flow.
