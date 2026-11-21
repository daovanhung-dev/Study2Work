---
task_id: "2026-10-24-complete-study-api03-dd-package"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Hoàn thiện package DD Study API #03 — Đăng nhập

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
  - path: `.agents/worklog/2026-10-24/complete-study-api01-dd-package.md`
    - carry_forward: Tách AC expected khỏi source hiện tại; API #01/#02 có discrepancy xác minh email và không sửa DD ngoài một API mỗi phiên.
  - path: `.agents/worklog/2026-10-24/complete-study-api02-dd-package.md`
    - carry_forward: DD Study gồm 8 sheet lõi và 3 report; giữ catalog làm contract chuẩn, static checks không thay cho runtime tests.
  - path: `.agents/worklog/2026-10-24/create-study-api100-dd.md`
    - carry_forward: Chỉ ghi field/side effect có nguồn; giữ `UNWIRED`, `SOURCE_REQUIRED`, discrepancy; output Markdown-only.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện riêng package Markdown API #03, ghi rõ expected/current discrepancy và rà điểm nối AC-02 sang API #04.
- Catalog: public `POST /api/v1/auth/login`; body `{email:email!, password:string!}`; response `ApiEnvelope<UserProfile>`; HTTP 201 `DESIGN_RESOURCE_CREATED`; errors chỉ 422 `DESIGN_VALIDATION_ERROR` và 500 `DESIGN_INTERNAL_ERROR`.
- AC-02: login thành công cấp access/refresh token; sai thông tin trả 401, tài khoản khóa trả 403; client tiếp tục gọi `GET /api/v1/users/me`; sau đó lưu session và điều hướng theo role.
- Deliverables: giữ 8 sheet lõi; thêm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không tạo ZIP theo workflow Study Server.

## CURRENT_BEHAVIOR

- Router: `app/api/v1.py` khai báo login public, route HTTP 200, gọi module #03; cùng module còn khai báo `POST /api/v1/auth/refresh` nhưng catalog/diagram không có API ID riêng cho route này.
- Login source: normalize email (trim/validate, max 255), từ chối password chỉ có whitespace; đọc `users`; sai email/password trả 401; status khác `ACTIVE` trả 403; phát hành JWT access và opaque refresh token; chỉ lưu HMAC-SHA256 hash của refresh token vào `refresh_tokens`; commit rồi trả profile cộng token fields với HTTP 200 `DESIGN_RESOURCE_RETRIEVED`.
- Refresh source: kiểm tra hash, trạng thái revoked/expiry và user ACTIVE; rotate token trong transaction. Route hiện tại là source-only/unlisted, không nhập vào contract API #03.
- Candidate DDL: `infra/postgres/study-server/DB.sql` có `users` và `refresh_tokens`; đây là artifact trong repo, không chứng minh schema live.
- Tests: test source của module bao phủ login/refresh, validation, 401/403, persistence/rotation và HTTP behavior; đã đọc, không chạy trong docs task.

## SOURCE_TRACE

```text
POST /api/v1/auth/login -> LoginRequest/FastAPI validation -> login view -> normalize email -> SELECT users -> verify password/status -> issue access/refresh -> INSERT hashed refresh token + commit -> HTTP 200 envelope(profile + token fields) -> API #03 tests (read only, not run)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Success response/status | Catalog: 201 `DESIGN_RESOURCE_CREATED`, UserProfile only. AC-02/current source: 200; current source adds token fields. | `DISCREPANCY` | Giữ catalog làm normative contract; ghi current source riêng. |
| Authentication errors | Catalog chỉ có 422/500; AC-02 và source có 401/403. | `DISCREPANCY` | Chưa tự mở rộng approved error set. |
| Session persistence | Catalog không đặc tả token/session; source insert hash vào `refresh_tokens`, DDL chỉ là candidate. | `SOURCE_BACKED / SOURCE_REQUIRED` | Không tuyên bố live schema hay quyết định retention/rotation policy. |
| Undeclared refresh route | Router/source có `/auth/refresh`, catalog/diagram không có endpoint row riêng. | `UNWIRED_CONTRACT / SOURCE_BACKED` | Không gộp refresh thành hành vi normative của login. |
| API #03 → #04 | AC-02 nói login rồi gọi `/users/me`; current login đã trả profile. #04 source nhận JWT claims `sub` + `roles`, Student-only. | `GROUP_OPEN_QUESTION` | Cần xác nhận profile retrieval có chủ ý lặp và claims/role wording. |
| Profile field | Catalog UserProfile có optional `bio`; #03 query/response không có bio. | `DISCREPANCY` | Không bịa cột/giá trị. |

## PLAN BEFORE REPORT AUTHORING

1. Giữ nguyên catalog method/path/auth/request/response/status/error set như expected contract; không biến current source thành approved contract.
2. Bổ sung ba report chuẩn bằng tiếng Việt; ghi câu hỏi về response token, status/error set, route refresh, limits/normalization, active-status rule, refresh-token persistence/rotation, `bio`, và AC-02 handoff sang #04.
3. Cập nhật tối thiểu `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md` để phân biệt contract catalog và source hiện tại; sửa source links hỏng đã ghi nhận.
4. Không sửa API #04, runtime, tests, schema, catalog, diagram hoặc client. Không chạy application tests.
5. Static verify manifest 11 file, 8 front matter/template appendix parity, exact catalog contract/error set, JSON examples, links/anchors, table widths, fences, newline/whitespace, fingerprint và `git diff --check`; recount inventory.

## CHANGES

- Files changed: API #03 `02_Overview.md`, `03_Request.md`, `04_Response.md`, `05_Data_Mapping.md`, `06_Error.md`, `07_table.md`, `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; inventory worklog. Không sửa `00_Cover.md`, `01_Lich_su.md`, API #04 hoặc runtime.
- CONTEXT_UPDATES: Không đổi source/contract/registry; không cần context validator.
- Context pages changed: None planned.
- Assumptions: AC-02 vẫn là expected flow; catalog là contract normative; DDL chỉ là candidate; route refresh chưa có catalog ID riêng. `07_table.md` ghi current login INSERT và tách refresh-only UPDATE.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Preflight/context | Root router, context map, Study scope/workflow, manifest skill wiring và ba docs worklogs đã được review. | VERIFIED_STATIC_ONLY |
| Current source/contract | Catalog, AC-02 diagram, #03 source/test, candidate DDL và nhóm #04 được đối chiếu. | VERIFIED_STATIC_ONLY |
| Package manifest/front matter | 11/11 Markdown files; 8/8 sheet front matter and workbook-source appendix structure. | VERIFIED_STATIC_ONLY |
| Contract and examples | Catalog #03 method/path/request/response/status/error set preserved; 4 JSON examples parse. | VERIFIED_STATIC_ONLY |
| Links/tables/hygiene | 42 local links resolve; 35 tables/453 rows consistent; fences balanced; no trailing whitespace; all files end in newline. | PASS |
| Fingerprints | Template `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; output `c88270b0c62420e16fcff5ca7248c72dea209e52b27016ea400b25feb693ab9d`. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No diagnostics for tracked changes in the API #03 folder/worklog. | PASS |
| Inventory postflight | 103/103 folders and core DDs; 94 full 11-file packages; #04–#12 report-incomplete (9); source route+view 12/103, without pair 91. | VERIFIED_STATIC_ONLY |
| Application tests/runtime | Tests not run; no runtime/live DB/deployment claim. | NOT_RUN |

## HANDOFF

- Remaining blockers: Owner cần quyết định các câu hỏi trong `OPEN_QUESTIONS.md`; không suy đoán để đóng discrepancy.
- Next action: Tiếp tục API #04 trong phiên riêng; macro-review AC-02 khi #04 được hoàn thiện.
