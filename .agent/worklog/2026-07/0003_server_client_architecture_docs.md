# Worklog - 0003 server_client_architecture_docs

| Field | Value |
|---|---|
| Session | `0003` |
| Time | `2026-07-02 Asia/Saigon` |
| Module | `GLOBAL_ARCHITECTURE` |
| Feature/function | Server/client architecture documentation refactor |
| Status | `DONE` |

## Goal

Refactor project architecture context into a clear Study-only Server/Client split and replace stale architecture documents that pointed at removed or superseded structures.

## Context Read

- BD: `docs/BD/Study2Work_Study_BD_Codex_Ready.md`
- DD: no approved business API DD; no business API implementation in this session
- Checklist: `docs/checklists/API.md`, module checklists
- Architecture: `.codex/PROJECT_CONTEXT.md`, `.codex/BACKEND_ARCHITECTURE.md`, existing `docs/architecture/`

## Files Created Or Modified

| Path | Action | Note |
|---|---|---|
| `docs/architecture/PROJECT_ARCHITECTURE.md` | created | Canonical Server/Client split, ownership map, Study modules and references. |
| `docs/architecture/SERVER_ARCHITECTURE.md` | created | Canonical FastAPI server architecture, API flow, envelope, persistence, migration and worker rules. |
| `docs/architecture/CLIENT_ARCHITECTURE.md` | created | Canonical web/mobile client responsibilities and target skeleton structure. |
| `docs/architecture/RUNTIME_FLOWS.md` | created | Synchronous API, mutation, async worker, migration and error/trace flows. |
| `docs/architecture/Kien_truc_du_an_Study2Work_tree.md` | replaced | Clean canonical tree summary, superseding stale broad tree. |
| `docs/architecture/Study2Work_UI_Screen_List_By_Module.md` | replaced | Study-only UI screen map. |
| `docs/architecture/Study2Work_Domain_Model_Coding_Practice.md` | replaced | Study-only bounded-context summary. |
| `docs/architecture/Study2Work_BusinessCode_Debug.md` | replaced | Study-only business code/debug convention. |
| `docs/architecture/De_an_he_thong_dao_tao_it_thuc_chien.md` | replaced | Study product architecture brief. |
| `docs/architecture/BACKEND_ARCHITECTURE_USAGE_VI.md` | replaced | Superseded pointer to canonical server architecture. |
| `README.md` | replaced | Root server/client overview and architecture entry points. |
| `.agent/AGENT_GUIDE.md` | modified | Runtime split and architecture read order. |
| `.agent/context/CONTEXT_INDEX.md` | modified | Architecture docs added to global sources and task map. |
| `.codex/PROJECT_CONTEXT.md` | modified | Server/client split and client state documented. |
| `.codex/BACKEND_ARCHITECTURE.md` | modified | Points to canonical server architecture. |
| `docs/checklists/API.md` | modified | Added architecture reference. |
| `docs/checklists/ADMIN.md` | modified | Corrected canonical server/client paths. |
| `docs/checklists/ASSESSMENT.md` | modified | Corrected canonical assessment path. |
| `docs/checklists/COMMUNITY.md` | modified | Corrected canonical community path. |
| `docs/checklists/README.md` | modified | Added architecture entry point and generic removed-scope guard. |

## Logic Changed

- No runtime logic changed.
- No business API or client feature was implemented.
- Architecture docs now define exactly two runtime sides: Server (`services/api`) and Client (`apps/*`).
- Stale architecture documents were replaced with clean Study-only documentation and no longer recommend superseded server paths or removed workflows.

## Tests Run

| Command/check | Result | Evidence |
|---|---|---|
| `uv run ruff check .` | PASS | `All checks passed!` |
| `uv run ruff format --check .` | PASS | `69 files already formatted` |
| `uv run mypy app` | PASS | `Success: no issues found in 66 source files` |
| `uv run pytest` | PASS | `4 passed`; one Starlette/httpx deprecation warning remains from dependency stack. |
| `docker compose config` | PASS | Compose resolved API, PostgreSQL and Redis services. |
| `git diff --check` | PASS | No whitespace errors; Git reported line-ending conversion warnings only. |
| Stale architecture/context scan | PASS | No stale removed-scope or superseded server-path matches in architecture/context/checklist docs. |
| Mojibake scan | PASS | No mojibake marker, replacement character or NUL matches in updated architecture/context/checklist docs. |

## Bugs Found

| ID | Status | Description | Link |
|---|---|---|---|
| `BUG-0003-001` | `FIXED` | Root `README.md` contained NUL/mojibake text and was replaced with a clean architecture entry point. | `README.md` |
| `BUG-0003-002` | `FIXED` | Legacy architecture documents described superseded server paths and removed workflows. | `docs/architecture/` |
| `BUG-0003-003` | `FIXED` | Module checklists still referenced superseded server paths for ADMIN, COMMUNITY and assessment practice. | `docs/checklists/` |

## Risks Or Unverified Points

- Client apps remain skeletons and are not runnable by design for this pass.
- Backend tests still report the existing Starlette/httpx deprecation warning.
- External architecture references were recorded as URLs in docs; no dependency upgrades were performed.

## Next Work

- Create approved API DDs for the first implementation slice before coding business APIs.
- In a separate client implementation pass, decide whether to create runnable Vue/Vite and Flutter skeletons.

## Suggested Commit Message

`docs(architecture): define study server client split`
