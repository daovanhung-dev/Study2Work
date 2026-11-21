---
task_id: "2026-10-24-create-study-api70-dd"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD Study API #70

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-24/create-study-api48-dd.md`
    - carry_forward: Contract trực tiếp phải tách khỏi phần `DERIVED`; không invent bảng, cột, enum hoặc policy.
  - path: `.agents/worklog/2026-10-24/create-study-api49-dd.md`
    - carry_forward: AC intent không thay thế response contract; giữ source/schema gaps và runtime `UNWIRED` riêng.
  - path: `.agents/worklog/2026-10-24/create-study-api50-dd.md`
    - carry_forward: Lập requirement/request/query/mutation/response matrices trước authoring; gói Study là Markdown, không ZIP.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo một DD Markdown tiếng Việt cho API #70; mỗi lượt chỉ xử lý một API; ghi plan và ma trận trước khi tạo DD; kiểm tra tĩnh ngay sau authoring.
- Canonical contract: `docs/lists/list_api.md` row #70 và AC-31 diagram. Manifest wire `createDD-markdown` cho `server-study`; workflow Study yêu cầu Markdown, không ZIP.
- Direct contract: `PUT /api/v1/admin/users/{user_id}`; Bearer JWT, role Admin; path `user_id:int64!`; response `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500 với các mã `DESIGN_*` trong catalog.
- Direct body: catalog và diagram chỉ khai báo path input; request body chưa được đặc tả. Không biến việc thiếu body schema thành khẳng định “không có body”.

## CURRENT_BEHAVIOR

- Pre-authoring inventory: catalog có 103 endpoint ID liên tục #01–#103; DD có 69 folder #01–#69, 69 đủ 8 sheet chính theo prefix, 57 đủ thêm ba report chuẩn; #70–#103 chưa có folder.
- Source: Không có route/module API #70 hoặc Admin user route hiện hành. `app/api/v1.py` và `app/modules/**/view.py` chỉ có cặp cho #01–#09, #12–#14. Đếm 12 API có route+view source, 91 chưa có cặp; đây không phải kết luận runtime pass.
- Auth: `app/utils/auth.py` hiện xác thực Student; chưa thấy Admin guard hoặc policy quyền quản lý user. Không tái sử dụng Student auth cho #70.
- Existing precedent: API #14 cập nhật `full_name`, `phone`, `avatar_url`; query hiện tại không cập nhật `role` hoặc `bio`. Đây là precedent source, không phải contract của #70.
- Schema: `infra/postgres/study-server/DB.sql` là legacy candidate, khai báo `users.id`, `full_name`, `email`, `password_hash`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`; không có `bio`/audit/delete columns. DB guide đánh dấu `DESIGN_ONLY`; live schema chưa verify. V1-PILOT dùng UUID projections/roles và không được trộn với legacy `users`.
- API #70 runtime: route, view, focused test chưa có; trạng thái `UNWIRED / NOT_FOUND`.
- Runnable tests: Không chạy application tests cho docs-only work.

## SOURCE_TRACE

```text
AC-31 Admin mở detail (#69) -> chọn Update -> PUT #70 -> update user/profile -> reload list/detail
```

- Diagram không gán cho #70 status update, delete, hoặc revoke session; #71 sở hữu status transition.
- `users` UPDATE/RETURNING là phương án persistence `DERIVED CANDIDATE` dựa trên legacy DDL và API #14; không phải implementation hiện hành.

## PREAUTHORING_PLAN_AND_MATRICES

| Matrix | Direct/verified source | Proposed handling before authoring |
|---|---|---|
| API Requirement | Catalog row #70; AC-31: Admin chọn Update, cập nhật user/profile rồi reload list/detail. | Giữ PUT/path/auth/response/errors đúng contract; giới hạn #70 ở profile và role, không nhận status/delete/session behavior. |
| Request Usage | Direct input chỉ có `path{user_id:int64!}`; body chưa đặc tả. API #14 source hiện nhận `full_name`, `phone`, `avatar_url`; tên API #70 có “thông tin/role”. | Body schema ghi `SOURCE_REQUIRED`; nêu candidate `full_name`, `phone`, `avatar_url`, `role` là `DERIVED`, không khẳng định requiredness/nullability/enum. Không thêm `bio`, email, status, id hoặc credential làm writable fields. |
| Query | Không có query/API #70 source. Legacy candidate có `users.id` và các cột profile/role nêu trên. | Ghi một `UPDATE ... WHERE id=:user_id ... RETURNING` chỉ là `DERIVED CANDIDATE`; dùng allowlist response an toàn; không đọc/trả `password_hash`. Live schema chưa verify. |
| Mutation | AC-31 nói update user/profile; #71 riêng cho status. API #14 source chỉ update `full_name`, `phone`, `avatar_url`, `updated_at`. | Candidate mutable allowlist: `full_name`, `phone`, `avatar_url`, `role`; `updated_at` do server cập nhật. Không tự thêm audit log, role policy, session revoke, bio persistence, status, delete. |
| Response Source | Catalog trả `ApiEnvelope<UserProfile>`; `UserProfile` tái sử dụng có `id`, `full_name`, `email`, `role`, `avatar_url?`, `bio?`, `phone?`, `status`, `created_at`, `updated_at`. | Giữ envelope và allowlist fields; enum values/null semantics cần owner/source xác nhận. `bio` hiện không có persistence source; đánh dấu gap thay vì trả giá trị giả. |

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Request body | Catalog/diagram chỉ nêu path; API title/AC mô tả update thông tin và role. | `SOURCE_REQUIRED` with `DERIVED` candidate | DD không được trình bày body fields như contract đã duyệt. |
| Admin authorization | Contract yêu cầu Admin; current auth helper là Student-only; chưa có Admin policy. | `UNWIRED / SOURCE_REQUIRED` | Implementation cần policy/permission source trước khi readiness. |
| Persistence schema | Legacy DDL có role/profile fields nhưng DB context `DESIGN_ONLY`; live schema chưa xác minh. | `DERIVED CANDIDATE / SOURCE_REQUIRED` | Query chỉ là candidate; không claim deployable schema. |
| `bio` | Reusable UserProfile có `bio?`, nhưng legacy users DDL và API #14 query không persist bio. | `DISCREPANCY` | Không thêm bio vào mutation/query cho tới khi có schema/contract nguồn. |
| Role values and side effects | `UserRole` members, permission policy, audit, and token/session effect chưa được xác định cho #70; diagram chỉ nhắc revoke session ở #71. | `SOURCE_REQUIRED` | Không invent enum values, audit behavior, or session revocation. |
| Error envelope/middleware | #70 chưa có route; current middleware allowlist không có path này; shared error helper fallback may differ from null-data guideline. | `UNWIRED / INFRASTRUCTURE GAP` | Chỉ ghi contract trực tiếp; không mô tả đó là current #70 runtime behavior. |

## AUTHORING_PLAN

1. Tạo đúng 8 sheet template và 3 report chuẩn trong `apps/study-server/docs/dd/70_admin_user_update/`.
2. Giữ các trường catalog/diagram là direct contract; đánh dấu từng phương án body/query/mutation suy ra là `DERIVED`; các quyết định thiếu nguồn là `SOURCE_REQUIRED` hoặc `Draft — Needs Confirmation`.
3. Chép nguyên văn phụ lục đối chiếu nguồn từ template vào từng sheet core; không tạo ZIP.
4. Chạy kiểm tra tĩnh: exact 11-file manifest, template suffix match, contract/error codes, labels, links/anchors, Markdown fences/tables/whitespace, JSON khi có, và `git diff --check`. Không chạy app tests.
5. Sau khi DD tĩnh đạt, cập nhật inventory API DD hiện tại từ 69/34 sang 70/33; số API có route+view vẫn 12/91; để AC-31 macro-review pending đến khi #72 tồn tại.

## CHANGES

- Files changed: `apps/study-server/docs/dd/70_admin_user_update/` (8 core sheets + 3 reports), `.agents/worklog/2026-10-24/create-study-api70-dd.md`, `.agents/worklog/2026-10-24/inventory-study-api-dd-counts.md`. Plan and matrices were recorded before creating the DD folder.
- CONTEXT_UPDATES: None planned; source/router/schema contract is not being changed.
- Context pages changed: None.
- Assumptions: Any body/query/mutation design beyond the direct catalog/diagram is visibly tagged `DERIVED`; missing requiredness, nullability, enums, permissions and side effects remain open/source-required.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| Project classification | `docs`, scope `server-study`, no cross-scope dependency. | `VERIFIED` |
| Context and skill routing | Root router, `.agents/AGENTS.md`, `.agents/context-map.md`, server-study scope, manifest and `createDD-markdown` resources loaded. | `VERIFIED` |
| Worklog preflight | Selector returned #48/#49/#50; all three selected worklogs read in full. | `VERIFIED` |
| Catalog/DD counts | Post-authoring: 103 endpoint rows; 70 DD folders with core sheets; 58 full 11-file packages; 33 IDs without a DD. | `VERIFIED_STATIC_ONLY` |
| Router/module inventory | #01–#09 and #12–#14 have router ID plus matching `view.py`; #70 has no route/module/test. | `VERIFIED_STATIC_ONLY` |
| Source and diagram trace | API #14 current profile mutation, legacy DDL, AC-31 #70 intent, and API #71 boundary reviewed. | `VERIFIED_STATIC_ONLY` |
| DD static package checks | Exact 11 files; 8/8 template appendix matches; direct contract/error set; JSON, links/anchors, tables and fences passed; `git diff --check` clean. | `VERIFIED_STATIC_ONLY` |
| Application tests | Not run because this task is docs-only. | `NOT_RUN_BY_SCOPE` |

## HANDOFF

- Remaining blockers: Owner confirmation is still needed for exact request body and field semantics, Admin permission policy, role enum, live DB schema, audit/token effects, and bio persistence.
- Next owner/action: Continue with only API #71; keep AC-31 macro-review pending until #72 exists.
