# AD-02 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-02-EV-001` | Source event section bundle | See source DD event section |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả sự kiện

| Event | Trigger | Expected handling | API / error | Current prototype / trạng thái |
|---|---|---|---|---|
| EV-01 — Khởi tạo danh sách | Mở AD-02 hoặc URL query thay đổi | Xác nhận Admin session/policy; parse filter/page từ URL; gọi #68; map Page. Query URL behavior là inventory requirement, chưa có client source. | #68 Bearer JWT + `role/status/keyword/page`; 200 `Page<UserProfile>`. | Không có route/caller/API. |
| EV-02 — Tìm kiếm keyword | Nhập keyword | Khi submit/debounce policy được duyệt, update URL và gọi #68. Tìm tên/email thôi; literal substring; không tìm ID. | `keyword?:string`; blank sau trim tương đương không filter. | Input chỉ nhận text, không handler. |
| EV-03 — Lọc role/status | Thay select | Update URL/refetch theo exact string values trong contract; enum/value mapping chưa được duyệt. | `role/status?:string`; unknown string hiện không bị 422 và có thể cho empty 200. | Values lowercase; không listener/refetch. |
| EV-04 — Đặt lại bộ lọc | Click Reset | Xóa `role/status/keyword` khỏi URL; page behavior (reset về 1 hay giữ) cần product decision trước khi wire. | Gọi lại #68 theo URL còn lại sau khi chốt. | Clear local inputs và focus search; URL/data không đổi. |
| EV-05 — Chuyển trang | Click previous/next | Set 1-based `page`; size/order do server; update URL; disable controls theo metadata. | Page default 1, size 20; malformed/out-of-range page → 422. | Nút trước/sau disabled. |
| EV-06 — Xem chi tiết user | Chọn row/ID | Dùng `items[].id` để mở AD-03; không dùng email làm route identity. | Handoff sang #69; response/error thuộc AD-03. | Không có row/action ở empty prototype. |
| EV-07 — Chỉnh sửa hoặc status/delete | Chọn action được phép | Điều hướng AD-04/#70 hoặc AD-05/#71/#72; chỉ reload #68 sau success theo flow AC-31. | #68 không ghi dữ liệu; mutation status/error theo DD tương ứng. | Chưa có row controls hoặc handler. |
| EV-08 — Thêm người dùng | Click Add user | Không mở form hoặc gửi request tới API khác trước khi có create-user contract/route. | Không có create API trong AC-31 #68–#72. | Button không có handler. |
| EV-09 — Export | Click Export | Không giả lập download; cần export contract/API, quyền và file URL/result. | #68 không export; #103 là report export khác domain, không được thay thế. | Button không có handler. |
| EV-10 — Refresh / guide | Click Refresh hoặc Guide | Refresh refetch #68; guide chỉ điều hướng tới nội dung đã xác định. | #68 GET; errors theo EV-01. | Refresh disabled; guide không handler. |
| EV-11 — Header/footer navigation | Click nav, notification hoặc footer | Điều hướng theo inventory/route được duyệt; notification/privacy/RBAC/support target còn cần map. | Không thêm API call từ mockup. | 8 placeholder anchors; notification no-op. |
| EV-12 — Hiển thị policy/system status | Tải screen | Render health/audit/sync/assurance chỉ khi có contract/source cho từng claim. | API #68 không có field hoặc side effect tương ứng. | Tất cả copy/badges là static; không dùng như dữ liệu live. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
