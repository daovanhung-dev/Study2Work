# Verification Report — API #90 Xóa quiz

## Scope

- DD output: `apps/study-server/docs/dd/90_admin_quizzes_delete/`.
- Task: một API Markdown DD; không sửa runtime, schema, catalog, diagram hoặc context pages.
- DD status: `Draft — Needs Confirmation`.
- Application tests: `NOT_RUN` — docs-only; API #90 không có route/module/test.

## Template

- Registered resource: tám file trong `.agents/skills/create_dd_api/docs/dd/DD_API_Template_MD/`.
- Used sheets: bảy shared templates và `07_table.md` lặp cho bốn mutation mapping sheets.
- Study workflow: Markdown-only; không tạo ZIP.

## Static checks

| Check | Result | Status |
|---|---|---|
| Expected package | 14 Markdown files: 11 sheets + 3 reports | PASS |
| Template appendix parity | 11/11 appendix suffixes match registered templates byte-for-byte | PASS |
| Catalog contract | Direct method/path/auth/response/status and exact five errors retained | PASS |
| AC-35/AC-16 trace | Full AC-35 #90 branch and AC-16 attempt/history references recorded | PASS |
| JSON examples | 2/2 success and 404 error envelopes parse and preserve direct schema/codes | PASS |
| Mutation mapping | Soft update and 3 ordered no-attempt deletes cross-reference Data Mapping | PASS |
| Tables/fences | 34 tables / 407 rows have consistent widths; 4 code-fence pairs balanced | PASS |
| Relative links/anchors | 37 local links and 12 anchors resolve | PASS |
| Whitespace | Final newlines present; no trailing whitespace | PASS |
| Source inventory | No API #90 route/module/test marker found under app/tests; endpoint remains UNWIRED | PASS |
| Runtime behavior | Application tests not run | NOT_RUN |

- Template manifest fingerprint (SHA-256 over sorted filenames and per-file SHA-256 digests): `3f033d853d64ce417542903e53a10f741b0a0a9b5187d04beb038c99866f2bb6`.
- Output manifest fingerprint (11 sheets + PLAN_RESULT + OPEN_QUESTIONS; same manifest formula): `9254b0a3f946a2d376b4130e87d994c9af8d7817fe24c4d10659175726c560ec`.

## Findings and limits

- AC-35 directly specifies soft-delete intent when attempts exist. Physical tombstone fields/value are unresolved.
- Hard delete when there are no attempts and child-first order are DERIVED proposals.
- No live schema verification; legacy and V1-PILOT models are distinct.
- AC-35 macro-review #87–#91 remains pending until API #91 DD exists.

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
