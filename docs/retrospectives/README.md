# Retrospectives

Retrospectives reduce repetition, context cost, and recurring mistakes. Do not reread all 30 worklogs when the index and checklists are enough.

## Cadence

| Field | Value |
|---|---|
| Frequency | After every 30 new sessions since the latest retrospective |
| Source of session truth | `.agent/worklog/INDEX.md` |
| Path format | `docs/retrospectives/RETRO_<START_SESSION>_<END_SESSION>.md` |
| Last updated | `2026-07-01` |

## Current State

| Item | Value |
|---|---|
| Latest retrospective | _none_ |
| Sessions covered | _none_ |
| Next trigger | After sessions `0001` through `0030` exist |

## Required Retrospective Template

```md
# Retrospective — <START_SESSION> to <END_SESSION>

| Field | Value |
|---|---|
| Sessions | `<START_SESSION>-<END_SESSION>` |
| Created | `YYYY-MM-DD` |
| Sources | `.agent/worklog/INDEX.md`, related checklists, risk worklogs |

## Repeated Work

- <Repeated workflow>

## Repeated Bugs

- <Repeated bug/fix>

## Token-Heavy Modules

- <Module and reason>

## Missing Or Conflicting Documents

- <OPEN_QUESTION or CONFLICT>

## Skills To Create Or Update

- <Skill action>

## Workflow Simplification

- <Improvement>

## Long Or Duplicated Context

- <Context action>

## Test Or Build Command Gaps

- <Command gap>

## Improvement Actions

| ID | Owner | Status | Action | Link |
|---|---|---|---|---|
| `<RETRO-ACTION-001>` | `<owner>` | `<status>` | `<action>` | `<link>` |
```

## Update Rule

Update `AGENTS.md` or `.agent/context/` only when an insight is stable, reusable, and prevents real agent mistakes.
