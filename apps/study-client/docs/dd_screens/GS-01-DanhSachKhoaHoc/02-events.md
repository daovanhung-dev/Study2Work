# GS-01 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-01-EV-001` | `GS01-EV-01` / `GS01-EV-01` — Khởi tạo route và nạp dữ liệu | See source event detail below |
| `GS-01-EV-002` | `GS01-EV-02` / `GS01-EV-02` — Nhập text vào search header (#2) | See source event detail below |
| `GS-01-EV-003` | `GS01-EV-03` / `GS01-EV-03` — Nhập text vào search chính (#7) | See source event detail below |
| `GS-01-EV-004` | `GS01-EV-04` / `GS01-EV-04` — Submit tìm kiếm (#8; có thể Enter từ #7) | See source event detail below |
| `GS-01-EV-005` | `GS01-EV-05` / `GS01-EV-05` — Thay đổi sort (điều kiện, chưa có element/marker) | See source event detail below |
| `GS-01-EV-006` | `GS01-EV-06` / `GS01-EV-06` — Chuyển trang (điều kiện, chưa có element/marker) | See source event detail below |
| `GS-01-EV-007` | `GS01-EV-07` / `GS01-EV-07` — Mở course card (điều kiện, chưa có card/marker) | See source event detail below |
| `GS-01-EV-008` | `GS01-EV-08` / `GS01-EV-08` — Click nav item Khóa học (#1) | See source event detail below |
| `GS-01-EV-009` | `GS01-EV-09` / `GS01-EV-09` — Click Đăng nhập (#3) | See source event detail below |
| `GS-01-EV-010` | `GS01-EV-10` / `GS01-EV-10` — Click Đăng ký (#4) | See source event detail below |
| `GS-01-EV-011` | `GS01-EV-11` / `GS01-EV-11` — Click footer navigation (#13–#16) | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 4. Sự kiện và xử lý dữ liệu

### `GS01-EV-01` — Khởi tạo route và nạp dữ liệu

- **Trigger / loại:** Page load tại route đề xuất `/courses`.
- **Điều kiện:** Guest mở catalog. Auth không bắt buộc theo route #05/#06 hiện hành. Study Web route chưa tồn tại trong checkout.
- **Input:** Locale ứng dụng nếu đã được cấu hình; query state ban đầu theo inventory `page:int32=1`, `size:int32=20`; không có `category`; sort chưa chọn. Không có query/path input được xác nhận khác.
- **Expected processing:**
  1. Tạo state loading; lấy locale từ cấu hình đã được duyệt nếu có. Không tự invent locale picker.
  2. Theo F02, đọc cache metadata #05 trước rồi resolve/network theo locale. Nếu gửi `locale` thì truyền nguyên giá trị; nếu omit, #05 default `vi-VN`. Cache policy và xử lý lỗi #05 đang mở.
  3. Gọi #06 không auth với `page=1&size=20`; không gửi category. `sort` chỉ gửi nếu có sort option đã được duyệt.
  4. Chờ response, kiểm tra HTTP và envelope `success`, `businessCode`, `data`; chỉ `DESIGN_RESOURCE_RETRIEVED` + schema hợp lệ là success source hiện tại.
  5. Map category list từ #05 vào metadata khi dùng được. Map #06 `items` và pagination; tổng PUBLISHED là `pagination.total`. Card visual mapping chưa được định nghĩa.
  6. Với `items=[]`, `total=0` vào candidate `EMPTY`; có items vào `READY`. API error vào `QUERY_ERROR`; `items=[]`, `total>0` là page rỗng/ngoài phạm vi cần state/recovery riêng, chưa được duyệt.
  7. Không retry, clamp page, render stale cache hay cho phép partial load tự động nếu chưa có policy.
- **API #05:** `GET /api/v1/categories?locale=<optional>`, public, không body/path/auth. Locale mặc định source `vi-VN`; query lấy `ACTIVE` category đúng locale, `id ASC`. HTTP 200, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `data={items:[{id:int64,name:string,slug:string,description?:string}],pagination:{page:int32,size:int32,total:int64,total_pages:int32}}`. Python model dùng `int`; catalog/DB category ID là int64. Empty cũng 200; với danh sách rỗng current metadata là page=1,size=0,total=0,total_pages=1. Query validation 422; DB/model failure 500 `DESIGN_INTERNAL_ERROR`.
- **API #06:** `GET /api/v1/courses?page=1&size=20[&sort=<field>:<direction>]`, public, không body/path/auth. Catalog khai báo `category?:int64`, `page?:int32`, `size?:int32`, `sort?:string`; source Pydantic model dùng Python `int`, nhưng validator trả 422 `DESIGN_VALIDATION_ERROR` cho mọi non-null category trước DB; không gửi. Page phải >=1; size 1..100. Sort source nhận `id|name|price|created_at` với `asc|desc`; cú pháp `field:direction`. Default SQL sort là `created_at DESC, id ASC`; sort field khác `id` thêm `id ASC` tie-breaker. Response `data={items:[{id:int64,title,description?,thumbnail_url?,price:string,status,mentor:{id:int64,full_name,avatar_url?}}],pagination:{page:int32,size:int32,total:int64,total_pages:int32}}`; Python models dùng `int`; query chỉ lấy `PUBLISHED`. Empty/out-of-range đều HTTP 200; total_pages=0 khi tổng bằng 0. Invalid query 422 `DESIGN_VALIDATION_ERROR`; DB/query/mapping/mentor-integrity error 500 `DESIGN_INTERNAL_ERROR`.
- **Error/output:** API lỗi, lỗi mạng hoặc timeout không đồng nghĩa catalog rỗng. API error shape source có `success:false`, `businessCode`, `message`, `data:null`, `meta` (có thể có `fieldErrors`), `traceId`; xử lý UX/retry/network copy chưa được duyệt. Không lưu dữ liệu ngoài category cache policy chưa định nghĩa. Đây là flow expected; current page prototype không phát request.

### `GS01-EV-02` — Nhập text vào search header (#2)

- **Element / trigger / loại:** #2; `input/change` trên header search.
- **Điều kiện tiên quyết:** Input có focus và Guest nhập nội dung. HTML hiện không có form hoặc listener cho control này.
- **Input:** Chuỗi do người dùng nhập; giới hạn, trim, debounce và quy tắc query rỗng chưa được xác nhận.
- **Xử lý:** Giữ nội dung trong control hiện tại. Không trim, debounce, đổi URL hoặc gọi API theo source. Nếu Product duyệt handoff tới GS-02, phải chốt query key, normalization, empty-query behavior, Enter behavior và URL sync trước khi implement.
- **Output / ngoại lệ:** Current state không đổi ngoài text input; không có route/API output. Không gọi #07 từ GS-01 vì #07 thuộc GS-02. Không có error mapping hiện hành.

### `GS01-EV-03` — Nhập text vào search chính (#7)

- **Element / trigger / loại:** #7; `input/change` trên ô tìm kiếm chính.
- **Điều kiện tiên quyết:** Control hiển thị và nhận text. HTML có `id="searchInput"`, nhưng script lỗi trước khi đăng ký listener cho input.
- **Input:** Chuỗi do Guest nhập; giới hạn, bắt buộc/tùy chọn, trim và debounce chưa có contract cho GS-01.
- **Xử lý:** Prototype dự định quan sát text nhưng setup dừng ở listener của các filter ID không tồn tại. Không dùng count giả 4/9, không chuẩn hóa text, không gọi #07. Handoff sang GS-02 phải theo quyết định về query semantics.
- **Output / ngoại lệ:** Current UI chỉ giữ text trong input; không thay đổi route/API state. Lỗi script không có UI error mapping; đây là lỗi của prototype, không phải lỗi API.

### `GS01-EV-04` — Submit tìm kiếm (#8; có thể Enter từ #7)

- **Element / trigger / loại:** #8 click; Enter từ #7 chỉ là candidate chưa được duyệt, không có `<form>` hiện hành.
- **Điều kiện tiên quyết:** Guest kích hoạt CTA; điều kiện bắt buộc/rỗng của text chưa được xác định.
- **Input:** Text hiện tại của #7 nếu CTA/Enter được xử lý; query key, trim, encoding và empty-query rule chưa chốt.
- **Xử lý expected:** Chỉ khi Product xác nhận, điều hướng tới GS-02 với query string đã duyệt. Inventory cho GS-02 route `/courses/search?q=` và gọi #07; F02 mô tả q trim/lowercase ở GS-02. Không gọi #07 từ GS-01 và không tự đoán normalization tại handoff.
- **Current output / ngoại lệ:** Prototype định cập nhật count giả 4/9, nhưng script throw trước khi gắn handler. Current UI không đổi URL/state, không gọi API và không có loading/error result. Query rỗng hoặc route failure chưa có policy.

### `GS01-EV-05` — Thay đổi sort (điều kiện, chưa có element/marker)

- **Trigger / loại:** Change trên control sort dự kiến; control chưa có trong PNG, DOM hoặc approved layout.
- **Input:** Giá trị sort theo allowlist backend `id|name|price|created_at` + `asc|desc`; API format `field:direction`. Không có lựa chọn label/default được duyệt. Source DB `name` maps API field `title`; UI label cần product/design decision.
- **Xử lý expected:** Validate lựa chọn trước request; inventory yêu cầu reset page về 1 sau sort/filter; giữ size đã được chốt (initial 20; có thay đổi size không được chỉ định); gọi lại #06 với sort/page/size và không gửi category. Phân tích response như EV-01, thay list và pagination nguyên tử theo behavior đã duyệt.
- **Lỗi/đầu ra:** 422 sort/page/size là validation error, không empty; 500/network là query error. Retry, restore prior list, loading affordance và copy chưa có policy. Current control/event không tồn tại; không có hành vi đang chạy.

### `GS01-EV-06` — Chuyển trang (điều kiện, chưa có element/marker)

- **Trigger / loại:** Click page control dự kiến; pagination chưa có trong source.
- **Input:** `page:int32` và `size:int32` theo API declaration; first request `page=1,size=20`. Python source model nhận `int`. Inventory không quy định user có thể đổi page size, vì vậy không giả định size selector.
- **Xử lý expected:** Kiểm tra page >=1, giữ sort hiện hành nếu có; gửi #06 với page/size/sort hiện tại, không category. Map response items + pagination. Không gọi #05 lại chỉ vì đổi page trừ khi cache policy yêu cầu sau khi được xác nhận.
- **Lỗi/đầu ra:** API trả HTTP 200 với `items=[]` khi requested page vượt total, `pagination.total` vẫn có thể >0. Recovery (clamp trang, báo hết trang hay giữ page) chưa được quyết định. 422/500/network giữ trạng thái lỗi riêng; không render empty catalog. Event/element chưa implement.

### `GS01-EV-07` — Mở course card (điều kiện, chưa có card/marker)

- **Trigger / loại:** Click card/link dự kiến sau khi một loaded-state design được duyệt.
- **Input:** `course.id:int64` theo catalog/DB, lấy từ item #06 (được biểu diễn bằng Python `int` trong source); không dùng title hoặc ID tự tạo.
- **Xử lý expected:** Mở route đề xuất GS-03 `/courses/:courseId` truyền đúng ID. GS-03 mới gọi #08; GS-01 không prefetch detail theo source hiện có. #08 source chỉ trả PUBLISHED và 404 nếu ID sai/missing/unpublished.
- **Lỗi/đầu ra:** GS-01 chưa có card markup hoặc router. Destination route và parameter casing (`courseId` vs API `course_id`) cần contract thống nhất. Không khẳng định điều hướng đã hoạt động.

### `GS01-EV-08` — Click nav item Khóa học (#1)

- **Element / trigger / loại:** #1; click navigation link.
- **Điều kiện tiên quyết:** Header được render và Guest kích hoạt nav item. Route `/courses` là proposal; current router không có trong checkout.
- **Input:** Không có payload nghiệp vụ; target dự kiến `/courses`.
- **Xử lý:** Current HTML đặt `href="#"`, không gọi handler/router/API. Khi có router được duyệt, item chỉ dẫn tới route GS-01; không nạp lại API chỉ vì click item active nếu chưa có policy.
- **Output / ngoại lệ:** Current destination không được Study Web route xác nhận; app/navigation output chưa wired. Không có API error path cho event này.

### `GS01-EV-09` — Click Đăng nhập (#3)

- **Element / trigger / loại:** #3; click anchor/navigation.
- **Điều kiện tiên quyết:** Header link hiển thị và Guest kích hoạt. `/login` là route proposal của SH-02.
- **Input:** Không có payload nghiệp vụ hoặc return context được xác nhận.
- **Xử lý:** Current anchor dùng `href="#"` và `data-path` mock; không có Study router hoặc handler. Sau khi route được duyệt/wired, chuyển tới SH-02 theo route contract; GS-01 không gọi auth API.
- **Output / ngoại lệ:** Current app không xác nhận navigation tới SH-02; không có API output/error. Return-to, history và auth redirect behavior chưa được định nghĩa.

### `GS01-EV-10` — Click Đăng ký (#4)

- **Element / trigger / loại:** #4; click anchor/navigation.
- **Điều kiện tiên quyết:** Header CTA hiển thị và Guest kích hoạt. `/register` là route proposal của SH-03.
- **Input:** Không có payload nghiệp vụ hoặc form data.
- **Xử lý:** Current anchor dùng `href="#"` và `data-path` mock; không có Study router hoặc handler. Sau khi route được duyệt/wired, chuyển tới SH-03; không submit API #01 từ GS-01.
- **Output / ngoại lệ:** Current app không xác nhận navigation tới SH-03; không có API output/error. Signup validation/response thuộc SH-03.

### `GS01-EV-11` — Click footer navigation (#13–#16)

- **Element / trigger / loại:** #13–#16; click footer anchor/navigation.
- **Điều kiện tiên quyết:** Footer links hiển thị và Guest kích hoạt một link.
- **Input:** Link label được chọn; không có payload form/query được xác nhận.
- **Xử lý:** Proposal mapping: `Trang chủ` → SH-01 `/`; `Khóa học` → GS-01 `/courses`; `Đăng nhập` → SH-02 `/login`; `Đăng ký` → SH-03 `/register`. Current anchors đều `href="#"`; không có Study router hoặc handler. Không gọi API chỉ vì chọn footer link.
- **Output / ngoại lệ:** Current app không xác nhận destination hoặc browser-history result. Route errors, deep-link và return behavior chưa có policy; không có API error mapping cho event này.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
