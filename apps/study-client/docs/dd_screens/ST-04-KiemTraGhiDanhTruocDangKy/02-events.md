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
- **Current UI behavior:** ST-04 calls public #08, then Student-authenticated #15; it renders course title/price and loading, not-found, login-required and error states. Existing focused tests still assert the former gate-only behavior; they were not run or updated in this task.

### EV-03 — Kiểm tra enrollment bằng API #15

- **Trigger / loại:** Sau khi #08 trả Course `PUBLISHED`; GET với Student Bearer.
- **Contract trên giấy:** `GET /api/v1/courses/{course_id}/enrollment-status`; Public/no Bearer; path duy nhất `course_id:int64`; success 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Enrollment>`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- **Response shape:** `Enrollment{id:int64,user_id:int64,course_id:int64,status:string,enrolled_at:date-time,completed_at:date-time|null}` from current source.
- **Current source:** Route/module/query/model exist. Validation requires Student identity; missing or invalid identity returns generic 404. Query selects only the caller's latest row (`ORDER BY e.id DESC LIMIT 1`); the course-wide fallback was removed. The response contains `user_id`. Client descriptor #15 is `WIRED`, and ST-04 calls through `StudentApiService`.
- **DISCREPANCY:** The API catalog still declares Public/no-Bearer, while AC-12 and this screen need a Student-specific Enrollment. After #08 has confirmed the course, ST-04 interprets #15 404 as no enrollment row for that Student. Latest-per-user selection is current source behavior; uniqueness of `(user_id, course_id)` is not established.
- **Mapping:** `ACTIVE` enters the already-enrolled branch; non-ACTIVE rows follow API #19's current eligibility behavior.
- **Side effects/retry/cache:** Read-only; no retry/cache was added.

### EV-04 — Điều hướng theo kết quả enrollment/payment

- **Trigger / loại:** Branch sau #15; free-enrollment mutation chỉ chạy sau CTA của Student.
- **Input:** Course #08 `PUBLISHED`, enrollment #15 của JWT Student, `courseId` an toàn và price từ #08.
- **Trình tự hiện hành:** (1) `ACTIVE` → mở `/student/courses`. (2) #15 404 sau #08 thành công → giá `0` hiện CTA miễn phí; giá dương điều hướng ST-05. Giá âm/không hợp lệ dừng ở error. (3) CTA miễn phí POST #19 với path/body `course_id`; user lấy từ JWT, server chỉ yêu cầu paid Order khi course price lớn hơn 0. (4) #19 thành công → GET #20 trang 1; chỉ mở ST-08 khi danh sách có đúng `course_id`. (5) #19 HTTP 409 cũng chỉ GET #20 để đối chiếu race; không gửi lại POST. (6) Paid branch chờ ST-05/#16 và ST-06/#17; browser return/callback không chứng minh payment.
- **Output/errors:** 401/403 → yêu cầu đăng nhập; #08 404 → not-found; #19 conflict được đối chiếu qua #20. Nếu #19 thành công nhưng #20 lỗi, retry chỉ GET #20 và không gửi lại #19.
- **Current source:** ST-04 gọi #08/#15/#19/#20; client descriptors #15/#19 là WIRED. DB/browser runtime chưa được kiểm tra. Paid branch phụ thuộc ST-05/#16 và ST-06/#17, vẫn còn trong implementation.

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
