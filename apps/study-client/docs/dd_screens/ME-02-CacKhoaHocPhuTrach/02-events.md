# ME-02 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `ME-02-EV-001` | `ME02-EV-01` / `ME02-EV-01` — Vào màn hình và tải danh sách | See source event detail below |
| `ME-02-EV-002` | `ME02-EV-02` / `ME02-EV-02` — Tìm tên/mã khóa học | See source event detail below |
| `ME-02-EV-003` | `ME02-EV-03` / `ME02-EV-03` — Lọc status | See source event detail below |
| `ME-02-EV-004` | `ME02-EV-04` / `ME02-EV-04` — Lọc level | See source event detail below |
| `ME-02-EV-005` | `ME02-EV-05` / `ME02-EV-05` — Sắp xếp | See source event detail below |
| `ME-02-EV-006` | `ME02-EV-06` / `ME02-EV-06` — Bỏ một active-filter chip | See source event detail below |
| `ME-02-EV-007` | `ME02-EV-07` / `ME02-EV-07` — Xóa toàn bộ bộ lọc | See source event detail below |
| `ME-02-EV-008` | `ME02-EV-08` / `ME02-EV-08` — Chuyển trang hoặc đổi page size | See source event detail below |
| `ME-02-EV-009` | `ME02-EV-09` / `ME02-EV-09` — Mở Workspace cho course | See source event detail below |
| `ME-02-EV-010` | `ME02-EV-10` / `ME02-EV-10` — Mở quản lý nội dung | See source event detail below |
| `ME-02-EV-011` | `ME02-EV-11` / `ME02-EV-11` — Mở danh sách chấm bài | See source event detail below |
| `ME-02-EV-012` | `ME02-EV-12` / `ME02-EV-12` — Mở tiến độ hoặc analytics course | See source event detail below |
| `ME-02-EV-013` | `ME02-EV-13` / `ME02-EV-13` — Tạo bài giảng mới | See source event detail below |
| `ME-02-EV-014` | `ME02-EV-14` / `ME02-EV-14` — Xem báo cáo học vụ tổng thể | See source event detail below |
| `ME-02-EV-015` | `ME02-EV-15` / `ME02-EV-15` — Điều hướng header và breadcrumb | See source event detail below |
| `ME-02-EV-016` | `ME02-EV-16` / `ME02-EV-16` — Header search, notification hoặc Mentor profile | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: 4. Event specifications

### `ME02-EV-01` — Vào màn hình và tải danh sách

- **Trigger / type:** Route enter / page load.
- **Input:** Route `/mentor/courses`; active Mentor access token do app shell quản lý; optional `status`, `page`, `size` chỉ khi UI state được thống nhất.
- **Precondition:** Mentor session hợp lệ. Current Study Web route/session `UNWIRED`.
- **API:** `GET /api/v1/mentor/courses`, `Authorization: Bearer <JWT>`, no body; default page=1,size=20, omit status.
- **Steps:** (1) Router/auth shell phải kiểm role trước khi render; (2) gọi #46; (3) API guard xác thực JWT/`MENTOR` trước DB; (4) validate query; (5) count và page cùng owner/status predicates; (6) map CoursePage; (7) khi success, bind Course fields/pagination theo §6; (8) không render sample KPI như runtime data.
- **Output:** 200 `DESIGN_RESOURCE_RETRIEVED`; `data.items` rỗng vẫn là success. Có thể giữ `partial` widget state chỉ khi sau này nhiều API được phê duyệt; hiện inventory ME-02 chỉ có #46.
- **Errors:** 401 authentication, 403 role denial, 422 query validation, 500 safe internal error; network/timeout/cache/retry presentation chưa được thiết kế.

### `ME02-EV-02` — Tìm tên/mã khóa học

- **Trigger / type:** Input/change trên #15.
- **Input:** String tên hoặc mã course; mockup có example `FE-ENT-04`.
- **Precondition:** Search contract và endpoint được duyệt.
- **Steps/output:** #46 hiện không có `q` hay course-code query; không gửi tham số không khai báo và không lọc giả ở client trên một page. Debounce, normalization, empty-query behavior, page reset và cross-page search đều `BLOCKED` tới khi có contract/source hỗ trợ.

### `ME02-EV-03` — Lọc status

- **Trigger / type:** Change #16 hoặc remove status chip #19.
- **Input:** UI values `all|active|upcoming|archived`.
- **Precondition:** Product/BE chốt mapping sang enum server.
- **Steps:** `all` tương ứng omit status theo API; current source chỉ nhận exact `DRAFT|PUBLISHED`. Không tự map các label khác. Sau khi mapping được duyệt, gửi status, page và size hợp lệ; count/list của #46 cùng filter.
- **Output/error:** 200 Page<Course> hoặc 422 `DESIGN_VALIDATION_ERROR`; hiện trạng UI chưa thể gửi 3 non-all values một cách có căn cứ.

### `ME02-EV-04` — Lọc level

- **Trigger / type:** Change select #17.
- **Input:** `enterprise|advanced|foundation|all`.
- **Xử lý / output:** #46 không nhận level và Course model không có level. Không gọi API với field này, không client-filter page đã tải như thể là toàn bộ danh sách. Cần source contract trước khi triển khai.

### `ME02-EV-05` — Sắp xếp

- **Trigger / type:** Change select #18.
- **Input:** `students_desc|progress_desc|updated_desc`.
- **Xử lý / output:** #46 không nhận sort; current order cố định `created_at DESC, id ASC`. Không hiển thị lựa chọn như hoạt động. Cần API/query + semantics metric được duyệt.

### `ME02-EV-06` — Bỏ một active-filter chip

- **Trigger / type:** Click close button trong #19.
- **Input:** Chip filter cần bỏ.
- **Current prototype:** HTML script dùng `querySelectorAll('button:has(...:contains("close"))')`; `:contains()` không phải CSS selector hợp lệ cho `querySelectorAll`, nên script có thể ném DOMException nếu chạy nguyên trạng. Nút cũng không có state/query binding.
- **Expected output:** Chỉ xóa đúng filter, reset page khi cần và refetch sau khi semantics/mapping đã được duyệt. Hiện `BLOCKED`.

### `ME02-EV-07` — Xóa toàn bộ bộ lọc

- **Trigger / type:** Click #20.
- **Input:** Current search/status/level/sort/term values và page.
- **Xử lý:** Không có handler trong HTML/runtime. Reset-to-default policy chưa xác định; không xóa state chỉ bằng DOM mutation rồi giả định server list đã được cập nhật. Sau approval cần refetch với query được hỗ trợ và page reset.
- **Output:** `BLOCKED`; API errors theo query nếu request sau này không hợp lệ.

### `ME02-EV-08` — Chuyển trang hoặc đổi page size

- **Trigger / type:** Click pagination #41 hoặc change page size #42.
- **Input:** Page integer, size integer.
- **API:** #46 accepts page `>=1`, size `1..100`; defaults `1/20`; screenshot exposes 10/20/50 (all within source bounds).
- **Steps:** (1) Validate page/size; (2) preserve only approved filters; (3) request #46; (4) use response pagination for controls/summary; (5) render `items=[]` as success even for out-of-range page; (6) decide whether changing size resets page (not specified in current source/approved screen contract).
- **Output/error:** 200 with current page metadata or 422 on invalid values; DB/projection issue maps 500. Request cancellation, stale response ordering, retry and cache rules chưa có FE source.

### `ME02-EV-09` — Mở Workspace cho course

- **Trigger / type:** Click #27/#33/#39.
- **Input:** `Course.id` từ #46 item đang chọn; current Course id type là integer.
- **Steps:** Không lấy ID từ title/code mẫu; chỉ enable destination khi item có ID và server-side route kiểm access. Route proposal ME-03 `/mentor/courses/:courseId`; destination API/source runtime phải tự validate authorization.
- **Output:** Navigation proposal; client route chưa wired. Assignment-course discrepancy có thể làm direct-owner-only destination từ chối course mà AC-21 xem là assigned.

### `ME02-EV-10` — Mở quản lý nội dung

- **Trigger / type:** Click action “Quản lý nội dung” trong #26/#32/#38.
- **Input:** Course ID của card.
- **Target:** Prototype ghi ME-06 `/mentor/courses/:courseId/content`, nhưng ME-02 inventory chỉ liệt kê ME-03/ME-04/ME-16; ME-03 lại liệt kê ME-06. Product cần chốt direct jump hay đi qua ME-03.
- **Output:** Không gọi #49 trên ME-02. Nếu direct navigation được duyệt, ME-06 tự gọi API theo source contract và kiểm quyền server-side. Hiện `DISCREPANCY / BLOCKED`.

### `ME02-EV-11` — Mở danh sách chấm bài

- **Trigger / type:** Click “Chấm đồ án/Capstone/Design” trong #26/#32/#38.
- **Input:** Card course ID và badge count mẫu.
- **Target:** Prototype ghi ME-09; inventory ME-02 không liệt kê ME-09 trong links. Route ME-09 hiện là proposal `/mentor/submissions`.
- **Output:** Không xem badge như count API và không gọi list #54 ở màn hình này; cần quyết định handoff/list filter. Current API reference của ME-02 chỉ #46.

### `ME02-EV-12` — Mở tiến độ hoặc analytics course

- **Trigger / type:** Click action “Tiến độ học viên” hoặc “Phân tích lớp học”.
- **Input:** Course ID đã lấy từ #46.
- **Targets:** ME-16 `/mentor/courses/:courseId/progress` theo inventory; card analytics có thể là ME-18 `/mentor/courses/:courseId/analytics`, nhưng action/ID trong prototype không thống nhất.
- **Current downstream source:** #65 trả progress mỗi active Student; #66 trả access/activity aggregate. Cả hai kiểm tra direct owner; không cho phép client tự tính Capstone/rating/average metric. Không gọi tại ME-02.
- **Output:** Route proposal; action-to-screen mapping cần chốt. `BLOCKED`.

### `ME02-EV-13` — Tạo bài giảng mới

- **Trigger / type:** Click #10.
- **Input:** Bắt buộc phải có `courseId` theo ME-04 route `/mentor/courses/:courseId/lectures/new`; nút tổng hiện không có selected course.
- **Xử lý:** Không chọn tùy tiện course đầu tiên hay dùng sample ID. Product cần thêm course picker/CTA per card hoặc đưa người dùng về ME-02 để chọn course; quyết định đó không có trong mẫu.
- **Output:** Chưa điều hướng; AC-21 course selection precedes upload/API #34 and create #47. CTA `BLOCKED`.

### `ME02-EV-14` — Xem báo cáo học vụ tổng thể

- **Trigger / type:** Click #9.
- **Input:** “Tổng thể” không truyền course ID/period.
- **Current source:** API #66 yêu cầu `course_id` và trả activity proxy, không phải toàn cohort completion/report. No global report API/route in ME-02 contract.
- **Output:** Destination/report semantics chưa có; không map sang #66 bằng cách chọn course mặc định. `NOT_FOUND / BLOCKED`.

### `ME02-EV-15` — Điều hướng header và breadcrumb

- **Trigger / type:** Click brand/nav/breadcrumb #1/#2/#6.
- **Input:** User-selected nav destination.
- **Steps:** Route proposals phải đối chiếu `list_screen.md`; `data-path` trong HTML chỉ là prototype attribute, mọi anchor href hiện `#`. Sau khi app router và Mentor shell được triển khai, route guard cần xác thực role; backend vẫn là authority cho course access.
- **Output:** No current navigation runtime. Dashboard `/mentor`, course list `/mentor/courses`, submissions `/mentor/submissions`, support `/mentor/support` là các route inventory proposals, không phải verified routes.

### `ME02-EV-16` — Header search, notification hoặc Mentor profile

- **Trigger / type:** Input #3 hoặc click #4/#5.
- **Input:** Search string hoặc button click.
- **Source gap:** Search copy nói học viên/bài tập; notification badge không có unread source/route trong ME-02; #46 mentor summary không có title/profile route. API #63 create notification và #64 check delivery status không phải notification inbox.
- **Output:** Không gắn hành vi/API chưa xác nhận. Cần destination, query/permission và response mapping trước khi triển khai.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
