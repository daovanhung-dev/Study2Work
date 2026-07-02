# Checklist — AI

| Field | Value |
|---|---|
| Module code | `AI` |
| Module name | AI Learning Support |
| Last updated | `2026-07-02` |
| Source BD | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` |
| Status model | `.agent/context/STATUS_MODEL.md` |

## Source BD Links

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `AI-BD-001` | `NOT_STARTED` | `2026-07-01` | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Section 5.6, BR-AI, AI API catalogue. |

## Related DD List

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `AI-DD-001` | `DRAFT` | `2026-07-02` | `docs/api-dd/ai/` | Canonical AI API DD drafts created; coding still waits for approval. |

## Feature / Function / View List

| ID | Type | Status | Updated | Link | Note |
|---|---|---|---|---|---|
| `AI-F01` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AI/` | AI roadmap suggestion. |
| `AI-F02` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AI/` | Code explanation and debugging hints. |
| `AI-F03` | Feature | `NOT_STARTED` | `2026-07-01` | `docs/DD/AI/` | Learning insight based on authorized context. |

## DD Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AI-DD-STATUS` | `DRAFT` | `2026-07-02` | `docs/api-dd/ai/` | API DD drafts generated; see `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md`. |

## Coding Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AI-CODE-STATUS` | `NOT_STARTED` | `2026-07-01` | `services/api/app/modules/ai/` | Canonical FastAPI foundation exists; no business API implementation evidence yet. |

## Test Status

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AI-TEST-STATUS` | `NOT_STARTED` | `2026-07-01` | `tests/` | No test command or test evidence yet. |

## Bug / Open Question

| ID | Status | Updated | Link | Description |
|---|---|---|---|---|
| `AI-BUG-001` | `NONE` | `2026-07-01` | `.agent/worklog/INDEX.md` | No AI bug recorded. |
| `AI-OQ-001` | `OPEN` | `2026-07-01` | `docs/BD/Study2Work_Study_BD_Codex_Ready.md` | Provider, rate limits and redaction policy need DD/ADR detail before coding. |

## Expected Affected Code Files

| ID | Status | Updated | Path | Note |
|---|---|---|---|---|
| `AI-FILE-001` | `NOT_STARTED` | `2026-07-01` | `services/api/app/modules/ai/` | Canonical FastAPI module reference. |
| `AI-FILE-002` | `NOT_STARTED` | `2026-07-01` | `apps/web-student/src/modules/dashboard/` | Potential Study insight surface. |
| `AI-FILE-003` | `NOT_STARTED` | `2026-07-01` | `apps/web-student/src/modules/practice/` | Potential code explanation/debug hint surface. |

## Related Worklogs

| ID | Status | Updated | Link | Note |
|---|---|---|---|---|
| `AI-WL-001` | `DONE` | `2026-07-02` | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | Created canonical API DD draft package for this module group. |

## Verification Evidence

| ID | Status | Updated | Link | Evidence |
|---|---|---|---|---|
| `AI-EV-001` | `VERIFIED` | `2026-07-02` | `.agent/worklog/2026-07/0004_api_dd_canonical_drafts.md` | Documentation generation checks completed for canonical API DD drafts. |

## Next Work

| ID | Status | Updated | Link | Task |
|---|---|---|---|---|
| `AI-NEXT-001` | `NOT_STARTED` | `2026-07-02` | `docs/api-dd/ai/` | Review DD drafts and resolve OPEN_QUESTION items before coding. |
