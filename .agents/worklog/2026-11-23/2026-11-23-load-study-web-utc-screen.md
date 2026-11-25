---
task_id: "2026-11-23-load-study-web-utc-screen"
date: "2026-11-23"
primary_task_type: "test"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: ["Study Web GS-01 -> Study Server API #05/#06 design references in the Study endpoint catalog; server source/runtime not inspected"]
status: "VERIFIED"
---

# Worklog: Nạp context Study Web và skill UTC Screen

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Supplied router context | Route task and declare mandatory context; provided in task, so not reopened | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Scope registry, context graph, read-set/target/worklog rules | Mandatory global context and routing | `READ` |
| `.agents/context-map.md` | Canonical flow, Study Web node, skill/worklog graph | Select the registered Study Web context and skill workflow | `READ` |
| `.agents/context-manifest.json` | `web-work.study-web`, `utc-screen`, `utc-screen-generation`, skills index | Verify exact registered scope, skill, workflow, and resource paths | `CHECKED_BY_TOOL` |
| `.agents/project/agent-control.md` | Target, silent execution, read-set, worklog rules | Mandatory task control and evidence requirements | `READ` |
| `.agents/target.md` | Active target table | Initialize leaf targets for this context-loading task | `READ` |
| `.agents/worklog/README.md` | Worklog contract and preflight | Create this worklog and follow selector process | `READ` |
| `.agents/worklog/TEMPLATE.md` | Required worklog sections | Use canonical worklog structure | `READ` |
| `scripts/select-worklogs.mjs` | Selector behavior and command | Run required same-type worklog preflight | `READ` |
| `.agents/worklog/2026-11-23/2026-11-23-load-study-web-utc-screen.md` | Current worklog body selected by the mandatory type selector | Confirm the initialized record and read-set after selector output | `READ` |
| `.agents/worklog/2026-11-01/test-study-server-all-apis.md` | Selected `test` worklog body | Carry forward relevant Study testing conventions | `READ` |
| `.agents/worklog/2026-10-11/test-study-api13-avatar-quick.md` | Selected `test` worklog body | Carry forward relevant Study testing conventions | `READ` |
| `.agents/project/INDEX.md` | Project context entry and ownership overview | Load requested project-wide context before the Study Web subcontext | `READ` |
| `.agents/skills/INDEX.md` | UTC Screen registry entry and resource links | Load the project skill registry for the requested UTC workflow | `READ` |
| `.agents/web-work/AGENTS.md` | Scope rules and Study Web routing | Load parent web scope rules | `READ` |
| `.agents/web-work/INDEX.md` | Scope page graph and subcontext links | Route to the Study Web context | `READ` |
| `.agents/web-work/study/AGENTS.md` | Study Web instructions | Load `apps/study-client` context rules | `READ` |
| `.agents/web-work/study/INDEX.md` | Study Web overview (lines 1–85), Guest GS-01 status (lines 155–195), and page/skill routing (lines 235–265) | Load the registered app context and active screen status | `READ` |
| `.agents/web-study/design.md` | Study Web screen behavior/visual requirements relevant to GS-01 | Load the screen-level test design guide | `READ` |
| `.agents/web-study/frontend-rules.md` | Study Web frontend structure and UI constraints | Understand app structure and screen boundaries relevant to UTC | `READ` |
| `.agents/skills/utc-screen-skill/SKILL.md` | Full skill workflow | Apply the project-registered UTC Screen skill | `READ` |
| `.agents/skills/utc-screen-skill/` | Filename-only inventory of registered resources | Identify only the skill resources required by the skill instructions | `CHECKED_BY_TOOL` |
| `.agents/skills/utc-screen-skill/huong-dan/01_Quy_trinh_12_buoc.md` | Full 12-step checklist and acceptance criteria | Load first mandatory supporting guide referenced by the skill | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/02_Quy_tac_sinh_ca.md` | Test design techniques | Load mandatory case design guide referenced by the skill | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/03_Anh_xa_Excel_JSON.md` | JSON and workbook field mapping | Load output mapping guidance referenced by the skill | `READ` |
| `.agents/skills/utc-screen-skill/tham-chieu/Nguon_quoc_te.md` | Scope of cited international references | Load the reference guidance without claiming certification | `READ` |
| `.agents/skills/utc-screen-skill/huong-dan/04_Mau_lenh_giao_viec_cho_AI.md` | Reusable task prompt | Load the final mandatory supporting guide referenced by the skill | `READ` |
| `.agents/skills/utc-screen-skill/vi-du/GS-01/utc-gs01.json` | Metadata, blockers, one sample case per layer; example is explicitly unapproved | Inspect the sample structure named by the skill, without treating it as approval | `READ` |
| `.agents/skills/utc-screen-skill/bao-cao/GS01_Doi_chieu_DD.md` | Full report | Load prior screen-specific audit evidence relevant to active GS-01 | `READ` |
| `.agents/skills/utc-screen-skill/bao-cao/kiem-tra-gs01.json` | Full validation summary | Load prior validation summary without treating it as execution evidence | `READ` |
| `apps/study-client/docs/dd_screens/screen-index.md` | GS-01 catalog row and links to canonical screen DD | Confirm the active screen's canonical DD package and source/API identifiers | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/` | Filename-only inventory of the active screen DD package and assets | Identify the actual DD files and any referenced images before content reads | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/00-overview.md` | Full DD overview | Read the screen scope, status, actor, and blockers | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/01-ui-elements.md` | Full UI elements section | Read every listed element and design status | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/02-events.md` | Full events section | Read every described event and branch | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/03-data-flow.md` | Full data flow section | Read initial/load/data transformation and states | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/04-api-integration.md` | Full API integration section | Read API #05/#06 usage and contract fields | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/05-business-rules.md` | Full business rules section | Read confirmed and unresolved screen rules | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/06-navigation.md` | Full navigation section | Read routes and handoffs | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/07-test-cases.md` | Full test case references | Distinguish planning references from executed evidence | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/images/README.md` | Image usage/marker notes | Read instructions for clean and numbered reference images | `READ` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/images/screen-clean.png` | Full image | Visually inspect the unnumbered screen reference | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/images/screen-numbered.png` | Full image | Visually inspect the numbered component reference | `CHECKED_BY_TOOL` |
| `apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc/code.html` | Relevant screen DD content | Read the active IDE screen input for the requested UTC context | `READ` |
| `apps/study-client/docs/list_screen.md` | GS-01 catalog row and current source note | Follow Study Web screen catalog preflight | `READ` |
| `apps/study-client/docs/list_endpoint.md` | Endpoint #05 and #06 rows | Follow Study Web API catalog preflight and identify design API references | `READ` |
| `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/GS-01.md` | Source overview, current-source update, requirements and status sections | Load the linked screen source note and provenance | `READ` |
| `apps/study-client/docs/screen_stitch/02_guest_discovery/GS-01_danh-sach-khoa-hoc/code.html` | Hash comparison with active DD prototype; duplicate content | Avoid rereading an identical prototype file | `CHECKED_BY_TOOL` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Nạp chỉ mục context dự án | Read the project index and capture its relevant routing/ownership context | Project index findings are recorded in this worklog |
| Nạp context Study Web cho `apps/study-client` | Read the registered Study Web scope and required pages | Study Web scope, page graph, and app boundaries are recorded |
| Nạp skill và workflow tạo UTC Screen | Read the registered skill instructions and applicable resources | Skill requirements and verification workflow are recorded |
| Đọc DD GS-01 đang mở trong IDE | Read the active GS-01 screen DD | Screen scope and input status are recorded without generating a UTC |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `test`
- selector_command: `node scripts/select-worklogs.mjs --type test --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-23/2026-11-23-load-study-web-utc-screen.md`
    - carry_forward: Current task classification is `test`; selected current log confirms the declared Study Web and UTC context plan.
  - path: `.agents/worklog/2026-11-01/test-study-server-all-apis.md`
    - carry_forward: Server-side HTTP suite was backed by temporary branch and fakes; do not treat fake-backed checks as live DB/provider or deployment evidence. Its `server-study` implementation facts do not transfer to the Study Web app.
  - path: `.agents/worklog/2026-10-11/test-study-api13-avatar-quick.md`
    - carry_forward: API #13 test used injected storage/S3 stubs and did not verify remote storage; this is a server-side boundary and does not establish Study Web behavior.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Load project context, the `apps/study-client` context, and the UTC Screen creation skill for the active Study screen.
- Canonical contract/approved DD: Registered Study Web context and `utc-screen` skill in `.agents/context-manifest.json`; active GS-01 DD identified by IDE context.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Nạp chỉ mục context dự án | `0% → 0%` | Initial target; acceptance requires reading `.agents/project/INDEX.md`. |
| Nạp context Study Web cho `apps/study-client` | `0% → 0%` | Initial target; acceptance requires reading registered Study Web pages. |
| Nạp skill và workflow tạo UTC Screen | `0% → 0%` | Initial target; acceptance requires reading the registered skill and applicable resources. |
| Đọc DD GS-01 đang mở trong IDE | `0% → 0%` | Initial target; acceptance requires reading the active DD input. |
| Nạp chỉ mục context dự án | `0% → 100%` | Read `.agents/project/INDEX.md`; ownership/page routing and task-local loading boundary are recorded above. |
| Nạp context Study Web cho `apps/study-client` | `0% → 100%` | Read parent and Study Web routers/index, required design/frontend rules, both Study catalogs, and the registered GS-01 screen row. |
| Nạp skill và workflow tạo UTC Screen | `0% → 100%` | Read registered `utc-screen` skill, all five mandatory guides, sample spec, and GS-01 validation/audit reports; confirmed the sample remains unapproved. |
| Đọc DD GS-01 đang mở trong IDE | `0% → 100%` | Read all eight DD sections, view clean/numbered images, read the active HTML prototype as text, and load the linked GS-01 source note; matching screen-stitch HTML hash confirms it is a duplicate. |

## CURRENT_BEHAVIOR

- Registered context: `web-work.study-web` is `VERIFIED_WITH_UNWIRED_COMPONENTS`; its route/index points to `apps/study-client` and registers `utc-screen` for Study Screen test planning.
- Screen/DD evidence: GS-01 is `/courses`, Guest/Discovery, API #05 then #06. The supplied DD is `BLOCKED`: the image shows only an empty state; loaded cards, sort, count, paging, category filter, search handoff, cache/error policy, and related design decisions remain unresolved.
- Current-source documentation: the 2026-11-21 GS-01 re-audit and Study Web index report an Angular `/courses` route, #05→#06 callers, response validation, stale-request cancellation, and count/list mismatch handling. They keep browser/live API/DB runtime unverified. This task did not inspect app source to independently verify those statements.
- Runnable tests: the Study Web index reports focused Guest tests 37/37; the UTC sample reports 73 planned cases with 23/23 requirement, 16/16 element, and 11/11 event references. None were run in this task, and the UTC sample is explicitly not approved for execution.
- Runtime wiring: no browser, API, database, deployment, or app source verification was requested or performed.

## SOURCE_TRACE

```text
not applicable: context-loading task; no application behavior change
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Expected design vs current-source report | DD remains `BLOCKED` because loaded-state, controls, category filter, cache/error policy, and search handoff lack approved design; 2026-11-21 audit/context reports route and #05/#06 callers in source. Runtime is still unverified. | `DISCREPANCY` | Future UTC must distinguish approved requirements from source-derived or proposed cases and retain `Chờ xác nhận DD` for unresolved decisions. |
| Older DD source excerpts | Earlier sections in the converted GS-01 package say the Study app/route/caller are absent or `UNWIRED`; later 2026-11-20/21 re-audits say the route/caller are source-wired and supersede those claims. The app source was not independently rechecked here. | `CONTEXT_STALE` | Use the newer audit as the registered context pointer, but do not claim browser/runtime verification. |
| Image vs HTML prototype | The clean screenshot has no header brand and shows only the empty catalog, while prototype HTML has extra/duplicate brand navigation and a broken orphan-filter script; the DD records this as B08. | `DISCREPANCY` | Treat HTML and static image as design evidence; do not execute the HTML or infer runtime behavior. |

## CHANGES

- Files changed: This worklog and `.agents/target.md` only.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: The active GS-01 DD in IDE context is the screen input to load; no UTC artifact is requested yet.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type test --limit 3` | Selected the current task log and the two newest prior `test` logs; all three bodies were reviewed; shortage 0. | `VERIFIED_PREFLIGHT` |
| `find .agents/skills/utc-screen-skill ...` | Found registered skill, five guides, schema/scripts, GS-01 sample and reports. | `VERIFIED_INVENTORY` |
| `find apps/study-client/docs/dd_screens/GS-01-DanhSachKhoaHoc ...` | Found all eight DD sections, prototype HTML, image notes, and clean/numbered screenshots. | `VERIFIED_INVENTORY` |
| `sha256sum .../dd_screens/.../code.html .../screen_stitch/.../code.html` | Both open-tab prototypes have the same SHA-256 (`d354d54d…6038fe5`). | `VERIFIED_DUPLICATE` |
| `view_image` for `screen-clean.png` and `screen-numbered.png` | Viewed the empty-state reference and the 16 numbered markers. | `VERIFIED_VISUAL` |
| `node scripts/validate-agent-context.mjs` | Exit 1 (`AGENT_CONTEXT_INVALID`): missing DB Admin context/source paths, one missing Study Web tracked source path (`apps/study-client/src/app/features/auth/.gitkeep`), and source drift including `web-work/study-web`; no scope context pages were changed in this task. | `FAIL_EXISTING_REPO_DRIFT` |
| Study Web test suites / UTC validators | Not run; this request was for context loading only. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: No blocker for context loading. GS-01 DD remains blocked for future UTC approval; the sample is a plan only and is not approved. The context validator currently fails on repository-wide source/context drift, including Study Web's tracked-source inventory.
- Next owner/action: Context is ready for a follow-up UTC generation request; retain source-vs-design status and unapproved cases.
