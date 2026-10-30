# Verification Report — API #87 Lấy danh sách quiz

## Scope

- DD output: apps/study-server/docs/dd/87_admin_quizzes_list/.
- Task: implement one Study Server API and synchronize its Draft DD/context. No database schema, catalog or diagram was changed.
- DD status: Draft — Needs Confirmation.
- Application tests: RUN; the focused suite and full Study suite passed with fake DB sessions.

## Template

- Registered template pack: tám file trong .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template pack SHA-256: 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137.
- Tám sheet giữ nguyên appendix suffix theo template; không tạo ZIP theo server-study workflow.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | 11 Markdown files: 8 sheets + 3 reports | PASS — 11/11 |
| Template appendix parity | 8/8 appendix suffixes compared byte-for-byte | PASS — 8/8 |
| Catalog contract | Direct GET/path, query fields/types, `ApiEnvelope<Quiz>`, 200 and 401/403/500 retained; local 422/Page fallback called out | PASS by source comparison |
| Focused API #87 | `pytest -q tests/modules/admin/api_87_admin_quizzes_list/test_admin_quizzes_list.py` | PASS — 20 |
| Linked regression | #07/#78/#82/#86/#87 test files | PASS — 93 |
| Full Study suite | `.venv/bin/pytest -q` | PASS — 1113; one upstream Starlette/httpx deprecation warning |
| Ruff | `.venv/bin/ruff check app tests` | PASS |
| OpenAPI | Imported composition root and inspected schema | PASS — 51 `/api/v1` templates / 58 operations; #87 exposes 200/401/403/422/500 |
| DD markup | 11/11 expected files, 35 local links/anchors, JSON examples parse, fences/newlines valid | PASS |
| `git diff --check` | Repository diff whitespace check | PASS |
| Context validator | Deno full validation reports existing missing `db-admin` pages/source and baseline source drift; `--skip-drift` isolates the same unrelated `db-admin` graph/source errors. No API #87 source/test path is missing. | PARTIAL — unrelated baseline blocker |

## Findings and limits

- Catalog says ApiEnvelope<Quiz>, while AC-35 and page query imply list/pagination. DD preserves direct type and records ApiEnvelope<Page<Quiz>> as an unapproved proposal.
- Nested questions are in reusable Quiz, but AC-35 list flow only says “Query quizzes”; API #87 keeps a metadata-only projection. API #88 adds DERIVED local question type/order and Admin choice shape candidates, not catalog approval.
- Legacy BIGINT tables and V1-PILOT UUID assessment model differ. Live DB is not verified.
- Shared ADMIN guard and middleware path are wired locally; quiz-management permission remains unimplemented because no policy source exists.
- Runtime returns Page metadata with `questions=[]`; the direct catalog remains singleton Quiz. Empty questions mean child rows are not loaded by this list projection, not that the source Quiz has no questions. Page cardinality and metadata-only projection remain unapproved fallbacks.
- The DB-facing HTTP tests use fake sessions; they do not verify live SQL/schema, migrations or deployment.

## AC-35 macro-review #87–#91 — document-level

- Status: VERIFIED_WITH_OPEN_QUESTIONS. The document review is complete after DD #91 exists; it does not approve proposals or verify runtime.
- Shared lifecycle proposal, all DERIVED:
  - #90 soft-deletes a quiz when any attempt exists and retains questions, choices, attempts and answers.
  - #90 hard-deletes only when there are no attempts; child-first order and transaction/race handling remain unapproved.
  - #87 excludes tombstones by default; an explicit status filter may include them only after the tombstone value and filter behavior are approved.
  - #89 rejects updates to a tombstone and proposes refusing replacement when attempt/answer history exists; its request body and 422 trigger remain open.
  - #29 rejects creation of a new attempt after tombstone; #30–#31 may let a previously created in-progress attempt finish; #32 reads retained result history. In-flight behavior, authorization and error mapping remain open.
  - #91 reads aggregate history while the soft-deleted quiz row remains; a hard-deleted or absent quiz maps to the direct 404 contract.
- AC-35 contract gaps remain: #87 list/page cardinality, #88 nested create schema and DRAFT/open lifecycle, #89 update body/replacement semantics, #91 statistics response versus Quiz, shared QuizQuestion/QuizChoice schema and Admin permission.
- The quiz status value DELETED, lifecycle transitions, live schema, transaction/concurrency policy, aggregate metrics/rounding and error integration require owner/source confirmation.
- API #87 runtime was not changed by API #88. API #88 adds migration 013/bootstrap/DB-diagram candidates; live schema and migration deployment remain unverified.
