# ST-04 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-04_markers.json](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-04-EL-001` | `ST04-EL-01` | Study2Work brand link (href="/") |
| #2 | `ST-04-EL-002` | `ST04-EL-02` | Trang chủ, Khóa học, Khóa học của tôi, Tiến độ |
| #3 | `ST-04-EL-003` | `ST04-EL-03` | Đăng nhập link (href="/login") |
| #4 | `ST-04-EL-004` | `ST04-EL-04` | Đăng ký link (href="/register") |
| #5 | `ST-04-EL-005` | `ST04-EL-05` | Trang chủ > Khóa học > Kiểm tra ghi danh |
| #6 | `ST-04-EL-006` | `ST04-EL-06` | Decorative verified_user icon |
| #7 | `ST-04-EL-007` | `ST04-EL-07` | Centered status card container |
| #8 | `ST-04-EL-008` | `ST04-EL-08` | Kiểm tra ghi danh |
| #9 | `ST-04-EL-009` | `ST04-EL-09` | Chưa thể xác nhận thông tin ghi danh. |
| #10 | `ST-04-EL-010` | `ST04-EL-10` | Hệ thống chưa thể xác định trạng thái ghi danh của khóa học này. Vui lòng quay lại danh sách khóa học hoặc thử lại sau. |
| #11 | `ST-04-EL-011` | `ST04-EL-11` | Quay lại danh sách khóa học (href="/courses") |
| #12 | `ST-04-EL-012` | `ST04-EL-12` | Study2Work footer wordmark |
| #13 | `ST-04-EL-013` | `ST04-EL-13` | Trang chủ, Khóa học, Đăng nhập, Đăng ký |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Tọa độ trong cột vị trí là bounding box CSS pixel đo trên render 1280×1024; ảnh render và annotation được xuất ở 2×. Target đầy đủ và tọa độ marker nằm trong [ST-04_markers.json](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04_markers.json). Mỗi marker tương ứng đúng một dòng dưới đây.

| # / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, nguồn dữ liệu, hiển thị/trạng thái | Event |
|---|---|---|---|
| 1 / `ST04-EL-01` | Brand Study2Work trong header; anchor tại `(32,18,116.984,28)`; quay về `/`. | Chữ tĩnh “Study2Work”; không có API/state. Visible ở prototype; focus style được khai báo, không có design state riêng ngoài mặc định/hover/focus từ CSS. | EV-06 |
| 2 / `ST04-EL-02` | Nhóm nav chính tại `(180.984,18,365.141,28)`: Trang chủ `/`, Khóa học `/courses`, Khóa học của tôi `/student/courses`, Tiến độ `/student/progress`. | Anchor tĩnh; “Khóa học” có màu/weight active nhưng không có `aria-current`. `<nav>` bị `hidden` dưới breakpoint `md`; không thấy mobile menu. Chưa xác minh route destination. | EV-06 |
| 3 / `ST04-EL-03` | Link “Đăng nhập” tại `(1047.516,14,97.375,36)`; mở `/login`. | Anchor tĩnh trong public shell; mâu thuẫn với tiền điều kiện Student đã đăng nhập. Không đọc session/role. | EV-06 |
| 4 / `ST04-EL-04` | Link “Đăng ký” tại `(1160.891,14,87.109,36)`; mở `/register`. | Anchor tĩnh trong public shell; không có event đăng ký trong ST-04. | EV-06 |
| 5 / `ST04-EL-05` | Breadcrumb group tại `(32,80,280.281,16)`: Trang chủ `/` → Khóa học `/courses` → nhãn hiện tại “Kiểm tra ghi danh”. | `<nav aria-label="Breadcrumb">`; nhãn hiện tại là span tĩnh, không có `aria-current`. Không mang course ID/filter. | EV-06 |
| 6 / `ST04-EL-06` | Icon `verified_user` tại `(608,200,64,64)` trong status card. | Icon Material Symbols trang trí theo hình ảnh; markup không có dữ liệu API hoặc trạng thái kiểm chứng. Không có alternative text/`aria-hidden` rõ ràng trong nguồn HTML. | Không có event; trạng thái tĩnh. |
| 7 / `ST04-EL-07` | Surface/card tại `(352,168,576,332)` bao quanh nội dung trạng thái. | Container layout `<div>`; không có `role="status"`/`alert`, dữ liệu hay điều khiển riêng. Trạng thái hiển thị mặc định trong prototype. | Không có event; chứa #6, #8–#11. |
| 8 / `ST04-EL-08` | H1 “Kiểm tra ghi danh” tại `(550.531,280,178.938,30)`. | Nội dung tĩnh; không nhận title từ API. Visible. | Không có event; trạng thái tĩnh. |
| 9 / `ST04-EL-09` | Headline “Chưa thể xác nhận thông tin ghi danh.” tại `(481.219,314,317.562,26)`. | `<p>` tĩnh; không phải business code/message từ #15 hay lỗi mạng. Không có role live/status. | Không có event; trạng thái tĩnh. |
| 10 / `ST04-EL-10` | Copy giải thích tại `(416,344,448,44)`: hệ thống chưa xác định được trạng thái, đề nghị quay lại hoặc thử lại sau. | `<p>` tĩnh. Có nhắc thử lại nhưng prototype không có retry control. Không có input/validation. | Không có event; trạng thái tĩnh. |
| 11 / `ST04-EL-11` | CTA anchor “Quay lại danh sách khóa học” tại `(504.906,420,270.172,48)`; href `/courses`. | Link được tạo kiểu button, có focus CSS; không truyền `courseId`, tab hoặc danh sách filter. Không có submit/mutation. | EV-05 |
| 12 / `ST04-EL-12` | Wordmark Study2Work ở footer tại `(32,972,116.984,28)`. | `<span>` chữ tĩnh, không phải link; không có API/state. | Không có event. |
| 13 / `ST04-EL-13` | Nhóm footer links tại `(950.484,978,297.516,16)`: Trang chủ `/`, Khóa học `/courses`, Đăng nhập `/login`, Đăng ký `/register`. | Bốn anchor tĩnh trong `<div>`; không có wrapper `<nav>` hoặc trạng thái session-aware. | EV-06 |

Prototype hiện không có input, select, modal, retry button hoặc thao tác thay đổi dữ liệu. `hover/focus` chỉ là CSS của anchor; không được hiểu là các state nghiệp vụ đã implement.

## 4. Conditional UI & state variations
- States theo inventory: loading/not-eligible/already-enrolled/free/paid
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
