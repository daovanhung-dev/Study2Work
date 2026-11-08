# GS-07 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-07_markers.json](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-07-EL-001` | `GS07-EL-01` | Header brand, primary navigation, authentication links and profile icon |
| #2 | `GS-07-EL-002` | `GS07-EL-02` | Breadcrumb links for resource list and GS-06 |
| #3 | `GS-07-EL-003` | `GS07-EL-03` | API #12 blocked status badge |
| #4 | `GS-07-EL-004` | `GS07-EL-04` | Resource identifier card, safe description and proposed route badge |
| #5 | `GS-07-EL-005` | `GS07-EL-05` | API #12 protocol reference card |
| #6 | `GS-07-EL-006` | `GS07-EL-06` | Security hand-off standards list |
| #7 | `GS-07-EL-007` | `GS07-EL-07` | Secure viewer toolbar and document label |
| #8 | `GS-07-EL-008` | `GS07-EL-08` | Disabled zoom-in control |
| #9 | `GS-07-EL-009` | `GS07-EL-09` | Disabled zoom-out control |
| #10 | `GS-07-EL-010` | `GS07-EL-10` | Disabled fullscreen control |
| #11 | `GS-07-EL-011` | `GS07-EL-11` | Gated empty preview panel and explanation |
| #12 | `GS-07-EL-012` | `GS07-EL-12` | Access unresolved status badge |
| #13 | `GS-07-EL-013` | `GS07-EL-13` | Viewer security rule and client scope strip |
| #14 | `GS-07-EL-014` | `GS07-EL-14` | Safe resource release information callout |
| #15 | `GS-07-EL-015` | `GS07-EL-15` | Disabled resource download button |
| #16 | `GS-07-EL-016` | `GS07-EL-16` | Return to GS-06 resource list link |
| #17 | `GS-07-EL-017` | `GS07-EL-17` | Hand-off matrix heading and state guidance |
| #18 | `GS-07-EL-018` | `GS07-EL-18` | Loading state simulator tab |
| #19 | `GS-07-EL-019` | `GS07-EL-19` | Gated state simulator tab |
| #20 | `GS-07-EL-020` | `GS07-EL-20` | Ready signed-URL simulator tab |
| #21 | `GS-07-EL-021` | `GS07-EL-21` | 403 forbidden simulator tab |
| #22 | `GS-07-EL-022` | `GS07-EL-22` | 404 not-found simulator tab |
| #23 | `GS-07-EL-023` | `GS07-EL-23` | 410 expired-link simulator tab |
| #24 | `GS-07-EL-024` | `GS07-EL-24` | Selected hand-off state detail panel |
| #25 | `GS-07-EL-025` | `GS07-EL-25` | Static WCAG and Ocean rhythm badge |
| #26 | `GS-07-EL-026` | `GS07-EL-26` | Footer brand, navigation and copyright |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Marker IDs và target coordinates được lưu trong `GS-07_markers.json`; ảnh gốc giữ trong cùng thư mục. Mỗi marker ánh xạ đúng một hàng dưới đây.

| Marker / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, dữ liệu, hiển thị và trạng thái | Sự kiện |
|---|---|---|---|
| #1 `GS07-EL-01` | Toàn bộ header: brand, primary navigation, đăng nhập/đăng ký và profile icon. | Logo/nav/auth anchors đều `href="#"` với `data-path`; avatar là `div`/icon, không có handler/session. Header là tĩnh; responsive behavior chưa được kiểm chứng. | `GS07-EV-06`. |
| #2 `GS07-EL-02` | Breadcrumb tài nguyên khóa học → GS-06 danh sách. | Hai anchors `href="#"`, `data-path="khoa-hoc"`; không có course/resource ID hoặc route. Breadcrumb cuối GS-07 là badge/text hiện hành, không phải link. | `GS07-EV-05`. |
| #3 `GS07-EL-03` | Badge trạng thái API #12 ở góc phải breadcrumb. | Copy `API #12 • BLOCKED (SIGNED URL PENDING)` là hand-off text viết cứng; không phản ánh health/runtime của API. | Không có event. |
| #4 `GS07-EL-04` | Thẻ định danh resource: shield, `:resourceId`, mô tả an toàn và route badge. | `:resourceId` là placeholder literal trong HTML; không được hydrate. Copy nói không lộ physical path, bucket hoặc metadata size; route badge `/resources/:resourceId` là proposed route, chưa wired. | Không có event. |
| #5 `GS07-EL-05` | Thẻ tham chiếu giao thức API #12. | Hiển thị `GET /resources/{resource_id}`, host mẫu `api.study2work.edu.vn`, `Auth: Bearer <access_token>` và signed URL/RBAC pending. Current catalog/source path là `/api/v1/resources/{resource_id}`, public/no Bearer. Card có discrepancy; không làm executable contract. | Không có event. |
| #6 `GS07-EL-06` | Danh sách quy chuẩn hand-off bảo mật trong API card. | Static copy: không lộ bucket private, không tạo file size/expiry giả, flat minimal UI. Hữu ích như design intent; không phải backend guarantee hoặc verified security control. | Không có event. |
| #7 `GS07-EL-07` | Viewer toolbar và nhãn “Khung hiển thị bảo mật”. | Khung tĩnh có biểu tượng file; không có iframe/media node hoặc loaded file. | Không có event riêng. |
| #8 `GS07-EL-08` | Nút zoom in trong viewer toolbar. | Semantic `<button>` kích thước 32×32px (`w-8 h-8`), `disabled`; không đổi viewer scale. | `GS07-EV-02` — không có click action khi disabled. |
| #9 `GS07-EL-09` | Nút zoom out trong viewer toolbar. | Semantic `<button>` kích thước 32×32px (`w-8 h-8`), `disabled`; không đổi viewer scale. | `GS07-EV-02`. |
| #10 `GS07-EL-10` | Nút fullscreen trong viewer toolbar. | Semantic `<button>` kích thước 32×32px (`w-8 h-8`), `disabled`; không gọi Fullscreen API hoặc đổi layout. | `GS07-EV-02`. |
| #11 `GS07-EL-11` | Empty/gated viewer panel: icon khóa, heading và mô tả. | Initial copy `Xem trước chưa khả dụng`; yêu cầu xác thực quyền và signed URL; không có file name/preview. Nội dung tĩnh; không chứng minh resource thiếu hoặc API response. | Không có event. |
| #12 `GS07-EL-12` | Badge `DESIGN_ONLY + ACCESS_UNRESOLVED`. | Static warning về trạng thái hand-off; không phải giá trị API hoặc backend state. | Không có event. |
| #13 `GS07-EL-13` | Security rule strip và `Client Scope: Read-Only Check`. | Static copy `Zero Information Disclosure`; tuyên bố không được xác minh bằng runtime. Client không có request/permission check. | Không có event. |
| #14 `GS07-EL-14` | Callout “Cơ chế phát hành tên an toàn”. | Static copy yêu cầu khóa tải tới khi backend cấp chữ ký hợp lệ; nói controls đáp ứng WCAG AA ≥44px. Hiện source controls preview disabled; compliance chưa được đo. | Không có event. |
| #15 `GS07-EL-15` | Nút “Tải xuống tài nguyên”. | Button `disabled` và `aria-disabled="true"`; không có href/filename/request. Không kích hoạt download. | `GS07-EV-03`. |
| #16 `GS07-EL-16` | Nút/link quay lại danh sách GS-06. | Anchor `href="#"`, `data-path="khoa-hoc"`; không truyền `resourceId`, `courseId`, `lessonId` hoặc source route. | `GS07-EV-04`. |
| #17 `GS07-EL-17` | Handoff matrix title, state count và hướng dẫn. | Copy tĩnh `6 states`; là số tab simulator, không phải số runtime states/API outcomes đã xác minh. | Không có event. |
| #18 `GS07-EL-18` | Tab Loading State. | Button `tab-loading`; click gọi local `switchHandOffState('loading')`. Thay text mô tả shimmer/busy/disabled; không tạo loading thực hoặc API call. | `GS07-EV-07`. |
| #19 `GS07-EL-19` | Tab Gated (Hiện tại). | `tab-gated`; local handler đặt title/copy và code `HTTP 423 Locked / Status: D - DESIGN_ONLY`. Initial screenshot ghi `HTTP 423 Locked / 501 Blocked Implementation`; cả hai chỉ là mock. | `GS07-EV-07`. |
| #20 `GS07-EL-20` | Tab 200 Ready (Signed URL). | `tab-ready`; local handler mô tả PDF/media, enabled download và sample `signed_url`/`expires_in: 3600`; không enable control hoặc render URL. | `GS07-EV-07`. |
| #21 `GS07-EL-21` | Tab 403 Forbidden. | `tab-403`; local handler hiển thị `AUTH_RESOURCE_UNAUTHORIZED`; current #12 catalog/source không khai báo 403. | `GS07-EV-07`. |
| #22 `GS07-EL-22` | Tab 404 Not Found. | `tab-404`; local code `RESOURCE_NOT_FOUND` khác current code `DESIGN_RESOURCE_NOT_FOUND`; status 404 có trong API hiện tại. | `GS07-EV-07`. |
| #23 `GS07-EL-23` | Tab 410 URL Expired. | `tab-expired`; local code ghi `HTTP 410 Gone / 401 Signature Expired`; current #12 không có 410/401 expiry contract. | `GS07-EV-07`. |
| #24 `GS07-EL-24` | State detail box: title, description, response/code sample. | JS local thay `detail-title`, `detail-desc`, `detail-code` bằng text. Initial gated text không trùng handler gated. Không parse status, response hoặc request. | `GS07-EV-07`. |
| #25 `GS07-EL-25` | Badge chất lượng `WCAG AA Contrast Verified` / `Ocean 4px Rhythm`. | Static badge; không chứng minh contrast/focus/touch-target audit. `.agents/web-study/design.md` là target design, không phải runtime proof. | Không có event. |
| #26 `GS07-EL-26` | Footer brand, navigation và copyright. | Text tĩnh; bốn footer anchors có `href="#"`/`data-path`; copyright `© 2025`. Không có footer route/config source. | `GS07-EV-08`. |

## 4. Conditional UI & state variations
- States theo inventory: loading/ready/403-unclear/404/link-expired
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-07_xem-tai-tai-nguyen/GS-07.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
