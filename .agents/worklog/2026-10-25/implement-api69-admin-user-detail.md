---
task_id: "2026-10-25-implement-api69-admin-user-detail"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #69 Admin user detail

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 62 coding worklogs available; selected and read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Keep password/token material out of profile projections; legacy BIGINT DDL and fake DB tests do not establish live DB behavior; preserve dirty worktree.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns query execution/orchestration; preserve response/business-code contracts and existing work.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: For catalog paths without 422, raw path parsing can map malformed/out-of-range values to the declared 404; local tests do not prove live schema.
- related worklogs also read: `.agents/worklog/2026-10-25/implement-api68-admin-users-list.md` and `.agents/worklog/2026-10-24/create-study-api69-dd.md`.
- related current DDs read: APIs #68–#72; current auth, response, middleware, route, API #04 profile, API #48 path handling, legacy DDL and API #68 tests.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [docs, test]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Implement read-only API #69 `GET /api/v1/admin/users/{user_id}` in AC-31, called after Admin selects a user from API #68; keep #70 profile/role update, #71 status and #72 delete outside this handler.
- Direct contract: Bearer JWT, role Admin, required path `user_id:int64`, no query/body; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, response `ApiEnvelope<UserProfile>`; exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-31 diagram and catalog agree on single-user detail; #68 list now returns `Page<UserProfile>`. No catalog, diagram or schema change is needed for #69.

## CURRENT_BEHAVIOR

- Runtime: `app/api/v1.py` wires API #68 only; no API #69 route/module/test exists. `DESIGN_CONTRACT_PATHS` includes `/api/v1/admin/users` but not the parameterized detail template.
- Authorization: shared `validate_current_user_request` accepts a required role and returns numeric JWT `sub`; API #68 already uses it with `role="ADMIN"`. No separate Admin permission relation, tenant boundary or MFA rule exists in checked-in DDL.
- Data: API #04 `UserProfile` and its SELECT use id, full_name, email, role, avatar_url, phone, status, created_at and updated_at; nullable avatar/phone serialize as null; the model omits bio and ignores extra source columns. Legacy `users` is BIGSERIAL with a `password_hash`; V1-PILOT identity/profile relations use UUID and do not map directly. Live schema is unverified.
- Errors: `error_response` serializes missing `data` as JSON null. Middleware recognizes FastAPI route templates through `request.scope.route.path`; adding the detail template to the allowlist will preserve DESIGN_* framework errors. Catalog has no 422.
- Related precedent: API #48 reads raw path text and maps malformed/out-of-int64 path input to its declared 404; API #68 validates ADMIN before DB access and safely excludes password_hash.
- Runnable tests at task start: 738 full Study tests passed in the preceding API #68 task; this is baseline evidence, not post-#69 verification.

## SOURCE_TRACE

```text
GET route -> shared JWT guard with role ADMIN -> parse raw user_id as signed int64 -> SELECT safe legacy users projection by id -> no row: catalog 404 -> validate/map UserProfile -> 200 envelope; SQL/projection error: rollback + safe 500 -> focused HTTP/OpenAPI tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Admin permission mapping | Catalog/AC-31 require Admin; API #68 uses shared ADMIN claim; no permission/tenant relation in DDL. | `SOURCE_BACKED_CAPABILITY / DERIVED_POLICY_MAPPING` | Require ADMIN before query, matching #68; DD remains Draft pending policy owner confirmation. |
| User source | Legacy BIGINT `users` matches int64 and API #04 projection; V1-PILOT UUID schema differs; live DB not inspected. | `DERIVED_LOCAL_CANDIDATE / NOT_VERIFIED_LIVE` | Read legacy candidate only; do not add a migration or join pilot identity. |
| Malformed/out-of-range path | Catalog lists 404 but not 422; API #48 uses 404 for invalid int64 path. | `DERIVED` | Parse raw path and map malformed/out-of-range to 404; do not add 422. |
| Missing row | Detail endpoint and catalog declare 404; no-row predicate not separately specified. | `DIRECT_CODE_STATUS / DERIVED_BRANCH` | Return 404 `DESIGN_RESOURCE_NOT_FOUND` after Admin authorization. |
| Profile fields | Catalog `UserProfile` has optional bio; API #04/current runtime has no bio and nullable avatar/phone. | `SOURCE_REQUIRED_FOR_BIO / SOURCE_BACKED_NULLABLES` | Reuse API #04 model, omit bio, preserve null avatar/phone; never select credentials. |
| Error data envelope | Existing DD says `{}` but `error_response` default is null. | `DISCREPANCY_RESOLVED_BY_CURRENT_SOURCE` | Document and test `data:null`; do not change shared helper. |
| Delete/status visibility and PII audit | APIs #71/#72 and policy/schema evidence are incomplete. | `SOURCE_REQUIRED` | No status/deletion predicate or audit/masking rule invented; keep these open in DD. |

## IMPLEMENTATION_PLAN

1. Freeze this plan before source edits. Preserve #69 method/path/auth/path type/no body/query/200/response/error set. Keep #70–#72 mutations separate.
2. Create `app/modules/admin/api_69_admin_user_detail/` with declarative success envelope reusing API #04 `UserProfile`; put the single safe SELECT in `query.py` as a constant only.
3. In `validate.py`, call the shared `validate_current_user_request(..., role="ADMIN")` before DB access and parse raw path text as signed int64. Invalid format/overflow maps to the catalog's 404; do not add a 422 code.
4. In `view.py`, execute one bound `users.id = :user_id` lookup after authorization; map no row to 404, validate safe UserProfile projection, map SQL/projection failure to safe 500 with rollback, and never commit or log PII.
5. Wire `GET /admin/users/{user_id}` in `app/api/v1.py` using raw `Request.path_params`, OpenAPI int64 path metadata and only 200/401/403/404/500 responses. Add the route template to middleware `DESIGN_CONTRACT_PATHS`.
6. Add focused TestClient coverage: ADMIN auth before query, valid profile with null optionals and omitted bio, no row 404, malformed/overflow path 404 without query, SQL and malformed projection 500/rollback, trace/envelope, read-only behavior and exact OpenAPI error/path schema.
7. Review AC-31 #68–#72 DD boundaries. Update the 11-file #69 DD to current source/runtime while preserving the eight Excel appendix suffixes; correct outdated `{}`/Student-only/UNWIRED statements, retain unresolved live-schema, Admin policy, PII/audit, bio and lifecycle questions. Update any linked report that falsely claims #69 remains unwired; do not alter sibling runtime.
8. Update only affected server-study route/runtime/security/database/architecture/module/test/source-status pages and manifest with API #69 paths and post-verification counts.
9. Run focused and full Study tests, Ruff, import/OpenAPI checks, DD relative-link/template checks, `git diff --check`, and Deno context validation. Report repository baseline failures separately; preserve all pre-existing worktree changes and do not stage/commit.

## PRE-CODE CHECKPOINT

Expected/current behavior, source trace, discrepancies and this plan are recorded before runtime, DD or context edits.

## CHANGES

- Added `app/modules/admin/api_69_admin_user_detail/` models, SQL constant, shared ADMIN/path validator and read-only view; wired GET route and middleware contract template.
- Added 13 focused TestClient tests covering authorization order, safe profile/null mapping, 404/500 branches, rollback, trace, read-only behavior and OpenAPI.
- Updated the 11-file API #69 DD package, including final verification report, while retaining all eight original Excel appendix suffixes. Corrected stale AC-31 group runtime summaries in the #70/#71 reports and confirmed #72 already reflects #69 runtime status.
- Updated server-study route/runtime/security/database/architecture/module/test/source-status pages and manifest; six API #69 source references exist.
- Preserved the existing broadly dirty worktree; no cleanup, staging, or commit.
- Assumptions: ADMIN claim follows API #68 local policy fallback; legacy `users` is a local candidate only; malformed path to 404 follows catalog error set and API #48 precedent. No live schema/deployment claim.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Coding worklog preflight | 62 available; selected/read #34/#47/#48; also read #68 implementation and prior #69 DD worklogs. | `VERIFIED_PREFLIGHT` |
| API #69 contract/DD/source trace | Catalog, AC-31 node, #68, #70–#72 boundaries, current auth/response/middleware/DDL/API #04 projection reviewed. | `VERIFIED_SOURCE_REVIEW` |
| Focused API #69 TestClient suite | 13 passed; one upstream Starlette/httpx deprecation warning. | `PASS` |
| Full Study suite | 751 passed, 1 warning in 31.37s. | `PASS` |
| Ruff | `./.venv/bin/ruff check app tests` — all checks passed. | `PASS` |
| OpenAPI | 39 `/api/v1` path templates / 40 operations; required int64 path and Authorization; exact 200/401/403/404/500 responses. | `PASS` |
| DD static checks | 11 files; 8 appendix suffixes match `HEAD`; relative links, JSON examples, fences and whitespace pass; 6 manifest source references exist. | `PASS` |
| AC-31 sibling report review | Corrected stale “all five APIs UNWIRED” claims in #70/#71 reports; #72 already reflects #68/#69 wired and #70–#72 unwired. | `PASS — DOCUMENT REVIEW` |
| Context validator `--skip-drift` | Fails only on pre-existing missing DB Admin pages/source roots and links; no Study context-path diagnostics. | `PARTIAL — BASELINE` |
| Context validator default | Same DB Admin baseline plus `CONTEXT_STALE` entries from current dirty worktree across Study/other scopes. | `PARTIAL — BASELINE` |
| `git diff --check` | No diagnostics. | `PASS` |
| Live DB/deployment | Not inspected; fake-session tests do not establish schema availability or migration/deployment state. | `NOT_VERIFIED_HERE` |

## HANDOFF

- Remaining blockers: none for local implementation under the selected DERIVED rules; live schema, separate Admin permission/tenant/MFA, PII audit, bio source and lifecycle visibility remain unverified. Context validator has unrelated DB Admin missing-path failures and default worktree drift.
- Next task in the one-API-per-session sequence: API #70.
