# ST-22 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-22-EV-001` | `ST22-EV-01` / ST22-EV-01 — Mở trang và xác định session/context | See source event detail below |
| `ST-22-EV-002` | `ST22-EV-02` / ST22-EV-02 — Tải achievement bằng API #38 | See source event detail below |
| `ST-22-EV-003` | `ST22-EV-03` / ST22-EV-03 — Kiểm tra envelope, map response và chọn state | See source event detail below |
| `ST-22-EV-004` | `ST22-EV-04` / ST22-EV-04 — Hiển thị summary metrics | See source event detail below |
| `ST-22-EV-005` | `ST22-EV-05` / ST22-EV-05 — Chiếu Achievement thành certificate/competency cards | See source event detail below |
| `ST-22-EV-006` | `ST22-EV-06` / ST22-EV-06 — Chọn competency filter chip | See source event detail below |
| `ST-22-EV-007` | `ST22-EV-07` / ST22-EV-07 — Sao chép identifier/proof | See source event detail below |
| `ST-22-EV-008` | `ST22-EV-08` / ST22-EV-08 — Mở certificate detail | See source event detail below |
| `ST-22-EV-009` | `ST22-EV-09` / ST22-EV-09 — Tải PDF certificate | See source event detail below |
| `ST-22-EV-010` | `ST22-EV-10` / ST22-EV-10 — Chia sẻ lên LinkedIn | See source event detail below |
| `ST-22-EV-011` | `ST22-EV-11` / ST22-EV-11 — Mở QR/proof verifier | See source event detail below |
| `ST-22-EV-012` | `ST22-EV-12` / ST22-EV-12 — Next certificate / readiness / tiếp tục khóa học | See source event detail below |
| `ST-22-EV-013` | `ST22-EV-13` / ST22-EV-13 — Mở academic integrity / On-Chain Proof info | See source event detail below |
| `ST-22-EV-014` | `ST22-EV-14` / ST22-EV-14 — Header, breadcrumb và footer navigation | See source event detail below |
| `ST-22-EV-015` | `ST22-EV-15` / ST22-EV-15 — Xử lý API/session/network errors | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### ST22-EV-01 — Mở trang và xác định session/context

- **Trigger / loại:** route entry/load; gọi từ ST-20 hoặc ST-09 theo inventory, chưa có runtime caller.
- **Element / điều kiện tiên quyết:** lifecycle route `/student/achievements` (không có marker trực quan) / Student session theo contract; route guard hiện chưa có source.
- **Input:** route `/student/achievements`, app session, optional approved `course_id` context. Không có user ID path/body.
- **Điều kiện:** Student actor; route và session implementation phải được bổ sung/xác nhận.
- **Xử lý:** (1) resolve route theo app router; (2) đọc session qua shared auth contract đã duyệt; (3) giữ `course_id` chỉ nếu caller/filter semantics được xác nhận; (4) không suy `course_id` từ label/course title; (5) chuyển widget API vào `loading` khi request bắt đầu.
- **Output:** expected screen context và `loading`; hiện không có route/session guard source nên runtime output chưa được xác minh.
- **Ngoại lệ:** thiếu/hết hạn session: dự kiến API trả 401 theo catalog; redirect/login/return URL policy chưa có trong ST-22 source. Không chuyển 401 thành empty.

### ST22-EV-02 — Tải achievement bằng API #38

- **Trigger / loại:** page load hoặc refresh được xác nhận; GET.
- **Element / điều kiện tiên quyết:** lifecycle ST-22 (không có marker trực quan) / route đã mở và Student Bearer session hợp lệ theo design; actual request caller chưa được wire.
- **Input:** optional `course_id:int64`; Authorization `Bearer <Student JWT>`; không path/body. Không thêm page/size/sort.
- **Xử lý:** (1) chuẩn hóa query theo parser/range rule khi được chốt; (2) xác thực request actor là Student; (3) gửi `GET /api/v1/users/me/achievements`; (4) giữ response HTTP/business code nguyên gốc; (5) không thêm retry, cache TTL, dedupe hay timeout policy chưa có nguồn.
- **Output:** catalog success 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Page<Achievement>>`. API runtime hiện `UNWIRED / NOT_FOUND`.
- **Ngoại lệ:** catalog errors 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 500 `DESIGN_INTERNAL_ERROR`. Network/timeout là transport failure, không phải business code/API response. Catalog không có 400/404/422.

### ST22-EV-03 — Kiểm tra envelope, map response và chọn state

- **Trigger / loại:** API #38 response.
- **Element / điều kiện tiên quyết:** response lifecycle của API #38 (không có marker trực quan) / EV-02 đã gửi request và nhận response.
- **Input:** response envelope; `data.items[]` logical `Achievement(id, code, title, awarded_at, course_id?)`; pagination metadata.
- **Xử lý:** (1) kiểm tra HTTP/business success; (2) parse envelope và `items`; (3) giữ type/nullability đúng contract; (4) không diễn giải `Page.total` thành số certificate/badge; (5) chỉ khi award/projection semantics được chốt mới render item thành earned record; (6) success-empty chỉ được map `empty` sau khi empty Page shape được xác nhận; (7) cập nhật UI state sau parse thành công.
- **Output:** earned list chỉ từ server-confirmed records; hoặc `empty` nếu response là success-empty theo rule được duyệt. Hiện chưa thể hoàn tất mapping do API #38 DD draft.
- **Ngoại lệ:** malformed envelope/type/null data chưa có endpoint-specific policy; giữ `error`/diagnostic, không hiển thị sample awards hoặc fallback empty như thể API success.

### ST22-EV-04 — Hiển thị summary metrics

- **Trigger / loại:** render/update nội bộ khi data thay đổi.
- **Element / điều kiện tiên quyết:** `ST22-EL-13`…`ST22-EL-16` / metric projection và nguồn dữ liệu được phê duyệt; hiện chưa có.
- **Input:** mockup count 02 certificates, 14 skill badges, 850 reputation, Top 3%; #38 items/page metadata.
- **Xử lý:** (1) nhận diện metric nào có approved source/definition; (2) hiện không có source hoặc công thức trong #38; (3) không dùng `items.length`, `total`, `code` hoặc `course_id` để suy metric; (4) để các metric sample ở trạng thái blocked cho đến khi source/aggregation được duyệt.
- **Output:** không có giá trị production nào được phép suy ra từ #38 hiện tại; mockup number không phải runtime data.
- **Ngoại lệ:** không hiện zero khi không có data nếu zero semantics chưa chốt; không hiện stale sample trong error/empty state.

### ST22-EV-05 — Chiếu Achievement thành certificate/competency cards

- **Trigger / loại:** render collection sau EV-03.
- **Element / điều kiện tiên quyết:** `ST22-EL-19`…`ST22-EL-28`, `ST22-EL-31`…`ST22-EL-35` / response item và projection tương ứng được contract xác nhận.
- **Input:** generic `Achievement` fields từ #38; PNG card fields gồm issuer, issue date, GPA, program, hash, QR, competency, level, description.
- **Xử lý:** (1) chỉ map `id/code/title/awarded_at/course_id` vào field tương ứng sau khi projection được phê duyệt; (2) không suy `title` là certificate/course title; (3) không dựng issuer/GPA/proof/QR/taxonomy từ code hoặc nội dung mockup; (4) yêu cầu contract bổ sung trước khi render certificate hoặc competency schema; (5) không thực hiện award mutation.
- **Output:** hiện chỉ có logical Achievement shape trên tài liệu; không thể tạo card đầy đủ trong PNG một cách có căn cứ.
- **Ngoại lệ:** duplicate IDs, revoked/expired records, sort order, null `course_id`, stable `code/title` và award lifecycle chưa được #38 định nghĩa.

### ST22-EV-06 — Chọn competency filter chip

- **Trigger / loại:** click/change trên All, Specialization, Community (mockup).
- **Element / điều kiện tiên quyết:** `ST22-EL-30` / taxonomy, filter semantics và backend/client filtering policy được duyệt; hiện đây chỉ là affordance trong PNG.
- **Input:** selected chip; optional API query `course_id` có semantics khác, không phải competency type.
- **Xử lý:** (1) không gửi chip label thành query; (2) không lọc client-side trên field category không tồn tại; (3) chỉ bật filter sau khi taxonomy, combination, default, empty semantics và API/local filtering policy được duyệt; (4) khi đó cập nhật selection/loading theo contract.
- **Output:** hiện là visual affordance không có hành vi được xác nhận.
- **Ngoại lệ:** unknown category/empty filter result behavior chưa định nghĩa; không đổi state earned thành empty bằng suy đoán.

### ST22-EV-07 — Sao chép identifier/proof

- **Trigger / loại:** click copy trên verification sample card.
- **Element / điều kiện tiên quyết:** `ST22-EL-12` / identifier hợp lệ do backend/contract xác nhận và copy action được duyệt; PNG hiện chỉ có sample value.
- **Input:** identifier hiển thị trong PNG là sample; không có response field hoặc proof source trong #38.
- **Xử lý:** (1) không sao chép giá trị placeholder/sample; (2) chỉ khi contract cung cấp exact identifier và user action được duyệt, copy giá trị đó vào clipboard; (3) hiển thị success/failure feedback theo UI standard sau khi policy được định nghĩa.
- **Output:** hiện không có copy action runnable hoặc valid value.
- **Ngoại lệ:** clipboard unsupported/permission denied/failure feedback chưa có source-specific behavior; không báo “verified” khi copy thành công.

### ST22-EV-08 — Mở certificate detail

- **Trigger / loại:** click “Xem bản gốc”/view affordance trên card.
- **Element / điều kiện tiên quyết:** view action thuộc `ST22-EL-23` hoặc `ST22-EL-28` / certificate detail route, ownership và visibility policy được wire.
- **Input:** record/certificate identifier; #38 chỉ trả Achievement ID/code, chưa xác nhận certificate ID/detail route.
- **Xử lý:** (1) không lấy sample certificate code làm route param; (2) chờ route/detail source, ownership, publication và visibility rule; (3) sau approval mới navigate theo contract và truyền ID tối thiểu.
- **Output:** hiện không có destination/handoff được xác nhận.
- **Ngoại lệ:** missing/inaccessible/revoked certificate behavior và return navigation chưa được đặc tả.

### ST22-EV-09 — Tải PDF certificate

- **Trigger / loại:** click “Tải PDF Vector” trên card.
- **Element / điều kiện tiên quyết:** PDF action thuộc `ST22-EL-23` hoặc `ST22-EL-28` / authenticated file source, ownership rule và approved download contract có hiệu lực.
- **Input:** certificate/file ID hoặc URL chưa có; #38 không trả file asset.
- **Xử lý:** không tạo download URL hay file từ mockup. Cần xác nhận issuer asset route, auth/authorization, MIME/size, expiry và disposition trước khi triển khai.
- **Output:** chưa có file/download action được xác nhận.
- **Ngoại lệ:** expired URL, 403, not found, file integrity, retry và duplicate download policy chưa có endpoint source; không thêm status/business code.

### ST22-EV-10 — Chia sẻ lên LinkedIn

- **Trigger / loại:** click LinkedIn affordance.
- **Element / điều kiện tiên quyết:** LinkedIn action thuộc `ST22-EL-23` hoặc `ST22-EL-28` / payload, consent và destination được duyệt.
- **Input:** certificate title/issuer/date/verification URL và user consent; chưa có field/source contract.
- **Xử lý:** không gửi dữ liệu hoặc mở external share từ sample values. Cần phê duyệt payload, privacy/consent, destination, URL trust và behavior khi thiếu fields.
- **Output:** chưa có share target/payload được xác nhận.
- **Ngoại lệ:** cancel, popup blocked, external destination error và privacy controls chưa được định nghĩa.

### ST22-EV-11 — Mở QR/proof verifier

- **Trigger / loại:** click QR hoặc proof affordance.
- **Element / điều kiện tiên quyết:** QR/proof element thuộc `ST22-EL-22` hoặc `ST22-EL-27` / verifier authority, URL và verification contract được xác nhận.
- **Input:** QR/hash sample từ PNG; #38 không chứa verifier URL, signature hoặc proof data.
- **Xử lý:** không decode sample thành trust assertion. Chỉ khi approved verifier/issuer contract có endpoint, signature/verification semantics và destination allowlist mới điều hướng/hiển thị result.
- **Output:** hiện không thể xác nhận authenticity, tamper status hoặc ledger inclusion.
- **Ngoại lệ:** invalid/expired/untrusted QR, remote verifier unavailable và tampered proof handling chưa có contract.

### ST22-EV-12 — Next certificate / readiness / tiếp tục khóa học

- **Trigger / loại:** panel render hoặc click CTA.
- **Element / điều kiện tiên quyết:** panel `ST22-EL-36`…`ST22-EL-38`, CTA `ST22-EL-39` / eligibility/progress source và target route được duyệt; hiện chỉ là mockup.
- **Input:** sample 72%, estimated date, prerequisite cards, course/lesson destination; không có field/route mapping trong #38.
- **Xử lý:** (1) không tính readiness/date; (2) không suy prerequisite completion từ achievement count; (3) không navigate bằng sample course label; (4) chỉ khi progress/eligibility API and route contract được duyệt mới map source state và CTA.
- **Output:** panel/CTA là mockup proposal, không phải computed eligibility.
- **Ngoại lệ:** stale progress, prerequisite unavailable, course not accessible và no-next-course behavior chưa được định nghĩa.

### ST22-EV-13 — Mở academic integrity / On-Chain Proof info

- **Trigger / loại:** click callout link.
- **Element / điều kiện tiên quyết:** `ST22-EL-40` / canonical destination/content authority được xác nhận.
- **Input:** label “Tìm hiểu tiêu chuẩn On-Chain Proof”; destination/content source absent.
- **Xử lý:** không tạo external/internal URL theo suy luận; chỉ navigate sau khi canonical destination và content authority được duyệt.
- **Output:** hiện là informational affordance không hoạt động.
- **Ngoại lệ:** destination unavailable/unsafe và return context chưa có policy.

### ST22-EV-14 — Header, breadcrumb và footer navigation

- **Trigger / loại:** click anchor/nav/logo/legal/support labels.
- **Element / điều kiện tiên quyết:** `ST22-EL-01`…`ST22-EL-04`, `ST22-EL-07`, `ST22-EL-41`…`ST22-EL-46` / route map and role guard được wire; một số labels chỉ có trên PNG.
- **Input:** visible labels; inventory links ST-20/ST-09; HTML empty prototype có back-to-progress anchor. Các destination khác không được xác nhận.
- **Xử lý:** (1) phân biệt inventory relationship với actual href; (2) hiện không khẳng định nav routes đã wired; (3) trước implementation chốt route map, back behavior, role guard, return context và legal/support destinations; (4) không truyền achievement payload qua URL trừ khi route contract yêu cầu.
- **Output:** current HTML có static back anchor; app navigation runtime chưa xác minh.
- **Ngoại lệ:** direct deep link, unauthorized route, missing screen và expired session cần shared routing/auth policy; không tự gán 404/403.

### ST22-EV-15 — Xử lý API/session/network errors

- **Trigger / loại:** response/error từ EV-02 hoặc route auth.
- **Element / điều kiện tiên quyết:** response lifecycle/API error boundary của #38 (không có marker trực quan) / EV-02 request đã bắt đầu hoặc route auth đã được đánh giá.
- **Input:** catalog HTTP/business codes, transport failures, parse failures.
- **Xử lý:** (1) giữ 401 `DESIGN_AUTHENTICATION_REQUIRED` thành auth/session error và dùng shared recovery policy khi có; (2) giữ 403 `DESIGN_ACCESS_DENIED` là access denied; (3) giữ 500 `DESIGN_INTERNAL_ERROR` là service error; (4) network/timeout/parse được phân biệt ở UI transport layer, không giả mã API; (5) lỗi không thay bằng empty hoặc mock earned data; (6) retry/cache policy chờ quyết định.
- **Output:** inventory state `error`; thông điệp/recovery CTA cụ thể chưa được chốt.
- **Ngoại lệ:** API catalog không định nghĩa 400/404/422, retry limit, timeout, stale cache hoặc partial success; không tự đưa vào API behavior.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
