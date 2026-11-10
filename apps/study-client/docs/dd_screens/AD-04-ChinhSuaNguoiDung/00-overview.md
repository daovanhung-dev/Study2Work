# AD-04 — Chỉnh sửa người dùng · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-04` |
| Module | Admin |
| Route | `/admin/users/:userId/edit` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED — API #70 body/role contract and user-management policies need approval`<br>; **Implementation:** `BLOCKED — Study Web is UNWIRED and product decisions remain open` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-04.md](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md), [AD-04_PLAN.md](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_PLAN.md), [AD-04_markers.json](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Chỉnh field/role chỉ sau khi API body, permission và field ownership được duyệt; dirty state + cancel về AD-03.
- In-scope: Numeric ID từ AD-03; GET #69 → PUT #70 → GET #69. Catalog/AC bỏ body; local strict body `full_name, phone, avatar_url, role` là `DERIVED`; không gửi email/status/adminNotes hoặc tự map `lecturer`.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-31 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Chỉnh field/role chỉ sau khi API body, permission và field ownership được duyệt; dirty state + cancel về AD-03. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #69, #70
- Liên kết màn hình dự kiến: [AD-03](../AD-03-ChiTietNguoiDung/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/dirty/saving/validation-error/unauthenticated/forbidden/not-found/saved-refresh-error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-04 source screen.png](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/screen_annotated.png))
- Luồng: Numeric ID từ AD-03; GET #69 → PUT #70 → GET #69. Catalog/AC bỏ body; local strict body `full_name, phone, avatar_url, role` là `DERIVED`; không gửi email/status/adminNotes hoặc tự map `lecturer`.
- Priority: P1; Gate/source status: **R**; #70 source-backed locally nhưng body/role `DERIVED`; **DD BLOCKED; IMPLEMENTATION BLOCKED:** body approval, role/PII/permission/ID-route/gate policy và Study Web `UNWIRED`; **RUNTIME NOT VERIFIED**

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-04 — Chỉnh sửa người dùng

> **Screen ID:** AD-04 · **Surface:** Page · **Priority:** P1<br>
> **DD status:** `BLOCKED — API #70 body/role contract and user-management policies need approval`<br>
> **Implementation:** `BLOCKED — Study Web is UNWIRED and product decisions remain open` · **Runtime:** `NOT VERIFIED`

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

| Thuộc tính | Đặc tả |
|---|---|
| Mục tiêu | Cho Admin chỉnh sửa các trường được hợp đồng và chính sách quản lý user cho phép. Inventory mô tả luồng `GET #69 → PUT #70 → GET #69`, dirty state và Cancel. |
| Actor / quyền | Admin đã xác thực và có quyền quản lý user theo AC-31. Catalog ghi Bearer JWT/Admin; source cục bộ kiểm tra claim `ADMIN`. Việc claim này đáp ứng quyền AC-31 là fallback `DERIVED`, chưa được owner xác nhận. |
| Route màn hình | `/admin/users/:userId/edit` theo inventory; đây là route đề xuất, chưa có Study Web router/client. API dùng `/api/v1/admin/users/{user_id}`. |
| Điều kiện vào | AD-03 chuyển tiếp ID user số từ #68/#69. API #69 trả profile hợp lệ và các trường được phép hiển thị theo policy. Không dùng mã `USR-*`, email hoặc phone làm path. |
| Điều kiện lưu | User-management policy, #70 request body, mapping role, PII và route/navigation được duyệt. Trong prototype hiện tại các trường và Save đều bị khóa. |
| API | #69 `GET /api/v1/admin/users/{user_id}`; #70 `PUT /api/v1/admin/users/{user_id}`. Cả hai dùng Bearer JWT/Admin, path `user_id:int64!`, response `ApiEnvelope<UserProfile>`. #70 catalog/AC chưa khai báo body. |
| Liên kết | AD-03 → AD-04 → AD-03; AD-05 là luồng trạng thái/xóa riêng. Handoff và route cần truyền cùng `user_id` số. |

### API #69 profile và #70 body candidate

| Field | Kiểu / quy tắc hiện có | Dùng trên AD-04 |
|---|---|---|
| `id` | `int64` path/ID candidate trong local legacy API. | Khóa user cho GET/PUT; không tự ánh xạ `USR-9281-VN` sang số. Live schema/deploy chưa xác minh. |
| `full_name` | #69 trả `string`; local #70 body yêu cầu string, trim, không rỗng, tối đa 150 ký tự. Body/rule #70 là `DERIVED`. | Candidate field có thể sửa sau khi body được duyệt. |
| `email` | #69 trả `string`; không có trong body/update #70. | Chỉ đọc; quy tắc hiển thị/masking PII chưa duyệt. |
| `phone` | #69 trả `string \| null`; local #70 yêu cầu key, nhận string/null, trim, blank thành null, tối đa 20 ký tự nếu là string. | Không có input trong prototype; phải giữ nguyên từ #69 nếu hợp đồng full-replacement được duyệt. |
| `avatar_url` | #69 trả `string \| null`; local #70 yêu cầu key, nhận string/null, trim, blank thành null; không kiểm tra URL syntax/length. | Không có input trong prototype; phải giữ nguyên từ #69 nếu hợp đồng full-replacement được duyệt. |
| `role` | #69 trả `string`; local #70 body chỉ nhận `STUDENT`, `MENTOR`, `ADMIN`. Allowlist và rule chuyển vai trò đều `DERIVED`. | Prototype hiển thị `student/lecturer/admin`; không tự map `lecturer` thành `MENTOR`. |
| `status` | #69 trả `string`; không thuộc body/update #70. #71 là API trạng thái riêng, ngoài mutation AD-04. | Chỉ đọc theo policy; không gửi `active/locked/pending` vào #70. |
| `adminNotes` | Không có trong #69/#70. | Không lưu/gửi; prototype textarea hiện bị khóa. Cần contract riêng nếu nghiệp vụ yêu cầu. |
| `created_at`, `updated_at` | Có trong UserProfile success response. | Hiển thị nếu có thiết kế và định dạng được duyệt; không coi actor/audit là các timestamp này. |

### Expected/current và trạng thái triển khai

| Chủ đề | Expected / contract | Current source hoặc prototype |
|---|---|---|
| API #70 body | Body cần được catalog/API owner duyệt. | Catalog/AC bỏ trống body; model runtime có body strict bốn key (`full_name`, `phone`, `avatar_url`, `role`) và được ghi `DERIVED`; API DD còn Draft. |
| Cập nhật | Chỉ sửa field/role được phê duyệt; không cập nhật email/status/notes nếu API không hỗ trợ. | Local query chỉ cập nhật `full_name`, `phone`, `avatar_url`, `role`, `updated_at`; không ghi audit và không thu hồi JWT role claim. |
| UI | Chỉ bật edit/save khi có schema, permission, route và policy. | Prototype là HTML tĩnh; inputs/selects/textarea và Save disabled; không có client API call. Study Web hiện `UNWIRED`. |
| ID/điều hướng | Truyền numeric `user_id` từ AD-03 và quay về cùng user sau Cancel/success theo route được duyệt. | Ảnh dùng `USR-9281-VN`; Back đi `/admin/users/USR-9281-VN/details`; Cancel đi `/admin/users`. Không có ánh xạ ID hoặc router. |
| Gate/audit/support | Chỉ hiển thị trạng thái có API/policy nguồn. | Gate, 85% sync, audit, SSO actor, compliance, RBAC-token, API verified và gửi yêu cầu đều là copy tĩnh, không có handler/endpoint #69/#70. |
| Validation/auth order | Error behavior phải theo API contract được duyệt. | Typed body có thể bị FastAPI request validation từ chối trước khi view chạy auth guard; API DD/context nói auth trước body. Test source không phân định invalid body + auth lỗi; thứ tự chưa được xác minh. |

### Nguồn truy vết

- [Inventory](../../list_screen.md) · [Kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) · [AD-04 plan](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_PLAN.md) · [AD-03](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md)
- [Ảnh gốc](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/screen.png) · [Ảnh chú thích](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/screen_annotated.png) · [HTML prototype](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/code.html) · [Marker map](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_markers.json) · [SVG overlay](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04_markers.svg)
- [API catalog](../../../../../docs/lists/list_api.md) · [AC-31 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- API #70 DD: [Overview](../../../../study-server/docs/dd/70_admin_user_update/02_Overview.md) · [Request](../../../../study-server/docs/dd/70_admin_user_update/03_Request.md) · [Response](../../../../study-server/docs/dd/70_admin_user_update/04_Response.md) · [Mapping](../../../../study-server/docs/dd/70_admin_user_update/05_Data_Mapping.md) · [Errors](../../../../study-server/docs/dd/70_admin_user_update/06_Error.md) · [Open questions](../../../../study-server/docs/dd/70_admin_user_update/OPEN_QUESTIONS.md)
- API #70 source: [route](../../../../study-server/app/api/v1.py) · [model](../../../../study-server/app/modules/admin/api_70_admin_user_update/models.py) · [validation](../../../../study-server/app/modules/admin/api_70_admin_user_update/validate.py) · [query](../../../../study-server/app/modules/admin/api_70_admin_user_update/query.py) · [view](../../../../study-server/app/modules/admin/api_70_admin_user_update/view.py) · [focused test source](../../../../study-server/tests/modules/admin/api_70_admin_user_update/test_admin_user_update.py)
- [Study Web boundary](../../../../../.agents/web-work/study/AGENTS.md) · [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Server API source status](../../../../../.agents/project/source-status.md)
