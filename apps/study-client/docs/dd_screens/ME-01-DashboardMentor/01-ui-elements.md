# ME-01 — UI Elements

## 1. Quy tắc ảnh & mapping
- [Ảnh gốc](images/screen-clean.png) · [Ảnh đánh số](images/screen-numbered.png)
- Ảnh numbered được sao chép nguyên trạng từ `screen_annotated.png`; mapping lấy từ JSON marker và DD nguồn. Không đổi ID marker nguồn trong lần chuyển đổi này.
- Marker JSON nguồn: [ME-01_markers.json](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers.json).

## 2. Danh sách phần tử
| Marker | Element ID trong package | Source Element ID | Nhãn từ marker JSON |
|---|---|---|---|
| #1 | `ME-01-EL-001` | `ME01-EL-01` | Study2Work brand and Mentor Portal label |
| #2 | `ME-01-EL-002` | `ME01-EL-02` | Primary navigation links |
| #3 | `ME-01-EL-003` | `ME01-EL-03` | Global learner/submission search input |
| #4 | `ME-01-EL-004` | `ME01-EL-04` | Notification bell and unread-count badge |
| #5 | `ME-01-EL-005` | `ME01-EL-05` | Current Mentor avatar and identity block |
| #6 | `ME-01-EL-006` | `ME01-EL-06` | Welcome greeting and online/helping status banner |
| #7 | `ME-01-EL-007` | `ME01-EL-07` | Duty/on-call schedule card and change-shift action |
| #8 | `ME-01-EL-008` | `ME01-EL-08` | Owned-course KPI card |
| #9 | `ME-01-EL-009` | `ME01-EL-09` | Pending-grading KPI card |
| #10 | `ME-01-EL-010` | `ME01-EL-10` | Support-ticket KPI card |
| #11 | `ME-01-EL-011` | `ME01-EL-11` | Mentor-rating KPI card |
| #12 | `ME-01-EL-012` | `ME01-EL-12` | Submission panel title, API note and view-all link |
| #13 | `ME-01-EL-013` | `ME01-EL-13` | Repeated submission preview cards and grade actions |
| #14 | `ME-01-EL-014` | `ME01-EL-14` | Course panel title, API note and view-all link |
| #15 | `ME-01-EL-015` | `ME01-EL-15` | Repeated owned-course cards and workspace/content actions |
| #16 | `ME-01-EL-016` | `ME01-EL-16` | Support inbox title and pending-count badge |
| #17 | `ME-01-EL-017` | `ME01-EL-17` | Repeated support-request previews and reply actions |
| #18 | `ME-01-EL-018` | `ME01-EL-18` | Open support workspace link |
| #19 | `ME-01-EL-019` | `ME01-EL-19` | Mentorship calendar heading and session count |
| #20 | `ME-01-EL-020` | `ME01-EL-20` | Repeated appointment cards, join-Meet and details actions |
| #21 | `ME-01-EL-021` | `ME01-EL-21` | Academic notices heading and term label |
| #22 | `ME-01-EL-022` | `ME01-EL-22` | Academic announcement list |
| #23 | `ME-01-EL-023` | `ME01-EL-23` | Footer brand, policies, institutional links and Mentor support |

## 3. Đặc tả từng element

### Trích từ DD nguồn: 4. Element map

Marker IDs và số thứ tự khớp [ảnh chú thích](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/screen_annotated.png), [marker JSON](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01_markers.json) và mỗi hàng bên dưới. Các marker gom nhóm component lặp; mỗi hàng ghi rõ instance và controls con. Marker không xác nhận dữ liệu hoặc action đang chạy.

| # / Element ID | Tên, loại, vị trí | Data/thuộc tính và điều kiện | Trạng thái / event |
|---|---|---|---|
| 1 `ME01-EL-01` | Brand Study2Work/Mentor Portal; link ở đầu header. | Logo và nhãn tĩnh; HTML `href="#"`; destination chưa được xác nhận. | Static; click thuộc `ME01-EV-11`. |
| 2 `ME01-EL-02` | Nhóm primary navigation: Dashboard, Khóa học phụ trách, Chấm bài & Đồ án, Hỗ trợ học viên, Thông báo. | Dashboard được highlight trong ảnh. Inventory có route cho ME-02/ME-09/ME-11; Notifications landing và route Dashboard chưa được xác minh. Tất cả anchors placeholder. | Default/active theo ảnh; route click `EV-02`, `EV-04`, `EV-06`; mục Thông báo `EV-10`. |
| 3 `ME01-EL-03` | Text input tìm học viên/bài tập ở header. | HTML `type=text`, placeholder “Tìm kiếm học viên, bài tập…”; không `id`, `name`, required, min/max, source data hoặc API contract. | Chỉ default tĩnh; `EV-08` bị chặn vì chưa có search behavior/API/route. |
| 4 `ME01-EL-04` | Notification bell và badge số `3`. | Giá trị badge là sample. Không có API unread-count/notification-list trên ME-01; #64 yêu cầu notification ID cụ thể. | Button tĩnh, không có open/mark-read event; `EV-10`. |
| 5 `ME01-EL-05` | Avatar, tên Mentor và title ở header. | Tên/title trong ảnh là sample. #46 chỉ trả `mentor{id, full_name, avatar_url?}` gắn từng course; không có endpoint profile hiện tại cho Mentor trong screen contract. | Read-only visual; data source/title mapping cần quyết định. |
| 6 `ME01-EL-06` | Welcome hero, greeting, role/company/description và online-status chips. | Tất cả text/status là sample; không có profile, online-presence hoặc availability source trong #46/#54/#58. | Decorative/static sample; không có event. |
| 7 `ME01-EL-07` | Duty/on-call schedule card và button “Đổi ca trực”. | Giờ trực, thứ trong tuần, trạng thái, SLA/ca và thao tác đổi lịch không có endpoint/contract. | Button tĩnh, `EV-11` bị chặn. |
| 8 `ME01-EL-08` | KPI số course phụ trách và active learners. | #46 `data.pagination.total` có thể biểu diễn tổng course theo filter; chưa chốt course owner vs assignment. Enrollment/active learner count không có trong response. Số `3`/`1,420` là sample. | Loading/empty/error riêng cho course widget theo inventory; metric học viên bị chặn. |
| 9 `ME01-EL-09` | KPI submissions cần chấm và số trễ hạn. | #54 trả page count theo `status` tùy chọn nhưng không có enum; không có due date/SLA hoặc “pending/late” definition. Số `12`, “8 Capstone, 4 Lab PR”, `2 quá hạn` là sample. | Không được tính overdue/pending; giữ nguyên status raw nếu thiết kế được duyệt. |
| 10 `ME01-EL-10` | KPI support requests chờ. | #58 trả array không pagination; array length là số request hiện được trả về, không tương đương số chờ/unread. Lifecycle và projection fallback còn derived; số `5` sample. | Không map `5 chờ` hoặc SLA; widget lỗi/rỗng tách riêng. |
| 11 `ME01-EL-11` | KPI mentor rating `4.95/5` và review count. | Không có rating/feedback API được ME-01 tham chiếu; không dùng #66 course activity analytics làm rating. `4.95`, `840` là sample. | Chưa có nguồn/định nghĩa metric; `EV-01` chưa thể tải widget này. |
| 12 `ME01-EL-12` | Heading/badge API/view-all của submission panel. | Text “API #54 (Rubrics V2)” không khớp current #54; #54 không có rubric, #55 detail source/context cũng không trả rubric. “12” là sample, không lấy từ page khi chưa thống nhất pending filter. | View-all `EV-04`; rubric tag và count là display blocker. |
| 13 `ME01-EL-13` | Repeated submission preview cards và mỗi nút “Chấm bài (ME-10)”. Có 4 sample rows. | Khả dụng từ #54: `id`, `assignment_id`, `user_id`, `content?`, `files[]`, `status`, `submitted_at`, `score?`, `feedback?`. Thiếu display name/avatar, assignment/course title, due date, tags, rubric. `files` hiện map 0..1 upload candidate; source relation derived. | Card/list loading/empty/error; click từng row/button `EV-05`. Direct ME-10 so với list-first ME-09 chưa chốt. |
| 14 `ME01-EL-14` | Heading course panel, “Đồng bộ API #46” label, link “Tất cả lớp học”. | API #46 current source-backed; “đang diễn ra” chưa khớp status enum `DRAFT/PUBLISHED`. Label API là nội dung asset, không cần hiển thị người dùng. | Link tất cả `EV-02`; state theo #46. |
| 15 `ME01-EL-15` | Ba course cards lặp; Workspace (ME-03) và icon cây nội dung. | #46 fields: `id`, `title`, `description?`, `thumbnail_url?`, `price` decimal string, `status`, `mentor{id, full_name, avatar_url?}`. Track, progress, learners, lesson count không có trong response. Source chỉ direct-owner. Nút Workspace đưa `courseId` tới ME-03; icon cây nội dung dự kiến ME-06 theo label nhưng link chưa có target trong HTML. | Card group `EV-03`; icon tree `EV-04` (course tree sub-action). Empty/partial/error phải thuộc widget riêng. |
| 16 `ME01-EL-16` | Heading hộp thư hỗ trợ và badge “5 chờ”. | Badge là sample; #58 không trả unread/queue count và không pagination. | View-all badge không phải trạng thái API; `EV-06` cho support workspace. |
| 17 `ME01-EL-17` | Repeated support request previews và mỗi nút “Trả lời ngay (ME-12)”. Có 3 sample rows. | #58 field có thể dùng: request `id/course_id/student/status/created_at/resolved_at?`; student `id/full_name/avatar_url?`; `messages[]` với author/content/attachments/created_at. Không có subject, course title, unread, SLA, hoặc last-activity field. Response tải full thread. | Card list `EV-07`; direct ME-12 so với ME-11 trước khi chọn request chưa chốt. |
| 18 `ME01-EL-18` | Link “Mở Workspace Hỗ Trợ Kỹ Thuật Tập Trung”. | HTML `href="#"`; inventory route ME-11 `/mentor/support` là đích phù hợp theo nhãn, nhưng chưa được nối trong app. | `EV-06`. |
| 19 `ME01-EL-19` | Lịch mentorship heading và số lượng ca `2`. | Không có API calendar/availability trong inventory của ME-01; kỳ/ngày/đếm là sample. | Không có loading/data event xác thực. |
| 20 `ME01-EL-20` | Hai appointment cards với thời gian, attendee, topic, room/link và buttons Meet/details. | Thời gian, attendee, Meet URL, room và “chuẩn bị diễn ra” là sample; không có provider/contract. | CTA `EV-11`; external navigation, permissions và URL security đều chưa xác định. |
| 21 `ME01-EL-21` | Academic notices heading và term “Fall 2025”. | Không có API list/broadcast notices cho Mentor trong ME-01. API #63 tạo notification; #64 đọc delivery status theo ID, không phải notices inbox. | Static heading/sample; `EV-12`. |
| 22 `ME01-EL-22` | Hai academic notice cards. | Nội dung và timestamp là sample; nguồn dữ liệu, quyền, trạng thái đã đọc và điều hướng chưa có contract. | Không coi là API #63/64 result; `EV-12`. |
| 23 `ME01-EL-23` | Footer brand, academic standards, partner links, hotline/email, policy links và copyright. | Logo, tổ chức, hotline `1900 6886`, email, chứng nhận, nội dung và năm là asset text; không có dữ liệu/URL được xác minh. Anchors placeholder. | Footer static; link events `EV-12`, không điều hướng runtime. |

## 4. Conditional UI & state variations
- States theo inventory: loading/partial/empty/error
- Detail/conditional visibility: xem section elements/state của [DD nguồn](../../screen_stitch/04_mentor/ME-01_dashboard-mentor/ME-01.md); không diễn giải ảnh tĩnh thành behavior runtime.

## 5. Link
- [Events](02-events.md) · [Data Flow](03-data-flow.md) · [Tests](07-test-cases.md)
