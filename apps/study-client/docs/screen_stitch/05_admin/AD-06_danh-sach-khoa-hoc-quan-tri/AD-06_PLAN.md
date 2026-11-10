# AD-06 — Kế hoạch Detailed Design

> **Screen ID:** AD-06 · **Tên:** Danh sách khóa học quản trị · **Đợt/ưu tiên:** W4 / P1<br>
> **Route đề xuất:** `/admin/courses` · **AC:** AC-32 · **API chính:** #73<br>
> **Trạng thái trước phiên:** inventory ghi `D`; source/API #73 hiện có route, module, test và test-environment report. Study Web vẫn `UNWIRED`; API DD #73 vẫn `Draft — Needs Confirmation`.

## 1. Phạm vi và nguyên tắc

- Hoàn thiện riêng AD-06 trong phiên này: plan trước, marker map, annotated image, A–F DD, screen inventory/reverse source index, global tracker và worklog. Không bắt đầu AD-07.
- Giữ nguyên `screen.png` và `code.html`; chỉ thêm `screen_annotated.png` và các tài liệu DD.
- Không coi các ô tìm kiếm, KPI, cột dữ liệu, status, nút, badge, nội dung đồng bộ hoặc lời bảo đảm quản trị trong HTML là runtime hoặc business contract.
- Tách contract AC/catalog, hành vi source hiện tại, bằng chứng test cô lập và runtime/deployment. Không tự tạo search, category relation, KPI, option list, export, create, moderation rule hoặc hành vi điều hướng.
- API #73 là read-only; không gọi #75/#76/#77 từ danh sách. Các mutation chỉ thuộc luồng AC-32 tiếp theo sau khi AD-07/AD-08/AD-09 và policy được chốt.
- Reverse API source index đổi #073 `D → R` vì route/module/test source tồn tại. Đây chỉ là phân loại source; API DD còn Draft, database live và Study Web runtime không được xác minh.
- Manifest không wire canonical skill cho `web-ui-only-dd`; `createDD-markdown` loại trừ UI-only DD. Không nạp API DD skill cho screen UI này.
- Không chạy app test hoặc runtime trong phiên. Dùng source/test/report đã có và kiểm tra tĩnh tài liệu/ảnh.

## 2. Bằng chứng đã rà soát

| Nhóm | Nguồn | Kết luận cho AD-06 |
|---|---|---|
| Inventory/dependency | `list_screen.md` row 64; `dd_screens/PLAN.md` | AC-32, #73, route đề xuất `/admin/courses`; từ AD-01/Admin shell, mở AD-07 bằng course ID. Mô tả tìm kiếm/filter/detail/status là expected design, cần đối chiếu source. |
| AC-32 | `apps/study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio` | Actor Admin, precondition có quyền course management; GET #73 → GET #74 → #75 update / #76 status / #77 delete theo policy → reload list. AC không cấp cho AD-06 API create/export/sync và không khóa danh sách status. |
| API catalog #73 | `docs/lists/list_api.md` | `GET /api/v1/admin/courses`; Bearer JWT/Admin; optional `status:string`, `mentor:int64`, `category:int64`, `page:int32`; success 200 `DESIGN_RESOURCE_RETRIEVED`; errors 401/403/422/500. Catalog không có search, size, sort hay KPI endpoint. |
| API #73 route/source | `apps/study-server/app/api/v1.py`; `modules/admin/api_73_admin_courses_list/{models,validate,query,view}.py`; shared `guest/_shared/course_catalog/{models,helpers}.py` | Shared role `ADMIN` guard xảy ra trước query validation/DB; status raw exact-match; mentor/category signed int64; valid category bị từ chối 422 vì relation chưa source-backed; page default 1, range 1..2,147,483,647, fixed size 20, `courses.id ASC`. Read-only count/page dùng cùng filter. |
| API #73 projection | Query/view + shared Course response model | `items[]`: `id`, `title`, nullable `description`, nullable `thumbnail_url`, exact decimal-string `price`, `status`, `mentor{id,full_name,avatar_url?}`; `pagination{page,size,total,total_pages}`. Search, code, lesson count, category, KPI aggregates và counters không có. Out-of-range page trả 200/empty items, giữ total; orphan mentor/count/projection failures trả safe 500 và rollback. |
| API #77 visibility | `modules/admin/api_77_admin_course_delete/query.py` | Local delete viết `status='DELETED'`; #73 không lọc status, nên unfiltered list có thể chứa bản ghi đó. Đây là current source behavior, không phải phê duyệt visibility/lifecycle policy. |
| Database | `infra/postgres/study-server/DB.sql`; `.agents/server-study/database.md` | Legacy candidate `courses` có numeric id, `mentor_id`, `name`, `price`, `status`; không có course-category FK. `categories` tồn tại nhưng không liên kết. V1-PILOT DDL khác mô hình; live schema/deploy chưa kiểm chứng. |
| Test evidence | API #73 test module; `apps/study-server/docs/testing/api-test-report-2026-11-01.md` | Report ghi 20/20 focused HTTP requests qua Uvicorn trên temporary schema/fixtures pass sau nullable SQL cast, 178 focused module tests và 1326 full-suite tests tại thời điểm report. Không chạy lại trong phiên; isolated test schema không chứng minh production. |
| API DD | `apps/study-server/docs/dd/73_admin_courses_list/{02_Overview,03_Request,04_Response,05_Data_Mapping,06_Error,OPEN_QUESTIONS}.md` | `Draft — Needs Confirmation`; còn câu hỏi category, permission, status enum/casing, page/order, orphan mentor, response fields, schema và macro flow #73–#77. |
| Prototype | `screen.png`, `code.html` | 1600×1514, empty state; 9 `href="#"` anchors, 8 buttons, one text input, two selects; chỉ Reset có listener nội bộ; không request/navigation. Bốn KPI đều zero hard-coded; status option lowercase; table có course code/lesson count; export/add/manual sync/policy controls không có handler. |
| Study Web/design | Study Web root, `.agents/web-work/study/*`, `.agents/web-study/design.md` | Editable app source/package/router/API client không có; ignored `dist` chỉ có route `/`; Study Web `UNWIRED`. Screenshot palette/font/layout lệch design guide; guide là target, không phải runtime. |

## 3. Expected behavior và current behavior

### Expected behavior

1. Admin có quyền quản trị course mở `/admin/courses`; route là đề xuất trong inventory, chưa có Study Web router.
2. Tải danh sách qua API #73 bằng Bearer JWT và truy vấn đã được contract/source chấp nhận. `page` mặc định 1; chỉ gửi status/mentor đã được phê duyệt; `all` phải được biểu diễn bằng cách bỏ query, không gửi literal `all`.
3. Ánh xạ response có nguồn: `Course.id`, `title`, `mentor.full_name`, `price`, `status`, thumbnail/description nếu UI dùng, và pagination metadata. Không suy ra course code từ `id` hoặc lesson count từ catalog.
4. Cho mở AD-07 bằng numeric `Course.id` sau khi có row; #74 là API chi tiết Admin. Thao tác sửa/trạng thái/xóa diễn ra ở screen tiếp theo sau policy/contract.
5. Category, search, KPI, export, add, sync/manual và moderation content chỉ được bật khi có contract/API/data/policy tương ứng.

### Current behavior

- Prototype hiển thị tĩnh một trang quản trị “Catalog V2” ở trạng thái zero-result, kèm các chỉ số 0 và footer/path tĩnh sai với endpoint hiện tại. Chỉ Reset đổi input/select phía client; không có request hoặc route.
- Local #73 hỗ trợ list + exact status + mentor + page. Category hợp lệ vẫn trả 422; không có search/aggregate. API #73 return có thể gồm `DELETED` rows vì query không loại trạng thái đó.
- API #73 có source và báo cáo test cô lập pass; API DD vẫn Draft; production/live schema và client integration chưa verified.

### DISCREPANCY

1. Search mockup (name/code/instructor) không có trong #73.
2. Mockup status options lowercase `draft/pending/published/archived` không có enum approval; source exact-match chuỗi không chuẩn hóa, còn #77 viết `DELETED` uppercase.
3. KPI tổng/pending/published/mentor hard-coded, trong khi #73 chỉ trả total của query đã lọc.
4. “Mã khóa” và “số bài học” không có trong response. Không đổi label/mapping để dùng `id` thay code.
5. Course-category relation thiếu, valid query 422; category phải tiếp tục disabled.
6. Export, tạo course, manual sync và governance statement không có handler/API/rule xác nhận ở AD-06.
7. Inventory purpose có nhắc “sửa trạng thái”; AC-32 sequence đi qua GET #74 trước khi chọn #75/#76/#77. Chưa xác nhận status action trực tiếp trên row AD-06.
8. Study Web source/router absent; tất cả behavior UI vẫn là design-only. Screenshot palette/type không theo đầy đủ target `.agents/web-study/design.md` (cobalt/Plus Jakarta Sans so với ocean-blue semantic tokens/Inter-system); đây là design mismatch, không phải runtime behavior.

## 4. Marker plan

Dự kiến **44 marker**, theo thứ tự từ đầu trang xuống footer; mỗi marker có đúng một dòng C trong DD. Marker group chỉ dùng cho một cụm tương tác/nhãn thống nhất (navigation group, table column headers, footer links), và các thành viên của cụm sẽ được liệt kê riêng trong mô tả.

1. Brand/logo; 2. nhóm điều hướng Admin; 3. SYSTEM NORMAL badge; 4. notifications; 5. identity/avatar Admin; 6. global breadcrumb; 7. RBAC badge; 8. local breadcrumb; 9. API #73 badge; 10. page title; 11. Catalog V2 badge; 12. page subtitle; 13. Export; 14. Add course; 15–18. bốn KPI cards; 19. search; 20. status select; 21. mentor select; 22. locked category; 23. active-filter summary; 24. Reset; 25. table header group (7 columns); 26. empty illustration; 27. empty heading; 28. empty copy; 29. disabled refresh; 30. sync-manual link; 31. static API source claim; 32. result count; 33. previous page; 34. page indicator; 35. next page; 36. governance icon; 37. governance heading; 38. governance copy; 39. standards CTA; 40. copyright; 41. footer system caption; 42–44. privacy/RBAC/support links.

Marker circles will sit beside the corresponding control/card/row where possible. The source remains untouched; annotation will be 2× dimensions.

## 5. Event and state coverage plan

| Event | Trigger | Planned treatment |
|---|---|---|
| EV-01 Load list | Enter `/admin/courses` | Describe expected #73 request in target flow and actual prototype as static. Specify auth ordering, query defaults, response mapping and empty/out-of-range/401/403/422/500. Retry behavior is unspecified by the API contract; do not choose a client policy here. |
| EV-02 Search/filter | Search input, status select, mentor select, locked category | Specify current prototype-only state behavior; #73 can represent approved status/mentor exact filters; search and option source are blocked; category stays disabled. No invented debounce. |
| EV-03 Reset filters | Reset control | Document actual JS reset of search/status/mentor to all with no request. Future server behavior depends on approved filter state and #73 call contract. |
| EV-04 Pagination | Previous/next/page indicator | Target `page` query only; fixed size 20, ID ascending. Prototype buttons are disabled. Handle current API's out-of-range empty page retaining total; don't infer clickability from the mockup. |
| EV-05 Open course | Row/action when data exists | Pass numeric `Course.id` to proposed AD-07 route and then #74. Current prototype has no rows/handler. Do not author AD-07 here. |
| EV-06 KPI/result display | List response | Bind row count/pagination only after definitions are approved; only pagination.total is source-backed. Four cards are not computable from #73. |
| EV-07 Unsupported controls | Export, add, manual sync, governance CTA and shell/footer links | Record presentational prototype affordances and absent handlers/contract. Keep disabled or remove only after owner decision; do not call unrelated #103 or #78. |
| EV-08 Access/errors | #73 response/auth failure/session expiry | Map 401/403 separately, handle 422 query/filter unsupported, 500 safe service error; session recovery destination and notice policy need shared auth contract. |

Candidate states: initial, loading, ready, empty, filtered-empty, out-of-range-empty-with-total, unauthorized, forbidden, validation-error, service-error, stale/refreshing only if a future refresh interaction is approved, and `UNWIRED` prototype state. Don't claim partial data or successful refresh.

## 6. Open decisions / blockers

1. Approve whether shared role claim `ADMIN` satisfies AC-32 course-management permission and any additional scope/safeguard.
2. Define status vocabulary/case/visibility, including `DELETED`, transition policy, and which values the list selector may expose.
3. Add/approve search contract (fields, normalization, page reset, query behavior) or remove the search affordance.
4. Resolve category relation and #73 response/query behavior before enabling category.
5. Approve KPI definitions and source; #73 `pagination.total` is filter-dependent and cannot supply four unfiltered aggregates.
6. Define course code and lesson count persistence/projection, or remove those columns.
7. Identify mentor option source and authorized labels/IDs for the mentor selector.
8. Decide export, course creation, manual-sync and governance/policy destinations/rules; current #73 and AC-32 don't supply them.
9. Confirm pagination URL/state, loading/failure retry and empty-state copy.
10. Wire Study Web source/router/API client and align target design system/accessibility before calling the screen implemented.
11. Verify live schema/migrations/deployment; the isolated API report is not production evidence.

## 7. Execution and verification order

1. [x] Complete docs worklog preflight; read three exact-type docs worklogs and prescribed context/source pages.
2. [x] Inspect current inventory, prototype/image, AC-32, API catalog/DD/source/test, DB candidate and Study Web boundary; record expected/current and discrepancies in worklog.
3. [x] Write this plan before marker map, annotation and DD.
4. [x] Create ordered marker JSON/SVG and 2× annotated image; preserve original hashes.
5. [x] Author A–F DD with one C row per marker, source-traced event/API/error/state/navigation behavior, and visible blockers.
6. [x] Update AD-06 inventory/reverse API source index and global tracker/checkpoint.
7. [x] Verify hashes, dimensions, marker sequence/coordinates/1:1 C rows, local links, 83 screen IDs/folders, core artifact count, whitespace and scoped diff. Do not run app tests/runtime.
8. [x] Update worklog with final verification; do not process another Screen ID.

## 8. Completion decision

Expected outcome: API #73 reverse source status is `R`, but DD remains Draft; AD-06 screen DD is expected to remain **DD BLOCKED** because key mockup features lack contract, category/status semantics are unresolved, and the UI is unwired. Implementation is **IMPLEMENTATION BLOCKED** by those contract/data and frontend dependencies. **RUNTIME NOT VERIFIED** for Study Web; the 2026-11-01 API report is limited to a temporary test branch and does not change that status.
