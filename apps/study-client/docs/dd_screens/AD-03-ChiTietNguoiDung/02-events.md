# AD-03 — Events (đặc tả xử lý)

## 1. Event index
| Event ID trong package | Source Event ID / heading | Chi tiết |
|---|---|---|
| `AD-03-EV-001` | `Source heading` / EV-01 — Mở AD-03 và lấy chi tiết user | See source event detail below |
| `AD-03-EV-002` | `Source heading` / EV-02 — Quay lại AD-02 | See source event detail below |
| `AD-03-EV-003` | `Source heading` / EV-03 — Chuyển sang AD-04 để chỉnh sửa | See source event detail below |
| `AD-03-EV-004` | `Source heading` / EV-04 — Chuyển sang AD-05 để khóa/trạng thái/xóa | See source event detail below |
| `AD-03-EV-005` | `Source heading` / EV-05 — Hiển thị nhật ký/audit và bảo mật | See source event detail below |
| `AD-03-EV-006` | `Source heading` / EV-06 — Shell, notification, profile và footer navigation | See source event detail below |

> Event IDs trong package là alias để theo template; Source Event IDs, steps và API links giữ theo DD nguồn. Alias không chứng minh event runtime.

## 2. Chi tiết event từ DD nguồn

### Trích từ DD nguồn: D. Đặc tả chi tiết từng sự kiện

### EV-01 — Mở AD-03 và lấy chi tiết user

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | Page route entry từ AD-02 hoặc deep link; kích hoạt bởi router khi route được wire. |
| Điều kiện tiên quyết | Route tồn tại; user ID được truyền; session/token còn hiệu lực; quyền quản lý user được owner xác nhận. API hiện kiểm tra Bearer/JWT và claim `ADMIN` trước parse/query. |
| Input | Path `user_id` dạng raw string do route cung cấp, kỳ vọng lấy từ API #68 `items[].id`; `Authorization: Bearer <token>`; `X-Trace-Id` tùy chọn theo API DD/middleware. Không có query/body. Không gửi email/phone. |
| API | **#69** `GET /api/v1/admin/users/{user_id}`. Catalog response `ApiEnvelope<UserProfile>`. Runtime source parse signed-int64; malformed/out-of-range → 404 theo fallback local. |

**Quy trình xử lý**

1. Resolve user ID từ route. Giữ nguyên signed-int64 representation khi truyền; không chuyển đổi sang UUID hay tìm qua email.
2. Đưa page vào `loading`. Kiểm tra có token/session theo auth shell đã duyệt; frontend không tự coi local UI badge là quyền truy cập.
3. Gửi GET #69 với path ID và Bearer token. Không gửi request body/query; không gọi API #68 lại trừ khi AD-02/navigation state contract yêu cầu riêng.
4. Backend shared guard xác thực principal/role trước khi parse path hoặc query row. Current source yêu cầu claim `ADMIN`; quyền user management cụ thể còn DERIVED/open.
5. Nhận HTTP response và kiểm tra `success`, `businessCode`, `data`, `meta`, `traceId`. Success theo source là HTTP 200 + `DESIGN_RESOURCE_RETRIEVED` + profile object.
6. Map `id`, `full_name`, `email`, `phone`, `role`, `status` vào #22, #19, #20, #24, #25, #26. Giữ nullable `phone` theo model; không tạo giá trị thay thế. `avatar_url`, `created_at`, `updated_at` không có slot trong screenshot. Không kỳ vọng `bio` từ runtime.
7. Chuyển sang `ready` chỉ sau khi profile hợp lệ. Không render `0 audit records`, sync state hoặc retention từ response #69; không kết luận profile rỗng từ `data:null` trên lỗi.
8. Ánh xạ lỗi: 401 → unauthenticated/auth shell; 403 → forbidden; 404 → not-found; 500/network → error state. Nội dung auth shell, retry/timeout policy và UI copy chưa có source/contract, cần dùng chuẩn frontend được duyệt.
9. Không có mutation, cache invalidation, optimistic update, retry count hoặc timeout rule được định nghĩa cho AD-03. Đây là GET; nếu cần retry policy phải theo shared client contract, không tự đặt tại screen DD.

**Kết quả / ngoại lệ**

- **200:** profile object hợp lệ; render các field được phép. Trace ID hỗ trợ correlation; không hiển thị raw token/PII trong log.
- **401:** `DESIGN_AUTHENTICATION_REQUIRED`; không render dữ liệu cũ như mới.
- **403:** `DESIGN_ACCESS_DENIED`; không vượt quyền bằng client-side guard.
- **404:** `DESIGN_RESOURCE_NOT_FOUND`; current source dùng cho ID malformed/out-of-range hoặc không có row. Hai nhánh path/no-row là mapping local được DD API đánh dấu DERIVED.
- **500:** `DESIGN_INTERNAL_ERROR`; source rollback an toàn khi query/mapping error và không trả raw SQL/detail.
- **Network/timeout:** inventory chưa quy định; hiển thị error state theo UI/API client convention sau khi được chốt, không hiển thị như 404 hay “chưa đồng bộ”.

### EV-02 — Quay lại AD-02

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | #10 và phần “Danh sách tài khoản” của #8. |
| Input | Current user ID không cần gửi trong URL quay lại. Bộ lọc/page của AD-02 chỉ giữ nếu có navigation-state contract. |
| Processing | Điều hướng đến route AD-02 đã phê duyệt; không gọi API từ nút back; nếu AD-02 tự tải lại thì xử lý trong DD AD-02/#68. |
| Result / exception | Hiển thị list route. Route hiện là đề xuất; prototype dùng fragment và chưa có router. Không đưa PII vào URL/history state ngoài quy định được duyệt. |

### EV-03 — Chuyển sang AD-04 để chỉnh sửa

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | #15 — “Chỉnh sửa thông tin (AD-04)”. |
| Current state | Button `disabled` và `aria-disabled=true`; prototype không có click handler. |
| Gating | Giữ disabled đến khi Admin policy, AD-04 route, editable field rules và API #70 request body/role rules được xác nhận. |
| Processing khi được wire | Điều hướng ID hiện tại sang AD-04; không PUT từ AD-03. AD-04 định nghĩa #70, validation, dirty state và lỗi. |
| Result | Quay lại hoặc refresh AD-03 theo flow AD-04 đã chốt. Không tự suy ra API #70 body hoặc thành công chỉ từ AC branch. |

### EV-04 — Chuyển sang AD-05 để khóa/trạng thái/xóa

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | #17 — “Khóa hoặc thay đổi trạng thái (AD-05)”. |
| Current state | Button `disabled` và `aria-disabled=true`; prototype không có handler. |
| Gating | Giữ disabled đến khi status/delete policy, confirmation, lifecycle, quyền và AD-05 contract được duyệt. |
| Processing khi được wire | Chuyển ID sang AD-05. #71/#72 thuộc màn hình đích; AD-03 không PATCH/DELETE. Không mặc định session revoke hoặc token invalidation. |
| Result | Thành công/refresh list/detail theo DD AD-05; conflict/404/validation handling phải theo source/contracts của màn hình đó. |

### EV-05 — Hiển thị nhật ký/audit và bảo mật

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | #11 subtitle, #21 heading/count, #23 empty panel, #27 retention/security note, #29 privacy banner, #30 RBAC/audit badge. |
| Current state | Tất cả là static copy. API #69 không trả session history, permission events, count, retention, system health, audit status hay compliance proof. |
| Điều kiện để triển khai | Có API/event source được duyệt, schema/actor/time/action mapping, permission/PII policy, retention semantics và empty/error/loading states. |
| Xử lý hiện tại | Không tạo request ngầm, không diễn giải count `0` là không có sự kiện, không dùng GET #69 làm audit feed. Giữ nội dung là prototype-only cho tới khi contract được bổ sung. |
| Kết quả | Blocker mở; chưa có UI state/data mapping có thể triển khai cho audit panel. |

### EV-06 — Shell, notification, profile và footer navigation

| Thuộc tính | Đặc tả |
|---|---|
| Element / trigger | #1–#7, #32; click nav, notification, admin avatar/profile, policy/RBAC/support links. |
| Input | Không có business data đầu vào trong AD-03; destination phụ thuộc screen/router catalog tương ứng. |
| Processing | Chỉ dùng route/action đã được định nghĩa ở screen tương ứng. Không kích hoạt API từ badge “System Normal”, “RBAC”, “sync” hay legal copy. |
| Current/result | Anchors là `#` hoặc không có handler. Các đích và profile/notification contracts chưa được AD-03 chứng minh; không giả lập điều hướng hoặc phản hồi. |

## Trace links
- [UI Elements](01-ui-elements.md) · [API Integration](04-api-integration.md) · [Business Rules](05-business-rules.md) · [Navigation](06-navigation.md) · [Test Cases](07-test-cases.md)
