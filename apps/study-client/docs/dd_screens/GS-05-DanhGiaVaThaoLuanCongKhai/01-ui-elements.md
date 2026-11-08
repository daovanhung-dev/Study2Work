# GS-05 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [GS-05_markers.json](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `GS-05-EL-001` | `GS05-EL-01` | Header brand and primary navigation group |
| #2 | `GS-05-EL-002` | `GS05-EL-02` | Header login and register links |
| #3 | `GS-05-EL-003` | `GS05-EL-03` | Breadcrumb from home through course detail to reviews |
| #4 | `GS-05-EL-004` | `GS05-EL-04` | Empty reviews card icon |
| #5 | `GS-05-EL-005` | `GS05-EL-05` | Reviews page heading |
| #6 | `GS-05-EL-006` | `GS05-EL-06` | Empty reviews explanatory copy |
| #7 | `GS-05-EL-007` | `GS05-EL-07` | Return to course detail link; source href is placeholder # |
| #8 | `GS-05-EL-008` | `GS05-EL-08` | Footer brand link |
| #9 | `GS-05-EL-009` | `GS05-EL-09` | Footer navigation links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: D. Đặc tả element

Marker order/ID trùng 1:1 với [marker map](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05_markers.json). Element state bên dưới mô tả HTML tĩnh; loaded-state elements vắng mặt không được tạo thành current behavior.

| # / Element ID | Tên, loại và vị trí | Thuộc tính / validation / nguồn / điều kiện | Trạng thái và event |
|---|---|---|---|
| 1 `GS05-EL-01` | Header landmark with brand `<a>` and primary `<nav>` anchors; top of page | Brand, Home and Courses anchors all have literal `href="#"`. Header is fixed, 64px high; primary nav uses `hidden md:flex` and is hidden below the `md` breakpoint. No API/state data or validation. | Static default; hover classes exist on some anchors. Navigation is `GS05-EV-08`; routes are not wired. |
| 2 `GS05-EL-02` | Two `<a>` authentication actions; header right side | Labels `Đăng nhập` and `Đăng ký`; both `href="#"`, CSS minimum height 44px. No session, auth callback, return URL or input data. | Static default with hover/active classes on register; `GS05-EV-08`; target routes are unverified. |
| 3 `GS05-EL-03` | Breadcrumb `<nav>`; below fixed header | Home, course-list and course-detail are `<a href="#">`; current-screen label is a `<span>`. No course name or `courseId`; no route validation. | Static default; breadcrumb links dispatch `GS05-EV-07` for course detail or `GS05-EV-08` for home/list. |
| 4 `GS05-EL-04` | Material Symbols `<span>` icon `chat_bubble_outline`; centered at top of empty card | Literal icon token only; not a review count, rating, sentiment or API status. No input/validation. | Static; no event. |
| 5 `GS05-EL-05` | `<h1>` page heading; centered in empty card | Literal `Đánh giá và thảo luận`; no course-name or review-count binding. | Static default; no event. |
| 6 `GS05-EL-06` | `<p>` empty-like copy; below heading in empty card | Literal `Chưa có nội dung để hiển thị.`; not conditional on `data.items=[]`, so it does not prove an API empty result. | Static default; intended response mapping is `GS05-EV-04`, but no binding exists. |
| 7 `GS05-EL-07` | Button-styled `<a>` return CTA; below empty copy | Literal label `Quay lại chi tiết khóa học`; `href="#"`, CSS minimum height 44px. It carries no course ID or history state. | Static default with hover/active classes; expected same-course navigation is `GS05-EV-07`. |
| 8 `GS05-EL-08` | Footer brand `<a>`; footer left | Literal `Study2Work`; `href="#"`; no API or dynamic data. | Static default; `GS05-EV-08`. |
| 9 `GS05-EL-09` | Footer `<nav>` containing four `<a>` links; footer right | Home, courses, login and register labels; all `href="#"`; no auth/session or input data. | Static default; some links have hover classes; `GS05-EV-08`. |

### Expected nhưng absent khỏi source

Review card/list, review title, content excerpt, author/avatar, timestamps, aggregate stars, individual rating, reply list/count, rating filter, pagination, loading skeleton, not-found/error panel, retry action và selected tab control không xuất hiện trong HTML hoặc screenshot có thể đọc. API #10 Draft DD có một số mapping/data, nhưng chưa đủ để biến các phần đó thành implemented UI. Root review `created_at` có mặt trong Draft query/order nhưng không có trong Draft response mapping; không hiển thị ngày review nếu contract chưa bổ sung.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/02_guest_discovery/GS-05_danh-gia-va-thao-luan-cong-khai/GS-05.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
