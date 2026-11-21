# AD-17 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-17-EV-001` | `Source heading` / EV-01 — Vào màn hình và đọc `quizId` | See source event detail below |
| `AD-17-EV-002` | `Source heading` / EV-02 — Xác thực và authorization | See source event detail below |
| `AD-17-EV-003` | `Source heading` / EV-03 — Tải thống kê qua API #91 | See source event detail below |
| `AD-17-EV-004` | `Source heading` / EV-04 — Xử lý response và ánh xạ giao diện | See source event detail below |
| `AD-17-EV-005` | `Source heading` / EV-05 — Xử lý lỗi API | See source event detail below |
| `AD-17-EV-006` | `Source heading` / EV-06 — Quay lại AD-15 | See source event detail below |
| `AD-17-EV-007` | `Source heading` / EV-07 — Kiểm tra kết nối dữ liệu (listener prototype) | See source event detail below |
| `AD-17-EV-008` | `Source heading` / EV-08 — Shell/footer placeholder controls | See source event detail below |
| `AD-17-EV-009` | `Source heading` / EV-09 — Claim tổng hợp nền sau khi submit | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### EV-01 — Vào màn hình và đọc `quizId`

- **Element / loại:** Angular route `/admin/quizzes/:quizId/statistics`; page entry/load; liên quan #12–#15, #18, #20–#21.
- **Điều kiện:** Angular source registers the route and page. Browser deep-link/runtime behavior is not verified. AC-35 yêu cầu Admin có quiz-management permission.
- **Đầu vào:** URL path segment `quizId`; direct API path yêu cầu `quiz_id:int64!`. Catalog xác nhận required int64; current #91 parser chỉ nhận toàn chuỗi 1–19 chữ số, giá trị dương trong signed-int64.
- **Xử lý:** `AD17Page` validates the complete raw route value against the same positive signed-int64 range before calling `AD17ApiService.getStatistics(quizId)`. Invalid/missing IDs stop locally; valid raw text is preserved. Fine-grained screen permission remains unimplemented; local API parsing and shared `ADMIN` guard are separate server behavior.
- **Kết quả:** Valid route IDs call #91 and can render the local projection. The separate Stitch prototype still renders placeholders and makes no request. The direct catalog contract does not provide Quiz title or analytics fields.
- **Ngoại lệ:** Missing/malformed/zero/overflow IDs render a local route error without HTTP; 401/403 follow EV-02; 404 from #91 can still represent a missing Quiz.

### EV-02 — Xác thực và authorization

- **Element / loại:** Screen guard/API auth, page entry; copy RBAC ở #11 và Admin shell #9 không thay thế kiểm tra.
- **Điều kiện:** Trước request #91. Expected actor theo AC-35 là Admin có quiz-management permission.
- **Đầu vào:** Bearer JWT/session của Admin; permission scope nếu policy được định nghĩa. Không truyền user ID/role do client tự khai.
- **Xử lý:** (1) Client yêu cầu token hiện hành; (2) backend current source gọi shared `validate_current_user_request(... role="ADMIN")` trước parse ID/query; (3) AC-35 fine-grained permission chưa có source-backed policy; (4) không truy cập DB nếu guard trả lỗi.
- **API:** Authorization header Bearer JWT; lỗi direct 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`. Local API source dùng chung guard; không chứng minh permission quản lý quiz riêng.
- **Kết quả:** Current caller uses the shared Admin API client for the Bearer token; the page renders shared error state copy for auth failures. AC-35 fine-grained permission is still unresolved, and browser behavior is not verified.

### EV-03 — Tải thống kê qua API #91

- **Element / loại:** Page load/network request; #20–#22/#23–#25 là consumer candidates.
- **Điều kiện:** Route ID có thể gửi theo contract; Admin auth/permission đạt; API response contract được chốt. Hiện contract mismatch ngăn mapping.
- **Đầu vào:** Path `quiz_id:int64!`; Bearer JWT. Không body, query hoặc filter theo direct catalog.
- **Xử lý current server:** (1) shared `ADMIN` guard; (2) parse path ID; (3) gọi một grouped `LEFT JOIN` trên legacy `quizzes` và `quiz_attempts`; (4) tính projection trong GET; (5) không commit/write. Query không filter `quiz.status` hoặc `attempt.status`, không đọc `quiz_answers`.
- **Direct API contract:** GET `/api/v1/admin/quizzes/{quiz_id}/statistics`; HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; response `ApiEnvelope<Quiz>`; 401/403/404/500. Không có retry, pagination, query filter hoặc body được khai báo.
- **Current local API response:** `AdminQuizStatistics` riêng với quiz_id, attempt/submitted/graded counts, average_score, passed_attempt_count và pass_rate_percent. Response model khác catalog; local DTO là DERIVED, không được client coi là approved.
- **Kết quả:** `AD17ApiService` is a current caller. The page maps local `AdminQuizStatistics` into Quiz ID plus attempt/submitted/graded counts, average, passed count and pass rate, with a visible contract notice. This source projection is not an approved catalog contract; no chart is computed on the client.

### EV-04 — Xử lý response và ánh xạ giao diện

- **Element / loại:** State transition/render success/no-data; #20–#25, #28–#29.
- **Điều kiện:** Có response từ #91 và schema đã được owner chốt. Điều kiện chưa đạt hiện tại.
- **Đầu vào:** Direct catalog success `ApiEnvelope<Quiz>`; local source success DTO là khác biệt riêng.
- **Xử lý:** (1) Parse envelope/business code; (2) so response schema với approved contract; (3) current direct type không chứa metric fields nên không suy ra analytics từ Quiz; (4) không đổi NULL/unknown thành zero; (5) không tính metric client-side; (6) chỉ sau quyết định response+metric mới chọn no-data/ready và map fields; (7) giữ source identity/trace metadata nếu contract giữ envelope.
- **Metric proposal, chưa được duyệt:** `attempt_count` mọi row; `submitted_attempt_count` khi submitted_at khác NULL; `graded_attempt_count` khi score khác NULL; average trên non-NULL score; pass theo score ≥ passing_score; passed count/rate NULL nếu threshold NULL; pass rate mẫu số graded attempts, NULL khi không có điểm. Các điều kiện này xuất phát từ API #91 DD/local SQL, không phải direct API catalog.
- **Metric không có trong local DTO:** score distribution, completion rate, average duration. Copy tại #16/#25/#29 không đủ cơ sở để tạo ba metric này.
- **Kết quả:** Angular source shows the local projection when the request succeeds, but does not define a separate no-data/zero/unknown semantic. The separate prototype's empty state is static. Approved analytics semantics remain BLOCKED until the schema is reconciled.

### EV-05 — Xử lý lỗi API

- **Element / loại:** Error-state handling khi EV-03 thất bại.
- **Đầu vào / response:**

| HTTP | Business code | Expected xử lý | Current evidence |
|---:|---|---|---|
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` | Coi session/token không hợp lệ hoặc hết hạn theo auth flow chung; không retry mù. | Local shared guard; page không xử lý. |
| 403 | `DESIGN_ACCESS_DENIED` | Báo không đủ quyền; không render data. | Local shared ADMIN; fine-grained quiz permission chưa được xác minh. |
| 404 | `DESIGN_RESOURCE_NOT_FOUND` | Báo Quiz không tìm thấy hoặc không truy cập được theo chính sách. | Local path malformed và missing row đều 404; tách message cần policy. |
| 500 | `DESIGN_INTERNAL_ERROR` | Hiển thị lỗi dịch vụ an toàn; không lộ chi tiết DB. | Handler rollback lỗi query/mapping và log trace; không có UI. |

- **Xử lý:** The current shared route state renders a generic error view and shared messages for 401/403/404/network failures; 500 falls through to the generic service error. No retry policy is defined. Network offline/timeout has no HTTP/business code in the catalog. There is no 422 in the direct #91 error set.
- **Kết quả:** Angular source can enter `error`; the separate prototype makes no request. Browser behavior is not verified.

### EV-06 — Quay lại AD-15

- **Element / loại:** Click anchor #13, #17 hoặc #26.
- **Điều kiện:** Người dùng kích hoạt một trong ba link về danh sách. Inventory liệt kê AD-15 là liên kết; HTML dùng `/admin/quizzes`.
- **Đầu vào:** Route hiện tại có thể có Quiz ID; yêu cầu giữ/loại bỏ param khi quay lại chưa được xác định.
- **Xử lý:** Angular page uses `RouterLink="/admin/quizzes"`; the prototype HTML uses anchors to the same path.
- **Kết quả:** The route target exists in Angular source; browser navigation, history stack, query/filter preservation and destination permission are not runtime-verified or specified.

### EV-07 — Kiểm tra kết nối dữ liệu (listener prototype)

- **Element / loại:** Click #27; listener trong `code.html`.
- **Điều kiện:** The control exists only in the Stitch prototype; it is not the Angular page's API control.
- **Đầu vào:** Không có user data hoặc route data in the prototype listener.
- **Xử lý theo thứ tự source:** (1) thêm `animate-spin` cho icon; (2) đổi nhãn thành “Đang kiểm tra máy chủ…”; (3) set `disabled=true`; (4) chờ 700 ms; (5) bỏ spin, đổi nhãn “Đã hoàn tất kiểm tra”, hiện `syncFeedback` bằng bỏ `hidden`/thêm `flex`; (6) chờ thêm 3000 ms; (7) reset nhãn ban đầu và bỏ disabled. Không có fetch/XHR, HTTP status, timeout network, retry hay API #91 call. Feedback là static string “Kết nối API hoạt động bình thường…Trống Analytics”.
- **Kết quả:** Chỉ timer UI; không thể coi là health check. Khi click lại, source không ẩn feedback cũ. UI behavior ở đây là prototype behavior, không phải acceptance cho connectivity thật.

### EV-08 — Shell/footer placeholder controls

- **Element / loại:** Click nav #2–#6, notification #8, breadcrumb #10/#12, footer #31–#33.
- **Điều kiện:** User click control.
- **Đầu vào / xử lý:** Prototype nav/footer anchors use `href="#"`; notification has no screen-specific listener; breadcrumb Hệ thống/Quản trị khảo thí are spans. These prototype controls do not establish Angular shell behavior.
- **Kết quả:** Placeholder/cursor styling có thể đổi; không mô tả như chức năng route đã triển khai. Không có API liên quan.

### EV-09 — Claim tổng hợp nền sau khi submit

- **Element / loại:** Copy trên note card #29 và empty explanation #25.
- **Điều kiện:** Prototype nói thí sinh nộp bài; AC-16 có luồng attempt/submit riêng.
- **Current evidence:** AC-35 vẽ thao tác Admin gọi GET #91 rồi aggregate; local #91 aggregate khi nhận GET. Không có background worker, event subscription, push invalidation hoặc liên kết #31/#32 được tìm thấy trong màn này.
- **Kết quả:** Không tự thiết kế event/job. Cần Product/BE xác nhận liệu có aggregation job/event hay chỉ GET-time aggregation; nội dung hiện có là static, không chứng minh dữ liệu tự cập nhật.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
