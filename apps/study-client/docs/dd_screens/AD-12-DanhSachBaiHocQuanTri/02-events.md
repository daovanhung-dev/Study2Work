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

Prototype HTML chưa phát sinh các event dưới đây. Angular source hiện có route/page và GET #82 caller; đây là source trace, không phải browser/runtime evidence. Client-side retry/timeout/cache policy chưa được xác định trong source.

### EV-01 — Vào màn hình và tải danh sách

- **Trigger / element:** route entry/reload AD-12; #14/#25–#34. **Type:** Load.
- **Precondition:** expected authenticated Admin có lesson-management permission; hiện chỉ local role `ADMIN` evidence. Route `/admin/lessons` là đề xuất.
- **Input:** optional query `course?:int64`, `status?:string`, `type?:string` theo catalog; no body. Mockup keyword/slug/status alias không được tự thêm vào request. Angular chỉ cho nhập raw Course ID qua text field.
- **Processing:** (1) Angular page bắt đầu `loading` qua `adminQueryState`. (2) Gọi #82 bằng Bearer; ban đầu không có query, Apply gửi đúng query `course` nếu có, Refresh lặp query đang áp dụng, Reset tải lại không filter. (3) Server kiểm tra JWT/role trước query parse/DB. (4) Parse `course` thành signed int64; supplied `type` bị validator từ chối 422, kể cả chuỗi rỗng. (5) Query active candidate legacy `lessons`, exact equality course/status, loại `DELETED`, order `course_id ASC NULLS LAST, sort_order ASC NULLS LAST, id ASC`. (6) Map row theo response `Lesson`; không pagination/count. (7) Local success trả `200 ApiEnvelope<Lesson[]>` `data` là array; catalog lại ghi singular. (8) UI source hiển thị loading/error/empty/loaded; runtime chưa xác minh.
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
- **Processing:** Angular hiện nhận Course ID trực tiếp dưới dạng raw text, không dùng slug, không đổi qua `Number`, không suy ra ID và không gọi API khác để tạo mapping. Apply gửi đúng `course`; current server accepts signed int64 including negative/zero, rejects invalid/overflow with 422 after auth.
- **Output/errors:** render filtered data sau response #82; local errors 401/403/422/500. Khóa học title/options và slug mapping vẫn chưa có source.

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

- **Trigger / element:** Apply, filter refresh #24, empty-state refresh #29 và reset #30.
- **Input:** filter hiện hành chỉ gồm optional raw text Course ID; rỗng nghĩa là không áp dụng filter.
- **Processing:** Apply gửi query hiện hành; Refresh lặp query đang áp dụng; Reset xóa draft và gọi lại #82 không filter. Nút Apply/Refresh/Reset khóa khi request đang tải. Không gửi search/type/status hoặc alias chưa được giải quyết; không có pagination để reset.
- **Output/errors:** hiển thị loading rồi map response theo EV-01; lỗi 401/403/422/500. `switchMap` thay request cũ khi query thay đổi; retry/cancel policy riêng chưa có. Runtime/focus behavior chưa xác minh.

### EV-07 — Mở chi tiết bài học

- **Trigger / element:** row/action dự kiến từ #25 khi response có row; screenshot chỉ có empty state, không có action row quan sát được.
- **Input:** `Lesson.id` numeric từ response, ứng viên path `lesson_id:int64` cho AD-13/#83.
- **Processing:** current Angular source tạo RouterLink từ `Lesson.id` chỉ khi đó là safe JS integer; ID ngoài range bị disable kèm cảnh báo precision. Link mở route AD-13, nơi page gọi #83. Backend hiện guard role `ADMIN`; fine-grained lesson permission và API DD còn mở. Không truyền `course_id` thay lesson ID, không dựa vào thứ tự row hoặc slug.
- **Output:** điều hướng tới AD-13 cho safe ID; browser/runtime chưa xác minh. Back/reload filter preservation chưa xác định. Không mô tả edit/delete buttons tại AD-12; AC-34 để các mutation #84–#86 ở AD-14.

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

### Current source — 2026-11-21

- EV-01 now accepts #82 data only when the envelope has the exact DESIGN_RESOURCE_RETRIEVED code and the payload is a Lesson[] whose entries match the local response projection. Invalid collection/item data goes to the page error state rather than throwing during row mapping.
- EV-07 still links only safe Lesson IDs to AD-13. The visible Lesson and Course identifiers now use precision-safe formatting in both list rows and detail fields. Filter, refresh, reset, API request and disabled-action behavior are unchanged.
