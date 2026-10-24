---
task_id: "2026-10-24-create-study-api68-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #68

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ catalog response; tách current source khỏi candidate; không map field assets chưa có source; Study chỉ giao Markdown.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Giữ discrepancy cây/list so với response đơn; không biến candidate thành contract; giữ exact error set và ghi source/schema gap.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Mỗi proposal phải có nhãn `DERIVED`; không tự tạo schema, enum, error code hoặc persistence; macro-review chỉ hoàn tất sau khi đủ nhóm API.
- shortage: `none`

## TASK_CLASSIFICATION

```text
primary_task_type: docs
secondary_task_types: []
project_scopes: [server-study]
cross_scope_dependencies: []
```

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD API tiếng Việt cho #68, lập plan và ma trận trước khi tạo thư mục DD, đọc kỹ diagram AC-31 và DD/API precedent, kiểm tra ngay sau khi authoring. Đây là API đầu của nhóm AC-31; macro-review #68–#72 chờ các DD cùng nhóm.
- Catalog #68: `GET /api/v1/admin/users`; Bearer JWT, role Admin; query `role?:string`, `status?:string`, `keyword?:string`, `page?:int32`; không khai báo body; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; direct response `ApiEnvelope<UserProfile>`; lỗi đúng 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`.
- AC-31: Admin đã đăng nhập/có quyền user management; màn hình gọi API danh sách; backend “Query users + pagination”; Admin chọn user hoặc thao tác; sau thao tác UI reload danh sách/chi tiết.
- Reusable `UserProfile`: `id:int64`, `full_name:string`, `email:email`, `role:UserRole`, optional `avatar_url:uri`, optional `bio:string`, optional `phone:string`, `status:UserStatus`, `created_at:date-time`, `updated_at:date-time`.

## CURRENT_BEHAVIOR

- Source/config: Không có route `GET /api/v1/admin/users`, module API #68 hoặc test API #68. `app/utils/auth.py` hiện có guard cho Student và không có Admin guard; path #68 không nằm trong `DESIGN_CONTRACT_PATHS`. Đây là nguồn hiện tại và không chứng minh endpoint behavior.
- Safe profile precedent: API #4 hiện đọc `users` theo ID và chỉ chọn `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`; không chọn `password_hash`. Model hiện tại không có `bio` và dùng `str` cho role/status, trong khi reusable schema dùng `UserRole`/`UserStatus` nhưng không liệt kê enum members. API #14 dùng lại model này.
- Schema: Legacy `infra/postgres/study-server/DB.sql` và `DB_UNICA_ERD.drawio` có `users.id BIGSERIAL`, `full_name`, `email`, `password_hash`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`. `DB_UNICA_TABLES.md` ghi trạng thái design-only. V1-PILOT `infra/postgres/02_study_db.sql` dùng `identity_projections`, `learner_profiles`, role assignment với UUID và không có bảng `users` tương đương; live schema chưa xác minh.
- Error infrastructure: Current helper thay `data` bị lược bằng `{}`; API guideline kỳ vọng `null`. Middleware chưa allowlist path #68; nếu sau này wire mà không cập nhật, lỗi validation/unhandled có thể rơi về business code fallback. Đây là discrepancy tích hợp có điều kiện, không phải runtime của #68.
- Runnable tests/runtime: Không có test API #68; docs-only, không chạy application tests.

## SOURCE_TRACE

```text
Admin Bearer principal -> xác thực Admin và quyền quản lý user (mechanism chưa có trong Study) -> nhận role/status/keyword/page -> Q1 đọc safe user projection + Q2 count cùng predicates (candidate từ legacy users) -> map UserProfile items và pagination candidate -> HTTP 200 hoặc exact catalog errors -> Admin chọn API #69/#70/#71/#72 -> reload danh sách
```

## PLAN BEFORE DD AUTHORING

1. Giữ nguyên endpoint, Admin Bearer, các query tùy chọn, success code, direct `ApiEnvelope<UserProfile>` và đúng 401/403/500. Không tự thêm body, query `size`, 404, 422 hay error/business code.
2. Đọc full AC-31 index và page trong `AC_04_ADMIN_MANAGEMENT.drawio`; giữ #68 list/query trước #69 detail, nhánh update/status/delete và reload. Không gộp behavior của #69–#72 vào API #68.
3. Ghi discrepancy: diagram mô tả “danh sách” và “pagination” nhưng catalog cùng diagram ghi response đơn `UserProfile`; request chỉ có `page`, không có `size`. Giữ direct response; trình bày candidate `Page<UserProfile>` riêng với nhãn `DERIVED`, chờ owner sửa contract trước implementation.
4. Với candidate để reviewer có phương án đơn giản: `role`/`status` exact-match; `keyword` trim + lowercase và tìm substring trong `full_name` hoặc `email`; page mặc định 1, kích thước cố định 20 theo precedent hiện hành API #07; thứ tự ổn định `users.id ASC`; Q2 count dùng cùng predicates. Đây là proposal `DERIVED`, chưa thành rule trực tiếp; không đặt whitelist enum cho role/status.
5. Chỉ dùng legacy `users` làm mapping candidate. Ghi riêng V1-PILOT UUID `identity_projections`/`learner_profiles`/role assignments và live schema chưa xác minh; không ghép hai schema.
6. Candidate response projection theo API #4/#14; không trả `password_hash`/credential. `bio` giữ optional contract nhưng `SOURCE_REQUIRED` vì thiếu cột/model/source trong current Study. Ghi email/phone là PII, yêu cầu Admin scope; không tự thêm audit table/log policy.
7. `07_table.md` là `N/A — READ-ONLY API`. Tạo 8 sheet template + `OPEN_QUESTIONS.md`, `PLAN_RESULT.md`, `VERIFICATION_REPORT.md` trong `68_admin_users_list`; không tạo ZIP, sửa runtime/schema/catalog/diagram.
8. Sau khi tạo, xác minh exact contract/error set, mọi UserProfile field, candidate-vs-direct boundary, filter/count/pagination coherence, không có credential leakage, 8/8 template appendix/front matter, JSON, links/anchors, tables, fences, whitespace, đủ 11 file và `git diff --check`.

### API Requirement Matrix

| API ID | Contract item | Giá trị | Basis/status |
|---|---|---|---|
| #68 | Method/path | `GET /api/v1/admin/users` | Catalog + AC-31; DIRECT |
| #68 | Actor/auth | Bearer JWT; role Admin | Catalog + AC-31 precondition; DIRECT requirement, runtime guard absent |
| #68 | Query | `role?:string`, `status?:string`, `keyword?:string`, `page?:int32` | Catalog; DIRECT |
| #68 | Body | Không khai báo | Catalog; DIRECT |
| #68 | Success | HTTP 200 `DESIGN_RESOURCE_RETRIEVED` | Catalog; DIRECT |
| #68 | Response | `ApiEnvelope<UserProfile>` | Catalog + diagram; DIRECT, conflicts with list/pagination purpose |
| #68 | Error | 401 `DESIGN_AUTHENTICATION_REQUIRED` | Catalog; DIRECT |
| #68 | Error | 403 `DESIGN_ACCESS_DENIED` | Catalog; DIRECT |
| #68 | Error | 500 `DESIGN_INTERNAL_ERROR` | Catalog; DIRECT |

### Request Usage Matrix

| Request item | Source/use | Query/response use | Rule/status |
|---|---|---|---|
| Authorization | Bearer JWT header | Candidate Admin identity/authorization | Admin guard/claim-to-role mapping `SOURCE_REQUIRED` |
| `role` | Optional query string | Candidate exact filter on legacy `users.role` | Filter presence DIRECT; semantics DERIVED; enum values unspecified |
| `status` | Optional query string | Candidate exact filter on legacy `users.status` | Filter presence DIRECT; semantics DERIVED; allowed values unspecified |
| `keyword` | Optional query string | Candidate substring over `full_name` or `email` | Presence DIRECT; trim/lowercase/OR fields DERIVED |
| `page` | Optional int32 query | Candidate 1-based page and offset | Presence/type DIRECT; default/minimum not stated; proposal default 1 DERIVED |
| Request body | None | None | DIRECT |
| `size`, `sort` | Not declared | No request mapping | Do not add to direct contract |

### Query Matrix

| Query | Type | Candidate source | Fields/predicate | Purpose/status |
|---|---|---|---|---|
| Q1 | SELECT | legacy `users AS u` | Safe profile projection: `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at` | Candidate list rows; no `password_hash`; no `bio` source |
| Q1 | WHERE | legacy `users AS u` | Optional `u.role = :role` | Exact equality DERIVED; no enum allowlist |
| Q1 | WHERE | legacy `users AS u` | Optional `u.status = :status` | Exact equality DERIVED; deletion visibility unresolved |
| Q1 | WHERE | legacy `users AS u` | Lowercase substring match against `u.full_name` OR `u.email` | DERIVED from `keyword` + UserProfile; escaping/collation needs confirmation |
| Q1 | ORDER | legacy `users AS u` | `u.id ASC` | Stable-order candidate DERIVED; no catalog sort parameter |
| Q1 | LIMIT/OFFSET | legacy `users AS u` | Fixed size 20; `(page - 1) * 20` | DERIVED precedent from API #07; contract has no `size` |
| Q2 | COUNT | legacy `users AS u` | Same optional role/status/keyword predicates as Q1 | Candidate total for PageMeta; only useful after response contract correction |
| N/A | JOIN | None | No join proposed | No related table needed in legacy candidate |

### Mutation Matrix

| Operation | Target | Condition | Fields | Status |
|---|---|---|---|---|
| None | N/A | GET is read-only | No INSERT/UPDATE/DELETE | `N/A — READ-ONLY API` |

### Response Source Matrix

| Response field/group | Direct/candidate type | Candidate source | Mapping/null rule | Evidence/status |
|---|---|---|---|---|
| Direct `data` | `UserProfile` object | Catalog reusable schema | Preserve direct contract | DIRECT; shape conflicts with list/pagination diagram |
| Candidate `data.items[]` | `UserProfile[]` | Q1 candidate | One safe profile per matching user | DERIVED; requires contract change |
| Candidate `data.pagination` | `PageMeta` | Q2 total + page config | `page`, fixed size 20, `total`, `total_pages` | DERIVED; requires response and page-size approval |
| `id` | int64 | legacy `users.id` | Direct candidate | BIGINT schema candidate; pilot UUID conflict |
| `full_name` | string | legacy `users.full_name` | Direct candidate | API #4/#14 safe projection precedent |
| `email` | email | legacy `users.email` | Direct candidate; restricted to Admin | PII; direct schema candidate |
| `role` | UserRole | legacy `users.role` | Direct candidate; exact stored value | Catalog enum members unresolved; API #4 runtime model uses str |
| `avatar_url` | uri? | legacy `users.avatar_url` | Reuse API #4 null serialization as candidate | Optional/null semantics unresolved |
| `bio` | string? | No current source | Do not fabricate; omit only if response owner approves | SOURCE_REQUIRED; pilot learner_profiles has separate UUID model |
| `phone` | string? | legacy `users.phone` | Reuse API #4 null serialization as candidate | PII; optional/null semantics unresolved |
| `status` | UserStatus | legacy `users.status` | Direct candidate | Catalog enum members unresolved; API #4 runtime model uses str |
| `created_at`, `updated_at` | date-time | legacy `users` timestamps | ISO-8601 candidate mapping | Legacy DDL candidate; live schema unknown |
| `password_hash` | Excluded | legacy `users.password_hash` | Never select or serialize | Security invariant from source/API #4 precedent |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Response cardinality | Catalog/diagram say `ApiEnvelope<UserProfile>`; AC-31 action is list and backend step says query + pagination | `DISCREPANCY` | Preserve direct shape; Page proposal is `DERIVED` and requires contract correction |
| Pagination input | Only `page` is declared; no size/default/minimum; response direct shape has no PageMeta | `DISCREPANCY / DERIVED` | Fixed size 20/page 1 proposal requires approval; malformed-page behavior has no catalog 422 |
| User schema | Legacy BIGINT `users` vs V1-PILOT UUID identity/profile/role tables | `DISCREPANCY / SOURCE_REQUIRED` | No single approved executable query; live schema not verified |
| Admin authorization | Contract requires Admin; current guard is Student-only, no Admin helper | `UNWIRED / SOURCE_REQUIRED` | Do not claim current authorization behavior |
| `bio` field | Reusable UserProfile includes optional bio; legacy users and current API #4 model lack it | `DISCREPANCY / SOURCE_REQUIRED` | Keep field optional in direct contract, do not fabricate a value |
| Role/status type | Reusable schema uses UserRole/UserStatus without enum member lists; current API #4 model exposes strings | `DISCREPANCY / SOURCE_REQUIRED` | Do not invent enum values or claim an implementation mapping |
| Filters | Query keys are direct; enum values, keyword fields/normalization and deleted-user policy absent | `DIRECT + DERIVED / SOURCE_REQUIRED` | Candidate semantics need owner approval |
| Error handling | Catalog permits only 401/403/500; current error helper uses `{}` for omitted data, guideline expects null; middleware path not allowlisted | `DISCREPANCY / conditional future wiring` | Do not add codes; reconcile before runtime wiring |
| PII | UserProfile exposes email and optional phone | `DIRECT / security review required` | Require Admin-only authorization; never expose password hash |

## CHANGES

- Files changed: `apps/study-server/docs/dd/68_admin_users_list/` (8 sheets + 3 reports); this worklog; `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md` refreshed after #68.
- CONTEXT_UPDATES: None; no source/schema/catalog/diagram or context page/manifest was changed. Existing user edits and prior untracked DDs were preserved.
- Assumptions: Candidate filter/pagination behavior is explicitly `DERIVED`; catalog shape and exact errors stay direct.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Worklog preflight | Selector chose #48/#49/#50; all three read in full; no shortage. | VERIFIED |
| Catalog/AC-31/DB ERD | Exact #68 row, full AC-31 page/index and users entity in DB ERD inspected. | VERIFIED_STATIC_ONLY |
| Current route/auth/tests | No route, API #68 module/test or Admin guard; middleware allowlist excludes path. | VERIFIED_STATIC_ONLY |
| Schema/profile precedent | Legacy DDL/ERD and pilot schema compared; API #4/#14 projection and API #07 pagination precedent inspected; UserRole/UserStatus types and missing enum members recorded. | VERIFIED_STATIC_ONLY |
| Plan-before-authoring | Requirement, request, query, mutation and response-source matrices recorded here before DD folder creation. | VERIFIED |
| DD package/template | Exact 11-file set; all 8 front matters and template appendix suffixes match byte-for-byte. | VERIFIED |
| Contract/response/errors | Exact endpoint/query/direct response/success/error set checked; all UserProfile fields including UserRole/UserStatus recorded; no 404/422 added. | VERIFIED_STATIC_ONLY |
| Markdown/JSON/links | JSON parsed; internal links/anchors, tables, fences and whitespace passed. | VERIFIED |
| Inventory refresh | 68 DD folders/core packages; 56 full packages; 35 missing; 12 route+view pairs and 91 without pair. | VERIFIED_STATIC_ONLY |
| AC-31 macro-review | Pending until #69–#72 DDs exist; no premature group-completion claim. | PENDING_GROUP |
| `git diff --check` | Chạy sau final update report/worklog/inventory; không có diagnostics. | VERIFIED |
| Runtime tests | Not run; docs-only. | NOT_RUN |
| Context validator | Not run; no `.agents/server-study` context page or registry was changed. | NOT_APPLICABLE |

## HANDOFF

- Remaining blockers: contract cardinality, page defaults/size/validation, Admin identity/guard, live schema, UserRole/UserStatus enum members, `bio` source and PII visibility need approval before implementation.
- Next API DD: #69; keep AC-31 group macro-review pending until #68–#72 are all present.
