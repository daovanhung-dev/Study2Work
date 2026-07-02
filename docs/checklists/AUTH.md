# Checklist — AUTH

| Field | Value |
|---|---|
| Module code | `AUTH` |
| Module name | Authentication, Identity, Profile, RBAC |
| Last updated | `2026-07-02` |
| Source BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| Status model | `.agent/context/STATUS_MODEL.md` |

## Source BD Links

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `AUTH-BD-001` | `NOT_STARTED` | `2026-07-01` | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Sections 3.1, 3.2, 5.1, BR-AUTH, AUTH API catalogue. |

## Related DD List

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `AUTH-DD-001` | `DRAFT` | `2026-07-02` | `docs/api-dd/auth/; docs/api-dd/user/` | Canonical AUTH and USER API DD drafts created; coding still waits for approval. |

## Feature / Function / View List

| ID | Type | Status | Updated | Link | Note |
|---|---|---|---|---|---|
| `AUTH-F01` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AUTH/` | Register and verify email. |
| `AUTH-F02` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AUTH/` | Login, refresh token, logout, password reset. |
| `AUTH-F03` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AUTH/` | OAuth Google/GitHub. |
| `AUTH-F04` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AUTH/` | Own profile, baseline skills, RBAC/mentor scope. |

## DD Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AUTH-DD-STATUS` | `DRAFT` | `2026-07-02` | `docs/api-dd/auth/; docs/api-dd/user/` | API DD drafts generated; see `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md`. |

## Coding Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AUTH-CODE-STATUS` | `NOT_STARTED` | `2026-07-01` | `services/api/app/modules/identity/` | Canonical FastAPI foundation exists; no business API implementation evidence yet. |

## Test Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AUTH-TEST-STATUS` | `NOT_STARTED` | `2026-07-01` | `services/api/tests/` | No test command or test evidence yet. |

## Bug / Open Question

| ID | Status | Updated | Link | Description |
|---|---|---|---|---|
| `AUTH-BUG-001` | `NONE` | `2026-07-01` | `.agent/worklog/INDEX.md` | No AUTH bug recorded. |
| `AUTH-OQ-001` | `VERIFIED` | `2026-07-01` | `.agent/context/CONTEXT_INDEX.md` | Backend stack decision resolved by ADR-001; business API coding still requires approved API DD. |

## Expected Affected Code Files

| ID | Status | Updated | Path | Note |
|---|---|---|---|---|
| `AUTH-FILE-001` | `NOT_STARTED` | `2026-07-01` | `services/api/app/modules/identity/` | Canonical FastAPI module reference. |
| `AUTH-FILE-002` | `NOT_STARTED` | `2026-07-01` | `services/api/app/modules/profile/` | Canonical FastAPI profile module reference. |
| `AUTH-FILE-003` | `NOT_STARTED` | `2026-07-01` | `apps/web-student/src/modules/profile/` | Student profile UI skeleton reference. |

## Related Worklogs

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `AUTH-WL-001` | `DONE` | `2026-07-02` | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | Created canonical API DD draft package for this module group. |

## Verification Evidence

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AUTH-EV-001` | `VERIFIED` | `2026-07-02` | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | Documentation generation checks completed for canonical API DD drafts. |

## Next Work

| ID | Status | Updated | Link | Task |
|---|---|---|---|---|
| `AUTH-NEXT-001` | `NOT_STARTED` | `2026-07-02` | `docs/api-dd/auth/; docs/api-dd/user/` | Review DD drafts and resolve OPEN_QUESTION items before coding. |
