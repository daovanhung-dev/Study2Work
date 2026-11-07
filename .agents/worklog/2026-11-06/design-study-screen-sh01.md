---
task_id: "2026-11-06-design-study-screen-sh01"
date: "2026-11-06"
primary_task_type: "docs"
secondary_task_types: []
project_scopes: ["web-work", "server-study"]
cross_scope_dependencies: ["SH-01 public landing page -> API #05 category and API #06 course source/contracts; route and data fields must be traced"]
status: "VERIFIED"
---

# Worklog: Rà soát Detailed Design màn hình Study SH-01

## PRIOR_WORKLOG_REVIEW

- primary_task_type: `docs`
- selector_command: `node scripts/select-worklogs.mjs --type docs --limit 3`
- selector_result: `READY`; 3 worklogs được chọn trong 153 log `docs` khả dụng.
- prior_worklogs_reviewed:
  - path: `.agents/worklog/2026-11-05/check-study-screen-stitch-coverage.md`
    - carry_forward: Inventory có 83 ID trong 84 thư mục ID tại thời điểm audit; SH-01 từng có hai biến thể. Kiểm kê file không xác nhận chất lượng DD hoặc runtime.
  - path: `.agents/worklog/2026-11-05/co-locate-study-screen-documents.md`
    - carry_forward: SH-01–SH-04 có bộ DD cũ cạnh ảnh nguồn; biến thể SH-01 thứ hai hiện không có trong cây. Không phục hồi nguồn thiếu.
  - path: `.agents/worklog/2026-11-05/complete-study-screen-docs.md`
    - carry_forward: SH-05/SH-06 đạt DD READY; SH-07 vừa được rà soát và bị chặn bởi API #18. SH-01 là bước W0 kế tiếp; chỉ xử lý một Screen ID trong phiên.
- shortage: `none` (đã đọc đủ 3 worklog được chọn)

## EXPECTED_BEHAVIOR

- Requirement: Hoàn thiện DD cho SH-01 theo objective 83 màn hình; lập/đối chiếu plan trước DD; giữ nguyên ảnh/HTML nguồn; tạo hoặc kiểm tra ảnh chú thích và marker map; truy vết toàn bộ element/event tới nguồn; cập nhật tracker và worklog. Phiên này chỉ xử lý SH-01.
- Canonical contract/approved DD: `apps/study-client/docs/list_screen.md` SH-01 (AC-03, #05/#06, route đề xuất `/`, links GS-01/GS-02/SH-02/SH-03); `screen_stitch/dd_screens/PLAN.md`; API catalog/API #05/#06; current Study Server source/tests; `.agents/web-study/design.md` là UI target, không phải runtime evidence.

## CURRENT_BEHAVIOR

- Source/config: SH-01 hiện có một thư mục variant-1 với PNG 559×1600, HTML, DD, plan, marker map và annotated image. PNG SHA-256 777f11eafd87807524c99ac6c21d402519311f3c9ff48f54c0781b543bc0d64f; HTML SHA-256 d22ed5ee5000b49f6c4b69297b460ed0d2841938b04887f5b3882b8582d3e5b8. Variant-2 có trong log/README cũ nhưng không có trong cây hiện tại. Study Web source/router/package.json và .agents/web-work/study/ không có.
- PNG/HTML discrepancy: PNG có KPI, năm chip + carousel, sáu card, benefit/testimonial/employer/email sections; HTML có bốn danh mục, hai card mẫu và empty state đồng thời, không có nhiều section trong ảnh. Header/search/auth controls cũng khác; HTML dùng href="#".
- API #05 source: route /api/v1/categories; locale mặc định vi-VN, match chính xác; lọc ACTIVE, order id ASC; success envelope DESIGN_RESOURCE_RETRIEVED, empty vẫn 200; 422 query validation; 500 DESIGN_INTERNAL_ERROR khi query/mapping lỗi.
- API #06 source: route /api/v1/courses; page default 1, size default 20 và range 1..100; sort allowlist id/name/price/created_at theo asc/desc, default created_at DESC/id ASC; chỉ PUBLISHED, DTO price decimal string và mentor projection. Bất kỳ category nào bị validator trả 422 DESIGN_VALIDATION_ERROR trước DB vì relation/filter không được hỗ trợ; DTO không có currency/review/duration/lesson-count/category fields.
- Current API source/test code exists; tests use fake sessions/data and were not run. No live DB, deployment, or Study Web runtime evidence was verified.

## SOURCE_TRACE

```text
SH-01 landing prototype -> proposed public route -> API #05 categories + API #06 published courses -> current Study route/validation/query/DB mapping/tests -> independent UI regions and downstream GS-01/GS-02/SH-02/SH-03 routes
```

## DISCREPANCIES_AND_STATUSES

| Item | Evidence | Status | Impact |
|---|---|---|---|
| SH-01 design variants | Prior inventory/worklog records two variants; current tree contains only variant-1. | NOT_FOUND / SOURCE_REQUIRED | Cover only current source; do not recreate missing variant. |
| PNG vs HTML authority | Full screenshot and smaller static HTML disagree on sections, controls and mock data; no approval chooses one as canonical. | DISCREPANCY / BLOCKER | DD remains blocked on intended surface/interaction choice. |
| #06 category filter | Catalog declares category, current validator rejects any category before DB because relation/filter is unsupported. | DISCREPANCY / SOURCE_WINS_FOR_CURRENT | SH-01 must not send category or enable category filtering. |
| GS-03 / #08 detail navigation | F02 names GS-03, SH-01 next-screen list omits it; #08 route/module/test source exists while catalog labels it D. | DISCREPANCY | Keep course-card navigation blocked pending route/client decision. |
| Marketing/newsletter content | KPI, review, duration, discounts, logos, certificates and email collection lack API/approval evidence. | UNSUPPORTED / BLOCKED | Do not present claims or collect email as real. |
| Runtime wiring | Study Web source/router absent; API fake-session tests are source evidence only. | UNWIRED / RUNTIME NOT VERIFIED | No UI behavior or live data claim. |

## CHANGES

- Updated SH-01_PLAN.md with source trace, 26 component groups, 14 event paths, blockers and acceptance gates before DD/artifact revision.
- Updated SH-01_markers.json; generated screen_annotated.png (1230×3200, 2× source centered with 28 source-pixel gutters) and reproducible SH-01_markers_overlay.svg. Source screen.png and code.html were retained unchanged.
- Reworked SH-01.md: 26 Element IDs, 14 detailed event flows, current API/error mappings, asset/source discrepancy, route navigation conflicts, state/accessibility/privacy sections and separate DD/implementation/runtime statuses.
- Updated global tracker row and continuation state to SH-01 BLOCKED and next Screen ID SH-02.
- CONTEXT_UPDATES: None; no runtime contract, architecture or DB schema is being changed.
- Context pages changed: None.
- Assumptions: Web UI-only DD has no canonical registered skill; registry excludes createDD-markdown from web-ui-only-dd, so document the design surface with source trace and explicit blockers.

## VERIFICATION

| Command/read | Result | Status |
|---|---|---|
| `node scripts/select-worklogs.mjs --type docs --limit 3` + read selected worklogs | 3 exact-type worklogs selected and read; no shortage. | VERIFIED |
| SH-01 static artifact/source audit | SHA-256 unchanged for PNG/HTML; 26 ordered unique markers map to 26 DD Element IDs; 14 unique sequential event IDs; JSON/source dimensions agree; 1230×3200 annotation visually reviewed; all relative Markdown links resolve; git diff --check clean. | VERIFIED |
| Tests/runtime | Not run; no Study Web runtime or live DB evidence. | NOT_RUN |

## HANDOFF

- Remaining blockers: PNG vs HTML authority; missing variant-2 source; #06 category filter; GS-03/#08 destination disagreement; unapproved marketing/email content and currency display; no Study Web router/runtime or live DB/deployment verification.
- Next owner/action: SH-02 in a separate W0 session; do not start another Screen ID in this session.
