---
task_id: "2026-10-25-implement-api70-admin-user-update"
date: "2026-10-25"
primary_task_type: "coding"
secondary_task_types: ["docs", "test"]
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Implement Study Server API #70 Admin user update

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `coding`
- selector_command: `deno run --allow-read --allow-env scripts/select-worklogs.mjs --type coding --limit 3`
- selector_result: 63 coding worklogs available; selected/read all 3; no shortage.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-25/implement-api34-upload-assets.md`
    - carry_forward: Preserve dirty files; checked-in legacy BIGINT schema and fake DB tests do not establish live schema or deployment; maintain exact response/error contracts.
  - path: `.agents/worklog/2026-10-25/implement-api47-mentor-lectures.md`
    - carry_forward: `query.py` contains SQL constants only; `view.py` owns DB execution/transaction; keep local schema choices separate from live database facts.
  - path: `.agents/worklog/2026-10-25/implement-api48-mentor-lecture-detail.md`
    - carry_forward: Follow source precedence, record DERIVED behavior explicitly, and preserve existing broad worktree changes.
- related current worklogs/DDs read: API #68 implementation, API #69 implementation, API #70 original DD creation; linked API #71/#72 open questions and AC-31 reports reviewed.
- shortage: `none`

## CLASSIFICATION

```text
primary_task_type: coding
secondary_task_types: [docs, test]
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Implement `PUT /api/v1/admin/users/{user_id}` in AC-31 as an Admin operation updating user profile/role and returning `ApiEnvelope<UserProfile>`.
- Direct contract: Bearer JWT, Admin actor, required `user_id:int64`, HTTP 200 `DESIGN_RESOURCE_UPDATED`, and exact errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-31 diagram says “UPDATE user/profile”; #71 owns account status, #72 owns delete/anonymization. Direct catalog and diagram do not specify the #70 body.

## CURRENT_BEHAVIOR

- Runtime before this task: APIs #68/#69 are wired; #70 has no route/module/test. Middleware already recognizes `/api/v1/admin/users/{user_id}` for #69, so its parameterized template will also map #70 validation errors.
- Auth: API #68/#69 use `validate_current_user_request(..., role="ADMIN")`. Guard validates signed JWT claims without a live admin-permission relation or database account-status lookup.
- Profile precedent: API #14 requires `full_name`, `phone`, `avatar_url`; it trims full name, enforces nonblank/max 150, normalizes blank nullable profile strings to null, enforces phone max 20, and writes `updated_at`.
- Schema evidence: checked-in legacy `users` is BIGINT with `full_name VARCHAR(150)`, `email`, `password_hash`, `role VARCHAR(20)`, nullable `avatar_url`, nullable `phone VARCHAR(20)`, `status`, `created_at`, `updated_at`. No bio or deleted_at column. V1-PILOT identity/profile relations are UUID and do not map to this `int64` API. Live schema is not verified.
- Role evidence: current runtime/API guards and data use role strings `STUDENT`, `MENTOR`, and `ADMIN`; the legacy column has no CHECK/enum. No approved transition, self-change, tenant, audit, PII, or session-revocation policy exists.
- Runnable test baseline: latest API #69 worklog records 751 full Study tests passed; this is pre-#70 evidence. No API #70 tests exist.

## SOURCE_TRACE

```text
PUT route -> shared ADMIN JWT guard -> signed-int64 raw path validation -> strict candidate full-replacement body validation -> one bound UPDATE users by id RETURNING safe UserProfile fields -> no row 404 / validation 422 / SQL, mapping or commit failure 500 with rollback -> success commit and ApiEnvelope<UserProfile> -> focused HTTP/OpenAPI tests
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Body absent from direct contract | AC-31 node/catalog provide path only; AC-31 names profile/role update; legacy users has matching writable columns. | `DISCREPANCY / DERIVED_FALLBACK` | Choose required full-replacement fields `full_name`, `phone`, `avatar_url`, `role`; reject extras; keep catalog/diagram unchanged and label body DERIVED. |
| Validation/nullable semantics | API #14 source applies trim/nonblank/max-150 name, trim/blank-to-null phone/avatar, phone max-20. | `SOURCE_BACKED_PRECEDENT / DERIVED_FOR_70` | Reuse the same rules for profile fields; phone/avatar are required keys but accept null under PUT replacement semantics. |
| Role values | Existing runtime uses STUDENT, MENTOR and ADMIN; DDL has a free-text column and catalog has no enum members. | `DERIVED_FALLBACK` | Accept only those three known application role labels; keep exact value, no transition/self/last-admin policy invented. |
| Authorization mapping | Catalog/diagram require Admin; #68/#69 locally use shared ADMIN claim; no separate policy relation is present. | `DERIVED_POLICY_MAPPING` | Require ADMIN before DB access, matching the adjacent Admin APIs; leave permission/tenant/MFA policy open. |
| Physical source | Legacy BIGINT `users` matches endpoint ID; V1-PILOT uses incompatible UUID identity relations; live metadata unavailable. | `DERIVED_LOCAL_CANDIDATE / NOT_VERIFIED_LIVE` | Update checked-in legacy candidate only; no migration or pilot join. |
| Invalid path | #70 declares 422; unlike #69, validation is part of direct error set. | `DERIVED_BRANCH_WITH_DIRECT_CODE` | Malformed or out-of-int64 path returns 422 `DESIGN_VALIDATION_ERROR`; valid int64 with no row returns 404. |
| Session/audit/PII/lifecycle effects | Diagram does not specify #70 audit/revoke; #71 owns status and only conditionally mentions session revocation; current access JWT relies on signed role claims until expiry. | `SOURCE_REQUIRED` | Do not mutate refresh tokens/status or add audit; document stale access-claim, PII and deleted-user visibility questions. |
| Error envelope | Current helper emits `data:null`; old #70 DD suggested `{}`. | `DISCREPANCY_RESOLVED_BY_CURRENT_SOURCE` | Keep helper behavior and test null error data; do not change shared response behavior. |

## IMPLEMENTATION_PLAN

1. Freeze this source trace and fallback before runtime edits; keep method/path/role/response and exactly catalog errors unchanged. Do not overlap #71 status or #72 delete.
2. Add module-local declarative request/envelope models. Use required full replacement keys `full_name:string`, `phone:string|null`, `avatar_url:string|null`, `role:Literal[STUDENT, MENTOR, ADMIN]`; forbid extra keys. This is a local DERIVED contract because body is omitted from direct sources.
3. In `validate.py`, run shared ADMIN guard; parse raw path as signed int64 (map malformed/overflow to catalog 422); reuse API #14 name/phone/avatar normalization and constraints; map errors with `error_response`.
4. In SQL-only `query.py`, add one bound UPDATE against legacy `users` by `id`, updating the four chosen fields and `updated_at`, returning only safe UserProfile fields. Preserve email/status/created_at; never select or update `password_hash`; do not add status, delete, audit or token side effects.
5. In `view.py`, own query, mapping, commit/rollback and response; map no row to 404, invalid returned projection and SQL/commit failure to safe 500, and commit only after validating the response projection.
6. Wire PUT beside #69 at the same path with required Authorization, int64 path and strict JSON request schema; declare only 200/401/403/404/422/500. Middleware path template already exists; confirm it maps 422 to the design code.
7. Add TestClient coverage for valid full update/normalization, role allowlist, extra/missing/invalid input, ADMIN before DB, malformed/out-of-range path, no-row 404, SQL/projection/commit rollback, safe response fields, trace/read-write behavior and OpenAPI.
8. Update all #70 DD pages/reports to separate direct contract from DERIVED runtime; preserve eight Excel appendix suffixes. Review AC-31 sibling report claims and update only stale current-state summaries for #70 wiring.
9. Update server-study routes/runtime/security/database/architecture/module/tests/entry/source-status and manifest; update route operations/test counts after verification.
10. Run focused/full Study tests, Ruff, import/OpenAPI checks, DD static checks, `git diff --check`, and context validation; distinguish existing DB Admin/missing-source and worktree-drift validator failures from API #70 evidence.

## PRE-CODE CHECKPOINT

Contract, diagrams, checked-in schema, API #14/#68/#69 source, linked #71/#72 boundaries, discrepancies and this plan are recorded before editing runtime or DD implementation pages.

## CHANGES

- Added `app/modules/admin/api_70_admin_user_update/{__init__,models,query,validate,view}.py` and `tests/modules/admin/api_70_admin_user_update/test_admin_user_update.py`.
- Wired `PUT /admin/users/{user_id}` with required Authorization/path metadata, strict request schema and the catalog 200/401/403/404/422/500 response set. Existing middleware path template is reused.
- Updated all API #70 DD sheets, open questions, plan result and verification report; preserved all eight template appendix suffixes. Updated current AC-31 sibling report claims for #71/#72.
- Updated server-study route/runtime/security/database/architecture/module/test context, project source status and manifest with six exact module/test source paths.
- Assumptions: body, role labels, full-replacement semantics, profile normalization, Admin claim mapping and legacy table target remain explicit DERIVED fallbacks; no live DB or security-policy approval is implied.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Coding worklog preflight | 63 available; selected/read #34/#47/#48. | `VERIFIED_PREFLIGHT` |
| API #70 DD, AC-31/catalog, legacy DDL and linked source trace | Reviewed before plan; exact findings recorded above. | `VERIFIED_SOURCE_REVIEW` |
| Focused API #70 tests | `./.venv/bin/pytest -q tests/modules/admin/api_70_admin_user_update` — 19 passed, one upstream Starlette/httpx deprecation warning. | `VERIFIED` |
| Full Study suite | `./.venv/bin/pytest -q` — 770 passed, one upstream Starlette/httpx deprecation warning. | `VERIFIED` |
| Ruff | `./.venv/bin/ruff check app tests` — All checks passed. | `VERIFIED` |
| OpenAPI/import | 39 unique API paths, 41 operations; PUT fields/required keys/role enum/Authorization and exact 200/401/403/404/422/500 set verified. | `VERIFIED` |
| DD static | 11 files, balanced fences, valid JSON examples and local links; eight appendix suffixes byte-equal to `HEAD`. | `VERIFIED_STATIC` |
| `git diff --check` | No diagnostics. | `VERIFIED` |
| Context validator `--skip-drift` | Exit 1 with 43 existing DB Admin missing-context/source diagnostics; Study structure produced no separate invalid diagnostic. | `BASELINE_INVALID` |
| Context validator default | Exit 1 with existing DB Admin missing paths and snapshot drift in server-study, server-work, web-work (including both subscopes), mobile-work and db-admin. | `BASELINE_INVALID_AND_STALE` |

## HANDOFF

- Local API #70 implementation and verification are complete. Live schema/deployment, Admin permission, role-transition, token invalidation, audit/PII and #72 lifecycle policy remain unverified; the DD stays Draft.
- Next task in the one-API-per-session sequence: API #71.
