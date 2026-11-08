# SH-06 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `SH-06-EV-001` | `SH06-EV-01` / `SH06-EV-01` — Mở route lỗi không khớp | See source event detail below |
| `SH-06-EV-002` | `SH06-EV-02` / `SH06-EV-02` — Ánh xạ kết quả API #08 từ GS-03 | See source event detail below |
| `SH-06-EV-003` | `SH06-EV-03` / `SH06-EV-03` — Quay về danh sách khóa học (GS-01) | See source event detail below |
| `SH-06-EV-004` | `SH06-EV-04` / `SH06-EV-04` — Quay về trang chủ (SH-01) | See source event detail below |
| `SH-06-EV-005` | `SH06-EV-05` / `SH06-EV-05` — Điều hướng header | See source event detail below |
| `SH-06-EV-006` | `SH06-EV-06` / `SH06-EV-06` — Mở toàn bộ danh sách course từ heading gợi ý | See source event detail below |
| `SH-06-EV-007` | `SH06-EV-07` / `SH06-EV-07` — Click course card | See source event detail below |
| `SH-06-EV-008` | `SH06-EV-08` / `SH06-EV-08` — Resolve danh sách gợi ý khóa học | See source event detail below |
| `SH-06-EV-009` | `SH06-EV-09` / `SH06-EV-09` — Liên hệ ban giáo vụ | See source event detail below |
| `SH-06-EV-010` | `SH06-EV-10` / `SH06-EV-10` — Footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 6. Đặc tả sự kiện

### `SH06-EV-01` — Mở route lỗi không khớp

- **Kích hoạt / loại:** Router resolve URL hoặc người dùng mở `/not-found`; `Load/Route match`.
- **Đầu vào:** `pathname`, route matcher result; không lấy ID từ text card/mock. Query/path không đưa nguyên văn vào UI.
- **Điều kiện:** Router xác định route không tồn tại, hoặc explicit SH-06 route được gọi. Client router hiện chưa có source.
- **Xử lý:** (1) Nhận kết quả match từ router; (2) không gọi API; (3) chuyển state `ROUTE_404`; (4) render status 404, title/message chung, hai CTA đã có trong inventory; (5) bỏ các params không cần thiết và không echo raw URL.
- **Kết quả:** SH-06 default state. Trực tiếp truy cập `/not-found` không làm lộ record cụ thể. Hành vi status HTTP của static host/SPA fallback chưa được source xác nhận.
- **Ngoại lệ:** Nếu router chưa có fallback, lỗi có thể do server/host trả HTML hoặc plain 404; chưa có client source để mô tả cụ thể.

### `SH06-EV-02` — Ánh xạ kết quả API #08 từ GS-03

- **Kích hoạt / loại:** GS-03 nhận HTTP response từ `GET /api/v1/courses/{course_id}`; `Response/Navigation`.
- **Đầu vào:** `course_id` từ route GS-03; HTTP status; JSON envelope; `businessCode`, `message`, `data`, `meta`, `traceId`; `X-Trace-Id` header.
- **Điều kiện:** Request thuộc course detail, không phải request gợi ý khóa học từ SH-06. SH-06 không tự fetch #08 khi mount.
- **Xử lý tuần tự:** (1) Route GS-03 parse ID theo route contract; (2) gọi GET #08; (3) parse response/envelope; (4) 200 + `DESIGN_RESOURCE_RETRIEVED`: validate Page singleton, lấy `items[0]` rồi tiếp tục GS-03; (5) 404 + `DESIGN_RESOURCE_NOT_FOUND`: không render course ID/status/reason, chuyển `RESOURCE_404` và hiển thị SH-06; (6) 403 nếu một guard ngoài #08 trả: giữ forbidden flow (SH-05), không coi là 404; (7) 500/network/timeout/invalid JSON: chuyển service-error handling riêng; (8) không cache 404 như resource truth vô thời hạn; cache TTL chưa có contract.
- **API:** #08 method/path/auth/body/query/status như mục 5.1. API current source có read-only DB query, không side effect.
- **Kết quả:** 404 state khi current business code/resource branch khớp. Không hiển thị error body thô; trace ID có thể dùng ở logging/support theo client policy nhưng prototype không có element trace display.
- **Ngoại lệ:** HTTP/body code mismatch, envelope thiếu, 404 bất ngờ, mentor mapping error trả 500, API timeout. Không retry 404; retry read 5xx/mạng chỉ theo shared client policy, không giả là not-found.

### `SH06-EV-03` — Quay về danh sách khóa học (GS-01)

- **Kích hoạt / loại:** Click #10 primary CTA; `Click/Navigation`.
- **Input:** Không có body/query; route đích `/courses` theo inventory.
- **Xử lý:** Validate route nội bộ; điều hướng GS-01. SH-06 không gọi API #05/#06; GS-01 sở hữu việc tải danh sách/filters.
- **Kết quả:** GS-01 loading/list/error theo DD của màn hình đó. Href hiện `#` nên target integration chưa tồn tại.
- **Ngoại lệ:** Route chưa đăng ký thì giữ error state hoặc router fallback; không chuyển tới external URL.

### `SH06-EV-04` — Quay về trang chủ (SH-01)

- **Kích hoạt / loại:** Click #11 hoặc brand/logo #1; `Click/Navigation`.
- **Input:** Relative route `/` từ inventory.
- **Xử lý:** Điều hướng home nội bộ; không truyền course ID, private query hoặc API response. SH-01 sở hữu API #05/#06 nếu dùng.
- **Kết quả / ngoại lệ:** SH-01 route chưa được chứng minh runtime; nếu router không xác nhận path thì không giữ href `#` như action thật.

### `SH06-EV-05` — Điều hướng header

- **Kích hoạt / loại:** Click header nav #2, login #3 hoặc register #4; `Click/Navigation`.
- **Input:** `data-path` hiện tại: home, courses, search, login hoặc register.
- **Xử lý:** Map tới route proposals từ inventory: `/`, `/courses`, `/courses/search?q=`, `/login`, `/register`; giá trị `q` mặc định và cách mở search chưa có contract. Xác nhận từng route trong router allowlist. Không gọi API từ SH-06; màn hình đích sở hữu request của mình.
- **Kết quả:** Tới trang được chọn sau khi route tồn tại. `href="#"` hiện tại không thực hiện điều hướng.
- **Ngoại lệ:** Route chưa có hoặc path ngoài allowlist: giữ state và không điều hướng ngoài site. #5 account icon không kích hoạt event vì source là div trang trí.

### `SH06-EV-06` — Mở toàn bộ danh sách course từ heading gợi ý

- **Kích hoạt / loại:** Click #14 “Xem tất cả”; `Click/Navigation`.
- **Input:** Route `/courses` theo GS-01.
- **Xử lý / output:** Cùng target với EV-03; không gọi API trong SH-06. Ở breakpoint nhỏ link bị ẩn, nhưng CTA #10 vẫn phải dùng được.
- **Ngoại lệ:** Router chưa có route thì ghi route blocker; không để anchor `#` trong production.

### `SH06-EV-07` — Click course card

- **Kích hoạt / loại:** Click card #15, #16 hoặc #17; `Click/Navigation`.
- **Input:** Current prototype chỉ có label/text/count, không có `course_id` hoặc source item. Target card cần object có ID do public course source được duyệt cấp.
- **Xử lý:** Không dùng title/mock index làm ID. Nếu card data và section được duyệt, mỗi item phải có ID từ nguồn public đã chọn rồi mới điều hướng GS-03 `/courses/{courseId}`; GS-03 gọi #08. Nếu chưa có contract, không triển khai card click; Product/UX phải chốt giữ/bỏ section thay vì tự chọn hành vi ẩn.
- **Kết quả:** Chỉ course `PUBLISHED` mới được GS-03 render. Missing/unpublished từ #08 quay lại SH-06 generic 404.
- **Ngoại lệ:** Không có data source/ID là blocker; không tạo API mới.

### `SH06-EV-08` — Resolve danh sách gợi ý khóa học

- **Kích hoạt / loại:** Render component #13/#15–#17 khi page state được dựng; `Load/data binding`.
- **Input:** Chưa có nguồn dữ liệu SH-06 được phê duyệt. HTML có 3 mock card; #08 detail chỉ trả một course và không thể cung cấp suggestions khi response 404.
- **Xử lý:** Không dùng hard-coded title/price/count làm dữ liệu thật. Product/UX phải quyết định giữ/bỏ khối, duyệt editorial content hoặc xác nhận dependency API #06 cùng quy tắc chọn/sắp xếp/copy. API #06 là public list API nhưng không có recommendation semantics trong contract SH-06. Không thêm API/field/business rule mới.
- **Kết quả / ngoại lệ:** `BLOCKED` cho tới khi có quyết định về section và data contract; không render mock values như dữ liệu runtime. API #06 source-backed không tự tạo dependency được duyệt.

### `SH06-EV-09` — Liên hệ ban giáo vụ

- **Kích hoạt / loại:** Click #19; `Click/Navigation`.
- **Input:** Contact channel/route chưa có trong inventory hoặc HTML (`href="#"`).
- **Xử lý:** Không gọi API hoặc tạo `mailto:`/route giả. Product phải xác nhận giữ/bỏ control và, nếu giữ, cung cấp support channel cùng URL/route đã duyệt.
- **Kết quả / ngoại lệ:** `BLOCKED`; prototype không điều hướng. Contact capability/route `NOT_FOUND` trong source/contract đã kiểm tra.

### `SH06-EV-10` — Footer navigation

- **Kích hoạt / loại:** Click một trong bốn anchor #21; `Click/Navigation`.
- **Input:** “Chương trình đào tạo”, “Tra cứu chứng chỉ”, “Quy chế học vụ”, “Hỗ trợ học viên”.
- **Xử lý:** Chỉ “Chương trình đào tạo” có thể map proposal `/courses`; các route còn lại không xuất hiện như screen route trong inventory. “Tra cứu chứng chỉ” không được map thành search course chỉ vì `data-path="tim-kiem"`. Product/UX phải xác nhận giữ/bỏ và route của từng link.
- **Kết quả / ngoại lệ:** Chưa có đích thì không expose link tương tác production; hiện href đều `#`. Không thêm route mới từ copy prototype.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
