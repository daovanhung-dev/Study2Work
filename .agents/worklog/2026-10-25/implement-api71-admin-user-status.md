---
task_id: "2026-10-25-implement-api71-admin-user-status"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["test", "docs"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #71 Admin user status

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 64 coding worklogs available; selected/read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve the Study API error/transaction contracts, keep fake DB tests separate from live schema, and preserve unrelated dirty worktree entries.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: `query.py` must contain SQL constants only; `view.py` owns query execution, side effects and commit/rollback; checked-in DDL does not establish live schema.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Follow diagram → infra → API catalog when resolving discrepancies, document DERIVED fallbacks, preserve route/error contracts, and verify linked endpoints.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [test, docs]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Direct catalog contract: `PATCH /api/v1/admin/users/{user_id}/status`, Bearer JWT/Admin, required `user_id:int64`, `ApiEnvelope<UserProfile>`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and only the listed 401/403/404/422/500 `DESIGN_*` errors.
- AC-31 diagram: STATUS branch updates account status; session revocation is conditional; then reloads user list/detail. #70 owns profile/role; #72 owns deletion/anonymization.
- DD #71 is `Draft — Needs Confirmation`. It proposes a required `{status}` body and `ACTIVE`/`SUSPENDED` lock/unlock candidates, plus conditional refresh-token revocation; it explicitly marks these as DERIVED, not approved enum/contract.

## CURRENT_BEHAVIOR

- Worktree: 481 modified/untracked entries at task start. Preserve every change outside the scoped #71 implementation/context/report updates.
- Runtime: APIs #68–#70 are wired; no #71 route/module/test exists. Middleware `DESIGN_CONTRACT_PATHS` contains `/api/v1/admin/users/{user_id}` but not the new `/status` route.
- Auth: #68–#70 use `validate_current_user_request(..., role="ADMIN")`; this verifies the JWT role claim, not a dedicated user-management permission, tenant, MFA or DB account status.
- DB/auth source: checked-in legacy `users.status` is nullable VARCHAR with ACTIVE default; legacy `refresh_tokens` has `user_id`, `expires_at`, `revoked_at`. API #3 login/refresh require ACTIVE; refresh rotation revokes a single token row. Access-JWT guard checks claims/roles only and does not consult account status/revocation.
- Response source: API #04 `UserProfile` is the safe profile allowlist; it omits bio and credentials. `error_response` currently returns `data: null`.
- Schema boundary: V1-PILOT UUID `identity_projections.account_status` enum differs from legacy BIGINT `users`; neither local DDL artifact proves live schema/deployment.
- Latest recorded pre-task verification: API #70 full Study suite 770 passed; API #71 has no tests.

## SOURCE_TRACE

```text
PATCH route -> shared ADMIN JWT guard -> raw signed-int64 path/body validation -> SELECT legacy user FOR UPDATE -> reject unsupported current state -> UPDATE users.status/updated_at RETURNING safe UserProfile -> when target is SUSPENDED revoke unexpired, unrevoked refresh rows in the same transaction -> validate safe profile -> commit -> ApiEnvelope<UserProfile>; failures map to exact catalog codes and rollback
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Implementation impact |
|---|---|---|---|
| Request body missing from direct contract | Catalog/diagram only specify path; operation means lock/unlock; DD proposes `{status}`. | `DISCREPANCY / DERIVED_FALLBACK` | Implement strict required `{status}` with only `ACTIVE` or `SUSPENDED`; preserve Draft and disclose the inference in the DD. |
| Status enum | Legacy `users.status` is unconstrained VARCHAR; diagram names lock/unlock; V1-PILOT has ACTIVE/SUSPENDED plus unrelated lifecycle states but uses UUID. | `DERIVED / SOURCE_REQUIRED` | Accept ACTIVE/SUSPENDED for this operation only. Never infer that pilot lifecycle values belong to legacy `users`. |
| Current-state transition | API #3 allows sign-in/refresh only for ACTIVE; #72 owns deletion lifecycle. No transition matrix is approved. | `DERIVED_FALLBACK` | Only change rows whose current status is ACTIVE or SUSPENDED; return catalog 422 for other current states to avoid activating pending/deletion states through a lock/unlock route. |
| Admin permission | Catalog/diagram say Admin; adjacent #68–#70 use shared `ADMIN` JWT role; no separate permission source exists. | `DERIVED_POLICY_MAPPING` | Reuse shared ADMIN guard before DB access; do not add tenant/MFA/self/last-admin policies. |
| Session revocation | Diagram says “revoke session if needed”; API #3 stores refresh tokens and checks status on refresh; no access-token denylist/version mechanism exists. | `DERIVED_FALLBACK / SOURCE_REQUIRED` | On target SUSPENDED, revoke unexpired and unrevoked refresh-token rows atomically with the status change. Do not revoke/restore rows on activation; state clearly that existing access JWTs may work until expiry. |
| Same-status request | DD leaves no-op behavior open; catalog has no 409. | `DERIVED_FALLBACK` | Return 200 and set `updated_at` to current timestamp; repeated suspension also reapplies eligible refresh-token revocation. Do not add 409. |
| Invalid path | Catalog includes 422 but does not define malformed/overflow mapping. #70 already uses raw signed-int64 parsing and 422. | `DERIVED_WITH_DIRECT_CODE` | Use signed-int64 bounds; malformed/out-of-range values return 422 `DESIGN_VALIDATION_ERROR`. |
| Error envelope | DD says current helper may emit `{}`; current `error_response` source emits `data: null`. | `DISCREPANCY_RESOLVED_BY_CURRENT_SOURCE` | Retain current helper behavior and document/test `data: null`. |
| Live schema, audit/PII and immediate access revocation | Only checked-in DDL/current source; no live metadata or approved policy. | `NOT_VERIFIED / SOURCE_REQUIRED` | No migration, audit, access-token mechanism, or deployment claim. |

## IMPLEMENTATION_PLAN

1. Freeze the diagram/infra/catalog precedence and all DERIVED choices in this worklog before runtime edits; do not change catalog/diagram or overlap #70/#72 mutations.
2. Add declarative request/envelope models: strict required `status: Literal["ACTIVE", "SUSPENDED"]`, extra fields forbidden, and `ApiEnvelope<UserProfile>` response.
3. Add API-specific validation using the shared `ADMIN` guard and raw signed-int64 parser. Return 422 with catalog code for malformed/out-of-range path; framework body-validation errors must also resolve to `DESIGN_VALIDATION_ERROR` through the route-template middleware entry.
4. Keep SQL constants only in `query.py`: (a) lock/read the user status by bound ID, (b) update status and `updated_at` returning safe UserProfile fields, and (c) conditionally revoke currently valid refresh-token rows for suspension.
5. In `view.py`, authenticate before DB; own lock/update/revoke/response mapping and transaction. Return 404 for no user, 422 for an existing unsupported current status, safe 500 plus rollback for query/projection/revoke/commit errors, and commit only after a valid safe profile projection.
6. Wire `PATCH /admin/users/{user_id}/status` in `app/api/v1.py`; add its parameterized route template to `DESIGN_CONTRACT_PATHS`; declare exactly 200/401/403/404/422/500 and the required int64/header/body OpenAPI fields.
7. Add focused HTTP tests for ADMIN auth before DB, request validation, ID bounds, 404, supported/unsupported current state, ACTIVE/SUSPENDED effects, refresh revoke rollback, projection/commit failures, trace/error envelope and OpenAPI. Run API #03 refresh tests as a linked regression, then the full Study suite and Ruff.
8. Update #71 DD runtime/data/error/plan/report pages while preserving eight Excel appendix suffixes. Review #68–#72 current-state claims and correct only stale runtime summaries; keep #72 unwired.
9. Update server-study route/runtime/security/database/architecture/module/test context, project source status and manifest required paths; refresh counts after test/OpenAPI verification.
10. Run DD static checks, import/OpenAPI check, `git diff --check`, and context validator. Report the existing missing DB Admin/snapshot-drift baseline separately from API #71 behavior.

## PRE-CODE CHECKPOINT

The catalog row, AC-31 STATUS node/edges, legacy and V1-PILOT DDL, API #03/#04 and #68–#70 source, middleware, response helper, DD #71 and all three coding preflight worklogs have been reviewed. The plan above is recorded before code, test or DD implementation edits.

## CHANGES

- Runtime files: `apps/study-server/app/api/v1.py`, `apps/study-server/app/core/middleware.py`, and new `app/modules/admin/api_71_admin_user_status/{__init__,models,query,validate,view}.py` plus focused tests.
- DD files: API #71 sheets/reports, including a separate `08_refresh_tokens_update.md` mapping; refreshed current AC-31 macro-review claims in #69/#70/#72 reports.
- Context files: server-study route/runtime/security/database/architecture/modules/tests/workflow, `.agents/project/source-status.md`, and `.agents/context-manifest.json` with six new source/test paths.
- CONTEXT_UPDATES: source-backed API #71 runtime recorded; current route/operation/test counts refreshed; remaining DB Admin/snapshot drift is tracked separately.
- Assumptions: Body/status/current-state/revoke/no-op choices remain DERIVED. Admin-role mapping is inherited from adjacent AC-31 runtime. No live DB, policy approval or immediate access-JWT invalidation is implied.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | 64 coding worklogs; selected/read #34/#47/#48. | `VERIFIED_PREFLIGHT` |
| API #71 direct contract, diagram, infra and linked source | Reviewed before plan; evidence and gaps recorded above. | `VERIFIED_SOURCE_REVIEW` |
| API #71 focused suite | `21 passed`; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Linked API #03/#68–#71 regression | `80 passed`; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Full Study suite | `791 passed`; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Ruff | `./.venv/bin/ruff check app tests` — all checks passed. | `PASS` |
| OpenAPI/import | 40 `/api/v1` paths, 42 operations; required int64 path/header/body and exact API #71 response set present. | `PASS` |
| DD/context/static validation | 12 DD Markdown files, JSON/links/fences/whitespace và 8 appendix suffixes pass; manifest có đủ 6 file; `git diff --check` pass. Context validator có 43 lỗi DB Admin ngoài scope; default thêm stale drift ở 7 scopes. | `PASS_WITH_BASELINE` |

## HANDOFF

- Remaining blockers: none for local DERIVED implementation; live schema, dedicated Admin policy, status enum approval, self/last-admin rules, audit/PII and immediate access-JWT revocation remain unverified.
- Next task in the one-API-per-session sequence: API #72.
