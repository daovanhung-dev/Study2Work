# AD-16 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-16-EV-001` | `Source heading` / EV-01 — Khởi tạo mode tạo (Load) | See source event detail below |
| `AD-16-EV-002` | `Source heading` / EV-02 — Khởi tạo mode chỉnh sửa (Load) | See source event detail below |
| `AD-16-EV-003` | `Source heading` / EV-03 — Thay đổi cấu hình chung (Input/Change) | See source event detail below |
| `AD-16-EV-004` | `Source heading` / EV-04 — Thêm câu hỏi (Click) | See source event detail below |
| `AD-16-EV-005` | `Source heading` / EV-05 — Lưu Quiz mới (#88) | See source event detail below |
| `AD-16-EV-006` | `Source heading` / EV-06 — Cập nhật Quiz hiện hữu (#89) | See source event detail below |
| `AD-16-EV-007` | `Source heading` / EV-07 — Hủy/quay về AD-15 (Click) | See source event detail below |
| `AD-16-EV-008` | `Source heading` / EV-08 — Safe Mode, autosave, schema và builder gate copy | See source event detail below |
| `AD-16-EV-009` | `Source heading` / EV-09 — Admin shell, breadcrumb và footer links (Click) | See source event detail below |
| `AD-16-EV-010` | `Source heading` / EV-10 — Validation, auth và API failure states | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện và xử lý dữ liệu

### EV-01 — Khởi tạo mode tạo (Load)

- **Element/kích hoạt:** Route candidate `/admin/quizzes/new`; hiện chưa có client route.
- **Đầu vào:** URL, session/auth state và permission cần có theo AC-35; form values ban đầu không nhận từ màn trước ngoài mode create.
- **Quy trình:** (1) Resolve route và mode; hiện không có router. (2) Kiểm tra Bearer/session và quiz-management permission; chưa có UI guard. (3) Nếu quyền hợp lệ, cần tải course options và defaults, nhưng không có API/source được chỉ định cho options/defaults. (4) Không gọi #87 để lấy course options trừ khi contract và mapping được duyệt. (5) Render blank config/questions như prototype chỉ làm trạng thái mẫu. (6) Chỉ enable builder/save sau khi schema/validation/permission/UI được duyệt.
- **API/output:** Không có request hiện tại. #88 chỉ chạy khi submit hợp lệ; create entry không tự POST. Destination sau create chưa xác định.
- **Ngoại lệ/trạng thái:** Loading, unauthorized, forbidden, error và empty course option chưa có UI implementation. Không thể đánh dấu create `ready` từ screenshot.

### EV-02 — Khởi tạo mode chỉnh sửa (Load)

- **Element/kích hoạt:** Candidate `/admin/quizzes/:quizId/edit`, truy cập từ action của một Quiz trong AD-15.
- **Đầu vào:** `quizId` route param. Catalog #89 khai báo `int64!`; format/positive check phía UI chưa được contract hóa.
- **Quy trình:** (1) Parse route ID theo contract đã chốt; (2) kiểm tra auth/permission; (3) cần GET admin Quiz detail để lấy config, Questions, Choices; (4) endpoint này không tồn tại. #87 list không phải detail và source local trả `questions=[]`; (5) không render dữ liệu giả, không gửi PUT, giữ edit state `blocked` và yêu cầu contract detail + question schema.
- **API/output:** Không có GET detail. #89 là mutation, không thể dùng làm read. Không tự dùng #87 để prefill.
- **Ngoại lệ/trạng thái:** Quiz missing/deleted và permission response chỉ có thể xác định sau khi có endpoint/load flow; catalog #89 404 chỉ áp dụng lúc mutation. Current screenshot không có ID/value.

### EV-03 — Thay đổi cấu hình chung (Input/Change)

- **Element:** #17–#20. Hiện không có listener, local UI state, error rendering hoặc submit path.
- **Đầu vào:** `title` text; course selector hiện chỉ có placeholder; duration optional number; passing score number. Phía server local #88/#89 fallback nhận `course_id` strict int64, `title` strict string, `duration_minutes` optional strict int/null, `passing_score` strict string. Đây là local derived request shape.
- **Quy trình:** (1) Nhận giá trị đã nhập. (2) Các native HTML `min/max` hiện hữu là hint prototype; không suy ra business validation. (3) Chưa có quy tắc normalize whitespace, required title, chọn course, decimal separator, rounding, bỏ trống duration hoặc đổi `%` thành request string. (4) Không gọi API khi field thay đổi. (5) Dirty/invalid state chưa implement; không claim autosave.
- **Kết quả/ngoại lệ:** Không có state change observable ngoài HTML control. Cần owner chốt required/range/precision, course ID source và mapping trước khi lập trình validator. Local fallback hiện kiểm tra title max 200, duration int32, score numeric fit; các checks này không xác nhận UI business policy.

### EV-04 — Thêm câu hỏi (Click)

- **Element:** #27 disabled Add Question. No event handler; không có question/choice inputs.
- **Tiền điều kiện:** Questions schema/type, editor behavior, answer-choice constraints, ordering, validation, source options và persistence semantics cần được xác nhận. Local #88 fallback shape có `questions[]`, từng item có `text`, `type`, `choices[]`, và Choice có `text`, `is_correct`.
- **Quy trình hiện tại:** (1) Browser không phát click cho disabled button. (2) Không tạo Question/Choice object. (3) Không cập nhật `questions` state/cache. (4) Không gọi API. (5) Gate/temporary-lock copy giữ nguyên.
- **Kết quả:** Empty state tiếp tục hiện. Không thể hoàn tất payload tạo/sửa; đây là blocker chính cho Save.

### EV-05 — Lưu Quiz mới (#88)

- **Element/kích hoạt:** #31 Save; disabled trong prototype, vì vậy hiện không có Submit event.
- **Tiền điều kiện expected:** Create mode; Admin session/quiz-management permission; form config và question schema hợp lệ; course option map sang ID; Save được enable theo rule đã duyệt. Các điều kiện này chưa đạt.
- **Đầu vào/candidate request:** Direct catalog quy định body top-level `{config:string!, questions:string!}`. Catalog không định nghĩa JSON fields bên trong. Local #88 fallback yêu cầu hai chuỗi JSON và nested shape trong §A.2; shape này `DERIVED`.
- **Quy trình khi có thể triển khai:** (1) Chuẩn hóa config/question input theo contract owner duyệt. (2) Validate client-side theo cùng contract; không dùng min/max prototype như business rule nếu chưa duyệt. (3) Encode `config` và `questions` thành hai string theo catalog. (4) Gửi `POST /api/v1/admin/quizzes` với Bearer JWT; không có header/idempotency key bổ sung được quy định. (5) Đọc HTTP/business code và envelope. (6) 201 `DESIGN_RESOURCE_CREATED`: nhận `Quiz` response; direct catalog schema không nêu chi tiết nested properties. Local source response dự kiến có IDs và answer keys nhưng là derived. (7) Cập nhật UI/cache hoặc điều hướng chỉ sau khi success mapping và destination được chốt; hiện chưa có chính sách. (8) Không retry tự động hoặc dedupe khi chưa có policy.
- **Lỗi:** 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR` theo catalog. Local fallback 422 khi body/nested JSON/shape/course invalid; 500/query/mapping/commit lỗi rollback sau khi đã vào transaction. Không có runtime client error view.
- **Đầu ra hiện tại:** Không gửi request; button disabled và Questions rỗng.

### EV-06 — Cập nhật Quiz hiện hữu (#89)

- **Element/kích hoạt:** #31 Save trong edit mode; disabled và edit mode không hydrate được.
- **Tiền điều kiện expected:** Edit route có ID đã xác minh, Quiz data/question set đã load, permission hợp lệ, dirty state có thay đổi và #89 body contract được phê duyệt. Hiện thiếu GET detail/body contract.
- **Đầu vào:** Direct catalog chỉ khai báo `quiz_id:int64!` trong path; không khai báo request body. Không thể xác định cập nhật config/question bằng API trực tiếp này.
- **Quy trình khi có thể triển khai:** (1) Validate ID/data theo contract đã duyệt. (2) Không gửi PUT cho tới khi body được thêm/chốt trong catalog/DD. (3) Local source fallback hiện parse positive int64 và reuse body #88; đây là `DERIVED`, không phải cách gọi được phê duyệt. (4) Local source lock quiz/child rows, kiểm tra attempt/answer history trước write, xác nhận target course, update Quiz, thay toàn bộ Choices/Questions theo request order, map response rồi commit. (5) Response local 200 mapping trả Quiz admin; giữ `status` và `created_at`. (6) UI/cache/route sau success cần owner quyết định; không tự invalidation/refetch.
- **Lỗi direct catalog:** 401/403/404/422/500 với business code tương ứng trong API catalog. Local fallback: 404 nếu Quiz không tồn tại/đã `DELETED`; 422 nếu path/body/Course invalid hoặc có attempt/answer history; 500 cho query/mapping/commit lỗi và rollback. History conflict hiện dùng HTTP 422, không phải 409.
- **Đầu ra hiện tại:** Không có edit data, body hoặc request; không có UI conflict/error state.

### EV-07 — Hủy/quay về AD-15 (Click)

- **Element:** #13 và #30; anchors trỏ `#/admin/quizzes`. #13 ở header, #30 ở footer action.
- **Đầu vào/quy trình:** (1) Browser xử lý anchor hash; HTML không khai báo router/listener. (2) Không gọi API. (3) Không có dirty-state check, draft restore hoặc query/page/filter preservation. (4) Destination AD-15 là expected handoff theo inventory, nhưng runtime chưa xác minh.
- **Kết quả/ngoại lệ:** Prototype hash đổi theo browser behavior; không khẳng định Study app render AD-15. Unsaved-change prompt và clear/preserve draft là open decision.

### EV-08 — Safe Mode, autosave, schema và builder gate copy

- **Element:** #15, #21, #23, #28. Đây là message regions, không phải action control.
- **Đầu vào/quy trình:** Không có event, API, timer, browser storage hoặc feature flag. Copy được render tĩnh từ HTML. “Autosave locally”, “schema đang chờ”, “SYSTEM NORMAL” và “Gate active” không phải server state.
- **Kết quả:** Không có dữ liệu được lưu/tải và không đổi trạng thái khi message hiển thị. Nếu cần autosave/gate, cần định nghĩa storage scope, lifecycle, recovery, schema version và security behavior trong contract riêng.

### EV-09 — Admin shell, breadcrumb và footer links (Click)

- **Element:** #2–#6, #8, #10–#12, #33–#35.
- **Đầu vào/quy trình:** Anchor/nav click. Top nav/footer dùng `href="#"`; breadcrumb phần lớn là spans; notification button không có handler. Không có route resolver, API call hoặc auth/session transition trong HTML.
- **Kết quả:** Chỉ browser fragment/default control behavior; destination thực tế không xác minh. Không suy ra route, logout, notification panel, role change hoặc help center.

### EV-10 — Validation, auth và API failure states

- **Nguồn:** API catalog #88/#89 và current local handlers; không có client runtime để map.
- **Quy trình response candidate:** (1) Nhận HTTP status + envelope/businessCode. (2) 401 yêu cầu xử lý phiên; refresh/login/redirect policy chưa được quy định. (3) 403 hiển thị access denied; detail/masking policy chưa có. (4) 422 hiển thị field/business validation theo error payload đã thống nhất; #89 local history refusal cũng là 422. (5) 404 ở #89 biểu thị Quiz không tồn tại theo catalog/local source, local source cũng trả 404 cho tombstone. (6) 500 hiển thị lỗi tổng quát/trace ID nếu contract xác nhận; không lộ SQL/body. (7) Không retry, replay hoặc giữ form/cache nếu policy chưa có.
- **Current result:** Không có loading, inline field error, auth error, API error, success toast hoặc conflict view. Trạng thái này là thiết kế candidate, chưa implement.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
