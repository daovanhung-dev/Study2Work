# ME-09 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-09_markers.json](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-09-EL-001` | `ME09-EL-01` | Logo và thương hiệu Study2Work LMS Mentor |
| #2 | `ME-09-EL-002` | `ME09-EL-02` | Điều hướng Tổng quan |
| #3 | `ME-09-EL-003` | `ME09-EL-03` | Điều hướng Khóa học phụ trách |
| #4 | `ME-09-EL-004` | `ME09-EL-04` | Điều hướng Chấm bài đang chọn |
| #5 | `ME-09-EL-005` | `ME09-EL-05` | Điều hướng Hộp thư hỗ trợ |
| #6 | `ME-09-EL-006` | `ME09-EL-06` | Điều hướng Thông báo |
| #7 | `ME-09-EL-007` | `ME09-EL-07` | Nút chuông thông báo |
| #8 | `ME-09-EL-008` | `ME09-EL-08` | Danh tính và avatar Mentor |
| #9 | `ME-09-EL-009` | `ME09-EL-09` | Nhãn Trung tâm Đánh giá và Phản hồi |
| #10 | `ME-09-EL-010` | `ME09-EL-10` | Tiêu đề Danh sách bài nộp cần chấm điểm |
| #11 | `ME-09-EL-011` | `ME09-EL-11` | Mô tả mục đích màn hình |
| #12 | `ME-09-EL-012` | `ME09-EL-12` | Badge Đồng bộ tự động: Bật |
| #13 | `ME-09-EL-013` | `ME09-EL-13` | Bộ lọc Khóa học phụ trách |
| #14 | `ME-09-EL-014` | `ME09-EL-14` | Bộ lọc Trạng thái bài nộp |
| #15 | `ME-09-EL-015` | `ME09-EL-15` | Ô tìm kiếm bài tập |
| #16 | `ME-09-EL-016` | `ME09-EL-16` | Nút Thiết lập lại bộ lọc |
| #17 | `ME-09-EL-017` | `ME09-EL-17` | Minh họa trạng thái rỗng |
| #18 | `ME-09-EL-018` | `ME09-EL-18` | Tiêu đề trạng thái chưa có bài cần chấm |
| #19 | `ME-09-EL-019` | `ME09-EL-19` | Nội dung giải thích trạng thái rỗng |
| #20 | `ME-09-EL-020` | `ME09-EL-20` | Nút Tải lại danh sách |
| #21 | `ME-09-EL-021` | `ME09-EL-21` | Thông tin tuân thủ hạn nộp 48 giờ |
| #22 | `ME-09-EL-022` | `ME09-EL-22` | Thông tin hệ thống chấm theo Rubric chuẩn |
| #23 | `ME-09-EL-023` | `ME09-EL-23` | Liên hệ Ban Đào tạo hỗ trợ chuyên môn |
| #24 | `ME-09-EL-024` | `ME09-EL-24` | Logo và thông tin bản quyền footer |
| #25 | `ME-09-EL-025` | `ME09-EL-25` | Liên kết Quy chế Giảng viên |
| #26 | `ME-09-EL-026` | `ME09-EL-26` | Liên kết Tiêu chuẩn đánh giá |
| #27 | `ME-09-EL-027` | `ME09-EL-27` | Liên kết Hỗ trợ kỹ thuật |

## 3. Đặc tả từng element

### Trích từ DD nguồn: C. Đặc tả element

Các element dưới đây khớp marker `#1`–`#27` trong [ảnh chú thích](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/screen_annotated.png), [marker map](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09_markers.json) và [SVG overlay](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09_markers_overlay.svg). “Static/design-only” mô tả asset hiện có; không phải cam kết runtime.

| Element ID | Tên / loại | Mục đích, thuộc tính và hành vi hiện biết |
|---|---|---|
| ME09-EL-01 | Brand/logo, link | Hiển thị logo “Study2Work / LMS Mentor”. HTML `href="#"`; route home chưa được xác định hoặc wire. Tên thương hiệu không lấy từ API #54. |
| ME09-EL-02 | Nav link “Tổng quan” | Điều hướng được kỳ vọng tới ME-01 hoặc mentor home, nhưng HTML `href="#"`; đích thực tế chưa được xác minh. |
| ME09-EL-03 | Nav link “Khóa học phụ trách” | HTML `href="#"`; không xác định course filter hay giữ state khi rời màn hình. |
| ME09-EL-04 | Nav link “Chấm bài” | Nav item active trong mockup. Không phải xác nhận route `/mentor/submissions` đã tồn tại. |
| ME09-EL-05 | Nav link “Hộp thư hỗ trợ” | HTML `href="#"`; không thuộc F09 grading list API #54. |
| ME09-EL-06 | Nav link “Thông báo” | HTML `href="#"`; route notification chưa được nối từ asset. |
| ME09-EL-07 | Notification bell, link/icon | Có badge chấm đỏ; HTML `href="#"`; unread count/data/API chưa được source xác nhận. Accessible label/notification state chưa được kiểm tra. |
| ME09-EL-08 | Mentor identity/avatar | Hiển thị mẫu “TS. Vũ Thành Đạt / MENTOR / GIẢNG VIÊN”. Không có current-user API/source mapping trong ME-09. Không coi tên hay role trong ảnh là authenticated identity. |
| ME09-EL-09 | Context eyebrow/icon | “Trung tâm Đánh giá & Phản hồi”; nhãn tĩnh của asset, không phải server category. |
| ME09-EL-10 | H1 page title | “Danh sách bài nộp cần chấm điểm”; nội dung heading tĩnh. |
| ME09-EL-11 | Page description | Mô tả điều phối kiểm tra/đồ án và phản hồi năng lực. Không được coi là quy tắc AC-23 hoặc dữ liệu API. |
| ME09-EL-12 | Sync badge | “Đồng bộ tự động: Bật”. Không có polling, websocket, timer hay invalidation trong HTML/API #54; trạng thái này là claim chưa được xác nhận. |
| ME09-EL-13 | Course filter: label + select | HTML ID `filter-course`, option mặc định `all`, tiếp theo `fe`, `be`, `ux`. Đây là static string sample, không phải `course_id:int64`; API #54 yêu cầu numeric ID. Nguồn option, default và mapping cần quyết định. |
| ME09-EL-14 | Status filter: label + select | HTML ID `filter-status`, giá trị mẫu `pending`, `graded`, `recheck`; label đầu “Chờ chấm điểm”. API chỉ lọc exact `status:string`; lifecycle/enum/status normalization chưa khóa. |
| ME09-EL-15 | Search label/input | HTML ID `search-keyword`, `type=text`; placeholder gợi ý tên chuyên đề/đồ án/mã bài. API #54 không nhận query search và response không có assignment title. Không có debounce/submit handler. |
| ME09-EL-16 | Reset filters button | HTML ID `btn-filter-reset`, `type=button`; đặt course=`all`, status=`pending`, search rỗng tại client. Không gọi #54, không xác nhận canonical default hoặc reset page. |
| ME09-EL-17 | Empty-state illustration | Hình tĩnh. Không truyền semantic status ngoài ý nghĩa “empty” của màn hình. |
| ME09-EL-18 | Empty-state heading | “Chưa có bài tập nào cần chấm điểm”. Chỉ được hiển thị sau khi API success có `items=[]`; HTML đang hard-code nên hiện không phân biệt loading/error. |
| ME09-EL-19 | Empty-state explanation | Nêu không có bài chờ hoặc Mentor chưa được phân công; sau đó khẳng định bài mới tự hiển thị. API #54 chỉ chứng minh empty result cho direct-owner scope; không chứng minh assignment policy, assigned Mentor hay automatic refresh. |
| ME09-EL-20 | Refresh list button | HTML ID `btn-refresh`. Prototype chỉ animate icon/disable nút 750 ms rồi bật lại; không gọi API. Future refresh cần gọi #54 theo contract đã duyệt; timeout, retry và polling chưa được xác nhận. |
| ME09-EL-21 | Deadline claim | “Tuân thủ hạn nộp 48h của Mentor”. #54 không trả due date/SLA; không hiển thị như calculated status nếu chưa có rule/source. |
| ME09-EL-22 | Rubric claim | “Hệ thống chấm theo bộ tiêu chí Rubric chuẩn”. #54 không trả rubric; API #55 current source cũng không trả rubric. Claim chưa được chứng minh cho grading flow. |
| ME09-EL-23 | Training-support claim | “Cần hỗ trợ chuyên môn? Liên hệ Ban Đào Tạo”. Icon/copy tĩnh; không có route/contact API trong ME-09 source. |
| ME09-EL-24 | Footer brand/copyright | Có logo, © 2025, WCAG 2.1 AA và mô tả cổng Mentor. Chỉ là copy; không chứng minh bản quyền hiện hành hoặc kiểm định accessibility đã chạy. |
| ME09-EL-25 | Footer link “Quy chế Giảng viên” | HTML `href="#"`; destination/content chưa được xác định. |
| ME09-EL-26 | Footer link “Tiêu chuẩn đánh giá” | HTML `href="#"`; không liên kết tới API rubric hoặc policy cụ thể trong source. |
| ME09-EL-27 | Footer link “Hỗ trợ kỹ thuật” | HTML `href="#"`; contact/help flow chưa được xác định. |

### C.1. Row/list state chưa có trong ảnh

Không có marker hoặc định nghĩa row/table vì cả PNG lẫn HTML không chứa loaded list. Không tự tạo card layout. Các trường source hiện có là `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?`, `feedback?`; không trường nào được tự đổi thành assignment title, tên Student, course name hay deadline. Inventory yêu cầu deadline/owner, do đó loaded-state element layout còn là blocker.

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-09_danh-sach-bai-can-cham/ME-09.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
