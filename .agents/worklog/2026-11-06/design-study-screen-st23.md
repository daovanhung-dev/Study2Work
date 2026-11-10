---
task_id: "2026-11-06-design-study-screen-st23"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-23 -> ST-24/ST-25; AC-19 -> API #39; API #39 contract and Study Server runtime"]
status: "VERIFIED"
---

# Worklog: ST-23 discussion list screen DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`, 3/188 exact-type docs worklogs selected; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Preserve expected/current separation; list source-backed UI elements only; record open decisions as blockers.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Keep static HTML/prototype evidence distinct from runtime and API wiring; retain source assets and hash evidence.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Use unique ordered markers with exact DD mapping; do not promote design-only API fields or behaviors to verified runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete one screen this session, ST-23, with a detailed plan, preserved source image, annotated image, marker map, DD sections A–F, tracker update, and traceable unresolved decisions.
- Canonical contract/approved DD: Inventory ST-23/F07, AC-19 and API catalog #39. API #39 is GET `/api/v1/discussions`, Student Bearer, optional `course_id:int64`, `page:int32`, `sort:string`, `ApiEnvelope<Page<Discussion>>`, catalog codes 200/401/403/500. API #39 DD remains Draft/Needs Confirmation; its seven open questions and the title/DDL mismatch are blockers, not approved behavior.

## CURRENT_BEHAVIOR

- Source/config: ST-23 directory originally had blank `screen.png` and static empty-state `code.html`. HTML has no list, filter, sort, create CTA, pagination, API call, auth guard, event handlers, or data binding. Study Web runtime is UNWIRED; Student API #39 route/module/query/test is NOT_FOUND. Admin discussion routes #97/#98 are a different actor/scope.
- Runnable tests: No ST-23 Student API or Study Web tests found; no tests run.
- Runtime wiring: Not verified. `screen_rendered.png` is a Chrome 155 static render of the existing HTML, not app/runtime evidence.

## SOURCE_TRACE

```text
Student route (inventory only; current Study Web router absent)
  -> expected GET API #39 /api/v1/discussions (catalog only; current Student route/module/query/test NOT_FOUND)
  -> expected discussion repository/DB projection (no #39 caller/callee to trace; checked-in legacy DDL has nullable course_id/user_id and no title)
  -> expected ApiEnvelope<Page<Discussion>> with catalog codes 200/401/403/500
  -> no Student #39 tests; Admin #97/#98 tests are not evidence for this flow
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Screenshot source unusable | Original `screen.png` is 1280x1142 blank/pale bands; HTML is a static empty-state prototype. | Source preserved; rendered substitute documented | Annotated image uses a separately rendered HTML artifact; this is not runtime verification. |
| Expected loaded list controls absent | Inventory expects course filter, sort, create and list; HTML has only empty state. | DISCREPANCY | No unsupported controls/markers/events are added. |
| API #39 unimplemented | No Student route/module/query/test; API DD is Draft with seven open questions. | DECLARED_NOT_RUNNABLE / NOT_FOUND | API mapping and implementation remain blocked. |
| Discussion projection mismatch | API catalog requires `title`; checked-in DDL has no title column, and course_id is nullable. | BLOCKER | No title/content inference or visibility policy is invented. |
| ST-24 handoff uncertainty | API #40 catalog body says `content:int64`, while AC/UI intent is text content. | BLOCKER | No create submission is specified from ST-23. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/03_student/ST-23_danh-sach-thao-luan/{screen_rendered.png,screen_annotated.png,ST-23_markers.json,ST-23_markers_overlay.svg,ST-23_PLAN.md,ST-23.md}`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; this worklog.
- CONTEXT_UPDATES: None; no `.agents` context page or registry changed.
- Context pages changed: None.
- Assumptions: Original blank PNG remains the source artifact. A separate HTML render is used as the visual basis because the source PNG is unusable; source hashes and renderer are recorded. No API defaults, database runtime facts, or unapproved behavior are assumed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Static consistency audit (Python stdlib: asset hashes/PNG dimensions, JSON/SVG parse, marker sequence/bounds/1:1 DD mapping, A–F sections, 10 event fields, API fields/codes, local Markdown links) | All checks passed. | PASS |
| Visual inspection of `screen_annotated.png` | 15 ordered markers visible; no important content obscured. | PASS |
| `git diff --check` | Passed after the final tracker and worklog updates. | PASS |
| Tests/runtime | Not run; user requested DD documentation and no runnable ST-23 Student UI/API exists. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #39 seven open questions, `Discussion.title` source, comments boundary, loaded-list/filter/sort/create design, Study Web route/UI wiring, Student API #39 runtime, and ST-24/API #40 content type mismatch.
- Next owner/action: Product/API owner resolves #39 and #40 contract questions; frontend/backend implementation follows approved contract. Next screen in a separate session is ST-24.
