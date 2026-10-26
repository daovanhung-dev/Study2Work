---
task_id: "2026-10-25-implement-api60-mentor-support-reply"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #60 Mentor support reply

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run -A scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 53 matching worklogs; selected and read all three; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: API #34 persists numeric UploadAsset IDs in legacy `uploads`; Mentor uploads use `LECTURE`; owner/purpose/course/status checks are source-backed locally; live DB and Object Storage remain unverified.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: API #47 accepts `asset_refs` as a JSON string containing an ordered unique int64 array, including `[]`; it resolves assets by Mentor, course and `LECTURE`; transaction writes ordered asset links atomically.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Use direct `courses.mentor_id` authorization, SQL-only query constants, safe catalog errors, transaction ownership, and preserve unrelated worktree changes.
- related_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api58.md`
    - carry_forward: User-directed local fallback adds BIGINT `support_requests`, `support_messages`, `support_message_uploads`; direct course owner and scoped UploadAsset projection are local choices, not live schema proof.
  - path: `.agents/worklog/2026-10-25/implement-api59-mentor-support-request-detail.md`
    - carry_forward: API #59 reads the same schema, returns the full chronological thread, maps other-owner to 403, malformed int64 path to 404, and reuses API #58 response models; tests use fake DB data.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Catalog/diagram: `POST /api/v1/mentor/support/{request_id}/reply`; Bearer JWT role Mentor; `request_id:int64!`; required `message:string!` and `attachment refs:string!`; HTTP 200 `DESIGN_RESOURCE_UPDATED`; `ApiEnvelope<SupportRequest>`; exact errors 401/403/404/422/500 and their catalog business codes.
- AC-24: #60 inserts a reply, does not resolve/change request status, and returns SupportRequest including the new message. #61 owns the later resolve branch.
- The DD is `Draft — Needs Confirmation`; source conflicts use diagram → checked-in infrastructure → catalog, then a documented DERIVED fallback under the user's overall task rule.

## CURRENT_BEHAVIOR

- API #60 route/module/tests are absent. `DESIGN_CONTRACT_PATHS` does not include the reply route.
- API #58/#59 current local source uses BIGINT `support_requests`, `support_messages`, `support_message_uploads`, numeric users, direct `courses.mentor_id`, and API #34 upload metadata. Migration 008 is checked-in source only.
- API #47 current source accepts ordered unique int64 IDs encoded as a JSON array string. API #60 DD's older proposal says comma-separated IDs; no catalog or diagram fixes the encoding.
- Shared DB helpers execute SQL without commit. Write APIs #47/#50–#53/#56–#57 own commit/rollback and validate projections before commit.
- Existing worktree contains broad dirty API/DD/context/DDL work through #59; all unrelated changes must be preserved.

## SOURCE_TRACE

```text
POST /api/v1/mentor/support/{request_id}/reply
  -> shared MENTOR guard
  -> strict int64 path + body validation
  -> lock request and check course owner
  -> resolve ordered UploadAsset refs by Mentor/course/LECTURE/UPLOADED
  -> INSERT support_messages; INSERT ordered support_message_uploads
  -> reload complete thread using the same detail projection as API #59
  -> validate SupportRequest envelope; commit once; return DESIGN_RESOURCE_UPDATED
  -> focused HTTP tests, full Study suite, OpenAPI and context checks
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Planned behavior |
|---|---|---|---|
| Physical support model | AC-24 says logical `INSERT SupportMessage`; API #58 migration 008 supplies matching local BIGINT tables; pilot UUID model is incompatible with int64 contract. | `RESOLVED_FOR_LOCAL_IMPLEMENTATION — DERIVED_FROM_API58` | Reuse checked-in legacy tables; add no migration; live schema remains unverified. |
| Ref encoding/wire key | Catalog says `attachment refs:string!`; DD proposes `attachment_refs` CSV; current API #47 source uses JSON array strings for ordered unique int64 upload IDs. | `DERIVED_FROM_CURRENT_LINKED_SOURCE` | Use `attachment_refs` containing a JSON array of int64 IDs; `[]` means none; update #60 DD only, not #35/#47. |
| Mentor scope/identity | Current #34/#46–#59 use numeric JWT `sub`; support request belongs to a course with direct `courses.mentor_id`. | `DERIVED_FROM_CURRENT_LOCAL_PATTERN` | Require shared MENTOR guard; author is `users.id = JWT sub`; authorize by direct course owner. |
| Missing/other owner | Catalog exposes 404 and 403; API #59 returns missing 404 and extant other-owner 403. | `DERIVED_FROM_API59` | Preserve 404 for missing and 403 for extant request outside owner scope. |
| Message validation | Catalog requires string but gives no blank/length policy; DD proposed whitespace-only rejection. | `DERIVED` | Reject empty/whitespace-only with 422; retain original text; add no length bound. |
| Attachment eligibility | API #34 creates Mentor `LECTURE` uploads scoped to course and `UPLOADED`; API #58/#59 link resolver uses the same policy. | `SOURCE_BACKED_LOCAL / DERIVED_FOR_SUPPORT` | Require every ref to resolve to current Mentor, request course, `LECTURE`, `UPLOADED`; generic 404 for missing/out-of-scope refs. |
| Request status | AC-24 gives status decision to #61 and does not specify post-resolve reply rejection. | `DERIVED` | Do not change status or add a status gate in #60; preserve current status. Keep post-resolve policy open. |
| Message visibility/order | Local schema has no internal flag; #59 returns every message ordered `created_at ASC, id ASC`. | `DERIVED_FROM_API59_SCHEMA` | Store in shared thread and return full ordered thread; no pagination or limit. |
| Path parse | #60 catalog includes 422; no path minimum is specified. | `DIRECT + SOURCE_PATTERN` | Malformed/overflow signed-int64 → 422; valid zero/negative values query normally and return 404 when absent. |
| Write/read transaction | Current DB helper leaves commit to caller; reply requires insert plus link rows and response hydration. | `DERIVED_FROM_CURRENT_DB_CONVENTION` | Lock request; insert message/links and rehydrate full response in one transaction; commit only after validated response. |
| Live schema/deployment | Only checked-in SQL/migration 008 is available. | `NOT_VERIFIED_HERE` | Do not apply migration or claim live/deployed behavior. |

## IMPLEMENTATION_PLAN

1. Read the root/context router, exact coding preflight worklogs, server-study pages, API #60 DD, AC-24 flow, DB source/migration, API catalog, and linked #34/#47/#58/#59/#61 sources. Record source precedence, dirty-tree boundary and requirement matrix before edits.
2. Reconcile #60 DD before runtime edits. Preserve direct catalog fields/status/error codes; record JSON-array `attachment_refs`, nonblank-only message validation, current #58 BIGINT model, direct course owner, full-thread rehydration and all remaining live/business-policy limitations as DERIVED.
3. Extract API #59's pure request/message projection mapper to a Mentor `_shared` module and make #59 use it. This lets #60 return the identical SupportRequest projection without calling another endpoint view or duplicating mapping logic; run #59 regression tests.
4. Add API #60 request/response models, signed-int64 and ordered unique JSON-array validators, SQL-only lock/upload/insert/link constants, and a view owning auth, queries, transaction, projection, safe errors and commit/rollback.
5. Add the thin route after the #58/#59 routes with raw path text and integer/int64 OpenAPI metadata; add its exact path template to `DESIGN_CONTRACT_PATHS` so framework 422 uses the design business code.
6. Add focused TestClient coverage for auth-before-DB, path/body errors, missing/other-owner requests, asset scope/missing/ordering, message/link persistence, full updated SupportRequest, trace, no status mutation and DB/link/projection/commit rollback.
7. Update the API #60 eight sheets and reports, affected server-study context pages/manifest and this worklog. Do not edit API #35/#47 contracts, API #61 behavior, catalog, diagrams or DB schema.
8. Run focused #59/#60 tests, full Study suite, Ruff, OpenAPI, DD/template/link/JSON checks, manifest checks, `git diff --check` and context validator; distinguish baseline DB Admin/context drift from API evidence.

## CHANGES

- Runtime: added `POST /api/v1/mentor/support/{request_id}/reply`, strict request/envelope models, raw signed-int64 and ordered JSON-array validators, SQL-only request/upload/insert/link constants, Mentor auth/ownership handling, one transaction and safe rollback.
- Projection: extracted the pure API #59 request/thread mapper into `mentor/_shared/support_request_projection.py`; #59 and #60 now use the same mapper.
- Tests: added 21 API #60 TestClient cases for auth, path/body validation, request/owner mapping, attachment scope/order, thread rehydration, unchanged status, trace/OpenAPI and rollback. Existing 13 API #59 tests pass.
- DD: reconciled the eight template sheets, split support-message and ordered-link mappings, preserved template appendices, updated plan/open-questions/verification report, and retained `Draft — Needs Confirmation`.
- Context: updated the eight affected server-study pages and registered API #60/shared projection paths in the context manifest.
- Worktree: preserved all unrelated user changes; no commit, push, live DB operation or migration apply.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `deno run -A scripts/select-worklogs.mjs --type coding --limit 3` | 53 matching worklogs; all three selected worklogs were read; no shortage. | `VERIFIED_PREFLIGHT` |
| API #58/#59/#60 source, catalog, AC-24, migration 008 and API #34/#47 linked source review | Local support fallback, Mentor identity pattern, UploadAsset eligibility, ordered JSON-array refs and #61 resolve boundary recorded before runtime edits. | `VERIFIED_STATIC` |
| `uv run pytest tests/modules/mentor/api_59_mentor_support_request_detail tests/modules/mentor/api_60_mentor_support_reply -q` | 34 passed (13 #59 regression + 21 #60). Initial assertions were corrected to match the established `meta.fieldErrors` envelope. | `PASS` |
| `uv run pytest -q` | 584 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| `uv run ruff check app/api/v1.py app/core/middleware.py app/modules/mentor/_shared/support_request_projection.py app/modules/mentor/api_59_mentor_support_request_detail/view.py app/modules/mentor/api_60_mentor_support_reply tests/modules/mentor/api_60_mentor_support_reply` | All checks passed. | `PASS` |
| OpenAPI composition | 30 `/api/v1` path templates, 31 operations; reply path and required `message`/`attachment_refs` fields present; path is integer/int64. | `PASS` |
| API #60 DD static validation | 12 Markdown files; nine sheets retain exact registered template appendices; front matter, JSON examples and relative file links pass. | `PASS` |
| `.agents/context-manifest.json` source paths | All eight newly registered shared/API60 runtime/test paths exist. | `PASS` |
| `git diff --check` | No whitespace errors. | `PASS` |
| `node scripts/validate-agent-context.mjs` | Node unavailable (`node: command not found`); Deno-compatible invocation used. | `NOT_RUN_NODE_UNAVAILABLE` |
| `deno run -A scripts/validate-agent-context.mjs` | Fails with unrelated missing DB Admin context/source paths and broad source drift in the pre-existing dirty workspace. | `BASELINE_FAILURE` |
| `deno run -A scripts/validate-agent-context.mjs --skip-drift` | Remaining findings are missing DB Admin context/source paths outside `server-study`. | `BASELINE_FAILURE_OUT_OF_SCOPE` |

## HANDOFF

- Local API #60 implementation, DD and context/worklog updates are complete. Business approval of DERIVED schema/identity/ref/lifecycle choices and live DB/deployment verification remain outside the evidence gathered here.
- Next API under the continuing one-API-per-session objective is #61; do not treat local fake-DB tests as live acceptance.
