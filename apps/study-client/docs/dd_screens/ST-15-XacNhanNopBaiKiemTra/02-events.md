# ST-15 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-15-EV-001` | `ST15-EV-01` / ST15-EV-01 — Mở route và dựng xác nhận | See source event detail below |
| `ST-15-EV-002` | `ST15-EV-02` / ST15-EV-02 — Tiếp tục kiểm tra | See source event detail below |
| `ST-15-EV-003` | `ST15-EV-03` / ST15-EV-03 — Xác nhận nộp và flush answer | See source event detail below |
| `ST-15-EV-004` | `ST15-EV-04` / ST15-EV-04 — Nhận kết quả submit thành công | See source event detail below |
| `ST-15-EV-005` | `ST15-EV-05` / ST15-EV-05 — Lỗi API, conflict hoặc kết quả mạng không rõ | See source event detail below |
| `ST-15-EV-006` | `ST15-EV-06` / ST15-EV-06 — Timer và summary trong lúc xác nhận | See source event detail below |
| `ST-15-EV-007` | `ST15-EV-07` / ST15-EV-07 — Header, backdrop và dismiss/accessibility interaction | See source event detail below |
| `ST-15-EV-008` | `Source heading` / D.1. Bảng response và state mapping | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ST15-EV-01 — Mở route và dựng xác nhận

- **Element/loại:** route load; không có control trigger.
- **Điều kiện:** Student session/context; `attemptId` có trên route. Ownership/attempt state sẽ do server bảo đảm khi contract có implementation.
- **Input:** path `attemptId:int64`; ST-14 handoff nếu có. Không có query/body/API read riêng trong inventory.
- **Xử lý:** (1) parse path theo type đã khai báo, không tự đặt route error/status ngoài contract; (2) yêu cầu Student context theo auth boundary khi có; (3) nhận summary/handoff đã được phê duyệt; (4) không dựng số liệu từ mockup và không tự gọi #28/#31; (5) render confirm khi đủ data; nếu thiếu summary source, giữ trạng thái chưa sẵn sàng theo UI decision cần owner chốt.
- **API:** không gọi API trong event này. Không có GET attempt/answer trong screen inventory.
- **Kết quả/ngoại lệ:** `opening → confirm` chỉ với route/context và dữ liệu cần thiết. Direct entry, refresh, expired session, missing handoff và loading/error presentation chưa được wire.

### ST15-EV-02 — Tiếp tục kiểm tra

- **Element/loại:** #17; Click/keyboard activation.
- **Điều kiện:** `confirm`; route có cùng `attemptId`; không có submit đã được server chấp nhận.
- **Input:** path `attemptId`; navigation/history context; dirty/pending answer state nếu được truyền.
- **Xử lý:** (1) giữ nguyên attemptId; (2) không gọi #31; (3) trở về ST-14 theo navigation graph; (4) khôi phục dirty queue/selection theo handoff contract khi có; (5) không discard pending answers hoặc tạo attempt mới.
- **API:** không gọi API. Không flush #30 chỉ do bấm Continue trừ khi policy navigation riêng được phê duyệt.
- **Kết quả/ngoại lệ:** dự kiến ST-14 cùng attempt. Exact URL/history, refresh/back behavior và unsaved-state guard chưa xác nhận; không tự áp `window.history.back()` chỉ vì HTML mẫu dùng cách đó.

### ST15-EV-03 — Xác nhận nộp và flush answer

- **Element/loại:** #18; Click/Submit/keyboard activation.
- **Điều kiện:** `confirm`; Student context; `attemptId`; có thể xác định pending #30 operations từ state hợp lệ. Inventory yêu cầu flush trước submit.
- **Input:** `attemptId:int64`; answer queue/state do ST-14 handoff tạo. Không nhận answer/count/score từ DOM hay URL.
- **Xử lý tuần tự:** (1) bỏ qua activation trùng trong khi cùng submit intent đang hoạt động; (2) chuyển `confirm → flushing_answers`; (3) chờ các #30 writes pending được xử lý theo queue contract được duyệt; không tự chọn ordering, concurrency hay retry; (4) nếu bất kỳ write nào lỗi/timeout/ambiguous, dừng và không gọi #31; (5) chỉ khi toàn bộ barrier được xác nhận thành công mới chuyển `submitting`; (6) gọi đúng một POST #31 với path `attemptId`, Bearer Student, không query/body; (7) không tự replay sau mất response do idempotency/reconciliation chưa chốt.
- **API phụ thuộc:** #30 PUT `/api/v1/attempts/{attempt_id}/answers` theo catalog; shape body hiện mơ hồ, 200 `DESIGN_RESOURCE_UPDATED`; 401/403/404/422/500. #30 DD/G-09 chưa cho phép đóng queue protocol. #31 POST như bảng A.4.
- **Kết quả:** flush barrier thành công chuyển sang `submitting`; lỗi flush giữ lại dữ liệu và ở error/ambiguous state. Không cập nhật UI thành submitted chỉ vì click hoặc vì #30 thành công.

### ST15-EV-04 — Nhận kết quả submit thành công

- **Element/loại:** response của #31; network completion.
- **Điều kiện:** event 03 đã hoàn thành flush barrier và #31 trả HTTP 200 với business code `DESIGN_RESOURCE_UPDATED`.
- **Input:** `ApiEnvelope<QuizAttempt>` theo catalog design; schema/projection/state enum vẫn cần xác nhận.
- **Xử lý:** (1) parse envelope theo schema được duyệt; (2) chỉ coi server accept là thành công; (3) không tự tính điểm hoặc “skill chart”; (4) map `PENDING_GRADE`/`GRADED` chỉ theo response/AC sau khi field contract chốt; (5) chuyển screen state `submitted`; (6) điều hướng ST-16 và chuyển `attemptId`/response theo approved navigation contract.
- **API:** không phát sinh request bổ sung tại ST-15. #32 thuộc ST-16; không gọi #32 làm side effect ngầm.
- **Kết quả/ngoại lệ:** server chấp nhận mới cho phép chuyển ST-16. Nếu response 200 nhưng envelope/schema không parse được, reconciliation và UI recovery chưa được quy định; không đoán state từ HTTP code một mình trong runtime cho tới khi contract hoàn chỉnh.

### ST15-EV-05 — Lỗi API, conflict hoặc kết quả mạng không rõ

- **Element/loại:** #18 và status/message region cần thiết kế; API/network response.
- **Điều kiện:** #30 flush failure, #31 business error, timeout hoặc connection loss.
- **Input:** HTTP/business code từ API; request lifecycle state; không có field-level body contract đầy đủ.
- **Xử lý:** (1) phân biệt lỗi flush #30 với lỗi #31; (2) không gọi #31 sau flush failure; (3) giữ pending/local answer state cho đến khi có reconciliation policy; (4) giữ nguyên business code API đã khai báo; (5) không coi 409 là success và không tự retry; (6) sau timeout/mất response #31 chuyển `ambiguous_network`, không tự gửi lại; (7) chỉ cho phép hành động tiếp theo theo recovery flow do API owner duyệt.
- **API/code mapping:** #31: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 422 `DESIGN_VALIDATION_ERROR`, 409 conflict code, 500 `DESIGN_INTERNAL_ERROR`. #30 không khai báo 409. Message, field-error projection, reauth, retry, reconciliation và destination chưa có contract.
- **Kết quả:** không thông báo submitted và không sang ST-16 nếu chưa có accepted response. UI copy/accessibility announcement chưa được thiết kế.

### ST15-EV-06 — Timer và summary trong lúc xác nhận

- **Element/loại:** #3, #11–#16; display/timer tick.
- **Điều kiện:** chỉ render nếu nguồn dữ liệu và policy được duyệt.
- **Input:** hiện không có authoritative countdown, server timestamp, summary projection, saved-state field, attempt ordinal/limit trong contract đã xác minh.
- **Xử lý:** (1) không khởi tạo timer từ số ảnh; (2) không suy ra timer #3 và #14 là cùng nguồn; (3) không tự tính unanswered/flagged/saved count nếu definition và handoff chưa chốt; (4) timer không auto-submit, lock hoặc expire; (5) không hiển thị instant grading/attempt-limit claim nếu chưa có contract.
- **API:** không có timer/summary endpoint được inventory khai báo cho ST-15.
- **Kết quả:** sample fields là design-only/blocked. Không phát sinh write hoặc navigation từ timer.

### ST15-EV-07 — Header, backdrop và dismiss/accessibility interaction

- **Element/loại:** #1, #4–#6; click, Escape, focus/keyboard interactions nếu được thiết kế.
- **Điều kiện:** dialog đang hiển thị.
- **Input:** action từ header/profile/backdrop/keyboard và current dirty/submit state.
- **Xử lý:** (1) không gán destination cho exit/profile khi contract không nêu; (2) không dismiss qua backdrop/Escape nếu có thể làm mất state cho đến khi close policy được duyệt; (3) bảo đảm modal semantics, keyboard reachability, visible focus, focus management và reduced-motion theo UI design target khi implement; (4) không thay đổi attempt state hoặc gọi API.
- **API:** không gọi API.
- **Kết quả/ngoại lệ:** destination và dismiss behavior là open decisions. Đây là yêu cầu thiết kế mục tiêu, chưa phải current runtime evidence.

### D.1. Bảng response và state mapping

| Response/tình huống | Mapping thiết kế | Điều kiện/giới hạn |
|---|---|---|
| #30 200 `DESIGN_RESOURCE_UPDATED` | Một answer write được API design chấp nhận. | Không chứng minh toàn bộ queue đã flush; không có runtime source/response field xác nhận saved count. |
| #30 401/403/404/422/500 | `flush_error` với business code tương ứng được giữ lại. | Field-level mapping/re-auth/retry chưa chốt; không gọi #31. |
| #31 200 `DESIGN_RESOURCE_UPDATED` | `submitted`, sau đó ST-16; AC-16 branch `PENDING_GRADE` hoặc `GRADED`. | Response schema/state mapping cần chốt; không hứa điểm tức thì. |
| #31 401/403/404/422/409/500 | `submit_error`/`conflict`, giữ màn hình. | Không coi 409 là thành công; copy/reconciliation/retry chưa được định nghĩa. |
| timeout/lost response #30 | `flush_ambiguous`; chặn #31. | API #30 outcome reconciliation chưa chốt. |
| timeout/lost response #31 | `ambiguous_network`. | Không auto-replay, không tự coi success; idempotency/reconciliation chưa chốt. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
