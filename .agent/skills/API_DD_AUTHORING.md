# Skill - API_DD_AUTHORING

## Goal

Create or update Study2Work API Detail Design packages consistently from BD, API checklist, diagrams and the canonical DD template.

## When To Use

- The user asks to create API DDs from `docs/checklists/API.md`.
- A canonical API row moves from `NOT_STARTED` to `DRAFT`, `IN_REVIEW` or `APPROVED`.
- A DD must be reviewed or refreshed after BD/checklist/diagram changes.

## Inputs

- `docs/checklists/API.md` canonical API row.
- `docs/BD/Study2Work_Study_BD_Codex_Ready.md` business context.
- Related diagrams under `docs/diagrams/`.
- Template under `docs/DD/Study2Work_API_DD_Template/`.

## Files To Read

- `AGENTS.md`
- `.agent/AGENT_GUIDE.md`
- `.agent/worklog/INDEX.md`
- `docs/checklists/API.md`
- `docs/BD/Study2Work_Study_BD_Codex_Ready.md`
- `docs/DD/Study2Work_API_DD_Template/`
- Related `docs/diagrams/**` files listed in the API checklist row

## Steps

1. Confirm the API is canonical and not `BLOCKED / OPEN_QUESTION` unless the user explicitly asks for a blocked stub.
2. Create one folder per operation at `docs/api-dd/<module>/<api-code-lowercase>/`.
3. Copy the full template structure and fill all files in this order: Overview, Request, Response, DataMapping, Error, History, checklist.
4. Write human review notes in Vietnamese when requested, while keeping contract identifiers, fields, enums, tables and business codes in English/camelCase/snake_case.
5. Replace every template placeholder; use `OPEN_QUESTION` for missing source detail instead of inventing an approved contract.
6. Keep DD status as `DRAFT` unless approval evidence exists.
7. Update API checklist, related module checklist, worklog index and DD history/evidence.

## Rules

- One DD package describes exactly one API operation.
- Do not create final DD/code for candidate APIs marked `BLOCKED / OPEN_QUESTION` without explicit approval.
- Do not include employer, recruitment, job, CV, interview, matching, shortlist, offer or hiring workflows in Study DDs.
- Every response must use the standard envelope with `businessCode`, `message`, `timestamp`, `traceId` and `data` or `errors`.
- Mutation APIs must document transaction, idempotency, concurrency, audit and async side effects.
- Protected APIs must document authentication, permission and ownership/scope.

## Verification

- `rg -n "{|}" docs/api-dd` returns no matches.
- Expected API DD folder/file counts match the task scope.
- All fenced `json` examples parse successfully.
- `docs/checklists/API.md` has the expected DD status/completion values.
- `git diff --check` has no whitespace errors.

## Example

For `AUTH-REGISTER-001`, create `docs/api-dd/auth/auth-register-001/`, fill every template file, set `Status = DRAFT`, link register/verify diagrams, document duplicate email and password secrecy rules, and record schema uncertainties as `AUTH-REGISTER-001-OQ-*`.

## Worklog/Bug Links

- `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md`
