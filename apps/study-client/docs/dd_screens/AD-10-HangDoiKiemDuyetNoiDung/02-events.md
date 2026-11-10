# AD-10 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-10-EV-001` | `Source heading` / EV-01 — Mở queue và tải trang đầu | See source event detail below |
| `AD-10-EV-002` | `Source heading` / EV-02 — Nhập từ khóa | See source event detail below |
| `AD-10-EV-003` | `Source heading` / EV-03 — Lọc định dạng | See source event detail below |
| `AD-10-EV-004` | `Source heading` / EV-04 — Lọc khóa học | See source event detail below |
| `AD-10-EV-005` | `Source heading` / EV-05 — Refresh, check-new-content và auto-sync | See source event detail below |
| `AD-10-EV-006` | `Source heading` / EV-06 — Chọn Content và chuyển sang AD-11 | See source event detail below |
| `AD-10-EV-007` | `Source heading` / EV-07 — Pagination | See source event detail below |
| `AD-10-EV-008` | `Source heading` / EV-08 — Shell, status, policy và footer affordances | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Mở queue và tải trang đầu

- **Trigger/type:** Route entry hoặc reload màn; `Load`. Element liên quan #12, #13, #22, #24–#25, #28.
- **Preconditions:** Route/client tồn tại; Bearer JWT hợp lệ; permission Admin/moderation được owner chốt. Hiện Study Web không có caller.
- **Input:** Query tùy chọn `type:string`, `course:int64`, `page:int32`; không path/body. Khởi tạo sạch không cần gửi filter. Trace ID có thể được middleware thêm.
- **API direct contract:** `GET /api/v1/admin/content/pending`, Bearer JWT/Admin; catalog trả `ApiEnvelope<Content>` và 401/403/500. Catalog không nêu 422.
- **Current local source (không phải contract đã duyệt):**
  1. Guard Bearer/JWT + role `ADMIN` chạy trước parse query và DB. Role mapping vẫn không chứng minh finer-grained moderation permission.
  2. `type` được giữ nguyên exact string; không whitelist/normalize. `course` parse signed int64; `page` positive int32, mặc định 1. Numeric parse/range lỗi trả 422 `DESIGN_VALIDATION_ERROR` (DERIVED, catalog chưa liệt kê).
  3. Count và list cùng filter trên `contents` active, `status='PENDING_REVIEW'`; optional exact `content_type`/`course_id`; `id ASC`, fixed size 20, offset theo page. Đây là local legacy schema candidate; không xác nhận live schema.
  4. Local success `200 DESIGN_RESOURCE_RETRIEVED` trả `data.items[]`, `data.pagination={page,size,total,total_pages}`. Item gồm tám Content fields đã liệt kê ở A. Không author/course-name/submitted-time/version join; không mutation/commit.
  5. Map `items=[]` thành empty state; nếu có items, không hiển thị unsupported fields. Trước khi dùng response cần owner đồng bộ Page-vs-singleton contract và danh sách cột.
- **Outcome/errors:** Empty/no-match/beyond-last-page → 200 empty Page hiện tại. 401 authentication, 403 role, 422 invalid numeric query (local-derived), 500 safe DB/projection error; network/timeout → client error state cần convention. Không tự retry/poll.
- **Current:** Screenshot chỉ render static `0/0`; không có request/state binding.

### EV-02 — Nhập từ khóa

- **Trigger/type:** Input event trên #18.
- **Input/current behavior:** Chuỗi text do người dùng nhập; HTML không đặt name, length hoặc validation, không có handler/debounce.
- **Expected/API boundary:** Placeholder hứa search title/lecturer nhưng #78 không khai báo keyword, không response author/lecturer. Không thêm client-only filtering hoặc query param khi chưa có yêu cầu/contract.
- **Processing/output:** Hiện tại chỉ đổi value trong input DOM; không gọi API, không đổi queue, count hoặc page.
- **Exceptions:** Không có validation/network state trong prototype. Nếu search được yêu cầu, cần chốt query, field scope, normalization, page reset, validation và API trước implementation.

### EV-03 — Lọc định dạng

- **Trigger/type:** Change trên #19.
- **Input:** Current selected value `all` (default), `video`, `doc`, hoặc `quiz`.
- **Current behavior:** Native select đổi selection; không có handler/API.
- **Candidate API processing:** `type` hiện là raw exact string filter trên local `contents.content_type`. Chỉ `all` có thể biểu thị “không gửi filter” như UI convention dự kiến; mapping đó cần phê duyệt. Không tự khẳng định `video/doc/quiz` trùng enum/storage values hoặc chuẩn hóa casing. Khi contract chốt, cần quyết định page reset (thông thường page 1 nhưng hiện chưa được duyệt) và đồng bộ count + rows.
- **Output/error:** Hiện queue không đổi. API local unknown type có thể trả empty Page thay vì validation; query error → 500. No form error currently.

### EV-04 — Lọc khóa học

- **Trigger/type:** Change trên #20.
- **Input:** Current values `all`, `fe`, `be`, `devops`, `data`; option labels là sample course names.
- **Current behavior:** Native selection only; không handler, option source/API hoặc ID mapping.
- **API boundary:** #78 cần numeric signed-int64 `course`; slugs không chuyển đổi an toàn sang ID. Không suy ra IDs, không gọi #73/options endpoint và không dùng label làm identifier khi chưa có approved option-source contract.
- **Output/error:** Hiện queue không đổi. Khi có ID, invalid numeric input trả local-derived 422; matching course có thể trả empty Page. Chưa định nghĩa selection reset/page behavior hoặc lỗi course-option load.

### EV-05 — Refresh, check-new-content và auto-sync

- **Trigger/type:** Click #21; #26 disabled; #27 là copy timer claim.
- **Input/current behavior:** Nút #21 không nhận payload; script thêm `animate-spin`, set `disabled`, đợi 700 ms rồi gỡ class/disabled. Không gọi #78. #26 luôn disabled. HTML không có `setInterval`, polling hoặc lifecycle listener.
- **Expected/API candidate:** Nếu refresh được wire, GET #78 có thể tải lại trang/filter hiện tại sau khi API cardinality/query contract được chốt. Không gửi mutation, không tạo retry tự động, và không coi “30 giây/lần” là polling spec.
- **Output/errors:** Prototype chỉ có local animation; không success/error/empty refresh result. Refresh contract cần xác định duplicate clicks, loading cancellation, timeout và failure-state behavior.

### EV-06 — Chọn Content và chuyển sang AD-11

- **Trigger/type:** Chọn row/action sau khi queue có item; đây là AC-33 expected action, không hiện trong empty prototype.
- **Preconditions/input:** Có item từ response đã được contract owner chốt; candidate `data.items[].id:int64` làm `content_id` route param của `/admin/content/:contentId/review`.
- **Processing:** Chỉ truyền ID; AD-11 gọi #79. Không lấy `course_id` hoặc ID hiển thị thay cho `Content.id`; không tự truyền version/author vì #78 không có fields đó. Chưa có row click/action HTML hoặc router.
- **Outcome:** AC-33 xác định chọn Content để mở detail; route/history, giữ filter/page, open-in-new-tab, stale item response và return path chưa được wire. Nếu queue rỗng thì không có selection.

### EV-07 — Pagination

- **Trigger/type:** Click #29/#31 hoặc page number #30. Prototype controls disabled/static.
- **Input/current behavior:** Page number “1”; no handler, page count or URL state.
- **Local API candidate:** `page` positive int32, mặc định 1, size cố định 20, order `id ASC`; `data.pagination` gồm `page`, `size`, `total`, `total_pages`. Size/order/cardinality là DERIVED và cần owner approval; API không có `size`/`sort` query.
- **Processing/output:** Current UI không đổi state hoặc gọi request. Nếu được phê duyệt, next/previous phải kiểm soát bounds từ pagination response; filter thay đổi/reset trang và đồng bộ browser history cần quyết định trước khi code.
- **Errors:** Invalid page trả 422 local-derived; page beyond total trả 200 Page rỗng theo current source. Không suy diễn page buttons disabled rules từ prototype empty sample.

### EV-08 — Shell, status, policy và footer affordances

- **Trigger/type:** Click nav/breadcrumb/notification/rubric/footer hoặc đọc status badge.
- **Current behavior:** Nav/footer/rubric anchors `href="#"`; notification không handler; breadcrumb spans không route. `SYSTEM NORMAL`, RBAC badges, policy copy và API ACTIVE là static. Không API/event/monitoring call.
- **Expected behavior:** Chỉ route, policy destination, authorization result, support/rubric link hoặc health status khi các nguồn tương ứng được xác nhận. Không suy ra các claim từ #78.
- **Output:** Prototype giữ nguyên page; không thay state, điều hướng hoặc gọi service.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
