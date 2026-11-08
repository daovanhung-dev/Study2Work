# SH-05 — Data Flow & State

## 1. Nguồn dữ liệu
| Field / object | Type | Source | Destination | Cập nhật khi |
|---|---|---|---|---|
| Chỉ liệt kê theo bằng chứng trong excerpt bên dưới | Theo DD/API source | API/inventory/design; status phải giữ nguyên | UI/state nêu ở DD nguồn | Theo event source |

## 2. State model

> Không tạo DTO/ViewModel mới khi chưa có contract. State, DTO và mapping được trích nguyên ngữ cảnh từ DD nguồn bên dưới.

## 3. API DTO → ViewModel mapping

### Trích từ DD nguồn: 2. Luồng hoạt động tổng thể

1. **Khởi tạo / nhận context:** Router hoặc lớp gọi chung chuyển tới SH-05 sau khi request được bảo vệ nhận lỗi xác thực cuối cùng, hoặc direct navigation vào route. Hợp đồng truyền status/error/return route vào view chưa được triển khai; không gọi #04 chỉ để dựng SH-05 vì có thể lặp lỗi.
2. **Chuẩn hóa response:** Đọc HTTP status, `businessCode`, `message`, `traceId` từ envelope và `X-Trace-Id` từ header. Chỉ dùng các giá trị server trả; không tạo `reason`, `timestamp`, role, hoặc trace ID giả. Nếu body/header cùng có trace ID nhưng khác nhau, giữ lỗi cho telemetry và không tự chọn giá trị thay thế theo quy tắc chưa được duyệt.
3. **Xử lý 401 trước khi hiển thị:** Theo intent inventory, auth manager có thể thử R-X01 tối đa một lần nếu có refresh token và policy cho phép. API #04 cũng trả cùng 401 khi profile không tồn tại; client không thể kết luận chỉ từ code rằng access token hết hạn. Nếu refresh thành công, cập nhật phiên theo storage đã duyệt và chỉ retry request gốc theo policy replay an toàn. Nếu request #04 vẫn trả 401, dừng retry; thông điệp/đích tiếp theo cần Product/Backend quyết định, không tự gọi đó là “hết phiên”.
4. **Xử lý 403:** Không gọi R-X01. Hiển thị thông điệp chung không tiết lộ role/permission nội bộ; giữ route trước đó chỉ khi là route nội bộ an toàn đã allowlist. Không tự điều hướng sang Mentor/Admin hoặc gán quyền.
5. **Xử lý lỗi dịch vụ:** 5xx, timeout, lỗi mạng, body không hợp lệ hoặc business code không khớp không được ánh xạ thành 403. Dùng trạng thái service error chung và giữ trace ID nếu có; retry chỉ theo chính sách an toàn của request, không tự lặp refresh.
6. **Ánh xạ UI:** State quyết định badge, title, mô tả và action. Trace card chỉ hiển thị dữ liệu lỗi allowlist; không render stack trace, token, profile, database detail hoặc payload chưa lọc.
7. **Tương tác:** Người dùng chọn login hoặc route lui an toàn. Hành động sao chép chỉ copy trace ID thật và thông báo kết quả accessible. Prototype state toggle không xuất hiện trong runtime.
8. **Rời màn hình:** Sau login thành công, SH-02 tiếp tục flow xác định role/profile theo contract riêng. Inventory G-14 ghi API #03 catalog `201/UserProfile-only` khác current source `200/profile+tokens`; SH-05 không định nghĩa response parser của SH-02, nên login handoff chưa thể xác minh end-to-end. `returnTo` chỉ được giữ nếu là relative route nội bộ đã allowlist; không đưa token hoặc PII vào URL. Sau 403, đích quay lại cụ thể cần được sản phẩm chốt khi không có route trước an toàn.

Quan hệ luồng: SH-05 có thể được gọi sau SH-02/API #04 hoặc bởi guard của một màn hình cần quyền. Với 401, SH-02 là đích đăng nhập. Với 403, route trước đó an toàn là đích ưu tiên; SH-01/GS-01 là các route công khai tham khảo trong inventory, không tự chọn làm fallback mặc định khi chưa có quyết định UX.

### Trích từ DD nguồn: Ma trận nội dung A–F

| Phần yêu cầu | Nội dung SH-05 |
|---|---|
| A. Tổng quan màn hình | §1 |
| B. Luồng hoạt động tổng thể | §2 |
| C. Đặc tả element | §3 (ảnh và marker) và §4 |
| D. Đặc tả sự kiện/API | §5 và §6 |
| E. Trạng thái và điều hướng | §7 và §8 |
| F. Tiêu chí nghiệm thu | §9 (blocker/sai khác) và §10 |

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

### Trích từ DD nguồn: 7. Ma trận trạng thái và điều hướng

| State | Điều kiện vào | UI/action | Chuyển tiếp |
|---|---|---|---|
| `INITIAL` | Router resolve, error context chưa parse | Không hiển thị dữ liệu giả; giữ shell/loading tối thiểu nếu cần | `RESOLVING` |
| `RESOLVING` | Đang chuẩn hóa status/envelope | Không có action refresh thứ hai | `UNAUTHORIZED`, `FORBIDDEN`, `SERVICE_ERROR` |
| `UNAUTHORIZED` | 401 sau khi recovery policy đã dừng, hoặc không có refresh token | Thông báo xác thực thất bại trung tính; chỉ nói phiên hết hạn khi đã xác nhận; login action theo policy; không render protected data | `LOGIN_NAVIGATION` hoặc outcome được Product chốt cho profile-missing |
| `REFRESHING` | Auth manager đang gọi R-X01 và attempt chưa dùng | Loading status; disable action lặp; không lộ token | `RETRYING`, `REFRESH_REJECTED`, `SERVICE_ERROR` |
| `RETRYING` | Refresh thành công, request gốc được phép replay | Giữ feedback loading; request gốc thử tối đa một lần | Route gốc/`UNAUTHORIZED`/`SERVICE_ERROR` |
| `FORBIDDEN` | API trả 403 | Thông điệp quyền bị từ chối; no refresh; safe-back action | `SAFE_BACK` |
| `REFRESH_REJECTED` | Refresh trả 401 hoặc account-inactive 403 | Không retry refresh; login hoặc access-denied outcome theo source/policy | `UNAUTHORIZED`/`FORBIDDEN` |
| `SERVICE_ERROR` | 5xx, timeout, network, parse error | Lỗi dịch vụ chung, trace ID nếu có; không giả thành 401/403 | Retry read theo policy hoặc safe navigation |
| `COPY_SUCCESS` / `COPY_FAILED` | EV-06 hoàn tất/thất bại | Accessible status/error feedback; auth state giữ nguyên | Trở lại state trước |
| `LOGIN_NAVIGATION` / `SAFE_BACK` | Người dùng chọn route action | Router điều hướng sau safe-route validation | SH-02 hoặc route an toàn |

| Từ | Điều kiện | Đến / dữ liệu được truyền |
|---|---|---|
| Màn hình được bảo vệ → SH-05 | 401 đã refresh-fail/không có token | `status`, `businessCode`, safe `message`, `traceId`, relative return route allowlisted nếu có. Không truyền token. |
| Màn hình được bảo vệ → SH-05 | 403 | Cùng error context; không gửi refresh token; không truyền role matrix. |
| SH-05 → SH-02 | 401 cuối cùng / login action | Safe `returnTo` relative route nếu policy/router xác nhận; không có token/PII. |
| SH-05 → route trước an toàn | 403 / safe-back | Chỉ route same-origin allowlisted; fallback khi direct entry cần Product chốt. |
| SH-05 → service error state | 5xx/network/timeout | Safe message và trace ID nếu có; giữ nguyên HTTP/business code, không đổi thành 403. |

## 4. Luồng đọc (Read)
- Orchestration từ inventory: Khi 401 có thể thử refresh runtime R-X01 1 lần; 403 KHÔNG refresh vô hạn.
- Chi tiết current/source mapping: xem [API Integration](04-api-integration.md) và DD nguồn.

## 5. Luồng ghi (Write)
- Chỉ mô tả mutation được DD/API source nêu; không thêm endpoint hoặc side effect.
- Source trace: [SH-05](../../screen_stitch/01_shared_auth_system/SH-05_khong-du-quyen-session-het-han/SH-05.md)

## 6. Cache / concurrency / lifecycle
- Cache, race, cleanup, pagination: xem các section source bên dưới; nếu không có bằng chứng thì để `CẦN_XÁC_NHẬN`.

## 7. Data errors & security
- Theo error/security/source-status section của DD nguồn; không coi state trong mockup là runtime behavior.

## 8. Trace
[Events](02-events.md) · [API](04-api-integration.md) · [Rules](05-business-rules.md)
