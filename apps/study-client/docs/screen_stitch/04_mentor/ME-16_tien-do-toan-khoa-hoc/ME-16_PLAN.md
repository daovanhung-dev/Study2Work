# ME-16 — Kế hoạch đặc tả màn hình Tiến độ toàn khóa học

## 1. Phạm vi phiên

- **Screen ID:** ME-16 — Tiến độ toàn khóa học.
- **Task type:** `docs`; scopes `web-work`, `server-study`.
- **Mục tiêu:** Hoàn thiện plan, marker map, ảnh có marker và DD A–F cho riêng ME-16; ghi rõ bằng chứng expected/current, trạng thái triển khai và các quyết định còn thiếu.
- **Không thuộc phiên này:** ME-17 và ME-18. Không thay đổi `screen.png` hoặc `code.html`; không chạy application tests/runtime.
- **Baseline asset:** `screen.png` 1600×1440, 294,250 bytes, SHA-256 `f94e642b19786f6a111f151986be61366cf96cd1571e222344dc6f804eea4d89`; `code.html` 21,826 bytes, SHA-256 `08529aff6c992afdb5f59f1a7dd04bbf2c3b92333c13a8744ed38e0d4f9b7eb9`.

## 2. Expected behavior

- `list_screen.md` và `dd_screens/PLAN.md` định nghĩa route `/mentor/courses/:courseId/progress`, AC-26, API #65, luồng sang ME-17/#67 và liên kết ME-18/#66.
- Mục đích trên danh mục là bảng tiến độ học viên/lesson, có nhóm hỗ trợ và trạng thái `loading`, `empty`, `ready`, `denied`.
- AC-26 diagram khai báo #65 là `GET /api/v1/mentor/courses/{course_id}/progress`, `course_id:int64`, Mentor RBAC, success `200 DESIGN_RESOURCE_RETRIEVED`, lỗi 401/403/404/500, response `ApiEnvelope<Page<Course>>`. Diagram xếp #66 aggregate learning events sau #65, rồi chọn Student và gọi #67 trước khi render dashboard + drill-down.
- Các yêu cầu dùng placeholder/slug, tìm email, phân nhóm nhắc nhở, số ghi danh, nhật ký nộp bài, chuyên cần, đồng bộ LMS, SCORM/xAPI, WCAG và làm mới 15 phút chưa được coi là contract.

## 3. Current behavior và source trace

### 3.1 Study Web và prototype

- Study Web được đăng ký `UNWIRED`; không có app/router/API client runtime để xác nhận route, auth guard, fetch, điều hướng hay trạng thái thực.
- `code.html` là prototype tĩnh. Có 14 anchor đều `href="#"`, một `<select>` với ba slug, một text input, ba filter button và một nút refresh.
- Chỉ refresh có handler: thêm spinner/disabled, chờ 1000 ms rồi khôi phục; không gọi API, toast, cập nhật dữ liệu hay polling. Search, select và filter không có handlers. Không có table header/rows; chỉ có empty state.
- Course selector labels/slugs, class code `CS-2025-FE02`, enrollment `0`, “Vừa xong”, hệ thống “đồng bộ trực tiếp”, claims copy, diagnostics, reminder criteria và cadence 15 phút đều là dữ liệu/copy tĩnh.

### 3.2 API #65

- Local route: `GET /api/v1/mentor/courses/{course_id}/progress`; Bearer auth và role `MENTOR`; path signed int64; không query/body/page-size.
- Local source kiểm tra course tồn tại và `courses.mentor_id` trước aggregate; response lỗi source-backed là 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- Query lấy distinct users từ enrollment `ACTIVE` với role `STUDENT`, lessons `PUBLISHED`, chọn bản ghi progress mới nhất theo `last_accessed_at DESC NULLS LAST, id DESC`. `completed_lessons` đếm trạng thái `COMPLETED`; `progress_percent = floor(sum(COALESCE(progress_percent, 0)) / total_published_lessons)`; mẫu số 0 cho kết quả 0.
- Local response hiện trả `data.items[]` gồm `student{id, full_name, avatar_url?}`, `completed_lessons`, `total_lessons`, `progress_percent`; `data.pagination` luôn là một trang chứa toàn bộ roster. Không có pagination request và không có bound.
- API catalog/AC-26 ghi `ApiEnvelope<Page<Course>>`; local source trả derived `ApiEnvelope<MentorStudentProgressPage>`. DD API #65 ở trạng thái Draft/Needs Confirmation; source behavior chưa phải approved contract. Không tự đổi catalog hoặc coi dữ liệu local là schema live.
- #65 không trả email, last activity, submission, attendance, due date, support category, course title/code, update timestamp hoặc reminder status.

### 3.3 Upstream, downstream và analytics boundary

- API #46 local source có `CoursePage` với numeric `id`, nhưng prototype selector dùng slugs; không có slug→int64 mapping hay selector handoff được duyệt.
- API #67 là route drill-down riêng cần cả `course_id` và `student_id`; local response có summary + lesson-level progress. ME-17 không được tự nhận student ID từ hàng chưa tồn tại.
- API #66 thuộc ME-18. Local source trả activity proxy `tracked_lesson_accesses`, `students_with_activity`, `last_activity_at` dựa trên `lesson_progress.last_accessed_at`, không phải event ledger. Catalog/AC cũng khai báo `Page<Course>`, còn local source trả summary object.
- **DISCREPANCY:** AC-26 diagram xếp #66 trước lựa chọn Student/#67; screen inventory tách ME-16/#65 → ME-17/#67 và ME-18/#66. Ghi nhận hai luồng, chờ owner xác nhận; không tự gộp analytics vào ME-16.
- Local Study database candidate dùng legacy BIGINT tables; V1-PILOT schema là UUID/versioned progress và khác mô hình. Live schema/deployment chưa được xác minh.

## 4. Dự kiến marker coverage

Tạo **42 marker tuần tự** cho các thành phần quan sát được. Mỗi marker sẽ có đúng một dòng element trong DD; icon/trang trí gắn với control hoặc khối copy gần nhất, còn các link/button độc lập có marker riêng.

1. Header brand; 2–6. năm mục điều hướng mentor; 7. notification icon/link; 8. profile mentor.
9–11. breadcrumb course list, breadcrumb course detail, breadcrumb current page; 12. class-code pill.
13–17. hero label, page title, descriptive copy, total-enrollment metric, update-time metric.
18–25. course label/control, completion label, ba filter riêng, search label/control.
26–27. table title bar, sync-status badge.
28–31. empty illustration, hourglass status badge, empty headline, empty-state description.
32–35. refresh action, ME-18 action, cohort diagnostic copy, LMS manual link.
36–37. system status/standards statement, stated refresh cadence.
38–42. footer brand icon, footer legal/certification copy, three footer links.

Marker coordinates sẽ đặt trong vùng tương ứng và trong bounds 1600×1440; ảnh annotation dùng bản sao của PNG, không chỉnh sửa ảnh nguồn. Nếu visual review cho thấy marker che chữ/control hoặc thiếu khối nhìn thấy, sửa tọa độ/map trước khi hoàn tất DD.

## 5. Sự kiện cần đặc tả

1. **EV-01 Load / resolve route:** input dự kiến `courseId` + auth state; không có Study Web runtime. Mô tả #65 source behavior và lỗi, nhưng chỉ sau khi numeric ID mapping, response contract và authorization policy được xác nhận mới đủ điều kiện implement.
2. **EV-02 Change course:** select hiện dùng slug và không có handler. #46 có numeric IDs nhưng không có mapping từ prototype; chặn.
3. **EV-03 Change progress filter:** ba nút không có handler; #65 response không chứa category đúng tiến độ/cần nhắc. Tiêu chí phân loại chưa có contract; chặn.
4. **EV-04 Search student:** input không có handler; API không có query/search và response không có email. Không tự suy rộng tìm email; chờ quy tắc client/server và dữ liệu được phê duyệt.
5. **EV-05 Refresh:** phân biệt hiệu ứng 1 giây hiện có với yêu cầu refresh dữ liệu. Prototype không gọi #65, và polling 15 phút không có implementation/contract.
6. **EV-06 Open student progress:** inventory yêu cầu action sang ME-17; prototype không có rows/actions. Handoff cần `course_id:int64` và `student_id:int64` cho #67.
7. **EV-07 Open ME-18 analytics:** anchor là placeholder; cần `course_id` hợp lệ, destination và quyết định về vị trí #66 theo discrepancy AC-26.
8. **EV-08 Header/breadcrumb/help/footer links:** tất cả hiện `href="#"`; record placeholder-only, không gán route mới.
9. **EV-09 Auto-refresh claim:** text “Mỗi 15 phút” không có timer; không thiết kế polling/retry/cache behavior nếu chưa có policy.

## 6. Trạng thái và blocker cần thể hiện trong DD

- **Prototype hiện có:** chỉ một trạng thái empty tĩnh.
- **Danh mục mong đợi:** loading, empty, ready, denied. DD sẽ tách chúng khỏi trạng thái prototype và ghi rõ điều kiện/chuyển trạng thái chưa được contract hóa.
- **Lỗi source #65:** mô tả HTTP/business code source-backed; không suy ra màn hình auth/session UX nếu Study Web chưa có.
- **Blockers:** Page<Course> vs student-progress-page; AC-26 ordering vs screen links; slug→int64; no paging bound; chưa có field/filter/search/reminder/submission/activity mapping; #65 formula/eligibility/privacy/live schema còn Draft/DERIVED; ME-17 action thiếu row; #66 analytics contract chưa chốt; Study Web UNWIRED.
- **Phân loại kết quả:** DD có thể đạt `DD READY` chỉ khi tài liệu mô tả đầy đủ phần đã biết và giữ mọi quyết định chưa có ở trạng thái block rõ ràng. `IMPLEMENTATION BLOCKED` được đánh giá riêng theo dependencies; không ghi `RUNTIME VERIFIED` khi chưa có runtime evidence.

## 7. Thứ tự thực hiện và kiểm soát

1. Hoàn tất plan này trước marker/DD.
2. Tạo `<ME-16>_markers.json` với `id`, label, type/group và tọa độ; tạo SVG overlay/annotated PNG từ `screen.png`.
3. Viết `ME-16.md` đủ A–F: expected/current split, source references, 42 element rows, tuần tự từng event với input/process/output/error, state/navigation matrix và acceptance checklist.
4. Cập nhật hai tracker rows: số artifact/marker, blocker và trạng thái riêng `DD READY`/`IMPLEMENTATION BLOCKED`/`RUNTIME NOT VERIFIED` hoặc giữ DD blocked nếu contract gap khiến không thể triển khai.
5. Cập nhật worklog; kiểm tra hash nguồn không đổi, JSON/map và marker sequence/in-bounds, 1:1 marker↔element, relative links, ảnh annotated đã xem trực tiếp, `git diff --check`. Không chạy app tests/runtime.
6. Dừng sau ME-16; ME-17 thuộc phiên khác.

## 8. Nguồn đã đối chiếu

- `apps/study-client/docs/list_screen.md` — ME-16/17/18, AC-26, route, API và luồng màn hình.
- `apps/study-client/docs/screen_stitch/dd_screens/PLAN.md` — tracker tổng và blocker hiện tại.
- `apps/study-client/docs/screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/{screen.png,code.html}` — thiết kế và prototype.
- `apps/study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio` — AC-26 sequence.
- `docs/lists/list_api.md` — API catalog #65–#67.
- `apps/study-server/app/api/v1.py`, `app/modules/mentor/api_46_mentor_courses/`, `api_65_mentor_course_progress/`, `api_66_mentor_course_analytics/`, `api_67_mentor_student_progress/` — local source routes/behavior/models.
- `apps/study-server/docs/dd/65_mentor_course_progress/`, `66_mentor_course_analytics/` and `apps/study-server/tests/modules/mentor/api_65_mentor_course_progress/test_mentor_course_progress.py` — API DD, unresolved questions and test coverage source; tests not run.
- `.agents/web-work/study/` — registered Study Web `UNWIRED` context; no Study runtime route/source verified.
