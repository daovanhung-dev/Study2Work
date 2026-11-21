---
task_id: "2026-11-06-design-study-screen-st09"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-08 enrollment handoff/API #20; ST-09 APIs #09/#37; ST-10 access/start APIs #22/#23/#24; ST-21 progress detail; Study Web built artifact/source boundary"]
status: "PARTIAL"
---

# Worklog: Detailed Design màn hình Study ST-09

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: node scripts/select-worklogs.mjs --type docs --limit 3
- selector_result: READY; 3 exact-type docs worklogs of 170 selected; no shortage.
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-11-06/design-study-screen-gs01.md
    - carry_forward: Separate expected from current behavior; keep Study Web feature routes UNWIRED; preserve source hashes and do not treat static design as runtime.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs02.md
    - carry_forward: Trace current backend source independently from API catalog; preserve route/field discrepancies; one screen ID per session.
  - path: .agents/worklog/2026-11-06/design-study-screen-gs03.md
    - carry_forward: Preserve assets; distinguish source-backed backend endpoints from missing frontend wiring; do not invent product or access behavior.
- shortage: none

## EXPECTED_BEHAVIOR

- User objective file read: /home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md. One Screen ID per session; plan before DD/annotation; produce original and annotated image, marker map, DD with element/event/API/state/acceptance traceability; preserve evidence boundaries and blockers.
- Inventory expects Student course overview at /student/courses/:courseId (AC-13/AC-18), with enrollment gating (#20), progress (#37), public curriculum (#09), lesson access/start path to ST-10 (#22–#24), and a relationship to ST-21 progress detail.
- AC-18 expects aggregate lesson, quiz and assignment progress; no formula is specified.
- Current canonical evidence and open questions are recorded separately in ST-09_PLAN.md and ST-09.md.

## CURRENT_BEHAVIOR

- ST-09 source PNG 1397×1600 SHA256 8b37e1c7dc459ab7a9ab87161f0990d259abf9291c7f3a85b4a05c3324ba7a7d; HTML SHA256 554e2fdc52b3fe01cbaf560f7525dca1742a0413b889882569c3d865a699bc46. Both retained unchanged.
- PNG/HTML represent a static gated handoff; no data fetch/auth/router. All anchors use href=#; CTA has no lessonId; clipboard handler copies a literal route template.
- API #09 is source-backed in Study Server: parse course_id, require PUBLISHED course, list PUBLISHED lessons sorted by sort_order/id, return Page<Lesson> with content and video_url nullable; no auth/enrollment gate. Test source was read but not run.
- #20/#37 and #22–#24 have no current route/module/query/test source. #20/#37 catalog response is ApiEnvelope<UserProfile>, insufficient to describe courses/progress.
- Study Web editable app source/package/router absent. Ignored compiled dist contains one / route and no Student course/progress routes/calls; provenance/serving unknown.
- Context pages were updated this turn to distinguish ignored dist artifact from source/runtime: .agents/web-work/study/AGENTS.md, .agents/web-work/study/INDEX.md, .agents/web-work/AGENTS.md, .agents/web-work/INDEX.md, .agents/web-study/design.md, .agents/project/architecture.md, .agents/project/dependencies.md, .agents/context-map.md.

## SOURCE_TRACE

- Screen route: expected inventory path → no editable Study Web router/source → no runtime screen.
- API #09: apps/study-server/app/api/v1.py route → get_course_curriculum → validate_course_id → published-course query → published-lesson query and mapping → ApiEnvelope<Page<Lesson>>; module test source exists and was read, not executed.
- APIs #20/#37/#22–#24: catalog/inventory declarations → search current Study Server app/tests → no route/module/query/test found.
- ST-08/ST-10/ST-21: inventory routes and relationships; source assets do not establish card/lesson/progress-detail handoff.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #09 badge | Screenshot says D; route/module/query/test source exists. | DISCREPANCY; SOURCE_BACKED | Keep screenshot unchanged; document source truth and stale badge. |
| API #09 access | Current public handler returns lesson content/video_url without enrollment check. | SOURCE_BACKED; ACCESS BLOCKER | Must not use public endpoint as membership or private media entitlement. |
| APIs #20/#37 | Catalog/DD Draft only; no route/module/query/test source; UserProfile response mismatch. | NOT_FOUND; DECLARED_NOT_RUNNABLE | Enrollment gate and progress cannot be implemented deterministically. |
| APIs #22–#24 | Inventory declarations only; current route/module/test absent. | NOT_FOUND | ST-10 lesson handoff/access unavailable. |
| Study Web | Editable source absent; ignored dist contains only / route. | UNWIRED | ST-09 runtime cannot be verified. |
| Visual states/navigation | Gated static mockup only; no loaded states, lesson list, progress, or ST-21 action. | DISCREPANCY / DESIGN GAP | DD remains blocked. |

## CHANGES

- Files changed: ST-09.md; ST-09_PLAN.md; ST-09_markers.json; ST-09_markers_overlay.svg; screen_annotated.png; global screen plan; this worklog; eight Study Web/project context pages listed above; .agents/context-manifest.json.
- Original screen.png and code.html preserved.
- Context pages updated because existing wording incorrectly implied there was no router/artifact anywhere; current source audit distinguishes an ignored root-only dist artifact from absent editable source and feature routes.
- No API, field, business rule or runtime behavior was invented.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Objective read | Completed before continuing this goal turn. | VERIFIED |
| Mandatory docs preflight | Selector result and 3 selected docs worklogs recorded above; files were read in full before source inspection. | VERIFIED |
| Static artifact/link/marker/hash audit | PASS: 20 ordered markers map one-to-one to 20 DD element rows; 10 events; 20 SVG circles; internal links resolve; source hashes and SVG embedded source hash preserved; dimensions 1397×1600 and 2954×3200; no trailing whitespace. | VERIFIED |
| git diff --check | Completed with no whitespace errors. | VERIFIED |
| node scripts/validate-agent-context.mjs | Exit 1, AGENT_CONTEXT_INVALID. Reports db-admin missing context/source paths and stale source inventories for server-study, server-work, web-work, mobile-work and db-admin; no ST-09 broken link or specific context finding. These repository-wide issues are outside this screen change. | FAIL (existing repository-wide context issues) |
| Tests/runtime | Not requested; no test suites or runtime flows will be run. | NOT_RUN |

## HANDOFF

- Remaining blockers: #20/#37 schemas and runtime source; #09 public content/video projection/access policy; #22–#24; AC-18 formula/empty/partial states; missing loaded UI/ST-21 control; Study Web route/session integration.
- Next screen: ST-10 in a separate session. Do not start another Screen ID in this session.

