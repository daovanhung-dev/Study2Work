---
task_id: "2026-11-09-code-review-skill-pack"
date: "2026-11-09"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["mobile-work", "web-work", "server-work", "server-study", "server-ai", "db-admin"]
cross_scope_dependencies: ["root AGENTS router -> code-review skill/workflow registry -> six scopeRefs"]
status: "PARTIAL"
---

# Worklog: Tạo và tích hợp skill review code chỉ đọc

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 266 worklog cùng loại; đã chọn và đọc đủ 3.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-08/create-84-study-screen-dds.md`
    - carry_forward: Verify registry wiring rather than assuming a skill is active because its files exist; report context validator baseline failures separately.
  - path: `.agents/worklog/2026-11-08/design-study-screen-gs07-reaudit.md`
    - carry_forward: Keep expected/current behavior and evidence status separate; do not promote local test source to runtime evidence.
  - path: `.agents/worklog/2026-11-08/design-study-screen-st01-reaudit.md`
    - carry_forward: Resolve source and contract status before making claims; preserve unresolved facts as explicit gaps.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Add one read-only `code-review` skill for user-requested diff reviews or path/module audits across all six code scopes. Check local rules, reuse, clean/maintainable design, and security. Report actionable findings in Vietnamese with evidence; do not edit code, run tests, or post PR comments.
- Canonical contract/approved plan: User-approved implementation plan in this conversation; official reference approaches are the OpenAI Codex read-only review-agent sample and OpenAI Plugins reviewer prompt.

## CURRENT_BEHAVIOR

- Source/config: Root task taxonomy currently has `coding`, `fix`, `docs`, and `test`; skill registry has DD skills only; workflow registry has no code-review workflow. Six scopes are declared, but current checkout is missing `.agents/db-admin/AGENTS.md` and `.agents/db-admin/INDEX.md`.
- Runnable tests: None requested or run. Context validator must run because agent context is changing.
- Runtime wiring: No code-review skill or workflow registered. The root router is the mandatory task entry.

## SOURCE_TRACE

```text
user review request -> root AGENTS classification/trigger -> manifest code-review skill + workflow -> relevant scope AGENTS/index and exact source/contract/tests -> read-only Vietnamese report
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Review task type | Root router and worklog template expose only coding/fix/docs/test. | `MISSING_ROUTING_CATEGORY` | Add `review` so a read-only review is not mislabeled as a test run. |
| DB Admin context | Manifest declares DB Admin scope paths, but both entry and index files are absent in current checkout. | `NOT_FOUND` | Wire review through root router and scope registry only; do not reconstruct unrelated context pages. |
| Context validator baseline | Prior worklog reports missing DB Admin paths and orphan `create_dd_screen` resources. | `BASELINE_REPORTED_NOT_RECHECKED` | Run validator after changes and report exact current output without expanding scope. |

## CHANGES

- Files changed: `.agents/skills/code-review/SKILL.md`, `.agents/skills/code-review/references/review-checklist.md`, `.agents/skills/code-review/references/report-format.md`, root/global agent routers, skills index, workflow registry, context manifest/map, five existing scope indexes, worklog README/template, and this worklog.
- CONTEXT_UPDATES: Registered `code-review` as an explicit-request-only workflow/skill for all six scopes; added `review` as a task type so reviews have exact-type worklogs.
- Context pages changed: root `AGENTS.md`, `.agents/AGENTS.md`, `.agents/context-map.md`, `.agents/skills/INDEX.md`, `.agents/project/workflows.md`, and existing Mobile/Web/Study Server/Work Server/AI Server scope indexes. DB Admin entry/index remain `NOT_FOUND` and were not recreated.
- Assumptions: One orchestrator skill with four review lenses; diff first and path/module fallback; report in Vietnamese; inspect test source but never execute tests; preserve worklog as required audit record.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| Docs worklog selector + selected logs | READY; three exact-type logs read in full. | VERIFIED |
| Current router, skill/workflow indexes, manifest, context map and validator wiring | Read before edits. | VERIFIED_STATIC_ONLY |
| Manifest structure and six scopeRefs | JSON parsed; skill and workflow entries reference each other; all six declared scope keys contain `code-review` in `skillRefs`. | VERIFIED_STATIC_ONLY |
| Application tests | Not requested; not run. | NOT_RUN |
| `node scripts/validate-agent-context.mjs` | `AGENT_CONTEXT_INVALID`; missing DB Admin context/source paths and broken links, 33 orphan resources under the pre-existing unregistered `create_dd_screen` pack, and `CONTEXT_STALE` for `server-study`, `server-work`, `web-work`, `web-work/work-web`, `mobile-work`, and `db-admin`. No error referenced the new `code-review` skill. | BASELINE_CONTEXT_DRIFT_REPORTED |
| Manifest/link registration | Manifest JSON parsed; registry and workflow cross-reference, all six scopeRefs/skillRefs, and code-review context-map links were checked; validator reported zero code-review-specific errors. | VERIFIED_STATIC_ONLY |
| `git diff --check` and new Markdown whitespace scan | No tracked diff whitespace errors; new skill and worklog Markdown have no trailing whitespace. | VERIFIED_STATIC_ONLY |
| Review acceptance scenarios | Skill instructions cover diff-origin filtering, current-state audit labeling, no-finding response, insufficient evidence, and read-only/no-test boundaries. | VERIFIED_BY_INSPECTION |
| Application tests | Not requested; not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: Repository-wide agent-context validation remains invalid due the listed baseline context/source drift; skill-specific registry checks show no new errors.
- Next owner/action: Skill implementation is complete. Restore or reconcile missing/stale context pages and register the separate `create_dd_screen` pack in a separate task.
