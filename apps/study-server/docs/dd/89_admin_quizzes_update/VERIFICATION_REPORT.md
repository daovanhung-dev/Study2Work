# Verification Report — API #89 Cập nhật quiz

## Scope

- DD package: `apps/study-server/docs/dd/89_admin_quizzes_update/` — 12 sheets and 3 reports.
- Implementation scope: API #89 runtime route/module, focused tests, DD and server-study context. No schema, migration, catalog or diagram change.
- DD status: Draft — Needs Confirmation. The implementation choices below remain DERIVED and are not owner-approved.

## Runtime verification

| Check | Result | Status |
|---|---|---|
| Focused API #89 HTTP tests | 26 passed | PASS |
| Linked API #87–#89 quiz regression | 67 passed | PASS |
| Full Study Server suite | 1160 passed; one upstream Starlette/httpx TestClient deprecation warning | PASS |
| Ruff | `ruff check app tests` passed | PASS |
| OpenAPI | 52 `/api/v1` path templates / 60 operations; API #89 exposes 200, 401, 403, 404, 422, 500 | PASS |
| API #89 route/module/test source | Wired locally in `app/api/v1.py`; shared error middleware recognizes the dynamic path; module and HTTP tests exist | PASS |

The tests use fake database sessions. They verify application orchestration and rollback behavior, not PostgreSQL row-lock/FK semantics, deployed schema, migration application, grants or production deployment.

## DD package checks

| Check | Result | Status |
|---|---|---|
| Expected package | 15 Markdown files: 12 sheets + 3 reports | PASS |
| Template appendix parity | All 12 sheet appendix tails match the registered templates byte-for-byte | PASS |
| Catalog contract | Direct method/path/auth/response/status and five catalog error branches retained | PASS |
| JSON examples | 3 fenced JSON examples parse | PASS |
| Tables and fences | 47 tables / 509 data rows have consistent widths; all fenced blocks are balanced | PASS |
| Relative links and anchors | 59 local links resolve; all package-local anchors resolve | PASS |
| Whitespace | No trailing whitespace; all files end with a newline | PASS |
| Package fingerprint | SHA-256 over 12 sheets + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md`, using `path + NUL + bytes + NUL`: `9095d00bfda986b86bf12d7741ce51928f7c3922873c658ca548cc847b8af4e6` | RECORDED |

## Findings and limits

- The direct catalog specifies only the `quiz_id` path; the `{config, questions}` body and full replacement behavior reuse API #88 as DERIVED proposals.
- The attempt/answer history rejection, tombstone behavior, target-course check, course move and lock order are local DERIVED choices that need owner review.
- Legacy BIGINT Quiz tables and V1-PILOT UUID assessment tables are incompatible models. Checked-in DDL/migration and fake-session tests do not establish live schema or deployment.
- Shared `ADMIN` role is enforced before raw input parsing; AC-35's separate quiz-management permission has no source-backed policy.
- DD status remains Draft — Needs Confirmation.

## AC-35 macro-review #87–#91 — document-level

- Status: `VERIFIED_WITH_OPEN_QUESTIONS`. This review covers the linked DDs after #91 exists; it does not approve proposals or verify production runtime.
- Shared lifecycle proposal, all DERIVED:
  - #90 soft-deletes a quiz when any attempt exists and retains questions, choices, attempts and answers.
  - #90 hard-deletes only when there are no attempts; child-first order and transaction/race handling remain unapproved.
  - #87 excludes tombstones by default; an explicit status filter may include them only after the tombstone value and filter behavior are approved.
  - #89 rejects updates to a tombstone and refuses replacement when attempt/answer history exists; request body and 422 trigger remain open.
  - #29 rejects creation of a new attempt after tombstone; #30–#31 may let a previously created in-progress attempt finish; #32 reads retained result history. In-flight behavior, authorization and error mapping remain open.
  - #91 reads aggregate history while the soft-deleted quiz row remains; a hard-deleted or absent quiz maps to the direct 404 contract.
- AC-35 contract gaps remain: #87 list/page cardinality, #88 nested create schema and DRAFT/open lifecycle, #89 update body/replacement semantics, #91 statistics response versus Quiz, shared QuizQuestion/QuizChoice schema and Admin permission.
- Quiz status values, lifecycle transitions, live schema, transaction/concurrency policy, aggregate metrics/rounding and error integration still need owner/source confirmation.
