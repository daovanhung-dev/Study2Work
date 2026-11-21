# GS-02 — Tìm kiếm khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-02` |
| Module | Guest / Discovery |
| Route | `/courses/search?q=` — Guest route now exists in Angular source; browser runtime remains unverified |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | `BLOCKED`; implementation status: `PARTIAL SOURCE` (nonempty-q #07 search subset); browser/API runtime: `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-02.md](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md), [GS-02_PLAN.md](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_PLAN.md), [GS-02_markers.json](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tìm theo q, đồng bộ URL, debounce và reset page khi query đổi.
- In-scope: GET #5 cache-first song song #7 nếu độc lập; q được trim phía UI; #7 cố định 20/page; không gửi category. **DISCREPANCY:** AC-04/API #05 DD mô tả #05 → #07; cần chốt thứ tự/cache behavior.
- Out-of-scope: Xem gate bên dưới; source wiring của search subset không đóng contract hoặc runtime gates.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-04 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tìm theo q, đồng bộ URL, debounce và reset page khi query đổi. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #05, #07
- Liên kết màn hình dự kiến: [GS-01](../GS-01-DanhSachKhoaHoc/00-overview.md), [GS-03](../GS-03-ChiTietKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | typing/loading/no-result/error |
| Current source | Study Web Angular route/caller | `SOURCE-WIRED / PARTIAL`; browser/API runtime `NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-02 source screen.png](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/screen_annotated.png))
- Luồng: GET #5 cache-first song song #7 nếu độc lập; q được trim phía UI; #7 cố định 20/page; không gửi category. **DISCREPANCY:** AC-04/API #05 DD mô tả #05 → #07; cần chốt thứ tự/cache behavior.
- Priority: P0; Gate/source status: **R**; **BLOCK:** Không khẳng định bộ lọc category đã chạy

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

### Current Study Web source re-audit (2026-11-21)

- GS-02 is routed at `/courses/search`; its current caller sends normalized nonempty `q` and `page` to public API #07, cancels the previous request when query/page changes, and validates the accepted envelope, course projection, requested page and fixed page size 20. It does not call #05, send category/facet parameters, or implement the unresolved cache/orchestration policy.
- #07's total comes from a separate COUNT query and its returned courses from a paged LIST query. GS-02 compares the item count with the expected count for the accepted page. On disagreement it preserves returned cards, hides the potentially stale total and pagination, offers a retry for the same query/page, and blocks page navigation until the reload. Matching zero/zero remains “no results”; an empty out-of-range page remains separate.
- Result-card navigation, screenshot facets/sort and six-versus-twenty page size remain unresolved against the supplied design. Browser/API/DB runtime remains unverified. This addendum supersedes older package statements that the Angular caller or route were absent; it does not close the DD design gates.

# GS-02 — Tìm kiếm khóa học

> DD status: BLOCKED  
> Implementation status: PARTIAL SOURCE; full DD implementation remains blocked
> Runtime status: RUNTIME NOT VERIFIED  
> Session scope: GS-02 only. Source trace and screen plan were completed before this DD and its annotation assets.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: 1. Tổng quan

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID | GS-02 |
| Tên | Tìm kiếm khóa học |
| Mục tiêu | Cho phép khách tìm khóa học theo từ khóa, xem kết quả và mở GS-03. Các bộ lọc, sort và phân trang hiển thị trong ảnh chỉ được triển khai khi contract tương ứng được xác nhận. |
| Actor dự kiến | Guest theo inventory và AC-04. |
| Quyền truy cập | API #05 và #07 là public. Guest `/courses/search` route now exists; no client-side permission middleware is added for this public screen. |
| Route dự kiến | `/courses/search?q=` theo list_screen.md; the route is registered in Angular source, with browser runtime still unverified. |
| Điều kiện trước | Có thể truy cập trang public; q có thể được truyền qua URL. Cách xử lý q rỗng còn mở. |
| Kết quả sau | Một trong các trạng thái prompt/typing, loading, có kết quả, không kết quả hoặc lỗi; khi người dùng mở course, truyền course ID nguồn từ API tới GS-03. |
| Màn hình liên kết | GS-01 → GS-02; GS-02 → GS-01 hoặc GS-03. Các route và chuyển trang phía client chưa được xác minh. |
| API | #05 GET /api/v1/categories; #07 GET /api/v1/courses/search. |
| Tài liệu kế hoạch | [GS-02_PLAN.md](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_PLAN.md) |
| Tài sản nguồn | [screen.png](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/screen.png), [code.html](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/code.html); cả hai được giữ nguyên. |
| Ảnh chú thích | [screen_annotated.png](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/screen_annotated.png), được tạo riêng từ screen.png. |
| Marker map | [GS-02_markers.json](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_markers.json). |

### 1.1. Bằng chứng và trạng thái hiện tại

**Expected behavior** được lấy từ [inventory màn hình](../../list_screen.md), AC-04, API catalog và tài liệu thiết kế. **Current behavior** được lấy từ source Study Server, DDL và prototype assets. Các nguồn có mâu thuẫn được giữ thành discrepancy; không tự chọn một bản làm UI chuẩn.

- screen.png (987×1600; SHA-256 6bda913843a92873f4ebed72bc45be5792c31eb38f20b80a1acd681aec04e72f) là trạng thái có q “React”, sáu card, tổng 12 kết quả, sidebar nhiều filter, sort “Phù hợp nhất”, phân trang sáu phần tử/trang, khuyến nghị lộ trình và header có tiện ích tài khoản.
- code.html (SHA-256 f1457fdb231b614cea31f2c0b9b2d42eb846ff80c333bd7dda30a5627e20c1da) là prototype Guest với header đăng nhập/đăng ký, GET form action=/courses/search, input name=q và thẻ trạng thái chưa có kết quả. HTML không có DOM của filter, card, suggestions hoặc pagination trong ảnh. Không có URL hydration, debounce, API call hay rendering kết quả. Các hàm JS rời tham chiếu ID/DOM không tồn tại hoặc không có call site.
- Study Web Angular app, package manifest, router và entrypoint hiện có. A bounded Guest group and GS-02 route/data-access caller now exist; the original image and HTML remain design/prototype assets, not runtime evidence.
- Inventory/AC yêu cầu q được chuẩn hóa, debounce/URL sync và reset trang khi q đổi; API source tự chuẩn hóa q bằng trim/lowercase. Khoảng debounce và quy tắc giữ hoa/thường trong URL hoặc field chưa được phê duyệt.
- **Expected orchestration discrepancy:** AC-04 diagram nối API #05 categories → API #07 search theo thứ tự; inventory F02 cho phép #07 chạy song song nếu độc lập, còn API #05 DD mô tả cache-first (cache hit thì bỏ request). Vì #07 không gửi category nên hai request có thể độc lập về dữ liệu, nhưng expected order/cache behavior chưa nhất quán. Current caller uses only #07; #05/cache/orchestration is not implemented.
- **Page-bound discrepancy:** API catalog khai báo `page?:int32`; current route parses Python `int`, checks only `page >= 1`, and sets no upper bound. Không có bằng chứng source xử lý giới hạn int32 hoặc offset cực lớn; cần đồng bộ contract/validator trước implementation.
- API catalog khai báo category là tùy chọn, nhưng source #07 từ chối category khác null bằng 422. G-05 trong inventory xác nhận giới hạn hiện tại; DDL được kiểm tra không có quan hệ khóa học–danh mục.
- Screenshot mô tả sáu item/trang, còn API #07 dùng cố định 20 item/trang. Các nhãn “Phù hợp nhất”, skill, duration, rating, tuition và nhiều thuộc tính card không có API/query contract tương ứng.

## Current source re-audit (2026-11-16)

- Angular registers `/courses/search` under a Guest layout. The page hydrates `q`, treats blank `q` as a prompt, submits normalized nonempty `q`, and calls public API #07 with `q` and `page` only. It renders title, optional description/thumbnail, mentor name, server totals and server pagination; it omits price because the response has no currency.
- Focused page/route tests cover prompt/no request, URL query normalization/synchronization, supported fields, API error, empty result, page reset/pagination and an out-of-range response. Study Web suite passes 127/127; production build passes with existing Student CSS budget warnings. Study Server suite passes 1,506/1,506; focused #05/#07 tests pass 29/29 using fake sessions.
- Local dev server returned HTTP 200 for `/courses/search`; the browser extension could not inspect the page, and API proxy target `127.0.0.1:3003` had no listener. Browser rendering and live API/DB integration remain `NOT VERIFIED`.
- `DD BLOCKED` remains in effect: source variant, facets, relevance sort, six-vs-twenty page size, card schema, empty-query approval, #05 cache/orchestration, navigation destinations and API page upper bound remain open. The prompt behavior for blank `q` is an implementation assumption pending B06, not a product decision.
