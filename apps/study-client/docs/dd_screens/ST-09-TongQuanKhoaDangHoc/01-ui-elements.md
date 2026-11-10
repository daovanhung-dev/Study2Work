# ST-09 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ST-09_markers.json](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ST-09-EL-001` | `ST09-EL-01` | Study2Work LMS brand and school icon |
| #2 | `ST-09-EL-002` | `ST09-EL-02` | Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo |
| #3 | `ST-09-EL-003` | `ST09-EL-03` | Static Nguyễn Văn A / Học viên text and person icon |
| #4 | `ST-09-EL-004` | `ST09-EL-04` | Mã màn hình ST-09; route /student/courses/:courseId; Trạng thái Gated / Unavailable |
| #5 | `ST-09-EL-005` | `ST09-EL-05` | Tổng quan khóa đang học (Gated Hand-off View) and the static subtitle |
| #6 | `ST-09-EL-006` | `ST09-EL-06` | API State badge listing #09 (D), #20 (D), #37 (D) |
| #7 | `ST-09-EL-007` | `ST09-EL-07` | Course-learning tree and enrollment entitlement warning |
| #8 | `ST-09-EL-008` | `ST09-EL-08` | Khóa học chưa sẵn sàng nạp cây nội dung học tập |
| #9 | `ST-09-EL-009` | `ST09-EL-09` | Static copy explaining enrollment, progress and media remain gated |
| #10 | `ST-09-EL-010` | `ST09-EL-10` | Policy icon, title/copy about APIs #09/#20/#37, and RESTRICTED_ACCESS badge |
| #11 | `ST-09-EL-011` | `ST09-EL-11` | Quay lại Khóa học của tôi (ST-08) |
| #12 | `ST-09-EL-012` | `ST09-EL-12` | Kiểm tra quyền học bài (ST-10) |
| #13 | `ST-09-EL-013` | `ST09-EL-13` | Hồ sơ kỹ thuật bàn giao / Developer Hand-off Specification and v1.2 Draft Refined badge |
| #14 | `ST-09-EL-014` | `ST09-EL-14` | Pre-condition, curriculum-integrity and progress-mapping statements |
| #15 | `ST-09-EL-015` | `ST09-EL-15` | Ocean Blue anchor, 4px spacing, elevation and layout-width rows |
| #16 | `ST-09-EL-016` | `ST09-EL-16` | WCAG contrast, keyboard navigation and aria-live claims |
| #17 | `ST-09-EL-017` | `ST09-EL-17` | Static integration warning to keep ST-09 gated until release |
| #18 | `ST-09-EL-018` | `ST09-EL-18` | Sao chép Route; inline clipboard action copies /student/courses/:courseId |
| #19 | `ST-09-EL-019` | `ST09-EL-19` | © 2025 Study2Work LMS and WCAG 2.1 AA Compliant chip |
| #20 | `ST-09-EL-020` | `ST09-EL-20` | Điều khoản dịch vụ, Chính sách bảo mật, Trợ giúp |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả chi tiết từng element

Các marker đánh số 1–20 khớp [screen_annotated.png](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/screen_annotated.png) và [ST-09_markers.json](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09_markers.json). Text trong asset là static content, trừ nút copy route có inline clipboard call. Element không xuất hiện trong ảnh không được tự thêm marker.

| # / Element ID | Tên, loại, vị trí và mục đích | Thuộc tính, dữ liệu, hiển thị | Trạng thái và sự kiện |
|---|---|---|---|
| **#1 — ST09-EL-01** | Brand Study2Work LMS và icon trường; anchor đầu header. | Label/icon tĩnh; HTML href=#. Không có input/validation hoặc binding. | Static/default; click được mô tả ở EV-07 nhưng đích chưa wired. |
| **#2 — ST09-EL-02** | Nhóm điều hướng chính: Trang chủ, Khóa học của tôi, Tiến độ, Thảo luận, Thông báo. | 5 label cố định; nav nằm trong hidden md:flex; href đều #, data-path chỉ là metadata tĩnh. Không có route-registry evidence. | Default/hover utility trong mockup; mobile menu không hiện trong HTML. EV-07. |
| **#3 — ST09-EL-03** | Nhận diện người học: Nguyễn Văn A, Học viên và person icon; đầu header bên phải. | Tên/role/icon hard-coded; không đọc session hoặc profile, không có menu control xác định. | Static/default; không có auth event. EV-01 lưu ý không được dùng nó làm chứng cứ Student session. |
| **#4 — ST09-EL-04** | Nhãn ST-09, route /student/courses/:courseId, badge Gated/Unavailable. | Các giá trị tĩnh; route là template hiển thị, chưa bind courseId. | Static/default; không có validation. EV-01. |
| **#5 — ST09-EL-05** | H1 “Tổng quan khóa đang học (Gated Hand-off View)” và subtitle. | Copy cố định; không lấy tên khóa hay dữ liệu API. | Static/default; không có event. |
| **#6 — ST09-EL-06** | API State panel liệt kê #09 (D), #20 (D), #37 (D). | Static labels. #09 badge mâu thuẫn với current backend source; #20/#37 D phù hợp với hiện trạng chưa wired. | Discrepancy indicator only; không có request state. |
| **#7 — ST09-EL-07** | Warning pill về course learning tree/enrollment gate. | Icon/text tĩnh, không có trạng thái server-driven. | Static/default; warning không thay thế authorization. |
| **#8 — ST09-EL-08** | Gated-state heading “Khóa học chưa sẵn sàng nạp cây nội dung học tập”. | H2 tĩnh. Không nêu business code, enrollment state hoặc lỗi cụ thể. | Static/default; không map một response nào. |
| **#9 — ST09-EL-09** | Explanatory copy cho biết enrollment, progress và media đang gated. | Paragraph tĩnh; không API binding. | Static/default. Bản copy là mô tả thiết kế, không xác thực access policy thực tế. |
| **#10 — ST09-EL-10** | Access policy notice, icon, nội dung về #09/#20/#37 và badge RESTRICTED_ACCESS. | Card tĩnh. Badge không phát sinh guard; HTML không gắn access state từ server. | Static/default; policy needs #20/#22+ contract. Không có event độc lập. |
| **#11 — ST09-EL-11** | Link “Quay lại Khóa học của tôi (ST-08)”. | Anchor tĩnh href=#, data-path=/student/courses. Không có courseId/filter/scroll state. | EV-05. Browser history behavior, SPA route và fallback chưa xác minh. |
| **#12 — ST09-EL-12** | CTA “Kiểm tra quyền học bài (ST-10)”. | Anchor/button styling tĩnh, href=#; không lessonId hoặc API input. Không thể thực hiện access check chỉ với courseId khi API contract chưa chốt. | EV-06. Không định nghĩa navigation thành công cho đến khi lesson selection/ID có nguồn. |
| **#13 — ST09-EL-13** | Section title developer handoff và version badge. | Text/version cố định; tài liệu kỹ thuật được trình bày như nội dung UI mẫu. | Static/default; không event. |
| **#14 — ST09-EL-14** | Gatekeeper specification card. | Copy tĩnh mô tả #20 membership và gate. Hiện #20 response/schema chưa chứng minh claim đó. | Static documentation card; EV-02 là expected flow chưa runnable. |
| **#15 — ST09-EL-15** | Token specification card. | Palette/typography/spacing claims là static. Study guide target dùng Inter/system, ocean #0B5F8A và content width khoảng 1120px; mockup dùng Plus Jakarta Sans, primary #004AC6, max width 1440px. | Static documentation card; design discrepancy, không có event. |
| **#16 — ST09-EL-16** | Accessibility specification card (WCAG). | Copy khẳng định role=alert và aria-live=polite, nhưng attributes đó xuất hiện trong explanatory text, không được áp dụng cho warning element trong HTML. | Static claim; cần audit khi implementation có source. Không event. |
| **#17 — ST09-EL-17** | Frontend integration notice. | Copy tĩnh báo frontend cần nối API/route. Không có runtime state. | Static/default; không event. |
| **#18 — ST09-EL-18** | Button “Sao chép Route”. | Inline handler gọi navigator.clipboard.writeText('/student/courses/:courseId'); copy literal template path, không bind ID. Không có success/failure UI hoặc permission fallback. | EV-09; only current HTML interaction with an inline call. |
| **#19 — ST09-EL-19** | Footer copyright và WCAG badge. | Static text/year/badge; không lấy config. | Static/default; không event. |
| **#20 — ST09-EL-20** | Footer navigation group: overview, my courses, progress, discussions, notifications, terms/privacy/help. | Hrefs #; data-path hints; legal/help slugs không có route contract. | EV-08. Không xác minh destination hoặc keyboard/runtime behavior. |

### Expected elements còn thiếu trong visual design

Inventory yêu cầu outline, per-lesson progress, course context và các nhánh loading/not-enrolled/no-lessons. Asset không có course title/header detail, lesson rows/cards, progress meter, completion state, empty state, loading skeleton, error/retry control hoặc progress-to-ST-21 action. Không gán Element ID cho controls chưa có hình. Chúng phải được bổ sung/duyệt trước khi DD READY.

## 4. Conditional UI & state variations
- States theo inventory: enrolled/not-enrolled/loading/no-lessons
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/03_student/ST-09_tong-quan-khoa-dang-hoc/ST-09.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
