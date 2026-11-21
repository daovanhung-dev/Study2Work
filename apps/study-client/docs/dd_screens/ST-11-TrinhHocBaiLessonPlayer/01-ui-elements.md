# ST-11 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-11_markers.json](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-11-EL-001` | `ST11-EL-01` | Study2Work wordmark in the top-left header |
| #2 | `ST-11-EL-002` | `ST11-EL-02` | Top-right “Quay lại khóa học của tôi” anchor |
| #3 | `ST-11-EL-003` | `ST11-EL-03` | “Khóa học của tôi” breadcrumb anchor |
| #4 | `ST-11-EL-004` | `ST11-EL-04` | Chevron and current “Bài học” location |
| #5 | `ST-11-EL-005` | `ST11-EL-05` | Centered unavailable-content card surface |
| #6 | `ST-11-EL-006` | `ST11-EL-06` | Decorative `play_lesson` icon in fallback card |
| #7 | `ST-11-EL-007` | `ST11-EL-07` | H1 “Bài học” |
| #8 | `ST-11-EL-008` | `ST11-EL-08` | Bold “Nội dung bài học hiện chưa sẵn sàng.” |
| #9 | `ST-11-EL-009` | `ST11-EL-09` | Supporting text asking the learner to check later or return to courses |
| #10 | `ST-11-EL-010` | `ST11-EL-10` | “Quay lại khóa học của tôi” primary anchor inside the card |
| #11 | `ST-11-EL-011` | `ST11-EL-11` | Study2Work footer wordmark |
| #12 | `ST-11-EL-012` | `ST11-EL-12` | “Tổng quan” footer anchor |
| #13 | `ST-11-EL-013` | `ST11-EL-13` | “Khóa học của tôi” footer anchor |
| #14 | `ST-11-EL-014` | `ST11-EL-14` | “Tiến độ” footer anchor |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Các marker #1–#14 ánh xạ một-một tới các hàng dưới đây và [ST-11_markers.json](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11_markers.json). Marker chỉ nhận diện UI hiện có; player/resources/progress controls chưa xuất hiện nên không được thêm như thể chúng đang được vẽ.

| # / Element ID | Tên, loại, vị trí, mục đích | Thuộc tính, nguồn dữ liệu, điều kiện | Trạng thái / sự kiện |
|---|---|---|---|
| **#1 — ST11-EL-01** | Brand link “Study2Work” ở header trái. | Anchor `href="/student/courses"`; label tĩnh; không có courseId/lessonId parameter. | Visible/default; hover class; EV-07. |
| **#2 — ST11-EL-02** | Header link “Quay lại khóa học của tôi” với icon arrow_back. | Anchor `href="/student/courses"`; text label hiển thị; icon font span không có aria-label riêng. | Visible; hover class; không có current route state; EV-07. |
| **#3 — ST11-EL-03** | Breadcrumb link “Khóa học của tôi”. | Anchor `href="/student/courses"`; không truyền courseId hoặc return context. | Visible; hover class; EV-07. |
| **#4 — ST11-EL-04** | Breadcrumb separator chevron và current location “Bài học”. | Chevron là icon text; current label là span tĩnh, không phải link; không có lesson title. | Static/default; không có event; aria-hidden semantics chưa khai báo. |
| **#5 — ST11-EL-05** | Fallback card/container giữa trang. | Surface trắng, border, radius/shadow; layout chứa unavailable-state content; không lấy state từ API. | Visible trong screenshot; container không tương tác. |
| **#6 — ST11-EL-06** | `play_lesson` decorative icon trong card. | Material Symbols text; không có lesson media/player binding hoặc accessible-name metadata. | Static icon; không phải play control; EV-03 không có current trigger. |
| **#7 — ST11-EL-07** | H1 “Bài học”. | Text tĩnh, không bind `Lesson.title` từ #24. | Static; không có loading/title mapping. |
| **#8 — ST11-EL-08** | Bold unavailable status “Nội dung bài học hiện chưa sẵn sàng.” | Text tĩnh; không gắn HTTP/business code; không phân biệt loading, access denied hay error. | Luôn hiển thị trong asset; fallback message không phải #24 response; EV-02. |
| **#9 — ST11-EL-09** | Supporting explanation “Vui lòng kiểm tra lại sau hoặc quay lại danh sách khóa học của bạn.” | Text tĩnh; không có retry timer hoặc dynamic error detail. | Static; “kiểm tra lại sau” không định nghĩa retry/polling. |
| **#10 — ST11-EL-10** | Primary CTA “Quay lại khóa học của tôi”. | Anchor `href="/student/courses"`, styled as button; không có `button` element, handler hoặc auth logic. | Visible/enabled anchor; EV-07. |
| **#11 — ST11-EL-11** | Footer Study2Work brand wordmark. | `div` tĩnh, không phải link. | Static; no event. |
| **#12 — ST11-EL-12** | Footer link “Tổng quan”. | Anchor `href="/student"`; text visible. | Visible; hover class; EV-08. |
| **#13 — ST11-EL-13** | Footer link “Khóa học của tôi”. | Anchor `href="/student/courses"`; text visible. | Visible; hover class; EV-08. |
| **#14 — ST11-EL-14** | Footer link “Tiến độ”. | Anchor `href="/student/progress"`; text visible. | Visible; hover class; EV-08. |

### Expected player elements/controls chưa có trong asset

Không có video/iframe/player, play/pause/seek, playback speed, subtitles/transcript, loading/buffering UI, current time/duration, progress bar, bookmark/resume position, resources panel/list, completion button/state, quiz/assignment link hoặc Next lesson CTA. Không tạo marker cho control chưa được thiết kế.

## 4. Conditional UI & state variations
- States theo inventory: loading/playing/paused/progress-saving/finished
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-11_trinh-hoc-bai-lesson-player/ST-11.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
