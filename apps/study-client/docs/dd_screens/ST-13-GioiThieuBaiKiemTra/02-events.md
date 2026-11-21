# ST-13 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-13-EV-001` | `ST13-EV-01` / ST13-EV-01 — Mở route và tải quiz | See source event detail below |
| `ST-13-EV-002` | `ST13-EV-02` / ST13-EV-02 — Xác nhận bắt đầu làm bài | See source event detail below |
| `ST-13-EV-003` | `ST13-EV-03` / ST13-EV-03 — Chọn CTA ôn lại bài giảng | See source event detail below |
| `ST-13-EV-004` | `ST13-EV-04` / ST13-EV-04 — Chọn xem lại attempt trước | See source event detail below |
| `ST-13-EV-005` | `ST13-EV-05` / ST13-EV-05 — Header, breadcrumb, support và footer links | See source event detail below |
| `ST-13-EV-006` | `Source heading` / Events không được suy ra từ static copy | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST13-EV-01 — Mở route và tải quiz

- **Element / loại:** route load; không phải control trong ảnh.
- **Tiền điều kiện:** người dùng mở route thiết kế với `quizId`; Student auth/session phải tồn tại theo contract Bearer Student, nhưng Study Web chưa có session/router source.
- **Input:** URL `quizId` (catalog path `quiz_id:int64!`), Student Bearer JWT. Không nhận user ID, attempt ID, answer, query hoặc body từ route.
- **Xử lý:**
  1. Đọc `quizId`; cách chuẩn hóa/range/invalid-path response chưa được nguồn chốt. Không đoán HTTP 400/422 hoặc redirect.
  2. Kiểm tra auth/role theo contract server; không coi avatar/name mockup là xác thực.
  3. Gửi GET #28 tới `/api/v1/quizzes/{quiz_id}`. Header `Authorization: Bearer …`; không có body/query được catalog khai báo.
  4. Khi 200 `DESIGN_RESOURCE_RETRIEVED`, đọc `data` theo Quiz contract. Chỉ map field đã được schema/API owner xác nhận. `questions`, `QuizChoice`, duration nullability, answer policy và ordering chưa hoàn tất.
  5. Không trả `is_correct`; không tự ghép API #29, #30 hoặc attempt history trong lúc load.
  6. Khi 401/403/404/500, dùng đúng response/business code. Cách phục hồi session, mapping not-found/access masking, retry và copy chưa được chốt; không suy ra 404=quiz đóng hoặc 403=hết lượt.
  7. Cập nhật trạng thái UI chỉ sau khi có mapping được duyệt. “Sẵn sàng”/“đóng” không được suy ra từ sample badges hoặc một response 200 chưa có eligibility semantics.
- **API contract:** API #28 `GET /api/v1/quizzes/{quiz_id}`; Bearer JWT, role Student; path `quiz_id:int64!`; response `ApiEnvelope<Quiz>`; success `200 DESIGN_RESOURCE_RETRIEVED`; errors `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED`, `404 DESIGN_RESOURCE_NOT_FOUND`, `500 DESIGN_INTERNAL_ERROR`. Catalog chưa khai báo 409, query, body, timeout, cache hay retry.
- **Output/side effect:** đọc dữ liệu quiz khi endpoint được triển khai; GET không có write được thiết kế. Không tạo attempt khi load. Cache/telemetry không được mô tả.
- **State/error:** dự kiến `loading`; 200 có thể dẫn đến `available` chỉ sau khi eligibility/open rule được chốt; 401/403/404/500 mapping UI còn cần contract. Network error và path parse chưa có API/UI rule.
- **Status:** API design only; API #28 Student route/module/test `NOT_FOUND`; Study Web `UNWIRED`.

### ST13-EV-02 — Xác nhận bắt đầu làm bài

- **Element / loại:** #16 button; Click.
- **Tiền điều kiện:** Student chủ động nhấn Start theo ST-13 inventory row; quiz có thể bắt đầu theo AC-16 (đủ quyền, đang mở). F05 và ST-14 inventory/DD chưa thống nhất screen owner/thứ tự của #29; eligibility owner giữa #28/#29 cũng chưa chốt.
- **Input:** `quiz_id` từ route; Student Bearer JWT. Không có request body, attempt number, `user_id`, idempotency key hoặc query param trong API catalog #29.
- **Xử lý:**
  1. Trước khi gửi request, resolve owner conflict giữa ST-13 row, F05 và ST-14 row/DD; không triển khai POST từ cả hai screen. Nếu chọn ST-14, phải giải quyết route `/student/quizzes/:quizId/attempts/:attemptId` đang yêu cầu ID trước POST. Hiện chưa có decision.
  2. Theo ST-13 row riêng lẻ, candidate trigger là explicit click; không tự gửi POST khi GET #28 thành công hay khi trang render.
  3. Kiểm tra route/auth prerequisite theo contract đã được duyệt; không dùng “Attempt 2”, `2/3`, deadline hoặc màu xanh trong mockup như bằng chứng đủ quyền.
  4. Chỉ nếu owner xác nhận ST-13 sở hữu request, gửi POST #29 tới `/api/v1/quizzes/{quiz_id}/attempts` với Bearer Student; không gửi body/query. Nếu owner giao request cho ST-14 thì ST-13 không gửi POST.
  5. Đọc HTTP status và `businessCode`. Không tự diễn giải 403/404/422/409 thành rule cụ thể ngoài code; API #29 Q-29-01..05 còn mở eligibility, attempt limit/expiry/resume, identity, path validation và initial response.
  6. Với 201 `DESIGN_RESOURCE_CREATED`, kiểm tra envelope/`data.id` theo API #29 logical QuizAttempt. `answers[]`, `started_at` clock/format và nullability `submitted_at`/`score` vẫn cần chốt. Không lấy attempt ID từ copy trong PNG.
  7. Chỉ sau khi có `attemptId` hợp lệ mới điều hướng theo sequence owner duyệt; ST-14 direct-entry guard và route chưa được implement/verify.
  8. Với timeout/connection ambiguity, không tự động POST lại: idempotency/dedup/reconciliation chưa được thiết kế. Hành động tiếp theo cần API/product decision.
- **API contract:** API #29 `POST /api/v1/quizzes/{quiz_id}/attempts`; Bearer JWT, role Student; path `quiz_id:int64!`; không body/query; success `201 DESIGN_RESOURCE_CREATED`; errors `401 DESIGN_AUTHENTICATION_REQUIRED`, `403 DESIGN_ACCESS_DENIED`, `404 DESIGN_RESOURCE_NOT_FOUND`, `422 DESIGN_VALIDATION_ERROR`, `409 DESIGN_STATE_CONFLICT`, `500 DESIGN_INTERNAL_ERROR`.
- **Output/side effect:** theo AC-16/API #29 design, success tạo attempt trạng thái ban đầu `IN_PROGRESS`; legacy candidate persistence là `quiz_attempts`, trong khi V1-PILOT DDL dùng `assessment_attempts` với UUID/lifecycle khác. Chưa có runtime write hoặc schema mapping xác minh. Sau success handoff về ST-14 theo screen owner/order cần chốt.
- **Retry/duplicate:** API #29 chưa khai báo idempotency key hoặc chống concurrent create. Không retry POST mù sau response mất; conflict/recovery phải chờ contract.
- **Status:** design only; route/module/test `NOT_FOUND`; click flow chưa được runtime verify.

### ST13-EV-03 — Chọn CTA ôn lại bài giảng

- **Element / loại:** #17 CTA; Click.
- **Input:** không có lesson ID hoặc course context được xác nhận từ route/API #28 response.
- **Xử lý:** screenshot đưa ra CTA nhưng inventory không chỉ định event/API/destination. HTML companion không chứa CTA tương ứng; không thể lấy `lessonId` từ asset. Không gọi #24 hoặc gán route ST-11 bằng suy đoán.
- **Output/exception:** destination, preservation of quiz context/history và quyền xem lesson chưa có contract; cần quyết định trước implementation.
- **API:** không có API được xác nhận.
- **Status:** `BLOCKED — missing handoff/lesson context`.

### ST13-EV-04 — Chọn xem lại attempt trước

- **Element / loại:** #27 button; Click.
- **Input:** PNG có dữ liệu attempt mẫu nhưng không có attempt ID/data source trong route contract.
- **Xử lý:** inventory đưa GET #32 vào ST-16, không xác nhận ST-13 gọi #32. Không tự ghép kết quả sample với path `attempt_id` hay tự hiển thị nội dung đáp án.
- **Output/exception:** route/destination, owner authorization, rule khi attempt đang pending grading và policy lộ đáp án chưa được duyệt.
- **API:** không xác nhận API cho event tại ST-13; #32 không được gọi theo suy đoán.
- **Status:** `BLOCKED — history source and result handoff missing`.

### ST13-EV-05 — Header, breadcrumb, support và footer links

- **Element / loại:** #1–#5, #19, #28–#29; click/focus theo affordance trong ảnh.
- **Input:** click target; không có route parameters/context contract đầy đủ.
- **Current source:** companion HTML fallback có static anchors tới `/`, `/courses`, `/student/courses`, `/student/progress`, `/login`, `/register`; screenshot có labels/destinations khác. Không có Study Web handler hoặc route map để xác nhận browser transition.
- **Xử lý:** không tạo router/API event từ label; không khai báo `href` mới. Link semantics, target, focus, external navigation, history/back behavior cần được quyết định cùng Study Web routing.
- **Output/exception:** route change chưa xác minh; auth/session recovery và unavailable destination chưa có policy.
- **Status:** `UNWIRED / DESTINATION NOT CONFIRMED`.

### Events không được suy ra từ static copy

- Không tạo countdown/timer, visibility-change/tab-blocking, auto-save webhook, reconnect/restore, auto-submit, certificate generation hoặc scoring function từ #21–#24.
- API #30 là answer-save design ở ST-14; nó không chứng minh realtime autosave hoặc proctoring đang tồn tại.
- Search, notification, profile, “view attempt” và discussion links không có event/API trong ST-13 contract hiện tại.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
