# Verification Report — API #51 Cập nhật nội dung Mentor

## Historical DD review

The initial DD-only report was written before API #49–#51 implementation and remains as design history in Git. Its statements that API #51 had no route/module and that version persistence was entirely SOURCE_REQUIRED are superseded by the current local source and migration 007. They remain unapproved DERIVED fallback, not canonical contract.

## Current implementation verification (2026-10-25)

| Check | Result | Evidence/status |
|---|---|---|
| Source order | Diagrams → legacy infra → API catalog → simplest fallback | AC-22/AC-33, migrations 006/007, API catalog row #51. |
| Template | Eight-file Markdown template opened from registered `DD_API_Template_MD` resource | `.agents/context-manifest.json`; template source retained. |
| Request | Strict required `content_type`, `title`, object `payload`; extra fields rejected | `DERIVED` from API #50; catalog still omits body. |
| Route | PUT composed in `app/api/v1.py`, HTTP 200, int64 OpenAPI path, shared Content response | Current source + focused route test. |
| Authorization | Shared Mentor JWT guard; locked direct `courses.mentor_id` check | Current source; direct-owner boundary derived from #49. |
| Mutation | Snapshot prior Content into `content_versions`; update current `contents`; single commit/rollback boundary | Current source and migration 007; live schema not verified. |
| Middleware | Parameterized API #51 path included in `DESIGN_CONTRACT_PATHS` | Current source; body errors produce 422 `DESIGN_VALIDATION_ERROR`. |
| Error set | 401/403/404/422/500 only | Catalog parity; no 409 added. |
| Focused tests | 23 passed | `uv run pytest -q tests/modules/mentor/api_51_mentor_content_update`; fake DB only. |
| Adjacent Content APIs | 68 passed | API #49/#50/#51 focused suites; fake DB. |
| Full Study suite | 404 passed | `uv run pytest -q` in the Study Server environment. |
| Ruff | Check and format pass | API #51 module/tests, router and middleware; 8 files already formatted. |
| Mypy | API #51 module pass | `--follow-imports=silent`; broader target run reports two existing errors in unrelated course catalog/auth files. |
| Context validator | Repository baseline invalid | Node command unavailable; Deno validator reports missing DB Admin paths and broad existing source snapshot drift; `--skip-drift` leaves DB Admin only. |
| Cross-API behavior | #52 publish, AC-33 approval, public published-version selection, original author remain open | No integration claim. |
| Live schema/deployment | Not probed | Migration/DDL source is not live evidence. |

## Remaining review boundary

- Body fields, full-replacement semantics, history schema and `PENDING_REVIEW` transition are DERIVED and require contract-owner confirmation.
- `archived_by` records who superseded the prior state; it does not satisfy original-author provenance in AC-33.
- Prior published content is retained as a snapshot, but current `contents` is set to `PENDING_REVIEW`; public serving behavior is unresolved.
- API #52 and #53 remain separate DDs and were not changed in this API #51 implementation.
