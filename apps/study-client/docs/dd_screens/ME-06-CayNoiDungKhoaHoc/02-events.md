# ME-06 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-06-EV-001` | `ME06-EV-01` / ME06-EV-01 — Mở màn hình và GET #49 | See source event detail below |
| `ME-06-EV-002` | `ME06-EV-02` / ME06-EV-02 — Dựng tree và giữ trạng thái | See source event detail below |
| `ME-06-EV-003` | `ME06-EV-03` / ME06-EV-03 — Lọc status | See source event detail below |
| `ME-06-EV-004` | `ME06-EV-04` / ME06-EV-04 — Tìm kiếm nội dung | See source event detail below |
| `ME-06-EV-005` | `ME06-EV-05` / ME06-EV-05 — Expand/collapse tree | See source event detail below |
| `ME-06-EV-006` | `ME06-EV-06` / ME06-EV-06 — Sắp xếp và lưu thứ tự | See source event detail below |
| `ME-06-EV-007` | `ME06-EV-07` / ME06-EV-07 — Thêm Chapter/root Content | See source event detail below |
| `ME-06-EV-008` | `ME06-EV-08` / ME06-EV-08 — Thêm nội dung con / liên kết ME-04 | See source event detail below |
| `ME-06-EV-009` | `ME06-EV-09` / ME06-EV-09 — Mở chi tiết qua ME-05 | See source event detail below |
| `ME-06-EV-010` | `ME06-EV-10` / ME06-EV-10 — Mở editor/sửa Content qua ME-07/#51 | See source event detail below |
| `ME-06-EV-011` | `ME06-EV-11` / ME06-EV-11 — Rubric/configuration/question bank | See source event detail below |
| `ME-06-EV-012` | `ME06-EV-12` / ME06-EV-12 — Thể hiện trạng thái nháp | See source event detail below |
| `ME-06-EV-013` | `ME06-EV-13` / ME06-EV-13 — Publish/unpublish qua ME-08/#52 | See source event detail below |
| `ME-06-EV-014` | `ME06-EV-14` / ME06-EV-14 — Xóa Content qua ME-08/#53 | See source event detail below |
| `ME-06-EV-015` | `ME06-EV-15` / ME06-EV-15 — Header/footer shell actions | See source event detail below |
| `ME-06-EV-016` | `ME06-EV-16` / ME06-EV-16 — Breadcrumb và handbook | See source event detail below |
| `ME-06-EV-017` | `ME06-EV-17` / ME06-EV-17 — Quality/audit panels và “xem toàn bộ” | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 5. Event specification

Các kết quả dưới đây mô tả current API source hoặc expected behavior có điều kiện; không event nào được runtime verified trên Study Web.

### ME06-EV-01 — Mở màn hình và GET #49

- **Trigger:** mở route đề xuất `/mentor/courses/:courseId/content`.
- **Điều kiện:** có numeric signed-int64 `courseId`; người dùng có Bearer token và role MENTOR. Client route/auth chưa được wire.
- **Request:** GET `/api/v1/mentor/courses/{course_id}/content`, không body/query.
- **Xử lý source:** auth/role trước; parse path; truy vấn course và direct-owner; đọc tất cả active Content; xác thực mapping/cây.
- **Thành công:** 200 `DESIGN_RESOURCE_RETRIEVED`, `data:Content[]`. Không mutation; không có cache rule/client retry source.
- **Lỗi:** 401 auth; 403 role/owner; 404 path sai hoặc course thiếu; 500 SQL/projection/tree integrity, safe message + rollback. Path sai hiện không tạo 422.
- **Đầu ra:** loading → empty khi `data=[]`, ready khi có nodes. No partial tree response.
- **Evidence:** route/view/query/model/local focused test source đã được đọc; test không chạy; live schema/deployment không xác minh.

### ME06-EV-02 — Dựng tree và giữ trạng thái

- **Trigger/input:** envelope thành công của EV-01.
- **Processing:** giữ từng `id/course_id/content_type/title/payload/status/parent_id/order`; lập lookup theo `id`; nối `parent_id`; siblings dùng `order` đã trả (API SQL đã order `id` tie-break). Không thêm nested field vào response model và không chọn version.
- **Status:** giữ đúng giá trị server. Không map `PENDING_REVIEW` thành “Draft”, `APPROVED` thành “Ready”, hoặc hide `PUBLISHED`/`hidden` trước khi enum/lifecycle được duyệt. Không render một node draft dưới badge published từ fixture.
- **Output/error:** empty tree là 200 rỗng, không lỗi; type/status/payload không nhận diện vẫn cần hiển thị an toàn hoặc chặn cho tới khi schema được chốt. UI fallback, retry, cache invalidation chưa có implementation.

### ME06-EV-03 — Lọc status

- **Trigger:** chọn tab `all/published/draft/hidden` (#17).
- **Current mockup:** lọc các `.lesson-row` theo lowercase `data-status`, ẩn các row không khớp; status sample hardcoded.
- **Expected safe behavior:** lọc client-side trên response đã load sau khi approved enum-to-tab mapping tồn tại. Không gọi API khác; không sửa status. Cần xác nhận nhóm “hidden” có status source nào.
- **Gap:** current API strings/status transitions dùng open/uppercase values; mapping chưa được contract xác nhận. Filter và search handlers độc lập có thể ghi đè DOM state.

### ME06-EV-04 — Tìm kiếm nội dung

- **Trigger:** nhập/clear query tại #18.
- **Current mockup:** lowercase/trim query rồi so với `row.innerText`; chỉ set `display:flex/none`.
- **Expected:** search visible tree labels sau khi response load; không gửi query tới #49 (API không nhận query). Cần gộp điều kiện search + status filter, bảo toàn ancestor section cần thiết và công bố no-match state.
- **Validation/output:** debounce/min length/no-match copy chưa được chỉ định; không đổi API data hoặc status.

### ME06-EV-05 — Expand/collapse tree

- **Trigger:** click chapter row hoặc controls mở/thu tất cả (#19, #21/#22/#36/#37).
- **Current mockup:** đổi class `.hidden` và icon chevron; expand/collapse-all hiện toast.
- **Expected:** state local theo page session; không GET lại hoặc mutate server. Cần keyboard semantics, `aria-expanded`, focus và quy tắc filter khi parent bị ẩn trước implementation.

### ME06-EV-06 — Sắp xếp và lưu thứ tự

- **Trigger:** kéo handle/hàng hoặc click “Lưu thứ tự sắp xếp” (#10).
- **Current mockup:** button chỉ gọi toast ghi nhầm API #52 PUT reorder; chưa thấy drag-save handler/network call.
- **API source:** #52 là PATCH publication; #50 cấp root order lúc tạo; #51 giữ nguyên parent/order. Không có reorder route trong scope/contract hiện tại.
- **Result:** `BLOCKED`; không gửi request giả, không optimistic-save. Cần endpoint/body, conflict/rollback semantics, ordering scope (root/siblings) và AC approval.

### ME06-EV-07 — Thêm Chapter/root Content

- **Trigger:** “Thêm Chương mới” (#11).
- **Candidate:** ME-07 create flow → POST #50 với `course_id/content_type/title/payload`.
- **Current API constraints:** server tạo root với `parent_id=NULL`, next root order, status `PENDING_REVIEW`; type/payload chưa có enum/schema xác nhận.
- **UI:** chưa có form/navigation handler. Chỉ cho phép sau khi chapter mapping, payload, status lifecycle và API DD được owner xác nhận; sau create expected refresh #49.
- **Failure:** API source có auth 401, direct-owner/absent course 403, body validation 422, database/mapping 500. Error UX/field mapping chưa có client source.

### ME06-EV-08 — Thêm nội dung con / liên kết ME-04

- **Trigger:** #12 hoặc nút “+ Bài học” trong chapter #23.
- **Expected handoff:** ME-04 được ghi trên mockup; list_screen mô tả ME-07 create/edit và luồng F08 đưa ME-04/ME-06 vào cùng content journey.
- **Current:** #50 không nhận `parent_id`, luôn tạo root; #47/#48 dùng `lessons`/`lectures`, chưa có mapping sang Content child. Không thể tạo child hoặc gán parent bằng cách suy đoán payload.
- **Result:** `BLOCKED`; cần API/content model và route handoff được duyệt. Không tự gọi #50 cho child.

### ME06-EV-09 — Mở chi tiết qua ME-05

- **Trigger:** “Xem ME-05” ở row #25.
- **Expected destination:** ME-05 `/mentor/lectures/:lectureId` dùng #48.
- **Current:** #49 trả `Content.id`; #48 đọc `lessons.id`; source chưa chứng minh cùng identifier/entity. Anchor là `#`.
- **Result:** không ghép `Content.id` thành `lectureId` nếu mapping không có; route/event blocked.

### ME06-EV-10 — Mở editor/sửa Content qua ME-07/#51

- **Trigger:** edit controls #25/#27/#29.
- **Precondition:** node ID và approved type-specific editor/payload mapping.
- **Expected:** mở ME-07; existing node được tìm trong #49 response (inventory) hoặc dùng API detail nếu được duyệt. Save dùng PUT #51; body thay thế `content_type/title/payload`.
- **Current server effect:** lock current Content/course, kiểm tra direct-owner, archive snapshot hiện tại vào `content_versions`, update 3 body fields, đặt `PENDING_REVIEW`, giữ `parent_id/order`, commit rồi trả Content 200. #51 không move/reorder node.
- **After:** expected invalidate/re-fetch #49; client cache/state chưa có code. Handle 401/403/404/422/500; conflict semantics optimistic version chưa có version token trong #49.

### ME06-EV-11 — Rubric/configuration/question bank

- **Trigger:** Auto-Grading Rubric/Cấu hình #31 hoặc Bộ đề #33.
- **Current source:** không có field/payload subtype/schema hoặc endpoint tương ứng trong #49–#53 trace. Các menu khác cũng chưa có action mapping.
- **Result:** `BLOCKED`; không route hoặc mutate dựa trên labels mẫu.

### ME06-EV-12 — Thể hiện trạng thái nháp

- **Trigger:** load item #34 hoặc đổi filter #17.
- **Source:** #49 trả nguyên `status`; #50 và #51 hiện tạo/đưa về `PENDING_REVIEW`; enum/lifecycle owner approval chưa có.
- **Result:** UI phải preserve raw value và chỉ gắn nhãn/style sau khi status dictionary được duyệt. Không dùng sample “Bản nháp” để kết luận source status.

### ME06-EV-13 — Publish/unpublish qua ME-08/#52

- **Trigger:** nút publish row #35 hoặc action menu sau này.
- **Expected:** mở ME-08 để review/confirm theo inventory; request target state `{published:boolean}`.
- **Current source:** PATCH #52; direct-owner; target true chỉ từ `APPROVED`, target false chỉ từ `PUBLISHED`; cùng target idempotent; trạng thái không hợp lệ trả 422; success 200 `DESIGN_RESOURCE_UPDATED` + Content. Readiness chỉ kiểm tra source status, chưa validate payload readiness.
- **Result:** nút “Xuất bản ngay” trên row đang hiển thị draft bị `BLOCKED` với source flow. Sau success, refresh #49; không set `data-status` optimistic như mockup.

### ME06-EV-14 — Xóa Content qua ME-08/#53

- **Trigger:** menu row → dialog/action ME-08 (dialog không hiện trong ảnh ME-06).
- **Expected:** cảnh báo dependency, confirm người dùng rồi DELETE #53; success refresh #49.
- **Current source:** direct-owner; `PUBLISHED` bị từ chối 422 tới khi unpublish; active parent có child bị từ chối 422; soft-delete row và trả `DeleteResult`. Không cascade.
- **Result:** dependency text/error mapping, confirmation, undo và refresh UI chưa có Study Web source. Không tự suy ra policy cascade hoặc hard delete.

### ME06-EV-15 — Header/footer shell actions

- **Trigger:** logo/nav/search/notification/account/footer (#1–#5, #43–#44).
- **Current:** nav/footer anchors là `#`; search input không có handler; notification button không có list handler; account block chỉ là display.
- **Result:** route destinations, search domain, notification API, profile/session menu và external links cần route/config/source; không coi text là URL.

### ME06-EV-16 — Breadcrumb và handbook

- **Trigger:** click breadcrumb #6 hoặc link handbook #40.
- **Current:** `href="#"`; course slug/title/handbook URL chỉ là mockup copy. #49 trả `course_id` và Content; không trả title/code.
- **Result:** đích ME-02/ME-03 và handbook URL phải được bind bằng route/content đã duyệt. Không tạo URL từ title hoặc slug mẫu.

### ME06-EV-17 — Quality/audit panels và “xem toàn bộ”

- **Trigger:** xem panel #39/#41 hoặc click #42.
- **Current:** quality criteria, event names, actors, timestamps, count `142` là fixture; link/button chưa wired.
- **Source boundary:** GET #49 không trả quality rules/audit records/count. Tồn tại DDL audit artifact không tự tạo read endpoint/client permission.
- **Result:** cần API/read model, pagination, actor/time privacy và rule ownership; tới lúc đó panel không thể hiện như dữ liệu runtime.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
