---
task_id: "2026-10-27-design-study-screen-sh07"
date: "2026-10-27"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["Study Web SH-07 operation panel -> Study API #18; linked ST-07, ME-15, AD-21 and AD-25 payment/notification/export journeys"]
status: "IN_PROGRESS"
---

# Worklog: Thiết kế Study Web screen SH-07

## PRIOR_WORKLOG_REVIEW

- primary_task_type: docs
- selector_command: deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3
- prior_worklogs_reviewed:
  - path: .agents/worklog/2026-10-27/design-study-screen-sh01.md
    - carry_forward: Dùng Study ocean tokens và spacing guide; design resource là target, không phải runtime. Cần xem cả ảnh annotated, giữ labels/content không bị marker che.
  - path: .agents/worklog/2026-10-27/design-study-screen-sh02.md
    - carry_forward: Trace current source so với DD/inventory và ghi discrepancy; không nạp font ngoài. ChatGPT website workflow có thể phụ thuộc CUA Chrome; không tuyên bố đã dùng nếu browser không khả dụng.
  - path: .agents/worklog/2026-10-27/design-study-screen-sh03.md
    - carry_forward: Giữ expected/current tách biệt, mọi status/claim phải theo source. Làm một screen mỗi phiên, tạo plan trước art, rà rendered views và giữ constraints linked screen.
- shortage: none (138 worklog docs khả dụng; đã đọc đủ 3 được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Thiết kế đúng một screen theo inventory order: SH-07 “Theo dõi tác vụ bất đồng bộ”, Panel, /operations/:operationId, AC-12/25/36/38, API #18. Cần PLAN trước artwork; clean và annotated images có marker cho từng element; detailed Vietnamese SCREEN.md dạng bảng; nếu inventory có child screen thì đặt folder con trong SH-07; lưu SVG/PNG/source/ZIP dưới apps/study-client/docs/dd_screens/resource/SH-07/.
- Canonical screen target: .agents/web-study/design.md và SH-07, ST-07, ME-15, AD-21, AD-25, F03/notification/export flow, shared error/state/security rules trong apps/study-client/docs/dd_screens/list_screen.md.
- Expected operation safety: Chỉ GET #18 với operation_id đã được backend xác nhận; không tự tạo ID; dừng polling ở terminal state. Current enum/ID mapping chưa được resolve; không vẽ trạng thái nào như verified nếu chưa có source.

## CURRENT_BEHAVIOR

- There is no `apps/study-client/` runtime source in this checkout; output is a design target.
- API #18 exists as Draft DD (`03_Request.md`, `04_Response.md`, `OPEN_QUESTIONS.md`), but has no route in `app/api/v1.py`, no runtime module, and no registration in `.agents/server-study/apis/declared-routes.md`; the current route inventory is 57 templates / 68 operations after API #97.
- API #18 DD leaves path ID `int64` vs UUID unresolved, authorization owner/Admin semantics unresolved, OperationKind/Status and terminal lifecycle unresolved, Study persistence/owner source unresolved, and `result` shape unresolved. Study DB inventory has no Operation table; there is no API #18 response/test implementation to use as runtime truth.
- Mentor API #63 returns an Operation-like UUID `NOTIFICATION_DISPATCH` with `QUEUED` after notification/outbox commit. API #64 takes `notification_id` as signed int64 (distinct from `operation_id`) and derives `QUEUED` / `FAILED` / `SENT` from delivery rows; this notification projection is not a generic Operation #18 implementation.
- Admin API #93 returns a Notification in `data` and a UUID `operation_id` in `meta`, so producer shapes do not share a confirmed generic Operation response.
- Study Web scoped entry says Vue subcontext .agents/web-work/study/, but the subcontext file is absent in current checkout; .agents/web-study/design.md is the canonical visual guide.

## SOURCE_TRACE

    inventory SH-07 -> API #18 Draft -> no route/module/declared runtime -> linked producers
    ST-06: #17 may return operation_id -> #18 only when backend confirms ID; client gateway callback is not payment proof
    ME-14: #63 returns UUID Operation-like notification dispatch -> #18 if ID supplied -> ME-15 #64 is queried by notification_id (int64); the two ID namespaces remain distinct
    AD-20: #93 returns Notification in `data` and operation UUID in `meta`; 202 is accepted, not sent
    AD-25: #103 202 -> #18 if operation_id exists -> download only if backend returns URL
    API #64 current source: owner-only MENTOR guard, notification ownership check, read-only notification/outbox aggregation; local DERIVED statuses QUEUED/FAILED/SENT

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| Operation state enum and ID mapping | API #18 Draft request/response/OPEN_QUESTIONS Q-18-01/Q-18-03; inventory §4.2/G-08. | DISCREPANCY / SOURCE_REQUIRED | Screen variants may depict inventory design states as DESIGN_ONLY; no ID cast, generic enum, terminal mapping, or poll cadence may be asserted as current behavior. |
| Authorization / ownership | API #18 Q-18-02/Q-18-05; API #64 source only proves Mentor sender ownership for its notification-specific route. | SOURCE_REQUIRED | Never reveal another owner's operation; render safe generic 403/404 states; do not infer Admin bypass. |
| Producer response contracts | #63 returns Operation-like data; #93 returns Notification data with operation_id metadata; #64 status requires notification_id. | DISCREPANCY | Keep operation_id, notification_id, and order_id separate; do not promise producer-specific result/action in the generic panel. |
| Generic Study persistence/runtime | API #18 open question says no Study Operation DDL/source; route/module/test not found. | NOT_FOUND / UNWIRED | Design is not evidence of a runnable API or live operation state. |
| Study Web subcontext | .agents/web-work/AGENTS.md/INDEX reference .agents/web-work/study/; file is absent. | NOT_FOUND / CONTEXT_MAP_DRIFT | Continue with canonical Study design guide and source; no unrelated context repair. |
| ChatGPT via @Chrome | Availability must be retried after PLAN is ready, per user's required sequence. | PENDING | No claim of website authoring until CUA proves the browser interaction. |

## CHANGES

- Files changed: This worklog; SH-07 design outputs will be recorded after plan/source review.
- CONTEXT_UPDATES: None planned; UI-only screen package.
- Context pages changed: None planned.
- Assumptions: None until operation source, linked producer flows and state mapping are traced.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| git status --short --branch | develop...origin/develop; existing SH-01..SH-06 resources/worklogs are untracked and preserved. | VERIFIED |
| deno run --allow-read scripts/select-worklogs.mjs --type docs --limit 3 | Selected/read SH-01, SH-02, SH-03; 138 available, no shortage. | VERIFIED |
| Root/global context and worklog contract | Read AGENTS.md, .agents/AGENTS.md, .agents/context-map.md, worklog README/TEMPLATE and web-work scope context. | VERIFIED_STATIC_ONLY |
| SH-07 inventory/canonical screen source | Read SH-07, linked ST-06/07, ME-14/15, AD-20/21/25, F03/F10/F13, ID rules and G-08. | VERIFIED_STATIC_ONLY |
| API #18 source/wiring/tests/DD and linked flows | Read API #18 request/response/open questions; inspected route registration, API #63/#64/#93 source and declared route inventory. | VERIFIED_STATIC_ONLY |
| UI/UX guidance | Read `.agents/web-study/design.md`; ran UI/UX Pro Max search. Search recommendations for dark/Glass styles conflict with canonical light ocean guide and are not adopted. | VERIFIED_STATIC_ONLY |
| ChatGPT @Chrome | Retry after plan completion. | PENDING |
| Render/package validation | Pending. | PENDING |

## HANDOFF

- Current step: Author the SH-07 visual/interaction plan, then submit that plan through the available @Chrome ChatGPT tab.
- Remaining workflow requirement: Submit the completed plan to ChatGPT via @Chrome if the CUA surface is available; then inspect/fix generated package and preserve provenance honestly.
