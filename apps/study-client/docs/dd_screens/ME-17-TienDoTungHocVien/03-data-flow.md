# ME-17 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### B1. Expected flow theo inventory

1. Mentor mở ME-17 từ một student row của ME-16. Cần mang theo course_id và student_id dạng int64. Route hiển thị trong inventory mới là đề xuất.
2. Xác thực session/role phía ứng dụng rồi khởi tạo loading. Client route/auth hiện không tồn tại để xác minh; chỉ server API #67 có Bearer/JWT guard với role MENTOR.
3. Sau khi ID carrier và response contract được duyệt, gọi GET #67 đúng một lần cho hai path ID. Không có query hoặc request body trong catalog/local route.
4. Với approved response, ánh xạ trường có contract lên trang. Hiện chưa thể xác định loaded timeline row, trạng thái “bài còn thiếu”, course name, assignment/quiz metrics hay các thẻ mô tả.
5. Nếu approved response có lessons rỗng, phân biệt empty curriculum với lỗi tải dữ liệu; không tự gắn nghĩa “chưa đồng bộ lịch sử” cho trường hợp đó.
6. Mentor có thể dùng nút refresh và quay lại ME-16 theo thiết kế. HTML hiện không điều hướng về màn hình thật và refresh không tải dữ liệu.
7. Khi không xác thực, không có quyền, không tìm thấy course/student, lỗi server hoặc mất mạng, cần UX/error policy được duyệt. Chưa có client mapping, retry hay session-expiry behavior.

### B2. Current API #67 source flow

1. GET route nhận raw course_id, student_id và Authorization header. OpenAPI khai báo hai path parameter bắt buộc signed int64; không có query/body/page-size.
2. Shared Bearer/JWT guard yêu cầu role MENTOR trước DB.
3. Validator parse cả hai ID thành signed int64. Giá trị malformed hoặc ngoài range trả 404 DESIGN_RESOURCE_NOT_FOUND.
4. Query kiểm course trước. Course không tồn tại trả 404; course không thuộc direct owner trả 403 DESIGN_ACCESS_DENIED.
5. Student phải có users.role=STUDENT và ACTIVE enrollment trong course; nếu không thì 404 DESIGN_RESOURCE_NOT_FOUND.
6. Query lấy lesson PUBLISHED theo sort_order ASC, id ASC. Khi có duplicate progress rows cho cùng user/lesson, giữ row có last_accessed_at DESC NULLS LAST, tie-break id DESC.
7. Lesson không có row progress được chiếu thành NOT_STARTED, percent 0, timestamps null. Model/view chấp nhận progress_status NOT_STARTED, IN_PROGRESS hoặc COMPLETED. Summary gồm completed_lesson count, số PUBLISHED lessons và floor(sum(progress_percent)/total lessons); mẫu số 0 cho percent 0.
8. Success source trả ApiEnvelope<StudentCourseProgress> với course_id; student{id,full_name,avatar_url}; summary{completed_lessons,total_lessons,progress_percent}; lessons[]{lesson_id,title,order,progress_status,progress_percent,last_accessed_at,completed_at}. Không có pagination hoặc DB write.
9. Local errors: 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 404 DESIGN_RESOURCE_NOT_FOUND, 500 DESIGN_INTERNAL_ERROR. Error body dùng envelope an toàn/data null theo local source.
10. Đọc test source cho thấy fake DB cases cho auth, IDs, owner/roster, empty curriculum, projection/error/OpenAPI/trace; test chưa chạy. Đây không phải bằng chứng live DB/deployment.

### B3. Current prototype flow

- screen.png/HTML hiển thị một empty timeline và các giá trị tĩnh. HTML có 12 anchor dùng href="#", một nút refresh và không có form, table, lesson row, route binding, API request, fetch, polling hay cache.
- Nút refresh chỉ thêm hiệu ứng quay icon, disable nút, chờ 600 ms rồi khôi phục. Không có network request hoặc data update.
- “Đang đồng bộ hồ sơ…” là literal heading của prototype; không phản ánh API loading state được nối.
- Header/footer, breadcrumb/back anchors không có destination runtime. Phần profile và ba tile là static content, không có click handler.

### Trích từ DD nguồn: E. Ma trận trạng thái và điều hướng

### E1. Trạng thái

| State | Điều kiện / evidence | Nội dung và chuyển tiếp |
|---|---|---|
| Prototype static-empty | Trạng thái đang thể hiện trong screenshot; HTML literal, không có data binding | Hiển thị card profile/tile/empty timeline như asset. Không chứng minh API loading hay runtime. |
| Loading (expected candidate) | Inventory nêu loading; có thể khởi tạo sau khi route/auth/IDs được duyệt | Chưa có client implementation. Không dùng literal “Đang đồng bộ hồ sơ…” làm API loading indicator nếu chưa được duyệt. |
| Ready (candidate) | Chỉ sau 200 với success shape và loaded presentation được chốt | Local API có summary/lesson snapshot; mapping tới page và timeline rows chưa được phê duyệt. |
| Empty curriculum (source condition) | Local response thành công nhưng lessons rỗng khi không có PUBLISHED lesson | Summary progress percent là 0; không đồng nghĩa lịch sử chưa sync hoặc học viên chưa làm hoạt động. UX cần xác nhận. |
| Denied (candidate) | Inventory state; local 401 authentication hoặc 403 direct owner mismatch | UX, re-auth và privacy copy chưa được định nghĩa. |
| Not found (candidate) | Inventory state; local 404 malformed ID, course không tồn tại hoặc Student không eligible | Giữ source error code; không phân biệt nguyên nhân trên UI nếu policy chưa duyệt. |
| System/network error (candidate) | Local 500 hoặc transport failure | Inventory chưa mô tả đầy đủ UX; copy/retry/timeout chưa có contract. |
| Refresh animation | EV-02 handler đang chạy | Nút disabled, icon quay; tối đa 600 ms; không có API/data transition. |

### E2. Điều hướng và dữ liệu handoff

| From / action | Destination | Dữ liệu cần truyền | Hiện trạng |
|---|---|---|---|
| ME-16 student row | ME-17 | Numeric course_id + student_id | Inventory dependency; ME-16 carrier/source mapping chưa được wire hoặc phê duyệt. |
| ME-17 back button | ME-16 | Cùng course_id, giữ auth session theo policy | Anchor href="#"; destination chưa hoạt động. |
| Header/breadcrumb/footer links | Không xác định | Không có | Placeholder href="#"; không giả định route. |
| ME-17 analytics | Không mở từ screen này theo source asset | ME-18/#66 thuộc flow riêng trong inventory | AC-26 diagram sequencing khác inventory; cần flow owner quyết định. |
| Lesson/assignment/quiz detail | Không xác định | #67 lesson_id có trong local source nhưng không có row action/design | Không có click target; không tạo route. |

### E3. Authorization, privacy, session

- Server local #67 authenticates Bearer/JWT và requires MENTOR trước DB. Điều này không xác nhận Study Web session guard.
- Local course access là direct-owner check; assigned Mentor semantics chưa được chứng minh. ACTIVE enrollment + STUDENT role là eligibility của current code, chưa được duyệt thành business rule.
- Source phân biệt 403 course owner mismatch và 404 missing/ineligible; client display/masking policy chưa có.
- 401 behavior sau expiry, login redirect, return URL, logout, denied screen và back navigation chưa được wire hoặc đặc tả.
- IDs phải được giữ theo contract int64; không đưa names, avatar, email hoặc course data vào URL.

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Chỉ gọi #67 với course_id + student_id numeric sau khi ME-16 handoff được chốt; không gộp #65/#66. Catalog ApiEnvelope<Page<Course>> khác local ApiEnvelope<StudentCourseProgress>; AC-26 đặt #66 trước chọn Student/#67, khác inventory; loaded timeline và mockup metrics chưa có field mapping.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [ME-17](../../screen_stitch/04_mentor/ME-17_tien-do-tung-hoc-vien/ME-17.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
