---
task_id: "2026-10-25-implement-api68-admin-users-list"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #68 Admin users list

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 61 coding worklogs available; selected 3 and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve shared response/auth contracts; legacy BIGINT tables remain local candidates, not live DB proof; keep credentials and password hashes out of projections.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: Follow SQL-constants-only query.py and keep query execution/orchestration in view.py; preserve all existing worktree changes.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Trace linked API persistence and HTTP mapping; local fake-DB tests do not verify live schema or deployment.
- related prior design record: `.agents/worklog/2026-10-24/create-study-api68-dd.md` read; its candidate list/page behavior and unresolved direct response discrepancy are carried forward for resolution under the current user instruction.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [docs, test]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Implement API #68 for the AC-31 Admin user-management list. Keep it separate from #69 detail and #70/#71/#72 mutations; AC-31 reloads the list after those operations.
- Catalog before reconciliation: GET `/api/v1/admin/users`; Bearer JWT/Admin; optional `role:string`, `status:string`, `keyword:string`, `page:int32`; no body; 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/500; success response currently says `ApiEnvelope<UserProfile>`.
- Diagram: AC-31 actor is Admin with user-management access; step n2 queries users + pagination; user chooses detail/update/status/delete and later reloads. Diagram's generic `ApiEnvelope` does not specify a collection type.
- Resolution under the user's diagram → infrastructure → catalog → simplest coherent fallback order: a user-management list with pagination needs `ApiEnvelope<Page<UserProfile>>`. Correct API #68's catalog/diagram response metadata accordingly; add 422 `DESIGN_VALIDATION_ERROR` for the declared int32 page's invalid/range input, following API #07's page-validation convention. Do not change unrelated API rows or diagram nodes.

## CURRENT_BEHAVIOR

- Source/config: API #68 route/module/tests are absent; `/api/v1/admin/users` is not in `DESIGN_CONTRACT_PATHS`. No Admin-specific source role/policy table was found. `validate_current_user_request` is generic over role claims and can enforce `ADMIN` before DB access.
- Related profile source: API #04 `UserProfile` safely selects id, full_name, email, role, avatar_url, phone, status, created_at and updated_at; it excludes password_hash and does not define bio. API #14 reuses the persisted profile fields. Current role/status source types are strings, without an enum allowlist.
- Related pagination source: API #07 uses page 1, fixed size 20, stable PageMeta and DESIGN_VALIDATION_ERROR for page < 1. API #54/#46 use the same Page shape. API #07's fixed size and filter semantics are precedent only until applied to #68 by this plan.
- Infrastructure: diagram/legacy DDL describe `users.id BIGSERIAL`, full_name, email, password_hash, role, avatar_url, phone, status, created_at, updated_at. No bio, deleted_at, or admin-permission relation is present in that candidate. V1-PILOT identity/profile/role tables use UUID and are structurally distinct. No live schema has been inspected.
- Shared behavior: `error_response` defaults error data to JSON null. Middleware maps RequestValidationError to DESIGN_VALIDATION_ERROR only for allowlisted design paths. Existing API #68 DD statements saying data `{}` and Student-only guard are stale against current source.
- Runnable tests: prior current-tree full suite evidence is 723 passing tests; API #68 has no route or tests at task start. This baseline will be reverified after changes.

## SOURCE_TRACE

```text
GET /api/v1/admin/users -> shared Bearer/JWT guard requiring ADMIN claim -> validate optional filters and int32 page -> bind same role/status/keyword predicates into COUNT and ordered page queries -> map safe API #04 UserProfile rows -> Page<UserProfile> envelope -> focused HTTP/OpenAPI tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Success cardinality | AC-31 says list + pagination; catalog only says UserProfile; DD proposed Page<UserProfile>. | `DISCREPANCY` resolved by source hierarchy | Correct only API #68 response metadata to Page<UserProfile>; keep empty list as HTTP 200. |
| Page rule/error | Catalog declares int32 but no default/minimum/422; API #07 uses default 1, fixed 20, min page 1 and 422. | `DERIVED` from linked pagination precedent | Use page 1, fixed size 20, int32 range, return 422 DESIGN_VALIDATION_ERROR for invalid page; update #68 error contract only. |
| Admin authorization | AC/catalog require Admin; no dedicated Admin permission relation, generic JWT role helper supports explicit ADMIN. | `SOURCE_BACKED` guard capability + `DERIVED` permission mapping | Require role claim ADMIN before queries; no extra table/policy is invented. |
| User source | Legacy users BIGINT matches int64; V1-PILOT identity is UUID and differs. | `DERIVED` local query target; live schema `NOT_VERIFIED` | Query checked-in legacy users shape only; add no migration and do not claim deployment. |
| UserProfile fields/PII | Reusable profile includes optional bio; API #04 current model omits bio, includes nullable avatar/phone and email. | `DISCREPANCY`/`SOURCE_REQUIRED` for bio | Reuse source-backed API #04 model, omit bio, return PII only behind ADMIN guard, never select password_hash. |
| Role/status filters | Query keys are direct but enum members are absent. | `DERIVED` | Exact-match arbitrary strings; do not invent enum whitelist; unknown value yields empty page. |
| Keyword matching | DD proposes case-insensitive substring on full_name/email; wildcard policy is open. | `DERIVED` | Normalize trim/lowercase through shared helper and use literal substring SQL semantics. |
| Deleted-user visibility | Legacy users candidate has no deletion column; #71/#72 policies are unresolved. | `SOURCE_REQUIRED` | Do not invent deletion predicate; list rows present in selected source and honor optional status filter. |
| Runtime/DD status | Existing DD says UNWIRED and has stale auth/error claims; current source confirms no API #68 route. | `UNWIRED` before implementation | Update API #68 DD/runtime evidence after wiring; retain Draft for live-schema/admin-permission/policy gaps. |

## IMPLEMENTATION_PLAN

1. Freeze this plan before runtime edits; use AC-31 as the functional list/pagination source, the legacy DDL as the only compatible int64 user-table candidate, and the catalog as the exact query/error inventory. Do not modify other API rows or admin mutation endpoints.
2. Correct the API #68 catalog response to `ApiEnvelope<Page<UserProfile>>`, make the AC-31 node's output explicit, and add only the page-validation 422 documented by the API #07 precedent. Keep method/path/query/no-body/200/401/403/500 unchanged.
3. Add `admin/api_68_admin_users_list` with declarative `AdminUsersQuery`, `AdminUsersPage`, `AdminUsersPagination` and typed success envelope; reuse API #04 `UserProfile` to preserve one safe profile contract and omit unsupported bio.
4. Keep `query.py` to SQL constants. Add paginated SELECT and COUNT over legacy `users` with identical optional role/status predicates, case-insensitive literal keyword substring on full_name/email, `id ASC`, limit 20 and computed offset. Bind all values; never select password_hash.
5. Implement input normalization in API-local `validate.py`: shared ADMIN JWT guard, validate page integer 1..2^31-1 with DESIGN_VALIDATION_ERROR, trim/lowercase optional keyword, and leave role/status values exact/unrestricted because no enum members are supported.
6. Implement view orchestration: authenticate before queries, validate filters, execute count/list with caller-owned read transaction, validate count and UserProfile projections, map empty results to a valid empty Page, return 500 safely for SQL/mapping failures, rollback failed reads, and never commit.
7. Wire the route with exact OpenAPI request/query/header/response/error metadata and add `/api/v1/admin/users` to middleware design-contract paths so framework validation/internal errors use DESIGN_* codes.
8. Add TestClient coverage for missing/non-ADMIN auth before DB, filters and literal keyword, default/fixed pagination/order/metadata, empty result, nullable fields and password-hash exclusion, invalid page/range, malformed rows/count, SQL failures/rollback, trace/envelope, and OpenAPI contract.
9. Review AC-31 sibling DDs #69–#72 for UserProfile/visibility/status/delete boundaries; keep those APIs unimplemented and record the group consistency findings. Update API #68 DD sheets/reports to match the selected contract and runtime, preserve all 8 template appendix suffixes, keep Draft for unresolved live schema/policy, and do not modify sibling DD runtime assumptions without evidence.
10. Update only affected server-study context pages and manifest source/test inventory, including the ADMIN role/API #68 route and post-test/OpenAPI counts.
11. Run focused API #68 tests, linked AC-31 contract checks, the full Study suite, Ruff, route import/OpenAPI checks, DD static/template/link checks, `git diff --check`, and Deno context validator. Preserve/report the pre-existing DB Admin validator baseline and all worktree changes; do not stage or commit.

## PRE-CODE CHECKPOINT

Plan and source trace are recorded before runtime, catalog, diagram, DD or context edits. The plan was recorded before code; implementation, contract, DD, context and verification updates are complete.

## CHANGES

- Runtime: added `apps/study-server/app/modules/admin/api_68_admin_users_list/` with typed page/envelope models, SQL-only count/page queries, shared ADMIN JWT validation, page/filter normalization and read orchestration.
- Route: registered `GET /api/v1/admin/users` in `app/api/v1.py`; added design-contract middleware mapping. OpenAPI declares optional role/status/keyword/page, required Authorization and 200/401/403/422/500.
- Contract: changed only API #68 catalog response to `ApiEnvelope<Page<UserProfile>>`, added 422 page validation, and made the AC-31 node explicit.
- Tests: added 15 focused TestClient cases. Safe projection reuses API #04 UserProfile and never selects password_hash.
- DD: updated all 8 canonical sheets plus open questions, plan result and verification report. Preserved each template appendix suffix byte-for-byte. DD remains Draft due live schema/permission/PII/lifecycle questions.
- Macro-review: corrected stale #68 response mismatch references in AC-31 sibling DDs #69–#72; their runtime remains unchanged/unwired.
- Context: updated server-study runtime, routes, architecture, database/security, module/test/source-status pages and manifest; appended the 7 API #68 module/test paths.
- Pre-existing worktree changes were retained; no staging or commit performed.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Coding worklog preflight | 61 available; selected/read #34/#47/#48 plus prior API #68 DD log. | `VERIFIED_PREFLIGHT` |
| Focused API #68 tests | 15 passed; one upstream Starlette/httpx TestClient deprecation warning. | `PASS` |
| Full Study suite | 738 passed, 1 warning in 31.62s. | `PASS` |
| Ruff | `./.venv/bin/ruff check app tests` — all checks passed. | `PASS` |
| OpenAPI | 38 `/api/v1` path templates, 39 operations; API #68 exposes query/header and 200/401/403/422/500 contract. | `PASS` |
| DD package/appendices | 11 files present; 8 source appendix suffixes byte-identical to pre-edit HEAD. | `PASS` |
| AC-31 stale reference scan | No remaining references claim the #68 list/cardinality mismatch is open. | `PASS` |
| `git diff --check` | No diagnostics. | `PASS` |
| Context validator `--skip-drift` | Fails only on missing DB Admin context/source roots and links outside scope. | `PARTIAL — BASELINE` |
| Context validator default | Same DB Admin baseline plus `CONTEXT_STALE` for existing tracked worktree changes across Study/other scopes. No sourceCommit rewrite. | `PARTIAL — BASELINE` |

## HANDOFF

- API #68 is implemented locally under the selected DERIVED fallback. Live schema, separate Admin permission/tenant policy, PII/audit and lifecycle visibility remain unverified; DD correctly remains Draft.
- AC-31 sibling APIs #69–#72 remain outside this runtime change.
- Next task in the one-API-per-session sequence: API #69.
