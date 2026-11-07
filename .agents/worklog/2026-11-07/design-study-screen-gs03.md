---
task_id: "2026-11-07-design-study-screen-gs03"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-03 course detail ↔ AC-05 and APIs #08/#09/#10; GS-02 entry and GS-04/05/06/ST-04 handoffs"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study GS-03

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type docs worklogs selected of 259; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; preserve assets; recheck Study Web wiring; do not infer runtime or test status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Trace the current source rather than mockup assumptions; distinguish API source from Draft policy and live-schema state; keep DD, implementation and runtime statuses separate.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve assets; confirm skill applicability in the registry; do not infer routes, identity, mappings or unsupported prototype behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Historical GS-03 artifacts/source findings are not authoritative until rechecked. Preserve original assets, keep API #08/#09/#10 source statuses distinct, and retain AC-05 versus F02 orchestration discrepancy.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Handle GS-03 only this session; review/write its plan before editing DD or annotation; preserve original source assets; ensure ordered 1:1 markers, source-traced screen DD, tracker/checkpoint and worklog; distinguish DD readiness, implementation block and runtime verification.
- Canonical contract/approved DD: Current inventory row 10 says `/courses/:courseId`, AC-05, APIs #08/#09/#10, course details/mentor/price, curriculum/review tabs and enrollment CTA; F02 says click `course_id` to GS-03 and load #09/#10 lazily by tab after #08 confirms PUBLISHED. Linked screens: GS-04/05/06/ST-04. Recheck AC-05/API catalog/DD and source before finalizing.
- API catalog contract declares #08/#09 `course_id:int64`; expected behavior for the design remains blocked where AC-05 conflicts with F02 or current backend source.

## CURRENT_BEHAVIOR

- Source/config: GS-03 bundle contains preserved source `screen.png`/`code.html`, plan, DD, marker JSON/SVG, `screen_annotated.png`, and `screen_rendered.png`. Current tracker/inventory now show #08/#09 source-backed and #10 declared but not runnable; route/UI status remains UNWIRED.
- #08: `app/api/v1.py` route accepts `course_id:str` and calls `get_course_detail`; validator uses shared `parse_integer`; query selects a PUBLISHED course with `LEFT JOIN users`; view returns a singleton `CoursePage` in `data.items`, 404 for invalid/missing/unpublished and 500 for DB/mapping errors. API #08 Draft DD specifies `INNER JOIN`; mapper requires mentor ID/name, so absent mentor data after current LEFT JOIN becomes mapping 500. Checked-in DDL allows nullable `mentor_id`; focused fake-session test source read, not run.
- #09: route accepts `course_id:str`; validator uses shared `parse_integer`; Q1 checks PUBLISHED course, Q2 returns PUBLISHED lessons ordered by `sort_order ASC, id ASC`; empty lessons return HTTP 200 with empty page; query/mapping errors return 500, SQLAlchemy query errors roll back. Focused fake-session test source read, not run.
- Shared parser discrepancy: `parse_integer` accepts a signed integer lexical form (including optional digit separators) and caps only Python's digit count; it does not enforce catalog signed-int64 range or a positive-only rule. Checked-in API tests cover normal and non-integer IDs, not int64 boundaries; no tests were run.
- #10: scoped source searches found no route/module/test under Study Server `app/` or `tests`; catalog/API DD only. Checked-in `discussions` DDL contains content/parent/status but no title or rating field/table. DDL is not live database proof.
- UI/runtime: `.agents/web-work/study/INDEX.md` says `UNWIRED`; current `apps/study-client/` listing contains docs/assets and ignored `dist/index.html`, but no editable application source or package manifest. No application runtime was run.
- Cross-screen handoff: GS-02 expects `course.id` from #07 to populate GS-03; GS-04/GS-05 expect the same `courseId`; ST-04 route also proposes that parameter but API #15 identity remains blocked. These routes remain design proposals.

## SOURCE_TRACE

```text
Expected: proposed GS-03 course detail -> AC-05 and APIs #08/#09/#10 -> linked GS-04/05/06/ST-04 flows; F02 specifies #08 gate then lazy #09/#10 by tab.
Current: `list_screen.md`/API catalog provide design contracts; Study Web caller/router is absent. Study Server #08/#09 routes call modules that validate → query → map → envelope; #08 returns singleton Page<Course>, #09 returns published lessons/empty-success; #10 has no executable source. Tests were read only. Checked-in DDL is a candidate artifact, not live schema evidence.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| #08 API shape | Current source and API catalog both describe singleton `Page<Course>`; API DD remains Draft. | SOURCE_BACKED / DESIGN CONTRACT | UI must read `data.items[0]`; product/BE must decide whether the detail contract should stay paginated. |
| #08 mentor join | Current source `LEFT JOIN` differs from API DD `INNER JOIN`; mentor ID/name required, nullable mentor ID allowed by checked-in DDL, missing mentor yields mapping 500. | DISCREPANCY | BE needs to confirm join/data-integrity policy. |
| #08/#09 ID type | Catalog requires `course_id:int64`; routes accept `str`, shared parser has no signed int64/positive bound. Oversized DB behavior not runtime-verified. | DISCREPANCY | Clarify range/validation and error mapping; no client rule invented. |
| #08 error mapping | AC-05 says 404/403; current #08 returns 404 for invalid/missing/unpublished. | DISCREPANCY | Preserve current source 404 and ask API/UI owners to reconcile AC. |
| #09 behavior | Current source filters published course and published lessons, deterministic sort, empty 200; tests source exists but not run; API DD remains Draft. | SOURCE_BACKED | Do not infer preview/access policy or deployed schema. |
| #10 | No route/module/test source; catalog and Draft DD only; DDL lacks review title/rating source. | DECLARED_NOT_RUNNABLE | Reviews/rating UI remains blocked. |
| AC-05 vs F02 | AC-05 eagerly sequences #08→#09→#10; inventory F02 lazily loads tabs after #08. | DISCREPANCY | Product/BE must resolve before implementation. |
| Enrollment and wiring | CTA absent; G-01/#15 identity conflict; Study Web app/router absent. | IMPLEMENTATION BLOCKED / UNWIRED | Keep handoff and runtime states unverified. |
| Assets/markers/events | Source hashes held; 10 markers, 6 event sections, local links statically checked. | VERIFIED | Retain static rendered derivative as non-runtime evidence. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-03_chi-tiet-khoa-hoc/GS-03_PLAN.md`, `GS-03.md`, `apps/study-client/docs/list_screen.md` (GS-03 row), `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (GS-03 row/checkpoint), this worklog.
- CONTEXT_UPDATES: none; no `.agents/` context source was changed.
- Context pages changed: none yet.
- Assumptions: No runtime behavior inferred from static HTML, source tests, Draft API DD or checked-in DDL.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; all three selected docs worklogs read individually. | VERIFIED |
| Objective and worklog contract review | Active objective retained; worklog README/TEMPLATE and historical GS-03 log reviewed. | VERIFIED |
| Context routing | Global context map, project index/architecture/dependencies/contracts, Web and Study-Web entries/index, Study-Server entry/index, Study design guide and skill registry/manifest routing read; manifest excludes web-ui-only DD from canonical DD skills. | VERIFIED |
| Current inventory/tracker/bundle listing | GS-03 inventory/F02, global tracker row and current artifact file list reviewed; no DD/source conclusion assumed from historical log. | VERIFIED |
| Objective file | `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` read at session continuation. | VERIFIED |
| Source trace | API #08/#09 route, validator, query/model/view and focused test source; API #10 scoped source search; API DD/catalog, AC-05, checked-in DDL, Study Web subcontext and GS-02/GS-04/GS-05/ST-04 handoffs reviewed. Tests and live DB were not run. | VERIFIED (source only) |
| Static bundle audit | 83 inventory IDs = 83 tracker IDs = 83 source folders; 10 ordered unique markers map 10 DD rows and 10 SVG labels; target points in source bounds; 6 event sections have input/process/outcome or explicit blocked outcome; 11 local links resolve. | VERIFIED |
| Image provenance and preservation | `screen.png` 1280×1024 SHA-256 `94360a8b1b1a9bbe0cdc110f6c243ce5aaabd8b6923331c5667421cb1c37d34d`; `code.html` SHA-256 `d4f4bfdb56324b7c96589af75362903a491a3f565c97152b63634573c9d69619`; rendered 1440×1200; annotated 3040×2400. | VERIFIED |
| `git diff --check` | Targeted diff check for the changed inventory/tracker files exited 0; no whitespace errors. | VERIFIED |

## HANDOFF

- Remaining blockers: loaded detail/CTA and tab design; AC-05/F02 call order; API #08/#09 int64 parser mismatch; #08 Page<Course> detail shape; AC 404/403 mismatch; #10 route/title/rating source; G-01 enrollment handoff; Study Web UNWIRED and runtime not verified.
- Next owner/action: GS-04 is the next Screen ID for a separate session; do not begin it in this session.
