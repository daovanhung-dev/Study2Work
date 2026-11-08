# AD-12 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-12-EV-001` | `Source heading` / EV-01 — Vào màn hình và tải danh sách | See source event detail below |
| `AD-12-EV-002` | `Source heading` / EV-02 — Nhập từ khóa tìm kiếm | See source event detail below |
| `AD-12-EV-003` | `Source heading` / EV-03 — Chọn khóa học | See source event detail below |
| `AD-12-EV-004` | `Source heading` / EV-04 — Chọn loại bài học | See source event detail below |
| `AD-12-EV-005` | `Source heading` / EV-05 — Chọn trạng thái | See source event detail below |
| `AD-12-EV-006` | `Source heading` / EV-06 — Làm mới hoặc reset bộ lọc | See source event detail below |
| `AD-12-EV-007` | `Source heading` / EV-07 — Mở chi tiết bài học | See source event detail below |
| `AD-12-EV-008` | `Source heading` / EV-08 — Chọn “Thêm bài học mới” | See source event detail below |
| `AD-12-EV-009` | `Source heading` / EV-09 — Shell, compliance copy, footer và trạng thái tĩnh | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết sự kiện

Prototype chưa phát sinh các event dưới đây; đây là event design và source trace, không phải behavior đang chạy. Trình tự chỉ gồm bước được áp dụng; client-side retry/timeout/cache policy để mở vì không có client source.

### EV-01 — Vào màn hình và tải danh sách

- **Trigger / element:** route entry/reload AD-12; #14/#25–#34. **Type:** Load.
- **Precondition:** expected authenticated Admin có lesson-management permission; hiện chỉ local role `ADMIN` evidence. Route `/admin/lessons` là đề xuất.
- **Input:** optional query `course?:int64`, `status?:string`, `type?:string` theo catalog; no body. Mockup keyword/slug/status alias không được tự thêm vào request.
- **Processing:** (1) UI target bắt đầu `loading`; không có client implementation hiện tại. (2) Gọi #82 với Bearer và query đã được duyệt. (3) Server kiểm tra JWT/role trước query parse/DB. (4) Parse `course` thành signed int64; supplied `type` bị validator từ chối 422, kể cả chuỗi rỗng. (5) Query active candidate legacy `lessons`, exact equality course/status, bỏ `DELETED`, order `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`. (6) Map row theo response `Lesson`; không pagination/count. (7) Local success trả `200 ApiEnvelope<Lesson[]>` `data` là array; catalog lại ghi singular. (8) UI target cần xử lý envelope/cardinality sau khi contract thống nhất.
- **Output/state:** non-empty list có thể thành `ready`; empty `[]` thành `empty`; hiện screenshot luôn hiển thị static empty. Không suy ra “sync pending”.
- **Errors:** 401/403; 422 malformed/overflow `course` hoặc any supplied `type`; safe 500 + rollback query/mapping/null projection failure. Catalog chưa liệt kê 422. #82 không có 404 path.
- **API details:** `GET /api/v1/admin/lessons`, Bearer/Admin theo catalog; query như trên; no request body; expected response catalog `ApiEnvelope<Lesson>`, actual local `ApiEnvelope<Lesson[]>`; timeout/retry/dedup/cache chưa có policy.

### EV-02 — Nhập từ khóa tìm kiếm

- **Trigger / element:** input #20, input/change/submit tùy client design; current HTML không có handler.
- **Input:** text placeholder gợi ý tên bài hoặc mã bài giảng; giới hạn/normalization/debounce/submit mode không được quy định.
- **Processing:** không gửi `q`, `keyword` hoặc code tới #82 vì route không khai báo query tương ứng; `Lesson` projection cũng không có lesson code. Giữ query chưa áp dụng hoặc disable input cho tới khi owner bổ sung contract và source.
- **Output/errors:** không có filter result hiện tại. Không tuyên bố 0 matches hay tự client-filter toàn bộ list khi chưa có cap/paging semantics. Validation, debounce, request cancellation và empty-query behavior là open decisions.

### EV-03 — Chọn khóa học

- **Trigger / element:** change #21; hiện select trong static HTML.
- **Input:** UI option slug (ví dụ `fe`, `be`, `ux`, `qa` trong prototype); API query cần `course` signed int64, đại diện candidate `Course.id`.
- **Processing:** chưa có mapping slug→int64 hoặc option API được duyệt. Không gửi slug vào int64, không suy ra ID, không gọi API khác để tạo mapping. Sau khi source/mapping được phê duyệt, client có thể gửi đúng numeric `course`; current server accepts signed int64 including negative/zero, rejects invalid/overflow with 422 after auth.
- **Output/errors:** chỉ render filtered data sau response #82 contract resolution; local errors 401/403/422/500. Mapping, empty option và reset default cần chốt.

### EV-04 — Chọn loại bài học

- **Trigger / element:** change #22.
- **Input:** prototype options `video`, `reading`, `assignment`, `quiz`.
- **Processing:** model/query/DDL candidate không cung cấp lesson type; mọi `type` hiện có trong query trả `422 DESIGN_VALIDATION_ERROR`, field `type`, code `UNSUPPORTED_FILTER`. Không gửi param hoặc ánh xạ sang field khác cho tới khi owner bổ sung contract.
- **Output/errors:** không có filtered state theo type ở current source. UI không được hiển thị thành công như thể filter đã áp dụng; cần thống nhất enum, data source, migration/query và catalog.

### EV-05 — Chọn trạng thái

- **Trigger / element:** change #23.
- **Input:** mockup aliases `active`, `draft`, `hidden`; API nhận raw `status:string`.
- **Processing:** current query dùng exact equality, không validate enum, normalize casing hoặc alias. Không tự map `active` sang `PUBLISHED`, `hidden` sang `ARCHIVED`, hoặc suy ra status khác từ mockup. Chỉ sau khi status vocabulary/mapping được duyệt mới gửi giá trị chính xác.
- **Output/errors:** nếu gửi chuỗi hợp lệ với request, backend lọc exact và vẫn loại `DELETED`; status không-match trả `[]`. Query status không có validation 422 theo current source; lỗi auth/query là 401/403/500.

### EV-06 — Làm mới hoặc reset bộ lọc

- **Trigger / element:** filter refresh #24; empty-state refresh #29; reset #30. HTML #29 disabled; tất cả controls không có handler.
- **Input:** current filter state phía client chưa tồn tại. Refresh nên giữ các filter đã xác nhận; reset cần xóa các filter và quay về default chỉ sau khi default được chốt.
- **Processing:** khi được wire, refresh/reset có thể gọi lại #82 với query hợp lệ. Không gửi search/type hoặc course/status alias chưa được giải quyết. Reset không thể làm việc như “clear pagination” nếu pagination chưa tồn tại.
- **Output/errors:** hiển thị loading rồi map response theo EV-01; lỗi 401/403/422/500. Chống double submit, request cancellation, retry và focus/accessibility feedback chưa có source. Nút empty refresh hiện disabled trong mockup.

### EV-07 — Mở chi tiết bài học

- **Trigger / element:** row/action dự kiến từ #25 khi response có row; screenshot chỉ có empty state, không có action row quan sát được.
- **Input:** `Lesson.id` numeric từ response, ứng viên path `lesson_id:int64` cho AD-13/#83.
- **Processing:** AC-34 dự kiến list → #83 detail. Chỉ điều hướng sau khi #83 contract, permission và route/client được chốt; không truyền `course_id` thay lesson ID, không dựa vào thứ tự row hoặc slug.
- **Output:** target AD-13; back/reload filter preservation chưa xác định. Không mô tả edit/delete buttons tại AD-12; AC-34 để các mutation #84–#86 ở AD-14.

### EV-08 — Chọn “Thêm bài học mới”

- **Trigger / element:** CTA #17.
- **Input:** không có payload/lesson ID.
- **Processing:** không có create route/API xác nhận trong AC-34 hoặc chuỗi #82–#86; không gọi #84 vì đó là update candidate. CTA hiện chỉ là prototype button.
- **Output:** không có success/navigation behavior được xác nhận. Cần create API, route/màn hình, quyền và form contract trước khi bật; đến khi đó presentation/disabled policy là quyết định sản phẩm.

### EV-09 — Shell, compliance copy, footer và trạng thái tĩnh

- **Trigger / element:** shell navigation #1–#13, assurance/API badges #7/#11/#16/#19, compliance #35–#38, footer #39–#42; click/route entry.
- **Input/processing:** HTML có hash anchors và các control tĩnh; không có monitoring, compliance, notification hay navigation request. Không biến copy thành trạng thái server, không suy diễn HLS/SCORM/xAPI/DRM support.
- **Output:** không có destination/action hiện tại. Target cần design-system responsive layout, keyboard/focus states và link destinations; `.agents/web-study/design.md` quy định ocean tokens, Inter/system stack và content width khoảng 1120px. Mockup dùng cobalt, Plus Jakarta Sans và full-width; ghi nhận sai khác, giữ nguyên asset nguồn.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
