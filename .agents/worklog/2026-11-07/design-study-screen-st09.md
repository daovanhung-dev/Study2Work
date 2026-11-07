---
task_id: "2026-11-07-design-study-screen-st09"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-09 Study Web course overview ↔ AC-13/AC-18 and APIs #09/#20/#37; upstream ST-08 and downstream ST-10/ST-21"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-09

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 236; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior distinct; trace route/auth/query/effects/response/tests from current source; preserve original assets; distinguish local source from declared contracts and runtime.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Do not infer API fields, filters, writes or policy from mockups; preserve API catalog/DD versus source discrepancies; keep Study Web `UNWIRED` unless editable route/client code proves otherwise.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: UI-only DD has no canonical skill; retain source-backed versus Draft status, avoid inferred identity/data mappings and keep runtime/live-schema claims limited to evidence.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st08.md`
    - carry_forward: AC-13 #20/#21 remain absent with unresolved course/progress payloads; ST-08 has no loaded course card; course ID handoff to ST-09 is expected only and not source-backed.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-09 only in this session; recheck its inventory row, contracts, source assets and current Study Web/Study Server behavior. Write/update `ST-09_PLAN.md` before any marker, annotation or screen DD changes. Preserve usable original assets; make numbered markers map 1:1 to all documented elements; provide A–F sections with traceable events, API contracts, states, navigation, security, errors and explicit blockers; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog. Do not infer course membership, progress formula, lesson access, data fields, API behavior, retry/cache rules, or route handoff.
- Canonical inventory details: `list_screen.md` row 23 defines ST-09 as `/student/courses/:courseId`, AC-13/AC-18, APIs #09/#20/#37, expected outline/per-lesson progress/continue CTA, links ST-10/ST-21 and states enrolled/not-enrolled/loading/no-lessons (P1, screen gate D). F04 explicitly says #09 is public and cannot replace a permission-based learning tree. AC-13 expects enrolled-course list plus progress; AC-18 says aggregate lesson + quiz + assignment progress but does not define a formula.

## CURRENT_BEHAVIOR

- Source/config: `screen.png` and `code.html` hashes match the existing plan. The HTML is static: anchors use `href="#"`; `data-path` values are hints; only copy-route has `navigator.clipboard.writeText('/student/courses/:courseId')`. Current Study Server has a registered public #09 route at `/api/v1/courses/{course_id}/curriculum` (router in `app/api/v1.py`, included by `app/main.py`), query/view/validator/model source, and focused test source. It selects a PUBLISHED course and PUBLISHED lessons ordered by `sort_order`, `id`; response lessons include nullable `content` and `video_url`; empty curriculum is HTTP 200; non-integer/missing/unpublished resources map to 404; SQL/mapping failure maps to 500. The route has no JWT/enrollment check. The declared `int64` path has no explicit signed-range check, and the API #09 Draft's error example uses `data={}` while the current error helper defaults to `data=null`. API #20/#37 and #22–#24 route/module/query/test source searches returned no matches; their #20/#37 DDs are Draft, with membership, progress schema/formula, identity and empty/error semantics open. Study Web editable source/router is absent from the non-docs file inventory; `dist/` is ignored, and its provenance/deployment is unknown. Live DB/deployment are not verified.
- Runnable tests: #09 focused test source exists and was read, not run. No #20/#37/#22–#24 focused test source was found. No application tests were run.
- Runtime wiring: The #09 route is registered in local source; no live API, live DB or deployment was exercised. Study Web feature routes remain UNWIRED and runtime is NOT VERIFIED.

## SOURCE_TRACE

```text
Expected: ST-09 inventory row 23; AC-13 course-list/progress outcome; AC-18 lesson+quiz+assignment aggregate; F04 public curriculum/access boundary; #20/#37 Draft contracts.
Current: registered public API #09 route, source query/model/tests, static gated mockup, placeholder navigation, no Study Web source/router, and no #20/#37/#22–#24 backend source.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #09 source status | Registered route/query/model/test source exists; the reverse API dependency index in `list_screen.md` now marks #009 as R. The ST-09 screen remains D because its client flow is unwired; API #09 DD remains Draft. | RESOLVED IN TRACKER | Keep screen gate, local source status, and API DD lifecycle distinct. |
| #20/#37 and #22–#24 | API #20/#37 are Draft and route/module/query/test sources are absent; #22–#24 are absent from current Study Server route/module/test source. | BLOCKER | Enrollment, progress, and lesson-access flows cannot be implemented or runtime-verified. |
| Public #09 projection | Current #09 checks publication only and returns `content`/`video_url`, without an enrollment/access check. | SECURITY/DESIGN BLOCKER | Do not treat the public response as enrollment or entitlement proof. |
| Marker endpoint metadata | Corrected all 20 `leader_to_canvas_px` values to match per-marker SVG path endpoints; source image and annotation geometry were preserved. | RESOLVED | Marker JSON, SVG, labels, and 20 DD element rows now map 1:1. |
| #09 error envelope | API #09 Draft example uses `data={}` for errors; current error helper defaults to JSON `null`. | DISCREPANCY / OPEN API DD | Record source response for ST-09; do not revise API contract in this screen task. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-07/design-study-screen-st09.md`, ST-09 plan/DD/marker JSON, `apps/study-client/docs/list_screen.md`, and `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`.
- Preserved: `screen.png`, `code.html`, `screen_annotated.png`, and `ST-09_markers_overlay.svg` are unchanged; source PNG/HTML hashes match the recorded values, and the SVG still embeds the exact source PNG.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: None; live DB/deployment and runtime behavior remain unverified.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective read; root router/context map/worklog contract and selected exact-type AD-01/AD-02/AD-03 worklogs reviewed. | VERIFIED |
| Scoped source and contract review | `list_screen.md` ST-09 and F04/API index, global plan rows ST-08/ST-09/ST-10/ST-21, AC API index, AC-13/AC-18 drawio, API #09 source/DD/catalog/test, #20/#37 Draft/open questions, #22–#24 source search, Study Web file/dist ignore state, Study design guide and direct ST-08 worklog reviewed. | VERIFIED_STATIC_REVIEW |
| Visual/marker audit | Original and annotated PNG visually reviewed. Source image/HTML hashes and dimensions match plan; embedded SVG image hashes to original; 20 ordered marker IDs, circles, labels, SVG paths and DD rows align; all endpoints/bounds/non-overlap checks pass. | VERIFIED_STATIC_REVIEW |
| DD/asset/tracker static audit | Explicit A–F headings, EV-01…EV-10, 20 element rows, local links, JSON/XML parse, API #009=R and ST-09=D, inventory 83/83, core artifact bundles 82/83 (ST-01 incomplete). | VERIFIED_STATIC_REVIEW |
| `git diff --check` and authored whitespace | Scoped `git diff --check` exited 0 for changed tracked files; changed ST-09 DD/plan/worklog have no trailing whitespace. Existing whitespace-only lines 3–6 of `list_screen.md` are outside changed hunks. | VERIFIED |
| Application tests/runtime/context validator | No app tests/runtime were run; no context page/manifest was changed, so context validator was not required. Live database/deployment remain unverified. | NOT_RUN / NOT_REQUIRED |

## HANDOFF

- Remaining blockers: #20/#37 membership/progress schemas and rules; #22–#24 lesson access/start/content APIs; public #09 content/video exposure and int64 range alignment; missing loaded-course/lesson/progress/UI states and ST-21 control; Study Web route/session/API integration.
- Next owner/action: ST-09 remains DD BLOCKED, IMPLEMENTATION BLOCKED, RUNTIME NOT VERIFIED. Stop this session; ST-10 is the next screen in a separate session.
