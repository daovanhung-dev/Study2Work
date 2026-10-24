# Verification Report — API #87 Lấy danh sách quiz

## Scope

- DD output: apps/study-server/docs/dd/87_admin_quizzes_list/.
- Task: one API Markdown DD; không sửa runtime, schema, catalog, diagram hoặc context pages.
- DD status: Draft — Needs Confirmation.
- Application tests: NOT_RUN — docs-only; API #87 không có route.

## Template

- Registered template pack: tám file trong .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template pack SHA-256: 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137.
- Tám sheet giữ nguyên appendix suffix theo template; không tạo ZIP theo server-study workflow.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | 11 Markdown files: 8 sheets + 3 reports | PASS — 11/11 |
| Template appendix parity | 8/8 appendix suffixes compared byte-for-byte | PASS — 8/8 |
| Catalog contract | GET/path, query fields/types, ApiEnvelope<Quiz>, 200 and exact 401/403/500 codes retained | PASS |
| JSON examples | Parsed all four code blocks labeled json | PASS — 4/4 |
| Tables and fences | 450 Markdown table lines have consistent columns; all five code fences are balanced | PASS |
| Relative links/anchors | Resolved 32 local links, including 15 anchor links | PASS |
| Whitespace | Final newline/trailing whitespace checked across all 11 untracked DD files; `git diff --check` checked tracked inventory edit | PASS |
| Source inventory | No API #87 route/path/ID marker or matching module/test found under Study app/tests | UNWIRED / NOT_FOUND |
| Runtime behavior | Application tests not run | NOT_RUN |

## Findings and limits

- Catalog says ApiEnvelope<Quiz>, while AC-35 and page query imply list/pagination. DD preserves direct type and records ApiEnvelope<Page<Quiz>> as an unapproved proposal.
- Nested questions are in reusable Quiz, but AC-35 diagram only says “Query quizzes”; QuestionType and QuizChoice are unresolved.
- Legacy BIGINT tables and V1-PILOT UUID assessment model differ. Live DB is not verified.
- Admin guard is absent; middleware path is not allowlisted. No API #87 runtime behavior is claimed.
- At authoring time macro-review was pending. The current document-level review is recorded below as `VERIFIED_WITH_OPEN_QUESTIONS`.
- Static package fingerprint (8 sheets + PLAN_RESULT.md + OPEN_QUESTIONS.md; verification report excluded): `09867b62e5ad28779c76aa202a38e22c105dd9d1fbad62740d6aeb1b3067efa1`.
- Application tests were not run; these checks validate Markdown structure and contract traceability only.

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
- No catalog, diagram, database schema or runtime source was changed; no application tests were run.
