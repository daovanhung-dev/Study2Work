# Checklist — ADMIN

| Field | Value |
|---|---|
| Module code | `ADMIN` |
| Module name | Admin and Platform Governance |
| Last updated | `2026-07-02` |
| Source BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| Status model | `.agent/context/STATUS_MODEL.md` |

## Source BD Links

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `ADMIN-BD-001` | `NOT_STARTED` | `2026-07-01` | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Section 5.7, BR-ADMIN, BR-PLATFORM, ADMIN API catalogue. |

## Related DD List

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `ADMIN-DD-001` | `DRAFT` | `2026-07-02` | `docs/api-dd/admin/` | Canonical ADMIN API DD drafts created; coding still waits for approval. |

## Feature / Function / View List

| ID | Type | Status | Updated | Link | Note |
|---|---|---|---|---|---|
| `ADMIN-F01` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/ADMIN/` | User/mentor management and scope assignment. |
| `ADMIN-F02` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/ADMIN/` | Learning content and rubric governance. |
| `ADMIN-F03` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/ADMIN/` | Settings, feature flags, audit, moderation. |
| `ADMIN-F04` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/ADMIN/` | Study analytics. |

## DD Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `ADMIN-DD-STATUS` | `DRAFT` | `2026-07-02` | `docs/api-dd/admin/` | API DD drafts generated; see `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md`. |

## Coding Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `ADMIN-CODE-STATUS` | `NOT_STARTED` | `2026-07-02` | `services/api/app/modules/platform/` | Canonical FastAPI foundation exists; no business API implementation evidence yet. |

## Test Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `ADMIN-TEST-STATUS` | `NOT_STARTED` | `2026-07-01` | `tests/` | No test command or test evidence yet. |

## Bug / Open Question

| ID | Status | Updated | Link | Description |
|---|---|---|---|---|
| `ADMIN-BUG-001` | `NONE` | `2026-07-01` | `.agent/worklog/INDEX.md` | No ADMIN bug recorded. |
| `ADMIN-OQ-001` | `VERIFIED` | `2026-07-02` | `.agent/context/CONTEXT_INDEX.md` | Out-of-scope admin placeholder removed from Study scope. |

## Expected Affected Code Files

| ID | Status | Updated | Path | Note |
|---|---|---|---|---|
| `ADMIN-FILE-001` | `NOT_STARTED` | `2026-07-02` | `services/api/app/modules/platform/` | Canonical FastAPI platform/admin foundation reference. |
| `ADMIN-FILE-002` | `NOT_STARTED` | `2026-07-02` | `apps/web-admin/src/modules/` | Study-only admin client skeleton reference. |
| `ADMIN-FILE-003` | `NOT_STARTED` | `2026-07-02` | `docs/architecture/PROJECT_ARCHITECTURE.md` | Canonical server/client architecture reference. |

## Related Worklogs

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `ADMIN-WL-001` | `DONE` | `2026-07-02` | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | Created canonical API DD draft package for this module group. |

## Verification Evidence

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `ADMIN-EV-001` | `VERIFIED` | `2026-07-02` | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | Documentation generation checks completed for canonical API DD drafts. |

## Next Work

| ID | Status | Updated | Link | Task |
|---|---|---|---|---|
| `ADMIN-NEXT-001` | `NOT_STARTED` | `2026-07-02` | `docs/api-dd/admin/` | Review DD drafts and resolve OPEN_QUESTION items before coding. |
