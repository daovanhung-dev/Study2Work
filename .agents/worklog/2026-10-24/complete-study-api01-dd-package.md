---
task_id: "2026-10-24-complete-study-api01-dd-package"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Hoàn thiện package DD Study API #01 — Tạo tài khoản mới

## CLASSIFICATION

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [server-study]
cross_scope_dependencies: []
```

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api100-dd.md`
    - carry_forward: Một API mỗi phiên; plan trước khi authoring; dùng AC diagram và source hiện hành; macro-review nhóm liên kết; Study output Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api101-dd.md`
    - carry_forward: Tách expected/current behavior, giữ discrepancy và `SOURCE_REQUIRED`; chỉ dùng route + matching module làm source-wired evidence, không suy runtime từ DD.
  - path: `.agents/worklog/2026-10-24/create-study-api102-dd.md`
    - carry_forward: Giữ contract canonical riêng với source implementation; report tiếng Việt; ghi rõ DB/diagram candidate không chứng minh live schema.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện package API #01 trong phiên riêng, giữ nội dung Vietnamese/source-aware, plan trước report authoring, đọc AC-01 và source liên quan, kiểm tra package ngay sau cập nhật.
- Deliverable basis: API #01 `POST /api/v1/auth/register` trong `docs/lists/list_api.md`, existing 8-sheet DD, AC-01, DB ERD/table guide, registered `createDD-markdown`, Study Markdown-only workflow.
- Direct contract: Public/no Bearer; body `email:email!`, `password:string!`, `full_name:string!`; `ApiEnvelope<UserProfile>`; HTTP 201 `DESIGN_RESOURCE_CREATED`; exact errors 422 `DESIGN_VALIDATION_ERROR`, 409 `DESIGN_STATE_CONFLICT`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-01 intended flow: validate input → check duplicate email → hash password/default STUDENT → create user and default profile transaction → call API #02 verification dispatch → provider sends email; post-accept provider failure is logged/retried without duplicate account.

## CURRENT_BEHAVIOR

- Source route: `app/api/v1.py` declares public POST `/auth/register`, HTTP 201, `RegisterRequest`, DB dependency, trace ID, and delegates to `create_user`.
- Module: validator trims/validates email with max length 255, rejects whitespace-only password, trims `full_name` and requires length 1–150. Password is hashed with Argon2id. Duplicate precheck reads `users.id`; INSERT writes user fields, defaults role to STUDENT, relies on DB default for status, sets avatar/phone NULL and timestamps with CURRENT_TIMESTAMP, then returns safe profile fields and commits.
- Error/transaction source: validation 422; duplicate and named unique-race constraint `users_email_key` return 409; failed/empty insert and database exceptions rollback and return 500. Success returns the canonical envelope without password/hash.
- Verification side effect: after commit the current #01 handler only logs `verification_dispatch_pending`; it does not invoke API #02, a provider, or a retry mechanism. API #02 calls its provider synchronously; provider exceptions return 500 with no retry worker, and the default stub accepts without sending email.
- Data source: `infra/postgres/study-server/DB.sql` is a BIGSERIAL `users` candidate matching current SQL; DB ERD has no profile table and no `bio` column. V1-PILOT identity/profile schema is a separate model; no live database metadata was checked.
- Tests: API #01 test source covers validation, success, duplicate/race, rollback, response safety, and path; tests were read but will not be run in this docs-only task.

## SOURCE_TRACE

```text
POST /api/v1/auth/register -> RegisterRequest/FastAPI type validation -> create_user -> validate_register_request -> SELECT users.id by normalized email -> Argon2id hash -> INSERT users -> commit/rollback -> log verification_dispatch_pending -> success/error ApiEnvelope -> API #01 tests (source reviewed; not run in this docs task)
```

## PLAN BEFORE REPORT AUTHORING

1. Preserve API #01 catalog contract and AC-01 as expected behavior; do not rewrite response/error codes, add fields, or treat source behavior as the approved contract.
2. Add `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, and `VERIFICATION_REPORT.md` in the existing API #01 folder. Record the registration/verification gap, default-profile versus users-only model, optional `bio` response gap, validation policy boundary, duplicate constraint/live-schema boundary, and no-runtime-test scope.
3. Keep API #01 expected post-create verification dispatch from AC-01 distinct from current implementation, which only logs a pending marker. Review existing API #02 DD and current route/view/provider for the connected AC-01 boundary; record that #02 exception behavior and retry differ from the diagram/DD, then hand #02 package/report updates to that API's own one-DD session.
4. Repair the two broken source links in `02_Overview.md`; remove leading/trailing whitespace in `05_Data_Mapping.md`; replace only outdated template appendix tails in `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, and `07_users_insert.md` with the corresponding registered template tails. Keep DD logic/body unchanged.
5. Do not modify runtime, tests, DB, catalog, AC diagram, or client; no ZIP is required by server-study workflow.
6. Validate 11-file package, front matter, all 8 appendix tails, contract/error set, JSON, local links/anchors, table widths, fences, whitespace/newlines, and fingerprints. Run `git diff --check`; do not run application tests.
7. Recount all API folders, core sheets, complete packages, and route+matching-view source pairs; append a new snapshot to the inventory worklog. Preserve prior worktree changes.

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #01 implementation | Current route and module exist; tests source exists. | `SOURCE_PRESENT / RUNTIME_NOT_RUN_THIS_TASK` | Current source is documented separately from approved contract. |
| AC-01 verification dispatch | Diagram calls API #02 after account creation; current #01 logs a pending marker only; #02 invokes provider synchronously, returns 500 on exception, has no retry worker, and defaults to a non-sending stub. | `DISCREPANCY` | End-to-end verification email/retry is not demonstrated by current code. |
| Default profile | AC-01 says user + default profile; ERD and runtime query map only `users`. | `DISCREPANCY / SOURCE_REQUIRED` | Do not invent a profile table or claim profile transaction. |
| UserProfile.bio | Catalog includes optional `bio`; ERD/current #01 INSERT/RETURNING do not include it. | `DISCREPANCY` | Keep field mapping unresolved; do not fabricate a value/column. |
| Email/user schema | Legacy Study DDL has BIGSERIAL users and unique email; V1-PILOT has a separate UUID identity/profile design; live metadata not inspected. | `SOURCE_REQUIRED / MODEL_DISCREPANCY` | Physical mapping/deployment cannot be concluded. |
| Validation contract | Catalog leaves min/max/policy unspecified; code currently applies email <=255, name 1–150, and nonblank password. | `DIRECT / CURRENT_SOURCE / OPEN_POLICY` | Do not elevate all runtime limits into approved business policy without owner confirmation. |

## CHANGES

- Files changed: API #01 `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; repaired links/whitespace/template appendix tails in existing API #01 sheets; this worklog and inventory worklog. No runtime/tests/schema/catalog/diagram/client/context changes.
- CONTEXT_UPDATES: None planned; no registered context/source contract changes.
- Context pages changed: None.
- Assumptions: Existing AC-01 flow remains expected behavior; current #01/#02 implementation mismatch remains explicit and unresolved.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Context and preflight | Root router, context map, worklog README/template, server-study entry/index/workflow and relevant pages read; selector logs #100/#101/#102 read. | VERIFIED_STATIC_ONLY |
| Skill registry | Manifest wires `createDD-markdown` and `docs-dd`; Study workflow requires Markdown folder and reports, no new ZIP. | VERIFIED_STATIC_ONLY |
| AC-01 | Diagram page `AC01` and index reviewed; direct register-to-verify flow and provider retry note recorded. | VERIFIED_STATIC_ONLY |
| Existing DD/source | API #01 eight sheets, API #02 connected DD, current route/module/provider/tests and DB candidates reviewed. | VERIFIED_STATIC_ONLY |
| Authoring | Three reports added; two broken source links, one whitespace issue and four template tails repaired. | VERIFIED_STATIC_ONLY |

## HANDOFF

- Remaining blockers: Contract owner confirmation for exact password policy, email normalization/uniqueness semantics, optional verification enablement and API #02 dispatch ownership, default-profile persistence, and `UserProfile.bio` mapping.
- Next action: In the next one-DD session, complete API #02 package and revisit the AC-01 dispatch boundary. Keep all contract/source questions open until approved.

## POSTFLIGHT — API #01 package completion — 2026-10-24

- API #01 now has 11 Markdown files: 8 existing sheets + `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`. This session did not create a second API DD.
- Static verification: 8/8 template appendix suffixes; 3 JSON examples parse; 426 Markdown table rows have consistent width; 36 local links/anchors resolve; fences/newlines/whitespace pass; output fingerprint `6a7839acb858aa0a4ed36bd2a7724e699e7575f01d180d917fdf43bebad9d7d4`; `git diff --check` passes.
- AC-01 group review found #01 does not invoke #02. #02 current view invokes the provider synchronously, maps provider exception to HTTP 500, has no retry worker, and the default stub does not send email. The AC-01 design remains expected behavior; #02 package review is handed to its own next session.
- Inventory after #01: 103/103 catalog IDs have folders and core sheets; 92 have the full 11-file package; #02–#12 remain core-only. Current route + matching-view source pair: 12 API IDs (#01–#09, #12–#14); 91 have no pair. Source count does not establish runtime verification.
- Test sources were inspected but no application tests were run; no runtime/deployment claim is made.
