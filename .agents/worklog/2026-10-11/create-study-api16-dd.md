---
task_id: "2026-10-11-create-study-api16-dd"
date: "2026-10-11"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["server-study"]
cross_scope_dependencies: []
status: "VERIFIED"
---

# Worklog: Tạo DD cho Study API #16

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3`
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-10-11/load-api13-detail-design-context.md`
    - carry_forward: Tách expected/current; dùng `createDD-markdown`; giữ `SOURCE_REQUIRED`, `UNWIRED` và `NOT_FOUND`; không biến contract thiết kế thành runtime.
  - path: `.agents/worklog/2026-09-28/study-module-layer-context.md`
    - carry_forward: Ưu tiên source hiện tại, giữ discrepancy, không suy diễn implementation từ context/design.
  - path: `.agents/worklog/2026-09-26/document-study-api3-view-comments.md`
    - carry_forward: DD không thay thế current source; giữ riêng contract/runtime và source-backed evidence.
- shortage: `none`

## EXPECTED_BEHAVIOR

- Requirement: Tạo DD draft cho API #16 `POST /api/v1/orders` theo 8-sheet Markdown template và thêm `PLAN_RESULT.md`, `OPEN_QUESTIONS.md`, `VERIFICATION_REPORT.md`.
- Canonical contract/approved DD: `docs/lists/list_api.md` đánh dấu catalog là `APPROVED_DESIGN_CONTRACT`; API #16 nhận Student Bearer JWT và body `{course_id:int64!, payment_provider:PaymentProvider!}`, trả `ApiEnvelope<Order>` với HTTP 201 và lỗi 401/403/422/500. AC-12 mô tả nhánh paid course tạo Order `PENDING` trước API #17.
- Approved handling: Tạo draft, giữ thiếu persistence/provider enum ở `SOURCE_REQUIRED`; không bổ sung runtime/schema/business rule.

## CURRENT_BEHAVIOR

- Source/config: `apps/study-server/docs/diagrams/DB_UNICA_TABLES.md` và ERD ghi V1 không có bảng `orders`; `infra/postgres/study-server/DB.sql` có `payments` nhưng không có `orders`.
- Runnable tests: Không chạy; API #16 chưa có route/module/test.
- Runtime wiring: Đã đọc `apps/study-server/app/api/v1.py`, route index và liệt kê module/test directories; không có route, module hoặc test cho API #16.

## SOURCE_TRACE

```text
Student client -> POST /api/v1/orders (design contract only)
-> AC-12 paid-course branch -> logical Order PENDING (physical persistence SOURCE_REQUIRED)
-> API #17 POST /api/v1/payments (separate API)
-> no API #16 runtime route/module/query/test found
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Order persistence | API catalog defines logical Order; ERD V1 and current DB.sql have no orders table | `SOURCE_REQUIRED` / `DISCREPANCY` | No physical mapping; do not substitute payments. |
| PaymentProvider enum | API row names PaymentProvider but no allowed values or semantics source found | `SOURCE_REQUIRED` | Validation and provider continuity remain open. |
| API #16 runtime | Current route/module/query/test surface omits endpoint | `UNWIRED` / `NOT_FOUND` | DD is expected design only. |
| Amount/currency/status | Order contract fields exist; source only sets initial status PENDING | `SOURCE_REQUIRED` | Value mapping and full status enum unresolved. |

## CHANGES

- Files changed: Created `apps/study-server/docs/dd/16_orders/` with 8 template sheets and 3 reports; created `apps/study-server/docs/dd/16_orders.zip`; created this worklog.
- CONTEXT_UPDATES: None.
- Context pages changed: None.
- Assumptions: API #16 is used in the AC-12 paid-course branch; API #17 remains separate; no Order mapping is inferred from `payments`. Existing untracked API #13 context worklog was preserved.

## VERIFICATION

| Command/check | Result | Status |
|---|---|---|
| `deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3` | Selected and read the active API #13 context log plus the two prior docs logs; no shortage. | VERIFIED |
| Current source/catalog/diagram/schema inspection | Confirmed the API #16 contract and AC-12 flow; route, module, query and test are absent; Order persistence/provider values are not source-backed. | VERIFIED |
| Inline static DD validation | 11 Markdown files, front matter, JSON examples, table widths, relative links/anchors, error-code set, code fences, whitespace and fingerprints passed. | VERIFIED |
| `unzip -t apps/study-server/docs/dd/16_orders.zip` | All archive entries tested; no errors. | VERIFIED |
| Runtime tests | Not run because API #16 is not wired; matches approved plan. | NOT_RUN |
| Context validator | Not run because no context page/manifest changed. | NOT_REQUIRED |

## HANDOFF

- Remaining blockers: Order persistence schema, provider values/semantics, amount/currency source, full OrderStatus enum and direct-call eligibility behavior remain open in DD.
- Next owner/action: Product/architecture owner supplies or approves these sources before changing DD to ready/final or implementing API #16.

