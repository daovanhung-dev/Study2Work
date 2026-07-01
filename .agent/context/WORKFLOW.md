# Agent Workflow

This workflow standardizes how coding agents start a session, read context, change code or documentation, verify work, and record evidence.

## 1. Start Of Every Session

1. Read `AGENTS.md`.
2. Read `.agent/AGENT_GUIDE.md`.
3. Read `.agent/context/CONTEXT_INDEX.md`.
4. Read `.agent/worklog/INDEX.md`.
5. Identify module, feature/function, actor, and task type: BD, API DD, coding, test, fix, refactor, or docs.
6. Select at most 10 latest worklogs from the index.
7. Open at most 5 full worklogs directly related to the current module or bug.
8. Check the related checklist in `docs/checklists/`.
9. Read BD, API DD, diagram, Codex context, and code files needed for the task.
10. Before coding, summarize module, source documents, state, risk, files expected to change, and checks expected to run.

## 2. Before Coding

Do not code unless these are clear:

- Module, feature/function, actor, and affected user role.
- BD source, at minimum `docs/BD/Study2Work_Study_BD_Codex_Ready.md`.
- Approved API DD for any official business API implementation.
- Related module checklist and API checklist.
- Related `.codex` architecture context.
- Affected code, database/API/UI/test files.
- Short dependency-aware implementation plan.
- Expected tests/checks.

If a business rule is missing or documents conflict, record `OPEN_QUESTION` or `CONFLICT`; do not invent the rule.

## 3. After Coding

After every code or architecture change:

1. Run relevant tests, lint, format check, build, or static verification.
2. Do not claim verification without command output or explicit evidence.
3. Create a new worklog under `.agent/worklog/YYYY-MM/<SESSION_NO>_<TASK_SLUG>.md`.
4. Update `.agent/worklog/INDEX.md`.
5. Update relevant checklist status, links, and evidence.
6. If design changed, update the related DD changelog or create an `OPEN_QUESTION`.
7. If the same workflow repeats across sessions, evaluate whether a reusable skill is needed.

## 4. Worklog Requirements

Each worklog must include:

- Session number.
- Time.
- Module/feature/function.
- Goal.
- Context read.
- Files created, moved, deleted, or modified.
- Logic or architecture changed.
- Tests/checks run and result.
- Bugs found.
- Risks or unverified points.
- Next work.
- Suggested commit message.

## 5. API DD And Checklist

Study2Work uses one API Detail Design package per API operation. Do not group multiple behaviors into one DD.

When creating an API DD:

1. Read the BD for API code, actor, role/permission, business rule, state, table, and side effects.
2. Read related activity, sequence, and class diagrams in `docs/diagrams/`.
3. Read `docs/checklists/API.md` for catalog status, readiness, blockers, and open questions.
4. Read the full template in `docs/DD/Study2Work_API_DD_Template/`.
5. Copy the template into `docs/api-dd/<module-code-lowercase>/<api-code-lowercase>/`.
6. Fill files in this order: Overview, Request, Response, DataMapping, Error, History, checklist.
7. Update `docs/checklists/API.md` with DD path, status, completion, evidence, and open questions.
8. Update the module checklist when module status changes.
9. Do not implement an API while DD is `DRAFT`, `IN_REVIEW`, or `BLOCKED`, unless the user explicitly requests a prototype.
10. Do not create final DD/code for a candidate API marked `OPEN_QUESTION` until Product/Tech Lead approves the API catalog entry.

## 6. Skills

Review the latest 10 worklogs. Create or update a skill in `.agent/skills/<SKILL_ID>.md` only when at least one condition is met:

- The same manual workflow appears in at least 2 sessions.
- The same bug or fix pattern appears at least twice.
- The task is complex, multi-step, and reusable.
- The issue previously caused significant context waste or architectural drift.

Do not create a skill for a small one-off task.

## 7. Retrospective

After every 30 new sessions since the latest retrospective:

1. Create `docs/retrospectives/RETRO_<START_SESSION>_<END_SESSION>.md`.
2. Summarize from `.agent/worklog/INDEX.md`, module checklists, and risk worklogs.
3. Do not open all 30 full worklogs unless required.
4. Update `AGENTS.md` or `.agent/` only for stable reusable improvements.

## 8. Evidence Rules

- `VERIFIED` requires evidence: command output, test report, screenshot, reviewer confirmation, issue link, or worklog evidence.
- `DONE` requires code, tests/checks, docs, checklist, and worklog completion for the task scope.
- If a command cannot run because the environment is missing, record `BLOCKED` or `OPEN_QUESTION`; do not invent a substitute.

