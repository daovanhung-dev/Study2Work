# Verification Report — API #49 Lấy cây nội dung course

## Scope

Review source/API contract, implement route and module, add the legacy Content DDL artifact and migration, update catalog/AC-22/ERD/DD/context, run API and Study Server verification, and macro-review related DD #50–#53. No live database or deployment action was performed.

## Deliverable manifest

| Area | Files/evidence | Status |
|---|---|---|
| Runtime | `app/api/v1.py`, middleware allowlist, `mentor/api_49_mentor_content_list/` | PASS — route and view source-backed locally |
| API tests | `tests/modules/mentor/api_49_mentor_content_list/test_mentor_content_list.py` | PASS — 20 focused TestClient cases |
| Database artifacts | Legacy `DB.sql`, migration `006_contents.sql`, `DB_UNICA_TABLES.md`, `DB_UNICA_ERD.drawio` | PASS — checked-in artifact only; live schema not verified |
| Contract/workflow | API catalog #49 and AC-22 diagram | PASS — both show `ApiEnvelope<Content[]>` |
| API #49 DD | 8 sheets plus plan/open questions/verification report | PASS — current source and unresolved decisions separated |
| Context | server-study pages and `context-manifest.json` | PASS for API #49 entries; project validator has repository-level blockers below |
| Related DD #50–#53 | Base `contents` persistence notes updated | PASS_WITH_OPEN_QUESTIONS |

## Contract and source checks

| Check | Result | Status |
|---|---|---|
| Worklog preflight | Selector found 43 coding worklogs; #34/#47/#48 logs were read before source edits. | VERIFIED |
| Route/OpenAPI | API #49 appears in the router, design-code allowlist and signed-int64 OpenAPI schema. | VERIFIED_BY_FOCUSED_TESTS |
| Auth/access | Shared Mentor guard; direct `courses.mentor_id` check; owner mismatch → 403. | SOURCE_BACKED; assigned-course access remains out of scope/open |
| Content query | `contents`, `deleted_at IS NULL`, all status values, stable parent/order/id ordering. | SOURCE_BACKED |
| Response/error behavior | Flat `Content[]`; roots omit null `parent_id`; empty tree → 200 `[]`; malformed/out-of-range ID and missing course → 404; catalog error set retained. | VERIFIED_BY_FOCUSED_TESTS |
| Tree mapping | Duplicate ID, missing parent, wrong-course row and cycle fail safely with 500; no partial response. | VERIFIED_BY_FOCUSED_TESTS |
| DDL boundary | BIGINT legacy `contents` table and migration 006 are checked in; V1-PILOT UUID model remains separate. | VERIFIED_STATIC_ONLY; live schema/deployment unknown |
| AC-22/AC-33 macro review | #49–#53 reviewed; base fields and soft-delete marker are available in DDL; version history, status lifecycle/readiness and audit remain open. | VERIFIED_WITH_OPEN_QUESTIONS |

## Commands

| Command | Result | Status |
|---|---|---|
| `uv run pytest tests/modules/mentor/api_49_mentor_content_list/test_mentor_content_list.py -q` | 20 passed, 1 upstream Starlette/httpx deprecation warning. | PASS |
| `uv run pytest -q` | 356 passed, 1 upstream Starlette/httpx deprecation warning. | PASS |
| `uv run ruff check app tests` | All checks passed. | PASS |
| `git diff --check` | No whitespace errors at initial post-edit verification. | PASS |
| Drawio XML parse | `DB_UNICA_ERD.drawio` and `AC_03_MENTOR_TEACHING.drawio` parse; API #49 AC-22 output is `Content[]`. | PASS |
| `node scripts/validate-agent-context.mjs` | Fails on repository baseline: missing `.agents/db-admin` context/source, plus context drift in existing dirty scopes. | BLOCKED_BY_EXISTING_REPO_STATE |
| `node scripts/validate-agent-context.mjs --skip-drift` | Still fails on missing DB Admin context/source; no server-study structural error was reported. | BLOCKED_BY_EXISTING_REPO_STATE |

## Remaining boundaries

- Do not infer live DB availability or migration 006 deployment from checked-in SQL or fake-session tests.
- Confirm whether array response, direct-owner-only access, empty-array semantics and current error branches match product intent.
- `ContentType`/`ContentStatus` values, subtype payload schemas, version selection/history, publish readiness and soft-delete child policy remain open.
- API #50–#53 remain separate endpoints; their implementation status is not inferred from this API #49 work.
