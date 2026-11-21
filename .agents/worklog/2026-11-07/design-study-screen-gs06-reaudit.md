---
task_id: "2026-11-07-design-study-screen-gs06-reaudit"
date: "2026-11-07"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["GS-06 courseId from GS-03 -> declared API #11; selected resourceId -> current API #12 -> GS-07; resource access semantics also affect ST-12"]
status: "VERIFIED"
---

# Worklog: Re-audit Detailed Design màn hình Study GS-06

Tiếp tục static verification và hoàn tất ngày 2026-11-08; phạm vi vẫn chỉ là GS-06.

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 262 exact-type docs worklogs available; selected 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad01.md`
    - carry_forward: Keep expected/current evidence separate; preserve original assets; do not infer report/data/API behavior from mockups; distinguish screen DD, implementation, and runtime status.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad02.md`
    - carry_forward: Recheck source and route wiring each session; keep declared API contract separate from current server behavior; don't claim tests/runtime from inspected files.
  - path: `.agents/worklog/2026-11-07/design-study-screen-ad03.md`
    - carry_forward: Use registry to confirm skill applicability; Web UI-only DD has no canonical skill; preserve missing-source, permission, schema and implementation blockers.
- additional handoff reviewed: `.agents/worklog/2026-11-06/design-study-screen-gs06.md`; prior GS-06 artifacts and source trace are a starting point, not authority over current source.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Re-audit only GS-06 in this session; reread the attached 83-screen objective; update its detailed plan before editing GS-06 DD, marker map/annotation, or shared trackers; verify the source image and annotation; update `list_screen.md`, `dd_screens/PLAN.md`, and this worklog; keep `DD READY`, `IMPLEMENTATION BLOCKED`, and `RUNTIME VERIFIED` distinct.
- Canonical inventory: GS-06 is the Guest course-resources tab, proposed `/courses/:courseId?tab=resources`, AC-06, APIs #11/#12, with GS-03/GS-07/ST-12 links. The expected contract and AC-06 flow must remain separate from current source evidence.
- Skill registry: `.agents/skills/INDEX.md` and `.agents/context-manifest.json` identify `createDD-markdown` for Web/API DD; Web UI-only DD has no canonical skill.

## CURRENT_BEHAVIOR

- Current GS-06 source image is PNG 1486×1600, SHA-256 `b90795438d5369466bb101e8f6730265667f8ecc45c0d047d66495410da87dcd`; current `code.html` SHA-256 `6843e2cc0f01a24e1db8100b8fec49d88e1f3fe39859b102bb9828d4905a8c31`. Both are unchanged design inputs.
- API #11 is present in catalog/API DD only; no Study Server route/module/query/test match was found. Its public GET contract declares `ApiEnvelope<Resource>` singleton, 200/404/500 and no pagination; the API DD is Draft.
- API #12 is composed locally at `/api/v1/resources/{resource_id}`. Current route has no auth dependency; validator requires positive signed-int64 and maps invalid path to 404; view reads legacy `resources`, conditionally gates linked parent lesson/course when `lesson_id` is non-null, returns direct URL, ignores `visibility`, and has no enrollment/access check or signer. SQL failures rollback and map to safe 500; model failures map to safe 500. Test source and the 2026-11-01 temporary-branch report were read; no tests were run in this session. API DD remains Draft and its `DECLARED_NOT_RUNNABLE` note is stale against current route/source evidence.
- AC-06 requires public-or-authorized access, a 403 branch and a signed URL for private objects. Catalog/current #11/#12 are public and list 404/500; current #12 has no 403/410/TTL/signer. Record `DISCREPANCY`.
- Legacy `infra/postgres/study-server/DB.sql` has `resources(id, lesson_id, name, resource_type, url, created_at)` and no `visibility`; V1-PILOT `infra/postgres/02_study_db.sql` has no generic `resources` table. Production/live schema and deployment remain unverified.
- Study Web current tree has no editable source, package manifest or router; it contains docs/assets, ignored dist and build metadata. Status remains `UNWIRED`.
- Existing annotation visually reviewed again: all 23 marker labels remain in the side gutters and point to the intended regions. Static JSON/SVG/image/mapping, local-link, whitespace and inventory checks passed; 83/83 IDs currently have all six core files, which proves presence only.
- Prototype visual differs from `.agents/web-study/design.md`: remote Google Fonts/Tailwind, Plus Jakarta Sans, cobalt palette, 1440px content width and mobile-hidden primary nav. Accessibility/WCAG claim is not measured.

## SOURCE_TRACE

```text
Expected: GS-03 courseId -> GS-06 resources list via #11 -> user selects resourceId -> #12 access/metadata decision -> permitted open/download -> GS-07; ST-12 shares some resource semantics.
Current: Study Web has no editable route/client -> #11 has declaration but no executable route/module/test -> user cannot load/select a real resource. Local #12 route -> positive int64 path guard -> legacy resources lookup -> conditional non-DELETED lesson/PUBLISHED course gate when lesson_id exists -> direct URL envelope or 404/500. It performs no visibility/enrollment authorization or signing. Production/live schema and browser flow are unverified.
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #11 list/cardinality/access | Catalog/API DD #11 says public singleton `ApiEnvelope<Resource>`; no current route/module/query/test. `visibility` has no legacy DDL source. | `DECLARED_NOT_RUNNABLE / DISCREPANCY` | No list/empty/order/page semantics; block data mapping and screen DD readiness. |
| API #12 access/URL/error behavior | Current local route/view/query/validator/model and test source; public/no-auth, conditional parent gate, direct URL; AC-06 expects 403/signer. | `SOURCE_BACKED LOCALLY / DISCREPANCY` | Do not treat 200 as authorization for private resources; no current 403/410/TTL contract. |
| API #12 API DD runtime label | API DD is Draft and says `DECLARED_NOT_RUNNABLE`; current app router and source tests include #12, and 2026-11-01 temporary branch report records HTTP 200. | `DOC/SOURCE DISCREPANCY` | Keep code/source status separate from Draft contract and production/live runtime. |
| Schema and Study Web | Legacy DDL has resources, V1-PILOT lacks generic resources; app source/router/package absent. | `SCHEMA DISCREPANCY / UNWIRED` | Production schema and screen runtime are not verified; implementation remains blocked. |
| Design/accessibility | Static prototype differs from Study Web guide; no responsive or contrast measurement. | `DESIGN DISCREPANCY / NOT VERIFIED` | Align implementation to canonical guide; no WCAG pass claim. |

## CHANGES

- Files changed: `GS-06_PLAN.md`, `GS-06.md`, `apps/study-client/docs/list_screen.md`, `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`, this worklog. Existing marker JSON/SVG and `screen_annotated.png` passed the audit and remain unchanged.
- CONTEXT_UPDATES: none.
- Context pages changed: none.
- Assumptions: none.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| Objective read | `/home/daovh/.codex/attachments/f6127670-d01c-46c9-b22a-2adfcbe78641/goal-objective.md` reread before continuing. | VERIFIED |
| Docs worklog preflight | Selector returned three exact-type docs worklogs; AD-01, AD-02, AD-03 read in full. | VERIFIED |
| Original assets | PNG IHDR `1486×1600`; source PNG/HTML SHA-256 values match the recorded originals; annotated PNG is `3132×3200` and was visually inspected. | VERIFIED |
| Marker/DD/SVG audit | Python standard-library audit: 23 ordered unique markers and coordinates; 23 SVG circles, labels and leader endpoints match JSON; embedded SVG PNG hash matches original; 23/23 DD element rows map; sections A–F and 10/10 event specs with trigger, precondition, input, processing, output and exception fields. | VERIFIED |
| Links and global inventory | No Markdown-relative links found in GS-06 DD/plan. Inventory has 83 unique IDs matching 83 folders and 83 tracker rows; all six core files are present in 83/83 folders (presence only; not DD quality evidence). | VERIFIED |
| Whitespace and scoped diff | Authored-text scan found no unexpected trailing whitespace across DD, plan, JSON, SVG, worklog and trackers; six quoted Markdown hard-break lines were preserved. `git diff --check -- apps/study-client/docs/list_screen.md apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` passed. | VERIFIED |
| Application tests/runtime | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: #11 collection/cardinality/visibility contract and route; #12 access/signer/expiry discrepancy; legacy-vs-V1-PILOT schema and live deployment; Study Web source/router; loaded/list/error design and Study design-system/accessibility alignment.
- Next owner/action: GS-06 re-audit is complete with `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED`; continue with GS-07 in a separate session.
