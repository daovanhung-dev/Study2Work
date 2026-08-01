# Plan 18 — Admin Learner Exceptional Actions

## 1. Mục tiêu

Hoàn thành **8 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **134–141**.

- API trực tiếp từ tài liệu/sequence: **0**.
- API suy dẫn từ BD: **8**.
- Module: 11. Admin quản lý học viên và hỗ trợ ngoại lệ (8).
- Lý do quy mô batch: 8 API mutation/audit có rủi ro cao; gom để áp dụng thống nhất reason, authorization, transaction, notification và rollback.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 17.
- Plan 09.
- Plan 02.
- RBAC.
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

### API 134 — `POST /api/v1/admin/learners/{learner_id}/progress-reset`

- **DD filename:** `API_134_POST_admin_learners_by_learner_id_progress_reset.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin có quyền cao
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Reset tiến độ theo phạm vi và lý do bắt buộc.
- **Input baseline:** Path: learner_id; Body: scope_type=PATH|COURSE|CHAPTER|LESSON|ASSIGNMENT, scope_id, reason, support_request_id?
- **Output baseline:** data: reset_id, before_summary, after_summary, audit_id, learner_notified
- **Business rules:** ADM-LRN-03, 06

### API 135 — `POST /api/v1/admin/learners/{learner_id}/active-path/cancel`

- **DD filename:** `API_135_POST_admin_learners_by_learner_id_active_path_cancel.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Hủy lộ trình ACTIVE theo ngoại lệ.
- **Input baseline:** Path: learner_id; Body: enrollment_id, reason, allow_choose_new_path
- **Output baseline:** data: old_status=ACTIVE, new_status=CANCELLED_BY_ADMIN, learner_eligibility, audit_id, notification_created
- **Business rules:** ADM-LRN-03, LP-04

### API 136 — `POST /api/v1/admin/learners/{learner_id}/active-path/transfer`

- **DD filename:** `API_136_POST_admin_learners_by_learner_id_active_path_transfer.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Chuyển lộ trình bảo đảm không tạo hai lộ trình ACTIVE đồng thời.
- **Input baseline:** Path: learner_id; Body: current_enrollment_id, target_path_id, progress_policy=RESET|KEEP_HISTORY, reason
- **Output baseline:** data: old_enrollment_status, new_enrollment, active_count=1, audit_id, learner_notified
- **Business rules:** ADM-LRN-04

### API 137 — `POST /api/v1/admin/learners/{learner_id}/suspend`

- **DD filename:** `API_137_POST_admin_learners_by_learner_id_suspend.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Tạm ngừng tài khoản vì vi phạm, bảo vệ tài khoản hoặc yêu cầu nội bộ.
- **Input baseline:** Path: learner_id; Body: reason, category, until?
- **Output baseline:** data: account_status=SUSPENDED, suspended_at, suspended_by, restrictions[], audit_id, notification_created
- **Business rules:** ACC-06, ADM-LRN-05

### API 138 — `POST /api/v1/admin/learners/{learner_id}/unsuspend`

- **DD filename:** `API_138_POST_admin_learners_by_learner_id_unsuspend.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Mở lại tài khoản và ghi lý do.
- **Input baseline:** Path: learner_id; Body: reason
- **Output baseline:** data: account_status, reopened_at, reopened_by, audit_id, notification_created
- **Business rules:** ADM-LRN-05

### API 139 — `GET /api/v1/admin/learners/{learner_id}/support-notes`

- **DD filename:** `API_139_GET_admin_learners_by_learner_id_support_notes.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Lấy ghi chú nội bộ theo quyền.
- **Input baseline:** Path: learner_id; Query: page, page_size
- **Output baseline:** data[]: note_id, content, author, visibility=INTERNAL|OFFICIAL_RESPONSE, created_at; meta
- **Business rules:** ADM-LRN-08

### API 140 — `POST /api/v1/admin/learners/{learner_id}/support-notes`

- **DD filename:** `API_140_POST_admin_learners_by_learner_id_support_notes.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Learner Support/Admin
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Tạo ghi chú nội bộ hoặc phản hồi chính thức.
- **Input baseline:** Path: learner_id; Body: content, visibility, related_request_id?
- **Output baseline:** data: note, notification_created_if_official
- **Business rules:** ADM-LRN-08

### API 141 — `GET /api/v1/admin/learners/{learner_id}/audit`

- **DD filename:** `API_141_GET_admin_learners_by_learner_id_audit.xlsx`
- **Module:** 11. Admin quản lý học viên và hỗ trợ ngoại lệ
- **Authentication/Authorization:** Admin có quyền
- **Basis:** SUY DẪN
- **Source:** BD-11
- **Purpose:** Xem audit log liên quan riêng đến học viên.
- **Input baseline:** Path: learner_id; Query: action_type?, from?, to?, page, page_size
- **Output baseline:** data[]: audit entries; meta
- **Business rules:** RBAC audit

## 5. Trọng tâm thiết kế của batch

- Progress reset, path cancel/transfer phải có scope, reason và impact preview.
- Transfer phải bảo đảm không tạo hai ACTIVE path.
- Suspend/unsuspend cần policy, session revocation và notification.
- Support notes phân biệt internal note/official response; audit không được sửa.

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

- **8 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 8/8 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
