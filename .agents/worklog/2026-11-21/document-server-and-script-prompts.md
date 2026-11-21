---
task_id: "2026-11-21-document-server-and-script-prompts"
date: "2026-11-21"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study", "server-work", "server-ai"]
cross_scope_dependencies: ["Các README/manifest/script của từng server con -> docs/prompts/build_server.md và docs/prompts/script.md"]
status: "VERIFIED"
---

# Worklog: Tạo tài liệu lệnh chạy server và script

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 290 available; 3 selected and read; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-21/reconcile-study-screen-completion-status.md`
    - carry_forward: Keep source and current runtime evidence separate; preserve unrelated dirty changes.
  - path: `.agents/worklog/2026-11-21/refresh-study-screen-completion-percentages.md`
    - carry_forward: Use `.agents/target.md` as the sole live target tracker; record completion evidence in the worklog and remove completed target rows.
  - path: `.agents/worklog/2026-11-21/revise-agent-target-tracking-context.md`
    - carry_forward: Keep only the three-column active target table and preserve historical worklogs and unrelated changes.
- shortage: `none`.

## EXPECTED_BEHAVIOR

- Requirement: Create `docs/prompts/build_server.md` with a table for service number, name, technology, command and address; create `docs/prompts/script.md` with commands to run the operational scripts. Commands must run from each server subproject's own root.
- Approved interpretation: Populate the server command column with local startup commands from current README/source, as clarified by the user. Cover the three present backend services and operational scripts in Study and Work Server; state script preconditions and database effects.

## TARGET_UPDATES

| Target | From → to | Evidence / reason |
|---|---:|---|
| Tạo tài liệu lệnh chạy server và script | `— → 0%` | Created active target; acceptance is both requested prompt documents with source-backed commands and subproject working-directory instructions. |
| Tạo tài liệu lệnh chạy server và script | `0% → 40%` | Rechecked current server READMEs, package manifests and script entrypoints; confirmed service addresses, script commands and subproject roots. |
| Tạo tài liệu lệnh chạy server và script | `40% → 85%` | Drafted both requested documents with three local server commands and all discovered operational script commands, including database effects and working directories. |
| Tạo tài liệu lệnh chạy server và script | `85% → 100%` | Read back both documents; the requested table, service commands/addresses, script flags, database effects and subproject working directories match the current README and source evidence. |

## CURRENT_BEHAVIOR

- Source/config: `docs/prompts/` is empty. Current source has Study, Work and AI server directories; DB Admin server directories are absent. Their README/package manifests declare the local startup commands and addresses. Study has Admin and two seed scripts; Work has an account seed script plus an internal Prisma wrapper; AI's declared `ai-server` console entrypoint only prints a greeting and does not start the API.
- Runnable tests: Not applicable to this documentation task; no tests have been run.
- Runtime wiring: Server startup is documented by each subproject README. Work Server script commands are exposed through `apps/work-server/package.json`.

## SOURCE_TRACE

```text
subproject README/package/script source -> verified service/script command -> docs/prompts reference
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Repository deployment map vs current server roots | `docs/gui/deploy/ip.md` refers to a root pnpm launcher and DB Admin service, while current root workspace/DB Admin server files are absent; Work README provides a direct subproject `npm run s2w` command. | `SOURCE_DISCREPANCY` | Document commands supported by current subproject README/source; omit unavailable DB Admin service. |
| AI console entrypoint vs API startup | `pyproject.toml` declares `ai-server`, but `src/ai_server/__init__.py` only prints a greeting; the README starts the API with Uvicorn. | `DECLARED_NOT_SERVER` | Identify the console entrypoint as a placeholder and document Uvicorn as the API start command. |

## CHANGES

- Files changed: `docs/prompts/build_server.md`, `docs/prompts/script.md`, `.agents/target.md`, and this worklog.
- CONTEXT_UPDATES: None; this task creates user-facing prompt documentation only.
- Context pages changed: None.
- Assumptions: Shell commands are run from the named server subproject. Operational seed scripts are included with clear database-effect notes; internal helpers and tests are excluded. AI's declared console entrypoint is documented as a placeholder because it does not start the API.
- Target progress updates and completion evidence: see `TARGET_UPDATES`.

## VERIFICATION

| Command | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` | `READY`; three selected docs worklogs were read; no shortage. | `VERIFIED_PREFLIGHT` |
| Current README, package manifest and script source inspection | Local startup commands/addresses and operational script modes were reconciled with each server subproject; AI console entrypoint behavior was checked. | `VERIFIED_STATIC` |
| Readback of `docs/prompts/build_server.md` and `docs/prompts/script.md` | Required table columns and three service rows are present; script commands, working directories, preconditions and database effects are documented. | `VERIFIED_STATIC` |
| Automated tests | Not run; this is a documentation-only task and tests were not requested. | `NOT_RUN` |

## HANDOFF

- Remaining blockers: None.
- Next owner/action: None; both requested prompt documents are complete.
