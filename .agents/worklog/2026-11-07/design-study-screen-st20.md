---
task_id: "2026-11-07-design-study-screen-st20"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: ["static verification"]
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["ST-20 progress dashboard → API #21 and #38; AC-18; links ST-09, ST-21, ST-22"]
status: "PARTIAL"
---

# Worklog: Re-audit ST-20 progress overview DD

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`, 247 available, 3 selected, no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected design, current source, and runtime verification separate; current source is authoritative for implementation claims.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Static HTML/screenshots are design evidence only; do not claim routes, data or actions are wired from prototypes.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Preserve explicit blockers and trace API claims to the current Study source and approved contract.
  - path: `.agents/worklog/2026-11-07/design-study-screen-st19.md` (supplemental, not selector-selected)
    - carry_forward: Keep API design, source-backed behavior, candidate schema and live schema evidence distinct; record UI/source mismatch without inferring behavior.
  - path: `.agents/worklog/2026-11-06/design-study-screen-st20.md` (supplemental, prior ST-20 session)
    - carry_forward: ST-20 already has plan, static HTML render, 16-marker map/annotation and A–F DD; re-audit before altering assets, preserve the PNG/HTML sources and keep the same API/orchestration blockers.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Re-audit ST-20 only; preserve its source screenshot and HTML, verify marker/DD mapping, maintain A–F coverage and event details, trace #21/#38 and AC-18, compare the prototype to the Study Web design target, and update the screen inventory, global tracker and dated worklog.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md` ST-20 row; `docs/lists/list_api.md` APIs #21/#38; API DDs #21/#38; AC-18 activity diagram and index. Inventory calls #21/#38 independently; AC-18 sequences #21 → #37 → #38. Preserve this discrepancy pending an owner decision.

## CURRENT_BEHAVIOR

- Source/config: Study Web editable source, package manifest and Student route are absent. Current Study Server has no Student route/module/query/test for API #21/#38; unrelated Mentor progress routes do not implement them. Existing ST-20 PNG is blank in its main region; companion HTML is a static empty-state prototype with Tailwind CDN/config and remote Plus Jakarta Sans, 1440px layout, and mixed primary tokens, which diverges from the Study Web design target.
- Runnable tests: Not run; this docs task does not request application tests.
- Runtime wiring: Study Web and Student API #21/#38 are `UNWIRED` / `NOT_FOUND`; runtime behavior is not verified.

## SOURCE_TRACE

```text
ST-20 inventory / static HTML → expected navigation and widgets only
Current Study Web route → NOT_FOUND
API #21/#38 catalog and Draft DD → declared contracts only
Current Study Server router/modules/tests → no Student #21/#38 wiring or DB side effect
AC-18 → design sequence #21 → #37 → #38; inventory instead requires independent #21/#38 calls
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #21 progress contract | Catalog returns `ApiEnvelope<UserProfile>` and ambiguous query; API DD open questions leave progress schema, aggregate, identity, merge and empty semantics open. | `DECLARED_NOT_RUNNABLE`; Draft | Required progress widgets cannot be mapped or computed. |
| API #38 achievements | Catalog returns `Page<Achievement>` with optional `course_id`; award source/rules, filter, pagination/order and empty policy remain open. | `DECLARED_NOT_RUNNABLE`; Draft | Do not derive or fabricate earned/locked achievements. |
| AC-18 request order | Inventory requires independent #21/#38; AC-18 sequences #21, #37, then #38 before render. | `DISCREPANCY` | Scheduling and partial-render behavior remain unresolved. |
| Study Web route/assets | No editable Study Web source/package/router; source PNG body is blank while HTML is a static no-data page. | `UNWIRED` | No runtime claims; loaded dashboard layout remains unavailable. |
| Prototype design tokens/dependencies | `code.html` uses Tailwind CDN, remote Plus Jakarta Sans, `max-w-[1440px]`, and mixed `#004AC6` / `#0B5F8A`; Study Web target specifies no remote font/CDN, a ~1120px content width and semantic ocean tokens. | `DISCREPANCY` | Needs visual alignment before implementation; source assets remain preserved. |

## CHANGES

- Files changed: `apps/study-client/docs/list_screen.md` (ST-20 blocker/status detail); `apps/study-client/docs/screen_stitch/03_student/ST-20_tong-quan-tien-do/ST-20_PLAN.md` (re-audit/design discrepancy); `.../ST-20.md` (event element/type metadata, CTA semantic type, static Tailwind clarification and design discrepancy); `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` (dated ST-20 audit); this worklog. PNG/HTML/marker assets were not regenerated or changed.
- CONTEXT_UPDATES: none planned.
- Context pages changed: none.
- Assumptions: Do not infer new API schema, route behavior, achievement rules, progress formula or request ordering.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Inline Python static audit | PNG dimensions/hashes; JSON IDs/bounds; SVG labels; DD element rows; 11 event IDs/types; A–F; local links (DD 18/18, plan 14/14) | `VERIFIED` |
| Inline Python authored-file whitespace audit | ST-20 DD, plan and worklog contain no trailing spaces/tabs | `VERIFIED` |
| Inline Python inventory count | 83/83 screen folders; 82/83 four-file core bundles; ST-01 is the only incomplete ID | `VERIFIED` |
| `rg -n 'users/me/progress|users/me/achievements|student/progress' apps/study-server/app/api/v1.py apps/study-server/app/modules apps/study-server/tests` | No matches; current Student API #21/#38 and ST-20 route source not found | `NOT_FOUND` |
| Study Web source/package check | `apps/study-client/src` and `package.json` absent; top level contains only `dist`, `docs`, `node_modules`, and `tsconfig.tsbuildinfo` | `UNWIRED` |
| `git diff --check -- <scoped files>` | No whitespace errors in tracked changes | `VERIFIED` |
| Visual inspection of `screen_annotated.png` | 16 labels remain legible and adjacent to the rendered targets | `VERIFIED` |
| Application tests/runtime | Not requested/performed | `NOT_RUN` |

## HANDOFF

- Remaining blockers: API #21/#38 contracts and Study Web route remain unwired; AC-18/inventory order unresolved; loaded-state design absent and current prototype differs from the design target.
- Next owner/action: API/product owners resolve #21/#38 schema/rules and AC-18 ordering; ST-21 already has its separate bundle, so ST-22 is the next Student screen in a later session.
