---
task_id: "2026-10-24-complete-study-api02-dd-package"
date: "2026-10-24"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Hoàn thiện package DD Study API #02 — Gửi email xác thực

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
    - carry_forward: Một API mỗi phiên; tách AC-01 expected behavior khỏi source; #01 hiện chỉ log marker và không gọi #02; Study DD là Markdown-only.
  - path: `.agents/worklog/2026-10-24/create-study-api100-dd.md`
    - carry_forward: Giữ contract catalog làm chuẩn; chỉ ghi field/schema trực tiếp có nguồn; DD package gồm 8 sheet và 3 report.
  - path: `.agents/worklog/2026-10-24/create-study-api101-dd.md`
    - carry_forward: Tách expected/current, giữ `SOURCE_REQUIRED` và discrepancy; dùng current source thay cho suy luận runtime.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện package Markdown API #02 trong phiên riêng, giữ nguyên contract, làm rõ expected/current discrepancy và rà điểm nối AC-01 với API #01.
- Catalog: public `POST /api/v1/auth/verify-email/send`; body `{user_id:int64!, email:email!}`; `ApiEnvelope<ActionResult>`; HTTP 202 `DESIGN_OPERATION_ACCEPTED`; errors chỉ gồm 422 `DESIGN_VALIDATION_ERROR` và 500 `DESIGN_INTERNAL_ERROR`. Reusable `ActionResult={status:string, reason?:string}`.
- AC-01: sau tạo tài khoản, nếu verification được bật thì gọi API #02 để Email Provider gửi verification; diagram mô tả log/retry khi gửi thất bại và không tạo account trùng.
- Deliverables: API #02 giữ 8 sheet hiện có, bổ sung `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; không tạo ZIP theo Study workflow.

## CURRENT_BEHAVIOR

- Route: `app/api/v1.py` khai báo public POST, inject provider, lấy trace ID/raw body và không inject DB dependency.
- Module: model khai báo `user_id:int`, `email:str`; validator yêu cầu raw `user_id` đúng kiểu integer và trim/kiểm tra email qua `normalize_email`; view gọi provider đồng bộ, lỗi exception trả 500 an toàn, success trả 202 với `data.status` và optional `data.reason`.
- Provider mặc định: `StubVerificationEmailProvider` bỏ qua input, trả `accepted`, không gửi email thật hoặc tạo token/link. Không có DB query/write hay retry worker.
- Test source có cases cho validation, public dispatch, không cần DB, provider error/response redaction; task docs-only sẽ không chạy tests.

## SOURCE_TRACE

```text
POST /api/v1/auth/verify-email/send -> VerifyEmailSendRequest + raw JSON -> validate exact integer and normalized email -> synchronous VerificationEmailProvider.dispatch(user_id,email,trace_id) -> safe 500 on exception or 202 DESIGN_OPERATION_ACCEPTED -> response envelope; no DB -> API #02 test source (read only, not run)
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| AC-01 dispatch connection | Diagram calls API #02 after registration; API #01 current view logs `verification_dispatch_pending` and does not invoke #02/provider. | `DISCREPANCY` | Account-to-email flow is not implemented end to end. |
| Retry/acceptance | AC-01 expects log/retry on provider delivery failure; #02 calls provider synchronously and returns 500 on exception; no worker exists. | `DISCREPANCY` | Async acceptance/retry semantics are design-only. |
| Real delivery | Default provider returns `accepted` but sends no email/token/link. | `STUB_ONLY / SOURCE_BACKED` | 202 from default provider is not proof of email delivery. |
| User/email binding | No database dependency/query verifies user existence or email ownership. | `SOURCE_REQUIRED` | Public caller can dispatch arbitrary supplied ID/email under current source; policy unresolved. |
| Input normalization | Catalog defines `email` and `int64` types only; current source trims/validates email and enforces raw JSON integer type, with no int64 range check. | `EXPECTED_CURRENT_GAP` | Keep runtime checks separate from approved format/range policy. |

## PLAN BEFORE REPORT AUTHORING

1. Preserve API #02 catalog method/path, public auth, request fields, response shape, HTTP status and exact error set.
2. Keep AC-01 verification/retry flow as expected behavior and document current #01/#02 source separately; link the completed #01 report.
3. Add the three standard reports in Vietnamese; record open decisions for dispatch ownership/enablement, acceptance/retry, provider delivery/token lifecycle, public abuse/rate limit, user/email binding, validation range/normalization and response status/reason semantics.
4. Repair only broken source links and any text that ambiguously describes expected retry as current behavior; do not modify contract, source, tests, catalog, diagram or schema.
5. Run static checks for 11-file package and required roles, template appendix parity, exact catalog contract/error set, JSON examples, local links/anchors, table widths, fences, whitespace/newlines, and `git diff --check`. Do not run application tests.
6. Recount inventory after completion: catalog/folders/core sheets/full report package and route-plus-matching-view IDs.

## CHANGES

- Files changed: API #02 `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`; corrected two broken source links and clarified expected/current behavior in `02_Overview.md`, `05_Data_Mapping.md`, and `06_Error.md`; this worklog and inventory worklog. No runtime, tests, schema, catalog, diagram, or client changes.
- CONTEXT_UPDATES: None planned; no runtime/schema/contract registry changes.
- Context pages changed: None planned.
- Assumptions: AC-01 remains expected behavior; no retry mechanism, token, table, user existence rule or email ownership behavior is inferred from current provider source.

## VERIFICATION

| Check | Result | Status |
|---|---|---|
| Context/preflight | Root router, context map, server-study scope/index/workflow, registry skill wiring and selected three docs worklogs reviewed. | VERIFIED_STATIC_ONLY |
| Current API #02 source | Route/model/validator/view/provider/test source reviewed; source implementation is present; application tests not run. | VERIFIED_STATIC_ONLY / NOT_RUN |
| Catalog/AC-01/DD | Exact API contract and AC flow reviewed; existing eight DD sheets read. | VERIFIED_STATIC_ONLY |
| Package manifest/template | 11 Markdown files (8 sheets + 3 reports); 8/8 front matters and template appendix suffixes pass. | VERIFIED_STATIC_ONLY |
| Contract/JSON/links | Catalog #02 method/path/request/response/status/errors preserved; exact three `DESIGN_*` codes; 4 JSON examples parse; 42 local links/anchors resolve. | VERIFIED_STATIC_ONLY |
| Markdown hygiene | 31 tables/370 table rows have consistent widths; fences balanced; all files end in newline; no trailing whitespace. | VERIFIED_STATIC_ONLY |
| Fingerprints | Template `3dc7fd2242dd1ed1bd9faba50aadad913a31b97ebf1392d6144bb905c5208137`; output `a4dd09da6e992fde1f0741e7889bcaf07ffda09cabacf4b7fc3ebd24781ca29a`. | VERIFIED_STATIC_ONLY |
| `git diff --check` | No diagnostics for API #02 folder and both worklogs. | PASS |
| Postflight inventory | 103 DD folders/core DDs; 93 full packages; #03–#12 incomplete reports; 12 source route+view pairs and 91 without. | VERIFIED_STATIC_ONLY |

## HANDOFF

- Remaining blockers: API/contract owner decisions listed in `OPEN_QUESTIONS.md`; AC-01 dispatch integration remains a source/diagram discrepancy.
- Next action: continue with API #03 in a later one-DD session; keep the one-API-per-session boundary.
