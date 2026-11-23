---
task_id: "2026-11-23-wire-utc-screen-skill-context"
date: "2026-11-23"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work"]
cross_scope_dependencies: []
status: "IN_PROGRESS"
---

# Worklog: Wire UTC Screen skill vào Study Web context

## READ_PLAN

| Path | Needed section/range | Task-specific reason | Status |
|---|---|---|---|
| `AGENTS.md` | Root router được cấp trong task context | Phân loại task, bootstrap và scope routing | `READ_FROM_CONTEXT` |
| `.agents/AGENTS.md` | Global context index, skill registry notes and validation rules | Xác định global registry pages cần đồng bộ | `READ_FROM_CONTEXT` |
| `.agents/context-map.md` | Skill graph, Study Web subcontext and workflow graph | Cập nhật human-readable context routing | `READ_FROM_CONTEXT` |
| `.agents/context-manifest.json` | `skills`, `workflows`, `scopes.web-work`, `subcontexts.study-web` | Wire machine-readable skill/workflow/scope/resource references | `READ_FROM_CONTEXT` |
| `.agents/project/agent-control.md` | Target/read-set/worklog rules | Tuân thủ task tracking và evidence | `READ_FROM_CONTEXT` |
| `.agents/target.md` | Active target table | Theo dõi 3 mục tiêu lá | `READ_FROM_CONTEXT` |
| `.agents/worklog/README.md` | Read-set and selector requirements | Bắt buộc worklog preflight | `READ_FROM_CONTEXT` |
| `.agents/worklog/TEMPLATE.md` | Required worklog sections | Khởi tạo worklog | `READ_FROM_CONTEXT` |
| `scripts/select-worklogs.mjs` | Selector CLI and matching behavior | Chọn worklog cùng loại `docs` | `READ_FROM_CONTEXT` |
| `scripts/validate-agent-context.mjs` | `contextNodes`, skill/resource registration, workflow and link checks | Establish baseline and verify resulting registry wiring | `READ_FROM_CONTEXT` |
| `.agents/skills/utc-screen-skill/SKILL.md` | Activation, input/output, 12-step process, stop/report rules | Định nghĩa skill trigger, scope and boundaries | `READ_FROM_CONTEXT` |
| `.agents/skills/utc-screen-skill/README.md` | Purpose, dependencies, commands and limits | Định nghĩa target and verification commands | `READ_FROM_CONTEXT` |
| `.agents/skills/INDEX.md` | Skill registry table and boundary rules | Đăng ký skill cho agent đọc thủ công | `READ_FROM_CONTEXT` |
| `.agents/project/workflows.md` | Validator baseline rule and Task routing table | Đăng ký workflow trigger and verification routing | `READ_FROM_CONTEXT` |
| `.agents/web-work/AGENTS.md` | Web scope and Study Web subcontext routing | Điều hướng từ scope entry đến UTC skill | `READ_FROM_CONTEXT` |
| `.agents/web-work/INDEX.md` | Web scope page/task table | Thêm link route cho Study Web UTC requests | `READ_FROM_CONTEXT` |
| `.agents/web-work/study/AGENTS.md` | Study Web router and screen workflow triggers | Thêm local skill activation boundary | `READ_FROM_CONTEXT` |
| `.agents/web-work/study/INDEX.md` | Study Web page graph and skill/workflow table | Thêm skill pointer to context index | `READ_FROM_CONTEXT` |
| `.agents/worklog/2026-11-23/wire-utc-screen-skill-context.md` | Current worklog, selected by mandatory selector | Phân biệt current task from historical docs worklogs | `READ_FROM_CONTEXT` |
| `.agents/worklog/2026-11-23/copy-stitch-html-to-dd-screens.md` | Summary, changes, verification, handoff | Carry forward recent Study Web documentation task | `READ` |
| `.agents/worklog/2026-11-23/load-study-client-context.md` | Summary, discrepancies, verification, handoff | Carry forward Study Web context findings | `READ` |
| `.agents/worklog/2026-11-21/2026-11-21-build-server-web-commands.md` | Worklog body was not selected | Do not substitute a nonselected log | `SKIPPED` |

## LEAF_TARGET_PLAN

| Target | Single operation | Acceptance evidence |
|---|---|---|
| Đăng ký skill UTC Screen cho Study Web | Wire skill entry, workflow, resource root and Study Web `skillRefs` in manifest | Validator recognizes `utc-screen` under `web-work/study-web`, registered resources and workflow |
| Gắn trigger UTC Screen vào global skill/workflow router | Update global skill index, context registry/map and common workflow routing | Human-readable pages identify UTC triggers, scope, workflow and boundaries |
| Gắn hướng dẫn UTC Screen vào Study Web context | Update Web parent and Study Web entry/index | Study Web context routes UTC requests to skill and keeps implementation/API-DD routes separate |

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-23/copy-stitch-html-to-dd-screens.md`
    - carry_forward: Recent docs task copied 82 reference HTML files into DD folders, preserved the 83 source files, and recorded a baseline-invalid context validator. No context page was modified.
  - path: `.agents/worklog/2026-11-23/load-study-client-context.md`
    - carry_forward: Study Web is routed under `web-work/study-web`; its previous context load found conflicting source-status prose, but those behavior details are not relevant to skill routing.
- selector also returned the newly created current worklog; it is not a prior task.
- shortage: `none` (296 matching docs worklogs available; 3 selected)

## EXPECTED_BEHAVIOR

- Requirement: Read `.agents/skills/utc-screen-skill` and wire it into agent context logic.
- Scope clarification: Register it only for `web-work/study-web`, as selected by the user during planning.
- Skill contract: Generate traceable screen-level test cases and UTC Excel from an existing DD; preserve `Chờ xác nhận DD` blockers and never claim execution without evidence.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Đăng ký skill UTC Screen cho Study Web | `0% → 100%` | Manifest recognizes `utc-screen`, the `web-work/study-web` scope, `utc-screen-generation` workflow and full resource directory; post-edit validator no longer reports UTC skill resources as orphans. |
| Gắn trigger UTC Screen vào global skill/workflow router | `0% → 100%` | Vietnamese and English triggers are registered; global skill index, context map and common workflow table route to UTC generation. |
| Gắn hướng dẫn UTC Screen vào Study Web context | `0% → 100%` | Study Web entry and index route UTC requests and state the boundary against screen implementation and Web/API DD authoring. |

## CURRENT_BEHAVIOR

- Before this task, source/config had skill files under `.agents/skills/utc-screen-skill/` but no manifest entry, Study Web `skillRefs`, or task trigger. After the change, the skill and workflow are registered and routed only from `web-work/study-web`.
- Runnable tests: No app tests apply; this task changes agent context only.
- Runtime/context wiring: `study-web-screen-coding` remains the Study Web implementation/demo workflow, and `createDD-markdown` handles Web/API DD authoring. UTC generation now has a separate route.

## SOURCE_TRACE

```text
UTC/testcase request for an existing Study Screen DD -> web-work/study-web context -> utc-screen-generation workflow -> utc-screen skill/resources -> JSON coverage check + Excel generation/structure check
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Context validator baseline | Before context edits, validator exits 1 with `AGENT_CONTEXT_INVALID`, including all Markdown files under `utc-screen-skill` as orphan resources, missing DB Admin context/source entries, a missing Study Web `.gitkeep`, and existing source drift. | `BASELINE_INVALID` | Registering the UTC skill should resolve its orphan-resource findings; unrelated baseline findings must remain identified and not be expanded into this task. |

## CHANGES

- Files changed: `.agents/AGENTS.md`, `.agents/skills/INDEX.md`, `.agents/context-map.md`, `.agents/context-manifest.json`, `.agents/project/workflows.md`, `.agents/web-work/AGENTS.md`, `.agents/web-work/INDEX.md`, `.agents/web-work/study/AGENTS.md`, `.agents/web-work/study/INDEX.md`.
- CONTEXT_UPDATES: Registered `utc-screen` with Study Web-only scope, its DD/test coverage triggers, full resource pack and `utc-screen-generation` workflow. Added skill and workflow routing to the global context graph and Study Web entry/index pages.
- Context pages changed: Global skill registry/router, context map, common workflow table, Web scope router/index, Study Web router/index.
- Assumptions: Skill is scoped to Study Web only; it designs UTC cases and does not author DD or establish runtime test execution.
- Target progress updates and completion evidence: registry and resource wiring is represented in the manifest; global triggers/workflow are listed in the registry, map and workflow table; Study Web-specific routing is in its entry and index. Final completion follows context validation.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/validate-agent-context.mjs` (pre-edit baseline) | Exit 1, `AGENT_CONTEXT_INVALID`; UTC resources are currently orphaned alongside unrelated DB Admin/source drift | `BASELINE_INVALID` |
| `jq empty .agents/context-manifest.json` | JSON parses successfully after registry edits | `PASS` |
| `git diff --check` | No whitespace errors in context edits | `PASS` |
| `node scripts/validate-agent-context.mjs` (post-edit) | Exit 1, `AGENT_CONTEXT_INVALID`; no UTC resource orphan is reported. Remaining findings are unrelated baseline drift: missing DB Admin context/source files, the missing Study Web `.gitkeep`, existing `create_dd_screen` orphan resources and stale source inventories. | `BASELINE_INVALID; UTC ROUTING VERIFIED` |

## HANDOFF

- Remaining blockers: Repository-wide context validator still flags unrelated missing DB Admin context/source files, one missing Study Web `.gitkeep`, existing `create_dd_screen` orphan resources and stale source inventories.
- Next owner/action: None for this task. The final context-validator invocation is run after this worklog and the active target table are closed.
