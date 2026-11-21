# ST-24 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-24_markers.json](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-24-EL-001` | `ST24-EL-01` | Study2Work brand/logo |
| #2 | `ST-24-EL-002` | `ST24-EL-02` | Primary Student navigation |
| #3 | `ST-24-EL-003` | `ST24-EL-03` | Global search field |
| #4 | `ST-24-EL-004` | `ST24-EL-04` | Notification control |
| #5 | `ST-24-EL-005` | `ST24-EL-05` | Student profile menu |
| #6 | `ST-24-EL-006` | `ST24-EL-06` | Institution breadcrumb strip |
| #7 | `ST-24-EL-007` | `ST24-EL-07` | Semester and enrollment status |
| #8 | `ST-24-EL-008` | `ST24-EL-08` | Discussion page breadcrumb |
| #9 | `ST-24-EL-009` | `ST24-EL-09` | Mentor-online indicator |
| #10 | `ST-24-EL-010` | `ST24-EL-10` | Hero context labels |
| #11 | `ST-24-EL-011` | `ST24-EL-11` | Page title |
| #12 | `ST-24-EL-012` | `ST24-EL-12` | Supporting description |
| #13 | `ST-24-EL-013` | `ST24-EL-13` | SLA response panel |
| #14 | `ST-24-EL-014` | `ST24-EL-14` | Section 01 heading and required note |
| #15 | `ST-24-EL-015` | `ST24-EL-15` | Course selector |
| #16 | `ST-24-EL-016` | `ST24-EL-16` | Module/lesson selector |
| #17 | `ST-24-EL-017` | `ST24-EL-17` | Topic title field |
| #18 | `ST-24-EL-018` | `ST24-EL-18` | Displayed title character count |
| #19 | `ST-24-EL-019` | `ST24-EL-19` | Topic tags and selected chips |
| #20 | `ST-24-EL-020` | `ST24-EL-20` | Add-tag entry |
| #21 | `ST-24-EL-021` | `ST24-EL-21` | Suggested tags note |
| #22 | `ST-24-EL-022` | `ST24-EL-22` | Section 02 heading |
| #23 | `ST-24-EL-023` | `ST24-EL-23` | Compose mode tab |
| #24 | `ST-24-EL-024` | `ST24-EL-24` | Preview mode tab |
| #25 | `ST-24-EL-025` | `ST24-EL-25` | Rich-text/Markdown toolbar |
| #26 | `ST-24-EL-026` | `ST24-EL-26` | Editor content area |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết element

`screen_annotated.png` annotate trực tiếp PNG gốc với gutter ngoài ảnh; `x/y` trong JSON nằm trên tọa độ `screen.png`. Screenshot chỉ ghi lại static sample state. Hover/focus/disabled/loading/success/error, keyboard behavior, accessible names và responsive layout chưa được chứng minh. Mọi control trong bảng dưới đây là element thiết kế, không phải component runtime.

| Element ID / marker | Tên, loại, vị trí và mục đích | Thuộc tính, data, visibility/state/validation | Event |
|---|---|---|---|
| ST24-EL-01 | Study2Work logo/brand; góc trái header. | Static logo/text; anchor prototype `#`; home route chưa xác nhận. | EV-10 |
| ST24-EL-02 | Primary Student navigation; header gồm Tổng quan, Khóa học, Khóa học của tôi, Lộ trình học, Diễn đàn. | Static labels/links trong ảnh; HTML chỉ đưa link forum về `/student/discussions`, phần còn lại là `#`. No active route wiring. | EV-10 |
| ST24-EL-03 | Global search field; header phải. | Placeholder “Tìm khóa học, bài l…” và icon; không có search API/event thuộc ST-24. | — |
| ST24-EL-04 | Notification control; bell và red dot. | Static notification indicator; unread count/source/action chưa có trong ST-24. | — |
| ST24-EL-05 | Student profile menu; avatar/name/role/dropdown. | Screenshot sample “Nguyen Hanh / Học viên”; không lấy làm session data, claims hay user profile hiện hành. | — |
| ST24-EL-06 | Institutional breadcrumb strip; home icon + “Cổng Học Viên Study2Work”. | Static text/icon; home anchor chưa có route contract. | EV-10 |
| ST24-EL-07 | Semester/enrollment-status strip; góc phải hàng breadcrumb trên. | Static “Học kỳ Fall 2024 • Trạng thái: Đang theo học”; không có API source hoặc policy để xác nhận. | — |
| ST24-EL-08 | Discussion breadcrumb; “Diễn đàn & Thảo luận > Tạo chủ đề mới”. | HTML prototype href về `/student/discussions`; runtime navigation chưa có. | EV-10 |
| ST24-EL-09 | Mentor-online indicator; badge đầu trang. | “Mentor Tech Lead đang online (8 người trực)” là sample literal; không có presence API/online SLA source. | — |
| ST24-EL-10 | Hero context-label group; badge “Hỗ trợ học thuật 1-on-1” + “Chuẩn code review công nghiệp”. | Static category/discipline labels; không được gửi trong API #40 hay dùng để định tuyến. | — |
| ST24-EL-11 | Page title; H1 “Tạo câu hỏi & Thảo luận kỹ thuật”. | Static heading, không bind theo course/module. | — |
| ST24-EL-12 | Supporting description; copy về chi tiết câu hỏi, MRE/log và mentor feedback. | Static explanatory content, không cam kết service/response behavior. | — |
| ST24-EL-13 | SLA response panel; timer, “<45 Phút”, giờ hành chính/ca tối. | Static SLA sample; không phải API-backed target, không hứa thời gian phản hồi. | — |
| ST24-EL-14 | Section 01 heading/required note. | Badge `01`, “Khóa học & Ngữ cảnh bài giảng”, `* Bắt buộc`; visual required note chưa định nghĩa field rule ngoài catalog. | — |
| ST24-EL-15 | Course selector; label “Khóa học liên quan” + dropdown. | Expected selected value `course_id:int64` required theo API #40. Screenshot sample course không phải default. Options/enrollment source, empty/error behavior, access validation và course ID parse chưa được xác nhận. | EV-02 |
| ST24-EL-16 | Module/lesson selector; label “Module / Bài học liên quan” + dropdown. | Sample lesson title; API #40 không khai báo `lesson_id`, module ID hoặc lesson field. Option source và ý nghĩa selector chưa có contract; không thêm vào request. | EV-03 |
| ST24-EL-17 | Topic title field; label + text input. | Logical type `string`, required theo catalog. Screenshot có title sample; min/max, blank/trim/normalization, encoding và field error chưa chốt. | EV-04 |
| ST24-EL-18 | Displayed title counter. | Static `74/150 ký tự`; giới hạn 150 chưa được API catalog/DD xác nhận. Không dùng làm validation rule hoặc reject threshold. | EV-04 |
| ST24-EL-19 | Topic tags field/selected chips. | Sample tags React 19, WebSocket, TanStack Query, Next.js, Performance với remove icons. API #40 không có tags field; tag taxonomy/persistence/limits chưa xác nhận. | EV-05 |
| ST24-EL-20 | Add-tag entry; inline placeholder “Thêm thẻ tag (nhấn Enter)…”. | Enter hint chỉ là visual instruction; add/remove/de-duplicate/case/empty behavior không có handler/contract. Không serialize vào body. | EV-05 |
| ST24-EL-21 | Suggested-tag note. | Static hashtags TypeScript/TailwindCSS/SSR/Zustand/Turbopack; không có recommendation API hoặc selection event source. | — |
| ST24-EL-22 | Section 02 heading; badge `02` + “Nội dung chi tiết & Đoạn mã lỗi”. | Static group title. | — |
| ST24-EL-23 | Compose tab; “Soạn thảo”. | Visually selected in screenshot. Current HTML has no tabs or handler; no runtime state. | EV-07 |
| ST24-EL-24 | Preview tab; “Xem trước”. | Visible mode action; preview renderer, escaping/sanitization, GFM subset and state retention not specified. | EV-07 |
| ST24-EL-25 | Rich-text/Markdown toolbar region. | One grouped toolbar containing **Bold**, **Italic**, **Text/heading (`T`)**, **Quote**, **Code**, **Link**, **Bulleted list**, **Numbered list**, **Ảnh chụp log**, and **Hỗ trợ GFM**. These are separate child actions/indicators in the image but grouped under one marker to keep annotations legible. No handlers, keyboard shortcuts, link validation, file limits, upload mapping or GFM parser are source-backed. | EV-06, EV-08 |
| ST24-EL-26 | Editor content area; large multiline textarea/editor surface. | Prefilled sample Markdown, technical prose and code/HTML-like text; illustrative static content, not user input/default data. Logical editor value is text, while catalog #40 requires `content:int64`; no mapping or safe transformation exists. | EV-06 |

**Không có marker vì không hiện diện:** submit/create/save button, cancel button, error message, validation helper, loading state/skeleton, attachment list/progress, confirmation modal. Inventory expects create, nhưng nút gửi và UX của state đó cần thiết kế bổ sung; không gắn marker cho phần tử chưa có.

## 4. Conditional UI & state variations
- States theo inventory: draft/invalid/submitting/created
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-24_tao-cau-hoi-chu-de/ST-24.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
