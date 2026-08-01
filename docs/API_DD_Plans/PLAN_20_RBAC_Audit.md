# Plan 20 — RBAC and Audit

## 1. Mục tiêu

Hoàn thành **8 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **150–157**.

- API trực tiếp từ tài liệu/sequence: **1**.
- API suy dẫn từ BD: **7**.
- Module: 13. Vai trò, phân quyền và audit (8).
- Lý do quy mô batch: 8 API tạo security control plane; cần cùng một permission vocabulary và quy tắc chống privilege escalation.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Canonical role/permission catalog.
- Audit event schema.
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
- `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`
- `BD/diagram/SEQUENCE/14. Study2Work_Study_SEQ_RBAC_Audit.md`
- `BD/diagram/AC/14. Study2Work_Study_AC_RBAC_Audit_Log.md`

## 4. Danh sách API phải hoàn thành

### API 150 — `GET /api/v1/admin/rbac/roles`

- **DD filename:** `API_150_GET_admin_rbac_roles.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Super Admin/Admin xem quyền
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Lấy danh sách vai trò nghiệp vụ.
- **Input baseline:** Không có
- **Output baseline:** data[]: role_code, name, description, risk_level, user_count
- **Business rules:** RBAC-01

### API 151 — `GET /api/v1/admin/rbac/permissions`

- **DD filename:** `API_151_GET_admin_rbac_permissions.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Super Admin/Admin xem quyền
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Lấy danh mục quyền chức năng.
- **Input baseline:** Query: group?
- **Output baseline:** data[]: permission_code, name, group, description, risk_level
- **Business rules:** RBAC-01

### API 152 — `GET /api/v1/admin/rbac/matrix`

- **DD filename:** `API_152_GET_admin_rbac_matrix.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Super Admin/Admin xem quyền
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Lấy ma trận vai trò-quyền để kiểm thử và quản trị.
- **Input baseline:** Không có
- **Output baseline:** data: roles[], permissions[], grants[{role_code, permission_code}]
- **Business rules:** RBAC-01

### API 153 — `GET /api/v1/admin/users/{user_id}/roles`

- **DD filename:** `API_153_GET_admin_users_by_user_id_roles.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Super Admin
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Xem vai trò quản trị của một người dùng.
- **Input baseline:** Path: user_id
- **Output baseline:** data: user_summary, roles[], effective_permissions[]
- **Business rules:** RBAC-01

### API 154 — `POST /api/v1/admin/users/{user_id}/roles`

- **DD filename:** `API_154_POST_admin_users_by_user_id_roles.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Super Admin
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Cấp vai trò Admin/Support/Moderator/Content Admin.
- **Input baseline:** Path: user_id; Body: role_code, reason, expires_at?
- **Output baseline:** data: assigned_role, effective_permissions[], audit_id
- **Business rules:** RBAC-06

### API 155 — `DELETE /api/v1/admin/users/{user_id}/roles/{role_code}`

- **DD filename:** `API_155_DELETE_admin_users_by_user_id_roles_by_role_code.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Super Admin
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Thu hồi vai trò quản trị.
- **Input baseline:** Path: user_id, role_code; Body: reason
- **Output baseline:** data: revoked=true, effective_permissions[], audit_id
- **Business rules:** RBAC-06

### API 156 — `GET /api/v1/admin/audit-logs`

- **DD filename:** `API_156_GET_admin_audit_logs.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Admin/Super Admin theo phạm vi
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-14
- **Purpose:** Tìm audit log theo đối tượng, người thực hiện, hành động và thời gian.
- **Input baseline:** Query: actor_id?, actor_role?, target_type?, target_id?, action?, channel?, from?, to?, page, page_size, sort=desc
- **Output baseline:** data[]: audit_id, actor, role, occurred_at, target, action, before_summary?, after_summary?, reason?, channel; meta
- **Business rules:** RBAC-05, RBAC-07

### API 157 — `GET /api/v1/admin/audit-logs/{audit_id}`

- **DD filename:** `API_157_GET_admin_audit_logs_by_audit_id.xlsx`
- **Module:** 13. Vai trò, phân quyền và audit
- **Authentication/Authorization:** Admin/Super Admin theo phạm vi
- **Basis:** SUY DẪN
- **Source:** BD-13
- **Purpose:** Xem chi tiết một bản ghi audit.
- **Input baseline:** Path: audit_id
- **Output baseline:** data: actor, role, timestamp, target, action, before, after, reason, channel, correlation_id?
- **Business rules:** RBAC-05, RBAC-07

## 5. Trọng tâm thiết kế của batch

- Role-permission matrix, scope và inherited/effective permissions.
- Chỉ Super Admin hoặc quyền tương đương được cấp/thu hồi role nhạy cảm.
- Chống self-escalation, xóa role cuối cùng và conflict of duties.
- Audit log immutable, filterable, PII-safe và có before/after phù hợp.

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
