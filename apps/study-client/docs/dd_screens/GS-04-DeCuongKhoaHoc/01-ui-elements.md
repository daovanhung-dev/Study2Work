# GS-04 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-04_markers.json](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-04-EL-001` | `GS04-EL-01` | Header brand and primary navigation group |
| #2 | `GS-04-EL-002` | `GS04-EL-02` | Header login and register actions |
| #3 | `GS-04-EL-003` | `GS04-EL-03` | Breadcrumb from home and course list through course detail to curriculum |
| #4 | `GS-04-EL-004` | `GS04-EL-04` | Curriculum page heading |
| #5 | `GS-04-EL-005` | `GS04-EL-05` | Empty curriculum card icon |
| #6 | `GS-04-EL-006` | `GS04-EL-06` | Empty curriculum heading |
| #7 | `GS-04-EL-007` | `GS04-EL-07` | Empty curriculum explanatory text |
| #8 | `GS-04-EL-008` | `GS04-EL-08` | Return to course detail link; source href is placeholder # |
| #9 | `GS-04-EL-009` | `GS04-EL-09` | Footer brand |
| #10 | `GS-04-EL-010` | `GS04-EL-10` | Footer navigation links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: D. Đặc tả element

Thứ tự và ID khớp 1:1 với 10 marker trong JSON/ảnh. “Hiện tại” chỉ mô tả HTML; “expected” không biến thành current behavior.

| # / Element ID | Thành phần và vị trí | Dữ liệu / điều kiện | Current state / event |
|---|---|---|---|
| 1 `GS04-EL-01` | Header brand `Study2Work` và primary nav `Trang chủ`, `Khóa học` | Brand và `Trang chủ` dùng `href="/"`; `Khóa học` dùng `/courses`. Nav có class `hidden sm:flex`, nên bị ẩn dưới breakpoint `sm`. Tất cả là literal. | Static; hover class có trong HTML. Anchor behavior là `GS04-EV-06`; router chưa wired. |
| 2 `GS04-EL-02` | Header actions `Đăng nhập`, `Đăng ký` | Literal href `/login`, `/register`; không có session/auth callback hoặc return URL. | Static, target chưa runtime verified; `GS04-EV-06`. |
| 3 `GS04-EL-03` | Breadcrumb `Trang chủ > Khóa học > Chi tiết khóa học > Đề cương khóa học` | Home `/`; course list `/courses`; “Chi tiết khóa học” là anchor `#`; current page là text. Không chứa `courseId` hoặc tên khóa học. | Static; click home/list thuộc `GS04-EV-06`; detail link thuộc `GS04-EV-05` nhưng hiện là placeholder. |
| 4 `GS04-EL-04` | H1 `Đề cương khóa học` | Literal text; không có course title/name binding. | Static; không có event. Loaded page title/data contract chưa có trong HTML. |
| 5 `GS04-EL-05` | Icon `toc` trong vòng tròn của empty card | Material Symbols; trang trí, không phải lesson count hoặc API status. | Static; không có event. |
| 6 `GS04-EL-06` | Heading trong empty card `Đề cương khóa học` | Literal; trùng ý với H1. | Static; không có event. |
| 7 `GS04-EL-07` | Empty copy `Chưa có nội dung đề cương để hiển thị.` | Literal; source không kiểm tra `items=[]`, do đó không thể hiểu là API-confirmed empty. | Static; không có event. Expected response mapping là `GS04-EV-03`. |
| 8 `GS04-EL-08` | CTA `Quay lại chi tiết khóa học` | Anchor có `href="#"`; không truyền lại `courseId`, không dùng history API. | Click chỉ theo placeholder anchor; expected return `GS04-EV-05` còn blocked. |
| 9 `GS04-EL-09` | Footer brand `Study2Work` | Plain `span`, không phải link. | Static; không có event. |
| 10 `GS04-EL-10` | Footer links `Trang chủ`, `Khóa học`, `Đăng nhập`, `Đăng ký` | Literal href lần lượt `/`, `/courses`, `/login`, `/register`. | Static; anchor behavior `GS04-EV-06`; destination routes chưa runtime verified. |

### Không có trong source

Không có lesson rows, chapter grouping, order label, duration, preview/private badge, play/open action, resource link, pagination, search, collapse/expand, selected-tab control, API loading, retry UI hoặc error panel. Không tạo marker/event như thể các element này đã tồn tại. Loaded-state design là deliverable còn thiếu.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-04_de-cuong-khoa-hoc/GS-04.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
