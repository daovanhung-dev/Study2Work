# SH-02 — API Integration

> API/status dưới đây lấy từ inventory và DD nguồn. Package-local API IDs chỉ là alias truy vết cho API catalog reference; chúng không tạo contract mới. `R/S/D/M/UX` hoặc nhãn cục bộ là evidence status, không tự động xác nhận UI/runtime. Route/contract thiếu nguồn phải giữ `CẦN_XÁC_NHẬN`.

## 1. API usage matrix
| API ID (package-local usage alias) | Source catalog ref | Method/path | Event | Auth |
|---|---|---|---|---|
| `SH-02-API-001` | #03 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |
| `SH-02-API-002` | #04 | See source contract excerpt | Source event IDs are preserved in [Events](02-events.md) | See source auth/permission evidence |

## 2. Contract / source detail

### Current approved contract for SH-02 (2026-11-21)

- `POST /api/v1/auth/login` uses the selected current Study Server contract: HTTP 200, `DESIGN_RESOURCE_RETRIEVED`, `ApiEnvelope<LoginData>` with profile fields and five token fields. The API catalog and API #03 DD have been reconciled; reusable `UserProfile` remains unchanged.
- Current source error branches are 401 invalid credentials, 403 non-ACTIVE account, 422 validation, and 500 internal error. Login 401 is handled in place and never triggers token refresh.
- The client accepts only the exact success status/code and valid profile/token fields, then stores credentials in the existing role-specific in-memory session. Student alone calls API #04. No `returnTo` is carried from this route.

The current Study Web implementation is reconciled to the selected API #03 source contract: SH02Page sends exactly one #03 request, requires HTTP 200 plus `DESIGN_RESOURCE_RETRIEVED`, reads a supported role, clears existing role sessions, and passes the envelope to the matching in-memory session manager. Only Student calls #04 and verifies exact success code plus role/email identity before navigating. Mentor/Admin do not call Student-only #04. The catalog and API #03 DD now declare HTTP 200 `LoginData`; no `returnTo` is carried. Focused tests pass; browser/live API runtime remains unverified.

- API refs trong inventory: #03, #04
- Orchestration/data notes: #03 → role-specific in-memory session → #04 only for Student → matching role route. No persistent token storage or `returnTo`.
- BE/source status and gates: source path and selected #03 contract are wired; `returnTo` and forgotten-password flow remain outside approved scope; live runtime remains unverified.
- Contract sources and discrepancies are preserved in the source excerpts below.

### Trích từ DD nguồn: 3. Truy vết API và hợp đồng

| API | Phương thức/đường dẫn | Trạng thái nguồn hiện tại | SH-02 sử dụng |
|---|---|---|---|
| #03 đăng nhập | POST /api/v1/auth/login | Client call source-wired; current server source returns HTTP 200 profile+tokens; catalog says HTTP 201 UserProfile-only | Send email/password once; role-specific session accepts response |
| #04 người dùng hiện tại | GET /api/v1/users/me | Client call source-wired for Student only; server source is Student-only | Verify returned Student role/email before `/student` |
| R-X01 refresh | POST /api/v1/auth/refresh | Existing source-only session behavior; not called directly by SH02LoginService | Existing session manager may refresh later API calls at local expiry; not a login-error retry |

### 3.1 Yêu cầu API #03

~~~http
POST /api/v1/auth/login
Content-Type: application/json

{"email":"<đầu vào người dùng>","password":"<đầu vào người dùng>"}
~~~

- Đăng nhập không cần Bearer token. Không gắn token truy cập cũ làm dữ liệu thay thế cho yêu cầu.
- LoginRequest hiện khai báo hai chuỗi: email và password.
- Validator hiện loại khoảng trắng/kiểm tra định dạng email, từ chối email chuẩn hóa dài hơn 255 ký tự và trả meta.fieldErrors cho trường sai.
- Validator từ chối password chỉ có khoảng trắng sau .strip(), nhưng gửi nguyên chuỗi mật khẩu ban đầu cho bước xác minh. Client không được cắt hoặc viết lại mật khẩu.
- Kiểm tra gốc required/type=email của trình duyệt chỉ là tiện ích; #03 vẫn là thẩm quyền. Không tự thêm độ dài tối thiểu/độ phức tạp mật khẩu, ghi nhớ đăng nhập, CAPTCHA hoặc MFA.

### 3.2 Thực thi và phản hồi theo nguồn hiện tại

POST /api/v1/auth/login được đăng ký trong [app/api/v1.py](../../../../study-server/app/api/v1.py) và chuyển tới [api_03_auth_login.view.login](../../../../study-server/app/modules/guest/api_03_auth_login/view.py):

1. validate_login_request chuẩn hóa email và từ chối mật khẩu chỉ có khoảng trắng.
2. LOGIN_USER truy vấn dòng người dùng theo email đã chuẩn hóa, lấy password_hash để xác minh ở máy chủ.
3. Không có người dùng và sai mật khẩu cùng dùng HTTP 401 DESIGN_AUTHENTICATION_REQUIRED với thông báo thông tin đăng nhập chung.
4. Nếu mật khẩu đúng nhưng users.status != ACTIVE, nguồn trả HTTP 403 DESIGN_ACCESS_DENIED.
5. auth_utils.issue_tokens tạo access JWT và refresh token opaque. Claim JWT hiện dùng sub + roles; refresh token được trả về client một lần, còn HMAC-SHA256 hash được chèn vào refresh_tokens.
6. Nguồn commit sau khi chèn hash refresh thành công. Lỗi SQL/lưu token rollback và trả HTTP 500 DESIGN_INTERNAL_ERROR an toàn.
7. Thành công theo nguồn hiện tại là HTTP 200 DESIGN_RESOURCE_RETRIEVED. data gồm phần hồ sơ được cho phép (id, full_name, email, role, avatar_url, phone, status, created_at, updated_at) cùng access_token, refresh_token, token_type="bearer", expires_in và refresh_expires_in.

**Lịch sử:** các trích đoạn DD nguồn tiếp theo được giữ để truy xuất quyết định trước khi reconcile. Chúng từng nêu #03 201/UserProfile-only; quyết định 2026-11-21 chọn current Study Server 200 `LoginData` và đã cập nhật API catalog/DD như phần Current approved contract phía trên. Không dùng đoạn trích lịch sử làm contract hiện hành.

### 3.3 Yêu cầu và phản hồi API #04

~~~http
GET /api/v1/users/me
Authorization: Bearer <access_token>
~~~

- Có đúng một header Authorization; không body, tham số đường dẫn hay query.
- Guard hiện giải mã token, yêu cầu sub là số dương và roles có STUDENT, rồi mới truy vấn DB.
- Phản hồi thành công hiện là HTTP 200 DESIGN_RESOURCE_RETRIEVED; data có id, full_name, email, role, avatar_url có thể null, phone có thể null, status, created_at, updated_at.
- Phản hồi #04 hiện không có permissions, bio, access/refresh token hoặc password hash. AC-02 đề cập permissions nhưng nguồn tại đây không có trường đó.
- Nguồn hiện kiểm tra vai trò học viên trong JWT, nhưng đọc role/status từ DB mà không đối chiếu vai trò với claim hoặc kiểm tra trạng thái DB trong truy vấn #04. Đây là quyết định API/bảo mật, không phải quy tắc mới ở màn hình.
- 401 áp dụng cho claim thiếu/không hợp lệ hoặc không tìm thấy người dùng trong DB; 403 áp dụng cho vai trò không phải học viên; 500 an toàn áp dụng cho lỗi DB/ánh xạ hồ sơ.
- Cả nhánh auth/claim không hợp lệ và profile không tồn tại hiện dùng HTTP 401 `DESIGN_AUTHENTICATION_REQUIRED` với thông điệp chung; response không cung cấp mã phân loại riêng để client quyết định có nên refresh. Không tự coi mọi #04/401 là token hết hạn.

### 3.4 Nguồn refresh R-X01

- Body hiện dùng {"refresh_token":"<token opaque>"}.
- Mã nguồn băm token được gửi, tìm dòng chưa thu hồi/chưa hết hạn cho tài khoản ACTIVE, cấp cặp access/refresh mới, thu hồi dòng cũ và chèn hash mới trong cùng một giao dịch.
- Token sai, hết hạn hoặc đã xoay trả 401. Route có trong nguồn nhưng không có ID API trong danh mục hoặc chính sách client Study Web được duyệt.
- Không ghi log giá trị token, không đưa vào URL hoặc payload minh họa trong DD.

### 3.5 Nguồn truy vết đã đối chiếu

| Nguồn | Phạm vi dùng trong DD |
|---|---|
| [Danh mục màn hình](../../list_screen.md) | SH-02, F01, API #03/#04, G-02/G-14, màn hình liên kết và trạng thái đích. |
| [AC-02 — Guest Account](../../../../study-server/docs/diagrams/AC_UNICA/AC_01_GUEST_ACCOUNT.drawio) | Luồng Guest đăng ký/đăng nhập và chuyển tới khu vực theo vai trò. |
| [API catalog](../../../../../docs/lists/list_api.md) | Hợp đồng thiết kế chuẩn #03/#04; là một vế của discrepancy với nguồn hiện tại. |
| [Router/API registration](../../../../study-server/app/api/v1.py) | Route/status/request metadata cho #03, #04 và R-X01. |
| [Login view](../../../../study-server/app/modules/guest/api_03_auth_login/view.py), [validator](../../../../study-server/app/modules/guest/api_03_auth_login/validate.py), [models](../../../../study-server/app/modules/guest/api_03_auth_login/models.py), [queries](../../../../study-server/app/modules/guest/api_03_auth_login/query.py) | Kiểm tra đầu vào, xác thực, cấp token, transaction và xoay refresh token hiện tại. |
| [Current-user view](../../../../study-server/app/modules/student/api_04_users_me/view.py), [models](../../../../study-server/app/modules/student/api_04_users_me/models.py), [queries](../../../../study-server/app/modules/student/api_04_users_me/query.py), [auth utilities](../../../../study-server/app/utils/auth.py) | Guard Bearer/JWT/role, allowlist hồ sơ và payload token hiện tại. |
| [Login source tests](../../../../study-server/tests/modules/guest/api_03_auth_login/test_auth_login.py), [current-user source tests](../../../../study-server/tests/modules/student/api_04_users_me/test_users_me.py) | Các nhánh source được test bằng fixture/fake session; chưa chạy trong phiên và không xác nhận DB/deployment trực tiếp. |
| [Refresh-token migration](../../../../../infra/postgres/study-server/migrations/002_refresh_tokens.sql), [Study DB DDL](../../../../../infra/postgres/study-server/DB.sql) | Cấu trúc đã commit; không chứng minh schema đang triển khai/live. |
| [Study Web design guide](../../../../../.agents/web-study/design.md) | Mục tiêu UI/accessibility/responsive; không phải bằng chứng runtime. |

## 3. API không sử dụng
- Không bổ sung API ngoài inventory và DD nguồn. Nếu screen không cần API, trạng thái phải được xác nhận từ source DD.

## 4. References
[Events](02-events.md) · [Data flow](03-data-flow.md) · [Tests](07-test-cases.md) · [Source DD](../../screen_stitch/01_shared_auth_system/SH-02_dang-nhap/SH-02.md)
