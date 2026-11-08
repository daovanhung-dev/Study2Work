# ME-14 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-14-EV-001` | `Source heading` / Quy ước xử lý | See source event detail below |
| `ME-14-EV-002` | `Source heading` / E01 — Mở/khởi tạo ME-14 | See source event detail below |
| `ME-14-EV-003` | `Source heading` / E02 — Trở lại ME-13/chọn người nhận | See source event detail below |
| `ME-14-EV-004` | `Source heading` / E03 — Nhập tiêu đề và đồng bộ preview | See source event detail below |
| `ME-14-EV-005` | `Source heading` / E04 — Thay đổi channel | See source event detail below |
| `ME-14-EV-006` | `Source heading` / E05 — Nhấn các nút formatting/link | See source event detail below |
| `ME-14-EV-007` | `Source heading` / E06 — Nhập nội dung và đồng bộ preview/word count | See source event detail below |
| `ME-14-EV-008` | `Source heading` / E07 — Chọn tệp đính kèm | See source event detail below |
| `ME-14-EV-009` | `Source heading` / E08 — Lưu bản nháp | See source event detail below |
| `ME-14-EV-010` | `Source heading` / E09 — Gửi thông báo (API #63 conditional; nút hiện bị disable) | See source event detail below |
| `ME-14-EV-011` | `Source heading` / E10 — Header navigation/breadcrumb | See source event detail below |
| `ME-14-EV-012` | `Source heading` / E11 — Bell/profile | See source event detail below |
| `ME-14-EV-013` | `Source heading` / E12 — Help và footer links | See source event detail below |
| `ME-14-EV-014` | `Source heading` / E13 — Stepper | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

### Quy ước xử lý

- Những event chỉ mô tả HTML prototype không được diễn giải thành frontend runtime requirement.
- API #63 behaviors dưới đây là đối chiếu current local source, không phải lời khẳng định Study Web hiện gọi API.
- Không tạo payload cho các field chưa có mapping được phê duyệt. Với thao tác bị chặn, đầu ra hiện tại là không mutation và không request.

### E01 — Mở/khởi tạo ME-14

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Truy cập route dự kiến `/mentor/notifications/new`; role Mentor dự kiến. | Kiểm tra source hiện tại: không có route/auth guard Study Web để chạy. | Runtime navigation/auth `UNWIRED`; đây không phải request thất bại có response code. |
| 2 | HTML khởi tạo không có query/state payload. | Dùng giá trị literal trong DOM: recipients chưa xác thực; title/body rỗng; In-app checked; Email disabled. Không gọi #62/#63. | Render prototype initial state; preview title/body placeholder; send disabled. |
| 3 | Refresh hoặc mở lại trang tĩnh. | Không đọc browser storage hoặc backend. | Các field trở về initial HTML; không có draft restore. |

### E02 — Trở lại ME-13/chọn người nhận

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click CTA #20 hoặc back action #44. | HTML chỉ có anchor với `href="#"` và `data-path="khoa-hoc-phu-trach"`; không có router handler. | Không có điều hướng ME-13 được xác minh. |
| 2 | Khi thiết kế route được nối trong tương lai. | Chủ contract phải quyết định giữ course + unique Student int64 IDs và draft title/body bằng carrier được duyệt. Không dùng query/local/session storage theo suy đoán. | Chưa có output/state preservation contract. |

### E03 — Nhập tiêu đề và đồng bộ preview

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | `input` trên `#announcement-title`; chuỗi text; browser giới hạn `maxlength=120`. | Script đọc raw `this.value`; cập nhật counter bằng `value.length + ' / 120 ký tự'`. | Counter đếm raw code units theo JS string length; không tính grapheme cluster. |
| 2 | Cùng event. | Script tính `trim()` để chọn preview placeholder hoặc user text; set `textContent`. | Preview không render HTML; chuỗi chỉ có whitespace trở về placeholder. |
| 3 | Thử gửi khi tích hợp chưa được nối. | Không submit vì Send disabled; không có local required validation. | Không request/lỗi UI. |
| 4 | Đối chiếu API nếu sau này submit. | #63 yêu cầu title string tối đa 200 theo model; prototype UI tối đa 120. Không có bằng chứng chọn 120 hay 200 làm canonical bound. | **BLOCKER:** cần quyết định bounds và required/nonblank rule; không suy ra từ dấu `*`. |

### E04 — Thay đổi channel

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Checkbox In-app #29 ban đầu checked; Email #30 ban đầu disabled. | HTML không gắn listener; selection state không được serialize. | Không đổi preview badge hoặc backend state. |
| 2 | Nếu Email được mở trong bản tương lai. | #63 nhận CSV token chính xác `PUSH`/`EMAIL`; channel parse loại token lạ, bỏ duplicate theo thứ tự. | Mapping In-app→PUSH chưa approved; worker/provider gửi chưa wired. |
| 3 | Không có channel nào hoặc CSV rỗng/không hợp lệ trong request #63. | API model/handler trả 422 `DESIGN_VALIDATION_ERROR` (một số lỗi JSON/schema xảy ra trước handler). | Hiện tại ME-14 không hiển thị lỗi vì không gọi API. |

### E05 — Nhấn các nút formatting/link

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click toolbar #32–#35 (`type=button`). | Không có `addEventListener`, `onclick`, editor library hoặc command handler. | Không thay đổi selection/body/preview; không có lỗi/request. |
| 2 | Tích hợp editor trong tương lai. | Cần xác định rich-text format, link safety, persistence representation và tương thích với #63 `content:int64`. | **BLOCKER:** không tự tạo HTML/Markdown/attachment URL representation. |

### E06 — Nhập nội dung và đồng bộ preview/word count

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | `input` trên `#announcement-body`; chuỗi text không có giới hạn HTML. | Script trim chuỗi cho preview; nếu rỗng/whitespace, hiển thị placeholder. | Không có max length hoặc min/nonblank validator. |
| 2 | Cùng event. | Đếm `trimmed.split(/\s+/).filter(Boolean).length`; hiển thị số từ. | Counter đúng là số từ; `id="body-char-count"` không biến nó thành character count. |
| 3 | Cùng event. | Cập nhật preview bằng `textContent`. | Không diễn giải markup/toolbar; input hiển thị như text. |
| 4 | Tạo request #63 theo source hiện tại. | `content` là signed int64 bắt buộc, không phải free-form body. | **BLOCKER:** không stringify/cast body sang ID; cần canonical content schema/API. |

### E07 — Chọn tệp đính kèm

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click #41. | Không có `<input type="file">`, `change` event, form, request hoặc selected-file list. | Không mở file picker được xác minh; không có upload state. |
| 2 | So khớp copy prototype với #34. | #34 yêu cầu multipart `file`, `purpose`, tùy/đòi `course_id`; purpose chỉ `SUBMISSION`/`LECTURE`. API nhận bất kỳ MIME/size hiện tại nhưng không có purpose notification. | #34 không tạo quan hệ attachment để #63 tiêu thụ; không thể dùng #34 để đáp ứng card này. |
| 3 | Nếu triển khai trong tương lai. | Phải duyệt purpose/ownership/course scope, giới hạn type/size, storage, attachment ID contract và cách #63 lưu/đính. | **BLOCKER:** không triển khai theo copy PDF/DOCX/ZIP ≤25 MB như thể đó là API behavior. |

### E08 — Lưu bản nháp

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click #45; button hiện enabled. | Không có click handler, API draft, DB mapping hay local persistence. | Không save; DOM giữ nội dung cho đến refresh/đóng tab. |
| 2 | Yêu cầu draft functionality. | Cần xác định nơi lưu, quyền truy cập, retention, attachment lifecycle, restore/edit route và trạng thái. | **BLOCKER:** chưa thể xác định success/error/loading state. |

### E09 — Gửi thông báo (API #63 conditional; nút hiện bị disable)

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click #46 trong prototype. | Native `disabled` + `aria-disabled=true`; click không kích hoạt submit. Không có `<form>`. | Không gọi API; không có local success/error. |
| 2 | Trước tích hợp future flow. | Cần Mentor auth, selected unique Student IDs int64, course binding, title rule, content representation, approved channels, attachment policy, duplicate/retry policy. | **BLOCKER:** payload hiện không thể được tạo đủ chính xác. |
| 3 | Khi body #63 parse được. | Contract body: `recipients:string` CSV positive Student int64 IDs; `title:string` max 200; `content:int64`; `channels:string` CSV `PUSH`/`EMAIL`; strict extra fields forbidden. API không nhận course_id/file/Idempotency-Key. | Duplicate recipient/channel được dedupe trong source; recipients phải cùng nằm trong ít nhất một ACTIVE roster của course do Mentor trực tiếp sở hữu. Điều kiện common-course là local `DERIVED`. |
| 4 | Request validation và auth. | Pydantic/FastAPI parsing có thể trả 422 trước handler. Với schema-valid body, Mentor Bearer guard runs first; sau đó parse CSV/scope checks. | 401 `DESIGN_AUTHENTICATION_REQUIRED`; 403 `DESIGN_ACCESS_DENIED`; 422 `DESIGN_VALIDATION_ERROR`. |
| 5 | DB transaction. | Insert notification row cho mỗi recipient (`title`, content lưu dạng decimal string theo source, sender, shared Operation UUID, unread false); insert delivery row `QUEUED` theo từng channel. Response validate trước commit. | DB dependency unavailable 503 `DESIGN_DEPENDENCY_UNAVAILABLE`; projection/other error 500 `DESIGN_INTERNAL_ERROR`; rollback. Không có 202 trước commit. |
| 6 | Thành công. | Return `success=true`, `businessCode=DESIGN_OPERATION_ACCEPTED`, HTTP 202; `data` là Operation projection gồm UUID `id`, kind `NOTIFICATION_DISPATCH`, status `QUEUED`, owner/timestamps; `meta.notification_ids` là int64 IDs theo recipient order. | “Accepted/queued”, chưa chứng minh delivered. Mapping/projection và contract còn Draft/DERIVED. |
| 7 | Handoff trạng thái sau accept. | Nếu cần status, API #64 path là `/api/v1/mentor/notifications/{notification_id}/status` với từng notification ID int64. #18 không có route, ID/lifecycle unresolved, và không nằm trên AC-25 edge. | Không thay `notification_id` bằng `data.id`; worker/provider chưa wired nên queued có thể tiếp tục tồn tại. |
| 8 | Retry sau timeout. | #63 không nhận idempotency key. | Có duplicate batch risk; retry UX/policy cần quyết định; không tự retry. |

### E10 — Header navigation/breadcrumb

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click link #1–#6, #9–#10. | `href="#"`; `data-path` không có router listener. | Route/permission/active state không được resolve. |
| 2 | Tích hợp sau này. | Dùng route registry hiện hành và role guard đã được phê duyệt; định nghĩa destination cho từng anchor. | Không suy ra route chỉ từ `data-path`. |

### E11 — Bell/profile

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click bell #7. | Anchor `href="#"`; unread dot tĩnh. | Không mở notification list; không có read-state update. |
| 2 | Profile #8. | Là `div` hiển thị, không có action/handler. | Không có navigation/menu. |

### E12 — Help và footer links

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click #63 hoặc #66–#68. | Các anchor đều `href="#"`; không có destination/handler. | Không mở tài liệu/trang hỗ trợ. |

### E13 — Stepper

| Bước | Input/điều kiện | Xử lý | Output/lỗi |
|---:|---|---|---|
| 1 | Click Bước 1/2/3 (#12–#14). | Các phần tử là display `div`, không có role/button/listener. | Không đổi bước hoặc state. Chỉ CTA #20/#44 được gắn nhãn quay lại ME-13, nhưng cũng chưa có router. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
