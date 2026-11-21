# ST-05 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-05_markers.json](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-05-EL-001` | `ST05-EL-01` | Study2Work brand link (href="/") |
| #2 | `ST-05-EL-002` | `ST05-EL-02` | Trang chủ, Khóa học, Khóa học của tôi, Tiến độ |
| #3 | `ST-05-EL-003` | `ST05-EL-03` | Đăng nhập link (href="/login") |
| #4 | `ST-05-EL-004` | `ST05-EL-04` | Đăng ký link (href="/register") |
| #5 | `ST-05-EL-005` | `ST05-EL-05` | Trang chủ, Khóa học, Kiểm tra ghi danh, Kiểm tra đơn hàng |
| #6 | `ST-05-EL-006` | `ST05-EL-06` | shopping_cart_checkout icon |
| #7 | `ST-05-EL-007` | `ST05-EL-07` | Centered white status card container |
| #8 | `ST-05-EL-008` | `ST05-EL-08` | H1 “Kiểm tra đơn hàng” |
| #9 | `ST-05-EL-009` | `ST05-EL-09` | “Quy trình thanh toán chưa thể bắt đầu.” |
| #10 | `ST-05-EL-010` | `ST05-EL-10` | Static unavailable-state explanatory copy |
| #11 | `ST-05-EL-011` | `ST05-EL-11` | “Quay lại kiểm tra ghi danh” anchor (href="/courses") |
| #12 | `ST-05-EL-012` | `ST05-EL-12` | Study2Work footer brand |
| #13 | `ST-05-EL-013` | `ST05-EL-13` | Trang chủ, Khóa học, Đăng nhập, Đăng ký |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker CSS bounds được đo từ DOM của HTML ở viewport 1280×1024; ảnh render và annotation ở 2× (2560×2048). Target bounds và marker centers đầy đủ ở [`ST-05_markers.json`](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05_markers.json). Tất cả element dưới đây là phần tử prototype hiện tại; phần tử xác nhận/amount/provider dự kiến nhưng chưa tồn tại không được đánh số như thể đang hiển thị.

| ID | Tên / loại / vị trí | Thuộc tính, nguồn và điều kiện | Trạng thái / event |
|---|---|---|---|
| #1 `ST05-EL-01` | Header brand link; anchor ở top-left (`x=32,y=14,w=149.281,h=36` CSS px). | Text/mark Study2Work + LMS Platform; `href="/"`; nội dung tĩnh trong HTML; luôn hiển thị ở desktop prototype. | Default/hover theo CSS. EV-06. Không xác nhận route home runtime. |
| #2 `ST05-EL-02` | Header primary navigation; nav group (`x=213.281,y=18,w=364.75,h=28`). | Bốn anchor: Trang chủ `/`, Khóa học `/courses`, Khóa học của tôi `/student/courses`, Tiến độ `/student/progress`; static. CSS `hidden md:flex`; không thấy mobile menu thay thế. | Default/hover; responsive hidden dưới breakpoint `md`. EV-06. Student links không chứng minh đã login. |
| #3 `ST05-EL-03` | Header Sign In link; anchor (`x=1031.516,y=10,w=105.375,h=44`). | Text “Đăng nhập”; `href="/login"`; static. | Default/hover. EV-06. |
| #4 `ST05-EL-04` | Header Sign Up link; anchor (`x=1144.891,y=10,w=103.109,h=44`). | Text “Đăng ký”; `href="/register"`; static. | Default/hover. EV-06. Public-shell/Student-auth discrepancy. |
| #5 `ST05-EL-05` | Breadcrumb group; nav (`x=32,y=238.25,w=1216,h=16`). | Links: Trang chủ `/`, Khóa học `/courses`, Kiểm tra ghi danh `/courses`; current text “Kiểm tra đơn hàng” is a span, not a link. Text and href static; không mang `courseId`. | Default/hover cho links. EV-06. Link “Kiểm tra ghi danh” có href không khớp nhãn. |
| #6 `ST05-EL-06` | Checkout status icon; `shopping_cart_checkout` span (`x=617.984,y=337.25,w=44.016,h=44`). | Material Symbol trong card; decorative/static, không có value hoặc click action. | Static; không biểu thị trạng thái payment server-side. Không có event. |
| #7 `ST05-EL-07` | Status card surface; centered `div` (`x=352,y=286.25,w=576,h=371.5`). | Container white card; chứa icon, title, status copy và CTA. Không phải Order entity hoặc API response. | Static layout. Không có loading/disabled state trong HTML. |
| #8 `ST05-EL-08` | H1 “Kiểm tra đơn hàng” (`x=513.266,y=423.25,w=253.453,h=38`). | Static page title; không bind course/order data. | Static. Không có event. |
| #9 `ST05-EL-09` | Status headline “Quy trình thanh toán chưa thể bắt đầu.” (`x=477.766,y=465.25,w=324.453,h=26`). | Hard-coded prototype copy; không map từ #16 hay business code. | Static unavailable copy; không được diễn giải là API error cụ thể. Không có event. |
| #10 `ST05-EL-10` | Supporting text (`x=416,y=499.25,w=448,h=45.5`). | Hard-coded: “Hệ thống chưa thể khởi tạo thông tin đơn hàng tại thời điểm này. Vui lòng kiểm tra lại điều kiện ghi danh.” Không có source/data binding. | Static; không có retry control. Không có event. |
| #11 `ST05-EL-11` | Return CTA anchor (`x=507.125,y=576.75,w=265.734,h=48`). | Label “Quay lại kiểm tra ghi danh”; includes arrow icon; `href="/courses"`; no course ID, query, return URL or state. | Default/hover/active CSS. EV-05. Label/target mismatch is unresolved. |
| #12 `ST05-EL-12` | Footer brand group (`x=32,y=968,w=148.875,h=32`). | Study2Work mark/text; static visual, not an anchor. | Static. No event. |
| #13 `ST05-EL-13` | Footer navigation; nav group (`x=950.484,y=976,w=297.516,h=16`). | Four static anchors: Trang chủ `/`, Khóa học `/courses`, Đăng nhập `/login`, Đăng ký `/register`. | Default/hover. EV-06. |

Không có Input, Select, Checkbox, Submit button, Modal, Order summary field, Provider selector hoặc confirm control trong HTML. Các control đó chỉ có thể được bổ sung sau khi có thiết kế/contract phê duyệt; không thuộc 13 marker hiện tại.

## 4. Conditional UI & state variations
- States theo inventory: confirming/order-creating/422/order-error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-05_kiem-tra-don-hang-checkout/ST-05.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
