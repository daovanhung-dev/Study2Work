# Plan 17 — Admin Learner Lookup and Support Resolution

## 1. Mục tiêu

Hoàn thành **6 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **128–133**.

- API trực tiếp từ tài liệu/sequence: **2**.
- API suy dẫn từ BD: **4**.
- Module: 11. Admin quản lý học viên và hỗ trợ ngoại lệ (6).
- Lý do quy mô batch: 6 API read/resolve cùng phục vụ support workflow và cần chung scope, PII masking, request context và decision record.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 05.
- RBAC.
- Audit log.
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
- `BD/11. Study2Work_Study_BasicDesign_Admin_Quan_Ly_Hoc_Vien_Ho_Tro_Ngoai_Le.md`
- `BD/diagram/SEQUENCE/12. Study2Work_Study_SEQ_Admin_Ho_Tro_Ngoai_Le.md`
- `BD/diagram/AC/12. Study2Work_Study_AC_Admin_Hoc_Vien_Ho_Tro_Ngoai_Le.md`
- `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`

## 4. Danh sách API phải hoàn thành

### API 128 — `GET /api/v1/admin/learners`

- **DD filename:** `API_128_GET_admin_learners.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Tra cứu học viên theo tên, liên hệ, mã, lộ trình và trạng thái.
- **Input baseline:** Query: q?, email?, phone?, learner_code?, path_id?, account_status?, onboarding_status?, support_status?, page, page_size
- **Output baseline:** data[]: learner summary, verification_state, account_status, active_path, progress_percent, open_support_request_count; meta
- **Business rules:** ADM-LRN

### API 129 — `GET /api/v1/admin/learners/{learner_id}/support-profile`

- **DD filename:** `API_129_GET_admin_learners_by_learner_id_support_profile.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-12
- **Purpose:** Lấy hồ sơ hỗ trợ tổng hợp, không trả mật khẩu/OTP.
- **Input baseline:** Path: learner_id
- **Output baseline:** data: basic_account, verification, onboarding, active_path, path_history, course_progress_summary, pending_assignments, support_history, admin_action_history
- **Business rules:** ADM-LRN-01

### API 130 — `GET /api/v1/admin/learners/{learner_id}/progress`

- **DD filename:** `API_130_GET_admin_learners_by_learner_id_progress.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Xem tiến độ chi tiết phục vụ hỗ trợ nhưng không sửa trực tiếp.
- **Input baseline:** Path: learner_id
- **Output baseline:** data: path_progress, courses[], chapters_or_lessons_incomplete[], assignments_by_status, last_learning_at, dropout_risk_indicators?
- **Business rules:** ADM-LRN-02

### API 131 — `GET /api/v1/admin/support-requests`

- **DD filename:** `API_131_GET_admin_support_requests.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Lấy hàng đợi yêu cầu đổi/reset/hủy lộ trình.
- **Input baseline:** Query: type?, status?, learner_id?, path_id?, assigned_to?, page, page_size, sort=oldest|newest
- **Output baseline:** data[]: request summary, learner, current_path, target_path?, reason, status, submitted_at; meta
- **Business rules:** ADM-LRN-03

### API 132 — `GET /api/v1/admin/support-requests/{request_id}`

- **DD filename:** `API_132_GET_admin_support_requests_by_request_id.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Xem yêu cầu, hồ sơ, tiến độ và lịch sử xử lý trước khi quyết định.
- **Input baseline:** Path: request_id
- **Output baseline:** data: request, learner_snapshot, progress_snapshot, prior_requests[], allowed_actions[], impact_preview
- **Business rules:** ADM-LRN-03

### API 133 — `POST /api/v1/admin/support-requests/{request_id}/resolve`

- **DD filename:** `API_133_POST_admin_support_requests_by_request_id_resolve.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin hoặc Support đủ quyền
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-12
- **Purpose:** Chấp thuận/từ chối yêu cầu và chọn hành động ngoại lệ.
- **Input baseline:** Path: request_id; Body: decision=APPROVE|REJECT, action=RESET|CANCEL|TRANSFER?, target_path_id?, reason, learner_message
- **Output baseline:** data: request_status, resulting_states, audit_id, notification_created
- **Business rules:** ADM-LRN-03, 04, 07

## 5. Trọng tâm thiết kế của batch

- Search/profile/progress phải giới hạn theo permission và mask PII.
- Không trả password hash, OTP, secret hoặc dữ liệu ngoài phạm vi.
- Resolve support request phải kiểm tra trạng thái hiện tại và chống xử lý hai lần.
- Decision phải lưu reason, action, actor, timestamp và audit.

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

- **6 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 6/6 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
