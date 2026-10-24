# Verification Report — API #89 Cập nhật quiz

## Scope

- DD output: apps/study-server/docs/dd/89_admin_quizzes_update/.
- Task: một API Markdown DD; không sửa runtime, schema, catalog, diagram hoặc context pages.
- DD status: Draft — Needs Confirmation.
- Application tests: NOT_RUN — docs-only; API #89 không có route/module.

## Template

- Registered template pack: tám file trong .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template pack SHA-256: 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137.
- Dùng bảy shared sheet templates và template table cho năm mapping sheets.
- Study workflow chỉ giao Markdown; không tạo ZIP.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | 15 Markdown files: 12 sheets + 3 reports | PASS |
| Template appendix parity | 12/12 sheet appendix suffixes match registered templates byte-for-byte | PASS |
| Catalog contract | Direct method/path/auth/response/status and exact five errors retained | PASS |
| DERIVED request example | Three JSON examples parse; request body and nested config/questions decode | PASS |
| Response/error examples | JSON examples parse and retain catalog business codes | PASS |
| Tables and fences | 46 tables / 592 rows have consistent widths; 4 fence pairs balanced | PASS |
| Relative links/anchors | 56 local links and 27 anchors resolve | PASS |
| Whitespace | Final newline and trailing whitespace check clean after removing extra blank line | PASS |
| Source inventory | No API #89 route/module/test marker found under app/tests; endpoint remains UNWIRED | PASS |
| Runtime behavior | Application tests not run | NOT_RUN |

- Package fingerprint (12 sheets + PLAN_RESULT + OPEN_QUESTIONS): `e01159b0e27df6ad1ee4d3986e1e1a55022cba9619360df560734c00ddff62f7`.

## Findings and limits

- Catalog body is path-only; config/questions and full replacement remain unapproved DERIVED proposals.
- Attempt/answer history references child IDs; history guard and concurrency strategy require owner review.
- Legacy QuestionType/QuizChoice/order gaps prevent a fully source-backed Quiz projection.
- Legacy BIGINT and V1-PILOT UUID models are incompatible; live schema was not verified.
- At authoring time macro-review was pending. The current document-level review is recorded below as `VERIFIED_WITH_OPEN_QUESTIONS`.

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
