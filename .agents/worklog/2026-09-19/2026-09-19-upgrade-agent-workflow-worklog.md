---
task_id: "2026-09-19-upgrade-agent-workflow"
date: "2026-09-19"
primary_task_type: "docs"
secondary_task_types: ["coding", "test", "context-maintenance"]
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: [".agents/context-manifest.json", ".agents/worklog", "scripts/select-worklogs.mjs", "scripts/validate-agent-context.mjs"]
status: "PARTIAL"
---

# Worklog: Nâng cấp agent workflow và di chuyển worklog

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-09-19/mobile-agent-context-inventory.md`
    - carry_forward: Context phải source-backed, inventory phải phân biệt runtime và unwired/stub.
  - path: `.agents/worklog/2026-09-18/agents-context-registry.md`
    - carry_forward: Registry, status, page graph và validator là các nguồn phải cập nhật cùng nhau.
  - path: `.agents/worklog/2026-09-18/integrate-create-dd-mobile-context.md`
    - carry_forward: Skill/resource wiring phải được kiểm tra bằng manifest và context validator.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Worklog canonical nằm dưới `.agents/worklog/YYYY-MM-DD/`.
- Mỗi task đọc tối đa 3 worklog gần nhất có cùng `primary_task_type`; thiếu thì đọc toàn bộ log có sẵn và ghi shortage.
- Workflow, manifest, template và validator phải cùng mô tả preflight này.

## CURRENT_BEHAVIOR

- 16 worklog lịch sử nằm dưới `docs/devs/worklogs`; `.agents/worklog` mới chỉ có README/template.
- Validator cũ coi mọi file dưới `.agents/worklog` là context graph candidate và chưa kiểm tra preflight registry.
- Node không có trong shell; Deno compatibility runner có thể chạy validator và selector.

## SOURCE_TRACE

```text
AGENTS.md
-> .agents/AGENTS.md
-> .agents/project/workflows.md
-> .agents/context-manifest.json
-> .agents/worklog/{README.md,TEMPLATE.md,YYYY-MM-DD/*.md}
-> scripts/select-worklogs.mjs
-> scripts/validate-agent-context.mjs
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Historical source path | 16 logs were under `docs/devs/worklogs`; all are now under `.agents/worklog` | RESOLVED | Legacy path is absent and registered as forbidden |
| Historical metadata | `repository-capability-review.md` and `work-server-dd-rewrite.md` lack canonical frontmatter | COMPATIBILITY | Selector parses their legacy metadata without rewriting historical content |
| Exact context validation | Existing source changes are newer than manifest snapshot in Study/Work/Web/DB Admin roots | CONTEXT_STALE | Registry validation passes with `--skip-drift`; source drift remains an existing handoff item |
| Node runtime | `node` is unavailable; Deno 2.9.6 is available | DECLARED_NOT_RUNNABLE | Verification uses the accepted Deno compatibility invocation |

## CHANGES

- Files changed: root/context routers, project and scope workflows, worklog contract/template, manifest, selector/validator scripts, docs/devs README, DD worklog reference, and 16 moved historical logs.
- CONTEXT_UPDATES: Added mandatory same-primary-type worklog preflight, canonical worklog root, selector registry, shortage policy and legacy path guard.
- Context pages changed: `AGENTS.md`, `.agents/AGENTS.md`, `.agents/project/workflows.md`, scope workflow READMEs, `.agents/context-manifest.json`.
- Assumptions: personal member timesheets under `docs/devs/<member>/worklogs/` are outside this migration; no runtime/API/database behavior changed.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | 3 docs logs selected in date/path order | VERIFIED |
| Selector for `coding` | 3 matching logs selected | VERIFIED |
| Selector for `fix` and `test` | 1 matching log each; shortage 2 reported | VERIFIED |
| Selector for unknown `architecture` type | 0 logs; shortage 3 reported | VERIFIED |
| `python3 -m json.tool .agents/context-manifest.json` | Manifest parsed successfully | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs --skip-drift` | `AGENT_CONTEXT_OK` | VERIFIED |
| `deno run --allow-read --allow-run --allow-env scripts/validate-agent-context.mjs` | Existing source drift reported in Study/Work/Web/DB Admin | CONTEXT_STALE |
| `git diff --check` | Passed | VERIFIED |
| Worklog migration count/path check | 16 entries under `.agents/worklog`; `docs/devs/worklogs` absent | VERIFIED |

## HANDOFF

- Remaining blockers: Refresh `sourceCommit` and affected scope context only when the existing application source drift is intentionally reconciled; this task did not change that source.
- Next owner/action: Use the selector and record `PRIOR_WORKLOG_REVIEW` in every future task worklog before deep inspection or edits.
