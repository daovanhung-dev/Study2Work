---
task_id: "2026-10-24-create-study-api71-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #71

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` (Node không có trong PATH)
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Giữ direct contract riêng với candidate; source/runtime và schema là các lớp evidence khác nhau.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: Đọc cả diagram AC trước khi chốt luồng; ranh giới API và enum/schema gap phải ghi rõ.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Giữ đúng package Markdown 8 sheet + 3 report, matrices trước authoring; label `DERIVED`/`SOURCE_REQUIRED` và không tạo ZIP.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown tiếng Việt cho đúng API #71 trong phiên này; lập plan trước khi tạo folder DD; kiểm tra ngay sau authoring; AC-31 macro-review chờ khi #72 tồn tại.
- Canonical contract: `docs/lists/list_api.md` row #71; AC-31 index/page trong `AC_04_ADMIN_MANAGEMENT.drawio`; reusable `ApiEnvelope<UserProfile>`; registered skill `createDD-markdown`; Study workflow Markdown-only.
- Direct contract: `PATCH /api/v1/admin/users/{user_id}/status`; Bearer JWT, role Admin; path `user_id:int64!`; `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_UPDATED`; 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- Direct request body: Không được khai báo trong catalog hoặc diagram; không kết luận API cấm body.
- AC-31 flow: Admin chọn thao tác STATUS → API #71 → “UPDATE account status; revoke session nếu cần” → reload danh sách/chi tiết. Session revoke là điều kiện cần xác nhận, không phải side effect bắt buộc đã khóa.

## CURRENT_BEHAVIOR

- Inventory trước task: 103 endpoint IDs; 70 DD folders #01–#70, 58 đủ gói 11 file; #71–#103 chưa có DD. Router+matching `view.py` source pairs hiện là #01–#09, #12–#14 (12 API); 91 chưa có cặp.
- Runtime: Không có route, module hoặc test API #71; `UNWIRED / NOT_FOUND`. Router hiện chỉ khai báo API IDs #01–#09, #12–#14.
- Authentication: shared `validate_current_user_request` kiểm tra Bearer/JWT và role Student; chưa có Admin guard/policy cho AC-31.
- Legacy DB candidate: `users.status VARCHAR(20) DEFAULT 'ACTIVE'`; `refresh_tokens` có `user_id`, `revoked_at`, expiry. DDL là candidate, live schema chưa xác minh.
- V1-PILOT artifact: `account_status` enum có `ACTIVE`, `SUSPENDED`, `DELETION_PENDING`, `ANONYMIZED`, nhưng UUID `identity_projections` khác legacy BIGINT `users`; không trộn hai schema. `ACTIVE`/`SUSPENDED` chỉ là candidate values cho khóa/mở khóa.
- Existing session behavior: API #3 login từ chối user có status khác `ACTIVE`; refresh query đọc status và refresh flow cũng từ chối user không `ACTIVE`. API #3 hiện revoke refresh token theo token ID. Access JWT guard hiện kiểm tra token claims/roles nhưng không truy vấn account status hoặc session revocation; thay status/revoke refresh token không chứng minh thu hồi ngay access JWT đang sống.
- Error/runtime integration: `error_response` chuyển absent `data` thành `{}`; scope guideline yêu cầu `data:null`. `DESIGN_CONTRACT_PATHS` chưa có API #71 path; route chưa wired nên đây là infrastructure gap, không phải API #71 runtime behavior.
- Runnable tests: Không có test API #71; không chạy application tests cho docs-only task.

## SOURCE_TRACE

```text
AC-31 Admin mở list (#68) -> chọn user/detail (#69) -> chọn STATUS -> PATCH #71 -> cập nhật account status -> có thể revoke session nếu policy yêu cầu -> reload list/detail
```

- API #70 là profile/role update; #71 chỉ sở hữu account status; #72 sở hữu soft-delete/anonymize.
- Current login/refresh checks show `ACTIVE` is required to begin/refresh a session. Current access-token helper does not check current account status.
- Candidate: status `SUSPENDED` khi khóa thì revoke active refresh-token rows; candidate revocation không invalidate access JWT đã phát hành. Mọi chi tiết body/state/revocation chưa được catalog đặc tả và phải gắn `DERIVED`.

## PREAUTHORING_PLAN_AND_MATRICES

| Matrix | Direct/current evidence | Proposed handling before authoring |
|---|---|---|
| API Requirement | Catalog: PATCH path, Admin Bearer, path int64, UserProfile response, exact 200/errors. Diagram: STATUS branch updates account status, conditional session revoke, then reload list/detail. | Giữ nguyên direct contract; không kéo profile/role edit từ #70 hoặc delete/anonymize từ #72 vào #71. |
| Request Usage | Direct input chỉ có `path{user_id:int64!}`. Body chưa được nêu. Endpoint `/status` và diagram cho phép suy ra target status field. | Ghi body candidate `{status:UserStatus!}` là `DERIVED`; candidate lock/unlock values `SUSPENDED`/`ACTIVE` có nguồn gợi ý trong V1-PILOT `account_status`, nhưng `UserStatus` contract members còn `SOURCE_REQUIRED`. |
| Query | Không có API #71 source. Legacy users status column exists only in DDL candidate. Refresh token source/query supports `revoked_at`, expiry and user association. | Q1 candidate UPDATE users.status by user ID and RETURNING safe UserProfile fields. Q2 conditional candidate revoke unrevoked, unexpired refresh-token rows on suspend; explicitly not a current query and not access-JWT revocation. |
| Mutation | Diagram direct intent updates account status; conditional “revoke session nếu cần”. Current API #3 revokes one refresh token by token ID and checks account ACTIVE. | M1 status mutation is `DERIVED` on legacy users. M2 all-user refresh-token revocation on suspend is optional `DERIVED` candidate; unlocking does not reactivate revoked refresh tokens. No audit/self-lock/other status transitions invented. |
| Response Source | Catalog output is UserProfile. Current API #4 model has id, profile, role, status, timestamps; profile queries use legacy users safe projection. | Return updated status in `data.status`, preserve other profile fields via candidate safe projection; `bio` has no source; optional null/omit and enum values remain open. |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Body schema/status values | Catalog/diagram omit body; `UserStatus` members are not listed. | `SOURCE_REQUIRED`; `{status}` and ACTIVE/SUSPENDED are `DERIVED` candidates | Candidate JSON cannot be treated as approved contract. |
| Status schema | Legacy users status is VARCHAR with ACTIVE default; V1-PILOT account_status is enum with ACTIVE/SUSPENDED and additional lifecycle states. | `DISCREPANCY / SOURCE_REQUIRED` | Keep model separation; confirm selected live schema and legal status transitions. |
| Session revocation | Diagram says “revoke session nếu cần”; current legacy refresh_tokens supports `revoked_at`, while access JWT guard has no DB status/revocation check. | `DERIVED / SOURCE_REQUIRED` | Proposed refresh-token revocation does not promise immediate access-token invalidation. |
| Admin authorization | Catalog/AC require Admin; current shared guard is Student-only and no Admin policy source exists. | `UNWIRED / SOURCE_REQUIRED` | Route cannot be called implementation-ready. |
| Runtime/API tests | No API #71 route/module/test. | `UNWIRED / NOT_FOUND` | DD only; no runtime claims. |
| Error envelope/path allowlist | Shared helper defaults data `{}`; guideline expects null; contract path absent from middleware allowlist. | `DISCREPANCY / CONDITIONAL_FUTURE_WIRING` | Record integration risks without describing them as endpoint behavior. |
| Status vs deletion | #71 changes account status; #72 soft-delete/anonymize by policy. | `DIRECT BOUNDARY` | Keep terminal deletion/anonymization out of #71. |

## AUTHORING_PLAN

1. Tạo đúng 8 core sheets và 3 reports tại `apps/study-server/docs/dd/71_admin_user_status/`.
2. Ghi direct contract nguyên trạng; body `{status}`, ACTIVE/SUSPENDED và refresh-token revoke là candidate `DERIVED`, còn allowed statuses, Admin policy, access-JWT invalidation và no-op semantics là `SOURCE_REQUIRED`/open.
3. Dùng API #68–#70 làm AC-31 liên quan; giữ list/detail/profile/status/delete boundaries riêng. Không kết luận group macro-review trước khi #72 tồn tại.
4. Chép nguyên appendix từ tám registered templates; không tạo ZIP.
5. Static verify exact 11-file manifest, template tails, catalog contract/error codes, body labels, session behavior boundary, JSON, links/anchors, table/fence/whitespace; chạy `git diff --check`. Không chạy app tests.
6. Sau khi DD đạt kiểm tra, cập nhật inventory lên 71 DD/32 thiếu; source wiring vẫn 12/91; cập nhật worklog/report với AC-31 macro-review `PENDING_GROUP` đến #72.

## CHANGES

- Files changed: `apps/study-server/docs/dd/71_admin_user_status/` (8 core sheets + 3 reports), `.agents/worklog/2026-10-24/create-study-api71-dd.md`, `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`. Requirement/plan/matrices were recorded before DD folder creation.
- CONTEXT_UPDATES: None planned; no route/schema/catalog/diagram change.
- Context pages changed: None.
- Assumptions: Chỉ dùng `ACTIVE`/`SUSPENDED` làm candidate lock/unlock do tên use case, login guard và pilot enum; không coi enum pilot là legacy UserStatus contract. Refresh-token revoke được đề xuất khi khóa, nhưng full session revocation chưa đạt vì current access JWT path không kiểm tra status/revocation.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Project classification | `docs`, scope `server-study`, no cross-scope dependency. | `VERIFIED` |
| Context and skill routing | Root/context-map, server-study pages, worklog contract, manifest skill wiring loaded. | `VERIFIED` |
| Worklog preflight | Deno selector returned #48/#49/#50; all three read in full. | `VERIFIED` |
| AC-31/source trace | Catalog row #71, AC-31 nodes/edges, API #3 session lifecycle, auth helper and legacy/pilot status evidence reviewed. | `VERIFIED_STATIC_ONLY` |
| Current API #71 source/test | No route/module/test found; route inventory checked. | `VERIFIED_STATIC_ONLY` |
| Plan before DD folder | Requirement, request, query, mutation and response-source matrices recorded here. | `COMPLETE` |
| DD static package checks | Exact 11-file manifest; 8/8 template tails; contract/error set; candidate boundaries; JSON, links/anchors, tables/fences/whitespace and `git diff --check` passed. | `VERIFIED_STATIC_ONLY` |
| Post-authoring inventory | 71/103 DDs, 59 full packages, 32 missing; route+view remains 12/103 and 91 without pair. | `VERIFIED_STATIC_ONLY` |
| Application tests | Not run; docs-only. | `NOT_RUN_BY_SCOPE` |

## HANDOFF

- Remaining blockers: Confirm request body/`UserStatus` values, live schema, Admin guard, exact session revocation requirement and handling of already-issued access JWTs.
- Next owner/action: Create only DD #72, then macro-review AC-31 APIs #68–#72 as one connected group.
