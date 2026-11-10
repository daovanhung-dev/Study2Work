# SH-05 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-05-API-001` | #04 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

- API refs trong inventory: #04
- Orchestration/data notes: Khi 401 có thể thử refresh runtime R-X01 1 lần; 403 KHÔNG refresh vô hạn.
- BE/source status và gate: **R**
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 5. Đặc tả API và dữ liệu

### 5.1 API #04 — GET `/api/v1/users/me`

| Thành phần | Contract/source hiện tại |
|---|---|
| Method / endpoint | `GET /api/v1/users/me` (API #04 trong `list_screen.md`). |
| Authentication | `Authorization: Bearer <access JWT>`. Route không khai báo body, query hoặc path parameter. Backend guard yêu cầu role `STUDENT`. |
| Request data | Không có request body. Không gửi refresh token tới API #04. |
| Thành công | HTTP 200, `DESIGN_RESOURCE_RETRIEVED`; `data` theo `UserProfile`: `id`, `full_name`, `email`, `role`, `avatar_url`, `phone`, `status`, `created_at`, `updated_at`. `bio` và `permissions` không được model hiện tại trả. |
| 401 | `DESIGN_AUTHENTICATION_REQUIRED` khi Authorization thiếu/sai hoặc identity không hợp lệ; profile không tìm thấy cũng được ánh xạ thành 401 trong `get_current_user`. |
| 403 | `DESIGN_ACCESS_DENIED` khi JWT không đạt role Student. |
| 500 | `DESIGN_INTERNAL_ERROR` khi profile query/model mapping lỗi; message an toàn. |
| Envelope / trace | Error: `{success:false,businessCode,message,data,meta,traceId}`; success dùng `success:true` cùng envelope. `X-Trace-Id` được trả ở response header. Không suy ra `meta` có field cụ thể nếu source không cung cấp. |
| Side effect | Read-only `CURRENT_USER_PROFILE` query; không commit. SH-05 không render profile data. |

Source path: [`app/api/v1.py`](../../../../study-server/app/api/v1.py) → [`api_04_users_me/view.py`](../../../../study-server/app/modules/guest/api_04_users_me/view.py) → [`models.py`](../../../../study-server/app/modules/guest/api_04_users_me/models.py), [`query.py`](../../../../study-server/app/modules/guest/api_04_users_me/query.py), và [`auth.py`](../../../../study-server/app/utils/auth.py). Test source: [`test_users_me.py`](../../../../study-server/tests/modules/guest/api_04_users_me/test_users_me.py); test đã được đọc nhưng không chạy trong phiên docs này.

### 5.2 R-X01 — POST `/api/v1/auth/refresh`

R-X01 là runtime capability ngoài API catalog, không phải API ID #03 (login). Source route cùng module login nhưng operation riêng; không có Authorization header requirement trên route.

~~~http
POST /api/v1/auth/refresh
Content-Type: application/json

{"refresh_token":"<opaque refresh token>"}
~~~

- Request body yêu cầu `refresh_token` không rỗng; không đưa token vào URL, query, log, error message hoặc UI.
- Thành công hiện tại: HTTP 200 `DESIGN_RESOURCE_RETRIEVED`; trả auth payload có profile allowlist, access token, refresh token mới và thông tin hạn dùng theo source.
- Server hash token nhận vào, tìm refresh session hợp lệ, yêu cầu tài khoản `ACTIVE`, phát hành cặp token mới, revoke refresh token cũ, insert hash mới và commit trong cùng transaction.
- Lỗi hiện tại: 401 `DESIGN_AUTHENTICATION_REQUIRED` nếu token sai/hết hạn/đã dùng; 403 `DESIGN_ACCESS_DENIED` nếu tài khoản không `ACTIVE`; validation lỗi 422; lỗi nội bộ 500 `DESIGN_INTERNAL_ERROR`.
- Retry: token cũ là one-time sau rotation. Không gửi lại cùng refresh token khi response outcome không rõ; không tạo vòng lặp hoặc refresh song song. Timeout/retry/reconciliation policy phía client chưa có source và cần quyết định trước khi implement.
- Persistence: nơi giữ token, CSRF/XSS mitigation, session cleanup và phối hợp nhiều request chưa được quyết định trong Study Web. Không ghi `localStorage`, `sessionStorage` hoặc cookie như contract đã chọn.

Source path: [`app/api/v1.py`](../../../../study-server/app/api/v1.py) và [`api_03_auth_login/view.py`](../../../../study-server/app/modules/guest/api_03_auth_login/view.py), [`models.py`](../../../../study-server/app/modules/guest/api_03_auth_login/models.py), [`validate.py`](../../../../study-server/app/modules/guest/api_03_auth_login/validate.py), [`query.py`](../../../../study-server/app/modules/guest/api_03_auth_login/query.py). Test source: [`test_auth_login.py`](../../../../study-server/tests/modules/guest/api_03_auth_login/test_auth_login.py); test không chạy trong phiên này.

### Trích từ DD nguồn: 11. Nguồn truy vết

- [Inventory `list_screen.md`](../../list_screen.md) — dòng SH-05, F01, API dependency index và shared state/navigation rules.
- [UC diagram](../../../../study-server/docs/diagrams/UC.drawio) — shared account/login/profile use cases.
- [AC-02/AC-11 diagram](../../../../study-server/docs/diagrams/AC_UNICA/AC_02_STUDENT_LEARNING.drawio) and [AC/API index](../../../../study-server/docs/diagrams/AC_UNICA/00_AC_API_INDEX.md).
- [Study API design catalog](../../../../../docs/lists/list_api.md); this is a design catalog and does not replace runtime source evidence.
- [Study Web design guide](../../../../../.agents/web-study/design.md).
- Study Server source: links trong mục 5; API #04 và R-X01 route/service/model/query.
- Runtime test source: links trong mục 5; chỉ là test source đã đọc, chưa chạy trong phiên này.
- `docs/BD/` / `docs/BRD/` vắng mặt; Study OpenAPI hiện là README placeholder; không có contract thực thi cho frontend SH-05. Live DB status chưa được xác minh trong phiên này.

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md)
