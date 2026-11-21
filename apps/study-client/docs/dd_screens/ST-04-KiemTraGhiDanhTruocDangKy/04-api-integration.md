# ST-04 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `ST-04-API-001` | #08 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `ST-04-API-002` | #15 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #08, #15
- Orchestration/data notes: #08 revalidates a published course; Student Bearer #15 resolves the caller's latest enrollment; an `ACTIVE` enrollment opens ST-08, a missing enrollment branches by course price, and paid courses hand off to ST-05. The explicit free action calls #19, then #20 confirms the course before navigation.
- BE/source status: **#08/#15/#19/#20 have Study Server routes and current client callers.** API #15 returns only the authenticated Student's latest enrollment and has no course-wide fallback. **DISCREPANCY:** `list_api.md` still declares #15 Public/no-Bearer, while AC-12 and the current caller require the Student identity. Live database/browser runtime remains unverified.
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
- **Current UI behavior:** ST-04 calls public #08, then Student-authenticated #15; it renders course title/price and loading, not-found, login-required and error states. Existing focused tests assert the former gate-only behavior; they were not run or updated.

### EV-03 — Kiểm tra enrollment bằng API #15

- **Trigger:** Sau khi #08 trả course `PUBLISHED`; GET với Student Bearer.
- **Catalog contract:** `GET /api/v1/courses/{course_id}/enrollment-status`; Public/no Bearer; path `course_id:int64`; response/error declarations remain as in `list_api.md`.
- **Current source:** Validation requires Student identity; missing/invalid identity returns generic 404. Query selects only that user's latest enrollment (`ORDER BY e.id DESC LIMIT 1`); course-wide fallback is removed. Client descriptor #15 is `WIRED`, and ST-04 calls through `StudentApiService`.
- **DISCREPANCY:** Catalog still says Public/no-Bearer while AC-12 and the screen use a Student-specific result. After #08 succeeded, the client interprets #15 404 as no enrollment for that Student. Latest-per-user is source behavior; `(user_id, course_id)` uniqueness is not established.
- **Mapping:** `ACTIVE` enters the already-enrolled branch; non-ACTIVE rows follow the current API #19 eligibility behavior. The handler is read-only; no retry/cache is added.

### EV-04 — Điều hướng theo kết quả enrollment/payment

- **Trigger:** Branch after #15; the free-enrollment mutation runs only after a Student activates the CTA.
- **Current flow:** `ACTIVE` opens `/student/courses`. A #15 404 after successful #08 uses price `0` to show free enrollment; positive price links to ST-05. Invalid/negative price stops with an error. The explicit free CTA POSTs #19 with path/body `course_id`; #19 gets user identity from JWT. After success, GET #20 page 1 must contain the course before ST-08 opens. A #19 HTTP 409 is reconciled through #20 without resending POST. The paid branch remains dependent on ST-05/#16 and ST-06/#17; browser return/callback is not payment proof.
- **Errors:** 401/403 show login-required; #08 404 shows not-found. If #19 succeeds but #20 fails, retry reads #20 only.
- **Current source:** ST-04 calls #08/#15/#19/#20; descriptors #15/#19 are WIRED. Database/browser runtime is unverified.

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
