# ST-24 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ST-24-EV-001` | `ST24-EV-01` / ST24-EV-01 — Mở ST-24 và xác lập Student context | See source event detail below |
| `ST-24-EV-002` | `ST24-EV-02` / ST24-EV-02 — Chọn course liên quan | See source event detail below |
| `ST-24-EV-003` | `ST24-EV-03` / ST24-EV-03 — Chọn module/bài học liên quan | See source event detail below |
| `ST-24-EV-004` | `ST24-EV-04` / ST24-EV-04 — Nhập title và hiển thị counter | See source event detail below |
| `ST-24-EV-005` | `ST24-EV-05` / ST24-EV-05 — Thêm/xóa tag | See source event detail below |
| `ST-24-EV-006` | `ST24-EV-06` / ST24-EV-06 — Soạn nội dung và dùng formatting controls | See source event detail below |
| `ST-24-EV-007` | `ST24-EV-07` / ST24-EV-07 — Chuyển Soạn thảo / Xem trước | See source event detail below |
| `ST-24-EV-008` | `ST24-EV-08` / ST24-EV-08 — Ảnh chụp log / đính kèm | See source event detail below |
| `ST-24-EV-009` | `ST24-EV-09` / ST24-EV-09 — Tạo topic mới (expected, trigger chưa có) | See source event detail below |
| `ST-24-EV-010` | `ST24-EV-10` / ST24-EV-10 — Quay lại ST-23 và header navigation | See source event detail below |
| `ST-24-EV-011` | `ST24-EV-11` / ST24-EV-11 — Validation/auth/API/transport errors | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

### ST24-EV-01 — Mở ST-24 và xác lập Student context

- **Trigger / loại:** Route entry / Load; không có marker vì route entry là page lifecycle.
- **Điều kiện:** Expected actor Student; AC-19 yêu cầu đăng nhập và quyền discussion course.
- **Input:** URL route `/student/discussions/new`; session/token từ shared auth nếu sau này được wire; course context từ màn trước chỉ khi caller contract xác định. Inventory không định nghĩa query/path transfer.
- **Xử lý:** (1) router hiện không tồn tại nên không có route resolve thực tế; (2) khi triển khai, dùng auth/session boundary được phê duyệt; (3) không lấy danh tính từ screenshot/profile text; (4) không tự redirect/return-to URL.
- **API:** Chưa có request load API được khai báo cho page initialization. #39 là list API, không phải course options API.
- **Output:** Hiện không có route transition runtime. Expected page state/data chưa khởi tạo được.
- **Ngoại lệ:** Missing/expired session và access-denied UX chưa có mapping riêng ngoài API catalog #40 401/403 ở lúc submit.

### ST24-EV-02 — Chọn course liên quan

- **Trigger / loại:** Change/select trên ST24-EL-15.
- **Điều kiện:** Course options phải là course Student được phép tham gia; source/options contract chưa được tìm thấy.
- **Input:** Giá trị dự kiến `course_id:int64`; source hiện tại trên screenshot chỉ là sample course label, không có numeric ID.
- **Xử lý:** (1) không suy `course_id` từ course title; (2) xác định API/state source và access predicate trước khi triển khai selector; (3) chỉ gửi body field `course_id` theo catalog #40; (4) không thêm course ID vào URL/query nếu chưa có contract.
- **API:** Không có options API được xác định trong ST-24 inventory/AC-19. #39 chỉ liệt kê discussion items.
- **Output:** Current artifact không có selectable data. Expected valid selection sẽ tạo giá trị candidate cho #40 sau khi mapping được duyệt.
- **Ngoại lệ:** Empty options, invalid ID, unenrolled course và course not found chưa có endpoint/field/error policy. Không tự thêm 404 hoặc 422 condition.

### ST24-EV-03 — Chọn module/bài học liên quan

- **Trigger / loại:** Change/select trên ST24-EL-16.
- **Điều kiện:** Ý nghĩa của selector/context và nguồn option phải được product/API xác nhận.
- **Input:** Static lesson label trong ảnh; API #40 không có `lesson_id` hoặc module field.
- **Xử lý:** (1) giữ selector ở mức visual evidence; (2) không dùng sample value làm default; (3) không gửi field ngoài `course_id/title/content`; (4) không lọc/hydrate theo endpoint không được chỉ định.
- **API:** Không gọi API đã xác định.
- **Output:** Không có current state transition hoặc persisted mapping.
- **Ngoại lệ:** Course đổi nhưng lesson selection reset/preserve thế nào chưa được định nghĩa.

### ST24-EV-04 — Nhập title và hiển thị counter

- **Trigger / loại:** Input/change trên ST24-EL-17; counter hiển thị ở ST24-EL-18.
- **Điều kiện:** Expected title là required string theo API catalog.
- **Input:** User text `title:string`; ảnh hiện text sample và `74/150 ký tự`.
- **Xử lý:** (1) nhận text; (2) catalog chỉ định required/type, không có max/min/blank/trim/normalization; (3) không chốt 150 là max chỉ từ counter; (4) không tạo server request trong lúc gõ; (5) counter behavior/Unicode grapheme counting chưa có source.
- **API:** Không gọi API khi typing. #40 body sẽ có `title` khi create contract được resolve.
- **Output:** Current screenshot là static sample, không có data binding; expected draft title và count chưa có runtime behavior.
- **Ngoại lệ:** Field-specific error copy, max-length handling, IME/Unicode count và unsaved draft retention chưa được định nghĩa.

### ST24-EV-05 — Thêm/xóa tag

- **Trigger / loại:** Enter trong ST24-EL-20 hoặc remove icon trên ST24-EL-19 (visual affordance; handler chưa có).
- **Điều kiện:** Tag vocabulary/semantics cần được xác nhận trước khi coi tag là dữ liệu.
- **Input:** Tag text và chip values sample; screenshot có năm selected labels và gợi ý tĩnh.
- **Xử lý:** (1) không suy add/remove, duplicate, case normalization hay suggestion-selection algorithm; (2) API #40 không khai báo `tags`; (3) không tự lưu vào `content` hoặc metadata.
- **API:** Không có tags API/request field trong catalog #40.
- **Output:** Current HTML không có tag control; screenshot chỉ thể hiện visual sample.
- **Ngoại lệ:** Empty/duplicate/unknown tag, chip limits và keyboard focus policy chưa được đặc tả.

### ST24-EV-06 — Soạn nội dung và dùng formatting controls

- **Trigger / loại:** Input/change trong ST24-EL-26; click toolbar children của ST24-EL-25.
- **Điều kiện:** User ở compose mode theo ảnh mẫu; current HTML không có editor.
- **Input:** User-authored multiline text/Markdown, selection/caret, formatting action. Screenshot body không phải source input thật.
- **Xử lý:** (1) editor value về mặt UI là text; (2) không tự xác định Markdown serialization, HTML sanitization, code fence, URL normalization, toolbar insertion rules hoặc GFM subset; (3) không autosave vì F07 không cho phép mutation này; (4) không convert nội dung sang integer.
- **API:** #40 yêu cầu `content:int64!`; request không tương thích trực tiếp với editor text. Không gọi API, cast, encode, truncate hoặc gắn file reference.
- **Output:** Chỉ có screenshot sample, không có current draft model/parser/persistence. Các formatting buttons trong ảnh không có HTML implementation.
- **Ngoại lệ:** Unsupported markup, malformed HTML, XSS/sanitization, content length và draft recovery policy đều chưa có contract.

### ST24-EV-07 — Chuyển Soạn thảo / Xem trước

- **Trigger / loại:** Click ST24-EL-23 hoặc ST24-EL-24.
- **Điều kiện:** Preview mode cần renderer và security/content policy được xác định.
- **Input:** Editor text và current tab state; current state không được giữ bởi code.html.
- **Xử lý:** (1) không suy preview output từ static screenshot; (2) không đổi/persist text khi đổi tab theo giả định; (3) xác định GFM subset, HTML escaping/sanitization và state preservation trước implementation.
- **API:** Không cần API theo visual; không có handler để chứng minh.
- **Output:** Screenshot đánh dấu “Soạn thảo” active; preview behavior chưa được thiết kế/verified.
- **Ngoại lệ:** Render failure, invalid markup và focus restoration chưa được xác định.

### ST24-EV-08 — Ảnh chụp log / đính kèm

- **Trigger / loại:** Click toolbar child “Ảnh chụp log” trong ST24-EL-25.
- **Điều kiện:** Không có upload contract hoặc event mapping cho AC-19.
- **Input:** Screenshot chỉ cho thấy label/icon; không có file bytes, accept type, limit, attachment ID hay reference.
- **Xử lý:** (1) không mở file picker behavior như current runtime; (2) không gọi API #34 vì đây là upload flow khác và chưa có mapping vào discussion; (3) không nhúng file hay URL vào body theo suy đoán.
- **API:** Chưa xác định.
- **Output:** Không có uploaded state/progress/list trong ảnh.
- **Ngoại lệ:** MIME, size, network, retry, orphan cleanup và permission chưa có source.

### ST24-EV-09 — Tạo topic mới (expected, trigger chưa có)

- **Trigger / loại:** Submit/create dự kiến; **không có button/form submit trigger trong screenshot hoặc current HTML**.
- **Điều kiện:** Student đã đăng nhập và course participation được xác nhận; title/body hợp lệ theo contract đã duyệt; UI cần có CTA được approve.
- **Input:** Catalog body đúng kiểu `{course_id:int64, title:string, content:int64}`. UI editor cung cấp text, chưa map được sang `content:int64`; course/title/data options cũng chưa hoàn thiện.
- **Xử lý:** (1) không thêm CTA hay gọi API ở trạng thái hiện tại; (2) khi blockers được giải quyết, kiểm tra required fields/type theo contract; (3) dùng Student Bearer; (4) chỉ khi có implementation được duyệt mới POST `/api/v1/discussions`; (5) chờ HTTP 201 `DESIGN_RESOURCE_CREATED`; (6) response `ApiEnvelope<Page<Discussion>>` có title/author/comments/Page mapping chưa được chốt; (7) inventory kỳ vọng về ST-23 và refresh #39 nhưng redirect-versus-fetch sequence chưa xác định.
- **API:** #40 catalog là design declaration, runtime `NOT_FOUND`. Không có path/query; request fields ở trên; `meta`/`traceId` theo API guidelines. Không có retry/idempotency/double-submit policy được nguồn hóa.
- **Output:** Expected topic creation and list refresh only after contract/runtime implementation. Current screen cannot submit; no persisted data or next state verified.
- **Ngoại lệ:** 401, 403, 422, 500 đúng catalog. Không thêm 404/409. Transport/timeout/parse failure không phải business code; rollback/partial transaction và safe retry chưa xác định.

### ST24-EV-10 — Quay lại ST-23 và header navigation

- **Trigger / loại:** Click breadcrumb, forum nav hoặc HTML fallback link.
- **Điều kiện:** Route `/student/discussions` cần được đăng ký trong Study Web.
- **Input:** Prototype href; HTML unavailable state có back link `/student/discussions`. Không có course ID, return URL hoặc saved draft contract.
- **Xử lý:** (1) treat `#` anchors là placeholder; (2) inventory nối ST-23 ↔ ST-24; (3) không tự thêm unsaved-changes modal, query state hoặc browser back policy; (4) sau success, refresh #39 như inventory kỳ vọng chỉ sau khi sequence được duyệt.
- **API:** Không có API trên navigation event. API #39 refresh sau create là expected inventory step riêng, hiện chưa runnable.
- **Output:** Static destination string only; actual route transition chưa verify.
- **Ngoại lệ:** Missing route, expired session, unsaved form và direct-entry behavior chưa có Study Web policy.

### ST24-EV-11 — Validation/auth/API/transport errors

- **Trigger / loại:** Local form validation hoặc response/transport failure trong EV-09 (nếu event được triển khai).
- **Điều kiện:** Chỉ phát sinh khi có form/API implementation; catalog #40 là declaration, hiện chưa có Student route hoặc request execution.
- **Input:** Required/type fields theo catalog; 401/403/422/500 catalog responses; transport/timeout/parse error.
- **Xử lý:** (1) giữ auth failure, access denial, validation, server và transport states riêng; (2) không map lỗi thành `created` hoặc form-unavailable empty state; (3) không thêm title max=150, tag/upload errors hay course-not-found codes; (4) không retry, rollback hay preserve-draft theo giả định; (5) error UI/copy/action cần design.
- **API:** Chỉ catalog #40: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 422 `DESIGN_VALIDATION_ERROR`, 500 `DESIGN_INTERNAL_ERROR`; 201 là success. #40 DD không khai báo 404/409/503.
- **Output:** Expected `invalid`/`error` state theo inventory, nhưng UI hiện không có feedback. No runtime state transition verified.
- **Ngoại lệ:** Field-level validation mapping, transaction rollback, duplicate submit, abort/unmount và retry policy là open decisions.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
