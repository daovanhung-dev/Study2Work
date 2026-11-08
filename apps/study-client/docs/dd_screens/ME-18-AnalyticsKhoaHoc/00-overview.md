# ME-18 — Analytics khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-18` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/analytics` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-18.md](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18.md), [ME-18_PLAN.md](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18_PLAN.md), [ME-18_markers.json](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/ME-18_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Expected KPI/chart cần được định nghĩa. Current #66 local source chỉ trả current-state proxy counts/timestamp, không phải learning-event history.
- In-scope: Chỉ gọi #66 với numeric course_id sau khi carrier và response được duyệt; không có period/query/export. Catalog ApiEnvelope<Page<Course>> khác local summary. AC-26 đặt #66 trước chọn Student/#67; inventory tách ME-18 khỏi ME-17. KPI, ETL state, timeframe và CSV chưa có mapping.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-26 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Expected KPI/chart cần được định nghĩa. Current #66 local source chỉ trả current-state proxy counts/timestamp, không phải learning-event history. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #66
- Liên kết màn hình dự kiến: [ME-16](../ME-16-TienDoToanKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/no-data/ready/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-18 source screen.png](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/screen_annotated.png))
- Luồng: Chỉ gọi #66 với numeric course_id sau khi carrier và response được duyệt; không có period/query/export. Catalog ApiEnvelope<Page<Course>> khác local summary. AC-26 đặt #66 trước chọn Student/#67; inventory tách ME-18 khỏi ME-17. KPI, ETL state, timeframe và CSV chưa có mapping.
- Priority: P2; Gate/source status: **R**; #66 route/module/query/model/focused-test source có local implementation. **DD BLOCKED; IMPLEMENTATION BLOCKED:** response mismatch, KPI/period/event semantics, course ID/owner policy, ETL/export, AC-26 ordering; Study Web UNWIRED; RUNTIME NOT VERIFIED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-18 — Phân tích khóa học

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-18 — Phân tích khóa học |
| Mục tiêu theo danh mục | Mentor xem chỉ số hiệu suất/hoàn thành của một course. Metric definitions, period và aggregation còn TBD. |
| Actor dự kiến | Mentor. API #66 hiện cần Bearer JWT với role MENTOR. Study Web không có route/auth runtime để xác minh. |
| Route đề xuất | /mentor/courses/:courseId/analytics theo list_screen.md; chưa được wire vào app. |
| Điều kiện vào | Mentor đã xác thực và có course context từ ME-16; cần numeric course_id:int64 cho API #66. ME-16 CTA hiện là href="#" và chưa có carrier/slug mapping được duyệt. |
| Điều kiện ra | Nút “Quay lại tiến độ toàn khóa (ME-16)” gợi ý về ME-16; link chưa có destination. AC-26 diagram xếp #66 trước chọn Student/#67, còn inventory tách ME-18/#66 khỏi ME-17/#67. |
| API | #66 GET /api/v1/mentor/courses/{course_id}/analytics. Không gộp #65 course roster progress hoặc #67 selected-Student progress. |
| Tác động dữ liệu | API #66 hiện chỉ đọc; không có mutation hoặc server-to-server call #65/#67. |
| Trạng thái đặc tả | **DD BLOCKED — chưa DD READY.** Response shape, KPI semantics, period, empty meaning và loaded presentation chưa được phê duyệt. |
| Trạng thái triển khai | **IMPLEMENTATION BLOCKED.** Không thể map KPI/timeframe/export hoặc xác nhận course identity và route từ nguồn hiện có. |
| Trạng thái chạy thật | **RUNTIME NOT VERIFIED.** Có server source/test source; Study Web chưa có app route. Live DB schema/deployment chưa xác minh. |

### Nguồn và độ tin cậy

| Nguồn | Bằng chứng sử dụng | Phân loại |
|---|---|---|
| [Danh mục màn hình](../../list_screen.md) | ME-18 route, KPI/charts mục tiêu, #66, states và link ME-16 | Expected behavior; metric definitions còn TBD |
| [Kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) | F10 dependencies và ME-18 status | Expected behavior / tracker |
| [ME-16 DD](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md) | Placeholder event mở ME-18 và cảnh báo về ID carrier/AC-26 order | Cross-screen evidence; chưa wired |
| [Ảnh gốc](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/screen.png) / [HTML mẫu](../../screen_stitch/04_mentor/ME-18_analytics-khoa-hoc/code.html) | Static controls, empty state, literal KPI/copy và inline sync handler | Prototype, không phải runtime |
| [API catalog](../../../../../docs/lists/list_api.md) | #66 method/path/auth/int64/response/errors được khai báo | Declared contract |
| [AC-26 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) | #65 → #66 → chọn Student → #67 | Expected behavior; khác inventory |
| [API #66 route](../../../../study-server/app/api/v1.py) và [module](../../../../study-server/app/modules/mentor/api_66_mentor_course_analytics) | Current route/auth/parse/query/aggregation/response/errors | Current source; DB/deployment chưa xác minh |
| [API #66 DD](../../../../study-server/docs/dd/66_mentor_course_analytics) | Draft/Needs Confirmation, direct catalog contract, local DERIVED summary và open questions | Current API documentation |
| [API #66 focused tests](../../../../study-server/tests/modules/mentor/api_66_mentor_course_analytics/test_mentor_course_analytics.py) | Auth, owner, aggregate, empty, error, read-only và OpenAPI coverage | Đã đọc; không chạy phiên này |
| [.agents/web-study/design.md](../../../../../.agents/web-study/design.md) / [.agents/server-study/database.md](../../../../../.agents/server-study/database.md) | Intended UI constraints và checked-in DB evidence boundary | Context; không phải runtime proof |

### Expected/current discrepancies

| Chủ đề | Expected evidence | Current evidence | Cần quyết định |
|---|---|---|---|
| Response shape | Catalog/diagram: ApiEnvelope<Page<Course>> | Local #66: ApiEnvelope<MentorCourseActivityAnalytics> summary | API owner duyệt schema; Page<Course> không có analytics fields |
| KPI definitions | Completion, average duration, discussion interaction trên mockup; danh mục nói KPI do BE trả nhưng chưa định nghĩa | #66 chỉ có tracked lesson/Student pairs, distinct Students, max last-access timestamp | Product/domain owner định nghĩa metric nguồn và công thức |
| Time window | Mockup có 7 ngày, 30 ngày, toàn khóa; danh mục nói period TBD | #66 không nhận query period/from/to và aggregate mọi timestamp còn lưu | Chốt window semantics và API support trước khi bật select |
| Learning event semantics | AC-26 nói “Aggregate learning events” | Legacy source chỉ có current progress last_accessed_at; không có event ledger | Xác nhận nguồn event hoặc chấp nhận proxy với tên/giới hạn rõ |
| Empty/inactive meaning | Screenshot nói Chưa kích hoạt/ETL chờ | #66 empty trả 0/0/null; không có pipeline status | Chốt cách phân biệt pipeline inactive với không có progress marker |
| Course context | Screenshot có tên, mã CS-402, học kỳ | #66 nhận course_id nhưng không trả course metadata/term | Chốt producer và numeric ID mapping; không lấy từ copy tĩnh |
| Export | CSV control trong mockup đang disabled | Không có export endpoint/job/file | Product/API cần xác định contract trước khi enable |
| AC-26 order | Inventory đặt #66 trên ME-18, liên kết ME-16 | Diagram đặt #66 trước chọn Student/#67 | Flow owner xác nhận sequencing |
| Web/runtime | Route trong inventory | Study Web source/client route absent, context UNWIRED | Chưa có UI runtime để xác minh |

### Quy tắc không suy diễn

1. Không ánh xạ tracked_lesson_accesses thành completion rate, discussion count hoặc số event.
2. Không ánh xạ students_with_activity thành enrollment count; local query không yêu cầu ACTIVE enrollment.
3. last_activity_at là MAX timestamp còn lưu trong progress state, không phải timestamp event stream hoặc dữ liệu trong timeframe được chọn.
4. Không thêm from/to, period, page, export, ETL state, chart, polling, cache hoặc job chỉ từ screenshot.
5. Course name/code/term, “Schema v2.4 Analytical Ready”, “WCAG 2.1 AA Compliant”, ETL/telemetry và “đủ số liệu thực tế” đều là static claim chưa được #66 chứng minh.
6. Giữ #65 roster, #66 course activity proxy và #67 student detail là các API riêng; AC-26/order discrepancy phải được owner giải quyết.
