---
task_id: "2026-11-07-design-study-screen-gs05"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-05 course-review tab ↔ GS-03 course gate, AC-05/API #08/#10 and public discussion/review data boundary"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-05

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 261; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; trace UI, API, auth, DB and tests independently; keep Study Web UNWIRED; do not infer live behavior from mockup or fake DB tests.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Keep screen copy/actions separate from API fields; preserve Draft contracts, identity/permission and schema blockers; no current route/client without source evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use only explicit ID/data handoffs; distinguish API catalog and AC from current route/query/response; preserve public/private and PII questions; do not claim tests/runtime/live DB verification.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Process GS-05 only in this session; re-audit its existing plan before DD, marker, image or tracker edits; preserve source assets; verify ordered one-to-one markers and complete event input/process/output/error definitions; trace APIs and linked screens; update inventory, global plan and this worklog; distinguish DD readiness, implementation status and runtime verification.
- Current inventory row 12 proposes `/courses/:courseId?tab=reviews`, AC-05, APIs #08/#10, links GS-03, paginated public review/reply list, course-404-vs-empty behavior and loading/empty/ready/error states; it suppresses average stars without a rating contract. AC-05 calls #08→#09→#10 and asks for aggregate rating; F02 says lazy tab loads; GS-05 row requires #08 reuse and paginated #10. Keep those distinct where they conflict.
- API catalog #10 declares public GET `/api/v1/courses/{course_id}/reviews`, `course_id:int64`, optional `page:int32` and literal “rating filter?:string”, `ApiEnvelope<Page<Discussion>>`, and 200/404/500. API #10 DD is Draft — Needs Confirmation, with unresolved `Discussion.title`, rating/filter/aggregate, `ACTIVE` visibility, page-size/order and malformed query behavior.

## CURRENT_BEHAVIOR

- GS-05 bundle currently has source `screen.png` 1280×1024 (SHA-256 `f6e8edf78933bc5b54a20bb135ce11f3a7b5937c368dd6a583356c2aabc90538`), source `code.html` (SHA-256 `e7072487f43a4e19e5faf9593f633b7db3d05f98a6806f753feca1fb59b49512`), HTML-derived `screen_rendered.png` 1440×1200, annotated PNG 3040×2400, nine-marker JSON/SVG, plan and DD. Visual review confirms original PNG is near blank; the HTML render shows only static header/breadcrumb/empty card/CTA/footer; gutter markers are legible and do not cover page content. Preserve both source assets.
- HTML anchors all use `href="#"`; no form, route binding, API request, state, pagination or event handler exists. It loads remote font/icon/Tailwind resources in the static prototype. Study Web current tree has docs/assets, ignored `dist`, `node_modules` and a build-info file, but no editable `src`, package manifest or feature router; keep `UNWIRED`.
- API #08 is current public `GET /courses/{course_id}` with route `str` path parsing via shared `parse_integer`; Q reads a `PUBLISHED` course with LEFT JOIN mentor, then maps singleton `Page<Course>`. Invalid/missing/unpublished gives 404; SQLAlchemy query failure rolls back and returns safe 500. Focused fake-session test source covers ordinary/invalid ID, not found, DB error, success and one TestClient route composition; it was read only and not run.
- API #10 remains catalog/Draft only: current `v1.py`, module tree and test tree contain no matching reviews route/module/tests. Current #97/#98 are ADMIN discussion moderation queue/detail routes, not a Guest course-review replacement. Study OpenAPI path is a placeholder. #10 DD explicitly says `title` has no `discussions.title` source, no course-rating/aggregate field exists, and its `parent_id IS NULL` plus `status='ACTIVE'` root/reply rules are assumptions.
- Checked-in legacy `DB.sql` candidate defines `discussions(id, course_id, user_id, parent_id, content, status, created_at, updated_at)` without title or rating. V1-PILOT `02_study_db.sql` has `assessment_reviews`/`assessment_review_scores` tied to assessment attempts, not a course-review relation; it does not resolve #10. Server context says live schema is not verified.
- AC-05 diagram sequences #08→#09→#10 and requests aggregate rating; F02 and GS-05 inventory specify lazy-by-tab and reuse #08. AC-05 includes a 404/403 course branch; #08 current source returns 404 for invalid/missing/unpublished, while #10 catalog lists only 404/500. These remain discrepancies, not UI implementation choices.

## SOURCE_TRACE

```text
Expected: GS-03 supplies the same `courseId` → GS-05 reviews tab; approved course gate → public #10 page request → review/reply list or empty state, distinct from missing/unpublished course; AC-05 additionally asks for aggregate rating.
Current: Study Web has no route/client/cache caller. #08 source gates on PUBLISHED and returns 404/500 as described above. #10 is declared/Draft only, with no runtime route/module/test or Study OpenAPI. Current legacy discussion DDL lacks title/rating; V1-PILOT assessment reviews are unrelated to course reviews; live schema is unverified. HTML is a static empty-like prototype with placeholder anchors.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #10 runtime | Catalog and Draft DD exist; focused source search found no current route/module/test; Study OpenAPI is a placeholder. | DECLARED_NOT_RUNNABLE | Do not document #10 as a working request. |
| Review/title/rating/visibility | Draft requires title without source; no course rating/aggregate; `ACTIVE` visibility and root/reply hierarchy are assumptions. | DISCREPANCY / BLOCKER | Do not invent review title, rating or public moderation policy. |
| Database | Legacy discussions lack title/rating; V1-PILOT assessment review tables are attempt-scoped; live schema not verified. | DISCREPANCY / NOT VERIFIED | Neither DDL candidate proves a public course-review source. |
| Orchestration and UI | F02 lazy tab conflicts with AC-05 eager sequence; inventory also asks #08 cache reuse. Loaded/error/page UI absent; Study Web UNWIRED. | OPEN / UNWIRED | Keep cache, direct-entry and event design unresolved. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_PLAN.md`, `GS-05.md`, `apps/study-client/docs/list_screen.md` (GS-05 row), `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (GS-05 row and re-audit checkpoint), this worklog. No source images or application code changed.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Docs worklog preflight | Selector `READY`; selected AD-01, AD-02 and AD-03 worklogs read in full. | VERIFIED |
| GS-05 source/contract audit | Current inventory, AC-05, F02/G-06, API catalog/#10 Draft DD, #08 route/validator/query/view/model/test source, #97/#98 Admin route boundary, legacy and V1-PILOT DDL, Study Web tree and source assets reviewed; test source only. | VERIFIED_SOURCE_REVIEW |
| Visual asset review | Original, rendered and annotated PNGs reviewed; original hashes and dimensions match plan. | VERIFIED |
| Static artifact audit | All 8 bundle files present; source hashes match; 9 ordered markers map 1:1 to DD rows and SVG labels/centers in gutter bounds; SVG embeds exact render; 8 events have type/trigger/precondition/input/process/output/error; A–I and links pass; 83 inventory/tracker/folder IDs match. | VERIFIED |
| Whitespace / `git diff --check` | Authored GS-05 DD/plan/worklog have no trailing whitespace; scoped `git diff --check` on modified tracked inventory/tracker exited 0. | VERIFIED |
| Application tests / runtime / live DB | Not run or verified. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #10 remains DECLARED_NOT_RUNNABLE; `Discussion.title`, course rating/aggregate, filter semantics and public root/reply policy lack approved source; loaded/pagination/error UI absent; AC-05 eager/aggregate/404-403 conflicts with F02 lazy and #08 source; cache/direct-entry behavior unresolved; Study Web UNWIRED and live schema unverified.
- Next Screen ID: GS-06 in a separate session after GS-05 audit completion.
