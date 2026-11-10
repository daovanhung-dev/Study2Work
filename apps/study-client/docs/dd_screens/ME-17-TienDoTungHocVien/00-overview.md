# ME-17 — Tiến độ từng học viên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-17` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/students/:studentId/progress` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-17.md](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17.md), [ME-17_PLAN.md](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17_PLAN.md), [ME-17_markers.json](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Timeline và bài còn thiếu là expected design; current #67 chỉ trả snapshot trạng thái lesson theo curriculum order, không có event history hoặc assignment/quiz activity.
- In-scope: Chỉ gọi #67 với course_id + student_id numeric sau khi ME-16 handoff được chốt; không gộp #65/#66. Catalog ApiEnvelope<Page<Course>> khác local ApiEnvelope<StudentCourseProgress>; AC-26 đặt #66 trước chọn Student/#67, khác inventory; loaded timeline và mockup metrics chưa có field mapping.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-26 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Timeline và bài còn thiếu là expected design; current #67 chỉ trả snapshot trạng thái lesson theo curriculum order, không có event history hoặc assignment/quiz activity. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #67
- Liên kết màn hình dự kiến: [ME-16](../ME-16-TienDoToanKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/denied/not-found |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-17 source screen.png](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/screen_annotated.png))
- Luồng: Chỉ gọi #67 với course_id + student_id numeric sau khi ME-16 handoff được chốt; không gộp #65/#66. Catalog ApiEnvelope<Page<Course>> khác local ApiEnvelope<StudentCourseProgress>; AC-26 đặt #66 trước chọn Student/#67, khác inventory; loaded timeline và mockup metrics chưa có field mapping.
- Priority: P2; Gate/source status: **R**; #67 route/module/query/model/focused test source có local implementation. **DD BLOCKED; IMPLEMENTATION BLOCKED:** catalog/local response mismatch, AC-26 ordering, selected-row carrier, loaded timeline/metrics, owner/ACTIVE-roster/privacy and live-schema confirmation; Study Web UNWIRED; RUNTIME NOT VERIFIED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-17 — Tiến độ từng học viên

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-17 — Tiến độ từng học viên |
| Mục tiêu theo danh mục | Mentor xem tiến độ của một học viên trong một khóa học; danh mục mô tả timeline học tập và bài còn thiếu. |
| Actor dự kiến | Mentor. API #67 hiện yêu cầu Bearer JWT với role MENTOR. Study Web không có route/client/auth runtime trong checkout. |
| Route đề xuất | /mentor/courses/:courseId/students/:studentId/progress theo list_screen.md; đây chưa phải route đã wire. |
| Điều kiện vào dự kiến | Mentor đã xác thực; có course_id và student_id dạng int64 từ dòng học viên được chọn tại ME-16. Carrier và slug-to-int64 mapping chưa có contract. |
| Điều kiện ra dự kiến | Quay về ME-16 theo cùng course_id. Inventory nối ME-16 → ME-17; AC-26 diagram đặt bước #66 trước chọn học viên/#67 và khác inventory. |
| API | #67 GET /api/v1/mentor/courses/{course_id}/students/{student_id}/progress. Không gộp #65 roster progress hoặc #66 course analytics. |
| Tác động dữ liệu | #67 hiện là read-only; không có mutation, ghi nhận sự kiện hay side effect DB. |
| Trạng thái đặc tả | **DD BLOCKED — chưa DD READY.** Catalog/API shape và loaded timeline presentation chưa được phê duyệt đủ để triển khai không suy đoán. |
| Trạng thái triển khai | **IMPLEMENTATION BLOCKED.** API mapping, identity handoff, loaded view, eligibility/authorization policy và Study Web runtime còn thiếu hoặc cần xác nhận. |
| Trạng thái chạy thật | **RUNTIME NOT VERIFIED.** Có current server source và test source, nhưng không có Study Web runtime; không xác minh deployment hoặc live schema trong phiên này. |

### Nguồn và độ tin cậy

| Nguồn | Bằng chứng sử dụng | Phân loại |
|---|---|---|
| [Danh mục màn hình](../../list_screen.md) | ME-17, route đề xuất, trạng thái kỳ vọng, API #67 và liên kết ME-16 | Expected behavior |
| [Kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) | Dependency F10, tracker và AC-26 discrepancy | Expected behavior / tracker |
| [ME-16 DD](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md) | Candidate handoff course_id + student_id từ roster; #65 local response vẫn lệch catalog | Cross-screen evidence; carrier chưa được wire |
| [Ảnh gốc](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/screen.png) và [HTML mẫu](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/code.html) | Empty state, literal copy, controls/anchors và refresh handler | Static prototype, không phải runtime |
| [API catalog](../../../../../docs/lists/list_api.md) | #67 method/path/auth/path IDs/response và error set được khai báo | Declared design contract; không chứng minh runtime |
| [AC-26 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) | Thứ tự #65 → #66 → chọn Student → #67 | Expected behavior; khác inventory |
| [#67 route](../../../../study-server/app/api/v1.py) và [module](../../../../study-server/app/modules/mentor/api_67_mentor_student_progress) | Current route, auth, parse, owner/roster checks, query, projection, response/errors | Current source; deployment/live schema chưa xác minh |
| [#67 API DD](../../../../study-server/docs/dd/67_mentor_student_progress) | Draft/Needs Confirmation, declared-vs-derived behavior và open questions | Current design documentation |
| [#67 focused test source](../../../../study-server/tests/modules/mentor/api_67_mentor_student_progress/test_mentor_student_progress.py) | Các case test local/fake DB đã khai báo | Đã đọc; không chạy trong phiên này |
| [.agents/web-study/design.md](../../../../../.agents/web-study/design.md) và [.agents/server-study](../../../../../.agents/server-study) | UI/runtime boundary và server source conventions | Context; Study Web là UNWIRED |

### Discrepancies và blockers

| Chủ đề | Expected evidence | Current evidence | Quyết định cần có |
|---|---|---|---|
| API #67 success shape | Catalog/AC khai báo ApiEnvelope<Page<Course>> | Local view/model trả ApiEnvelope<StudentCourseProgress> dạng singular, không có Page | API/flow owner duyệt contract và mapping |
| AC-26 ordering | Inventory tách ME-16/#65 → ME-17/#67 và ME-18/#66 | Diagram đặt #66 trước chọn Student và #67 | Flow owner chốt orchestration; không tự đổi thứ tự |
| Handoff identity | ME-16 chọn học viên trong course và phải truyền cả hai int64 | Không có route/client/carrier; ME-16 prototype dùng slug ở course context | Chốt nguồn numeric IDs và route state |
| Loaded timeline | Danh mục yêu cầu timeline/bài còn thiếu | Screenshot/HTML chỉ có empty state; #67 là snapshot per-lesson theo thứ tự curriculum | Duyệt populated row design và ý nghĩa trạng thái; không diễn giải snapshot thành lịch sử sự kiện |
| Nội dung tĩnh trong mockup | Course title, enrollment, assignment/quiz, self-study, last-send, comment/milestone claims | #67 không trả các dữ kiện đó | Xác định nguồn/loại bỏ claims trước implementation; không gọi API mới theo suy đoán |
| Quyền và schema | Inventory nói kiểm tra ownership | Local source yêu cầu direct owner, ACTIVE enrollment và role STUDENT; legacy BIGINT khác V1-PILOT UUID | Xác nhận assigned Mentor vs direct owner, privacy/error policy, schema/deployment |
| Study Web | Route đề xuất trong inventory | Không có editable src/package.json/route; context UNWIRED | Chưa có runtime để xác minh |

### Quy tắc không suy diễn

1. Tách declared catalog/AC khỏi current source. Local behavior không tự trở thành contract đã duyệt.
2. Không gộp #65, #66, #67. #65 trả roster summary, #66 là course analytics/current-state activity proxy, #67 là per-student lesson snapshot.
3. Không coi empty timeline copy là bằng chứng không có event history; #67 không trả event ledger.
4. Không ánh xạ course title, student code, enrollment badge, assignment/quiz count, self-study time, last-send freshness, mentor comments hoặc project milestones từ fields không liên quan.
5. Không thêm API, polling, pagination, cache, retry, timer đồng bộ hay click-through lesson khi chưa có contract/source.
6. Tên “giám sát trực tiếp”, WCAG 2.1 AA và “tự động đánh dấu hoàn thành” là static copy/claim, chưa được runtime hoặc policy xác nhận.
