# ST-04 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-04-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-04-API-002` | #15 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08, #15
- Orchestration/data notes: GET #8 trước; #15 chỉ gọi khi BE chốt identity/selection; nếu miễn phí → #19, nếu trả phí → #16.
- BE/source status và gate: **#08 R; #15 D; DD BLOCKED**; **BLOCK:** #15 Public nhưng không xác định user; auth/free-paid/entitlement flow chưa chốt; Study Web UNWIRED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: D. Đặc tả sự kiện và API

Không có handler/event logic trong HTML. Các event dưới đây phân loại tương tác tĩnh và luồng AC dự kiến, đồng thời tách rõ phần có source thực thi và phần bị chặn. Không áp dụng retry, timeout, cache, debounce, idempotency key hoặc client transaction vì chưa có contract.

### EV-01 — Khởi tạo route và kiểm tra ngữ cảnh Student

- **Trigger / loại:** Page route load; không có marker click.
- **Element:** ST-04 route.
- **Input:** `courseId` raw từ route đề xuất; authenticated session/Student role theo precondition AC-12.
- **Tiền điều kiện:** Cần route được implement và identity/session contract có sẵn. Cả hai hiện chưa được xác minh trong Study Web.
- **Trình tự:** (1) Nhận nguyên chuỗi route param; không tự chuẩn hóa slug thành integer. (2) AC-12 yêu cầu Student đã đăng nhập; không có guard hiện hành để thực hiện redirect/403. (3) Nếu route được nối, chỉ chuyển `course_id` sau khi mapping được duyệt; nếu không xác định được input thì dừng và không gọi API. (4) HTML hiện tại không thực hiện bước nào trong luồng này.
- **Output/state:** Hiện chỉ render prototype tĩnh. Route state, auth failure view và luồng quay lại sau login chưa có contract.
- **Lỗi/ngoại lệ:** ID sai định dạng có thể bị #08 trả 404 nếu request tới được API; session hết hạn/role không hợp lệ và redirect target chưa được quyết định.

### EV-02 — Đọc course đã xuất bản bằng API #08

- **Trigger / loại:** Route đã có `course_id` hợp lệ; GET dữ liệu.
- **API contract:** `GET /api/v1/courses/{course_id}`; Public/no Bearer theo [`list_api.md`](../../../../../docs/lists/list_api.md); `course_id:int64!`; không query/body. API #08 có route trong [`v1.py`](../../../../study-server/app/api/v1.py) và handler [`view.py`](../../../../study-server/app/modules/guest/api_08_courses_detail/view.py).
- **Trình tự:** (1) Lấy raw path string. (2) Backend `validate_course_id` parse integer; nếu parse thất bại, trả 404. (3) Query chỉ tìm course có `status="PUBLISHED"`, hiện dùng `LEFT JOIN users` mentor. (4) Không tìm thấy hoặc chưa publish → 404; SQLAlchemy error → rollback rồi 500. (5) Map `id`, `title`, nullable `description`, nullable `thumbnail_url`, decimal-string `price`, `status`, `mentor{id,full_name,avatar_url?}`. Thiếu mentor ID/name hoặc giá invalid/missing làm mapping trả 500. (6) Thành công trả standard envelope `success=true`, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `data.items=[Course]`, `pagination={page:1,size:1,total:1,total_pages:1}`, `meta={}`, `traceId`. Category không có trong response. (7) UI mapping/price display chưa implement; không suy luận eligibility.
- **Response/error hiện hành:** 200 `DESIGN_RESOURCE_RETRIEVED`; 404 `DESIGN_RESOURCE_NOT_FOUND` cho ID sai hoặc course không tồn tại/không PUBLISHED; 500 `DESIGN_INTERNAL_ERROR` cho query/mapping error. Error envelope có `success=false`, `message`, `data=null`, `meta`, `traceId` theo `core/responses.py`.
- **DISCREPANCY:** API #08 Draft DD mô tả `INNER JOIN`; source SQL đang dùng `LEFT JOIN`, sau đó mapper coi mentor thiếu là lỗi 500. Current source được dùng để mô tả hiện trạng. Catalog #08 khai báo 404/500; route khai báo HTTP success default 200 và view trả JSONResponse status thực tế.
- **Side effects:** Read-only; không sửa enrollment/order.
- **Retry/cache:** Không có chính sách được xác nhận; không tự thêm.
- **Current UI behavior:** ST-04 không gọi #08 vì không có route/client.

### EV-03 — Kiểm tra enrollment bằng API #15 (BLOCKED)

- **Trigger / loại:** Sau khi #08 trả course thành công và contract danh tính được giải quyết; GET.
- **API contract trên giấy:** `GET /api/v1/courses/{course_id}/enrollment-status`; Public/no Bearer; path duy nhất `course_id:int64`; không query/body; success 200 `DESIGN_RESOURCE_RETRIEVED` với `ApiEnvelope<Enrollment>`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`.
- **Response shape Draft:** `Enrollment{id:int64,user_id:int64,course_id:int64,status:EnrollmentStatus,enrolled_at:date-time,completed_at:date-time|null}`. `status` enum chưa được xác nhận; đây là response Draft, không phải runtime.
- **Blocker:** Request không nêu Student hoặc selector; response có `user_id`; nhiều enrollment có thể trùng course. Chưa có source unique/selection rule. 404 không phân biệt course missing với enrollment missing. Không được gọi endpoint theo một lựa chọn suy đoán, không tự thêm auth/ID, không chọn active/latest.
- **Trình tự nếu/ khi contract được duyệt:** (1) chuẩn hóa `course_id` theo contract. (2) Backend phải resolve đúng identity/enrollment bằng rule được duyệt. (3) Parse success/error envelope và chỉ nhận branch/status được xác nhận. (4) Cập nhật state/UI theo state machine được product duyệt. Những bước này chưa có implementation nên chưa thể chốt mapping.
- **Current source:** Không tìm thấy #15 route/module/query/model/test trong Study Server; UI cũng không có caller. Không có output/error response thực tế.
- **Side effects/retry/cache:** Theo Draft API read-only, nhưng chưa có source; semantics retry/cache chưa được chốt.

### EV-04 — Điều hướng theo kết quả enrollment/payment (BLOCKED)

- **Trigger / loại:** Branch nội bộ sau kết quả #15 và policy được phê duyệt; không có control branch trong HTML.
- **Input:** Course #08 và kết quả enrollment #15; quyết định eligibility/giá/thanh toán từ backend theo contract còn thiếu.
- **Trình tự theo AC-12:** (1) Enrollment hiện hữu → nhánh Khóa học của tôi. (2) Chưa ghi danh và đủ điều kiện free theo rule server → POST #19. (3) Nhánh trả phí → ST-05 tạo order #16, ST-06 tạo payment #17; #18 operation status được biểu diễn không nối trong diagram, cần làm rõ thứ tự. (4) Client callback không chứng minh payment thành công. (5) Server xác minh entitlement/payment trước #19; sau đó #20 tải lại khóa học tới ST-08.
- **Output/errors:** UI state, route payload, error mapping, duplicate/conflict handling và retry policy chưa thể xác định. Inventory nêu các state `already-enrolled/free/paid`, nhưng API #15 identity blocker làm chúng không implementable hiện nay.
- **Current source:** #16–#20 chưa có route/module/query/model/test được tìm thấy trong Study Server; HTML không chứa các nhánh này. Không gọi API hoặc ghi nhận thành công enrollment.

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

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/03_student/ST-04_kiem-tra-ghi-danh-truoc-dang-ky/ST-04.md)
