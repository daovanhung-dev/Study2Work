# AD-19 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-19-EV-001` | `Source heading` / EV-01 — Mở AD-19 và tải danh sách | See source event detail below |
| `AD-19-EV-002` | `Source heading` / EV-02 — Nhập tiêu đề tìm kiếm | See source event detail below |
| `AD-19-EV-003` | `Source heading` / EV-03 — Đổi channel/status filter | See source event detail below |
| `AD-19-EV-004` | `Source heading` / EV-04 — Đặt lại filters | See source event detail below |
| `AD-19-EV-005` | `Source heading` / EV-05 — Làm mới danh sách | See source event detail below |
| `AD-19-EV-006` | `Source heading` / EV-06 — Bắt đầu soạn thông báo | See source event detail below |
| `AD-19-EV-007` | `Source heading` / EV-07 — Chọn notification row/action sang AD-21 | See source event detail below |
| `AD-19-EV-008` | `Source heading` / EV-08 — Điều hướng pagination | See source event detail below |
| `AD-19-EV-009` | `Source heading` / EV-09 — Xem quy chuẩn phát hành | See source event detail below |
| `AD-19-EV-010` | `Source heading` / EV-10 — Shell navigation, notification icon và footer links | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Mở AD-19 và tải danh sách

- **Element / loại:** Screen initialization / Load.
- **Điều kiện:** Candidate route đã được wire; authenticated Admin và permission mapping được owner chốt; query filter chỉ chứa enum đã duyệt.
- **Đầu vào:** Route candidate /admin/notifications; Bearer JWT; optional status:string, channel:string, page:int32. Không có body/path. Search text không thuộc request.
- **Trình tự:**
  1. Nhận route và lấy auth/session từ shared auth layer; không lấy Admin identity từ mockup.
  2. Kiểm tra notification-management permission theo AC-36. Local source hiện chỉ cho role ADMIN, nên không dùng thay thế nếu policy chưa chốt.
  3. Khởi tạo loading state và tạo request chỉ từ query đã được xác nhận. Catalog không định nghĩa page default, page size hoặc search.
  4. Gọi GET /api/v1/admin/notifications với Authorization Bearer. Không phát đồng thời metric request vì chưa có API metric.
  5. Nếu HTTP 200, kiểm tra envelope/businessCode và shape. Direct catalog mong đợi data:Notification. Current local source trả data:{items:Notification[],pagination:{page,size,total,total_pages}}; không tự chấp nhận hai shape như một contract thống nhất.
  6. Nếu owner xác nhận Page, map item.id/title/content/channels/status/created_at và pagination fields. read_at/scheduled_at chỉ map khi response có giá trị; không suy recipient hoặc send time.
  7. Chuyển loading sang ready khi có item, empty khi danh sách hợp lệ nhưng rỗng. Copy empty-state sync claim không được coi là fact từ API.
  8. Không cache/persist result, retry tự động hay poll vì không có policy/source cho các hành vi này.
- **API / mapping:** Contract trực tiếp: #92, GET /api/v1/admin/notifications, Bearer/Admin, query status/channel/page; success 200 DESIGN_RESOURCE_RETRIEVED + ApiEnvelope<Notification>; errors 401 DESIGN_AUTHENTICATION_REQUIRED, 403 DESIGN_ACCESS_DENIED, 503 DESIGN_DEPENDENCY_UNAVAILABLE, 500 DESIGN_INTERNAL_ERROR. Local #92 fallback response/API behavior is listed in section A and must remain DERIVED until catalog/DD approval.
- **Kết quả và ngoại lệ:** 401 → shared session-expired/auth flow; 403 → access-denied; 503 → dependency-unavailable; 500 → generic retrieval error. Current source adds 422 for invalid/non-positive page; đây không phải direct catalog error. Local empty/out-of-range page returns 200 empty Page. No 404 is listed for #92. Preserve traceId if available; no UI policy to expose raw internal error.

### EV-02 — Nhập tiêu đề tìm kiếm

- **Element / loại:** #20 text input; Input event.
- **Điều kiện:** Input đang hiện; không cần API session để gõ trong mockup.
- **Đầu vào:** Chuỗi người dùng nhập; HTML không khai báo length/required/trim/debounce.
- **Trình tự:** 1) Nhận text vào control. 2) Không áp validation tự tạo. 3) Không chuẩn hóa, lọc hay lưu query state vì source không định nghĩa. 4) Không gọi #92: search không có trong catalog. 5) Không ánh xạ kết quả. 6) Không cập nhật table. 7) Giữ giá trị control cho đến Reset hoặc điều hướng. 8) Chuyển blocker search API/owner decision cho implementation.
- **Kết quả:** Hiện tại chỉ có thể nhập text trong mockup; không có search behavior. Không trình bày “không có kết quả” dựa trên text này.

### EV-03 — Đổi channel/status filter

- **Element / loại:** #21/#22 Select change.
- **Điều kiện:** Control hiện; option khác “all” được chọn.
- **Đầu vào:** Prototype channel app/email/system và status draft/scheduled/published. Catalog chỉ khai báo query string; không khai enum.
- **Trình tự:** 1) Đọc raw value. 2) Không đổi lowercase, trim hoặc alias. 3) Không dịch app→PUSH hay published→SENT; mapping không có nguồn. 4) Không gọi #92 trong trạng thái contract hiện tại. 5) Không cập nhật table/metric. 6) Giữ selection trong control; 7) đưa enum mapping/empty-filter semantics cho owner. 8) Sau khi được duyệt mới tạo query status/channel theo contract.
- **Local source evidence:** Validator giữ nguyên chuỗi; SQL lọc chính xác status/channel. Local values là FAILED/QUEUED/SENT và EMAIL/PUSH. Chuỗi khác có thể cho list rỗng; không có normalization.
- **Kết quả:** Control đổi giá trị nhưng không lọc dữ liệu trong HTML hiện tại.

### EV-04 — Đặt lại filters

- **Element / loại:** #23 Button click.
- **Điều kiện:** Button được bật trong mockup.
- **Đầu vào:** Giá trị search, channel, status đang có.
- **Trình tự:** 1) Nhận click. 2) Không có validation/quyền/API. 3) Gọi resetFilters() trong HTML. 4) Đặt input rỗng và select về option mặc định. 5) Không reset page state vì script không quản lý page. 6) Không fetch #92. 7) UI chỉ đổi giá trị controls. 8) Không có success/error toast.
- **Kết quả:** Filters được xóa cục bộ; danh sách/metric không được reload. Contract tương lai cần quyết định reset có gọi API và về page 1 hay không.

### EV-05 — Làm mới danh sách

- **Element / loại:** #34 Button click; local timer.
- **Điều kiện:** Button chưa bị disabled bởi một lần click đang hoạt động.
- **Đầu vào:** Không có filter/request payload được chuẩn hóa.
- **Trình tự:** 1) Nhận click. 2) Không kiểm tra auth/quyền hoặc query. 3) Handler thêm animation class và disable button. 4) Timer 800ms chạy. 5) Không gọi API/network. 6) Không nhận response/error. 7) Hủy class và enable button khi timer kết thúc. 8) Không đổi list.
- **Kết quả:** Chỉ có spinner ngắn. Không được mô tả là reload thành công. Retry/timeout chưa áp dụng vì chưa có request.

### EV-06 — Bắt đầu soạn thông báo

- **Element / loại:** #15 Anchor/button click.
- **Điều kiện:** User chọn CTA; Admin create permission và destination chưa được xác minh.
- **Đầu vào:** Không có record/filter state được truyền trong HTML.
- **Trình tự:** 1) Browser nhận href /admin/notifications/create. 2) HTML không intercept click. 3) Không gọi #93 tại AD-19. 4) Inventory AD-20 route là /admin/notifications/new. 5) Study Web router không có source để xác nhận một trong hai URL. 6) Không tự redirect hoặc tạo alias. 7) UI/runtime hiện chưa thể xác định destination. 8) Reconcile route trước khi implementation.
- **Kết quả:** Ý định điều hướng sang AD-20 được ghi nhận; route đang mâu thuẫn và UNWIRED. Payload #93 thuộc AD-20, không chuyển data tự tạo từ AD-19.

### EV-07 — Chọn notification row/action sang AD-21

- **Element / loại:** #30 action-column placeholder / future row click.
- **Điều kiện:** Cần có row hợp lệ và row interaction được thiết kế; screenshot hiện không có row và HTML không có handler.
- **Đầu vào:** Candidate notification id:int64 từ item.id nếu shape/Page contract được duyệt. Recipient, campaign id hoặc operation_id không được giả định.
- **Trình tự:** 1) Nhận click chỉ khi row/action control thực sự được wire. 2) Xác nhận ID dương int64 theo catalog path của AD-21 API. 3) Không gọi API từ AD-19 trong prototype. 4) Inventory dự kiến mở /admin/notifications/:notificationId. 5) AD-21 dùng #94/#95/#96 theo trạng thái; inventory nói GET #96 khi xem nhưng #96 là endpoint status, không phải GET detail chung. 6) Không truyền các trường thiếu hoặc tự tạo detail response. 7) Lưu filter/page khi quay lại chỉ sau khi có navigation-state contract. 8) Nếu item ID hoặc detail endpoint không được duyệt, dừng và giữ list.
- **Kết quả:** Handoff AD-21 là expected relation, chưa runtime-confirmed; không có action control hiện hành.

### EV-08 — Điều hướng pagination

- **Element / loại:** #36–#40 buttons/indicator; click.
- **Điều kiện:** Buttons hiện disabled trong HTML; do đó event không thực thi ở prototype.
- **Đầu vào:** Nếu được wire, catalog chỉ có page?:int32; không có size/metadata. Local fallback hiện tại page mặc định 1, size 20.
- **Trình tự:** 1) Không xử lý click khi disabled. 2) Không tính first/previous/next/last từ 0/0 placeholder. 3) Không gọi #92. 4) Nếu Page được duyệt, bind page/total_pages và chỉ enable actions hợp lệ theo metadata; đây là thiết kế có điều kiện, chưa phải behavior hiện tại. 5) page local phải >=1 và int32. 6) Query/filter giữ nguyên chỉ khi state contract quy định. 7) Map response đúng page. 8) Out-of-range local source returns empty 200; catalog chưa chốt semantics.
- **Kết quả:** Pagination vẫn disabled. Page origin, size, ordering, empty/out-of-range behavior cần approval.

### EV-09 — Xem quy chuẩn phát hành

- **Element / loại:** #44 anchor click.
- **Điều kiện:** Click link; target screen chưa có trong inventory/router.
- **Đầu vào:** Không có.
- **Trình tự:** 1) Browser nhận href /admin/guidelines/notifications. 2) Không có router/contract source target. 3) Link không gọi API. 4) Không xác nhận nội dung policy hoặc 30-minute claim. 5) Không tạo route mới trong DD. 6) Ghi blocker route/policy ownership. 7) Không có response mapping. 8) Runtime outcome chưa biết.
- **Kết quả:** Mockup chỉ thể hiện ý định xem guideline; đích đến chưa xác nhận.

### EV-10 — Shell navigation, notification icon và footer links

- **Element / loại:** #2–#6, #8, #10, #46–#48; click.
- **Điều kiện:** User tương tác với shell control.
- **Đầu vào:** Nav anchor href #; footer href #; header notification icon không có handler. Breadcrumb có text/cursor styling nhưng không có route callback.
- **Trình tự:** 1) Nhận click hoặc key activation theo HTML browser behavior. 2) Không có destination/API handler. 3) Không thực hiện auth check hoặc notification list. 4) Không cập nhật page state. 5) Không suy shell menu hoặc active route từ data-path. 6) Không lưu state. 7) Không có success/error response. 8) Đích đến cần router/shell owner xác nhận.
- **Kết quả:** Tất cả là static/unwired navigation. System/RBAC copy không chứng minh health hay quyền.

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
