---
task_id: "2026-11-07-design-study-screen-st11"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-10 → ST-11 lessonId/content handoff; AC-14/AC-15; APIs #24–#27; Study Web source/runtime boundary"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-11

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 238; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Preserve expected/current separation; trace the source boundary; keep Study Web `UNWIRED`; avoid runtime/test claims and assumptions from mockups.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Trace caller, auth, query, DB effect, response and focused test source; keep API Draft versus local source distinction; preserve unresolved identity/privacy/schema decisions.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Do not infer identity, route or data fields from mockup; distinguish current source from catalog/AC; fake DB tests do not establish live schema/runtime; UI-only DD has no canonical skill.
- additional_dependency_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-st10.md`
    - carry_forward: ST-10 currently lacks lessonId from ST-09; #24 is listed by both ST-10 and ST-11; APIs #24–#27 had no Student source in the prior audit; recheck current source this session.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Complete ST-11 only in this session. Inspect current inventory, AC-14/15, APIs #24–#27, backend source and existing assets; update `ST-11_PLAN.md` before editing the DD, marker map or annotation; preserve original assets; keep ordered one-to-one markers; author the screen DD with A–F sections and traceable events, API behavior, state, navigation and blockers; update `list_screen.md`, `dd_screens/PLAN.md` and this worklog. Do not invent lesson selection, player behavior, progress trigger, resource/next flow, media policy or retry semantics.
- Canonical inventory and contract details: `list_screen.md` row 25 expects route `/student/lessons/:lessonId`, AC-14/15, APIs #24–#27, lazy #26 and #27 after completion; ST-10 row 24 also lists #24, and ST-09 does not currently hand off a lessonId. API catalog declares Student Bearer, int64 lesson path, and `ApiEnvelope<Lesson>` for all four APIs; #25 body requires `position`, `percent`, `completed`.

## CURRENT_BEHAVIOR

- Source/config: `code.html` is a static unavailable-content fallback with 7 anchors; no media/player/resource/progress/next control or API handler. Study Web editable source/router is absent and context is `UNWIRED`. Study Server has no Student route/module/query/test for #24–#27; Admin `/admin/lessons*` endpoints #82–#86 are distinct. API DD #24–#27 are Draft with unresolved open questions.
- Data design: legacy BIGINT `DB.sql` candidate and V1-PILOT UUID/versioned `02_study_db.sql` describe different models. Neither has an approved lesson-progress mapping for #25 `position`/`percent`; block-level `last_position_seconds` is not a lesson mapping. Live schema is unverified.
- Runnable tests: Focused route/module/test inventory reviewed read-only; no application tests were run.
- Runtime wiring: Study Web and Student APIs remain unverified/UNWIRED; screenshots, API catalog and checked-in DDL are not runtime proof.

## SOURCE_TRACE

```text
Expected: `list_screen.md` ST-11 row; AC-14/15 diagrams and API index; API catalog #24–#27; API DD open questions Q-24-01…06, Q-25-01…08, Q-26-01…07 and Q-27-01…05. AC-14 describes access → start → lesson → progress/aggregate → completion; AC-15 shows lesson/resources/next before render, while inventory places #26 lazy and #27 after completion.
Current: `screen.png`, `code.html`, markers/DD, Study Web context, `app/api/v1.py`, Student modules/tests, Admin lesson route contrast, `infra/postgres/study-server/DB.sql`, `infra/postgres/02_study_db.sql`, and `.agents/project/database.md`. Source asset is static fallback; #24–#27 have no Student implementation; the two DDL families differ and neither proves live schema.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Static fallback vs expected player | PNG/HTML has only the unavailable-content card and static links; expected player/progress/resource/next controls are absent. | DISCREPANCY | Keep current fallback separate from expected behavior; no control markers to add. |
| API #24 fetch ownership and context | ST-10 and ST-11 both list #24; ST-09 has no `lessonId` handoff. | BLOCKER | Leave owner, caching and duplicate-call behavior unresolved. |
| APIs #24–#27 current source | No Student route/module/query/test; API DDs are Draft. Admin #82–#86 are distinct. | NOT_FOUND | Keep implementation/runtime status separate from catalog declarations. |
| Progress/storage and DDL | Legacy BIGINT `lesson_progress` has no `position` or user/lesson unique key; V1-PILOT UUID `lesson_progress_facts` has no position/percent; block progress has separate `last_position_seconds`. | BLOCKER | Do not claim an approved lesson-level persistence mapping or live schema. |
| API #26/#27 sequence and payload | #26 catalog response is Lesson despite resources purpose; AC-15 eager sequence differs from inventory lazy/after-completion flow. | DISCREPANCY / BLOCKER | Do not choose payload, ordering, empty result or orchestration. |

## CHANGES

- Files changed: this worklog; `ST-11_PLAN.md` (dated re-audit added before DD edits); `ST-11.md` (A–F structure and DDL/security qualification); `list_screen.md`; `dd_screens/PLAN.md`.
- Marker JSON/SVG and source/annotated image were reviewed; no marker/image edits were needed.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Worklog preflight | Objective/router/context-map/worklog contract reviewed; exact-type docs selector `READY` 3/238; AD-01, AD-02, AD-03 worklogs and direct upstream ST-10 worklog reviewed. | VERIFIED |
| Scoped source and contract review | Inventory, AC-14/15/index, API catalog and four API DD open-question files, Study Web context, Study Server route/module/test inventory, both DDL candidates and DB context reviewed. | VERIFIED (read-only) |
| Plan-before-DD gate | Re-audit findings and intended A–F/DDL changes appended to `ST-11_PLAN.md` before editing the DD. | VERIFIED |
| Static artifact audit | JSON and SVG XML parse; 14 ordered marker IDs match 14 DD element rows and 14 SVG circles; embedded PNG bytes equal `screen.png`; local links resolve. Original hashes match baseline; `file` confirms 1280×1024 source and 2820×2048 annotated PNG; annotation visually reviewed. | VERIFIED |
| DD, links and repository bundle audit | Explicit A–F headings, 8 sequential event IDs, HTML has 7 anchors and no media/form/input/canvas/button elements; 83/83 inventory/folders and 82/83 core bundles, missing only ST-01. | VERIFIED |
| Whitespace/status checks | Scoped `git diff --check` for tracked tracker files passed; authored ST-11 plan/DD/worklog have no trailing whitespace; tracker rows show DD/implementation blocked and runtime not verified. | VERIFIED |
| Tests/runtime | No application tests, browser runtime, deployment or live database check was run. | NOT RUN (per task scope) |

## HANDOFF

- Remaining blockers: Expected player UI is absent; ST-10/ST-11 #24 ownership and ST-09 lessonId handoff are unresolved; APIs #24–#27 lack Student implementation and approved details; progress persistence, resources response/security, next ordering/terminal semantics and Study Web wiring remain open.
- Next owner/action: ST-11 session complete; stop here. ST-12 is the next candidate for a separate session.
