# Worklog Index

Worklogs trace work from BD, DD, checklist, and skill context to code, tests, bugs, and follow-up. Do not create fake worklogs for sessions without real coding, documentation, or verification work.

## Session Numbering

| Field | Value |
|---|---|
| Next session | `0003` |
| Path format | `.agent/worklog/YYYY-MM/<SESSION_NO>_<TASK_SLUG>.md` |
| Example | `.agent/worklog/2026-07/0003_<task_slug>.md` |
| Last updated | `2026-07-01` |

## Read Rule At Session Start

1. Select at most 10 latest worklogs from the index.
2. Open at most 5 full worklogs directly related to the current module or bug.
3. Prioritize worklogs with risk, failed tests, open questions, or the same module.

## Worklog Table

| Session | Date | Module | Task slug | Status | Risk | Worklog | Summary |
|---|---|---|---|---|---|---|---|
| `0002` | 2026-07-01 | `GLOBAL_CONTEXT/BACKEND` | `context_backend_refactor` | `DONE` | Docker Compose not started; pytest has dependency deprecation warning | `.agent/worklog/2026-07/0002_context_backend_refactor.md` | Migrated agent context to `.agent`, created `.codex` backend context, replaced empty NestJS skeleton with FastAPI foundation and removed empty out-of-scope placeholders. |
| `0001` | 2026-07-01 | `GLOBAL_DOCS/DIAGRAMS` | `study_diagrams_refresh` | `DONE` | Docker daemon unavailable; Java PlantUML fallback passed | `.agent/worklog/2026-07/0001_study_diagrams_refresh.md` | Refreshed Study-only use case, activity, class, and sequence diagram pack from canonical BD. |

## Required Worklog Template

```md
# Worklog - <SESSION_NO> <TASK_SLUG>

| Field | Value |
|---|---|
| Session | `<SESSION_NO>` |
| Time | `YYYY-MM-DD HH:mm TZ` |
| Module | `<MODULE_CODE>` |
| Feature/function | `<FEATURE/FUNCTION>` |
| Status | `<STATUS>` |

## Goal

<Goal of this session.>

## Context Read

- BD: `<link>`
- DD: `<link>`
- Checklist: `<link>`
- Skill: `<link or none>`

## Files Created Or Modified

| Path | Action | Note |
|---|---|---|
| `<path>` | `<created/modified/moved/deleted>` | `<note>` |

## Logic Changed

<Short implementation summary.>

## Tests Run

| Command/check | Result | Evidence |
|---|---|---|
| `<command>` | `<result>` | `<output/link>` |

## Bugs Found

| ID | Status | Description | Link |
|---|---|---|---|
| `<BUG-ID>` | `<status>` | `<description>` | `<link>` |

## Risks Or Unverified Points

- `<risk/open question>`

## Next Work

- `<next task>`

## Suggested Commit Message

`<type(scope): message>`
```

## Index Update Rule

After creating a new worklog, update the `Worklog Table`, relevant module checklist, and evidence links.
