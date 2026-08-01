# Plan 03 — Profile Contact Navigation

## 1. Mục tiêu

Hoàn thành **5 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **16–20**.

- API trực tiếp từ tài liệu/sequence: **0**.
- API suy dẫn từ BD: **5**.
- Module: 02. Tài khoản, xác thực và hồ sơ (5).
- Lý do quy mô batch: 5 API có cùng ownership dữ liệu người dùng và phụ thuộc trực tiếp trạng thái tài khoản/onboarding.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 02.
- Onboarding state.
- Learning path enrollment state.
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
- `BD/diagram/AC/03. Study2Work_Study_AC_Tai_Khoan_Xac_Thuc_Ho_So.md`
- `BD/03. Study2Work_Study_BasicDesign_Onboarding.md`
- `BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md`

## 4. Danh sách API phải hoàn thành

### API 016 — `GET /api/v1/me/profile`

- **DD filename:** `API_016_GET_me_profile.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Lấy hồ sơ tài khoản, hồ sơ học tập và thiết lập cá nhân.
- **Input baseline:** Không có
- **Output baseline:** data: basic_profile, verified_contacts, learning_profile, notification_preferences_summary, path_history_summary
- **Business rules:** ACC-07

### API 017 — `PATCH /api/v1/me/profile`

- **DD filename:** `API_017_PATCH_me_profile.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Cập nhật các trường hồ sơ học viên được phép tự sửa.
- **Input baseline:** Body: display_name?, avatar_url?, province?, school_or_company?, current_major_or_job?, primary_goal?, weekly_study_hours?, preferred_time_slots?
- **Output baseline:** data: updated_profile, updated_fields[], updated_at
- **Business rules:** ACC-05, ACC-07

### API 018 — `POST /api/v1/me/contact-change`

- **DD filename:** `API_018_POST_me_contact_change.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Yêu cầu đổi email/số điện thoại và gửi xác thực kênh mới.
- **Input baseline:** Body: contact_type=email|phone, new_value, current_password?
- **Output baseline:** data: change_request_id, masked_new_value, verification_required, expires_at
- **Business rules:** ACC-03

### API 019 — `POST /api/v1/me/contact-change/confirm`

- **DD filename:** `API_019_POST_me_contact_change_confirm.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Xác nhận kênh liên hệ mới trước khi áp dụng.
- **Input baseline:** Body: change_request_id, token_or_otp
- **Output baseline:** data: contact_changed=true, verified_contact, changed_at
- **Business rules:** ACC-03

### API 020 — `GET /api/v1/me/navigation-context`

- **DD filename:** `API_020_GET_me_navigation_context.xlsx`
- **Module:** 02. Tài khoản, xác thực và hồ sơ
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-02
- **Purpose:** Xác định màn hình đích sau đăng nhập hoặc khi mở hành động bắt đầu học.
- **Input baseline:** Không có
- **Output baseline:** data: account_status, verification_required, onboarding_required, active_path, can_activate_path, next_route, blocking_reason?
- **Business rules:** PC-05, ACC luồng 4.2

## 5. Trọng tâm thiết kế của batch

- Phân định field người dùng được tự sửa và field hệ thống quản lý.
- Đổi email/điện thoại phải xác thực kênh mới trước khi cập nhật chính thức.
- Mask dữ liệu liên hệ và chống account enumeration.
- Navigation context phải quyết định theo account status, onboarding status và active path.

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

- **5 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 5/5 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
