# ME-16 — Tiến độ toàn khóa học · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-16` |
| Module | Mentor |
| Route | `/mentor/courses/:courseId/progress` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: Source status is described in the source DD. |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-16.md](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16.md), [ME-16_PLAN.md](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16_PLAN.md), [ME-16_markers.json](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/ME-16_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Bảng roster progress; filter/support categories chưa có contract.
- In-scope: #65 local source trả derived student progress page nhưng catalog còn Page<Course>; numeric course_id cần mapping; chỉ handoff student_id sang ME-17/#67 khi có row; #66 thuộc ME-18, AC-26 ordering khác inventory.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-26 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Bảng roster progress; filter/support categories chưa có contract. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #65
- Liên kết màn hình dự kiến: [ME-17](../ME-17-TienDoTungHocVien/00-overview.md), [ME-18](../ME-18-AnalyticsKhoaHoc/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/denied |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-16 source screen.png](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-16_tien-do-toan-khoa-hoc/screen_annotated.png))
- Luồng: #65 local source trả derived student progress page nhưng catalog còn Page<Course>; numeric course_id cần mapping; chỉ handoff student_id sang ME-17/#67 khi có row; #66 thuộc ME-18, AC-26 ordering khác inventory.
- Priority: P2; Gate/source status: **R**; #65 route/module/query/model/focused tests có local source. **DD READY; IMPLEMENTATION BLOCKED:** API DD Draft/DERIVED, response/catalog mismatch, slug→int64, roster bound, filter/search/reminder data, AC-26 ordering, live schema và Study Web UNWIRED; RUNTIME NOT VERIFIED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-16 — Tiến độ toàn khóa học

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

| Thuộc tính | Đặc tả |
|---|---|
| Screen ID / tên | ME-16 — Tiến độ toàn khóa học |
| Mục tiêu danh mục | Cho Mentor xem tiến độ học viên trong một course và mở chi tiết học viên; danh mục cũng liên kết ME-18 analytics. |
| Actor | Mentor. Local API #65 yêu cầu Bearer token có role `MENTOR`; đây chưa phải bằng chứng Study Web có auth guard. |
| Route dự kiến | `/mentor/courses/:courseId/progress` theo `list_screen.md`; app/router Study Web hiện `UNWIRED`. `courseId` cần mapping sang int64 để gọi API. |
| Điều kiện vào | Danh mục kỳ vọng Mentor đã xác thực và có course context. Local #65 kiểm tra course tồn tại và direct owner `courses.mentor_id`. Quy tắc assigned-course chưa được xác nhận. |
| Điều kiện ra | Candidate sang ME-17 với `course_id:int64` và `student_id:int64` qua API #67; candidate sang ME-18 với course ID qua #66. Cả hai link và handoff chưa wired trong prototype. |
| API liên quan | #65 roster progress; #67 student detail ở ME-17; #66 analytics thuộc ME-18. API #46 có course list numeric ID nhưng không có slug mapping cho selector prototype. |
| Trạng thái tài liệu | **DD READY** — source-backed behavior, prototype và blocker được tách biệt. |
| Trạng thái triển khai | **IMPLEMENTATION BLOCKED** — các contract, định danh course, dữ liệu filter và luồng AC-26 chưa được xác nhận; Study Web `UNWIRED`. |
| Trạng thái chạy thật | **RUNTIME NOT VERIFIED** — không có Study Web runtime/deployment/live schema verification trong phiên này. |

### Nguồn và độ tin cậy

| Nguồn | Nội dung dùng trong đặc tả | Mức bằng chứng |
|---|---|---|
| [Danh mục màn hình](../../list_screen.md) | Tên, route dự kiến, AC-26, #65, link ME-17/ME-18 và states kỳ vọng | Expected behavior |
| [Kế hoạch DD màn hình](../../screen_stitch/dd_screens/PLAN.md) | Blocker catalog `Page<Course>` của #65 | Expected behavior / tracker |
| [AC-26 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio) | API sequence, roles, inputs, response catalog và error set | Expected behavior; có discrepancy với screen inventory |
| [API catalog](../../../../../docs/lists/list_api.md) | #65–#67 method/path/request/response được khai báo | Expected behavior; catalog chưa khớp local response |
| [API #65 route](../../../../study-server/app/api/v1.py) và [module](../../../../study-server/app/modules/mentor/api_65_mentor_course_progress/view.py) | Local route, auth, owner check, SQL result, response/error behavior | Current source, chưa xác nhận deployment/live schema |
| [API #65 model](../../../../study-server/app/modules/mentor/api_65_mentor_course_progress/models.py) và [query](../../../../study-server/app/modules/mentor/api_65_mentor_course_progress/query.py) | Local response fields, roster eligibility, lesson/progress selection and formula | Current source; local assumptions là DERIVED trong API DD |
| [API #65 DD](../../../../study-server/docs/dd/65_mentor_course_progress/02_Overview.md) | Draft status, contract questions, derived behavior | Current documentation; needs confirmation |
| [API #65 focused tests](../../../../study-server/tests/modules/mentor/api_65_mentor_course_progress/test_mentor_course_progress.py) | Test cases được khai báo cho local implementation | Test source inspected; tests không chạy trong phiên này |
| `code.html`, `screen.png` | Static visual and controls | Prototype only, not runtime |

### Discrepancies và blockers

1. **API response:** AC-26/catalog khai báo `ApiEnvelope<Page<Course>>`; local #65 trả `ApiEnvelope<MentorStudentProgressPage>`. Không coi response local là contract đã duyệt và không map course fields sang roster progress.
2. **AC-26 ordering:** diagram đi `#65 → aggregate enrollment/progress → #66 → aggregate learning events → chọn Student → #67`; `list_screen.md` tách ME-16/#65 → ME-17/#67 và ME-18/#66. Chờ flow owner xác nhận vị trí analytics.
3. **Course identity:** route/#65 nhận signed int64; prototype selector có slug `cs-frontend-2025`, `fs-backend-nodejs`, `ai-ml-pipeline`. Không có mapping; hiện chưa thể gọi #65 an toàn từ selector.
4. **Data availability:** local #65 không trả email, last activity, submissions, attendance, due date, course name/code, enrollment timestamp, reminder/risk category, update time hoặc sync state.
5. **Filtering/search:** #65 không nhận filter/search; category thresholds và server/client query contract chưa có.
6. **Roster bound:** local #65 trả toàn bộ roster trong một trang, không request pagination; giới hạn an toàn và hành vi roster lớn chưa được chốt.
7. **Source/schema:** API #65 DD còn Draft/Needs Confirmation; local SQL dùng legacy BIGINT schema, khác V1-PILOT UUID/versioned schema; live DB/deployment chưa verified.
8. **Web app:** prototype anchors/controls chưa wired; Study Web không có route, client hay runtime để xác minh.
9. **Visual claims:** class code, số `0`, “Vừa xong”, “đồng bộ trực tiếp”, “Mỗi 15 phút”, cohort diagnosis, SCORM/xAPI, WCAG, nộp bài và chuyên cần đều là static copy/data; không coi là runtime facts.
