---
task_id: "2026-10-24-create-study-api69-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #69

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-24/create-study-api48-dd.md
    - carry_forward: Giữ contract catalog; dùng schema legacy chỉ như candidate; Admin/Mentor auth chưa có source thì không tự thiết kế DB mapping; giữ PII và field thiếu ở trạng thái mở.
  - path: .agents/worklog/2026-10-24/create-study-api49-dd.md
    - carry_forward: Tách direct contract khỏi AC intent; label mọi suy luận DERIVED; giữ schemas legacy và V1-PILOT riêng.
  - path: .agents/worklog/2026-10-24/create-study-api50-dd.md
    - carry_forward: Dùng 8 sheet template + 3 report; no ZIP cho Study; chỉ author sau plan và ma trận; không invent table, column, auth rule, enum hay business code.
- shortage: none

## EXPECTED_BEHAVIOR

- Requirement: Tạo đúng một DD Markdown tiếng Việt cho API #69, lập plan và ma trận trước khi tạo folder DD, giữ nguyên contract catalog, đọc AC-31/diagram và DD liên quan, static-verify gói ngay sau authoring.
- Canonical contract: docs/lists/list_api.md row #69; reusable ApiEnvelope and UserProfile; AC-31 index and activity diagram; registered createDD-markdown skill; Study API DD workflow requires Markdown folder and forbids creating a ZIP.
- Contract trực tiếp: GET /api/v1/admin/users/{user_id}; Bearer JWT, role Admin; path user_id:int64 required; no body/query; HTTP 200 DESIGN_RESOURCE_RETRIEVED; ApiEnvelope<UserProfile>; errors exactly 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 500 DESIGN_INTERNAL_ERROR.

## CURRENT_BEHAVIOR

- Source/config: API #69 has no route, view module or focused test in apps/study-server. Current app/api/v1.py declares catalog IDs #01–#09 and #12–#14. The reusable current-user guard validates Student role only; there is no Admin authorization guard or user-management permission source. Current error_response turns absent data into {}; DESIGN_CONTRACT_PATHS does not include the Admin detail path.
- Data source: Legacy Study DB.sql and DB guide describe candidate BIGINT users fields id, full_name, email, password_hash, role, avatar_url, phone, status, created_at and updated_at. Current API #4/#14 profile query/model use only the safe projection id, full_name, email, role, avatar_url, phone, status, created_at and updated_at; neither has bio. V1-PILOT identity/profile/role tables use UUID and do not map directly to the BIGINT UserProfile contract. Live schema is not verified.
- Runnable tests: Not run; this is docs-only. No API #69 test source was found.
- Inventory before this DD: 68 API DD folders and 35 missing of 103; 12 catalog IDs have a route declaration plus matching view.py, 91 do not. This is source-presence evidence, not proof of runtime behavior.

## SOURCE_TRACE

AC-31 Admin selects a user -> GET /api/v1/admin/users/{user_id} -> intended Admin authentication/authorization -> candidate read of one legacy users row by id using a safe field allowlist -> map ApiEnvelope<UserProfile> -> 200, or catalog 404 when no user is found. No mutation. Admin guard, physical live relation, and exact not-found/auth implementation remain unverified.

## PLAN BEFORE DD AUTHORING

1. Preserve the direct contract exactly: method/path, Admin Bearer requirement, required int64 path parameter, no request body/query, ApiEnvelope<UserProfile>, success 200 DESIGN_RESOURCE_RETRIEVED and only the catalog 401/403/404/500 errors. Do not add 422 or another business code.
2. Read AC-31 index and all page nodes/edges: list + pagination (#68) -> select a user -> detail (#69) -> read user/profile/role -> branch to #70/#71/#72. Keep group macro-review pending until #72 DD exists.
3. Q1 candidate reads only users.id, full_name, email, role, avatar_url, phone, status, created_at, updated_at from legacy users by users.id = :user_id. Do not select password_hash. Treat this as a legacy design candidate only; live schema is unverified.
4. No joins or writes. Missing row maps to catalog 404 as a DERIVED branch; malformed/overflow path mapping is unresolved because the contract has no 422 and API #69 is not wired.
5. Map every UserProfile field individually. Keep bio SOURCE_REQUIRED because neither legacy users nor current API #4/#14 profile projections provide it; do not synthesize it from pilot learner_profiles, which uses UUID identity. Role/status are candidate stored strings; enum members are not defined. Keep optional-field null/omit semantics open.
6. Require Admin authorization before reading the row, but do not invent claim mapping, permission table, tenant boundary, or Admin identity lookup. Current helper is Student-only.
7. Preserve email and phone as Admin-only PII; never select/return password_hash, refresh-token material or credentials.
8. Create the 8 core template sheets plus OPEN_QUESTIONS.md, PLAN_RESULT.md and VERIFICATION_REPORT.md under apps/study-server/docs/dd/69_admin_user_detail/. Keep all sheets Draft — Needs Confirmation; do not edit source, catalog, schema or AC diagrams; do not create a ZIP.
9. After authoring, verify exact 11-file manifest, template front matter and appendix tails, direct contract/error set, UserProfile field coverage, query allowlist, valid JSON examples, relative links/anchors, Markdown tables/fences/whitespace and git diff --check. Do not run application tests.
10. Update the inventory worklog with counts after #69; keep AC-31 macro-review pending until DDs #70–#72 exist.

### API Requirement Matrix

| API ID | Contract item | Value | Basis/status |
|---|---|---|---|
| #69 | Method/path | GET /api/v1/admin/users/{user_id} | Catalog + AC-31; DIRECT |
| #69 | Actor/auth | Admin / Bearer JWT | Catalog + AC-31 precondition; DIRECT requirement, current guard absent |
| #69 | Path | user_id:int64! | Catalog; DIRECT |
| #69 | Body/query | None | Catalog; DIRECT |
| #69 | Success | HTTP 200 DESIGN_RESOURCE_RETRIEVED; ApiEnvelope<UserProfile> | Catalog; DIRECT |
| #69 | Errors | 401 DESIGN_AUTHENTICATION_REQUIRED; 403 DESIGN_ACCESS_DENIED; 404 DESIGN_RESOURCE_NOT_FOUND; 500 DESIGN_INTERNAL_ERROR | Catalog; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT header | Establish Admin identity/role before user-row access | DIRECT requirement; Admin guard/claim mapping SOURCE_REQUIRED |
| user_id | Required path int64 | Candidate users.id = :user_id; maps to data.id | DIRECT type; malformed/overflow behavior unresolved |
| Body | None | None | DIRECT |
| Query | None | None | DIRECT |

### Query Matrix

| Query | Type | Candidate source | Columns/predicate | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | Legacy users AS u | u.id, u.full_name, u.email, u.role, u.avatar_url, u.phone, u.status, u.created_at, u.updated_at; WHERE u.id = :user_id; LIMIT 1 | Single safe profile projection; legacy candidate only, live relation unverified |
| Q1 result | Branch | Candidate users row | No row | Map to catalog 404; DERIVED from detail contract |
| Q1 exclusions | SELECT exclusion | Legacy users | password_hash and all token/credential data | Security allowlist; never return |
| Q2 | N/A | N/A | No joins/count query | Not needed for one-user detail |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | N/A — READ-ONLY API |

### Response Source Matrix

| Response field | Contract type | Candidate source/mapping | Status |
|---|---|---|---|
| success | boolean | Envelope branch | DIRECT convention |
| businessCode | string | Catalog | Exact success/error code; DIRECT |
| message | string | Safe application message | Exact text unspecified; DERIVED |
| data.id | int64 | users.id | Legacy candidate |
| data.full_name | string | users.full_name | Legacy candidate; API #4/#14 precedent |
| data.email | email | users.email | Legacy candidate; PII, Admin-only |
| data.role | UserRole | users.role | Legacy candidate string; enum members unresolved |
| data.avatar_url | uri? | users.avatar_url | Legacy candidate nullable; null/omit contract open |
| data.bio | string? | No source in legacy/current API #4/#14 | SOURCE_REQUIRED; do not synthesize |
| data.phone | string? | users.phone | Legacy candidate nullable; PII and null/omit semantics open |
| data.status | UserStatus | users.status | Legacy candidate string; enum members unresolved |
| data.created_at | date-time | users.created_at | Legacy candidate; serialize per API date-time convention |
| data.updated_at | date-time | users.updated_at | Legacy candidate; serialize per API date-time convention |
| meta | object | Envelope convention | Empty object candidate; no pagination for detail |
| traceId | uuid | Trace middleware convention | Current source-backed convention |
| password_hash | Excluded | Legacy users.password_hash | Never select or serialize |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #69 route/module/test | Current Study router/module/test search has no match | UNWIRED / NOT_FOUND | DD is design-only |
| Admin authorization | Catalog/AC-31 require Admin; current shared guard is Student-only | SOURCE_REQUIRED | Cannot specify current claim, permission or identity mapping |
| Schema | Legacy BIGINT users candidate differs from V1-PILOT UUID projections; live DB unverified | DISCREPANCY / SOURCE_REQUIRED | Candidate SQL is not runtime-ready |
| UserProfile.bio | Reusable schema has optional bio; legacy users and current #4/#14 projection lack it | SOURCE_REQUIRED | Do not invent or join UUID pilot profile |
| Enum/null rules | UserRole/UserStatus members and optional avatar/phone null-vs-omit semantics are unspecified | SOURCE_REQUIRED | Preserve contract types and open questions |
| Error envelope | Current helper emits data {} when data is absent; API guideline expects null | DISCREPANCY | Document current helper behavior without claiming #69 runtime behavior |
| AC-31 consistency | #68 direct list contract is ApiEnvelope<UserProfile> while AC-31 describes list + pagination | DISCREPANCY / MACRO_REVIEW_PENDING | #69 detail remains a single UserProfile; reconcile group only after #72 |

## CHANGES

- Files changed: apps/study-server/docs/dd/69_admin_user_detail/ (8 template sheets + 3 reports), this worklog, and .agents/worklog/2026-10-24/inventory-study-api-dd-counts.md.
- CONTEXT_UPDATES: None planned; no runtime, schema, catalog, diagram or convention changes.
- Context pages changed: None.
- Assumptions: Only the single-row legacy query shape and missing-row-to-404 branch are DERIVED candidates. Do not resolve live schema, Admin policy, enum values, bio or null semantics.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selector returned #48/#49/#50; all three files read in full. | VERIFIED |
| Project context and DD skill | Root instructions, context map, server-study router/index/workflow, createDD registry/skill and 8 registered templates loaded. | VERIFIED_STATIC_ONLY |
| Catalog and AC-31 diagram | #69 row and all AC-31 nodes/edges inspected. | VERIFIED_STATIC_ONLY |
| Source/schema/prior DD | Catalog, AC-31 nodes/edges, legacy and V1-PILOT schema artifacts, API #4/#14 projections, #68 DD, auth/error/middleware source reviewed. | VERIFIED_STATIC_ONLY |
| Template/API package | Exact 11-file manifest, 8/8 template front matters and appendix suffixes, direct contract/error set, UserProfile fields and safe SQL projection checked. | VERIFIED |
| Markdown/JSON/links | Two JSON examples parse; local links/anchors, table cell counts, fences and whitespace passed. | VERIFIED |
| Inventory | Refreshed after #69: 69 DD folders, 57 full packages, 34 missing; 12 source route/view pairs and 91 without. | VERIFIED_STATIC_ONLY |
| git diff --check | Final DD/report/worklog/inventory diff check; no diagnostics. | VERIFIED |
| Application tests | Not run; docs-only task. | NOT_RUN |

## HANDOFF

- Remaining blockers: Admin auth/permission, live schema choice, bio source, enum members, optional-field null rules and malformed path behavior remain open.
- Next owner/action: After #69 is statically verified, continue at API #70. Do not macro-review AC-31 until #72 DD exists.

