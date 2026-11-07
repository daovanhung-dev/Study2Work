---
task_id: "2026-11-05-design-study-screen-sh07"
date: "2026-11-05"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-07 operation tracking UI -> API #18 operation-status contract/source; operation ID and status mapping must be traced"]
status: "IN_PROGRESS"
---

# Worklog: Thiết kế màn hình Study SH-07 Theo dõi tác vụ bất đồng bộ

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs được chọn trong 152 log `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: 83 mã trong inventory; ảnh/HTML chỉ chứng minh design assets, không chứng minh runtime.
  - path: `.agents/worklog/2026-11-05/co-locate-study-screen-documents.md`
    - carry_forward: DD, plan, marker map và annotated image phải nằm cạnh nguồn; lập plan trước DD/annotation; SH-01–SH-04 cần review riêng theo DoD mới.
  - path: `.agents/worklog/2026-11-05/complete-study-screen-docs.md`
    - carry_forward: SH-05/SH-06 đã rà soát riêng; SH-07 là bước kế, còn 77 mã thiếu bộ asset đầy đủ; chỉ xử lý một Screen ID mỗi phiên.
- shortage: `none` (đã đọc đủ 3 worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Objective file yêu cầu hoàn thiện từng màn hình trong phiên độc lập, lập `<SCREEN_ID>_PLAN.md` trước, giữ nguyên ảnh nguồn, tạo annotated image/marker map/DD truy vết được, cập nhật tracker/worklog và phân biệt DD READY, implementation blocker, runtime verification. Phiên này chỉ làm SH-07.
- Canonical contract/approved DD: Objective file; SH-07 row trong `apps/study-client/docs/list_screen.md`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; AC-12/25/36/38 và API #18 design artifacts, đối chiếu với current Study Server source.
- SH-07 inventory expectation: route proposal `/operations/:operationId`; theo dõi job thanh toán/thông báo/xuất báo cáo; GET #18 chỉ với `operation_id` được BE xác nhận; dừng polling ở terminal state; liên quan ST-07, ME-15, AD-21, AD-25. Inventory đánh dấu D và block do operation-status enum/ID mapping chưa thống nhất.

## CURRENT_BEHAVIOR

- Source/config: SH-07 `screen.png` 1503×1600 và `code.html` tồn tại; chưa có SH-07 DD/plan/marker map/annotated image trước phiên này. HTML là prototype tĩnh: default `Gated / Unavailable`, `STAGING-MOCK-07`, UUID fallback mẫu, copy ID, modal bật/tắt, lifecycle cards tĩnh, CTA `href="#"`; không gọi API hay poll. Modal đề xuất 3000ms/backoff hoặc SSE, sample `result_url/error`, TTL 24h/15min và “DB migration v2.4 int64” không được xác nhận bởi API #18 contract/current Study schema. Study Web `src/`/package manifest và Study subcontext `.agents/web-work/study/` vắng trong checkout.
- Current API #18: API catalog row là `D`, `GET /api/v1/operations/{operation_id}`, Bearer JWT, operation owner, `operation_id:int64`, response `ApiEnvelope<Operation>`. Catalog convention, reusable `Operation.id`, AC-12/25/36/38 lại khai báo UUID. API #18 DD đang Draft; current `app/api/v1.py` không có route, không có module/query/test #18, Study DDL không có bảng Operation. Migration 009 chỉ thêm `notifications.operation_id UUID` cho dispatch notification.
- Related current producer/read APIs: #63 có source/test; sinh UUID, insert cùng UUID vào các notification rows, trả HTTP 202/`DESIGN_OPERATION_ACCEPTED` với `data:OperationResponse` (`NOTIFICATION_DISPATCH`,`QUEUED`) và `meta.notification_ids`. #64 nhận `notification_id:int64`, kiểm tra Mentor sender, trả UUID Operation nhưng state local chỉ `QUEUED`/`FAILED`/`SENT`. #93 sinh UUID, trả 202 nhưng `data` là Notification và `meta.operation_id` + `notification_ids`, không trả `data:Operation` như tracking summary. #96 là notification status theo `notification_id:int64`, không phải generic API #18. API #17 payment và #103 report export không có current route/module/test source. Không thay API #18 bằng notification-specific API.
- Runnable tests: Không chạy; đã đọc test source API #63/#64/#93 và API #18 verification record xác nhận không có test #18.
- Runtime wiring: Không có Study Web source/router. API #18 `UNWIRED / NOT_FOUND`; API #63/#64/#93/#96 có source routes nhưng nguồn/test không xác nhận deployed runtime/live DB.

## SOURCE_TRACE

```text
ST-06/API #17, ME-14/API #63, AD-20/API #93, AD-25/API #103 producers -> current returned operation_id/notification_id -> proposed SH-07 route -> catalog API #18 -> absent route/module/query/test and no Study Operation table -> SH-07 static gate state
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| API #18 ID type | `list_api.md` row uses `operation_id:int64`; catalog convention, reusable Operation schema and four AC diagrams use UUID; API #63 source emits UUID. | `DISCREPANCY` | Do not parse, coerce, truncate, or invent an ID. Contract owner must settle one type across producers, route and storage. |
| Operation lifecycle/status | API #18 reusable `OperationStatus` has no values; screen/list/HTML propose QUEUED/RUNNING/SUCCEEDED/FAILED/EXPIRED; notification-specific source returns QUEUED/FAILED/SENT. | `DISCREPANCY / SOURCE_REQUIRED` | Do not use the prototype's five-card reference list as a live enum or infer terminal states. |
| Operation source/persistence | Current API #18 route/module/query/test and Study Operation table are absent; Study migration 009 adds only a UUID column on notifications. Work Server operations table belongs to a separate user/schema. | `UNWIRED / NOT_FOUND` | No generic read or storage mapping is available; don't map the Work table or invent Study storage. |
| Producer response alignment | Catalog tracking summary says all producers return Operation; row #93 and current #93 source return Notification data with operation_id metadata; #103 row returns Report; #17/#103 have no current route. #63 returns Operation. | `DISCREPANCY` | Consumers cannot rely on one data path or generic `result` shape; producer/contract owner must align before integration. |
| Authorization/owner result access | API row says owner; tracking summary says owner/Admin; AC diagrams say Student/Mentor/Admin owner-only. API #64 current source enforces Mentor sender ownership, but #18 is absent. | `DISCREPANCY` | Role matrix, owner predicate and wrong-owner 403/404 behavior remain unapproved. |
| Polling, expiry and result | API #18 DD says cadence, retention, transitions and per-kind result are unspecified; HTML claims 3s/backoff or SSE, 24h/15min TTL, `result_url/error`. | `DESIGN_ONLY / SOURCE_REQUIRED` | Don't add interval, SSE route, timeout/TTL, download action or result mapping from the prototype. |
| Navigation | Inventory links SH-07 to ST-07/ME-15/AD-21/AD-25; source HTML recovery CTAs point to GS-01/SH-01 and all anchors are `#`. No safe-return payload is defined. | `DISCREPANCY / UNWIRED` | Product/FE must approve caller return behavior; don't drop operation origin or invent a route parameter. |
| Study Web route/runtime | `apps/study-client/src/`, package manifest and `.agents/web-work/study/` absent; route exists only as inventory proposal. | `NOT_FOUND / DESIGN_ONLY` | UI and route runtime cannot be verified. |

## CHANGES

- Files changed: `.agents/worklog/2026-11-05/design-study-screen-sh07.md`; `apps/study-client/docs/screen_stitch/01_shared_auth_system/SH-07_theo-doi-tac-vu-bat-dong-bo/SH-07_PLAN.md` (created before DD/annotation); `SH-07.md`; `SH-07_markers.json`; `SH-07_markers_overlay.svg`; `screen_annotated.png`; `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md`; `.agents/worklog/2026-11-05/complete-study-screen-docs.md`.
- CONTEXT_UPDATES: None; no architecture, runtime contract, DB schema or context convention page changed.
- Context pages changed: None.
- Assumptions: SH-07 is a shared route/view concept in the inventory, but UI runtime is absent. Do not invent an operation API, ID translation, event bus, payment/notification/export business rules or status enum. `createDD-markdown` is registered for API/DD work but explicitly excludes web UI-only DD; no UI-only skill is registered, so this task uses source-traced screen documentation only.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` and read selected worklogs | Selected/read 3 exact-type worklogs; none missing. | VERIFIED |
| SH-07 source/artifact trace | Original image/HTML dimensions and hashes captured; UI prototype, current API #18 absence, producer ID/response differences, notification-only routes and Study schema evidence recorded. | VERIFIED_STATIC_ONLY |
| `SH-07_PLAN.md` review | Written before DD and annotation; 35 visible marker targets, 10 event paths, API/source discrepancies, state gates and acceptance blockers recorded. | VERIFIED_STATIC_ONLY |
| SH-07 artifacts | DD, plan, 35-marker map and annotated image reviewed; DD has 35 visible elements, hidden modal details, 10 events and source-backed blockers. Annotation was visually inspected after moving badges away from text. | VERIFIED_STATIC_ONLY |
| SH-07 static inventory/artifact/link/hash audit | 83 unique inventory IDs = 83 folders = 83 tracker rows; 7 full asset sets (SH-01–SH-07), 76 remaining; 35 ordered unique markers map to 35 DD Element IDs; 10 event IDs; all SH-07 DD/plan local links resolve; source PNG/HTML hashes unchanged; both images 1503×1600. | VERIFIED_STATIC_ONLY |
| Whitespace and diff check | `git diff --check` on tracked edits and inline Python trailing-whitespace scan of all touched Markdown/JSON/SVG text files; no errors. | VERIFIED_STATIC_ONLY |
| Tests/runtime | Not run; no runtime execution requested. | NOT_RUN |

## HANDOFF

- Remaining blockers: API #18 route/module/query/test and generic Study Operation storage are absent; UUID/int64 ID, status/lifecycle, owner policy, producer/result mapping, polling/retention and safe-return navigation remain unresolved. Study Web router/runtime is absent. The annotation/doc audit does not establish runtime behavior.
- Next owner/action: SH-07 is `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`. Continue with SH-01 legacy draft review in a separate session, following W0 order; do not begin it in this session.
