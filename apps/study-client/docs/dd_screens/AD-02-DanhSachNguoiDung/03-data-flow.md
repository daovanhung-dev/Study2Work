# AD-02 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: B. Luồng hoạt động tổng thể

### Expected flow — sau khi các blocker được giải quyết

1. Admin mở route được phê duyệt. App xác thực session và quyền user-management theo auth/RBAC contract; không xem badge “RBAC V2.4” trong mockup là bằng chứng quyền đã được kiểm tra.
2. Screen đọc `role`, `status`, `keyword`, `page` từ URL query theo yêu cầu inventory. Gọi `GET #68` với Bearer token và đúng query. Debounce hay nút submit, page reset khi filter thay đổi, và canonical hóa URL cần được chốt ở client design.
3. Khi thành công, map `data.items` vào các cột ID, họ tên, email, role, status, ngày tạo; dùng pagination metadata để render tổng số và page controls. Không hiển thị field ngoài cột được duyệt.
4. `items=[]` là empty Page HTTP 200, không phải lỗi hoặc trạng thái đồng bộ. Không suy ra “chưa đồng bộ auth server” từ response rỗng.
5. Admin chọn một user để mở AD-03 và API #69; edit mở AD-04 và API #70. Nhánh status/delete thuộc AD-05 với #71/#72. Sau mutation thành công, flow AC-31 yêu cầu reload list/detail; AD-02 không tự thực hiện mutation qua #68.

### Current HTML behavior

- Header/footer links dùng `href="#"`; không có app router hoặc client API call.
- Search và hai select chỉ là controls tĩnh. Listener duy nhất là Reset: clear keyword/role/status và focus search; URL không đổi.
- Refresh và hai nút pagination disabled. Add, Export và “Xem hướng dẫn nhập liệu” không có listener.
- Empty state nói dữ liệu đang chờ đồng bộ từ auth server, nhưng API #68 không trả sync state. “System Normal”, “RBAC V2.4”, “Bảo mật cấp 3” và cam kết mọi truy xuất được audit đều là static copy; API #68 không cung cấp health/audit fields hay audit side effect.

### Current server source trace

```text
No Study Web caller/route → apps/study-server/app/api/v1.py:get_admin_users_endpoint
→ get_admin_users(raw Authorization/role/status/keyword/page, Session, trace)
→ shared validate_current_user_request(role="ADMIN") before DB
→ validate page + normalize keyword
→ COUNT_ADMIN_USERS and LIST_ADMIN_USERS over legacy users candidate
→ safe UserProfile projection + Page metadata + success envelope
→ 401/403/422/500 safe envelopes; query/projection failures rollback; no commit/write
```

COUNT và LIST dùng cùng role/status/keyword predicates; page query dùng `LIMIT 20`, offset từ page và `ORDER BY users.id ASC`. Keyword là lowercase literal substring trên `full_name` hoặc `email`; `%`/`_` không phải wildcard. Unknown role/status strings không bị enum validator chặn và có thể cho empty Page. API #68 không tìm theo ID. Catalog/AC response shape khớp current local response; filter, paging, schema target và permission policy vẫn có trạng thái `DERIVED`/Draft.

### Trích từ DD nguồn: E. Trạng thái và điều hướng

### Screen states và API mapping

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

### Navigation / data handoff

| Từ AD-02 | Đích | Handoff | Ranh giới |
|---|---|---|---|
| Chọn user | AD-03 `/admin/users/:userId` | `id` từ `items[]` → #69. | Không đưa email/PII vào URL. |
| Edit | AD-04 `/admin/users/:userId/edit` | `id` → #69 detail và #70 update theo DD màn đó. | Không sửa trực tiếp qua #68. |
| Status/delete action | AD-05 `/admin/users/:userId/actions` | #71 hoặc #72; sau success refetch #68. | Policy/token/lifecycle còn mở; AD-02 chỉ là handoff. |
| Primary navigation | AD-01 hoặc các screen quản trị tương ứng | Dùng route catalog của từng Screen ID. | Prototype anchors hiện là `#`; không khẳng định destination đang chạy. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: GET #68 với filter/page và giữ query URL; local source chỉ search name/email, exact-match role/status, fixed page 20. Không suy ra search ID hoặc tạo/export user từ mockup.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [AD-02](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
