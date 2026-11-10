# AD-05 — Khóa/mở khóa/xóa tài khoản · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-05` |
| Module | Admin |
| Route | `/admin/users/:userId/actions` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED — status, deletion, permission, session and audit policies need approval`; **Implementation:** `BLOCKED — Study Web route/client are UNWIRED and product decisions remain open` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-05.md](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05.md), [AD-05_PLAN.md](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_PLAN.md), [AD-05_markers.json](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Xem trạng thái user và chỉ cho action theo policy đã duyệt; không mặc định session revoke, audit hoặc hard delete.
- In-scope: GET #69 → PATCH #71 hoặc DELETE #72 → refresh #68/#69 theo AC-31; #71 body/status và #72 delete policy cần duyệt; không tự giả định token effect.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-31 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Xem trạng thái user và chỉ cho action theo policy đã duyệt; không mặc định session revoke, audit hoặc hard delete. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #69, #71, #72
- Liên kết màn hình dự kiến: [AD-02](../AD-02-DanhSachNguoiDung/00-overview.md), [AD-03](../AD-03-ChiTietNguoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | no-selection/loading/ready-read-only/mode-selected/submitting/unauthenticated/forbidden/not-found/validation-error/success/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-05 source screen.png](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen_annotated.png))
- Luồng: GET #69 → PATCH #71 hoặc DELETE #72 → refresh #68/#69 theo AC-31; #71 body/status và #72 delete policy cần duyệt; không tự giả định token effect.
- Priority: P2; Gate/source status: **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** #71 body/status/session, #72 delete/visibility/retention, Admin permission/audit/safeguards và Study Web UNWIRED còn mở; RUNTIME NOT VERIFIED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-05 — Khóa/mở khóa/xóa tài khoản

> **Screen ID:** AD-05 · **Surface:** Dialog / action page · **Priority:** P2
> **DD status:** `BLOCKED — status, deletion, permission, session and audit policies need approval`
> **Implementation:** `BLOCKED — Study Web route/client are UNWIRED and product decisions remain open` · **Runtime:** `NOT VERIFIED`

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

| Thuộc tính | Đặc tả |
|---|---|
| Mục tiêu | Cho Admin có quyền theo AC-31 xem trạng thái tài khoản đã chọn và thực hiện hành động trạng thái hoặc xóa chỉ khi các chính sách tương ứng được duyệt. |
| Actor / quyền | Admin đã xác thực và được cấp quyền quản lý người dùng theo AC-31. API catalog ghi Bearer JWT/Admin; local source kiểm tra claim `ADMIN`. Mapping claim đó sang quyền AC-31, tenant/scope, MFA/step-up, self-lock và last-Admin safeguards chưa được xác nhận. |
| Route | `/admin/users/:userId/actions` là route đề xuất trong inventory, chưa tồn tại trong Study Web source. Path param phải là numeric `user_id` signed-int64; không dùng ID hiển thị kiểu `USR-*`, email hoặc phone. |
| Điều kiện vào | Handoff từ AD-02 hoặc AD-03 có `user_id`; session và permission policy hợp lệ; #69 trả profile được phép hiển thị. Direct entry, thiếu ID hoặc ID sai định dạng phải có trạng thái lỗi theo policy/router còn cần chốt. |
| Điều kiện thực hiện mutation | Chỉ khi request body/status transition của #71 hoặc semantics/retention của #72 được duyệt; phải có permission và safeguard rõ ràng. Lý do kiểm toán chỉ được thu thập/lưu nếu có contract lưu trữ được duyệt. |
| API | #69 `GET /api/v1/admin/users/{user_id}` để đọc hồ sơ. #71 `PATCH /api/v1/admin/users/{user_id}/status` để đổi trạng thái. #72 `DELETE /api/v1/admin/users/{user_id}` để xóa theo contract. #71 catalog/AC không khai báo body; #72 không có body/query. |
| Liên kết | AD-02 danh sách → AD-03 chi tiết → AD-05 action; AC-31 mô tả load lại list/detail sau action. Chuyển tiếp và quay lại phải giữ numeric `user_id` khi policy/route yêu cầu. Hiện prototype back links cùng trỏ `/admin/users`, chưa có router. |
| Hậu điều kiện | Chỉ coi mutation thành công khi HTTP/business code và payload đúng contract. Inventory đề nghị refresh #68/#69; đích sau #72, visibility của `DELETED` và selected-user context còn phải được duyệt. |

### Expected behavior và current behavior

| Chủ đề | Expected / contract | Current source hoặc prototype |
|---|---|---|
| User-management permission | AC-31 yêu cầu Admin có quyền quản lý user. | Catalog yêu cầu Bearer JWT/Admin; #69/#71/#72 local source dùng shared `ADMIN` guard. Mapping `ADMIN` claim sang permission AC-31 và safeguards chưa được chứng minh. |
| #71 request/status | AC-31 và API catalog chỉ thể hiện path, không có body/status allowlist. | Local route/model hiện yêu cầu strict `{status: "ACTIVE"|"SUSPENDED"}`; đây là `DERIVED`, không phải approved contract. Chỉ trạng thái hiện tại `ACTIVE`/`SUSPENDED` được local view đổi; ví dụ `DELETED` và `PENDING_EMAIL_VERIFICATION` → 422. Cùng trạng thái vẫn cập nhật `updated_at`; gửi SUSPENDED lần nữa có thể revoke các refresh-token row eligible mới phát sinh. |
| #71 session effect | AC-31 chỉ nêu revoke session “if needed”; không chốt mọi access/session token. | Local suspend thu hồi refresh-token row chưa revoke và chưa hết hạn; stateless access JWT có thể còn dùng đến hết hạn. Activate không khôi phục refresh token đã revoke. |
| #72 delete | AC-31 mô tả logical delete/anonymize theo policy; catalog không có body. | Local source chỉ đặt `users.status='DELETED'`, cập nhật `updated_at`; giữ profile/quan hệ/refresh-token rows, không anonymize, không ghi audit, không kiểm tra dependency. `deleted_at` response là alias của `updated_at`, không phải cột xóa riêng. |
| Sau xóa | Visibility/retention/điều hướng phải theo policy được duyệt. | #68/#69 local query không loại `DELETED`; bản ghi vẫn hiển thị. #72 lặp lại hoặc không tìm thấy đều 404. #03 login/refresh yêu cầu `ACTIVE`; access JWT đang phát hành có thể vẫn còn hiệu lực. |
| Audit reason | Chỉ yêu cầu khi API/persistence/audit contract xác định được. | Prototype đánh dấu reason bắt buộc, nhưng textarea disabled; #71 không nhận reason và #72 không có body. Không API nào trong flow ghi audit. |
| Client/runtime | Route, auth, API client và UI phải được implement để dùng màn hình. | AD-05 là HTML tĩnh. Không có user ID, fetch/XHR, handler, Study Web route/client/package manifest hoặc editable app source. Study Web hiện `UNWIRED`. |
| Mockup claims | Health, RBAC, read-only gate, audit/ISO và session impact chỉ hiển thị khi có nguồn. | Những claim này là copy tĩnh; không được #69/#71/#72 xác minh. Hai back links là `/admin/users`; nav/footer links `#`; action tabs không có listener; confirm và reason disabled. |

### Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global DD plan](../../screen_stitch/dd_screens/PLAN.md) · [AD-05 plan](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_PLAN.md) · [AD-05 markers](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.json)
- [Original screenshot](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen.png) · [Annotated screenshot](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen_annotated.png) · [HTML prototype](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/code.html) · [SVG marker overlay](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.svg)
- [AD-02 list](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md) · [AD-03 detail](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md) · [AD-04 update](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md)
- [API catalog](../../../../../docs/lists/list_api.md) · [AC-31 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- #69 local route/source: [v1 router](../../../../study-server/app/api/v1.py) · [API #69 module](../../../../study-server/app/modules/admin/api_69_admin_user_detail)
- #71 local source: [API #71 module](../../../../study-server/app/modules/admin/api_71_admin_user_status) · [focused test source](../../../../study-server/tests/modules/admin/api_71_admin_user_status/test_admin_user_status.py) · [Draft API DD](../../../../study-server/docs/dd/71_admin_user_status/02_Overview.md)
- #72 local source: [API #72 module](../../../../study-server/app/modules/admin/api_72_admin_user_delete) · [focused test source](../../../../study-server/tests/modules/admin/api_72_admin_user_delete/test_admin_user_delete.py) · [Draft API DD](../../../../study-server/docs/dd/72_admin_user_delete/02_Overview.md)
- [API #03 auth source](../../../../study-server/app/modules/guest/api_03_auth_login) · [Study Web boundary](../../../../../.agents/web-work/study/AGENTS.md) · [Study Web design target](../../../../../.agents/web-study/design.md)
