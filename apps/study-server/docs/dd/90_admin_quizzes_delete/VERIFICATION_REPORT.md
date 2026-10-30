# Verification Report — API #90 Xóa quiz

## Scope

- DD output: `apps/study-server/docs/dd/90_admin_quizzes_delete/`.
- Task: wire một API theo catalog/AC-35, cập nhật DD và Study context; không sửa schema, catalog hoặc diagram.
- DD status: `Draft — Needs Confirmation`.
- Application tests: 18 focused; 100 linked #86–#90; full Study suite 1178 passed.
- OpenAPI: 52 unique `/api/v1` path templates / 61 operations; API #90 DELETE shares API #89's path template.

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
| Tables/fences | 34 tables / 410 data rows have consistent widths; 4 code-fence pairs balanced | PASS |
| Relative links/anchors | 39 local links and all in-package anchors resolve | PASS |
| Whitespace | Final newlines present; no trailing whitespace | PASS |
| Source inventory | API #90 route/module/test marker exists under app/tests and imports through the FastAPI router | PASS |
| Runtime source | Route/module/test exist locally; raw path, ADMIN auth, transaction and catalog response are wired | PASS |
| Runtime behavior | Focused/linked/full HTTP tests use fake DB sessions; live PostgreSQL/deployment not verified | PASS_WITH_LIMITS |

- Template manifest fingerprint (SHA-256 over sorted `filename digest` lines for the seven shared sheets and the table template): `6db317d91d0c072ff46e2086221a9534116d28006ae17afc268c31fae31ab5d4`.
- Output manifest fingerprint (same formula over 11 sheets, `OPEN_QUESTIONS.md` and `PLAN_RESULT.md`): `899df2f7d4940120f65efec2ec4c5c3e15b6a50a97a80aa0795df102afb129a5`.

## Findings and limits

- AC-35 directly specifies soft-delete intent when attempts exist. Runtime applies that branch and retains history; the `DELETED` value/timestamp mapping remain DERIVED.
- Runtime also treats linked answer rows without an attempt row as history to protect references; this integrity safeguard is DERIVED.
- Runtime hard-deletes choices → questions → Quiz when no attempt/answer history exists. This no-history branch and child-first order remain DERIVED proposals.
- No live schema verification; legacy and V1-PILOT models are distinct.
- API #29's create-attempt status/locking policy remains unresolved; API #90's own row locks do not establish cross-API race safety.

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
- No catalog, diagram, database schema or migration was changed. API #90 source and HTTP tests now exist locally; fake-session tests do not establish live database behavior or deployment.
