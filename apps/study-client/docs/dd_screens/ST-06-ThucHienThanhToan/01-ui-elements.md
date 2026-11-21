# ST-06 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-06_markers.json](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-06-EL-001` | `ST06-EL-01` | Study2Work brand link (href="/") |
| #2 | `ST-06-EL-002` | `ST06-EL-02` | Trang chủ, Khóa học, Khóa học của tôi, Tiến độ |
| #3 | `ST-06-EL-003` | `ST06-EL-03` | Đăng nhập link (href="/login") |
| #4 | `ST-06-EL-004` | `ST06-EL-04` | Đăng ký link (href="/register") |
| #5 | `ST-06-EL-005` | `ST06-EL-05` | Trang chủ, Khóa học, Kiểm tra đơn hàng, Thực hiện thanh toán |
| #6 | `ST-06-EL-006` | `ST06-EL-06` | H1 Thực hiện thanh toán and its bottom separator |
| #7 | `ST-06-EL-007` | `ST06-EL-07` | Centered white status card container |
| #8 | `ST-06-EL-008` | `ST06-EL-08` | credit_card icon |
| #9 | `ST-06-EL-009` | `ST06-EL-09` | H2 Thực hiện thanh toán |
| #10 | `ST-06-EL-010` | `ST06-EL-10` | Chưa có thông tin thanh toán để hiển thị. |
| #11 | `ST-06-EL-011` | `ST06-EL-11` | Static copy about unavailable or ended payment transaction |
| #12 | `ST-06-EL-012` | `ST06-EL-12` | Quay lại kiểm tra đơn hàng anchor (href="/student/checkout/:courseId") |
| #13 | `ST-06-EL-013` | `ST06-EL-13` | Study2Work footer brand |
| #14 | `ST-06-EL-014` | `ST06-EL-14` | Trang chủ, Khóa học, Đăng nhập, Đăng ký |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Marker CSS bounds được đo từ DOM ở viewport 1280×1024; render/annotation ở 2× (2560×2048). Full target bounds và marker centers có trong [`ST-06_markers.json`](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06_markers.json). Tất cả phần tử dưới đây là current HTML prototype; không có element payment action hoặc polling.

| ID | Tên / loại / vị trí | Thuộc tính, nguồn và điều kiện | Trạng thái / event |
|---|---|---|---|
| #1 `ST06-EL-01` | Header brand link; anchor top-left (`x=32,y=14,w=149.281,h=36` CSS px). | Mark/text Study2Work LMS Platform; `href="/"`; static. | Default/hover CSS. EV-06. Route home chưa verify. |
| #2 `ST06-EL-02` | Header primary navigation group; nav (`x=213.281,y=18,w=364.75,h=28`). | Links: Trang chủ `/`, Khóa học `/courses`, Khóa học của tôi `/student/courses`, Tiến độ `/student/progress`; static. Class `hidden xl:flex`; không có menu thay thế thấy trong HTML. | Default/hover; responsive hidden dưới `xl`. EV-06. Student links không chứng minh auth. |
| #3 `ST06-EL-03` | Header Sign In link (`x=1047.516,y=12,w=105.375,h=40`). | “Đăng nhập”; `href="/login"`; static. | Default/hover. EV-06. |
| #4 `ST06-EL-04` | Header Sign Up link (`x=1160.891,y=12,w=87.109,h=40`). | “Đăng ký”; `href="/register"`; static. | Default/hover. EV-06. |
| #5 `ST06-EL-05` | Breadcrumb nav (`x=32,y=96,w=1216,h=16`). | Anchors: Trang chủ `/`, Khóa học `/courses`, Kiểm tra đơn hàng `/student/checkout`; current “Thực hiện thanh toán” là text/span. Breadcrumb order target không có ID. | Default/hover cho anchors. EV-06. Không truyền `orderId`. |
| #6 `ST06-EL-06` | Page-title header group: H1 + separator (`x=32,y=136,w=1216,h=55`). | H1 “Thực hiện thanh toán”; lower border là style của wrapper, không phải API/data. | Static. Không có event. |
| #7 `ST06-EL-07` | Payment status card surface (`x=384,y=327.375,w=512,h=328.25`). | White rounded `div`; container cho icon, title/status copy và CTA. Không phải Payment/Operation record. | Static layout. Không có loading/disabled state trong HTML. |
| #8 `ST06-EL-08` | Credit-card icon (`x=624,y=375.375,w=32,h=32`). | Material Symbol `credit_card`; decorative/static. | Static; không biểu thị payment method hoặc server status. Không có event. |
| #9 `ST06-EL-09` | Card title H2 “Thực hiện thanh toán” (`x=550.969,y=443.375,w=178.063,h=26`). | Hard-coded heading, lặp lại page H1; không bind payment/order data. | Static. Không có event. |
| #10 `ST06-EL-10` | Status headline (`x=416,y=485.375,w=448,h=24`). | Hard-coded “Chưa có thông tin thanh toán để hiển thị.”; không map từ #17/#18 status. | Static unavailable message; không đồng nghĩa failed/cancelled. Không có event. |
| #11 `ST06-EL-11` | Supporting explanation (`x=416,y=513.375,w=448,h=42.25`). | Hard-coded message nói không tìm thấy payment khả dụng hoặc giao dịch đã kết thúc; không có source state. | Static; không có retry link hoặc provider/gateway detail. Không có event. |
| #12 `ST06-EL-12` | Return CTA anchor (`x=504.281,y=579.625,w=271.438,h=44`). | “Quay lại kiểm tra đơn hàng”, arrow icon, `href="/student/checkout/:courseId"`; placeholder path không được interpolate trong HTML. | Default/hover CSS. EV-05. Không truyền order ID. |
| #13 `ST06-EL-13` | Footer brand group (`x=32,y=968,w=148.875,h=32`). | Static Study2Work mark/text; không phải anchor. | Static. Không có event. |
| #14 `ST06-EL-14` | Footer navigation (`x=950.484,y=976,w=297.516,h=16`). | Anchors: Trang chủ `/`, Khóa học `/courses`, Đăng nhập `/login`, Đăng ký `/register`; static. | Default/hover. EV-06. |

Không có button initiate/retry, payment method selector, Order summary, Operation status, timer/polling control, Modal, redirect/callback handler hoặc transaction detail trong HTML. Không tạo thêm marker cho element dự kiến chưa có.

## 4. Conditional UI & state variations
- States theo inventory: pending/running/failed/cancelled/succeeded
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-06_thuc-hien-thanh-toan/ST-06.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
