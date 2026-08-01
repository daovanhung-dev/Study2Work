# Plan 02 — Authentication Core

## 1. Mục tiêu

Hoàn thành **9 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **7–15**.

- API trực tiếp từ tài liệu/sequence: **3**.
- API suy dẫn từ BD: **6**.
- Module: 02. Tài khoản, xác thực và hồ sơ (9).
- Lý do quy mô batch: 9 API tạo thành một security boundary thống nhất: đăng ký, xác thực, phiên đăng nhập và vòng đời mật khẩu.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- User/account state machine.
- JWT/session strategy.
- Business code chuẩn cho auth.
- Áp dụng canonical response envelope từ `Study2Work_System_Architecture.md`: `success`, `businessCode`, `message`, `data`, `meta`, `traceId`; lỗi dùng `errors[]` và không trả stack trace.
- Khóa quy ước JSON/query naming (`camelCase` hay `snake_case`) trước khi chốt bản Final; catalog hiện còn các tên như `page_size` trong khi kiến trúc tích hợp minh họa `pageSize`.
- Mỗi API là một workbook riêng; không gộp nhiều API vào một workbook.

## 3. Nguồn bắt buộc phải đọc khi thực hiện plan

- `BD/0. Study2Work_Study_Business_Description.md`
- `BD/base/0. Study2Work_System_Architecture.md`
- `BD/base/1. Study2Work_Study_Architecture.md`
- `BD/diagram/UC/01. Study2Work_Study_Diagram_UC_Tong_Quan.md`
- `BD/diagram/CLASS/01. Study2Work_Study_Diagram_CLASS_Mo_Hinh_Nghiep_Vu.md`
- `BD/diagram/CLASS/study2work_study_full_schema_seed.sql`
- `Detail_Design_API_Template_Optimized.xlsx`
- `Study2Work_API_Catalog_from_BD(1).csv`
- `BD/02. Study2Work_Study_BasicDesign_Tai_Khoan_Xac_Thuc_Ho_So.md`
- `BD/diagram/SEQUENCE/03. Study2Work_Study_SEQ_Tai_Khoan_Xac_Thuc_Dang_Nhap.md`
- `BD/diagram/AC/03. Study2Work_Study_AC_Tai_Khoan_Xac_Thuc_Ho_So.md`
- `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`

## 4. Danh sách API phải hoàn thành

### API 007 — `POST /api/v1/auth/register`

- **DD filename:** `API_007_POST_auth_register.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Public
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-03
- **Purpose:** Tạo tài khoản học viên ở trạng thái chờ xác thực.
- **Input baseline:** Body: display_name, email? hoặc phone?, password, accepted_terms, accepted_terms_version
- **Output baseline:** data: user_id, account_status=REGISTERED_PENDING_VERIFICATION, verification_channel, verification_required, next_action
- **Business rules:** ACC-01, ACC-02

### API 008 — `POST /api/v1/auth/login`

- **DD filename:** `API_008_POST_auth_login.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Public
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-03
- **Purpose:** Đăng nhập và trả ngữ cảnh điều hướng theo trạng thái tài khoản.
- **Input baseline:** Body: identifier(email/phone), password
- **Output baseline:** data: access_token, refresh_token?, expires_in, user, account_status, onboarding_status, active_path?, next_route
- **Business rules:** ACC-02, ACC-06

### API 009 — `POST /api/v1/auth/logout`

- **DD filename:** `API_009_POST_auth_logout.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Learner/Admin
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Đăng xuất phiên hiện tại.
- **Input baseline:** Header: Authorization; Body: refresh_token?
- **Output baseline:** data: logged_out=true, revoked_session_id?
- **Business rules:** Luồng 3.3

### API 010 — `POST /api/v1/auth/verification/send`

- **DD filename:** `API_010_POST_auth_verification_send.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Public/Authenticated pending
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Gửi hoặc gửi lại link/OTP xác thực có giới hạn chống spam.
- **Input baseline:** Body: channel=email|phone, destination?
- **Output baseline:** data: verification_id, channel, masked_destination, expires_at, resend_available_at
- **Business rules:** ACC-02; chống spam

### API 011 — `POST /api/v1/auth/verify-contact`

- **DD filename:** `API_011_POST_auth_verify_contact.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Public/Authenticated pending
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-03
- **Purpose:** Xác nhận email/điện thoại và chuyển tài khoản sang VERIFIED.
- **Input baseline:** Body: verification_id, token_or_otp
- **Output baseline:** data: verified=true, account_status=VERIFIED, verified_at, next_route=/onboarding
- **Business rules:** ACC-02

### API 012 — `GET /api/v1/auth/account-status`

- **DD filename:** `API_012_GET_auth_account_status.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Authenticated
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Lấy trạng thái tài khoản, xác thực, onboarding và quyền học hiện tại.
- **Input baseline:** Không có
- **Output baseline:** data: account_status, verification_status, onboarding_status, active_path, restrictions[], next_route
- **Business rules:** ACC-02, ACC-06

### API 013 — `POST /api/v1/auth/password/forgot`

- **DD filename:** `API_013_POST_auth_password_forgot.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Public
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Khởi tạo quy trình khôi phục mật khẩu mà không tiết lộ tài khoản có tồn tại.
- **Input baseline:** Body: identifier(email/phone)
- **Output baseline:** data: accepted=true, reset_channel?, masked_destination?, expires_at?
- **Business rules:** Không lộ dữ liệu nhạy cảm

### API 014 — `POST /api/v1/auth/password/reset`

- **DD filename:** `API_014_POST_auth_password_reset.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Public
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Đặt mật khẩu mới bằng token/OTP khôi phục.
- **Input baseline:** Body: reset_token_or_otp, new_password, confirm_password
- **Output baseline:** data: password_reset=true, sessions_revoked?, login_required=true
- **Business rules:** Luồng 3.4

### API 015 — `PUT /api/v1/auth/password`

- **DD filename:** `API_015_PUT_auth_password.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Authenticated
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Đổi mật khẩu khi đã đăng nhập.
- **Input baseline:** Body: current_password, new_password, confirm_password
- **Output baseline:** data: changed=true, changed_at, sessions_revoked?
- **Business rules:** Luồng 3.4

## 5. Trọng tâm thiết kế của batch

- Chuẩn hóa email/điện thoại, chống duplicate race condition và không tiết lộ tài khoản tồn tại.
- Hash mật khẩu, password policy, token/OTP TTL, resend throttling và brute-force protection.
- Vòng đời session/access/refresh token, logout/revocation và trạng thái tài khoản.
- Mọi sự kiện nhạy cảm phải có audit/security log nhưng không trả thông tin kỹ thuật.

## 6. Quy trình thực hiện cho từng API

1. **Reconcile nguồn:** đối chiếu catalog với BD, AC, Sequence, Class Diagram, schema SQL và kiến trúc. Ghi rõ dữ kiện, suy luận, giả định và xung đột.
2. **Tạo workbook:** sao chép template; đặt filename theo danh sách; không thay đổi cấu trúc sheet nếu chưa có lý do.
3. **Overview + History:** điền định danh, module, endpoint, method, auth, owner, source, transaction, affected tables, assumptions và version `0.1.0 Draft`.
4. **Request:** mô tả Path/Query/Header/Body theo JSON Path; type, format, required, nullable, default, validation và ví dụ.
5. **Response:** dùng canonical envelope; mọi field phải có source và mapping; list API phải có `meta.pagination`; HTTP 204 không có body.
6. **Data Mapping:** viết theo đúng execution order; tại mỗi query nêu bảng, mục đích, params, SQL/pseudocode, xử lý kết quả; nêu transaction, locking, idempotency, side effects và rollback.
7. **Error:** liệt kê toàn bộ validation/auth/permission/not-found/conflict/business/system/dependency errors; mỗi lỗi trỏ về Data Mapping Ref.; business code không trùng nghĩa.
8. **DB sheets:** chỉ duplicate `DB_TABLE_TEMPLATE` cho bảng có INSERT/UPDATE/DELETE/UPSERT hoặc thay đổi schema/constraint/index. SELECT thuần chỉ mô tả trong Data Mapping.
9. **Review chéo:** Request → variable → query/table → response; Data Mapping → Error; mutation → audit/notification/outbox; xóa toàn bộ placeholder không áp dụng.
10. **Chốt trạng thái:** chỉ đổi sang `Ready for Review` khi toàn bộ checklist đạt; API suy dẫn vẫn giữ cờ xác nhận.

## 7. Deliverables

- **9 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 9/9 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
