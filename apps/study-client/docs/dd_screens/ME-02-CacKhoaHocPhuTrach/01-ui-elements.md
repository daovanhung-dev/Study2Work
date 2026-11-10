# ME-02 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-02_markers.json](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-02-EL-001` | `ME02-EL-01` | Brand/logo Mentor Portal |
| #2 | `ME-02-EL-002` | `ME02-EL-02` | Primary navigation Mentor |
| #3 | `ME-02-EL-003` | `ME02-EL-03` | Header search học viên/bài tập |
| #4 | `ME-02-EL-004` | `ME02-EL-04` | Notification button và badge mẫu |
| #5 | `ME-02-EL-005` | `ME02-EL-05` | Mentor avatar, tên và chức danh mẫu |
| #6 | `ME-02-EL-006` | `ME02-EL-06` | Breadcrumb Dashboard → ME-02 |
| #7 | `ME-02-EL-007` | `ME02-EL-07` | Context kỳ học, đồng bộ LMS, mã Mentor |
| #8 | `ME-02-EL-008` | `ME02-EL-08` | Page chip, tiêu đề và mô tả |
| #9 | `ME-02-EL-009` | `ME02-EL-09` | CTA báo cáo học vụ tổng thể |
| #10 | `ME-02-EL-010` | `ME02-EL-10` | CTA tạo bài giảng mới |
| #11 | `ME-02-EL-011` | `ME02-EL-11` | KPI khóa phụ trách chính |
| #12 | `ME-02-EL-012` | `ME02-EL-12` | KPI tổng học viên |
| #13 | `ME-02-EL-013` | `ME02-EL-13` | KPI tỷ lệ hoàn thành trung bình |
| #14 | `ME-02-EL-014` | `ME02-EL-14` | KPI chuẩn Capstone |
| #15 | `ME-02-EL-015` | `ME02-EL-15` | Search khóa học/tên/mã |
| #16 | `ME-02-EL-016` | `ME02-EL-16` | Filter status |
| #17 | `ME-02-EL-017` | `ME02-EL-17` | Filter cấp độ |
| #18 | `ME-02-EL-018` | `ME02-EL-18` | Sort theo học viên/tiến độ/cập nhật |
| #19 | `ME-02-EL-019` | `ME02-EL-19` | Active-filter chips (status và kỳ học) |
| #20 | `ME-02-EL-020` | `ME02-EL-20` | Xóa tất cả bộ lọc |
| #21 | `ME-02-EL-021` | `ME02-EL-21` | Tổng số khóa hiển thị |
| #22 | `ME-02-EL-022` | `ME02-EL-22` | Course 1: thumbnail, level/status, mã và rating |
| #23 | `ME-02-EL-023` | `ME02-EL-23` | Course 1: title và description |
| #24 | `ME-02-EL-024` | `ME02-EL-24` | Course 1: submission-count badge |
| #25 | `ME-02-EL-025` | `ME02-EL-25` | Course 1: student/curriculum/lab/progress metrics |
| #26 | `ME-02-EL-026` | `ME02-EL-26` | Course 1: action links quản lý/chấm/progress |
| #27 | `ME-02-EL-027` | `ME02-EL-27` | Course 1: CTA Workspace ME-03 |
| #28 | `ME-02-EL-028` | `ME02-EL-28` | Course 2: thumbnail, level/status, mã và rating |
| #29 | `ME-02-EL-029` | `ME02-EL-29` | Course 2: title và description |
| #30 | `ME-02-EL-030` | `ME02-EL-30` | Course 2: submission-count badge |
| #31 | `ME-02-EL-031` | `ME02-EL-31` | Course 2: student/curriculum/lab/progress metrics |
| #32 | `ME-02-EL-032` | `ME02-EL-32` | Course 2: action links quản lý/chấm/analytics |
| #33 | `ME-02-EL-033` | `ME02-EL-33` | Course 2: CTA Workspace ME-03 |
| #34 | `ME-02-EL-034` | `ME02-EL-34` | Course 3: thumbnail, level/status, mã và rating |
| #35 | `ME-02-EL-035` | `ME02-EL-35` | Course 3: title và description |
| #36 | `ME-02-EL-036` | `ME02-EL-36` | Course 3: submission-count badge |
| #37 | `ME-02-EL-037` | `ME02-EL-37` | Course 3: student/curriculum/case/progress metrics |
| #38 | `ME-02-EL-038` | `ME02-EL-38` | Course 3: action links quản lý/chấm/progress |
| #39 | `ME-02-EL-039` | `ME02-EL-39` | Course 3: CTA Workspace ME-03 |
| #40 | `ME-02-EL-040` | `ME02-EL-40` | Pagination summary |
| #41 | `ME-02-EL-041` | `ME02-EL-41` | First/previous/page/next/last controls |
| #42 | `ME-02-EL-042` | `ME02-EL-42` | Page-size selector |
| #43 | `ME-02-EL-043` | `ME02-EL-43` | Footer brand và giới thiệu |
| #44 | `ME-02-EL-044` | `ME02-EL-44` | Footer tiêu chuẩn học thuật |
| #45 | `ME-02-EL-045` | `ME02-EL-45` | Footer liên kết viện-trường |
| #46 | `ME-02-EL-046` | `ME02-EL-46` | Footer hỗ trợ Mentor |
| #47 | `ME-02-EL-047` | `ME02-EL-47` | Copyright, certification và policy links |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 3. Element map (47 markers)

Marker source coordinates dùng gốc trên trái, ảnh `screen.png` 1100×1600. JSON map lưu 47 ID duy nhất. Các hàng repeated card được tách thành từng card để nhận diện đúng ba mẫu riêng; marker trên ảnh chỉ trỏ component, không xác nhận sample text là dữ liệu runtime.

| Marker / Element ID | Tên, loại, vị trí và thuộc tính | Data/visibility/state | Event |
|---|---|---|---|
| #1 `ME02-EL-01` | Brand/logo “Study2Work — Mentor Portal”; anchor header. | HTML `href="#"`, không destination. Branding là static design content. | EV-15 |
| #2 `ME02-EL-02` | Primary navigation group: Dashboard, Khóa học phụ trách, Chấm bài & Đồ án, Hỗ trợ học viên, Thông báo. | Năm anchor có `href="#"`; `data-path` là text prototype, không phải router. Route proposal phải lấy từ inventory; current page active visual only. | EV-15 |
| #3 `ME02-EL-03` | Header global search input, type text, placeholder “Tìm kiếm học viên, bài tập…”. | Không id/name/required/validation/API; responsive ẩn ở breakpoint nhỏ theo class HTML. | EV-16 |
| #4 `ME02-EL-04` | Notification bell button và badge `3`. | Badge sample; unread endpoint/notification inbox và open/mark-read behavior không được screen/API #46 xác nhận. | EV-16 |
| #5 `ME02-EL-05` | Mentor avatar, tên “TS. Trần Hoàng Long”, title “Lead Mentor / Principal Architect”. | Static sample; API #46 nhúng Mentor summary trên từng Course nhưng không cung cấp profile/title độc lập. | EV-16 |
| #6 `ME02-EL-06` | Breadcrumb Dashboard → Khóa học phụ trách. | Dashboard route proposal `/mentor`; anchor là `#`; current page text read-only. | EV-15 |
| #7 `ME02-EL-07` | Semester/sync/Mentor context: `Q2/2025`, “Đồng bộ LMS thời gian thực”, `MTR-9821`. | Không có time-period, sync heartbeat/freshness hoặc Mentor code field trong #46. Static sample. | N/A |
| #8 `ME02-EL-08` | ME-02 chip, page heading “Khóa học phụ trách & Quản lý đào tạo” và description. | `API #46 Live` trong HTML là nhãn mẫu; current source-backed không chứng minh live deployment. Copy vẫn là static. | N/A |
| #9 `ME02-EL-09` | Button “Xem báo cáo học vụ tổng thể”. | Không có route/API report tổng thể; #66 nhận từng `course_id` và trả activity proxy. | EV-14 |
| #10 `ME02-EL-10` | Primary button “Tạo bài giảng mới”. | ME-04 route cần `courseId`; page-level CTA không chỉ rõ course hoặc cách chọn course. | EV-13 |
| #11 `ME02-EL-11` | KPI “Khóa phụ trách chính”, `03`, `100% Active`, kỳ Quý 2. | #46 pagination total có thể đếm tập theo predicate/status nhưng không phân biệt “chính”, “active”, “được phân công” hoặc kỳ. | N/A |
| #12 `ME02-EL-12` | KPI “Tổng học viên”, `2,830`, `+14.2%`. | #62 chỉ trả active roster theo một course, không tổng toàn màn hình, growth period hay dedup cross-course. | N/A |
| #13 `ME02-EL-13` | KPI “Tỷ lệ hoàn thành TB”, `84.5%`, `+3.8% MoM` và progress bar. | #65 trả per-Student progress; #66 activity proxy. Không có approved aggregate/period formula cho KPI này. | N/A |
| #14 `ME02-EL-14` | KPI “Đạt chuẩn Capstone”, `96.2%`, “EduTrust QA”. | Không có Capstone/credential/pass-rate API hoặc metric definition trong ME-02 contract. | N/A |
| #15 `ME02-EL-15` | Course search input, tên hoặc mã ví dụ `FE-ENT-04`. | #46 không có `q`/course-code query hoặc Course code response. No current handler. | EV-02 |
| #16 `ME02-EL-16` | Status select: all, `active`, `upcoming`, `archived`; mockup đang chọn active. | #46 chỉ chấp nhận `DRAFT|PUBLISHED`; không tự map UI labels sang enum. | EV-03 |
| #17 `ME02-EL-17` | Level select: all, Enterprise, Advanced, Foundation. | #46 query/model không có level; Course response không có level field. | EV-04 |
| #18 `ME02-EL-18` | Sort select: student count, progress, updated. | #46 không nhận sort query; current order là created_at descending/id ascending. | EV-05 |
| #19 `ME02-EL-19` | Active filter chips status và `Q2/2025`, mỗi chip có close button. | Semester filter không được API hỗ trợ; status mapping chưa chốt. HTML buttons không có id/state binding. | EV-06 |
| #20 `ME02-EL-20` | Button “Xóa tất cả bộ lọc”. | Không có handler/state model; reset page/query policy chưa được duyệt. | EV-07 |
| #21 `ME02-EL-21` | Result count “Hiển thị 3 / 3 khóa học hợp lệ”. | #46 trả `pagination.total`; “hợp lệ” không phải API metric. Cần xác định filter và current page trước khi hiển thị. | N/A |
| #22 `ME02-EL-22` | Course 1 media block: thumbnail, Enterprise badge, “Đang giảng dạy”, mã `FE-ENT-04`, rating `4.96`/`1,420 đánh giá`. | #46 `thumbnail_url`/`status` có thể map; không có level, code, rating hoặc review count. Thumbnail trong HTML dùng URL ngoài; runtime source không xác minh. | N/A |
| #23 `ME02-EL-23` | Course 1 title và description. | Map `Course.title` và nullable `description`; nếu null, display fallback/collapse chưa được thiết kế. Title cursor style không kèm handler. | N/A |
| #24 `ME02-EL-24` | Course 1 badge “8 bài nộp đang chờ duyệt”. | #46 không có submission count/status. ME-02 inventory không gọi #54; “pending” definition và aggregate chưa có contract tại screen. | N/A |
| #25 `ME02-EL-25` | Course 1 metrics: `1,420` học viên, 48 bài giảng/8 chương, 12 lab & quiz, progress 64%/module. | Không có trong #46 Course. #62/#65 không trả đầy đủ fields/grain này; #49 content tree không được khai báo trong ME-02 row. Tất cả sample. | N/A |
| #26 `ME02-EL-26` | Course 1 action group: Quản lý nội dung (ME-06), Chấm đồ án (ME-09), Tiến độ học viên (ME-16). | HTML links `#`; inventory ME-02 links ME-03/04/16, không có ME-06/09 direct handoff. Badge chấm `8` sample. | EV-10, EV-11, EV-12 |
| #27 `ME02-EL-27` | Course 1 CTA “Vào Workspace (ME-03)”. | Handoff `Course.id` từ API #46; route proposal `/mentor/courses/:courseId`. API vẫn phải kiểm access; assignment chưa được hỗ trợ bởi query direct-owner. | EV-09 |
| #28 `ME02-EL-28` | Course 2 media block: Advanced/status, code `BE-GO-02`, rating `4.95`/`890 đánh giá`. | `thumbnail_url/status` có thể map; level/code/rating/reviews không có trong Course. | N/A |
| #29 `ME02-EL-29` | Course 2 title và description. | Map `title`/nullable `description`; text mẫu. | N/A |
| #30 `ME02-EL-30` | Course 2 badge “4 bài nộp chờ duyệt”. | #46 không có submission count; pending policy không xác định. | N/A |
| #31 `ME02-EL-31` | Course 2 metrics: 890 learners, 56 lessons/10 chuyên đề, 16 benchmark labs, progress 52%/module Kafka. | Không có trong #46; #62/#65/#66 không trả các metric/labels này. | N/A |
| #32 `ME02-EL-32` | Course 2 action group: Quản trị nội dung, Chấm đồ án Capstone, Phân tích lớp học. | HTML anchors `#`; phân tích lớp học route/ID không ghi rõ. API #66 per-course activity không phải toàn bộ report shown. | EV-10, EV-11, EV-12 |
| #33 `ME02-EL-33` | Course 2 CTA “Vào Workspace (ME-03)”. | Cần `Course.id`; screen route đề xuất, chưa wired. | EV-09 |
| #34 `ME02-EL-34` | Course 3 media block: Intermediate/status, code `UX-DS-01`, rating `4.98`/`520 đánh giá`. | #46 chỉ có thumbnail/status trong các trường phù hợp; level/code/rating/reviews unsupported. | N/A |
| #35 `ME02-EL-35` | Course 3 title và description. | Map `title`/nullable `description`; text mẫu. | N/A |
| #36 `ME02-EL-36` | Course 3 badge “2 bài nộp chờ duyệt”. | #46 không trả submission count; không tính từ page list. | N/A |
| #37 `ME02-EL-37` | Course 3 metrics: 520 learners, 32 lessons/6 blocks, 8 case studies, progress 78%/Capstone. | Không có trong #46; không có API Capstone/average/module label được screen khai báo. | N/A |
| #38 `ME02-EL-38` | Course 3 action group: Quản lý nội dung, Chấm đồ án Design, Tiến độ học viên. | HTML anchors `#`; badges/route/filter scope chưa có contract. | EV-10, EV-11, EV-12 |
| #39 `ME02-EL-39` | Course 3 CTA “Vào Workspace (ME-03)”. | Cần ID course từ current result; route runtime chưa tồn tại. | EV-09 |
| #40 `ME02-EL-40` | Pagination summary `1–3` trong `3 khóa học phụ trách`. | Có thể so khớp `pagination.page/size/total` sau khi filter được quyết định; text “phụ trách” còn ownership/assignment mismatch. | EV-08 |
| #41 `ME02-EL-41` | Pagination buttons first/previous/page 1/next/last. | Screenshot disable first/previous/next/last với một page; phải lấy `total_pages`, không suy từ sample. `page` int, min 1. | EV-08 |
| #42 `ME02-EL-42` | Page-size select `10/20/50`, selected 10. | #46 chấp nhận 1–100, default 20. UI default 10 và page-reset policy cần quyết định. | EV-08 |
| #43 `ME02-EL-43` | Footer Study2Work LMS và mô tả. | Static text/image, không phải response #46; version/content owner chưa có source trong screen contract. | N/A |
| #44 `ME02-EL-44` | Footer danh sách tiêu chuẩn học thuật. | `li` text tĩnh, không link/API action. | N/A |
| #45 `ME02-EL-45` | Footer danh sách liên kết viện-trường. | `li` text tĩnh, không link/API action. | N/A |
| #46 `ME02-EL-46` | Footer hỗ trợ Mentor: hotline, email và handbook. | Contact text/handbook destination chưa được xác minh; `li` không phải link. | N/A |
| #47 `ME02-EL-47` | Copyright, ISO/EduAccredited và policy labels. | Static sample; policy labels là `span`, không có href. | N/A |

## 4. Conditional UI & state variations
- States theo inventory: loading/empty/ready/denied
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-02_cac-khoa-hoc-phu-trach/ME-02.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
