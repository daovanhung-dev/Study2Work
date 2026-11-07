# Kế hoạch màn hình — GS-02 Tìm kiếm khóa học

> **Trạng thái kế hoạch:** `SOURCE_TRACE_COMPLETE; PLAN_READY`. DD dự kiến `BLOCKED`; implementation `BLOCKED`; runtime `NOT VERIFIED`. Plan được lập trước DD, marker JSON và ảnh chú thích. **Phiên:** chỉ xử lý GS-02.

## Re-audit plan — 2026-11-07

- Revalidate only this existing GS-02 bundle after the GS-01 handoff; keep the one-Screen-ID-per-session boundary.
- Recheck the current inventory/global tracker, AC-04/F02 and API #05/#07 contracts against current Study Server route, validators, query, response, errors, DB artifacts and focused test source. Recheck Study Web source/wiring status and current asset hashes.
- Audit `GS-02.md`, the 26-marker map/overlay and annotated PNG for current one-to-one mapping, event input/process/output, local links, image bounds and status separation. Inspect the existing plan before any DD or annotation edit.
- Preserve `screen.png` and `code.html`. Make only evidence-backed corrections; leave the bundle and tracker unchanged where the re-audit passes. Do not run application tests or claim runtime/live-schema verification.
- Record evidence and unresolved blockers in the active dated worklog; update the global tracker/checkpoint only if current evidence changes the documented status. Do not start another Screen ID.

## 1. Mục tiêu, phạm vi và nguồn

- Hoàn thiện riêng DD cho trang tìm kiếm công khai; giữ nguyên `screen.png` và `code.html`; đánh dấu các component nhìn thấy trong ảnh gốc; truy vết event/API/data/route theo inventory, AC, catalog, source và tests.
- Inventory: GS-02 `/courses/search?q=` proposal, AC-04, APIs #05/#07, P0/W0; search theo q, URL sync, debounce, reset page khi q đổi; #05 cache-first và #07 song song nếu độc lập; UI trim q; #07 fixed 20/page; không gửi category cho tới khi BE hỗ trợ; liên kết GS-01/GS-03; states typing/loading/no-result/error.
- AC-04: actor Guest; tìm kiếm từ khu vực khám phá; input → debounce/normalize → category/search APIs → validation → query khóa học PUBLISHED → quyết định empty/results. Diagram ghi không gọi request khi keyword rỗng nếu không cần; diagram/catalog vẫn khai báo `category` nhưng current source từ chối.
- Assets trước phiên: `screen.png` 987×1600, SHA-256 `6bda913843a92873f4ebed72bc45be5792c31eb38f20b80a1acd681aec04e72f`; `code.html` SHA-256 `f1457fdb231b614cea31f2c0b9b2d42eb846ff80c333bd7dda30a5627e20c1da`. Giữ nguyên bytes của cả hai.
- Screenshot là populated state: q=`React`, filter sidebar, sáu course cards, count 12, “Phù hợp nhất”, 6 items/page, course recommendation CTA và logged-in-looking header. HTML là Guest header + GET form + no-result card; không có filter/card/result/pagination DOM. Tách discrepancy, không chọn source of truth bằng suy luận.
- Study Web hiện không có app source/package/router/entrypoint; không coi prototype HTML, source API hay route inventory là UI runtime. Project context được cập nhật trong phiên để stack và runtime Study Web không còn bị khẳng định là Vue hiện hành.
- Canonical API design `docs/lists/list_api.md` khai báo #07 optional q/category/page/sort và reusable `Course.category`; current #07 source trả 422 với category. `list_screen.md` G-05 xác nhận category filter #06/#07 chưa hoạt động. Checked-in Study DDL có categories và courses độc lập, không có course-category relation.

## 2. Expected behavior và current evidence

| Hạng mục | Expected theo inventory/AC/catalog | Current source và cách ghi trong DD |
|---|---|---|
| Actor / route | Guest, AC-04; đề xuất `/courses/search?q=`. | Screenshot header có notification/avatar và menu học tập như authenticated shell; HTML lại là Guest. Không có Study router. Role/header variant cần chốt. |
| q / debounce / URL | URL sync; debounce; reset page khi q đổi; UI trim; F02 nói trim/lowercase. | HTML có native `GET /courses/search` form `name=q`, nhưng không hydrate từ URL, không debounce và input không có ID. API #07 trim/lowercase server-side; quy tắc viết q vào URL/display và debounce interval chưa có. |
| Empty q | AC diagram khuyên không gọi khi rỗng nếu không cần; HTML gợi ý nhập keyword/quay về danh sách. | API #07 blank/omitted q được chuẩn hóa thành `None`, bỏ predicate và trả tất cả khóa học PUBLISHED. Chưa rõ empty query là prompt hay browse-all. |
| Category/facets | Category metadata từ #05; visual có lĩnh vực đào tạo, skill level, duration, min rating, tuition. | #07 từ chối mọi category khác null trước DB; không có query cho skill/duration/rating/price. DDL thiếu relation category-course. Không gửi filter unsupported. |
| Sort | Inventory yêu cầu sort. | Screenshot “Phù hợp nhất”; API chỉ nhận `id/name/price/created_at:asc|desc`, default `created_at DESC, id ASC`. Không có relevance score/field. |
| Result count / page | API #07 Page<Course>; fixed size 20, page reset khi q/sort đổi. | Screenshot hiển thị 1–6/12 và trang 1,2; API luôn 20/page (không có size parameter), nên total 12 tương ứng một trang. Catalog declares page int32, while current route uses Python int and validates only `page >= 1` with no upper bound. |
| Course card | Reusable API Course khai báo title, description, thumbnail, price, status, mentor và optional category. | Current #07 response trả id/title/description?/thumbnail_url?/price decimal string/status/mentor; không có currency/category/rating/duration/discount/tags. Screenshot values/ratings/discounts chưa có contract/data source. |
| #05 orchestration | `list_screen.md` F02 yêu cầu cache-first theo locale và cho phép #07 chạy song song nếu độc lập; API #05 DD mô tả cache hit thì bỏ request. | AC-04 activity diagram nối tuần tự #05 categories → #07 search; API #05 DD cũng ghi nạp category trước course search. Current client không có orchestration/cache source; #07 không cần response #05 khi category không gửi. Thứ tự expected giữa AC-04 và inventory/API #05 DD cần owner xác nhận; không suy ra cache hit, concurrency hay partial-load policy. |
| Results / detail | GS-02 → GS-01/GS-03; mở detail dùng course ID. | #07 source-backed; GS-03 route/#08 là destination proposal, không có frontend navigation. Screenshot cards là mock content, chưa có ID ánh xạ. |
| Promo/footer/header controls | Có mặt trong screenshot; inventory GS-02 chỉ cam kết search, filters, pagination, results. | Learning-path/advisor/header notification/avatar/footer destinations không có đủ route/service contract; HTML không có phần lớn controls. Ghi là visible design scope, chưa được xác nhận behavior. |

## 3. Kế hoạch element và marker

Ảnh mặc định 987×1600; map 26 component groups từ header xuống footer, theo mẫu DD đã dùng cho repeated UI: một marker cho reusable results grid, các item con/instances được liệt kê trong DD. Checkbox/radio từng lựa chọn được liệt kê dưới marker group, không đánh tráo chúng thành behavior API có thật.

Ảnh chú thích dự kiến render nguồn ở scale 2 với outer gutter 40px mỗi bên: canvas 2134×3200, source offset output x=80/y=0. Marker tròn xanh `#0B5F8A`, chữ trắng đậm, viền trắng, đường kính 40px output; leader line ngắn chỉ nằm trong gutter. Trường `side` quyết định gutter trái/phải; `y_source` bám gần component. Callout cùng gutter cách nhau tối thiểu 20px source (40px output); vị trí gần nhau trong panel CTA được đẩy lên/xuống để không chồng marker. Không vẽ marker lên source pixels.

| # | Element ID | Component được đánh dấu | Target source (x,y) | Gutter side / y source |
|---:|---|---|---:|---|
| 1 | `GS02-EL-01` | Header brand + primary navigation group | 340,25 | left / 18 |
| 2 | `GS02-EL-02` | Header global search input | 720,25 | right / 18 |
| 3 | `GS02-EL-03` | Header notification + avatar utility group | 945,25 | left / 42 |
| 4 | `GS02-EL-04` | Breadcrumb navigation | 145,80 | right / 79 |
| 5 | `GS02-EL-05` | Main query form: input, clear affordance, submit | 370,123 | left / 120 |
| 6 | `GS02-EL-06` | Popular keyword prompt + suggestion chips | 330,163 | right / 160 |
| 7 | `GS02-EL-07` | Search query/result summary + result-count pill | 195,221 | left / 220 |
| 8 | `GS02-EL-08` | Sort select | 833,221 | right / 220 |
| 9 | `GS02-EL-09` | Grid/list view toggle group | 950,221 | left / 240 |
| 10 | `GS02-EL-10` | Active-filter chips + clear-all affordance | 490,285 | right / 284 |
| 11 | `GS02-EL-11` | Filter sidebar heading + reset action | 140,299 | left / 299 |
| 12 | `GS02-EL-12` | Six-card search results grid (reusable card instances) | 610,330 | right / 325 |
| 13 | `GS02-EL-13` | Training-field category checkbox group | 136,388 | left / 380 |
| 14 | `GS02-EL-14` | Skill-level radio group | 130,535 | right / 515 |
| 15 | `GS02-EL-15` | Duration radio group | 130,636 | left / 630 |
| 16 | `GS02-EL-16` | Minimum-rating radio group | 135,750 | right / 745 |
| 17 | `GS02-EL-17` | Tuition checkbox group | 132,855 | left / 860 |
| 18 | `GS02-EL-18` | Apply-filter button | 134,949 | right / 950 |
| 19 | `GS02-EL-19` | Career-path recommendation panel | 610,1170 | left / 1135 |
| 20 | `GS02-EL-20` | CTA `Xem Lộ trình nghề nghiệp` | 750,1170 | right / 1170 |
| 21 | `GS02-EL-21` | CTA `Hỏi cố vấn Tech` | 890,1170 | left / 1170 |
| 22 | `GS02-EL-22` | Displayed result range `1–6 / 12` | 360,1307 | right / 1305 |
| 23 | `GS02-EL-23` | Previous/page number/next pagination group | 845,1307 | left / 1305 |
| 24 | `GS02-EL-24` | Footer brand, description and accreditation badges | 184,1462 | right / 1460 |
| 25 | `GS02-EL-25` | Footer navigation columns | 625,1460 | left / 1460 |
| 26 | `GS02-EL-26` | Copyright + enterprise-platform tagline | 500,1572 | right / 1570 |

## 4. Event plan

| Event ID | Trigger/element | Input | Processing/result / unresolved behavior |
|---|---|---|---|
| `GS02-EV-01` | Route load `/courses/search` | URL `q`, optional page/sort; locale/config if available | Restore URL state; read #05 cache-first and call #07 for non-empty normalized q; calls may be concurrent if category is not used. Empty-q state, cache miss/failure and partial rendering policy need confirmation. |
| `GS02-EV-02` | Type/change query in #5 | string q | Expected debounce and URL sync; trim/lowercase per F02; reset page=1; interval and displayed-case policy unspecified. API independently trim/lowercases. |
| `GS02-EV-03` | Clear query affordance #5 | current q | Expected clear/focus/query reset; empty-q behavior is open. Current HTML has no clear button; helper seeks absent input ID. |
| `GS02-EV-04` | Submit search form / Enter #5 | q | HTML native GET to `/courses/search?q=...`; inventory also expects API #07. Current app does not exist. Do not submit blank q as search until browse-all vs prompt policy is settled. |
| `GS02-EV-05` | Click suggestion chip #6 | suggested string | Screenshot supplies example chip labels, but no approved preset/submit semantics; no current DOM/handler. |
| `GS02-EV-06` | Change category checkbox group #13 | category ID/name | #05 can supply metadata, but #07 returns 422 for any category. Do not send request; requires BE/DB support. |
| `GS02-EV-07` | Change skill/duration/rating/tuition groups #14–17 | selected options | API #07 has no parameters for these facets; local selected state is visible in screenshot only. No submission behavior can be implemented against current API. |
| `GS02-EV-08` | Apply filters #18 | all selected filters + q | Intended search submission is blocked by unsupported filters and missing query contract; no current DOM/API behavior. |
| `GS02-EV-09` | Reset filters #11 | selected facets | Expected clear selections/active chips and reset page=1; unsupported options and q-preservation semantics need confirmation. HTML helper has no sidebar DOM/call site. |
| `GS02-EV-10` | Remove active chip / clear all #10 | filter key or clear-all | Screenshot shows removable chips; chip-to-filter mapping and whether clear-all also clears q are unapproved. |
| `GS02-EV-11` | Change sort #8 | sort field/direction | Reset page=1 per inventory; API accepts `id/name/price/created_at:asc|desc`; visible “Phù hợp nhất” has no mapping. |
| `GS02-EV-12` | Toggle grid/list #9 | `grid` or `list` | Local layout-only state, no API call expected; prototype helper references missing grid/button IDs and is never called. |
| `GS02-EV-13` | Open result card/CTA #12 | `course.id` from #07 | Proposed GS-03 route with that ID; source has no card or router and screenshot sample items do not identify API IDs. |
| `GS02-EV-14` | Previous/next/page #23 | page:int | Keep q/sort, reset/retain filters only after supported policy; #07 fixed size20, returns 200 empty for out-of-range page. Screenshot's six-per-page total conflicts. |
| `GS02-EV-15` | Click header nav/breadcrumb #1/#4 | link label | GS-01 and current route links appear in design; other destinations (learning path/forum) lack mapped route contract. HTML uses prototype paths only. |
| `GS02-EV-16` | Use global header search #2 | string | Screenshot shows a distinct input; relationship to hero q/form is unspecified and HTML omits it. Do not invent a second search API/route. |
| `GS02-EV-17` | Click notification/avatar #3 | none | Account utility has no GS-02 route/menu contract; screenshot actor/header variant is unresolved. |
| `GS02-EV-18` | Click career-path/advisor CTAs #20–21 | none | Destination/service is not specified in screen inventory/API; treat as unresolved design content. |
| `GS02-EV-19` | Click footer navigation #25 | link label | Screenshot lists destination labels; route ownership and accessible behavior are not mapped to this screen. No current client router. |

## 5. State, API and cross-screen evidence

- Inventory states: `typing`, `loading`, `no-result`, `error`. Screenshot additionally represents populated results. DD will separate initial/typing, loading, ready, no-result, query-error, category-metadata-error, and out-of-range page; exact empty-q and partial #05 policy are unresolved.
- API #05: public `GET /api/v1/categories?locale=<optional>`, no body/path/auth; default `vi-VN`; exact locale + `ACTIVE` categories ordered by id; `200 DESIGN_RESOURCE_RETRIEVED`, `data.items` plus pagination, empty success; validation 422 and DB/model 500 `DESIGN_INTERNAL_ERROR`.
- API #07: public `GET /api/v1/courses/search?q=<optional>&page=<int>&sort=<optional>`; catalog/model also declare optional `category`, but current source rejects every non-null category with `422 DESIGN_VALIDATION_ERROR`; no `size` input. Query default page=1. `q` trim/lowercase, blank means no q predicate. Sort format `field:direction`, fields `id/name/price/created_at`, direction `asc/desc`; default `created_at DESC,id ASC`. SQL binds parameters, searches `LOWER(c.name) LIKE %q%`, counts/pages only PUBLISHED courses, fixed `size=20`. Success is `ApiEnvelope<CoursePage>` with fields id, title, optional description/thumbnail_url, decimal-string price, status, mentor{id,full_name,avatar_url?}; no category/currency/rating/duration/tags/old price. Empty/out-of-range are HTTP 200; query/category validation 422; query/integrity/mapping errors 500 `DESIGN_INTERNAL_ERROR`.
- #07 tests are fake-session source: they verify q normalization, fixed page size despite `size=5`, category 422 before DB, pagination/empty/error mapping. They were read but not run. DDL is checked-in only; no live database verification.
- Cross-screen targets: return to GS-01 and open GS-03 from a result item. `/courses/search?q=` and `/courses/:courseId` are route proposals; GS-03 #08 current backend source does not wire browser navigation.

## 6. Blockers and acceptance gates

1. `GS02-B01 SOURCE_VARIANT_MISMATCH`: screenshot is loaded state while code.html is an empty-state Guest prototype; header/actor also differ. Product/Design must select/repair authoritative UI variant.
2. `GS02-B02 FACETS_UNSUPPORTED`: category produces 422; skill/duration/rating/tuition are not #07 inputs and DDL has no category relation. Do not submit visible selected filters.
3. `GS02-B03 SORT_RELEVANCE_UNSUPPORTED`: screenshot default “Phù hợp nhất” cannot map to API allowlist/default.
4. `GS02-B04 PAGE_SIZE_CONFLICT`: design paginates 6 items and shows 12 total, API fixed page size 20. Need align design or backend contract.
5. `GS02-B05 COURSE_CARD_SCHEMA`: current API lacks category, tags, currency, duration, rating and discount/old-price fields displayed in screenshot. No derived/mock values may be presented as real.
6. `GS02-B06 EMPTY_QUERY_SEMANTICS`: blank q makes API return all PUBLISHED courses, while AC/HTML may show a prompt. Decide if search route calls API for blank q and how URL/display case is normalized.
7. `GS02-B07 CACHE_AND_PARTIAL_LOAD`: AC-04 models #05 → #07 in sequence, while inventory F02/API #05 DD describe cache-first and allow independent parallel search; client source is absent, and TTL/invalidation/fallback/partial-load policy is not approved.
8. `GS02-B08 STUDY_WEB_UNWIRED`: no app source/router/package/entrypoint; no event, URL, debounce or navigation runtime is verified.
9. `GS02-B09 EXTRA_DESTINATIONS`: account utilities, learning-path/advisor promos and footer destinations have no route/service contract.
10. `GS02-B10 PAGE_RANGE_CONTRACT`: API catalog declares int32 but route uses unbounded Python int and checks only the lower bound; align contract/validation and oversized-offset behavior.

- [x] PNG/HTML dimensions and hashes inventoried; source assets retained.
- [x] API #05/#07 route, model, validator, SQL, mapper, responses, relevant tests, AC-04, catalog and checked-in DDL traced; tests not run.
- [x] 26 ordered markers match DD component groups; annotation visually reviewed for legibility/occlusion. A first render exposed overlapping callouts #19/#21; #19 was moved to y_source=1135 and the final crop has separated circles.
- [x] DD includes complete visible components, 19 event paths, states, API/error mapping and unresolved navigation/data contracts.
- [x] Static element/event/link/hash/image/tracker checks pass; the final worklog records the global context-validator result.
- [ ] Do not mark DD READY until design/source variants, facet/sort/page/card contracts and empty-query policy are resolved.

## 7. Session result

- Result: Source/API/AC trace complete; plan preceded DD and annotation. DD, ordered marker map, SVG overlay and annotated image are complete; source assets remain unchanged; static checks pass.
- DD status: `DD BLOCKED`; implementation `IMPLEMENTATION BLOCKED`; runtime `RUNTIME NOT VERIFIED`.
- Next Screen ID after this session: GS-03 in a separate session. No other Screen ID is part of this session.
