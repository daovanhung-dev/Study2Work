# ST-04 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-04-EV-001` | `Source heading` / EV-01 — Khởi tạo route và kiểm tra ngữ cảnh Student | See source event detail below |
| `ST-04-EV-002` | `Source heading` / EV-02 — Đọc course đã xuất bản bằng API #08 | See source event detail below |
| `ST-04-EV-003` | `Source heading` / EV-03 — Kiểm tra enrollment bằng API #15 (BLOCKED) | See source event detail below |
| `ST-04-EV-004` | `Source heading` / EV-04 — Điều hướng theo kết quả enrollment/payment (BLOCKED) | See source event detail below |
| `ST-04-EV-005` | `Source heading` / EV-05 — Quay lại danh sách khóa học | See source event detail below |
| `ST-04-EV-006` | `Source heading` / EV-06 — Điều hướng header, breadcrumb và footer | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện và API

Không có handler/event logic trong HTML. Các event dưới đây phân loại tương tác tĩnh và luồng AC dự kiến, đồng thời tách rõ phần có source thực thi và phần bị chặn. Không áp dụng retry, timeout, cache, debounce, idempotency key hoặc client transaction vì chưa có contract.

### EV-01 — Khởi tạo route và kiểm tra ngữ cảnh Student

- **Trigger / loại:** Page route load; không có marker click.
- **Element:** ST-04 route.
- **Input:** `courseId` raw từ route đề xuất; authenticated session/Student role theo precondition AC-12.
- **Tiền điều kiện:** Route hiện được đăng ký tại `/student/enroll/:courseId`; Student session/guard và identity contract chưa có trong Study Web.
- **Trình tự:** (1) Nhận nguyên chuỗi route param, giữ path string khi gọi #08 theo pattern hiện có của GS-03. (2) Không tự chuẩn hóa slug thành integer; #08 hiện parse `course_id` và trả 404 nếu không hợp lệ. (3) AC-12 yêu cầu Student đã đăng nhập; route hiện chưa guard. (4) HTML prototype vẫn không thực hiện các bước này.
- **Output/state:** Page có loading/course-not-found/course-error/enrollment-gate state từ #08; auth failure view và luồng quay lại sau login chưa có contract.
- **Lỗi/ngoại lệ:** ID sai định dạng có thể bị #08 trả 404 nếu request tới được API; session hết hạn/role không hợp lệ và redirect target chưa được quyết định.

### EV-02 — Đọc course đã xuất bản bằng API #08

- **Trigger / loại:** Route đã có `course_id` hợp lệ; GET dữ liệu.
- **API contract:** `GET /api/v1/courses/{course_id}`; Public/no Bearer theo [`list_api.md`](../../../../../docs/lists/list_api.md); `course_id:int64!`; không query/body. API #08 có route trong [`v1.py`](../../../../study-server/app/api/v1.py) và handler [`view.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/view.py).
- **Trình tự:** (1) Route page passes the raw path string to `GS03CourseDetailService`, which sends GET #08 with no Authorization. (2) Backend `validate_course_id` parses integer; invalid input returns 404. (3) Query only finds `status="PUBLISHED"`, currently using `LEFT JOIN users` for mentor. (4) Missing/unpublished course → 404; SQLAlchemy error → rollback then 500. (5) Success returns `data.items=[Course]` and singleton pagination. (6) Study Web maps a successful PUBLISHED course to the enrollment gate, a 404 to not-found and other HTTP/envelope errors to a generic error. It does not render price or infer eligibility.
- **Response/error hiện hành:** 200 `DESIGN_RESOURCE_RETRIEVED`; 404 `DESIGN_RESOURCE_NOT_FOUND` cho ID sai hoặc course không tồn tại/không PUBLISHED; 500 `DESIGN_INTERNAL_ERROR` cho query/mapping error. Error envelope có `success=false`, `message`, `data=null`, `meta`, `traceId` theo `core/responses.py`.
- **DISCREPANCY:** API #08 Draft DD mô tả `INNER JOIN`; source SQL đang dùng `LEFT JOIN`, sau đó mapper coi mentor thiếu là lỗi 500. Current source được dùng để mô tả hiện trạng. Catalog #08 khai báo 404/500; route khai báo HTTP success default 200 và view trả JSONResponse status thực tế.
- **Side effects:** Read-only; không sửa enrollment/order.
- **Retry/cache:** Không có chính sách được xác nhận; không tự thêm.
- **Current UI behavior:** ST-04 calls #08 after route activation; focused tests verify the public GET, gate and 404 path. The response price is not rendered.

### EV-03 — Kiểm tra enrollment bằng API #15 (BLOCKED)

- **Trigger / loại:** Sau khi #08 trả course thành công và contract danh tính được giải quyết; GET.
- **Contract trên giấy:** `GET /api/v1/courses/{course_id}/enrollment-status`; Public/no Bearer; path duy nhất `course_id:int64`; success 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Enrollment>`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- **Response shape Draft:** `Enrollment{id:int64,user_id:int64,course_id:int64,status:EnrollmentStatus,enrolled_at:date-time,completed_at:date-time|null}`. `status` enum chưa được xác nhận; đây là response Draft, không phải runtime.
- **Blocker:** Request không nêu Student hoặc selector; response có `user_id`; nhiều enrollment có thể trùng course. Chưa có source unique/selection rule. 404 không phân biệt course missing với enrollment missing. Không được gọi endpoint theo một lựa chọn suy đoán, không tự thêm auth/ID, không chọn active/latest.
- **Trình tự nếu/ khi contract được duyệt:** (1) chuẩn hóa `course_id` theo contract. (2) Backend phải resolve đúng identity/enrollment bằng rule được duyệt. (3) Parse success/error envelope và chỉ nhận branch/status được xác nhận. (4) Cập nhật state/UI theo state machine được product duyệt. Những bước này chưa có implementation nên chưa thể chốt mapping.
- **Current source:** Study Server now has route/module/query/model/test for #15. The handler resolves a valid Student Bearer token when supplied; without a token, or when token validation fails, it selects any enrollment for the course (`ORDER BY e.id DESC LIMIT 1`). The response includes `user_id`. Client descriptor remains `UNWIRED`, and ST-04 sends no #15 request. This is a source/DD/security discrepancy, not an approved identity selection contract. Tests use fake sessions and do not establish live DB safety.
- **Side effects/retry/cache:** Theo Draft API read-only, nhưng chưa có source; semantics retry/cache chưa được chốt.

### EV-04 — Điều hướng theo kết quả enrollment/payment (BLOCKED)

- **Trigger / loại:** Branch nội bộ sau kết quả #15 và policy được phê duyệt; không có control branch trong HTML.
- **Input:** Course #08 và kết quả enrollment #15; quyết định eligibility/giá/thanh toán từ backend theo contract còn thiếu.
- **Trình tự theo AC-12:** (1) Enrollment hiện hữu → nhánh Khóa học của tôi. (2) Chưa ghi danh và đủ điều kiện free theo rule server → POST #19. (3) Nhánh trả phí → ST-05 tạo order #16, ST-06 tạo payment #17; #18 operation status được biểu diễn không nối trong diagram, cần làm rõ thứ tự. (4) Client callback không chứng minh payment thành công. (5) Server xác minh entitlement/payment trước #19; sau đó #20 tải lại khóa học tới ST-08.
- **Output/errors:** UI state, route payload, error mapping, duplicate/conflict handling và retry policy chưa thể xác định. Inventory nêu các state `already-enrolled/free/paid`, nhưng API #15 identity blocker làm chúng không implementable hiện nay.
- **Current source:** Study Server now exposes routes for #16–#20, but the client descriptors remain `UNWIRED` and their screen contracts still have unresolved order, payment, identity and entitlement rules. ST-04 does not call them or record enrollment success.

### EV-05 — Quay lại danh sách khóa học

- **Trigger / loại:** Click link/button-like anchor #11.
- **Input:** Không có user input; static href `/courses`.
- **Trình tự:** (1) Browser/client nhận anchor activation. (2) Điều hướng theo `/courses` nếu route tồn tại. (3) Không có course ID, tab, filter hay return URL được truyền. (4) Không có API call hay mutation.
- **Output/lỗi:** Rời prototype tới URL `/courses`; route runtime, giữ trạng thái danh sách và fallback khi route thiếu chưa xác minh. Network/API error không áp dụng cho anchor này.

### EV-06 — Điều hướng header, breadcrumb và footer

- **Trigger / loại:** Click anchor #1–#5, #12–#13; click navigation.
- **Input:** Các href tĩnh trong HTML: `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`. Breadcrumb current label là text, không clickable.
- **Trình tự:** (1) Nhận link đích từ anchor. (2) Browser/client thực hiện điều hướng nếu route tồn tại. (3) Không có auth-aware route selection, API, mutation, ID/filter/session state truyền qua trong markup. (4) Header primary nav bị ẩn dưới breakpoint `md`, không có menu thay thế được thấy trong HTML.
- **Output/lỗi:** Mở path tương ứng nếu có route; Study Web route availability chưa được xác minh. Link Student không chứng minh người dùng đã được xác thực; link đăng nhập/đăng ký vẫn hiện trong prototype.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
