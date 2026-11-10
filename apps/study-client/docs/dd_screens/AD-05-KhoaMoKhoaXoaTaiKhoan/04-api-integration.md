# AD-05 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `AD-05-API-001` | #69 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-05-API-002` | #71 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `AD-05-API-003` | #72 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #69, #71, #72
- Orchestration/data notes: GET #69 → PATCH #71 hoặc DELETE #72 → refresh #68/#69 theo AC-31; #71 body/status và #72 delete policy cần duyệt; không tự giả định token effect.
- BE/source status và gate: **R**; **DD BLOCKED; IMPLEMENTATION BLOCKED:** #71 body/status/session, #72 delete/visibility/retention, Admin permission/audit/safeguards và Study Web UNWIRED còn mở; RUNTIME NOT VERIFIED
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: Nguồn truy vết

- [Screen inventory](../../list_screen.md) · [Global DD plan](../../screen_stitch/dd_screens/PLAN.md) · [AD-05 plan](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_PLAN.md) · [AD-05 markers](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.json)
- [Original screenshot](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen.png) · [Annotated screenshot](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/screen_annotated.png) · [HTML prototype](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/code.html) · [SVG marker overlay](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05_markers.svg)
- [AD-02 list](../../screen_stitch/05_admin/AD-02_danh-sach-nguoi-dung/AD-02.md) · [AD-03 detail](../../screen_stitch/05_admin/AD-03_chi-tiet-nguoi-dung/AD-03.md) · [AD-04 update](../../screen_stitch/05_admin/AD-04_chinh-sua-nguoi-dung/AD-04.md)
- [API catalog](../../../../../docs/lists/list_api.md) · [AC-31 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_04_ADMIN_MANAGEMENT.drawio)
- #69 local route/source: [v1 router](../../../../study-server/app/api/v1.py) · [API #69 module](../../../../study-server/app/modules/admin/api_69_admin_user_detail)
- #71 local source: [API #71 module](../../../../study-server/app/modules/admin/api_71_admin_user_status) · [focused test source](../../../../study-server/tests/modules/admin/api_71_admin_user_status/test_admin_user_status.py) · [Draft API DD](../../../../study-server/docs/dd/71_admin_user_status/02_Overview.md)
- #72 local source: [API #72 module](../../../../study-server/app/modules/admin/api_72_admin_user_delete) · [focused test source](../../../../study-server/tests/modules/admin/api_72_admin_user_delete/test_admin_user_delete.py) · [Draft API DD](../../../../study-server/docs/dd/72_admin_user_delete/02_Overview.md)
- [API #03 auth source](../../../../study-server/app/modules/guest/api_03_auth_login) · [Study Web boundary](../../../../../.agents/web-work/study/AGENTS.md) · [Study Web design target](../../../../../.agents/web-study/design.md)

### Trích từ DD nguồn: Luồng mục tiêu sau khi các policy và API contract được duyệt

1. **Nhận handoff:** AD-02/AD-03 chuyển numeric `user_id` sang route AD-05. Route là đề xuất; không ánh xạ `USR-*`, email hoặc phone sang path ID.
2. **Kiểm tra đầu vào và phiên:** kiểm tra `userId` theo signed-int64 path contract trước khi gọi API. Client áp dụng auth/session/navigation policy đã duyệt. Không dùng các badge RBAC hoặc “Read-Only” trên ảnh làm bằng chứng quyền.
3. **Tải hồ sơ:** gọi `GET /api/v1/admin/users/{user_id}` (#69), Bearer JWT/Admin, không body/query. Local #69 kiểm tra shared ADMIN guard, parse path và đọc safe UserProfile từ legacy `users` candidate. Chuyển UI sang loading rồi ready khi nhận HTTP 200 + `DESIGN_RESOURCE_RETRIEVED` và payload hợp lệ.
4. **Ánh xạ dữ liệu:** map ID/status/profile chỉ theo API #69 và field/PII policy đã duyệt. `status` hiện là string; không đổi lowercase aliases thành API status hoặc tự tạo allowlist. `DELETED` hiện vẫn có thể xuất hiện trong #68/#69 local source.
5. **Chọn action:** lock/unlock/delete tabs chỉ ghi nhận local draft action. Không gọi API khi chỉ đổi tab. Chỉ cho phép Confirm sau khi status transition, delete policy, permission/safeguards và audit/session behavior được duyệt. Hiện prototype giữ reason và confirm disabled.
6. **Mutation trạng thái:** nếu #71 body được duyệt, gửi đúng body/status đã thống nhất. Local candidate hiện là `{status: "SUSPENDED"}` cho khóa hoặc `{status: "ACTIVE"}` cho mở khóa, nhưng không được dùng trước khi body/state policy được duyệt. Không đưa reason vào body vì source/catalog hiện không có field đó.
7. **Mutation xóa:** nếu #72 semantics được duyệt, gửi bodyless DELETE. Local source đang đặt marker `DELETED`, không xóa vật lý/anonymize, không audit hoặc revoke token. Không diễn đạt action là “vĩnh viễn” nếu policy chưa xác nhận.
8. **Xử lý response:** xác nhận HTTP status, `businessCode`, envelope và response shape trước khi cập nhật. #71 success trả `UserProfile`; #72 success trả `DeleteResult`. Error envelope dùng `data:null`; không biến 404/422 thành success hoặc dependency conflict. Không retry mutation tự động sau timeout/response không rõ kết quả vì retry/idempotency policy chưa có contract.
9. **Sau mutation:** theo inventory/AC-31, refetch #68/#69 khi action được duyệt. Cần chốt trước cách #72 xử lý khi #68/#69 tiếp tục hiển thị user có `DELETED` status, và route/detail/list đích sau thành công. Không giả định redirect, undo hoặc hide row.
10. **Rời màn hình:** back/return điều hướng tới AD-02 hoặc AD-03 bằng numeric ID theo route policy. Prototype hiện tại chỉ có link về `/admin/users`; selected row/profile không được giữ bởi handler nào.

### Trích từ DD nguồn: API request/response matrix

| API | Direct catalog/AC contract | Current local implementation | Screen mapping |
|---|---|---|---|
| #69 | `GET /api/v1/admin/users/{user_id}`; Bearer JWT/Admin; signed `int64` path; no body/query. 200 `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<UserProfile>`; 401/403/404/500. | Shared ADMIN guard; signed-int64 parsing; safe read-only projection from local legacy `users` candidate. | Load selected user/status. Do not treat static profile, permission or audit copy as API response. |
| #71 | `PATCH /api/v1/admin/users/{user_id}/status`; Bearer JWT/Admin; signed `int64` path. Catalog/AC omit request body. 200 `DESIGN_RESOURCE_UPDATED`, `ApiEnvelope<UserProfile>`; 401/403/404/422/500. | Strict required body `{status: "ACTIVE"|"SUSPENDED"}` is `DERIVED`; row lock; only current ACTIVE/SUSPENDED; update status/updated_at; suspend revokes eligible refresh rows in same transaction. | Keep disabled until body, transition/status vocabulary, permission and session effects are approved. Never attach reason with this contract. |
| #72 | `DELETE /api/v1/admin/users/{user_id}`; Bearer JWT/Admin; signed `int64` path; no body/query. 200 `DESIGN_RESOURCE_DELETED`, `ApiEnvelope<DeleteResult>`; 401/403/404/422/500. | Conditional soft marker `DELETED`; returns `{id,status:"deleted",deleted_at}` with `deleted_at` aliasing updated_at. Preserves profile/dependent/token rows; no audit/anonymization/dependency check. | Keep disabled until deletion/retention/visibility/session policy is approved; do not label as irreversible hard delete. |

**Shared request rules:** send Bearer credentials only through the approved HTTP client; never place tokens or PII in the URL. Do not add query parameters, `reason`, audit IDs, client-generated deletion time, `X-Trace-Id`, idempotency key or retry semantics unless the API contract defines them. The catalog has no retry, timeout or duplicate-submission guarantee for these mutations. Error envelope carries `data:null`; surface safe server message according to common error policy without exposing SQL/stack traces.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/05_admin/AD-05_khoa-mo-khoa-xoa-tai-khoan/AD-05.md)
