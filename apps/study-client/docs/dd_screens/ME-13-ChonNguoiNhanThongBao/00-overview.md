# ME-13 — Chọn người nhận thông báo · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `ME-13` |
| Module | Mentor |
| Route | `/mentor/notifications/new/recipients` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **Screen ID:** ME-13 · **Loại:** bước trong flow tạo thông báo · **DD status:** DD BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [ME-13.md](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13.md), [ME-13_PLAN.md](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13_PLAN.md), [ME-13_markers.json](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/ME-13_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Chọn course và học viên được phép nhận, không tự lấy toàn bộ users.
- In-scope: GET #46 → GET #62 theo numeric course_id → giữ unique Student IDs int64 cho ME-14; handoff carrier chưa được duyệt.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-25 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Chọn course và học viên được phép nhận, không tự lấy toàn bộ users. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #46, #62
- Liên kết màn hình dự kiến: [ME-14](../ME-14-SoanThongBaoMentor/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/selected/denied |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [ME-13 source screen.png](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/04_mentor/ME-13_chon-nguoi-nhan-thong-bao/screen_annotated.png))
- Luồng: GET #46 → GET #62 theo numeric course_id → giữ unique Student IDs int64 cho ME-14; handoff carrier chưa được duyệt.
- Priority: P2; Gate/source status: **R**; #46/#62 route/module/query/model/test source-backed locally. **BLOCK:** prototype slugs không ánh xạ int64; #46 không có semester/assigned-course; course status eligibility; support_needed thiếu progress/attendance source; loaded roster/selection UI chưa có; #63 CSV recipient mapping vẫn Draft/DERIVED, không có course_id, content:int64 lệch text, privacy/email/WCAG claims chưa được xác nhận; live schema và Study Web UNWIRED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# ME-13 — Chọn người nhận thông báo

> **Screen ID:** ME-13 · **Loại:** bước trong flow tạo thông báo · **DD status:** DD BLOCKED · **Implementation:** BLOCKED · **Runtime:** NOT VERIFIED

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Mục tiêu, actor và ranh giới

ME-13 là bước đầu của flow tạo thông báo Mentor: chọn một course, tải roster hợp lệ, chọn scope/người nhận rồi chuyển recipient IDs sang ME-14. Actor được AC-25 xác định là Mentor. Prototype còn ghi quyền “Điều phối viên & Mentor phụ trách”, nhưng API #46/#62/#63 chỉ chấp nhận role MENTOR và #46/#62 hiện kiểm tra course do Mentor trực tiếp sở hữu; coordinator-only và assigned-Mentor access không được xác nhận.

Route /mentor/notifications/new/recipients là route đề xuất trong inventory. Study Web hiện UNWIRED, không có app source/package/router cho màn hình này. Không khẳng định route, component state, guard hay request nào đang chạy thực tế. Route sau là đề xuất /mentor/notifications/new (ME-14). Entry route trước ME-13, đích của Cancel và mọi destination của header/footer hiện chưa được xác nhận.

### Điều kiện, dữ liệu và trạng thái

- **Precondition kỳ vọng:** phiên đăng nhập có role Mentor; một course đủ điều kiện do Mentor quản lý; trước khi sang ME-14 phải có danh sách recipient IDs hợp lệ.
- **Input:** route/session identity của Mentor; danh sách course từ #46; course_id số nguyên int64; roster từ #62; lựa chọn scope và IDs đã chọn.
- **Output logic:** tập Student IDs int64 duy nhất cùng course context cho ME-14. Hình thức vận chuyển/persistence qua route chưa được chốt. Không đặt IDs trong URL, query, session storage hay local storage khi chưa có quyết định.
- **Trạng thái trong ảnh:** chưa chọn course, danh sách học viên rỗng, selected count 0, estimated count 0, scope “Tất cả học viên trong khóa” đang được chọn trực quan, Continue disabled. Đây là trạng thái của prototype.
- **Không có mutation API ở ME-13.** #46 và #62 là GET. API #63 thuộc ME-14; được truy vết ở đây chỉ để xác định ràng buộc handoff.

### Expected behavior và current behavior

| Chủ đề | Expected / prototype | Current source |
|---|---|---|
| Course | Học kỳ hiện tại, khóa có học viên đăng ký và Mentor được phân công | #46 chỉ trả course do Mentor trực tiếp sở hữu; status tùy chọn DRAFT/PUBLISHED; không có semester/enrollment/assignment fields. HTML options dùng slug như cs101; #62 cần course_id int64. |
| Roster | Chọn all, support-needed hoặc specific từ roster | #62 trả ACTIVE enrollments và Student summaries. Không có progress/checkpoint/attendance/support category. HTML hiện chỉ có empty-state, không có row/checkbox. |
| Privacy/channel | Badge nói chế độ ẩn danh, LMS và email trường liên kết | #62/#63 không thiết lập anonymity hoặc email liên kết. Channel gửi nằm ở body #63 nhưng ME-13 không có channel control. |
| Continue | Sang ME-14 sau khi chọn course | Ảnh và HTML đặt disabled; HTML không có handler. #63 từ chối danh sách recipients rỗng. |
| Runtime | Gọi APIs theo hành vi đã mô tả | API #46/#62/#63 có route/module/tests cục bộ; Study Web UNWIRED. Không có runtime screen evidence. |

### Quy tắc và bảo mật

1. Chỉ dùng course IDs và Student IDs do API trả về; không coi slug tĩnh trong HTML là IDs hợp lệ.
2. #62 xác minh quyền sở hữu trực tiếp của course và chỉ trả role STUDENT có enrollment ACTIVE. Backend xác minh lại nên client không phải nguồn quyết định quyền.
3. #46 trả page có phân trang; nếu tổng khóa vượt size của một page, chỉ hiển thị page đầu không bảo đảm đủ course. Kích thước/lấy hết trang phải theo approved client pattern; giới hạn API hiện là size 1..100.
4. Course status eligibility chưa được chốt. #46 có thể trả DRAFT và PUBLISHED; #62 không kiểm tra trạng thái course.
5. Scope all phải materialize thành các Student IDs cụ thể. Scope specific cần danh sách IDs người dùng chọn. Scope support-needed chưa triển khai/được định nghĩa bởi #62.
6. #63 kiểm tra recipients theo một ACTIVE roster chung thuộc bất kỳ course nào do Mentor trực tiếp sở hữu, vì body không có course_id. Điều này không ràng buộc recipients với đúng course ME-13 đang hiển thị; cần xác nhận hoặc sửa contract ở phạm vi API trước khi triển khai.
7. API IDs là int64. Nếu client dùng JavaScript number, giá trị lớn hơn Number.MAX_SAFE_INTEGER có thể mất chính xác. Client cần chuẩn hóa chiến lược giữ int64 an toàn và CSV serialize sau khi contract được duyệt.
8. Không ghi dữ liệu recipient vào URL/logs. Cơ chế lưu/chuyển tạm thời phải theo quyết định bảo mật và router state của Study Web.

### API dependency trace

**API #46 — GET /api/v1/mentor/courses**

- Route tại [v1.py](../../../../study-server/app/api/v1.py#L777); view/query/validator tại [api_46_mentor_courses](../../../../study-server/app/modules/mentor/api_46_mentor_courses).
- Authorization: Bearer token, role MENTOR, lấy numeric mentor identity trước query. Owner predicate là c.id thuộc mentor_id xác thực.
- Query: status tùy chọn, chỉ DRAFT/PUBLISHED; page mặc định từ shared DEFAULT_PAGE, phải ≥1; size từ DEFAULT_SIZE, 1..100.
- Order: created_at DESC, id ASC. Response success envelope DESIGN_RESOURCE_RETRIEVED, data CoursePage gồm items và pagination {page,size,total,total_pages}; không có course thì 200 với items rỗng. Chỉ map fields có trong Course model; ME-13 cần tối thiểu id và title.
- Lỗi: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 422 DESIGN_VALIDATION_ERROR cho query sai, 500 DESIGN_INTERNAL_ERROR khi query/mapping thất bại. Không có semester filter hay assignment relation.
- Local API test: [test_mentor_courses.py](../../../../study-server/tests/modules/mentor/api_46_mentor_courses/test_mentor_courses.py). Test source có sẵn nhưng không chạy trong phiên DD này; fake DB không chứng minh live schema.

**API #62 — GET /api/v1/mentor/courses/{course_id}/students**

- Route tại [v1.py](../../../../study-server/app/api/v1.py#L1268); view/query/model tại [api_62_mentor_course_students](../../../../study-server/app/modules/mentor/api_62_mentor_course_students).
- Authorization: Bearer token, role MENTOR. course_id là path int64; source parse ID sau auth. Sai format/range hoặc không tồn tại trả 404 DESIGN_RESOURCE_NOT_FOUND; course không thuộc Mentor trực tiếp trả 403 DESIGN_ACCESS_DENIED.
- Query joins course/enrollment/user, filters e.status=ACTIVE and u.role=STUDENT, selects distinct Student and orders u.id ASC. Không lọc account status và không kiểm tra course status.
- Success: HTTP 200, DESIGN_RESOURCE_RETRIEVED, data array [{id:int64,full_name:string,avatar_url?:string}], meta {}. Empty roster là 200 với data:[].
- Lỗi khác: 401 DESIGN_AUTHENTICATION_REQUIRED; 500 DESIGN_INTERNAL_ERROR khi DB/projection lỗi. Không pagination, email, course display label, progress, checkpoint, due date hoặc attendance.
- Local API test: [test_mentor_course_students.py](../../../../study-server/tests/modules/mentor/api_62_mentor_course_students/test_mentor_course_students.py). Không chạy trong phiên này.

**API #63 — POST /api/v1/mentor/notifications (downstream ME-14, not called by ME-13)**

- Route/view/model/validator/query tại [api_63_mentor_notifications_create](../../../../study-server/app/modules/mentor/api_63_mentor_notifications_create); API DD [03_Request.md](../../../../study-server/docs/dd/63_mentor_notifications_create/03_Request.md) còn Draft — Needs Confirmation; [OPEN_QUESTIONS.md](../../../../study-server/docs/dd/63_mentor_notifications_create/OPEN_QUESTIONS.md) ghi recipient mapping còn mở.
- Request hiện tại là JSON strict, extra fields bị từ chối: recipients:string (CSV positive int64 Student IDs), title:string tối đa 200, content:signed int64, channels:string (CSV PUSH/EMAIL). Mọi field required. recipients/channel CSV parse trim tokens và collapse duplicate theo lần đầu; blank/malformed/empty list là 422 DESIGN_VALIDATION_ERROR. Screenshot free-form content chưa tương thích content:int64.
- Server xác thực Mentor, rồi xác minh toàn bộ recipients là Student có enrollment ACTIVE trong ít nhất một common course do Mentor trực tiếp sở hữu. Không có course_id, scope enum, anonymity flag hay email preference field. Recipient mismatch trả 403 DESIGN_ACCESS_DENIED.
- Khi hợp lệ, source tạo một legacy notification row mỗi recipient và một QUEUED delivery-outbox row mỗi channel trong transaction; chỉ sau commit mới trả 202 DESIGN_OPERATION_ACCEPTED. data là Operation {id:UUID,kind:NOTIFICATION_DISPATCH,status:QUEUED,owner_id:int64,submitted_at,updated_at}; meta.notification_ids:int64[] giữ ID thông báo riêng. 202 không chứng minh worker/provider đã gửi.
- Các lỗi còn lại: 401 DESIGN_AUTHENTICATION_REQUIRED, 422 DESIGN_VALIDATION_ERROR, 503 DESIGN_DEPENDENCY_UNAVAILABLE cho DB unavailable, 500 DESIGN_INTERNAL_ERROR. Không có idempotency key; retry sau timeout có thể tạo batch trùng. Không dùng operation UUID thay notification_id; API #18 và #64 là handoff sau, thuộc ME-15.
- API #63 local tests nằm tại [test_mentor_notifications_create.py](../../../../study-server/tests/modules/mentor/api_63_mentor_notifications_create/test_mentor_notifications_create.py). DD này không chạy tests; local tests/fallback schema không xác minh live DB/deployment/worker.

### Traceability references

- Danh mục/route/state/API dependencies: [list_screen.md](../../list_screen.md), ME-13 và flow F10.
- Activity diagram AC-25: [AC_03_MENTOR_TEACHING.drawio](../../../../study-server/docs/diagrams/AC_UNICA/AC_03_MENTOR_TEACHING.drawio), page AC-25.
- Study Web status: .agents/web-study/AGENTS.md and INDEX.md mark the app UNWIRED; design guidance is .agents/web-study/design.md.
- Scope routing and prior docs decisions: [.agents/worklog/2026-11-06/design-study-screen-me13.md](../../../../../.agents/worklog/2026-11-06/design-study-screen-me13.md).
