---
task_id: "2026-11-06-design-study-screen-st21"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-20 → ST-21; AC-18/API #37; ST-21 lesson handoff to ST-10/ST-11; DB progress candidates"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-21

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; 3 exact-type docs worklogs selected of 186; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Separate expected from current route/API; keep static prototype claims distinct; preserve source assets; no canonical skill applies to UI-only DD.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Current Study Web has no route/runtime; API declarations/source/tests/DB must be distinguished; do not infer UI behavior from stale HTML or mock data.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Trace every relevant API and linked screen; preserve API orchestration/source discrepancies; do not treat checked-in schema or static assets as runtime evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Goal objective read in prior continuation; active goal covers all 83 screens, one Screen ID per session. This session covers ST-21 only.
- Inventory ST-21: `/student/progress/:courseId`, AC-18/#37, lesson done/in-progress/not-started, completion rate and evidence timestamps; lesson navigation to ST-10/ST-11 after gate; states loading/empty/in-progress/completed.
- AC-18/API design: Student selects a course then #37 aggregates lesson + quiz + assignment progress; catalog says Student Bearer, `course_id:int64!`, `ApiEnvelope<UserProfile>`, 200/401/403/404/500.
- No skill was invoked: manifest and skill registry exclude `web-ui-only-dd` from canonical Web/API DD skills.

## CURRENT_BEHAVIOR

- Original `screen.png` 1280×1024 SHA256 `1bd43f7a29ad1b1591953a03846d57ce5736839e8fa6c47921d12a334056bf65`; visually mostly blank with dark bottom strip.
- `code.html` SHA256 `7eb0ba19f73bccf1b248205fdbac94eedf25ec059345f69c77175cfd2f3bcda6`; static no-progress fallback with no script, API request, auth, route binding or lesson rows. Rendered as supplemental 1280×916 `screen_rendered.png`, SHA256 `ac30e06639a2002b0c2343303d6c91955be2885d925ec0a71dd16b69688f9ded`; annotation is HTML-derived only.
- API #37 DD Draft; current Student route/module/query/test NOT_FOUND; #65/#67 are distinct Mentor endpoints. Current Study Web inventory has no `src`, no `package.json`, no editable router; ignored dist has a single `/` route and no `/student/progress`; serving/deployment remains unverified.
- API DD candidate legacy `lesson_progress` differs from V1-PILOT `lesson_progress_facts`/`progress_snapshots`; none proves live schema or the #37 runtime query.

## SOURCE_TRACE

```text
Expected inventory: ST-20(courseId) → ST-21 GET #37(course_id) → course progress →
  ST-10/ST-11 by lesson_id after access gate.
AC-18: Student login → select course → #37 → aggregate lessons + quizzes + assignments.
Current: Student #37 route/module/query/test absent; Study Web ST-21 route absent;
  PNG blank; HTML static no-progress fallback.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #37 response | Catalog/API DD return `ApiEnvelope<UserProfile>`; UserProfile has no progress fields | DISCREPANCY / BLOCKER | Cannot map course/lesson progress or expected metrics |
| Aggregate rules | AC-18 names lessons, quizzes, assignments only; API DD Q-02/Q-03 open | BLOCKER | Denominator, weighting, attempt/submission selection, statuses, rounding unresolved |
| Access/identity/empty | API DD Q-04–Q-08 open; no Student source | BLOCKER / DECLARED_NOT_RUNNABLE | Cannot define course authorization, 403/404, no-progress or invalid-path behavior |
| Schema candidates | Legacy lesson_progress vs V1-PILOT lesson_progress_facts/progress_snapshots | DISCREPANCY / DESIGN_ONLY | Do not select a DB model or claim live schema |
| UI/runtime | Original PNG blank; HTML static fallback; Study Web Student route absent | UNWIRED / DISCREPANCY | Loaded state and navigation are not runtime behavior |

## CHANGES

- Files changed: `ST-21_PLAN.md`; `ST-21.md`; `ST-21_markers.json`; `ST-21_markers_overlay.svg`; `screen_rendered.png`; `screen_annotated.png`; global `dd_screens/PLAN.md`; this worklog. Original `screen.png` and `code.html` preserved.
- CONTEXT_UPDATES: none; no context page or manifest changed.
- Assumptions: none. Static no-progress copy is not treated as API empty contract.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective, context/worklog preflight | Current objective workflow followed; selector selected/read 3 exact-type docs worklogs of 186. | VERIFIED |
| Artifact/marker/DD/link audit | 11 unique ordered/in-bounds markers map one-to-one; JSON/SVG valid; image dimensions checked; annotation visually reviewed; DD A–F and 9 ordered events present; 21 relative links resolve; PNG/HTML/render hashes preserved. | VERIFIED |
| Tracker counters and next pointers | ST-21 row is blocked with API/UI evidence; 33/83 complete, 50 remaining; next Student ST-22; Mentor pointer ME-04. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Tests/runtime | Not run; no API/runtime claim. | NOT_RUN |
| Context validator | No context page/manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: API #37 progress DTO, aggregate and attempt/submission rules, enrollment/course access/identity/403-vs-404/empty/path behavior, schema generation/live DB, loaded-state design, Study Web route, lesson access gate.
- Next action: ST-22 in a separate screen session; independent Mentor pointer remains ME-04.
