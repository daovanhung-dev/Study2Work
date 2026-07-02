# Skills Index

Skills are reusable instructions for repeated workflows or bug patterns. Do not create a skill before there is worklog evidence.

## Creation Rule

Review the latest 10 worklogs. Create `.agent/skills/<SKILL_ID>.md` when at least one condition is true:

- The same manual workflow appears in at least 2 sessions.
- The same bug or fix pattern appears at least twice.
- The task is complex, multi-step, and reusable across modules.
- A previous issue caused significant context waste or architecture drift.

Do not create a skill for small one-off work.

## Skill Table

| Skill ID | Status | Created | Updated | Related modules | Trigger | Worklog evidence | File |
|---|---|---|---|---|---|---|---|
| `API_DD_AUTHORING` | `ACTIVE` | 2026-07-02 | 2026-07-02 | API DD / documentation | Canonical API DD creation is complex and reusable across modules. | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | `.agent/skills/API_DD_AUTHORING.md` |

## Required Skill Template

```md
# Skill - <SKILL_ID>

## Goal

<What this skill helps repeat safely.>

## When To Use

<Trigger conditions.>

## Inputs

- <Input/precondition>

## Files To Read

- <Path>

## Steps

1. <Step>

## Rules

- <Rule>

## Verification

- <Check/evidence>

## Example

<Example>

## Worklog/Bug Links

- <Worklog or bug link>
```

## Update Rule

After creating or editing a skill, update the `Skill Table` and link the skill in relevant module checklists.
