---
task_id: "2026-10-11-create-study-api17-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD draft cho Study API #17

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/create-study-api16-dd.md`
    - carry_forward: Tách expected/current; giữ Order và Payment là API/resource riêng; không biến bảng `payments` thành Order; duy trì `SOURCE_REQUIRED` cho schema/provider gaps.
  - path: `.agents/worklog/2026-10-11/load-api13-detail-design-context.md`
    - carry_forward: Dùng `createDD-markdown`; contract thiết kế không chứng minh runtime; ghi rõ `UNWIRED`, `NOT_FOUND` và nguồn ngoài chưa xác minh.
  - path: `.agents/worklog/2026-09-28/study-module-layer-context.md`
    - carry_forward: Ưu tiên source hiện tại, tách discrepancy, không suy diễn implementation từ design/context.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD Markdown draft API #17 `POST /api/v1/payments` theo template 8 sheet, kèm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md` và ZIP; ghi các nguồn thiếu/discrepancy, không sửa runtime, catalog, DB hay diagram.
- Canonical contract/approved DD: `docs/lists/list_api.md` đánh dấu catalog `APPROVED_DESIGN_CONTRACT` và API #17 là Student Bearer, body `{order_id:int64!, provider:string!}`, response `ApiEnvelope<Operation>`, HTTP 202 `DESIGN_OPERATION_ACCEPTED`; AC-12 mô tả payment gateway và nhánh success/failure.

## CURRENT_BEHAVIOR

- Source/config: `app/api/v1.py`/route context không khai báo API #17. `DB.sql`/ERD V1 có bảng thiết kế `payments`, không có `orders`, `order_id` hoặc `operations`; live schema không được xác nhận. API catalog có xung đột kiểu `operation_id` giữa convention/schema/diagram (`uuid`) và dòng API #18 (`int64`).
- Runnable tests: Không tìm thấy route/test API #17; runtime tests không chạy vì endpoint chưa được wire và task chỉ tạo tài liệu.
- Runtime wiring: Scan `apps/study-server/app` và `apps/study-server/tests` không thấy route/payment/operation implementation cho API #17.

## SOURCE_TRACE

```text
Student -> API #17 design contract -> 202 ApiEnvelope<Operation>
-> payment gateway in AC-12 -> success continues to API #19 enrollment;
   failure/cancel stops flow -> API #18 tracks operation per catalog
Current Study route/module/query/test: NOT_FOUND / UNWIRED
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #17 runtime | Current route and test scan has no payment endpoint | `UNWIRED` / `NOT_FOUND` | DD records expected design only. |
| Order/payment persistence | Logical `Order`/`Payment` schemas; V1 ERD/DB.sql has `payments` but no `orders` or `payments.order_id` | `SOURCE_REQUIRED` / `DISCREPANCY` | No physical Order-to-Payment mapping or amount/user/course source can be claimed. |
| Provider/payment gateway | Contract has `provider:string`; allowed values and gateway protocol are absent | `SOURCE_REQUIRED` | No enum, callback, retry or confirmation semantics are invented. |
| Operation tracking | `Operation` schema defines UUID ID but `GET API #18` row declares int64 path; persistence/status values are absent | `DISCREPANCY` / `SOURCE_REQUIRED` | Record integration gap without choosing a type or storage model. |
| DB runtime state | `DB.sql` and ERD are design evidence; live metadata is not verified | `NOT_VERIFIED` | Do not claim table availability in runtime. |

## CHANGES

- Files changed: Created apps/study-server/docs/dd/17_payments/ with 8 template sheets plus PLAN_RESULT.md, OPEN_QUESTIONS.md and VERIFICATION_REPORT.md; created apps/study-server/docs/dd/17_payments.zip; finalized this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: Draft with source gaps as approved; preserve API #16 DD, API catalog, diagrams, DB schema and runtime source.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3 | Selected and read the API #16 DD log, API #13 context log and Study module context log; no shortage. | VERIFIED |
| Source/catalog and AC-12 review | API #17 request/response/codes match catalog; AC-12 payment gateway branch and source limitations recorded. | VERIFIED |
| Inline Python Markdown validation | 11 files present; eight sheets in order; front matter, JSON, table widths, relative links/anchors, code fences and trailing whitespace passed. | VERIFIED |
| Inline contract/code check | API #17 endpoint/body/response and 401/403/422/503/500 error code set match list_api.md. | VERIFIED |
| Template/output SHA-256 checks | All eight template fingerprints match; output fingerprints recorded in VERIFICATION_REPORT.md. | VERIFIED |
| unzip -t apps/study-server/docs/dd/17_payments.zip | All archive entries tested; no compressed-data errors. | VERIFIED |
| Study runtime tests | Not run; API #17 is not wired and task scope is documentation. | NOT_RUN |
| Context validator | Not run because no agent context page/manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Q-17-01..Q-17-10 need authoritative decisions before finalizing the DD or implementing API #17.
- Next owner/action: Review OPEN_QUESTIONS.md and provide approved Order–Payment mapping, provider/gateway contract, amount/user/course sources, payment lifecycle and Operation design.
