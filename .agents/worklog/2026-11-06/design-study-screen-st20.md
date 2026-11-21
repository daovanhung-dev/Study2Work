---
task_id: "2026-11-06-design-study-screen-st20"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["AC-18 orchestration; Student APIs #21/#38; inventory F07 and transitions ST-19/ST-21/ST-22"]
status: "VERIFIED"
---

# Worklog: Detailed Design màn hình Study ST-20

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: READY; selected 3 exact-type docs worklogs of 184; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs01.md`
    - carry_forward: Keep prototype claims separate from current route/API evidence; preserve original assets; do not infer UI behavior from static markup.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs02.md`
    - carry_forward: Treat Study Web as UNWIRED unless current source proves otherwise; distinguish declared API contracts from executable routes and preserve unresolved field/route mismatches.
  - path: `.agents/worklog/2026-11-06/design-study-screen-gs03.md`
    - carry_forward: Trace every linked API/current source separately; preserve AC-vs-inventory orchestration conflicts; do not apply an API DD skill as a UI-only contract.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Goal objective was read at `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` before continuing.
- Inventory ST-20: Student `/student/progress`, AC-18, APIs #21/#38, total lessons/course progress/actual achievements, independent widget loads, links ST-21/ST-22, states loading/partial/empty/error.
- AC-18 diagram sequences #21, #37, #38 before rendering; this conflicts with inventory's independent #21/#38 orchestration and ST-21 ownership of #37. Preserve discrepancy pending owner resolution.
- API #21 catalog declares `ApiEnvelope<UserProfile>` with ambiguous query wording; #38 declares `ApiEnvelope<Page<Achievement>>` and optional course_id, but no award policy/pagination request.

## CURRENT_BEHAVIOR

- `screen.png` is 1280×1123 with header/footer and blank main body; source SHA256 retained from pre-edit review: `a308a1e1739b155f20abbb6d9269f132a0125997cf06a4f08caf15818559a135`.
- `code.html` is a static no-progress fallback, no script/API/auth/route handler; source SHA256 retained: `0d1cf1f32505c59a712956ff1a11b28355755d0d410658fb9621d2c8f02b5e3e`.
- Rendered HTML to supplemental `screen_rendered.png` (1280×1079, SHA256 `00b273505d7982eb92477d076d5e60b923d30209e4510d504cc55785b1c688ea`); static HTML/CSS only, not app/API runtime. Annotated image SHA256 `24345f519dd43f2df8a973107921391549b5dde56b3e7e3744646230e31500f1`; original screen/HTML preserved.
- Current Study Web has no editable route/runtime; Student #21/#38 route/module/query/test are NOT_FOUND. Mentor progress APIs are separate. DB candidate lesson_progress is not live-schema proof and no achievements table is confirmed.

## SOURCE_TRACE

```text
Expected: ST-20 → independent #21 and #38 widgets → ST-21 / ST-22
AC-18: #21 → aggregate → #37 course detail → #38 → render
Current: Study Web ST-20 route absent; Student #21/#38 route/module/query/test absent;
         original PNG body blank; HTML is static empty fallback.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Progress #21 schema | Catalog response is UserProfile, no progress fields; query string ambiguous; API DD Draft | BLOCKER / DECLARED_NOT_RUNNABLE | Cannot map totals, per-course progress, formulas or empty states |
| Achievement #38 | API DD Draft, no award rule/source table, no current Student route; response Page without request pagination fields | BLOCKER / DECLARED_NOT_RUNNABLE | Cannot determine awards, projection, course semantics or ordering |
| Orchestration | Inventory says #21/#38 independent; AC-18 sequences #21→#37→#38 | DISCREPANCY | Do not invent request timing/partial behavior |
| Visual assets | Original PNG body blank; HTML static empty state | VERIFIED | Supplemental render used for visible HTML elements; loaded dashboard absent |
| Study Web | No editable app route/package/source for ST-20 | UNWIRED | No runtime navigation/API claim |

## CHANGES

- Files changed: `ST-20_PLAN.md` (already authored before marker/DD); `screen_rendered.png`; `screen_annotated.png`; `ST-20_markers.json`; `ST-20_markers_overlay.svg`; `ST-20.md`; this worklog; global `dd_screens/PLAN.md` (ST-20 blocker/progress/next pointers).
- Preserved: original `screen.png` and `code.html`.
- CONTEXT_UPDATES: none; no project/scope context page or manifest changed.
- Assumptions: none. HTML empty copy is not treated as API empty-state contract.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Objective and worklog preflight | Objective read; selector selected and all 3 exact-type docs worklogs read (3 of 184). | VERIFIED |
| Artifact/marker/static audit | JSON/SVG valid; 16 unique ordered markers in bounds map one-to-one to DD; rendered/annotated PNG dimensions checked; visual inspection confirms markers adjacent to targets without covering copy/controls. | VERIFIED |
| DD structure, links, tracker counters, original source hashes | A–F present; 11 ordered events; 18 relative links resolve; original PNG/HTML hashes unchanged; tracker 32/83 complete, 51 remaining, next Student ST-21 and Mentor ME-04. | VERIFIED |
| `git diff --check` | No whitespace errors. | VERIFIED |
| Tests/runtime API | Not run per task instruction; no app/API runtime checked. | NOT_RUN |
| Context validator | No context pages changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: progress DTO/query/formula/empty shape; achievement policy/projection/filter/pagination/empty shape; AC-18 orchestration discrepancy; loaded-state design; Study Web and Student API runtime.
- Next owner/action: resolve contracts and wire runtime before implementation can be verified. Next screen within Student sequence is ST-21 in a separate session; independent Mentor pointer is ME-04.
