# ST-20 — Plan chi tiết

**Screen ID:** ST-20\
**Tên:** Tổng quan tiến độ (Page)\
**Route trong inventory:** `/student/progress`\
**Actor:** Student\
**Kế hoạch:** PLAN COMPLETE\
**DD dự kiến:** BLOCKED bởi payload tiến độ #21, award policy/response #38 và orchestration AC-18 chưa được chốt
**Implementation/runtime:** Study Web hiện `UNWIRED`; API Student #21/#38 và frontend route chưa có current source.

## 1. Mục tiêu và giới hạn

- Đặc tả riêng ST-20 trong phiên này; nối từ ST-19/ST-08 và sang ST-21/ST-22 theo inventory.
- Giữ riêng yêu cầu inventory/AC/API design khỏi code, screenshot, HTML và trạng thái runtime hiện tại.
- Bảo toàn `screen.png` và `code.html`. PNG hiện có header/footer nhưng body chính trống; HTML có tiêu đề, copy empty-state và nút tới `/student/courses`. Kế hoạch sẽ render HTML tĩnh thành ảnh bổ sung `screen_rendered.png` nếu Chromium render được mà không phụ thuộc vào API runtime; ghi provenance và dùng ảnh này làm nền annotation. Không ghi đè ảnh gốc.
- Đánh số mọi cụm UI nhìn thấy trong bản HTML rendered; mỗi marker map một-một với dòng DD. Ghi body của PNG gốc là `blank/unrendered main region`, không xem đó là dashboard loaded.
- Mô tả #21/#38, phần tải độc lập/partial state, empty states, lỗi, route sang ST-21/ST-22 và các khác biệt orchestration mà không tự tạo schema, metric, badge rule, API behavior hoặc pagination.

## 2. Bằng chứng và ranh giới source

### Expected behavior

- Inventory ST-20: route `/student/progress`, AC-18, API #21 + #38; tổng số lesson, tiến độ theo course và achievements thực tế; gọi #21/#38 độc lập, render widget theo trạng thái API riêng; link ST-21/ST-22; states `loading/partial/empty/error`.
- API catalog #21: `GET /api/v1/users/me/progress`, Student Bearer; query khai báo mơ hồ nguyên văn `course_id list hoặc aggregate?:string`; response `ApiEnvelope<UserProfile>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/500.
- API #21 DD `Draft — Needs Confirmation`: UserProfile không chứa progress, query grammar, aggregate fields/formula, current-user binding, empty result và course merge key đều chưa được xác định.
- API catalog #38: `GET /api/v1/users/me/achievements`, Student Bearer, optional `course_id:int64`, response `ApiEnvelope<Page<Achievement>>`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/500. Request không khai báo page/size/sort.
- API #38 DD `Draft — Needs Confirmation`: không có award rules/projection/table, course filter semantics, pagination/order hoặc empty Page policy; không thêm pagination/error fields.
- AC-18 diagram vẽ tuần tự #21 → aggregate → chọn course → #37 detail → aggregate lesson/quiz/assignment → #38 achievements → render. Inventory ST-20 yêu cầu #21/#38 độc lập và đặt #37 ở ST-21. Giữ đây là `DISCREPANCY`, không tự chọn cách chạy.

### Current behavior

- `screen.png` là ảnh 1280×1123: header có brand và ba nav links; main body trống đồng màu từ dưới header đến footer; footer có brand, chương trình, hỗ trợ, liên hệ và legal strip. Không có tiêu đề/body/tiến độ/achievement hiển thị.
- `code.html` là static empty-state fallback: header, breadcrumb, page title/description, card “Chưa có dữ liệu tiến độ để hiển thị.”, copy hướng người dùng kiểm tra sau và link `/student/courses`, footer. Có Tailwind CDN/config và remote Google Font Plus Jakarta Sans; layout dùng `max-w-[1440px]`, config có `primary=#004AC6` trong khi một số control hardcode `#0B5F8A`. Không có API fetch, form handler hay auth logic. PNG và HTML không khớp phần body.
- Đây là **DISCREPANCY** với intended target `.agents/web-study/design.md`: không thêm remote font/CDN, ưu tiên Inter/system sans-serif, content width khoảng 1120px và dùng semantic `ocean-primary=#0B5F8A`. Giữ asset nguồn; chưa có loaded-state design đã xác nhận để áp dụng các quy tắc này.
- Nếu Chromium render HTML thành công, `screen_rendered.png` chỉ chứng minh nội dung HTML/CSS tĩnh được dựng; không chứng minh app route/API/runtime. Render source, kích thước và hash sẽ được ghi lại.
- Current Study Web không có editable app source/package/router/Student route; ignored `dist` chỉ có `/`.
- API #21/#38 không xuất hiện trong `app/api/v1.py`, current module/test tree hoặc Study declared route inventory. API #65/#67 là Mentor progress endpoints khác actor/path, không thay thế Student #21/#37. Không tìm thấy Student achievements runtime.
- DB guide đánh dấu #21/#37 query `DESIGN_ONLY`; checked-in DDL có candidate `lesson_progress` nhưng không có achievements table. DDL/ERD không xác nhận live schema.

## 3. Source trace và quyết định đặc tả

```text
Expected inventory: Student opens ST-20 → GET #21 and #38 independently →
  render progress and achievements widgets separately → ST-21 or ST-22.
Expected AC-18: #21 → aggregate → select course → #37 detail → #38 → render.
Current: ST-20 web route absent; Student API #21/#38 route/module/query/test absent.
  Screen PNG main region is blank; HTML has a static no-progress fallback.
```

- `#21` cannot yield a confirmed progress widget from the catalog `UserProfile` response; keep response schema discrepancy open.
- `#38` may only display fields of `Achievement` once award criteria/source/pagination are approved; don't fabricate earned or locked badges.
- `#37` is linked to ST-21 by inventory; AC-18 serial flow includes it before #38. No implementation ordering is asserted in ST-20 while these disagree.
- Widget independence in inventory permits documenting separate success/error UI states, but exact concurrency/sequence, auth retry and partial-render timing remain unresolved due AC-18 conflict and absent client source.

## 4. Marker plan

If `screen_rendered.png` is valid, number 16 visible component groups in reading order:

| Marker range | Component group |
|---|---|
| 01–02 | Brand link and primary navigation group (overview, my courses, active progress) |
| 03–09 | Breadcrumb, page heading/description, empty-state icon/title/description, view-courses CTA |
| 10–16 | Footer brand/description, program links, support links, contact details, copyright/legal strip and terms/privacy links |

The original PNG's unrendered main region will be recorded as a source discrepancy rather than numbered as a rendered control. If HTML rendering fails or is not faithful, annotate visible components from `screen.png` and record the fallback limitation in the plan/DD.

## 5. Event plan

1. **ST20-EV-01 Page entry/auth:** require Student context by design; route and guard are not current source. No client-side role claim is treated as server authorization.
2. **ST20-EV-02 Load progress #21:** endpoint is GET, Bearer Student, no body; preserve the catalog's ambiguous query declaration; no unsupported parameters/statuses are added. Response UserProfile cannot currently map required progress UI.
3. **ST20-EV-03 Load achievements #38:** GET with optional `course_id`; on overview, whether to omit the filter and include global/course awards needs policy; no page/size/sort fields are declared despite Page response.
4. **ST20-EV-04 Map progress widget:** preserve course merge, total lessons, denominator, completion formula, rounding and empty/no-enrollment distinction as unresolved. Don't derive metrics from lesson_progress without canonical rule.
5. **ST20-EV-05 Map achievement widget:** only backend-confirmed unlocked items can render; do not compute award IDs/codes/title/time or locked state on the client.
6. **ST20-EV-06 Handle independent/partial results:** inventory allows per-widget partial state; AC-18 serial order conflicts. Document partial/error states without prescribing scheduling until owner resolves orchestration.
7. **ST20-EV-07 Select course/open ST-21:** pass a valid course ID from an approved source; #37 is inventory-bound to ST-21, while AC-18 places it inside AC-18 flow. Route/access contract remains design-only.
8. **ST20-EV-08 Open achievements ST-22:** route and course filter/selection transfer are not wired; no badge action is created.
9. **ST20-EV-09 Empty-state CTA to ST-08:** HTML links `/student/courses`; route exists only in inventory/HTML, not current Study Web source.
10. **ST20-EV-10 Header/footer navigation:** prototype links are static/placeholders; describe visible links without claiming current route behavior.
11. **ST20-EV-11 API error handling:** keep #21/#38 catalog errors exactly 401/403/500; no catalog 404/422. Query parse/network errors lack endpoint-specific policy.

## 6. Blockers

- API #21 has no Student source and no progress response schema; query selector, aggregate source/formula, user binding, course merge and empty shape unresolved.
- API #38 has no Student source/award registry/table; achievement criteria/projection/filter/pagination/ordering/empty result unresolved.
- Inventory says #21 and #38 are independent; AC-18 places #37 between them and renders only after achievements. Request ordering is not reconciled.
- Screen PNG omits the body; HTML only provides unavailable/empty state, not the expected loaded dashboard.
- HTML visual prototype uses remote CDN/font, a 1440px layout and mixed primary tokens that diverge from the Study Web design target; no approved loaded-state visual is available.
- Study Web route/runtime is absent; ST-21/ST-22 route/data handoff not implemented.
- Candidate DDL has lesson_progress but no achievements table; it is not live schema proof.

## 7. Verification plan

- Record original PNG/HTML hashes/dimensions; ensure originals remain byte-identical.
- If browser render succeeds: record Chromium render provenance/hash/dimensions; inspect HTML-derived image and use it for annotation with clear source metadata. Otherwise annotate original PNG and mark main body unavailable.
- Validate ordered markers/count/coordinates, unique mapping against DD element rows, event IDs, relative links, API error sets, tracker status/counters/next pointers and whitespace.
- Run `git diff --check`; no tests or runtime API checks are planned.

## 8. Sources

- [Screen inventory and F07](../../../list_screen.md)
- [Original screenshot](./screen.png), [HTML companion](./code.html)
- [API catalog](../../../../../../docs/lists/list_api.md)
- [API #21 overview](../../../../../../apps/study-server/docs/dd/21_users_me_progress/02_Overview.md), [open questions](../../../../../../apps/study-server/docs/dd/21_users_me_progress/OPEN_QUESTIONS.md)
- [API #38 overview](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/02_Overview.md), [open questions](../../../../../../apps/study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md)
- [AC-18 diagram](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio), [AC/API index](../../../../../../apps/study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md)
- [Progress table design](../../../../../../apps/study-server/docs/diagrams/DB_UNICA_TABLES.md), [candidate DDL](../../../../../../infra/postgres/study-server/DB.sql)
- [Current Study route inventory](../../../../../../.agents/server-study/apis/declared-routes.md), [Study Web design target](../../../../../../.agents/web-study/design.md)


## 9. Kết quả thực hiện plan

- Chrome headless render thành công từ `code.html`: `screen_rendered.png`, 1280×1079, SHA256 `00b273505d7982eb92477d076d5e60b923d30209e4510d504cc55785b1c688ea`. Đây là HTML/CSS tĩnh, không có app/API runtime. `screen.png` và `code.html` giữ nguyên hash nguồn.
- Đã tạo annotation trên ảnh render bổ sung với 16 marker đặt cạnh nhóm UI; JSON/SVG và 16 hàng element DD ánh xạ một-một. Ảnh được xem trực quan; marker không che text/control.
- Đã tạo DD A–F với 11 event; ghi rõ blockers #21/#38, mâu thuẫn orchestration inventory/AC-18, route UNWIRED và giới hạn của empty-state HTML.
- Static audit ban đầu: JSON hợp lệ; marker 1–16 duy nhất/trong bounds; SVG XML hợp lệ; 18 link trong DD và 14 link trong plan resolve; section A–F và event 01–11 đủ; tại checkpoint đó tracker 32/83, 51 còn thiếu, next Student ST-21, Mentor ME-04; `git diff --check` sạch. Tests/runtime không chạy.
- Rà soát lại ngày 2026-11-07: ba PNG, hash source PNG/HTML, 16 marker/element mapping, 11 event, SVG, A–F, 18 link DD, 14 link plan và whitespace được kiểm tra lại; bổ sung rõ event element/type, sửa phân loại CTA thành anchor link tạo kiểu button, và ghi nhận lệch prototype với Study Web design target. Không dựng lại ảnh hay sửa source asset. Kiểm kê hiện tại là 83/83 thư mục và 82/83 bộ core artifacts hoàn chỉnh (ST-01 còn thiếu); ST-20 tiếp tục `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED`. Không chạy application tests hoặc runtime.
