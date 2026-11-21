# VERIFICATION_REPORT — Study API #03

**Endpoint:** `POST /api/v1/auth/login`
**DD status:** `Draft — Needs Confirmation`
**Source status:** route/module/source tests exist; the current catalog and login-specific DD match the source-backed HTTP 200 `LoginData` response for SH-02.

> Current reconciliation (2026-11-21): the original report below recorded the pre-reconciliation catalog status. API #03 catalog/DD now declare HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<LoginData>`, and the source-backed 401/403/422/500 branches. The combined targeted Study Server run includes API #03 and passed 87 tests across #03/#18/#63/#68/#93. Live deployment remains unverified.

## Phạm vi và nguồn đã kiểm tra

- [Catalog API #03 và reusable schemas](../../../../../docs/lists/list_api.md).
- [AC-02 index](../../diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC-02 activity diagram](../../diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio).
- Current router, API #03 model/validator/query/view, auth utility, candidate DDL và focused test source.
- Tám sheet DD API #03 và API #04 overview/response/current route boundary.
- Registry-wired `createDD-markdown` template và Study Server Markdown-only workflow.

## Package checks

| Check | Result | Status |
|---|---|---|
| File manifest | Chính xác 11 Markdown files: 8 sheet + 3 report chuẩn. | PASS |
| Front matter/source appendix | 8/8 front matter hợp lệ; 8/8 appendix có cấu trúc workbook-source gồm metadata và bản ghi ô. Template fingerprint: `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`. | PASS — STRUCTURAL |
| Catalog contract | Public POST, body email/password, `ApiEnvelope<UserProfile>`, HTTP 201 `DESIGN_RESOURCE_CREATED`; normative errors chỉ 422/500. Giữ nguyên trong DD. | VERIFIED_STATIC_ONLY |
| JSON examples | 4/4 JSON blocks parse hợp lệ. | PASS |
| Local links/anchors | 42 liên kết nội bộ/path/anchor resolve; không có missing path hoặc anchor. | PASS |
| Markdown tables | 35 bảng; 453 dòng table có số cột nhất quán. | PASS |
| Fences/whitespace/newlines | Code fences cân bằng; không trailing whitespace; mọi file có final newline. | PASS |
| Output fingerprint | SHA-256 theo basename/NUL/bytes/NUL trên 8 sheet + `PLAN_RESULT.md` + `OPEN_QUESTIONS.md`: `4c67fd0645beed0c41d3a59794e62445949faa50c746efbf7b5d8b4711afe7af`. | PASS — RECALCULATED 2026-11-21 |
| `git diff --check` | Không có diagnostics cho thay đổi tracked trong folder/worklog API #03. | PASS |
| Application tests/runtime | Original DD task did not run tests; combined targeted Study Server suite on 2026-11-21 included API #03 and passed 87 tests across #03/#18/#63/#68/#93. Live API/DB/deployment remain unverified. | SOURCE_TESTED; RUNTIME_NOT_VERIFIED |

## Expected behavior và current-source boundary

Current catalog and login DD follow checked-in source for the SH-02 slice: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<LoginData>`, and source-backed 401/403/422/500 branches. AC-02 still differs in some token/session and follow-up #04 details; those broader questions remain in `OPEN_QUESTIONS.md`. The source also persists a refresh-token hash, but that does not verify deployed schema or runtime.

Current `POST /api/v1/auth/refresh` là route source hiện có nhưng chưa có catalog row riêng; report không tính nó là contract API thứ hai hoặc nhập flow refresh vào login.

## Source trace

```text
POST /api/v1/auth/login -> LoginRequest -> normalize email/password checks -> SELECT users -> verify credential/status -> issue token pair -> INSERT refresh-token hash and commit -> HTTP 200 LoginData -> focused API #03 source test (included in combined 87-pass run)
```

## Connected API #04 boundary

AC-02 tiếp tục gọi `GET /api/v1/users/me`. Current login đã trả profile cơ bản; current #04 đọc lại profile và dùng claims `sub` + `roles`, Student-only. Diagram wording (`user_id`/`role`) và lý do fetch profile lần hai vẫn cần xác nhận; API #04 files không bị sửa trong package này.

## Câu hỏi và giới hạn

- Remaining questions include token claim/expiry policy, refresh-route API identity, validation/account-status policy, refresh-token schema/lifecycle, `UserProfile.bio`, and the #03→#04 handoff; see [OPEN_QUESTIONS.md](./OPEN_QUESTIONS.md).
- DDL trong repo không xác nhận live DB. Không chạy application tests, không gọi DB thật, không xác minh deployment/session/client behavior.
- Inventory sau package: 103 API folders/core DDs; 94 full 11-file packages; #04–#12 còn thiếu ba reports. Source route-plus-matching-view vẫn 12/103; 91 API chưa có cặp source. Đây là source inventory, không phải runtime pass.
