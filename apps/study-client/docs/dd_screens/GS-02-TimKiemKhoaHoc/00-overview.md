# GS-02 — Tìm kiếm khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `GS-02` |
| Module | Guest / Discovery |
| Route | `/courses/search?q=` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: DD status: BLOCKED; Implementation status: IMPLEMENTATION BLOCKED; Runtime status: RUNTIME NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [GS-02.md](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02.md), [GS-02_PLAN.md](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_PLAN.md), [GS-02_markers.json](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/GS-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tìm theo q, đồng bộ URL, debounce và reset page khi query đổi.
- In-scope: GET #5 cache-first song song #7 nếu độc lập; q được trim phía UI; #7 cố định 20/page; không gửi category. **DISCREPANCY:** AC-04/API #05 DD mô tả #05 → #07; cần chốt thứ tự/cache behavior.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

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
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [GS-02 source screen.png](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/02_guest_discovery/GS-02_tim-kiem-khoa-hoc/screen_annotated.png))
- Luồng: GET #5 cache-first song song #7 nếu độc lập; q được trim phía UI; #7 cố định 20/page; không gửi category. **DISCREPANCY:** AC-04/API #05 DD mô tả #05 → #07; cần chốt thứ tự/cache behavior.
- Priority: P0; Gate/source status: **R**; **BLOCK:** Không khẳng định bộ lọc category đã chạy

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# GS-02 — Tìm kiếm khóa học

> DD status: BLOCKED  
> Implementation status: IMPLEMENTATION BLOCKED  
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
| Quyền truy cập | API #05 và #07 là public; chưa có Study Web router/middleware để xác minh quyền ở client. |
| Route dự kiến | /courses/search?q= theo list_screen.md. Đây là route proposal, chưa được nối vào ứng dụng web trong checkout hiện tại. |
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
- Checkout hiện không có Study Web app source, package manifest, router hoặc entrypoint. Vì vậy ảnh và HTML là tài sản thiết kế/prototype; không phải bằng chứng runtime.
- Inventory/AC yêu cầu q được chuẩn hóa, debounce/URL sync và reset trang khi q đổi; API source tự chuẩn hóa q bằng trim/lowercase. Khoảng debounce và quy tắc giữ hoa/thường trong URL hoặc field chưa được phê duyệt.
- **Expected orchestration discrepancy:** AC-04 diagram nối API #05 categories → API #07 search theo thứ tự; inventory F02 cho phép #07 chạy song song nếu độc lập, còn API #05 DD mô tả cache-first (cache hit thì bỏ request). Vì #07 không gửi category nên hai request có thể độc lập về dữ liệu, nhưng expected order/cache behavior chưa nhất quán. Current Study Web không có client orchestration source để xác nhận runtime.
- **Page-bound discrepancy:** API catalog khai báo `page?:int32`; current route parses Python `int`, checks only `page >= 1`, and sets no upper bound. Không có bằng chứng source xử lý giới hạn int32 hoặc offset cực lớn; cần đồng bộ contract/validator trước implementation.
- API catalog khai báo category là tùy chọn, nhưng source #07 từ chối category khác null bằng 422. G-05 trong inventory xác nhận giới hạn hiện tại; DDL được kiểm tra không có quan hệ khóa học–danh mục.
- Screenshot mô tả sáu item/trang, còn API #07 dùng cố định 20 item/trang. Các nhãn “Phù hợp nhất”, skill, duration, rating, tuition và nhiều thuộc tính card không có API/query contract tương ứng.
