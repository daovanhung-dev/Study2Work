---
task_id: "2026-10-24-complete-study-api04-dd-package"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Hoàn thiện package DD Study API #04 — Lấy hồ sơ hiện tại

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
    - carry_forward: Giữ catalog làm expected contract; AC/source khác nhau phải có discrepancy; một API được author trong mỗi phiên.
  - path: `.agents/worklog/2026-10-24/complete-study-api02-dd-package.md`
    - carry_forward: Study output là 8 sheet + 3 report, Markdown-only; source presence không đồng nghĩa runtime verification.
  - path: `.agents/worklog/2026-10-24/complete-study-api03-dd-package.md`
    - carry_forward: API #03 vừa được source-review; access token hiện dùng `sub` + `roles`, AC-02 diagram ghi `user_id` + `role`; macro-review #03→#04 cần giữ khác biệt response/token và lần fetch profile.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện riêng package API #04, ghi tiếng Việt, source-aware, review AC-02 và AC-11; sau khi có #04 thực hiện macro-review nhóm #03/#04 và #04/#13/#14.
- Catalog: `GET /api/v1/users/me`; Bearer JWT, role Student; `ApiEnvelope<UserProfile>`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; errors `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED`, `500 DESIGN_INTERNAL_ERROR`. Input notation lặp `auth{bearer_jwt!}` hai lần; route/diagram thể hiện một Authorization header.
- AC-02: sau login, gọi #04 để đọc profile/role/permissions, lưu session và điều hướng theo role. Diagram nêu claim `user_id`, `role`; API response status 200 và error branches 401/403/500.
- AC-11: GET hồ sơ hiện tại → UI cho sửa → #13 upload avatar → #14 cập nhật profile bằng URL avatar → reload/hiển thị profile.
- Deliverables: giữ 8 sheet #04; thêm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không tạo ZIP.

## CURRENT_BEHAVIOR

- Router: GET `/users/me`, header `Authorization` optional ở tầng FastAPI để view ánh xạ missing/malformed sang 401; inject DB Session và trace ID; success status 200.
- Auth: `validate_current_user_request` parse Bearer; `decode_access_token` kiểm tra chữ ký/algorithm/issuer/audience, type và JWT claims; `validate_access_claims` lấy positive numeric `sub`, list `roles`, normalize uppercase; yêu cầu `STUDENT` có mặt trong roles. Claim thiếu/sai trả 401; không có Student trả 403; lỗi config decode có thể trả 500.
- Query: SELECT `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at` từ `users` theo `id=:user_id`; không đọc password hash, không lọc status, không mutation. User không có row trả 401; SQLAlchemy error rollback rồi 500; model mapping lỗi trả 500.
- Response: `UserProfile` source model không có `bio`; avatar/phone null được serialize; success 200 `DESIGN_RESOURCE_RETRIEVED`; trace ID giữ trong envelope/header.
- Data evidence: current SQL và `infra/postgres/study-server/DB.sql` dùng `users`; DDL là artifact, live DB chưa xác minh.
- Tests: source test bao phủ profile allowlist/trace, `sub` numeric mapping, Bearer/JWT/claims errors, Student guard trước DB, missing user, DB rollback/redaction và model mapping failure; test source đã đọc, không chạy trong docs task.
- AC-11 group current source: #13 upload Object Storage và chỉ trả URL; #14 có route/module/test source, update `full_name`, `phone`, `avatar_url`, nhưng model extra-ignore request `bio`; #04 reload cũng không trả `bio`.
- Candidate DDL khai báo `users.status VARCHAR(20) DEFAULT 'ACTIVE'` nhưng không `NOT NULL`; current `UserProfile.status` bắt buộc, nên row NULL gây `ValidationError` → safe 500. Live schema chưa xác minh.

## SOURCE_TRACE

```text
GET /api/v1/users/me -> Authorization + trace ID + DB Session -> validate_current_user_request -> Bearer/JWT decode -> validate sub/roles and STUDENT role -> SELECT users by numeric sub -> 401 if no row / rollback+500 on SQL error / 500 on UserProfile mapping error -> safe UserProfile envelope 200 -> API #04 tests (read only, not run)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| JWT claim naming | AC-02 ghi `user_id`/`role`; current #03/#04 use `sub`/`roles`; catalog #04 không khóa claim keys. | `DISCREPANCY` | Chốt shared token contract; không ghi diagram claim như current implementation. |
| Permissions | AC-02 nói đọc profile/role/permissions; catalog response chỉ `UserProfile`, current #04 trả profile có role nhưng không permissions. | `SOURCE_REQUIRED / CONTRACT_GAP` | Không thêm permissions field hay endpoint mới. |
| UserProfile.bio | Reusable schema có `bio?`; current #04 query/model không có bio; optional field có thể omit nhưng không thể populate. | `SOURCE_GAP` | Giữ contract field optional; ghi current omission và liên hệ API #14 unresolved persistence. |
| Missing user mapping | Catalog có 401 nhưng không nêu tình huống; current #04 trả 401 khi query không tìm thấy user. | `CURRENT_SOURCE_BACKED / SEMANTICS_OPEN` | Bỏ nhãn assumption-only; hỏi semantics identity inconsistency. |
| Role/status freshness | Current guard kiểm tra `STUDENT` từ token roles; query không lọc `users.status` hoặc đối chiếu `users.role`. | `POLICY_OPEN` | Chưa biết token stale sau role/status change còn được đọc hồ sơ hay không. |
| API #14 status | Current router/module/test tồn tại; #14 PLAN/VERIFICATION cũ ghi `UNWIRED/NOT_FOUND`. | `CONTEXT_STALE_IN_DD_REPORT` | Cập nhật report trạng thái source, không tuyên bố test/runtime pass mới. |
| AC-02 handoff | AC nói #03 nhận token rồi gọi #04; catalog #03 response không có token, current #03 source có; #04 trả profile nhưng không permissions. | `GROUP_DISCREPANCY` | Ghi macro-review #03/#04 và các điểm cần owner chốt. |
| AC-11 `bio` | Diagram/API #14 yêu cầu `bio`; current #14 model/query bỏ qua, #04 response/query cũng không có source. | `DISCREPANCY / SOURCE_REQUIRED` | Không tạo persistence hoặc giá trị giả; giữ câu hỏi xuyên suốt #04/#14. |
| `users.status` nullability | Checked-in DDL candidate không có `NOT NULL`; #04 model bắt buộc string. | `SCHEMA_CANDIDATE_GAP` | Nếu deployed row NULL, source mapping trả 500; live schema và requiredness cần xác nhận. |
| Avatar side-effect boundary | #13 upload storage và #14 update DB là hai request riêng, không chung transaction/compensation hiện được xác nhận. | `GROUP_OPEN_QUESTION` | Ghi risk/decision cần chốt; không mô tả cleanup/rollback như hành vi hiện có. |

## PLAN BEFORE REPORT AUTHORING

1. Giữ đúng catalog #04 method/path/auth/schema/status/errors; chuẩn hóa ký hiệu duplicate Bearer thành một header theo route, ghi lỗi notation.
2. Sửa Overview/Request/Data Mapping/Error để mô tả expected claims riêng với source `sub`/`roles`, current query fields/branches, missing-row 401 là source-backed, `bio` optional nhưng không được source, và auth role/status freshness gap. Sửa các source links hỏng.
3. Bổ sung ba report tiếng Việt với AC-02/AC-11, current source/tests, DDL/live-schema boundary, questions về permissions, claim contract, role/status freshness và `bio`.
4. Macro-review AC-02 #03→#04 và AC-11 #04/#13/#14. Không author API thứ hai; chỉ cập nhật API #14 `PLAN_RESULT.md`/`VERIFICATION_REPORT.md` để sửa claim `NOT_FOUND` trái current source; giữ #14 contract/schema gap như cũ.
5. Không sửa runtime, tests, schema, catalog, diagrams, API #13 contract hay API #14 core DD; không chạy application tests.
6. Static validate 11-file package, front matter/template appendix structure, exact catalog contract/error set, JSON, local links/anchors, tables, fences, whitespace/newlines, fingerprint, `git diff --check`; recount inventory và report source/runtime boundary.

## CHANGES

- Files changed: hoàn thiện 8 sheet API #04; thêm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; sửa trạng thái source trong API #14 `PLAN_RESULT.md` và `VERIFICATION_REPORT.md`; cập nhật worklog này và inventory worklog. Không sửa runtime, tests, schema, catalog, diagram, client hoặc context page.
- CONTEXT_UPDATES: Không đổi source/contract/registry; context validator không áp dụng vì không sửa context page.
- Context pages changed: None.
- Assumptions: `sub`/`roles` là current-source fact; `user_id`/`role` là expected wording của AC-02. `bio`, permissions, status freshness, missing-user semantics và storage/database compensation vẫn là open question.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Context/preflight | Root router, global context map, server-study AGENTS/INDEX/workflow, manifest registry, registered `createDD-markdown` skill/template và selector docs worklogs #01/#02/#03 được review. | VERIFIED_STATIC_ONLY |
| Diagram/API group | AC-02 và AC-11 XML/page flow; API #03 DD/source; #13 DD/source; #14 DD/source/reports/test-file presence reviewed. | VERIFIED_STATIC_ONLY |
| Current API #04 source/tests | Router, auth, trace/response, view/query/model, candidate DDL và focused test source reviewed; application tests không chạy. | VERIFIED_STATIC_ONLY / NOT_RUN |
| Package manifest | Chính xác 11 Markdown files: 8 sheet + 3 reports; front matter 8/8; workbook appendix structure 8/8. | PASS — STATIC |
| Contract/source boundary | Catalog #04 method/path/request/response/status/error set preserved; expected/current claims, bio/permissions/status/missing-user gaps recorded. | VERIFIED_STATIC_ONLY |
| JSON and links | 4 JSON blocks parse; 63 local links/path/anchors resolve; zero missing links/anchors. | PASS — STATIC |
| Markdown structure | 33 tables/384 data rows (450 table lines); widths consistent; code fences balanced; all files end newline; no trailing whitespace. | PASS — STATIC |
| Fingerprints | 8 template file SHA-256 baselines recorded; output fingerprint `3a49273b98ec9b9e287ff2807107a34852a1453cbf2f5f8ab9f8e0b44d35eb08`. | PASS — STATIC |
| `git diff --check` | Scoped tracked changes have no diagnostics; untracked Markdown also passed trailing-whitespace/newline checks. | PASS |
| API #14 source-status refresh | Removed current `NOT_FOUND/UNWIRED` claims; route/module/query/test source marked present, with no new runtime/test pass claim; report links resolve. | PASS — STATIC |
| Application tests/runtime/live DB | Not run. | NOT_RUN |

## HANDOFF

- Remaining blockers: Contract owner decisions về JWT claim keys, permissions source, role/status freshness, missing-user semantics, `bio` persistence/requiredness, candidate/deployed status nullability và #13→#14 compensation behavior.
- Next action: Hoàn thiện API #05 trong phiên kế tiếp; tiếp tục macro-review theo nhóm AC sau khi các DD liên quan sẵn sàng.

## POSTFLIGHT — API #04 package completion — 2026-10-24

- API #04 có đúng 11 Markdown files; contract catalog giữ nguyên; 8/8 sheet front matter và appendix; 4 JSON blocks hợp lệ; 63 links/anchors resolve; 33 bảng, 384 dòng dữ liệu và 450 dòng bảng nhất quán; fences/whitespace/newline pass.
- Template fingerprints: 8 file baseline được lưu trong `VERIFICATION_REPORT.md`; output fingerprint `3a49273b98ec9b9e287ff2807107a34852a1453cbf2f5f8ab9f8e0b44d35eb08`.
- AC-02 macro-review #03→#04 hoàn tất ở mức tài liệu; claim naming, permissions và lần đọc profile thứ hai còn mở. AC-11 macro-review #04/#13/#14 ghi rõ `bio` gap và side-effect boundary; API #14 reports không còn nói route/module/test `NOT_FOUND`.
- Inventory sau #04: 103/103 folders/core DDs; 95 package đủ 11 file; #05–#12 còn thiếu 3 reports (8); route+view source pair 12/103 (#01–#09, #12–#14), 91 không có cặp. Đây là source inventory, không phải runtime verification.
- Application tests/runtime/live DB không chạy/xác minh trong task docs-only này.
