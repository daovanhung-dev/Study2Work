# AD-02 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-02-API-001` | #68 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #68
- Orchestration/data notes: GET #68 với filter/page và giữ query URL; local source chỉ search name/email, exact-match role/status, fixed page 20. Không suy ra search ID hoặc tạo/export user từ mockup.
- BE/source status và gate: **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** Study Web UNWIRED; role/status options và ID-search mismatch; Add/export/audit/sync unsupported; Admin permission, PII/lifecycle, live schema còn mở; RUNTIME NOT VERIFIED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: UserProfile mapping có thể dùng từ API #68

| Trường response | Kiểu / null | Ý nghĩa cho AD-02 | Giới hạn |
|---|---|---|---|
| `id` | integer, signed-int64 candidate | Cột mã user; dùng làm `user_id` khi mở detail. | Local source đọc legacy BIGINT; live schema chưa xác minh. |
| `full_name` | string | Cột họ và tên. | Không có display-name khác trong response này. |
| `email` | string | Cột email. | PII visibility cần owner xác nhận. |
| `role` | string | Cột vai trò. | Enum members và UI label mapping chưa được duyệt. |
| `status` | string | Cột trạng thái. | Enum members và nhãn UI chưa được duyệt. |
| `created_at` | datetime | Cột ngày tạo. | Quy tắc timezone/format hiển thị chưa được chốt. |
| `avatar_url` | string hoặc null | Có thể dùng cho avatar nếu UI quyết định hiển thị. | Screenshot không có avatar column trong bảng. |
| `phone` | string hoặc null | Không hiển thị trên bảng hiện tại. | Không thêm PII này vào list UI khi chưa có yêu cầu/quyền rõ ràng. |
| `updated_at` | datetime | Có trong profile response. | Không có cột tương ứng trong screenshot; không cần render ở AD-02. |
| `bio`, `password_hash` | Không có | Không render. | API #68 bỏ `bio`; SQL không chọn `password_hash`. |

### Trích từ DD nguồn: Nguồn truy vết

- [Inventory và flow screen](../../list_screen.md) · [Tracker DD](../../screen_stitch/dd_screens/PLAN.md)
- [Ảnh gốc](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/screen.png) · [HTML prototype](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/code.html) · [Ảnh marker](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/screen_annotated.png)
- [API catalog #68](../../../../../docs/lists/list_api.md) · [AC-31 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #68 overview](../../../../study-server/docs/dd/68_admin_users_list/02_Overview.md) · [request](../../../../study-server/docs/dd/68_admin_users_list/03_Request.md) · [response](../../../../study-server/docs/dd/68_admin_users_list/04_Response.md) · [open questions](../../../../study-server/docs/dd/68_admin_users_list/OPEN_QUESTIONS.md)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web source boundary](../../../../../.agents/web-work/study/AGENTS.md)
- [Current API route](../../../../study-server/app/api/v1.py) · [API #68 query/view](../../../../study-server/app/modules/admin/api_68_admin_users_list/view.py) · [SQL](../../../../study-server/app/modules/admin/api_68_admin_users_list/query.py) · [validation](../../../../study-server/app/modules/admin/api_68_admin_users_list/validate.py) · [HTTP test source](../../../../study-server/tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py)

### Trích từ DD nguồn: Screen states và API mapping

| State | Entry condition | Expected UI | Current evidence |
|---|---|---|---|
| `loading` | Route load hoặc query thay đổi; #68 pending. | Giữ filter context, báo đang tải và tránh submit lặp. | Prototype không có request/loading state. |
| `ready` | HTTP 200, `items.length > 0`. | Render các row/metadata; actions điều hướng theo quyền/contract. | Không có row design/data. |
| `empty` | HTTP 200, `items=[]`; có thể do chưa có user hoặc filter không match. | Nói rõ không có kết quả; không kết luận sync lỗi hoặc đang chạy. | Mockup static chờ sync; không phân biệt no-match và sync. |
| `filter-error` | #68 trả 422 cho `page` parse/range. | Giữ filter; liên kết lỗi với page state; cho phép sửa/đặt lại. Filter role/status unknown hiện không gây 422. | Chưa có client validation/error state. |
| `unauthenticated` | #68 trả 401. | Dùng auth shell/session handling đã được duyệt. | Route/auth shell chưa có trong Study Web source. |
| `forbidden` | #68 trả 403 khi token không có ADMIN claim. | Hiển thị access denied theo shared auth UX; không render danh sách cũ như mới. | Không có role guard ở client. |
| `error` | #68 trả 500 hoặc network không xác định. | Thông báo an toàn và nút thử lại khi khả dụng; không lộ query/PII/raw SQL. | Refresh disabled; chưa có error handler. |

**Empty pagination:** API trả `page=1,size=20,total=0,total_pages=0`; mockup `0/0` chưa xác định có nghĩa current page hay record count. Chốt copy/UI representation trước implement.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md)
