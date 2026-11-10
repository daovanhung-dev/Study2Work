# AD-03 — Chi tiết người dùng · Tổng quan

| Trường | Giá trị |
|---|---|
| Screen ID | `AD-03` |
| Module | Admin |
| Route | `/admin/users/:userId` — route trong inventory, không phải xác nhận router runtime |
| Actor/role | Theo DD nguồn; xem overview/source trace bên dưới |
| DD status | Draft (package được chuyển đổi); source status: **DD status:** `BLOCKED — policy, audit source, and live-schema decisions remain open`<br>; **Implementation:** `BLOCKED — Study Web is UNWIRED` · **Runtime:** `NOT VERIFIED` |
| Owner | Không được xác định trong inventory/DD nguồn đã chuyển; `CẦN_XÁC_NHẬN` |
| Version / last updated | 0.1 / 2026-11-08 |
| Nguồn đối chiếu | [AD-03.md](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md), [AD-03_PLAN.md](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_PLAN.md), [AD-03_markers.json](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_markers.json), [list_screen.md](../../list_screen.md) |

## 1. Mục tiêu & phạm vi
- Mục tiêu: Hiển thị profile/status/role theo #69; nhật ký chỉ khi có API audit được duyệt.
- In-scope: Nhận `id` từ AD-02/#68 → GET #69; không đưa PII vào URL. #69 không trả audit/sync; không nhận diện `204/NULL_PAYLOAD` như success.
- Out-of-scope: Xem gate bên dưới; không kết luận Study Web route/UI đã wired hoặc runtime đã chạy.

## 2. Use cases chính
| Use case / AC | Actor | Kết quả kỳ vọng theo inventory |
|---|---|---|
| AC-31 | Theo DD nguồn; `CẦN_XÁC_NHẬN` nếu nguồn chưa chốt | Hiển thị profile/status/role theo #69; nhật ký chỉ khi có API audit được duyệt. |

## 3. Precondition / Entry / Dependencies
- Điều kiện vào, role guard và dependency: xem trích đoạn tổng quan nguồn; không bổ sung giả định.
- API references: #69
- Liên kết màn hình dự kiến: [AD-04](../AD-04-ChinhSuaNguoiDung/00-overview.md), [AD-05](../AD-05-KhoaMoKhoaXoaTaiKhoan/00-overview.md)
- Links: [UI](01-ui-elements.md) · [Events](02-events.md) · [Navigation](06-navigation.md)

## 4. UI states
| State | Nguồn | Giá trị |
|---|---|---|
| Inventory states | `list_screen.md` | loading/ready/unauthenticated/forbidden/not-found/error |
| Current runtime | Worklog/context Study Web | `UNWIRED` / `RUNTIME NOT VERIFIED` |

## 5. Luồng chính và hình ảnh
- Ảnh clean: [screen-clean.png](images/screen-clean.png) (copy từ [AD-03 source screen.png](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/screen.png))
- Ảnh numbered: [screen-numbered.png](images/screen-numbered.png) (copy từ [source annotated PNG](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/screen_annotated.png))
- Luồng: Nhận `id` từ AD-02/#68 → GET #69; không đưa PII vào URL. #69 không trả audit/sync; không nhận diện `204/NULL_PAYLOAD` như success.
- Priority: P1; Gate/source status: **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** #69 source-backed locally, nhưng ADMIN permission mapping, legacy/live schema, PII/enum/lifecycle và audit/retention policy còn mở; Study Web UNWIRED; prototype 204/audit/sync claims không được API #69 hỗ trợ; RUNTIME NOT VERIFIED

## 6. Open questions / Change log
- `CẦN_XÁC_NHẬN`: các gate/source questions trong inventory và DD nguồn vẫn giữ nguyên; không tự đóng blocker.
- 2026-11-08 — Chuyển nội dung nguồn sang 8-file template; không chỉnh source, không xác minh runtime.

## Trạng thái và ranh giới bằng chứng

# AD-03 — Chi tiết người dùng

> **Screen ID:** AD-03 · **Surface:** Page · **Priority:** P1<br>
> **DD status:** `BLOCKED — policy, audit source, and live-schema decisions remain open`<br>
> **Implementation:** `BLOCKED — Study Web is UNWIRED` · **Runtime:** `NOT VERIFIED`

## Trích đoạn tổng quan từ DD nguồn

### Trích từ DD nguồn: A. Tổng quan màn hình

### Expected behavior

| Thuộc tính | Đặc tả |
|---|---|
| Route đề xuất | `/admin/users/:userId` theo inventory. Đây chưa phải route runtime. API dùng `/api/v1/admin/users/{user_id}`. |
| Actor / điều kiện | Admin đã xác thực và có quyền quản lý user theo AC-31. API catalog ghi Bearer JWT/Admin; source hiện kiểm tra claim `ADMIN`. Việc claim này đủ đại diện cho quyền user management là fallback `DERIVED`, chưa được owner xác nhận. |
| Mục tiêu | Xem hồ sơ một user được chọn từ AD-02. Có thể chuyển sang AD-04 hoặc AD-05 sau khi các quyền, route và hợp đồng màn hình đích được xác nhận. |
| Handoff vào | Chọn `items[].id` từ API #68 tại AD-02; truyền ID trong path sang AD-03/#69. Không đưa email hoặc phone vào URL. |
| API chính | `GET /api/v1/admin/users/{user_id}` (#69), Bearer JWT, path `user_id:int64!`; không có query hoặc body. |
| Success | HTTP 200, `businessCode=DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`. |
| Errors | Catalog/source: 401 `DESIGN_AUTHENTICATION_REQUIRED`, 403 `DESIGN_ACCESS_DENIED`, 404 `DESIGN_RESOURCE_NOT_FOUND`, 500 `DESIGN_INTERNAL_ERROR`. Runtime error envelope dùng `data:null`. |
| State tối thiểu | `loading`, `ready`, `unauthenticated`, `forbidden`, `not-found`, `error`. `204`/`NULL_PAYLOAD` không phải success state của #69. |
| Screens liên quan | AD-02 (`/admin/users`) → AD-03 → AD-04 (`/admin/users/:userId/edit`) hoặc AD-05 (`/admin/users/:userId/actions`) theo AC-31. Các route đích vẫn là đề xuất. |

### UserProfile mapping khả dụng từ API #69

| Response field | Kiểu / null | AD-03 sử dụng | Giới hạn |
|---|---|---|---|
| `id` | `int` / signed-int64 candidate | Mã người dùng; làm path handoff. | Legacy BIGINT candidate; live schema chưa xác minh. |
| `full_name` | `string` | Họ và tên. | Bắt buộc theo runtime model. |
| `email` | `string` | Địa chỉ email. | PII; masking/visibility policy chưa xác nhận. |
| `phone` | `string \| null` | Số điện thoại. | PII; giữ null nếu hiển thị, không tự thay bằng giá trị khác. |
| `role` | `string` | Vai trò hệ thống. | Enum members và nhãn hiển thị chưa được định nghĩa. |
| `status` | `string` | Trạng thái tài khoản. | Enum members và lifecycle visibility chưa được định nghĩa. |
| `avatar_url` | `string \| null` | Không hiển thị trong ảnh hiện tại. | Có trong model; không thêm element ngoài screenshot trong phiên này. |
| `created_at`, `updated_at` | date-time | Không hiển thị trong ảnh hiện tại. | Timezone/format UI chưa được chốt. |
| `bio` | Không có trong runtime response model | Không hiển thị. | Catalog optionality không tạo field trong local model; không lấy từ UUID pilot profile. |

### Tách expected behavior và current behavior

| Chủ đề | Expected behavior | Current behavior / bằng chứng |
|---|---|---|
| Điều hướng và gọi API | Mở detail bằng ID từ AD-02 và đọc một `UserProfile` qua #69. | Study Web chưa có source/router/client; route trong inventory là đề xuất. HTML chỉ là prototype. |
| Quyền truy cập | AC-31 yêu cầu Admin có quyền user management. | Runtime shared guard xác thực Bearer/JWT và claim `ADMIN` trước parse ID/query. Mapping claim này sang quyền AC-31 còn `DERIVED`; tenant/MFA/permission relation chưa có source. |
| Dữ liệu profile | Hiển thị các trường được phép từ `data`. | API #69 SELECT allowlist từ checked-in legacy `users`; test dùng fake row. V1-PILOT UUID schema khác; live schema/deploy chưa xác minh. |
| Empty state / response | User không tồn tại là 404; success có profile object. | Prototype hiển thị “CHƯA ĐỒNG BỘ”, không có user được chọn và ghi `204 / NULL_PAYLOAD`; điều này không khớp contract/source #69 (200 hoặc 401/403/404/500). |
| Audit, sync, status badges | Chỉ render khi có endpoint, event schema và policy được duyệt. | #69 không trả audit, sync hoặc system-health data. “0 bản ghi”, lưu 180 ngày, tự động giám sát, RBAC audit và System Normal là static claims. |
| Mutations | #69 chỉ đọc; cập nhật/trạng thái/xóa là luồng AD-04/AD-05. | Nút AD-04 và AD-05 đang disabled; không có handler hay request. |
| Shell navigation | Dùng route/destination đã được xác định. | Nav/footer anchors dùng `href="#"`; breadcrumb dùng fragment; không có listener hay router. |

### Nguồn truy vết

- [Inventory và screen flow](../../list_screen.md) · [Kế hoạch tổng](../../screen_stitch/dd_screens/PLAN.md) · [Plan AD-03](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_PLAN.md)
- [Ảnh gốc](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/screen.png) · [Ảnh đánh số](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/screen_annotated.png) · [HTML prototype](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/code.html) · [Marker map](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03_markers.json)
- [API catalog #69](../../../../../docs/lists/list_api.md) · [AC-31 activity diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- [API #69 Overview](../../../../study-server/docs/dd/69_admin_user_detail/02_Overview.md) · [Request](../../../../study-server/docs/dd/69_admin_user_detail/03_Request.md) · [Response](../../../../study-server/docs/dd/69_admin_user_detail/04_Response.md) · [Error](../../../../study-server/docs/dd/69_admin_user_detail/06_Error.md) · [Open questions](../../../../study-server/docs/dd/69_admin_user_detail/OPEN_QUESTIONS.md)
- [API #69 route](../../../../study-server/app/api/v1.py) · [API #69 view](../../../../study-server/app/modules/admin/api_69_admin_user_detail/view.py) · [query](../../../../study-server/app/modules/admin/api_69_admin_user_detail/query.py) · [validation](../../../../study-server/app/modules/admin/api_69_admin_user_detail/validate.py) · [model](../../../../study-server/app/modules/admin/api_69_admin_user_detail/models.py) · [focused test source](../../../../study-server/tests/modules/admin/api_69_admin_user_detail/test_admin_user_detail.py)
- [Study Web design target](../../../../../.agents/web-study/design.md) · [Study Web boundary](../../../../../.agents/web-work/study/AGENTS.md) · [Project API source status](../../../../../.agents/project/source-status.md)
