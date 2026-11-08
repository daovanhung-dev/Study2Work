# AD-02 — Danh sách người dùng · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-02` |
| Module | Admin |
| Route | `/admin/users` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED — decisions remain open` · **Implementation:** `BLOCKED — Study Web is UNWIRED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-02.md](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md), [AD-02_PLAN.md](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02_PLAN.md), [AD-02_markers.json](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Bảng users, keyword, status, role, pagination; chọn user để mở AD-03/AD-04; API #68 chỉ đọc.
- In-scope: GET #68 với filter/page và giữ query URL; local source chỉ search name/email, exact-match role/status, fixed page 20. Không suy ra search ID hoặc tạo/export user từ mockup.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-31 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Bảng users, keyword, status, role, pagination; chọn user để mở AD-03/AD-04; API #68 chỉ đọc. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #68
- Liên kết màn hình dự kiến: [AD-03](../AD-03-ChiTietNguoiDung/00-overview.md), [AD-04](../AD-04-ChinhSuaNguoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/empty/ready/filter-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-02 source screen.png](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/screen_annotated.png))
- Luồng: GET #68 với filter/page và giữ query URL; local source chỉ search name/email, exact-match role/status, fixed page 20. Không suy ra search ID hoặc tạo/export user từ mockup.
- Priority: P1; Gate/source status: **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** Study Web UNWIRED; role/status options và ID-search mismatch; Add/export/audit/sync unsupported; Admin permission, PII/lifecycle, live schema còn mở; RUNTIME NOT VERIFIED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-02 — Danh sách người dùng

> **Screen ID:** AD-02 · **Surface:** Page · **Priority:** P1
> **DD status:** `BLOCKED — decisions remain open` · **Implementation:** `BLOCKED — Study Web is UNWIRED` · **Runtime:** `NOT VERIFIED`

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

| Thuộc tính | Đặc tả |
|---|---|
| Route đề xuất | `/admin/users` — inventory đề xuất; current Study Web chưa có route này. |
| Actor / precondition | Admin đã đăng nhập và có quyền quản lý user theo AC-31. API #68 hiện yêu cầu JWT claim `ADMIN`; việc claim này đại diện cho user-management permission là fallback `DERIVED`, chưa được owner xác nhận. |
| Mục đích | Tra cứu danh sách tài khoản bằng keyword, role, status và page; chọn user để mở AD-03 hoặc AD-04. API #68 chỉ đọc danh sách. |
| API chính | `GET /api/v1/admin/users` (#68), Bearer JWT; query `role?:string`, `status?:string`, `keyword?:string`, `page?:int32`; không có body, `size` hay `sort`. |
| Success | `ApiEnvelope<Page<UserProfile>>`; `data.items[]` và `data.pagination{page,size,total,total_pages}`. Page mặc định 1, size cố định 20, thứ tự local `id ASC` (`DERIVED`). |
| States | Inventory yêu cầu `loading / empty / ready / filter-error`. Current #68 còn trả 401/403/500; việc trình bày các lỗi quyền theo auth shell và cách hiển thị 500 cần theo UI contract được duyệt. |
| Navigation | AD-03 `/admin/users/:userId` để xem chi tiết; AD-04 `/admin/users/:userId/edit` để chỉnh sửa. AC-31 tiếp tục tới AD-05 cho #71/#72. |

API #68 direct contract đã đồng bộ catalog/AC thành `ApiEnvelope<Page<UserProfile>>`. Các quy tắc page default/size/order, keyword normalization, exact filter và claim-to-permission mapping hiện là local `DERIVED`; tài liệu API #68 còn `Draft — Needs Confirmation`.

### UserProfile mapping có thể dùng từ API #68

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

### Tách expected behavior và current behavior

| Chủ đề | Expected behavior | Current behavior / bằng chứng |
|---|---|---|
| Route và data | Mở `/admin/users`, gọi #68 và hiển thị Page theo filter/page được duyệt. | Study Web không có editable source, package manifest hay route. HTML là prototype tĩnh. |
| Search/filter | Inventory yêu cầu keyword, role, status và giữ query URL. | HTML có input/select nhưng không request. Keyword copy còn nói tìm theo user ID; #68 chỉ tìm tên/email. UI values `student/instructor/admin` và `active/locked/pending`; #68 exact-match chuỗi và không khai báo enum list. |
| Pagination | 1-based `page`; UI dùng `total/total_pages`; size do server cố định. | Nút trước/sau disabled; mockup hiển thị `0/0`. API empty Page trả `page=1,total_pages=0`, nên cách biểu diễn empty-page cần quyết định. |
| Row actions | Chọn user đi tới #69; update/status/delete theo nhánh AC-31 và màn tương ứng. | Không có row vì prototype ở empty state; không có action handler. |
| Create/export/audit | Chỉ enable khi có contract, route và quyền phù hợp. | Add user, Export, help, sync, security/RBAC và audit copy là static; #68 read-only và không trả audit/sync data. |
| Runtime | Chỉ xác nhận sau khi Study Web route/client và serving được kiểm tra. | Study Web `UNWIRED`; API #68 có local source/test nhưng fake-DB tests không chứng minh live schema/deployment. |

### Nguồn truy vết

- [Inventory và flow screen](../../list_screen.md) · [Tracker DD](../../screen_stitch/dd_screens/PLAN.md)
- [Ảnh gốc](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/screen.png) · [HTML prototype](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/code.html) · [Ảnh marker](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/screen_annotated.png)
- [API catalog #68](../../../../../docs/lists/list_api.md) · [AC-31 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #68 overview](../../../../study-server/docs/dd/68_admin_users_list/02_Overview.md) · [request](../../../../study-server/docs/dd/68_admin_users_list/03_Request.md) · [response](../../../../study-server/docs/dd/68_admin_users_list/04_Response.md) · [open questions](../../../../study-server/docs/dd/68_admin_users_list/OPEN_QUESTIONS.md)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web source boundary](../../../../../.agents/web-work/study/AGENTS.md)
- [Current API route](../../../../study-server/app/api/v1.py) · [API #68 query/view](../../../../study-server/app/modules/admin/api_68_admin_users_list/view.py) · [SQL](../../../../study-server/app/modules/admin/api_68_admin_users_list/query.py) · [validation](../../../../study-server/app/modules/admin/api_68_admin_users_list/validate.py) · [HTTP test source](../../../../study-server/tests/modules/admin/api_68_admin_users_list/test_admin_users_list.py)
