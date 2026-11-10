# Kế hoạch màn hình — GS-01 Danh sách khóa học

> **Trạng thái kế hoạch:** `SOURCE_TRACE_COMPLETE; PLAN_READY`. DD dự kiến `BLOCKED`; implementation `BLOCKED`; runtime `NOT VERIFIED`. Kế hoạch này được ghi trước DD, marker map và ảnh chú thích. **Phiên:** chỉ xử lý GS-01.

## 1. Mục tiêu, phạm vi và nguồn

- Hoàn thiện riêng DD cho trang khám phá danh sách khóa học, giữ nguyên hai source asset, đánh dấu mọi component nhìn thấy trong ảnh mặc định và truy vết các hành vi tới inventory, AC, catalog, source và tests.
- Không thay đổi API/DDL hoặc thêm field, route, data, cache rule hay UI control chưa có căn cứ. Ghi riêng target design và current source; chưa giải quyết thay Product/BE các discrepancy.
- Inventory: route đề xuất `/courses`; AC-03; API #05/#06; links GS-02 và GS-03; Guest/public; W0/P0; grid/list, sort, paging, result count và course-detail navigation. Inventory yêu cầu #05 cache-first theo locale rồi #06 page 1/size 20; không gửi category khi #06 chưa hỗ trợ.
- AC-03: Guest; điều kiện có khóa học public; hậu điều kiện là danh sách theo filter/pagination. F02 nối SH-01 → GS-01/GS-02 → GS-03; tìm kiếm riêng dùng GS-02/#07; click course dự kiến tới GS-03.
- Assets hiện có trước phiên: `screen.png` (1280×1114, SHA-256 `3ad9b03ef8862cc09e8879c3009318b097a6d7217b86f9144201ef10bb6251c7`) và `code.html` (SHA-256 `d354d54db1ff21f8df8dd71fbf57c4836e751a0b021d76461d0c855968038fe5`). Thư mục chưa có plan/DD/annotated image/marker map. Giữ nguyên bytes của ảnh và HTML.
- Current checkout có `apps/study-client/docs`, `dist`, `node_modules` và `tsconfig.tsbuildinfo`, nhưng không có Study app source, `package.json`, router hoặc entrypoint. Không dùng `dist` hay HTML prototype làm runtime evidence. `.agents/web-work/study/AGENTS.md` và `INDEX.md` hiện tồn tại, được manifest đăng ký là `study-web: UNWIRED`; chúng mô tả đúng việc thiếu app source và không chứng minh route/runtime. Study OpenAPI chỉ là README placeholder (`NOT_FOUND`).
- Skill registry xác nhận Web UI-only DD không có skill canonical; `createDD-markdown` loại trừ `web-ui-only-dd`. Không áp template API DD cho màn hình này.

## 2. Expected behavior và current evidence

| Hạng mục | Expected theo inventory/AC/catalog | Current source và xử lý trong DD |
|---|---|---|
| Route/actor | `/courses` là route đề xuất; Guest/public; liên kết GS-02, GS-03. | Không có Study Web route/router. Anchor trong HTML đều `href="#"`; `data-path` chỉ là metadata mock. Ghi route là proposal, không tuyên bố đã hoạt động. |
| Nạp danh mục #05 | GET public `/api/v1/categories`, optional `locale`; category chips chỉ là dữ liệu/cache theo inventory, không phải filter đang chạy. | Source dùng `vi-VN` nếu locale bị bỏ qua; query lấy category `ACTIVE`, locale match chính xác, `id ASC`; trả `DESIGN_RESOURCE_RETRIEVED` + `CategoryPage`, kể cả rỗng. Không có client cache/runtime source; cache TTL/invalidation chưa được quy định. |
| Nạp khóa học #06 | GET public `/api/v1/courses`; page=1, size=20; sort/pagination theo inventory; chỉ khóa học public. | Source chỉ đọc `PUBLISHED`, mặc định page=1/size=20, size 1..100, sort allowlist `id/name/price/created_at` + `asc/desc`, mặc định `created_at DESC, id ASC`. Mọi `category != null` bị validator từ chối bằng 422 trước DB. |
| Course data | Catalog `Course`: `id`, `title`, optional description/thumbnail, decimal-string price, status, mentor, optional category. | Current #06 response có `id`, `title`, `description?`, `thumbnail_url?`, `price` decimal string, `status`, `mentor{id,full_name,avatar_url?}`; không có `category`. Không có currency/rating/duration/lesson-count trong response. Không tự hiển thị field/copy chưa có dữ liệu. |
| Loaded list / sort / pagination | AC-03 và inventory yêu cầu danh sách, sort, paging, result count. | Screenshot hiện có chỉ là empty-state; HTML để filter/category/sort toolbar, card grid và pagination thành comment trống, không có card markup. Không có approved loaded-state/card composition hoặc tập tùy chọn sort/page control để chuyển thành DD triển khai. |
| Empty/error | Inventory phân biệt `loading/empty/ready/query-error`. Chỉ empty data mới hiển thị empty state. | Screenshot/HTML copy gộp “chưa có dữ liệu hoặc đang được cập nhật”. API #06 trả 200 với `items:[]` cả khi không có course lẫn page nằm ngoài phạm vi; API errors là 422/500. Không được map lỗi hoặc trang ngoài phạm vi thành “catalog rỗng”; exact copy/recovery cho empty page và lỗi chưa có thiết kế. |
| Tìm kiếm | GS-02 có route proposal `/courses/search?q=` và dùng API #07; inventory liên kết GS-01 → GS-02. | Hero button trong HTML chỉ định cập nhật count giả 4/9; không gọi API/đổi route. Script setup lỗi trước khi gắn các listener vì `filterLevel`/các ID khác không tồn tại. Cần xác nhận query handoff/normalization trước khi bật. |
| Course detail | Click course dự kiến mở GS-03 với `course_id` của item; API #08 public chỉ trả course `PUBLISHED`. | Current #08 route/module tồn tại; parse raw path, 404 invalid/missing/unpublished và trả singleton `Page<Course>` cho item published. Không có Study Web navigation để xác minh route/client handoff. |
| Assets/UI runtime | Source image là trạng thái thiết kế hiện có. `.agents/web-study/design.md` là visual target. | Screenshot empty-state không có logo Study2Work ở header, còn HTML có brand và nav item brand lặp; HTML tải Plus Jakarta Sans/Material Symbols/Tailwind CDN, trong khi guide yêu cầu Inter/system và không remote font. Ghi source discrepancy/design drift; không thay source. |

## 3. Kế hoạch element và marker

Ảnh mặc định 1280×1114 có 16 component nhìn thấy, scan theo thứ tự từ header xuống footer. Marker là hình tròn xanh `#0B5F8A`, chữ trắng đậm, stroke trắng, đường kính xấp xỉ 32px. Tọa độ target/center theo pixel gốc. Đặt marker ở gutter/khoảng trống để không che text/control; không dùng leader line. Các vùng category/sort/card/pagination không hiện trong ảnh nên không được giả làm marker; ghi là conditional/source-gap trong DD.

| # | Element ID | Component nhìn thấy | Target (x,y) | Marker center (x,y) |
|---:|---|---|---:|---:|
| 1 | `GS01-EL-01` | Header nav item `Khóa học` (active) | 355,32 | 275,32 |
| 2 | `GS01-EL-02` | Header search input + leading search icon | 726,32 | 972,32 |
| 3 | `GS01-EL-03` | Header link `Đăng nhập` | 1096,32 | 1036,32 |
| 4 | `GS01-EL-04` | Header CTA `Đăng ký` | 1204,32 | 1258,72 |
| 5 | `GS01-EL-05` | Page title `Danh sách khóa học` | 218,120 | 20,82 |
| 6 | `GS01-EL-06` | Supporting description | 300,161 | 610,143 |
| 7 | `GS01-EL-07` | Main search input + leading icon | 350,224 | 640,182 |
| 8 | `GS01-EL-08` | Main CTA `Tìm kiếm` + arrow icon | 727,222 | 810,181 |
| 9 | `GS01-EL-09` | Empty-state book illustration/icon | 640,368 | 640,303 |
| 10 | `GS01-EL-10` | Empty-state heading | 640,441 | 480,441 |
| 11 | `GS01-EL-11` | Empty-state explanatory copy | 640,475 | 878,475 |
| 12 | `GS01-EL-12` | Footer brand `Study2Work` | 85,1054 | 20,1019 |
| 13 | `GS01-EL-13` | Footer link `Trang chủ` | 980,1054 | 958,1017 |
| 14 | `GS01-EL-14` | Footer link `Khóa học` | 1062,1054 | 1041,1017 |
| 15 | `GS01-EL-15` | Footer link `Đăng nhập` | 1145,1054 | 1123,1017 |
| 16 | `GS01-EL-16` | Footer link `Đăng ký` | 1218,1054 | 1248,1017 |

HTML-only source item: header brand/link `Study2Work` is present in `code.html` but not visible in `screen.png`; document as a source discrepancy without a marker in the screenshot-based map. No marker for controls represented only by comments or JavaScript selectors.

## 4. Event plan

| Event ID | Trigger/element | Input | Processing/result |
|---|---|---|---|
| `GS01-EV-01` | Route load `/courses` | Public route; optional locale; initial page=1/size=20; no category | Expected #05 category resolution then #06 list per F02; validate each envelope and distinguish ready/empty/error. Cache behavior and whether #06 proceeds after #05 failure need an approved policy. Current page makes no request. |
| `GS01-EV-02` | Type in header search #2 | Search text string | Current input has no ID/listener/form. Desired GS-02 handoff is not wired; exact submit/key behavior and q normalization remain open. |
| `GS01-EV-03` | Type in hero input #7 | Search text string | HTML script intends to observe text, but throws earlier at a missing filter ID; no handler is attached. No API call is current. |
| `GS01-EV-04` | Click hero search #8 / press Enter | Hero input text | HTML intended fake count 4/9 only; no real filter, navigation or API. Inventory links GS-02 and its `q` route, but exact handoff requires confirmation; #07 belongs to GS-02, not an API call from GS-01 by inference. |
| `GS01-EV-05` | Change sort (expected conditional control; absent from source image/DOM) | Approved allowlisted sort key/direction | Inventory says reset page to 1 after sort/filter; current #06 accepts `id`, `name`, `price`, `created_at` with `asc/desc`, default `created_at DESC, id ASC`. UI option labels/default beyond source default need Product approval. |
| `GS01-EV-06` | Change page (expected conditional control; absent from source image/DOM) | `page:int32` (API query parsed as int); initial page=1/size=20 per inventory. Whether size can change is not specified. | Request #06 with page/size and current approved sort; map `items` and pagination. API returns 200 for out-of-range pages; recovery/clamping behavior is not specified. |
| `GS01-EV-07` | Open a course item (expected conditional card; absent from source image/DOM) | `course.id:int64` from #06 response | Proposed route `/courses/:courseId` to GS-03; no extra fields should be inferred. Current #08 accepts path and only resolves published rows; client router/handoff is absent. |
| `GS01-EV-08` | Click active header `Khóa học` #1 | No payload | Current `href="#"`; route already appears active in design, but no router/navigation runtime exists. |
| `GS01-EV-09` | Click header `Đăng nhập` #3 | No payload | `data-path="dang-nhap"`, `href="#"`; `/login` is a route proposal for SH-02, not current runtime. |
| `GS01-EV-10` | Click header `Đăng ký` #4 | No payload | `data-path="dang-ky"`, `href="#"`; `/register` is a route proposal for SH-03, not current runtime. |
| `GS01-EV-11` | Click footer nav #13–#16 | Link label | All anchors use `href="#"`; proposals are `/`, `/courses`, `/login`, `/register`. Targets require the Study router and approved navigation behavior. |

No active category filter, reset action, card click, result counter or pagination control exists in the visible screenshot/HTML DOM. The orphan script's `.category-btn`, `btnResetFilter`, `filterLevel`, `filterFormat`, `filterPrice` and `filteredCount` references are not additional visible events; document them as broken prototype source only.

## 5. State, API and cross-screen checks

- Expected states from inventory: `LOADING`, `EMPTY`, `READY`, `QUERY_ERROR`. DD will add `EMPTY_PAGE` (items empty while total>0) and `CATEGORY_ERROR`/`PARTIAL_ERROR` as evidence distinctions; exact copy and whether partial rendering is allowed are open decisions.
- API #05: public `GET /api/v1/categories`; optional `locale:string`; no body/path/auth/pagination. Omitted locale resolves to `vi-VN`; source filters `status='ACTIVE'` and exact locale, returns `200 DESIGN_RESOURCE_RETRIEVED` with `data.items` and one-page pagination. Empty is 200; invalid query 422; DB/model failure 500 `DESIGN_INTERNAL_ERROR`.
- API #06: public `GET /api/v1/courses`; optional `category:int64`, `page:int32`, `size:int32`, `sort:string`; no body/auth. Source defaults page=1/size=20, max size 100; category always returns `422 DESIGN_VALIDATION_ERROR`; default sort `created_at DESC, id ASC`; only `PUBLISHED`; response is `ApiEnvelope<Page<Course>>`; empty and out-of-range are HTTP 200; query/model/mentor integrity failures are safe 500.
- #06 current `Course` fields map only from source-backed DB row and mentor join. Catalog `category?:Category` is not present in source response. The DDL has no course-category relation; no category filter may be sent from GS-01.
- API #08 is only downstream for GS-03; no course-detail API is loaded by GS-01. Its current source response is a singleton `Page<Course>` despite the “detail” route and catalog. Keep any downstream screen discrepancy separate from the GS-01 list response.
- Public browsing has no auth/owner requirement in #05/#06. Study Web token/session/nav behavior is unavailable. No retry/timeout/cache TTL contract is evidenced.
- Current image/HTML style uses Plus Jakarta Sans/Material Symbols and Tailwind CDN; intended Study guide says Inter/system and no remote font, 1120px content target, semantic controls and responsive reflow. This is design drift, not a runtime source.

## 6. Blockers and acceptance gates

1. `GS01-B01 LOADED_STATE_DESIGN`: source image and HTML show empty state only; card, sort, result count and pagination controls/layout are missing despite AC/inventory expectations. Cannot claim DD READY without an approved loaded-state design or approved source.
2. `GS01-B02 CATEGORY_FILTER_UNSUPPORTED`: catalog/API declaration permits category, but current #06 validator rejects it and no course-category relation exists in checked-in DDL. Do not enable/send category.
3. `GS01-B03 SEARCH_HANDOFF_UNRESOLVED`: two search inputs and CTA lack working behavior; GS-02/#07/q is a screen link, but exact query handoff/normalization is unapproved; prototype fake count must not be copied.
4. `GS01-B04 PARTIAL_LOAD_AND_CACHE_POLICY`: inventory says cache-first #05 then #06; there is no client cache source/TTL or failure policy when one request fails. Do not invent behavior.
5. `GS01-B05 COURSE_SHAPE_DISCREPANCY`: reusable catalog Course includes optional category; current #06 response omits it. Currency and rating/duration fields are also absent from source.
6. `GS01-B06 EMPTY_PAGE_AND_ERROR_COPY`: API #06 can return empty `items` for both zero total and out-of-range page, while screenshot copy conflates empty and updating. Define separate error/empty-page recovery/copy before implementation.
7. `GS01-B07 STUDY_WEB_UNWIRED`: current checkout has no app source/router/package/entrypoint; no route, cache or interaction is runtime verified.
8. `GS01-B08 SOURCE_VARIANT_MISMATCH`: screenshot header omits the Study2Work brand visible in HTML; HTML has duplicate brand/nav markup and broken orphan filter script. Keep screenshot source intact; product must choose/correct source of truth.

- [x] Screen source image and HTML hashes/dimensions inventoried; originals must remain unchanged.
- [x] Current API #05/#06 source and relevant test source, API catalog, AC-03 and DDL relation checked; tests/runtime not run.
- [x] 16 ordered markers match 16 visible DD elements; annotation visually reviewed and marker overlap corrected.
- [x] DD includes visible elements, conditional events, states, API/error/navigation trace and source-backed unresolved blockers.
- [x] Static marker/element/event/link/hash/image/tracker/worklog checks pass (see session worklog).
- [ ] Screen stays `DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED` until blockers are resolved.

## 7. Session result

- Result: Source and contract trace completed; plan preceded DD and annotation. DD, ordered marker map, SVG overlay and annotated image were created; original source assets were preserved and static checks passed.
- DD status: `DD BLOCKED` until the loaded-state design, search handoff, cache/partial-error policy and category/course schema discrepancies are resolved; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`.
- Next Screen ID after this session: GS-02, in a separate session. No other Screen ID is part of this session.

### Re-audit note (2026-11-07; before DD edits)

- Corrected the prior context status: `.agents/web-work/study/AGENTS.md` and `INDEX.md` exist and the manifest registers `study-web: UNWIRED`; current `apps/study-client/` still has no editable `src/`, `package.json`, router or entrypoint. Study OpenAPI remains a `NOT_FOUND` placeholder.
- Rechecked API catalog and AC-03: both describe public category/course reads, and AC-03 shows #05 before #06. Inventory F02 says cache-first by locale, page 1/size 20 and no category until supported. Catalog `Course` has `category?:Category`, and #06 declares `category?:int64`.
- Rechecked current route/module/test source: #05 defaults omitted locale to `vi-VN`, queries exact-locale `ACTIVE` categories ordered by ID and returns one-page `Page<Category>`; #06 validates page/size/sort, rejects any non-null category with 422 before DB access, selects only `PUBLISHED`, and returns a `Course` without category. API #06 source uses Python `int`; catalog/DDL identifiers are int64/BIGSERIAL. Checked-in DDL and migrations have no course-category relation. API #08 is the public downstream detail route and only returns published courses. Relevant tests were read, not run.
- Confirmed seven GS-01 artifacts remain present. Original `screen.png` is 1280×1114 (SHA-256 `3ad9b03ef8862cc09e8879c3009318b097a6d7217b86f9144201ef10bb6251c7`); `code.html` SHA-256 `d354d54db1ff21f8df8dd71fbf57c4836e751a0b021d76461d0c855968038fe5`. Existing JSON/SVG have 16 sequential labels; the annotated image was viewed and markers remain clear of text. No marker/image edit is planned.
- Plan update precedes the DD/source-reference and event-detail corrections in this re-audit. Preserve `DD BLOCKED`, `IMPLEMENTATION BLOCKED`, and `RUNTIME NOT VERIFIED` while the existing product/API blockers remain open.
- Final audit: 16 ordered markers map 16/16 DD elements, all coordinates are in bounds, SVG labels are 1–16, 11 event sections each document input/process/output or error, 32 local DD/plan links resolve, and A–F are present. Original image/HTML hashes and 1280×1114 dimensions are unchanged; annotation was viewed. Global inventory/tracker remains 83/83. No application tests, runtime, or live schema checks were run.
