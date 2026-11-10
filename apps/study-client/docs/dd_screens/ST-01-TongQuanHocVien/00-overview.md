# ST-01 — Tổng quan học viên · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ST-01` |
| Module | Student |
| Route | `/student` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Trạng thái:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Tài liệu truy vết được inventory, activity và API catalog hiện có; không thể chốt data mapping, orchestration hoặc xử lý rỗng do #20/#21/#38/#43 đều Draft và không có route Study runtime. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ST-01.md](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01.md), [ST-01_PLAN.md](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_PLAN.md), [ST-01_markers.json](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Tổng quan khóa đang học, tiến độ, thành tích và thông báo; widget độc lập.
- In-scope: Chỉ sau role STUDENT hợp lệ; load #20/#21; thành tích #38, thông báo #43 lazy/parallel.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-13,AC-18,AC-20 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Tổng quan khóa đang học, tiến độ, thành tích và thông báo; widget độc lập. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #20, #21, #38, #43
- Liên kết màn hình dự kiến: [ST-08](../ST-08-KhoaHocCuaToi/00-overview.md), [ST-20](../ST-20-TongQuanTienDo/00-overview.md), [ST-26](../ST-26-ThongBaoHocVien/00-overview.md), [ST-02](../ST-02-HoSoCaNhan/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | partial-widget/empty/loading/403 |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ST-01 source screen.png](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/screen_annotated.png))
- Luồng: Chỉ sau role STUDENT hợp lệ; load #20/#21; thành tích #38, thông báo #43 lazy/parallel.
- Priority: P1; Gate/source status: **D; DD BLOCKED; IMPLEMENTATION BLOCKED; RUNTIME NOT VERIFIED:** #20/#21 Draft response UserProfile không biểu diễn Course/progress theo AC-13; nhánh EMPTY/HAS DATA cùng tới node render; #21 query/formula/merge, #38 award/projection/filter/page và #43 recipient/fields/order còn mở; API routes/modules/tests NOT_FOUND; AC-18 order lệch inventory widget độc lập; HTML endpoint paths sai, anchors chỉ là `#`; Study Web UNWIRED và visual target lệch design guide

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ST-01 — Tổng quan học viên

> **Trạng thái:** `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. Tài liệu truy vết được inventory, activity và API catalog hiện có; không thể chốt data mapping, orchestration hoặc xử lý rỗng do #20/#21/#38/#43 đều Draft và không có route Study runtime.

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### A.1. Định danh và phạm vi

| Thuộc tính | Giá trị |
|---|---|
| Screen ID / tên | ST-01 — Tổng quan học viên (Page) |
| Actor | Student theo inventory, AC-13, AC-18, AC-20 và các API catalog liên quan. |
| Mục tiêu | Hiển thị khóa học, tiến độ, thành tích và thông báo dưới dạng các widget riêng; chỉ render dữ liệu có nguồn được xác nhận. |
| Route trong inventory | `/student` (đề xuất; current Study Web không có route source). |
| APIs dự kiến | #20 courses, #21 progress tổng hợp, #38 achievements, #43 notifications. Tất cả là design-only trong API catalog, không phải runtime calls. |
| Liên kết màn hình | ST-08 Khóa học của tôi, ST-20 Tổng quan tiến độ, ST-26 Thông báo học viên, ST-02 Hồ sơ cá nhân. Đây là quan hệ inventory; route/handoff client chưa wired. |
| Elements / events | 37 nhóm element `ST01-EL-01…37`; 10 event `ST01-EV-01…10`. |
| Current asset state | Static specification-gated hand-off; không có course, progress, award hoặc notification payload thật. |
| Trạng thái | `DD BLOCKED`; `IMPLEMENTATION BLOCKED`; `RUNTIME NOT VERIFIED`. |

### A.2. Expected behavior — inventory, AC và API catalog

- Inventory ST-01 khai báo `/student`, actor Student, widget khóa học/tiến độ/thành tích/thông báo; #20/#21 khi vào màn hình, #38/#43 lazy hoặc parallel; state labels `partial-widget/empty/loading/403`. Đây là target design, không xác nhận runtime.
- AC-13 yêu cầu #20 đọc danh sách Enrollment/Course, sau đó #21 đọc tiến độ và client ghép theo course. Activity diagram có nhánh `EMPTY` và `HAS DATA` cùng đi tới node “Hiển thị khóa học + % hoàn thành”. Đây là `DISCREPANCY`; không tự sửa nhánh hoặc chọn một order khác.
- AC-18 yêu cầu #21 aggregate, chọn một course, #37 detail progress, #38 achievement rồi render. Inventory ST-01 và ST-20 lại xem #21/#38 là các widget độc lập. Không suy luận thời điểm gọi #38 hoặc ép ST-01 theo chuỗi chi tiết AC-18.
- AC-20 định nghĩa #43 lấy notification list/unread badge; #44/#45 thực hiện mark-read ở luồng notification center. ST-01 chỉ có link tới ST-26, không có mutation event.
- API catalog contract được giữ nguyên: #20 GET `/api/v1/users/me/courses`; #21 GET `/api/v1/users/me/progress`; #38 GET `/api/v1/users/me/achievements`; #43 GET `/api/v1/users/me/notifications`. Không dùng các endpoint path khác xuất hiện trong HTML.
- [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md) và [AC activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) là nguồn quy trình; API catalog/DD và current source là các bằng chứng riêng.

### A.3. Current behavior và tài sản

- `screen.png` là ảnh gốc hợp lệ 1067×1600, SHA-256 `8ac0708a12c0221ef529b26c3fc601d46405003476225fdc492475df8ed6b9cd`; ảnh được giữ byte-for-byte và dùng làm nền annotation.
- `code.html` là static hand-off page, SHA-256 `f9870e9e6ec797ee96f340d663efaa9904ae1c5b5f3300be140575c50244770f`. Nội dung có status gate, nguyên tắc zero synthetic data, bốn widget unavailable và endpoint matrix; không có API `fetch`/XHR, forms, inputs, buttons, data binding hoặc app handler. Có Tailwind CDN/config, ba remote Google Fonts imports và 13 anchor `href="#"`; nhãn `data-path` không tạo route.
- Endpoint matrix trong HTML ghi #20 `/api/v1/courses/enrolled`, #21 `/api/v1/students/progress`, #38 `/api/v1/achievements`, #43 `/api/v1/notifications/latest`. Cả bốn khác path trong API catalog. Đặc biệt “latest” không có ordering được khóa cho #43.
- Study Web hiện không có editable `src`, package manifest, router hoặc Student `/student` route. Current ignored `dist` chỉ là build artifact; serving/deployment chưa được xác minh.
- Exact-path search trong `apps/study-server/app/api/v1.py`, `app/modules/` và `tests/` không thấy #20/#21/#38/#43. API DDs của bốn endpoint đều `Draft — Needs Confirmation`; không có query, response projection hoặc DB side effect runtime để truy vết.
- Tên “Nguyễn Văn A”, “Hợp đồng chờ kích hoạt”, “WCAG 2.1 AA Compliant” và nội dung gateway trong ảnh/HTML là static UI copy; không xác nhận current user, API health, accessibility audit, chữ ký/chứng chỉ hoặc notification transport.

### A.4. Ma trận API và source status

| API | Request theo catalog | Response / statuses theo catalog | Current source và điểm chưa chốt |
|---|---|---|---|
| #20 | `GET /api/v1/users/me/courses`; Student Bearer; `status?:string`, `page?:int32`; body không khai báo. | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/422/500 theo catalog. | `NOT_FOUND` route/module/query/test. Draft Q-20-01…05: catalog UserProfile khác danh sách Course của AC-13; status predicate/enum, page semantics, empty wire shape và JWT subject → Enrollment ownership chưa xác nhận. |
| #21 | `GET /api/v1/users/me/progress`; Student Bearer; query ghi `course_id list hoặc aggregate?:string`; body không khai báo. | `ApiEnvelope<UserProfile>`; 200 `DESIGN_RESOURCE_RETRIEVED`; 401/403/500. | `NOT_FOUND` route/module/query/test. Draft Q-21-01…05: selector grammar, nguồn/công thức progress, response schema/merge key, user binding và no-enrollment/no-progress shape chưa chốt. |
| #38 | `GET /api/v1/users/me/achievements`; Student Bearer; `course_id?:int64`; body không khai báo. | `ApiEnvelope<Page<Achievement>>`; catalog fields `id`, `code`, `title`, `awarded_at`, `course_id?`; 200/401/403/500. | `NOT_FOUND` route/module/query/test. Draft Q-01…06 về award criteria, projection/source, filter/access, pagination/order/empty và query validation. Không có contract cho certificate, proof, KPI hoặc signature. |
| #43 | `GET /api/v1/users/me/notifications`; Student Bearer; `unread_only?:boolean`, `page?:int32`; body không khai báo. | `ApiEnvelope<Page<Notification>>`; 200/401/403/500. | `NOT_FOUND` route/module/query/test. Draft Q-43-01…07: recipient/broadcast, channels/status, read timestamps, pagination/order, timezone/null behavior và error envelope chưa được chốt. |

Tài liệu từng API: [#20](../../../../study-server/docs/dd/20_users_me_courses/02_Overview.md) / [questions](../../../../study-server/docs/dd/20_users_me_courses/OPEN_QUESTIONS.md), [#21](../../../../study-server/docs/dd/21_users_me_progress/02_Overview.md) / [questions](../../../../study-server/docs/dd/21_users_me_progress/OPEN_QUESTIONS.md), [#38](../../../../study-server/docs/dd/38_users_me_achievements/02_Overview.md) / [questions](../../../../study-server/docs/dd/38_users_me_achievements/OPEN_QUESTIONS.md), [#43](../../../../study-server/docs/dd/43_users_me_notifications/02_Overview.md) / [questions](../../../../study-server/docs/dd/43_users_me_notifications/OPEN_QUESTIONS.md). DDL/ERD là design evidence, không phải live schema proof.

### A.5. Discrepancies, bảo mật và visual target

| Vấn đề | Expected evidence | Current evidence / impact |
|---|---|---|
| #20 response vs AC-13 | AC-13 cần danh sách Course/Enrollment. | Catalog/API DD trả `UserProfile`; không có list projection hoặc empty collection shape. Không map profile thành danh sách khóa học. |
| #21 response/merge | AC-13 cần ghép Course + progress; AC-18 cần aggregate dashboard. | Catalog trả `UserProfile` không có progress fields; query, merge key, denominator/formula và empty behavior chưa có. Không tính phần trăm/summary. |
| AC-13 empty branch | Diagram ghi EMPTY và HAS DATA cùng đến một node hiển thị list + %. | Không thể quyết định empty-state target hoặc hoàn thành flow chỉ bằng sơ đồ hiện có. |
| #21/#38 order | Inventory ST-01/ST-20 gọi widget độc lập; AC-18 đặt #21 → #37 → #38. | `DISCREPANCY`; giữ #38 responsibility theo inventory nhưng không tự chọn timing/orchestration. |
| #38 claims | Mockup nói cần ký kiểm định hệ thống chấm điểm ST-22. | Achievement schema không có signature/certificate/proof/metrics; không có award criteria hoặc validator source. Không biểu thị claim như sự thật. |
| #43 “latest” | Widget title là “Thông báo mới nhất”. | API #43 khai báo Page và optional filters; sorting/default order chưa được duyệt. `read_at`, `channels`, `status` và recipient source có gaps. Không khẳng định latest/unread counts. |
| API URLs | Catalog là các `/users/me/...` paths ở bảng A.4. | HTML matrix dùng bốn path sai; đây là static mockup discrepancy, không phải API source. |
| Widgets/state/error | Inventory liệt kê partial/empty/loading/403; prototype hiển thị các card gate. | Không có loading/error UI, data binding hoặc failure handling runtime. Empty không được suy từ auth/API/network error. |
| Navigation | Inventory liên kết ST-08/ST-20/ST-26/ST-02. | 13 anchor trong HTML đều `href="#"`; không có Study router. `data-path` không phải route. Legal/help/discussion destinations chưa có contract ở màn hình này. |
| Design system | `.agents/web-study/design.md`: semantic ocean tokens, system/Inter không remote import, max content khoảng 1120px, accessible states/reflow. | Prototype tải Plus Jakarta Sans/Material Symbols và Tailwind CDN; config dùng primary `#004AC6`/`#2563EB`, `max-w-[1440px]`, đồng thời claim WCAG chưa được test. Cần alignment trước implementation. |

**Bảo mật:** actor theo AC là Student đăng nhập. Không nhận `user_id` từ query/UI; identity phải gắn với principal theo contract backend khi endpoint được triển khai. Current `/users/me` source không chứng minh các route #20/#21/#38/#43 đã có guard. Không render profile placeholder thành current user, không trả dữ liệu widget khi actor/session chưa được xác minh.

### A.6. Nguồn

- [Inventory](../../list_screen.md), [source screenshot](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/screen.png), [HTML companion](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/code.html), [plan](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_PLAN.md).
- [API catalog](../../../../../docs/lists/list_api.md), [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md), [AC diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio).
- API DD/open questions: [#20](../../../../study-server/docs/dd/20_users_me_courses), [#21](../../../../study-server/docs/dd/21_users_me_progress), [#38](../../../../study-server/docs/dd/38_users_me_achievements), [#43](../../../../study-server/docs/dd/43_users_me_notifications).
- [DB table guide](../../../../study-server/docs/diagrams/DB_UNICA_TABLES.md), [legacy DDL](../../../../../infra/postgres/study-server/DB.sql), [V1-PILOT DDL](../../../../../infra/postgres/02_study_db.sql).
- [Study Web design target](../../../../../.agents/web-study/design.md), [Study route inventory](../../../../../.agents/server-study/apis/declared-routes.md), [markers](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_markers.json), [overlay](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/ST-01_markers_overlay.svg), [annotated image](../../screen_stitch/03_student/ST-01_tong-quan-hoc-vien/screen_annotated.png).
