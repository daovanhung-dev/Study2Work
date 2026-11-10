# ME-09 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-09-EV-001` | `ME09-E01` / ME09-E01 — Vào màn hình / tải danh sách | See source event detail below |
| `ME-09-EV-002` | `ME09-E02` / ME09-E02 — Đổi bộ lọc khóa học | See source event detail below |
| `ME-09-EV-003` | `ME09-E03` / ME09-E03 — Đổi trạng thái bài nộp | See source event detail below |
| `ME-09-EV-004` | `ME09-E04` / ME09-E04 — Nhập từ khóa bài tập | See source event detail below |
| `ME-09-EV-005` | `ME09-E05` / ME09-E05 — Reset bộ lọc | See source event detail below |
| `ME-09-EV-006` | `ME09-E06` / ME09-E06 — Tải lại danh sách | See source event detail below |
| `ME-09-EV-007` | `ME09-E07` / ME09-E07 — Chọn một submission để mở ME-10 | See source event detail below |
| `ME-09-EV-008` | `ME09-E08` / ME09-E08 — Header links, bell và avatar | See source event detail below |
| `ME-09-EV-009` | `ME09-E09` / ME09-E09 — Footer/policy/support links | See source event detail below |
| `ME-09-EV-010` | `Source heading` / D.1. Error/business code mapping cho #54 | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### ME09-E01 — Vào màn hình / tải danh sách

- **Element:** route ME-09; trigger `Load`.
- **Tiền điều kiện:** user có session/token hợp lệ và MENTOR role; UI token/session source chưa có trong checkout.
- **Input:** optional `course_id:int64`, `status:string`, `page:int32`; API defaults `course_id=null`, `status=null`, `page=1`. Page size server 20.
- **Xử lý dự kiến:**
  1. Đọc route và auth state theo implementation contract sẽ được phê duyệt; không lấy profile mẫu từ HTML.
  2. Chỉ dựng query từ field #54 đã hỗ trợ; không gửi `q`, `size`, sort hoặc UI value chưa map.
  3. Gọi `GET /api/v1/mentor/submissions` với `Authorization: Bearer ...`.
  4. Nhận response, kiểm tra HTTP status, `success`, `businessCode` và shape `data.items/data.pagination` theo current source.
  5. `items=[]` → empty state; non-empty → loaded state cần row layout được duyệt; không suy deadline/owner/title.
  6. Lỗi → state tương ứng; API error phải giữ `traceId` cho hỗ trợ, không hiển thị raw SQL.
- **Output:** loading → empty/ready/error/auth/access/validation. Request lifecycle và UI mapping chưa chạy trong app.
- **Current source:** #54 GET source-backed, screen event UNWIRED.

### ME09-E02 — Đổi bộ lọc khóa học

- **Element:** `ME09-EL-13`; trigger `Change`.
- **Input hiện tại:** values `all`, `fe`, `be`, `ux` (string sample).
- **Xử lý:**
  1. Không gửi value dạng `fe/be/ux` vào `course_id`; route chỉ nhận positive int64.
  2. Khi có contract options/default, chuyển selected course ID thành query numeric `course_id`; “all” tương ứng không truyền filter chỉ khi đây là default được duyệt.
  3. Reset page về 1 là lựa chọn thiết kế hợp lý nhưng chưa có màn hình/API contract xác nhận; phải được khóa cùng filter semantics.
  4. Gọi lại #54 sau khi được duyệt; render kết quả/empty/error theo response.
- **Output hiện tại:** chỉ thay đổi local selected value nếu dùng HTML prototype; không tải danh sách. Nguồn danh sách course option không xác định trong orchestration ME-09.

### ME09-E03 — Đổi trạng thái bài nộp

- **Element:** `ME09-EL-14`; trigger `Change`.
- **Input hiện tại:** `pending`, `graded`, `recheck`.
- **Xử lý:** #54 so sánh `status` exact, không trim/lowercase và không xác thực enum. Không đổi tự động thành `SUBMITTED`/`GRADED` khi chưa có mapping approved. Khi mapping và defaults được duyệt, truyền giá trị server chính xác và yêu cầu lại trang 1 theo quyết định paging.
- **Output:** chỉ data trả từ #54; unknown string có thể tạo empty page thay vì validation error. Không kết luận “recheck” là source status.

### ME09-E04 — Nhập từ khóa bài tập

- **Element:** `ME09-EL-15`; trigger `Input`/`Submit` nếu sản phẩm xác nhận.
- **Input:** free text từ người dùng; HTML không có max length, normalization, debounce hay submit event.
- **Xử lý hiện hành:** không có API #54 query key hoặc event handler để tìm theo tên/mã bài. Không gửi query tùy tạo; không lọc client-side trên Page 20 vì response không có assignment title.
- **Output:** ở prototype chỉ thay đổi input text. Cần product/API decision để bỏ, disable hoặc định nghĩa search contract.

### ME09-E05 — Reset bộ lọc

- **Element:** `ME09-EL-16`; trigger `Click`.
- **Input:** state course/status/search hiện tại.
- **Xử lý hiện hành:** đặt course=`all`, status=`pending`, search=`""`; không reset page, không gọi #54 và không phản hồi kết quả.
- **Output:** control value thay đổi local. Default “pending” chưa phù hợp chắc chắn với API hiện không có enum; không dùng làm canonical state khi chưa được duyệt.

### ME09-E06 — Tải lại danh sách

- **Element:** `ME09-EL-20`; trigger `Click`.
- **Input:** current filters/page/auth state; exact default retention behavior chưa được xác định.
- **Xử lý hiện hành:** icon quay và button disable 750 ms rồi enable; không fetch, cancel request cũ, chặn double request hay kiểm tra response.
- **Xử lý cần duyệt:** gọi lại #54 với filter/page được giữ; khi request còn chạy thì hiển thị loading/disabled; success cập nhật list và pagination; error giữ/khôi phục dữ liệu cũ hay thay bằng error state cần quyết định. Không auto-refresh theo badge nếu không có polling contract.

### ME09-E07 — Chọn một submission để mở ME-10

- **Element dự kiến:** row/action trong loaded list; element này không hiện trong PNG/HTML nên chưa có marker.
- **Input hiện hành:** #54 item `id:int64`; inventory gọi logical ID là `submission_id`.
- **Xử lý dự kiến:**
  1. User chọn đúng một row sau khi row layout và keyboard action được duyệt.
  2. Lấy `data.items[].id`, không dùng `assignment_id` hoặc `user_id`.
  3. Mở proposed route `/mentor/submissions/{id}` để ME-10 gọi #55.
  4. #54 item không phải detail; không truyền score/feedback/sample data làm trusted detail.
- **Output:** handoff sang ME-10; không gọi #55/#56/#57 trực tiếp từ ME-09. Route/handoff chưa được frontend xác minh.

### ME09-E08 — Header links, bell và avatar

- **Elements:** `ME09-EL-01`–`ME09-EL-08`.
- **Trigger/input:** click/tap/keyboard activation; HTML anchors `href="#"`, sample Mentor identity và notifications state.
- **Xử lý/output:** HTML không cung cấp route destination, menu, logout, unread API hoặc identity hydration. Không điều hướng suy từ `data-path`; không khẳng định app header dùng cùng nav route với API.

### ME09-E09 — Footer/policy/support links

- **Elements:** `ME09-EL-21`–`ME09-EL-27`.
- **Trigger/input:** click/tap/keyboard activation trên các link; ba claim strip là text/icon tĩnh.
- **Xử lý/output:** ba footer anchors đều `href="#"`. Claim 48 giờ, rubric và liên hệ Ban Đào tạo không kích hoạt API trong HTML; đích policy/support chưa được xác định. Không mô tả là điều khoản hệ thống đang áp dụng.

### D.1. Error/business code mapping cho #54

| HTTP | Current API behavior | Xử lý màn hình yêu cầu sau khi UI contract được duyệt |
|---:|---|---|
| 200 | `DESIGN_RESOURCE_RETRIEVED`; có items hoặc Page rỗng. | Empty/ready theo `items.length`, không dựa vào message text. |
| 401 | Bearer/token/claims không hợp lệ hoặc thiếu. | Hiển thị yêu cầu đăng nhập/hết phiên theo auth policy; policy/route chưa được source-backed. |
| 403 | Role không phải MENTOR hoặc course filter trỏ tới owner khác. | Hiển thị quyền bị từ chối, không lặp lại request vô hạn. |
| 422 | `course_id`/`page` sai range hoặc request query invalid theo route constraints. | Map field/query error; status string hiện không có enum validation. |
| 409 | Có khai báo trong catalog/AC node cũ nhưng không có nhánh 409 trong current view. | Không tạo UI conflict behavior cho #54 đến khi có trigger/business rule. |
| 500 | SQL/projection failure → `DESIGN_INTERNAL_ERROR`. | Hiển thị lỗi an toàn và giữ trace ID; retry policy/chính sách giữ dữ liệu cũ cần quyết định. |
| Network/timeout | Không phải business code; chưa có client source. | Chưa xác định timeout, cancel, retry hoặc stale data behavior. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
