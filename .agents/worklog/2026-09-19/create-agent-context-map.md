---
task_id: "2026-09-19-create-agent-context-map"
date: "2026-09-19"
primary_task_type: "docs"
secondary_task_types: ["context-maintenance", "test"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: [".agents/context-map.md", ".agents/context-manifest.json", "scripts/validate-agent-context.mjs"]
status: "PARTIAL"
---

# Worklog: Tạo bản đồ liên kết Agent Context

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-19/2026-09-19-upgrade-agent-workflow-worklog.md`
    - carry_forward: Manifest, workflow, template và validator phải được cập nhật cùng nhau khi thay đổi context governance.
  - path: `.agents/worklog/2026-09-19/mobile-agent-context-inventory.md`
    - carry_forward: Map phải phân biệt source-backed, wired, unwired, placeholder và không suy diễn từ tên file.
  - path: `.agents/worklog/2026-09-18/agents-context-registry.md`
    - carry_forward: Page graph, skill/resource registry, status và validator là các phần liên kết của cùng context system.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Có một map Markdown canonical dưới `.agents/context-map.md` mô tả load order,
  physical tree, registry graph và cross-scope contract graph.
- `context-manifest.json` vẫn là machine-readable source of truth và đăng ký
  map mới.
- Validator phải kiểm tra map tồn tại, link hợp lệ và mọi registry path đều
  được map đề cập.

## CURRENT_BEHAVIOR

- Context đã có root router, project pages, 6 scopes, Web subcontexts, 2 skills,
  7 workflows, 6 contracts và worklog preflight nhưng chưa có một map tổng hợp.
- `scripts/validate-agent-context.mjs` trước task chỉ kiểm tra page graph/registry
  hiện có, chưa kiểm tra coverage của context map.

## SOURCE_TRACE

```text
AGENTS.md
-> .agents/AGENTS.md
-> .agents/context-manifest.json
-> .agents/project/INDEX.md + project pages
-> scope AGENTS.md/INDEX.md + subcontext pages
-> skills/workflows/contracts/worklog registry
-> .agents/context-map.md
-> scripts/validate-agent-context.mjs
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Human-readable map | No aggregate `.agents` map existed before task | RESOLVED | Added canonical tree and relationship map |
| Machine/human registry link | Manifest had no `contextMap` field | RESOLVED | Added `contextMap` and validator coverage checks |
| Historical source drift | Full validator still reports existing Study/Work/Web/DB Admin drift from snapshot | CONTEXT_STALE | Does not block map/registry validation with `--skip-drift` |
| Web boundary | Study Web is Vue subcontext; Work Web is React parent graph reuse | VERIFIED | Map records them separately and forbids pattern mixing |

## CHANGES

- Files changed: `.agents/context-map.md`, `.agents/context-manifest.json`,
  `.agents/AGENTS.md`, `scripts/validate-agent-context.mjs` and this worklog.
- CONTEXT_UPDATES: Registered the human-readable map, added path coverage and
  link validation, and documented project/scope/skill/workflow/contract/worklog
  relationships.
- Context pages changed: global registry only; no runtime source, API, database
  or scope behavior was changed.
- Assumptions: resource paths are represented at canonical directory/entry level;
  generated/cache/example descendants are not expanded into the map tree.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `python3 -m json.tool .agents/context-manifest.json` | Manifest parsed successfully | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Only pre-existing source `CONTEXT_STALE` reports remain | CONTEXT_STALE |
| `git diff --check` | Passed | VERIFIED |
| Map coverage check | All manifest project/scope/subcontext/skill/workflow/contract/worklog paths are mentioned | VERIFIED |
| Vue/React boundary review | Study Web and Work Web are represented as separate nodes | VERIFIED |

## HANDOFF

- Remaining blockers: Existing application source drift remains outside this
  documentation-only task.
- Next owner/action: Update `context-map.md` together with the manifest whenever
  a registered context node, relationship or workflow changes.
