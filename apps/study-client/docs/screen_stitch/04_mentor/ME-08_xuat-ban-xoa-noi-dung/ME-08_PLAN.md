# ME-08 — Kế hoạch Detailed Design: Xuất bản/xóa nội dung

> **Plan status:** COMPLETE — expected/current trace, source-backed DD, annotated image and static audit are complete for this Screen ID.
> **Screen status dự kiến:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.

## 1. Phạm vi và đầu vào

- Phiên này chỉ xử lý **ME-08**; không author DD cho ME-06 hoặc ME-09. Chỉ ghi handoff giữa các màn hình liên quan.
- Phân loại: `primary_task_type: docs`; `secondary_task_types: [test]`; `project_scopes: [web-work, server-study]`; cross-scope dependency: ME-06 selection/#49 Content[] → #52 publish/unpublish hoặc #53 delete → refresh #49.
- Expected từ [`list_screen.md` ME-08](../../../list_screen.md#L168) và F08: route đề xuất `/mentor/content/:contentId/actions`; Actor Mentor; AC-22; PATCH #52 hoặc DELETE #53 rồi GET #49 refresh; liên kết ME-06; states `confirm/processing/success/blocked`.
- Goal objective yêu cầu mỗi phiên một Screen ID, plan trước annotation/DD, marker khớp một-một, source trace, tracker/worklog cập nhật và tách `DD READY`, `IMPLEMENTATION BLOCKED`, `RUNTIME VERIFIED`.
- Skill registry xác nhận `createDD-markdown` loại trừ `web-ui-only-dd`; không có skill canonical cho UI-only DD.
- `screen.png`: 1600×1530; SHA-256 `71b2db17d21899584fa4e70da2ee4955e83d7e701cda21a00d6117dc7e89dc78`; giữ nguyên.
- `code.html`: SHA-256 `18e7ee943af98918cd70eb141289015b2fc550088a4c726d57cef8d39ebb6a8b`; static page. 15 anchors đều `href="#"`; hai buttons đều disabled; không input, form, submit, API hoặc client event binding. Có remote font/Tailwind imports.
- Study Web context `UNWIRED`; no editable app source, package manifest or route. HTML/screenshot không phải runtime evidence.

## 2. Expected flow và current source trace

### Expected behavior

1. ME-06 chọn một Content trong course và mở action dialog; Mentor có quyền quản lý course.
2. ME-08 hiển thị đúng Content/status và cảnh báo tác động trước khi mutation.
3. Mentor xác nhận publish/unpublish qua #52 hoặc xóa qua #53.
4. Sau mutation thành công, refresh cây bằng #49 rồi quay về ME-06.

### Current behavior

- Screenshot/HTML hiển thị placeholder “Chưa chọn nội dung thao tác”; current status là mẫu “Bản nháp (Chưa xuất bản)”; “Mức độ tác động cấu trúc” là “Cấp độ thấp”; publish/delete đều disabled. Chỉ có nút publish, chưa có control unpublish.
- Side copy khẳng định tự cập nhật hoàn thành chứng chỉ, giữ điểm danh/bài nộp, có nhật ký audit, môi trường production, vùng Châu Á–Thái Bình Dương và Safe Mode; #49/#52/#53 không cung cấp các dữ liệu/tác động này.
- #49 cần `course_id`, trả active flat `Content[]` gồm `id/course_id/content_type/title/payload/status/parent_id/order`; không có detail endpoint. Response này có thể dùng để hydrate exact Content nếu ME-06 chuyển `courseId`.
- #52 route source cần strict body `{published:boolean}` dù catalog/AC chỉ khai báo path. Local transition proposal là `APPROVED → PUBLISHED` hoặc `PUBLISHED → APPROVED`; lặp target là no-op; source chỉ đổi status và trả Content với 200 `DESIGN_RESOURCE_UPDATED`.
- #53 route source không nhận body. Nó soft-delete khi target không PUBLISHED và không có active direct Content child; response `{id,status:"deleted",deleted_at}` với 200 `DESIGN_RESOURCE_DELETED`. Response không có `course_id`, active child/PUBLISHED guards là DERIVED.
- Catalog/API DD vẫn chưa duyệt request/transition/readiness của #52 hoặc eligibility/dependency của #53. AC-22 chỉ yêu cầu status update/soft delete và reload tree; không xác định state machine, child policy hoặc các hệ quả với học viên.

## 3. Artifact và marker plan

1. Kế hoạch này được ghi trước marker map, ảnh chú thích và DD.
2. Tạo **46 marker** theo thứ tự đọc từ header, breadcrumb, page header, target/impact/audit, action panel, footer meta rail tới footer.
3. Giữ ảnh gốc 1600×1530 và dựng ảnh chú thích tỷ lệ 2× (3200×3060); không thay đổi `screen.png` hoặc `code.html`.
4. Đặt marker ở lề/khoảng trống để không che chữ, badge, trạng thái hoặc nút; render rồi xem toàn ảnh, dời marker nếu chạm nội dung.
5. DD có 46 element ID `ME08-EL-01`…`ME08-EL-46`; mọi visible link/button/panel có API event, điều hướng candidate, hoặc ghi rõ static/blocked.

| # | Element inventory |
|---:|---|
| 1–4 | Brand; Mentor primary navigation; notifications; Mentor identity/avatar |
| 5–8 | Breadcrumb: course list; content tree; current screen; top protection badge |
| 9–14 | Page icon; Mentor board label; WCAG badge; title; description; policy-manual CTA |
| 15–20 | Target panel label/status badge; content icon; target name label/placeholder; selection instructions |
| 21–23 | Current publication label/draft sample; structure-impact label/value |
| 24–27 | Student-impact panel/title/description; two unsupported consequence rows |
| 28–29 | Recent coordination/audit heading and static row/time |
| 30–36 | Action panel heading; publish card; disabled publish button/reason; delete card; disabled delete button/reason; return-to-tree CTA |
| 37 | Data-protection/compliance badge and explanatory text |
| 38–42 | Environment, region, Safe Mode and approval-policy link meta rail |
| 43–46 | Footer brand/copyright and three footer links |

## 4. Event and state plan

1. **Open/hydrate:** parse `contentId` from proposed route and obtain `courseId`/selected Content from ME-06 context. If no verified context, do not use the sample. Expected #49 lookup is scoped to the course; find exact active ID. Route/state transport remains open.
2. **Publish:** only a user-confirmed target `published=true` may call PATCH #52. Body is current-source/DERIVED, not catalog-approved. Current source allows transition only from APPROVED; response/status and errors must be mapped exactly. Revalidate #49 after 200.
3. **Unpublish:** inventory expects this action but screenshot lacks a control. If approved, target `published=false` currently maps PUBLISHED→APPROVED; do not infer a toggle or add the control as canonical. Revalidate #49 after 200.
4. **Delete:** after explicit confirmation call DELETE #53 with path only. Current source blocks PUBLISHED before dependency lookup and blocks an active direct Content child; other non-PUBLISHED states pass this local fallback. Do not claim broader enrollment/submission/asset/audit protection. On success, preserve courseId from ME-06 because DeleteResult has no courseId, then reload #49.
5. **Navigation:** return-to-tree, breadcrumb, header, policy/manual and footer anchors are `#`; route destinations are not wired. Never infer route from `data-path` attributes.
6. **State/error cases:** loading, target-not-found, owner-denied, ready, confirming, processing-publish/unpublish/delete, success-await-refresh, validation-blocked, deleted, and server/network error. Current API #52/#53 have no 409; #53 repeated delete yields 404 after tombstone. Retry/reconciliation UX is open.
7. **Static panels:** label all unsupported status, progress, audit, student-impact, production, region and safe-mode copy as design-only; no API call or event is inferred.

## 5. Session acceptance checklist

- Original PNG/HTML hashes remain unchanged; screenshot and HTML discrepancies are recorded.
- `ME-08_PLAN.md` predates marker JSON/SVG, annotated PNG and DD.
- 46 ordered unique in-bounds markers; JSON↔SVG↔DD one-to-one; no marker obscures content; image dimensions preserve 2× aspect ratio.
- Every action/event traces to inventory/AC/current route/module/query/view/test source or is labeled open/DERIVED/blocked.
- #52 catalog/body/state discrepancy and #53 derived guards are explicit; no unapproved transition, dependency policy or audit effect is presented as canonical.
- Local API tests are inspected only; no test, runtime, deployed DB or live API claim is made.
- Update global ME-08 row/checkpoint and this worklog; run static link/marker/hash audit and `git diff --check`.
