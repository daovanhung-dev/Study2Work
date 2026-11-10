# ST-14 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-14-EV-001` | `ST14-EV-01` / ST14-EV-01 — Mở route và khởi tạo quiz | See source event detail below |
| `ST-14-EV-002` | `ST14-EV-02` / ST14-EV-02 — Nhận handoff hoặc phục hồi attempt | See source event detail below |
| `ST-14-EV-003` | `ST14-EV-03` / ST14-EV-03 — Chọn đáp án và autosave | See source event detail below |
| `ST-14-EV-004` | `ST14-EV-04` / ST14-EV-04 — Chuyển câu, chọn câu từ grid và lọc câu chưa trả lời | See source event detail below |
| `ST-14-EV-005` | `ST14-EV-05` / ST14-EV-05 — Gắn hoặc bỏ cờ xem lại | See source event detail below |
| `ST-14-EV-006` | `ST14-EV-06` / ST14-EV-06 — Hiển thị/đếm thời gian | See source event detail below |
| `ST-14-EV-007` | `ST14-EV-07` / ST14-EV-07 — Chọn nộp bài và chuyển ST-15 | See source event detail below |
| `ST-14-EV-008` | `ST14-EV-08` / ST14-EV-08 — Thoát bài thi/quay lại | See source event detail below |
| `ST-14-EV-009` | `ST14-EV-09` / ST14-EV-09 — Phím tắt chọn đáp án/chuyển câu/gắn cờ | See source event detail below |
| `ST-14-EV-010` | `ST14-EV-10` / ST14-EV-10 — Trạng thái mạng/WebSocket/autosave claim | See source event detail below |
| `ST-14-EV-011` | `Source heading` / D.1. Bảng error/business code dùng cho events | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST14-EV-01 — Mở route và khởi tạo quiz

- **Element/loại:** route load; không phải control trong ảnh.
- **Điều kiện:** Student mở `/student/quizzes/:quizId/attempts/:attemptId`; session/role hợp lệ theo contract. Study Web chưa có router/auth guard để xác nhận.
- **Input:** `quizId:int64!`, `attemptId:int64!` từ URL; Bearer JWT. Không nhận `user_id`, answer, score hoặc quyền từ query/client.
- **Xử lý theo thứ tự:**
  1. Parse path IDs theo kiểu int64. Quy tắc dương/range và route error chưa được catalog chốt; không tự đặt status/redirect.
  2. Xác nhận identity/Student role qua auth boundary dùng chung khi có implementation; current app không có source route để chỉ ra token storage/refresh.
  3. Xác thực handoff: `attemptId` phải là ID tạo từ POST #29. ST-13 DD hiện đặt #29 tại click Start; dòng ST-14/F05 lại có thể đặt #29 ở ST-14. Owner phải chọn đúng một trigger; không POST lần hai.
  4. Theo sequence được duyệt, gọi GET #28 `/api/v1/quizzes/{quiz_id}` với `Authorization: Bearer …`; không query/body theo catalog. Thứ tự #28 so với #29 cần chốt do nguồn mâu thuẫn.
  5. Parse envelope/businessCode. Với 200 `DESIGN_RESOURCE_RETRIEVED`, map Quiz fields chỉ khi schema response được xác nhận. Không dùng data từ PNG làm fallback.
  6. 401/403/404/500 giữ business code; cách hiển thị/re-auth/retry và copy chưa có contract. Network/timeout không có status API được nêu.
- **API:** #28 `GET /api/v1/quizzes/{quiz_id}`; Student Bearer; path `quiz_id:int64!`; response `ApiEnvelope<Quiz>`; 200/401/403/404/500 theo catalog.
- **Kết quả:** `loading → quiz_received` chỉ khi #28 success. Không xác lập attempt đã resume hay answer loaded; đây là blocker do thiếu endpoint đọc attempt.

### ST14-EV-02 — Nhận handoff hoặc phục hồi attempt

- **Element/loại:** route/navigation state; không phải marker control.
- **Input:** `quizId`, `attemptId` từ path; có thể có dữ liệu `QuizAttempt` do POST #29 trả tại ST-13 cùng session, nhưng navigation-state format/persistence chưa được quy định.
- **Xử lý:**
  1. Không suy ra attempt từ badge `2/3` hoặc lịch sử mockup.
  2. Nếu ST-13 đã tạo attempt theo ST-13 EV-02, chỉ tiếp nhận `id` từ response #29 hợp lệ; không gọi POST lần nữa tại ST-14.
  3. Nếu direct entry/refresh xảy ra, inventory không có GET attempt/answers. #28 chỉ đọc Quiz; không đủ để dựng `IN_PROGRESS`, started time, saved answers hoặc flags. Hiển thị “ready”/resume state chưa thể đặc tả cho tới khi có contract.
  4. Nếu POST #29 thật sự được owner chuyển sang ST-14, phải cập nhật ST-13 và inventory/handoff trước khi lập trình; kiểm tra 201 response/`data.id`, giữ 401/403/404/422/409/500. Không tự retry sau timeout vì duplicate/idempotency chưa chốt.
- **API:** Không gọi API trong ST14-EV-02 hiện tại; #29 là API tạo attempt theo catalog và candidate handoff, chưa chốt screen owner.
- **Kết quả:** `attemptId` hợp lệ là tiền điều kiện; refresh/resume, duplicate create, network ambiguity và data restoration là `BLOCKER`.

### ST14-EV-03 — Chọn đáp án và autosave

- **Element/loại:** #18–#21; Change/Click hoặc bàn phím.
- **Điều kiện:** question/options đã tải; Student có quyền; attempt vẫn cho phép cập nhật theo server policy. Attempt status/expiry policy hiện chưa xác nhận.
- **Input:** `attemptId:int64`, `question_id:int64`, lựa chọn hiện tại. API catalog ghi thêm `answer(s):string!`, nhưng tên JSON key và representation không được giải quyết.
- **Xử lý:**
  1. Lấy `question_id`/choice IDs từ response được xác nhận; không lấy label hoặc answer correctness từ DOM/ảnh.
  2. Validate question thuộc quiz/attempt và choice hợp lệ chỉ theo predicate/schema mà API owner chốt; hiện chưa có field/enum/limits đủ để tạo validator.
  3. Cập nhật UI selection/dirty state theo policy được duyệt; không xóa lựa chọn cũ nếu response/network failure chưa được reconciled.
  4. Contract inventory yêu cầu PUT #30 khi answer đổi. Endpoint: `/api/v1/attempts/{attempt_id}/answers`; header Bearer JWT; body tối thiểu catalog notation `question_id:int64!`, `answer(s):string!`. Không đưa JSON ví dụ runnable cho tới khi property/encoding được chốt.
  5. Không tự thêm debounce, queue ordering, request version, Idempotency-Key, retry interval hoặc concurrent-save rule. Đây là Q-30-01/Q-30-03.
  6. Với 200 `DESIGN_RESOURCE_UPDATED`, parse `ApiEnvelope<QuizAttempt>` nhưng `data.answers` có thể full attempt/subset và shape chưa rõ. Chỉ chuyển UI thành `saved` sau response thành công; không tuyên bố server timestamp nếu response không cấp.
  7. Với 401/403/404/422/500, giữ business code; UI có thể không báo đã lưu. Mapping 404 (attempt/question/foreign quiz), field errors và recovery chưa chốt. API #30 không có 409. Network timeout/response mất không cho biết server đã ghi hay chưa.
- **API:** #30 PUT; Student Bearer; path `attempt_id:int64!`; request body theo catalog còn mơ hồ; response `ApiEnvelope<QuizAttempt>`; 200 `DESIGN_RESOURCE_UPDATED`; lỗi 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`.
- **Kết quả/side effect:** AC-16 kỳ vọng UPSERT AttemptAnswer; DDL candidate không có unique `(attempt_id, question_id)` và không chứng minh live write. Không xác nhận persistence cho đến khi contract/runtime có mặt.

### ST14-EV-04 — Chuyển câu, chọn câu từ grid và lọc câu chưa trả lời

- **Element/loại:** #22/#24 previous/next; #29 question grid; #30 filter; click/tap/keyboard.
- **Điều kiện:** danh sách questions đã nhận từ #28 và current question index hợp lệ.
- **Input:** question ID đang chọn, target từ grid hoặc index ±1; answer/dirty state hiện tại.
- **Xử lý:**
  1. Xác định target từ danh sách/order được server trả; order semantics hiện chưa có contract hoàn chỉnh.
  2. Nếu target không tồn tại hoặc ngoài biên, không đổi selection. Trạng thái disabled của previous/next cần được design chốt.
  3. Nếu answer đang dirty/saving, không drop local state. Quy tắc flush-before-navigation, queue/serialization và failure recovery còn mở; không tự chặn hay tự gửi request thứ hai ngoài contract.
  4. Grid chỉ đổi current question; không suy ra answered/flagged state nếu state đó chưa được hydrate/confirm.
  5. Filter dựa trên định nghĩa “unanswered” sau khi answer projection/state lifecycle được chốt. Filter không ghi API, không nên làm mất selected question/state; empty result behavior chưa thiết kế.
  6. Tính progress/count chỉ theo formula được owner xác nhận. PNG hiển thị `14/20` và các counter không khớp; không dùng con số đó làm thuật toán.
- **API:** không có API điều hướng/filter trong catalog; #30 chỉ lưu khi answer thay đổi, và sequencing cần contract.
- **Kết quả:** current question/filter view cập nhật cục bộ; persisted answer/progress không được giả định từ điều hướng.

### ST14-EV-05 — Gắn hoặc bỏ cờ xem lại

- **Element/loại:** #23; Click, shortcut `P`.
- **Điều kiện:** câu đang hiển thị; semantics toggle/flag còn phải xác nhận.
- **Input:** current `question_id` và desired flagged state.
- **Xử lý:**
  1. Chỉ đọc/đổi local flag nếu UI flow được duyệt; inventory không khai báo flag field hay API.
  2. Không đưa flag vào #30 answer payload; catalog body không có field này.
  3. Không báo flag đã lưu qua reload/thiết bị khác khi không có persistence source.
  4. Định nghĩa rõ flag có thể áp dụng cho answered question hay không, counter/list style và toggle idempotency trước implementation.
- **API:** không có API flag trong ST-14 inventory.
- **Kết quả:** local presentation là proposal; cross-session persistence `BLOCKED`.

### ST14-EV-06 — Hiển thị/đếm thời gian

- **Element/loại:** #3/#9; Timer.
- **Điều kiện:** API/business owner xác định duration/deadline, authoritative clock, pause/resume và expiry behavior.
- **Input:** server-provided time fields/config chỉ khi contract được bổ sung; hiện `Quiz.duration_minutes?` là schema design, không có `deadline_at`/started timestamp policy hoàn chỉnh.
- **Xử lý:**
  1. Không dùng hai số trong PNG làm giá trị ban đầu hoặc tính số giây còn lại.
  2. Không suy ra deadline từ local clock, không thêm timer endpoint hay server field.
  3. Khi time source/policy chưa có, ẩn timer hoặc đánh dấu design placeholder; không tự khóa lựa chọn/auto-submit.
  4. Hết hạn/đồng hồ sai lệch cần status/error từ API; #30 không liệt kê 409 và G-09 còn mở.
- **API:** không có API timer riêng. #28 duration có thể optional theo Quiz logical schema; actual field/nullability/runtime chưa xác nhận.
- **Kết quả:** không phát sinh side effect/submit tự động từ thời gian trong DD này.

### ST14-EV-07 — Chọn nộp bài và chuyển ST-15

- **Element/loại:** #12; Click.
- **Điều kiện:** attempt và route context đã có; save pending behavior cần được ST-15 contract chốt.
- **Input:** `attemptId` từ route; số câu chưa trả lời nếu computation được xác nhận.
- **Xử lý:**
  1. Không xem sample count là dữ liệu authoritative.
  2. Chuyển sang route ST-15 theo inventory với `attemptId`; destination path `/student/attempts/:attemptId/submit`.
  3. ST-15 chịu trách nhiệm xác nhận, flush PUT #30 còn pending, rồi POST #31 một lần theo inventory; ST-14 không gọi #31.
  4. Không khóa attempt hoặc cập nhật `submitted` chỉ vì click/navigate; chỉ server #31 success có thể xác nhận submit.
  5. Handoff context nào phải truyền giữa screen (dirty queue/remaining count/quiz ID) chưa được định nghĩa. Không serialize token hoặc answer vào query URL.
- **API:** không gọi #31 từ ST-14. #31 contract thuộc ST-15; state machine/409/double-submit chưa khóa.
- **Kết quả:** điều hướng ST-15 nếu route/runtime được wire; UI/route hiện tại chưa tồn tại để xác nhận.

### ST14-EV-08 — Thoát bài thi/quay lại

- **Element/loại:** #1/#5; Click/browser back.
- **Điều kiện:** route có attempt; dirty/saving state phải được biết nếu runtime triển khai.
- **Input:** click target/history event, route params, local dirty state nếu có.
- **Xử lý:**
  1. Hai nút trong ảnh có thể trùng semantics; route destination chưa có contract.
  2. Không coi HTML anchor static `/student/quizzes/:quizId` là router proof.
  3. Nếu có unsaved state, cảnh báo, flush, giữ state hay rời trang là policy chưa quyết định; không tự discard hoặc POST #29 lại.
  4. Quay ST-13 là một khả năng theo graph nhưng không được xác nhận là destination của hai controls.
- **API:** không có API rời bài.
- **Kết quả:** navigation/dirty-state behavior `BLOCKED` cho tới khi route/handoff policy được phê duyệt.

### ST14-EV-09 — Phím tắt chọn đáp án/chuyển câu/gắn cờ

- **Element/loại:** #25, #18–#24; keyboard.
- **Điều kiện:** focus đang ở vùng quiz và mapping của phím được xác nhận; không có keyboard handler hiện tại.
- **Input:** phím `1–4`, `→`, `P` đúng như copy mockup.
- **Xử lý:**
  1. `1–4` có thể chọn option theo thứ tự chỉ khi số lượng/order choice được server xác nhận; không ép 4 options.
  2. `→` trong ảnh ghi chuyển câu; hướng/trạng thái edge chưa định nghĩa. Không gán phím trái khi ảnh không nêu.
  3. `P` đề xuất gọi toggle flag; persistence chưa có.
  4. Focus scope, form/text input conflict, screen reader, visible key hint và accessibility behavior phải được chốt theo Study Web design target.
- **API:** theo event tương ứng; chọn answer có thể dẫn #30 sau khi payload chốt; flag không có endpoint.
- **Kết quả:** shortcut là design-only; không có implementation/runtime evidence.

### ST14-EV-10 — Trạng thái mạng/WebSocket/autosave claim

- **Element/loại:** #31 và trạng thái #10; status display/reconnect.
- **Điều kiện:** cần có network/API state source; WebSocket chỉ khi có protocol/event contract.
- **Input:** #30 request lifecycle khi endpoint tồn tại; online/offline signal hoặc heartbeat chỉ sau khi được định nghĩa.
- **Xử lý:**
  1. PNG copy “Trực tuyến”, `WebSocket ping 18ms`, “Idempotent Autosave” không được coi là data source hoặc behavior proof.
  2. HTTP #30 response có thể chứng minh một lần request thành công nếu route chạy; không chứng minh idempotency/realtime.
  3. Không tự thêm WebSocket handshake, polling, retry/backoff, offline queue hoặc ping API.
  4. Khi network lỗi/timeout, kết quả write có thể ambiguous; không hiển thị saved và không replay tự động khi chưa có idempotency/reconciliation policy.
- **API:** #30 như EV-03; không có API ping/WebSocket trong inventory.
- **Kết quả:** chỉ render trạng thái theo contract đã xác nhận; hiện runtime `NOT_FOUND`/`UNWIRED`.

### D.1. Bảng error/business code dùng cho events

| API | Thành công | Lỗi theo catalog | Các điều chưa được định nghĩa |
|---|---|---|---|
| #28 GET quiz | 200 `DESIGN_RESOURCE_RETRIEVED` | 401 authentication; 403 access; 404 resource; 500 internal | Eligibility-vs-not-found, answer projection, timeout/network UI, retry/cache. |
| #29 POST attempt | 201 `DESIGN_RESOURCE_CREATED` | 401 authentication; 403 access; 404 resource; 422 validation; 409 state conflict; 500 internal | Trigger owner, eligibility predicate, duplicate/concurrent create, resume/timeout recovery, initial response fields. |
| #30 PUT answers | 200 `DESIGN_RESOURCE_UPDATED` | 401 authentication; 403 access; 404 resource; 422 validation; 500 internal | Exact body/property/limits; attempt ownership/status; question membership; upsert key; concurrency/transaction; response projection; retry/version/idempotency. **Không có 409 trong catalog #30.** |

HTTP/business code được giữ nguyên từ contract; UI message, field-errors và recovery không được tự suy ra từ status alone.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
