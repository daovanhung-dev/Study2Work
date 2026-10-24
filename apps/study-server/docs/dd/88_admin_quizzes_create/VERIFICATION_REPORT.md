# Verification Report — API #88 Tạo quiz mới

## Scope

- DD output: apps/study-server/docs/dd/88_admin_quizzes_create/.
- Task: one API Markdown DD; không sửa runtime, schema, catalog, diagram hoặc context pages.
- DD status: Draft — Needs Confirmation.
- Application tests: NOT_RUN — docs-only; API #88 không có route.

## Template

- Registered template pack: tám file trong .agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/.
- Template pack SHA-256: 3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137.
- Dùng bảy shared sheet templates và template table cho ba mapping files.
- Study workflow chỉ giao Markdown; không tạo ZIP.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | 13 Markdown files: 10 sheets + 3 reports; exact manifest | PASS — 13/13 |
| Template appendix parity | 7 shared sheet tails + 3 table tails compared byte-for-byte | PASS — 10/10 |
| Catalog contract | Direct method/path/body/response/status and exact errors retained | PASS — static comparison |
| Outer/embedded JSON | Parse all fenced JSON examples; decode config/questions strings | PASS — 4 blocks; both nested values parsed |
| Tables and fences | Validate all table widths and balanced fences | PASS — 45 tables / 544 rows; 4 fence pairs |
| Relative links/anchors | Resolve every local link and anchor | PASS — 39 links / 19 anchors |
| Whitespace | Final newline, trailing whitespace and diff check | PASS — no whitespace findings |
| Source inventory | Router/module/test scan for API #88 | PASS — no source marker found |
| Runtime behavior | Application tests not run | NOT_RUN |

- Static package fingerprint (10 sheets + PLAN_RESULT.md + OPEN_QUESTIONS.md; verification report excluded): `c968202b7c1ecdbc658a83dc1ec5e3a85c2cbe6f268f9c907f3c2fc434803814`.

## Findings and limits

- Direct catalog uses two strings; nested JSON is an unapproved DERIVED proposal.
- Legacy BIGINT quiz_questions has no QuestionType column; V1-PILOT QuestionType belongs to UUID assessment relations.
- QuizChoice shape, choice order, answer validation and correct-answer exposure remain unresolved.
- Atomic three-table write and course-not-found 422 are DERIVED proposals, not runtime facts.
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
