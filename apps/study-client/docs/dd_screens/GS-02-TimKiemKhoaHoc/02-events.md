# GS-02 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `GS-02-EV-001` | `GS02-EV-01` / GS02-EV-01 — Khởi tạo route / tải dữ liệu | See source event detail below |
| `GS-02-EV-002` | `GS02-EV-02` / GS02-EV-02 — Nhập hoặc thay đổi từ khóa | See source event detail below |
| `GS-02-EV-003` | `GS02-EV-03` / GS02-EV-03 — Xóa từ khóa | See source event detail below |
| `GS-02-EV-004` | `GS02-EV-04` / GS02-EV-04 — Submit form / nhấn Enter | See source event detail below |
| `GS-02-EV-005` | `GS02-EV-05` / GS02-EV-05 — Chọn suggestion chip | See source event detail below |
| `GS-02-EV-006` | `GS02-EV-06` / GS02-EV-06 — Đổi checkbox danh mục | See source event detail below |
| `GS-02-EV-007` | `GS02-EV-07` / GS02-EV-07 — Đổi skill, duration, rating hoặc tuition | See source event detail below |
| `GS-02-EV-008` | `GS02-EV-08` / GS02-EV-08 — Áp dụng filter | See source event detail below |
| `GS-02-EV-009` | `GS02-EV-09` / GS02-EV-09 — Reset filter | See source event detail below |
| `GS-02-EV-010` | `GS02-EV-10` / GS02-EV-10 — Xóa chip filter / clear all | See source event detail below |
| `GS-02-EV-011` | `GS02-EV-11` / GS02-EV-11 — Thay đổi sort | See source event detail below |
| `GS-02-EV-012` | `GS02-EV-12` / GS02-EV-12 — Chuyển grid/list | See source event detail below |
| `GS-02-EV-013` | `GS02-EV-13` / GS02-EV-13 — Mở khóa học từ kết quả | See source event detail below |
| `GS-02-EV-014` | `GS02-EV-14` / GS02-EV-14 — Chuyển trang | See source event detail below |
| `GS-02-EV-015` | `GS02-EV-15` / GS02-EV-15 — Header nav hoặc breadcrumb | See source event detail below |
| `GS-02-EV-016` | `GS02-EV-16` / GS02-EV-16 — Dùng global header search | See source event detail below |
| `GS-02-EV-017` | `GS02-EV-17` / GS02-EV-17 — Notification/avatar/account utilities | See source event detail below |
| `GS-02-EV-018` | `GS02-EV-18` / GS02-EV-18 — CTA lộ trình / hỏi cố vấn | See source event detail below |
| `GS-02-EV-019` | `GS02-EV-19` / GS02-EV-19 — Link footer | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Sự kiện

### GS02-EV-01 — Khởi tạo route / tải dữ liệu

- **Trigger/element:** route load; element #5/#7/#13.
- **Điều kiện:** route proposal hợp lệ; Guest/public. Chưa có client router.
- **Input:** q từ URL; page mặc định 1; sort tùy chọn; locale tùy chọn từ cấu hình. Category không được gửi.
- **Xử lý theo thứ tự:**
  1. Đọc q/page/sort từ URL; kiểm tra kiểu dữ liệu.
  2. Chuẩn hóa q theo expected F02 (trim/lowercase) cho request; hiển thị q theo policy chưa được chốt.
  3. Nếu q rỗng, chờ quyết định prompt hay browse-all; source #07 nếu được gọi với q rỗng trả toàn bộ PUBLISHED.
  4. Đọc cache #05 trước khi gọi network nếu client cache được thiết kế; cache key/TTL/invalidation hiện chưa xác định. Cache hit/miss behavior chưa được triển khai.
  5. Nếu policy cho phép tìm kiếm với q hiện tại, gọi #07 với q/page/sort; có thể chạy độc lập song song với #05 vì không gửi category.
  6. Kiểm tra HTTP status/business code/envelope; map items và pagination theo §4. Không biến 422/500 thành empty result.
  7. Cập nhật loading/ready/no-result/error; chỉ hiển thị field có trong response.
- **API:** #05 và #07 như §4; #07 không gọi khi policy empty-q chưa cho phép.
- **Kết quả/ngoại lệ:** partial error giữa #05/#07 chưa có policy. Runtime event chưa tồn tại trong Study Web checkout.

### GS02-EV-02 — Nhập hoặc thay đổi từ khóa

- **Trigger/element:** input/change trên #5.
- **Điều kiện:** input enabled; người dùng nhập chuỗi.
- **Input:** string q.
- **Xử lý:** nhận input → trim/lowercase theo expected F02 → khi q thực sự đổi thì reset page về 1 → đồng bộ URL → đợi debounce rồi gọi #07 nếu q không rỗng và policy đã duyệt → map response theo §4. Khoảng debounce, canonical URL casing, hủy request trước và xử lý response đến sai thứ tự chưa có contract.
- **API:** #07 với q/page=1/sort hiện hành; không gửi category/facets.
- **Kết quả/ngoại lệ:** typing/debounce/loading/ready/no-result/error theo inventory; validation/internal/network theo §4. Không khẳng định hành vi đang chạy từ HTML.

### GS02-EV-03 — Xóa từ khóa

- **Trigger/element:** clear affordance ở #5.
- **Điều kiện:** q không rỗng và control clear hiển thị.
- **Input:** q hiện tại.
- **Xử lý:** clear input → reset page=1 → đồng bộ URL theo quy tắc q rỗng → focus/selection behavior nếu được thiết kế → chờ policy empty-q.
- **API:** không gọi #07 cho đến khi có quyết định; gọi với q rỗng sẽ bỏ predicate và trả tất cả PUBLISHED.
- **Kết quả/ngoại lệ:** prompt hoặc browse-all là blocker. HTML có JS helper tham chiếu input ID không tồn tại; không có runtime handler.

### GS02-EV-04 — Submit form / nhấn Enter

- **Trigger/element:** submit #5.
- **Điều kiện:** form hợp lệ theo validation được duyệt.
- **Input:** q từ input.
- **Xử lý:** đọc q → chuẩn hóa theo policy → xác định empty-q behavior → đặt page=1 → điều hướng GET/URL sync theo route proposal → gọi #07 theo EV-01/EV-02.
- **Prototype evidence:** code.html có native GET form tới /courses/search với name=q; input không được hydrate từ URL. Native GET không chứng minh API call/results runtime.
- **Kết quả/ngoại lệ:** route/API behavior bị chặn bởi thiếu Study Web source và empty-q decision. Không tạo endpoint frontend riêng.

### GS02-EV-05 — Chọn suggestion chip

- **Trigger/element:** chip tại #6.
- **Điều kiện:** suggestion được hiển thị.
- **Input:** label/value của chip từ cấu hình cần xác nhận; hiện chỉ có text trong screenshot.
- **Xử lý:** semantics chưa xác định: điền input, submit ngay, hay cả hai. Sau khi Product chốt, dùng EV-02 hoặc EV-04; không tạo danh sách keyword mặc định từ ảnh.
- **API:** nếu được chốt thành tìm kiếm, chỉ #07 theo §4.
- **Kết quả/ngoại lệ:** hiện là UI design content, chưa có event handler trong HTML hoặc source web.

### GS02-EV-06 — Đổi checkbox danh mục

- **Trigger/element:** checkbox trong #13.
- **Điều kiện:** metadata #05 đã nạp nếu UI dùng danh mục động.
- **Input:** category id/name; id nguồn từ #05.
- **Xử lý:** metadata #05 có thể ánh xạ label, nhưng submit category qua #07 bị validator từ chối trước query DB. Không gửi request với category. Chỉ thay đổi local visual selection nếu đó là prototype; không lọc hoặc tuyên bố kết quả đã đổi.
- **API:** #05 đọc danh mục; #07 category khác null trả 422 DESIGN_VALIDATION_ERROR.
- **Kết quả/ngoại lệ:** cần sửa contract/backend/DDL hoặc bỏ facet khỏi UI trước khi triển khai filter.

### GS02-EV-07 — Đổi skill, duration, rating hoặc tuition

- **Trigger/element:** #14, #15, #16 hoặc #17.
- **Điều kiện:** facet option đang hiển thị.
- **Input:** option value theo mockup; chưa có enum/field canonical.
- **Xử lý:** không gửi API vì #07 không khai báo các query fields này; response course không có duration/rating/category/tuition tiers để xác định điều kiện phù hợp. Không lọc danh sách ở client bằng dữ liệu thiếu.
- **API:** không gọi.
- **Kết quả/ngoại lệ:** thao tác thực tế bị chặn; option list, semantics radio/checkbox và mapping cần contract.

### GS02-EV-08 — Áp dụng filter

- **Trigger/element:** button #18.
- **Điều kiện:** filter selections tồn tại.
- **Input:** category/skill/duration/rating/tuition state.
- **Xử lý:** không serialize hay submit các giá trị unsupported; giữ trạng thái không áp dụng hoặc disable control theo quyết định thiết kế chưa có. Không tự xóa selections mà không báo người dùng.
- **API:** không gọi #07; category gây 422 và các facet khác không được API nhận.
- **Kết quả/ngoại lệ:** blocker GS02-B02; không tuyên bố filtered results.

### GS02-EV-09 — Reset filter

- **Trigger/element:** reset ở #11.
- **Điều kiện:** có ít nhất một selection.
- **Input:** local filter state hiện tại.
- **Xử lý:** inventory/prototype gợi ý reset, nhưng không quy định giữ q/sort hay xóa active chips; chờ policy. HTML helper không có sidebar DOM/call site. Không gọi API chỉ vì reset.
- **API:** không gọi nếu chưa có filter contract.
- **Kết quả/ngoại lệ:** reset semantics chưa được phê duyệt.

### GS02-EV-10 — Xóa chip filter / clear all

- **Trigger/element:** #10.
- **Điều kiện:** active chip tồn tại.
- **Input:** filter key/value hoặc clear-all action; mapping chip tới filter chưa có source.
- **Xử lý:** chưa thể cập nhật query hoặc gọi API do facet contract không hỗ trợ. Cần quyết định clear-all có bao gồm q/sort hay chỉ facet.
- **API:** không gọi.
- **Kết quả/ngoại lệ:** không render active chips như filter đã áp dụng nếu backend chưa xác nhận state.

### GS02-EV-11 — Thay đổi sort

- **Trigger/element:** select #8.
- **Điều kiện:** lựa chọn ánh xạ tới sort API được duyệt.
- **Input:** field:direction.
- **Xử lý:** khi sort đổi, đặt page=1 theo inventory → cập nhật URL/state → gọi #07 với sort hiện hành. Chỉ các field/direction allowlist ở §4 được gửi. “Phù hợp nhất” không có mapping.
- **API:** #07; invalid sort trả 422 DESIGN_VALIDATION_ERROR.
- **Kết quả/ngoại lệ:** sort labels/default UI và mapping “Phù hợp nhất” cần Product/BE quyết định; không giả định source default tương đương relevance.

### GS02-EV-12 — Chuyển grid/list

- **Trigger/element:** #9.
- **Điều kiện:** results view có thể hiển thị.
- **Input:** grid hoặc list.
- **Xử lý:** đây là thay đổi presentation local, không cần API; cập nhật layout chỉ sau khi component/runtime được triển khai. Persistence qua reload chưa xác nhận.
- **API:** không gọi.
- **Kết quả/ngoại lệ:** HTML có helper nhưng selector/call site không khớp DOM; hiện không verified.

### GS02-EV-13 — Mở khóa học từ kết quả

- **Trigger/element:** card/CTA trong #12.
- **Điều kiện:** item từ response #07 có id.
- **Input:** course.id nguồn từ API.
- **Xử lý:** lấy ID của item đã chọn → điều hướng tới route proposal /courses/:courseId của GS-03 → GS-03 dùng ID theo contract riêng. Không lấy ID từ title/thumbnail hoặc mock card.
- **API:** không gọi #08 từ event này trừ khi GS-03 tự nạp detail; đó là flow của GS-03.
- **Kết quả/ngoại lệ:** không có router/client navigation hiện tại; route proposal chưa runtime-verified.

### GS02-EV-14 — Chuyển trang

- **Trigger/element:** #23.
- **Điều kiện:** có page tiếp theo/trước theo pagination response.
- **Input:** page integer ≥1, q và sort hiện hành. Catalog ghi `int32`, nhưng runtime không có upper-bound check; xem blocker GS02-B10 trước khi truyền page tùy ý.
- **Xử lý:** cập nhật page → gọi #07 với q/page/sort → giữ page size 20 cố định. Không dùng page size 6 từ screenshot. Response items rỗng với total>0 là out-of-range; recovery/clamp policy cần quyết định.
- **API:** #07; page<1 trả 422; page ngoài total pages trả 200 items rỗng và giữ total.
- **Kết quả/ngoại lệ:** với total=12, source API chỉ có một trang 20 item; page 2 như ảnh không hợp lệ về mô hình hiện hành.

### GS02-EV-15 — Header nav hoặc breadcrumb

- **Trigger/element:** #1 hoặc #4.
- **Điều kiện:** link có destination đã xác nhận.
- **Input:** route label/link.
- **Xử lý:** GS-01 là screen liên kết theo inventory; các route khác trong header/breadcrumb phải map tới screen/route được duyệt. Không suy ra destination từ text hoặc mock HTML href=#.
- **API:** không gọi từ thao tác điều hướng.
- **Kết quả/ngoại lệ:** current Study Web router absent; link behavior chưa runtime-verified.

### GS02-EV-16 — Dùng global header search

- **Trigger/element:** #2.
- **Điều kiện:** input global search được enable.
- **Input:** string.
- **Xử lý:** screenshot cho thấy ô riêng với hero input nhưng không xác định đồng bộ state/submit route. Không tạo event/API thứ hai. Khi contract quyết định rằng ô này dùng cùng search flow, gọi lại EV-02/EV-04.
- **API:** chưa gọi riêng.
- **Kết quả/ngoại lệ:** control không có trong HTML; semantics unresolved.

### GS02-EV-17 — Notification/avatar/account utilities

- **Trigger/element:** #3.
- **Điều kiện:** account utility hiển thị theo role.
- **Input:** account/session state chưa có trong GS-02 contract.
- **Xử lý:** không gọi notification/profile API hoặc mở menu/route khi chưa có screen/API dependency cụ thể. Product cần giải quyết Guest actor so với header logged-in trong screenshot.
- **API:** không có API thuộc GS-02 đã xác nhận.
- **Kết quả/ngoại lệ:** behavior và visibility theo role chưa xác định; không xem screenshot là chứng cứ actor đã đăng nhập.

### GS02-EV-18 — CTA lộ trình / hỏi cố vấn

- **Trigger/element:** #20 hoặc #21.
- **Điều kiện:** CTA được hiển thị và destination/service được xác nhận.
- **Input:** không có payload đã đặc tả.
- **Xử lý:** không tự tạo route, form, chat hay contact service. Chờ mapping tới screen/service owner.
- **API:** chưa xác định; không gọi API.
- **Kết quả/ngoại lệ:** nội dung marketing trong screenshot chưa đủ để mô tả chuyển trang.

### GS02-EV-19 — Link footer

- **Trigger/element:** link trong #25.
- **Điều kiện:** destination tồn tại trong route map đã duyệt.
- **Input:** link label.
- **Xử lý:** điều hướng theo mapping được phê duyệt; không lấy href=# của prototype làm route thật. Footer brand/accreditation tại #24 và copyright #26 không tạo event điều hướng nếu không có anchor.
- **API:** không gọi.
- **Kết quả/ngoại lệ:** destinations chưa được trace/Study Web router chưa tồn tại.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
