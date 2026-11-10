---
task_id: "2026-11-07-design-study-screen-sh01-reaudit"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-01 public landing page → Study APIs #05/#06; public route and DTOs must match Study Server source"]
status: "VERIFIED"
---

# Worklog: Re-audit Detailed Design màn hình Study SH-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 exact-type worklogs selected of 250; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current behavior separate, inspect route and runtime wiring, preserve original assets, and distinguish source-backed APIs from actual UI/runtime evidence.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Treat current Study Server source and tests as evidence of local implementation only; do not infer live schema or deployment; UI-only DD has no canonical skill.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Recheck exact source in the current worktree; preserve route/client `UNWIRED` and API/catalog discrepancies; do not claim tests or runtime were verified.
  - path: `.agents/worklog/2026-11-06/design-study-screen-sh01.md`
    - carry_forward: SH-01 already has a 26-element DD/plan/annotation bundle; primary blockers remain PNG/HTML authority, unsupported category filtering, GS-03 navigation, marketing/email claims, and missing Study Web runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Re-audit SH-01 only in this session. Preserve original `screen.png` and `code.html`; verify markers and DD traceability; make the required A–F DD structure directly auditable; update the screen plan, global tracker, and this worklog. Keep unresolved product/API decisions as blockers and distinguish DD, implementation, and runtime status.
- Canonical references: current goal objective; `apps/study-client/docs/list_screen.md` SH-01 row; AC-03; API catalog #05/#06; current Study Server route/module/model/test source; Study Web design guide and current source-status context.

## CURRENT_BEHAVIOR

- Screen bundle exists at `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/`: source PNG/HTML, DD, plan, JSON marker map, SVG overlay, annotated PNG.
- Current source review confirms public GET #05 `/api/v1/categories` and #06 `/api/v1/courses`; #06 parses `category` but returns 422 while no category relation is source-backed. Checked-in legacy DDL has no course-category column/relation; this does not prove live schema.
- Study Web remains `UNWIRED`: current tree has docs, ignored `dist`, and `node_modules`; editable source/router/package manifest are absent. No UI runtime is established.
- Existing DD covers the required topics in sections 1–10, but does not provide an explicit crosswalk from required A–F labels to those sections.

## SOURCE_TRACE

```text
Expected: Guest opens proposed `/` → independently load public #05 categories and #06 published courses → map only documented DTO fields → navigate to approved discovery/auth destinations.
Current: no editable Study Web route/client → FastAPI #05/#06 route → guest module view/validation/query/model → current response mapping and local fake-session test source. #06 rejects any category filter with 422; DDL candidate has no course-category relation. Live DB/deployment remain unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| PNG vs HTML authority | Current screenshot and HTML differ materially in sections, controls, sample cards and empty-state presentation. | `DISCREPANCY / BLOCKER` | Keep both as source evidence; do not infer a unified runtime screen. |
| Prototype fragment links | HTMLParser finds 16 fragment hrefs: 5 match section IDs, 5 are bare `#`, and 6 auth/legal fragments have no matching target. | `STATIC_ONLY / ROUTE_UNWIRED` | DD now distinguishes in-page scroll from missing targets and app routes; no route is inferred. |
| Category filter | Catalog accepts `category`; current #06 validator rejects any provided category with 422; legacy DDL has no source-backed relation. | `DISCREPANCY / BLOCKER` | Category chips remain informational/disabled; do not send the filter. |
| Course detail destination | AC/F02 points toward GS-03/#08; SH-01 inventory next-screen list omits it; #08 has local source while catalog status is Draft. | `DISCREPANCY / BLOCKER` | Do not invent card navigation. |
| Unsupported marketing/email content | KPI, testimonials, company marks, certifications, currency/discount and email collection lack mapped source/approval. | `UNMAPPED / BLOCKER` | Suppress claims or keep the form disabled/hidden until contracts and approval exist. |
| Study Web runtime and variant-2 | Editable app source/router and second source variant are absent from current tree. | `UNWIRED / NOT_FOUND` | Do not claim route or runtime verification; do not recreate missing asset. |

## CHANGES

- Files changed: `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-01_trang-gioi-thieu-study__variant-1/SH-01_PLAN.md` (re-audit plan/findings), `SH-01.md` (A–F crosswalk, explicit EV-06/07 outputs, precise fragment behavior, whitespace cleanup), `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (dated checkpoint/pointer correction), and this worklog.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Original `screen.png` and `code.html` were preserved; no API/backend or UI implementation behavior was changed.
- Assumptions: none; current blockers remain explicit.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Objective/router/context/worklog preflight | Goal objective re-read; root router, context map, worklog contract/template, project boundary context, Study Web and Study Server scope pages reviewed; exact docs selector `READY` 3/250; selected AD-01/AD-02/AD-03 and prior SH-01 worklog read. | `PASS` |
| SH-01 source/contract review | Inventory, AC-03 index, API catalog, #05/#06 route/module/query/model/test source, legacy DDL candidate, Study Web source tree and design guide rechecked. #05/#06 remain public/source-present; #06 category returns 422. | `PASS_STATIC_REVIEW` |
| HTML prototype link audit | 16 fragment hrefs classified: 5 in-page section targets, 5 bare top fragments and 6 unresolved auth/legal targets; no fetch/XHR/listeners present. | `PASS_STATIC_REVIEW` |
| Marker/DD/image audit | 26 ordered unique markers match 26 element rows and SVG labels; targets are within the 559×1600 source; JSON/SVG parse; source hashes unchanged; PNG dimensions 559×1600 and 1230×3200; annotation visually reviewed. Fourteen ordered event sections now each expose trigger/precondition, input, process, result/output and exception/error; A–F crosswalk present. | `PASS` |
| Links/whitespace/diff | DD/plan local links resolve; authored-file whitespace scan clean; scoped `git diff --check` passed. | `PASS` |
| Application tests/runtime/live DB | Not requested/performed; Study Web implementation/runtime absent. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: source/design authority for PNG vs HTML, category contract, course-card destination, approval/source for marketing/email/currency claims, missing Study Web implementation, and live DB/deployment verification.
- Session outcome: re-audit and tracker update complete; expected screen status remains `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next Screen ID: SH-02, in a separate session after this SH-01 re-audit.
