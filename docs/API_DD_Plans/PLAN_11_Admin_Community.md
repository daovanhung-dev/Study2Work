# Plan 11 — Admin Community

## 1. Mục tiêu

Hoàn thành **8 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **75–82**.

- API trực tiếp từ tài liệu/sequence: **1**.
- API suy dẫn từ BD: **7**.
- Module: 08. Cộng đồng Zalo (8).
- Lý do quy mô batch: 8 API quản trị cùng một aggregate group/report và cần thống nhất lifecycle, scope, moderator và audit.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 10.
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
- `BD/08. Study2Work_Study_BasicDesign_Cong_Dong_Zalo.md`
- `BD/diagram/SEQUENCE/09. Study2Work_Study_SEQ_Cong_Dong_Zalo.md`
- `BD/diagram/AC/09. Study2Work_Study_AC_Cong_Dong_Zalo.md`
- `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`

## 4. Danh sách API phải hoàn thành

### API 075 — `GET /api/v1/admin/community-groups`

- **DD filename:** `API_075_GET_admin_community_groups.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Tra cứu và quản lý danh sách nhóm cộng đồng.
- **Input baseline:** Query: q?, scope?, status?, moderator_id?, page, page_size
- **Output baseline:** data[]: group management summary; meta
- **Business rules:** COM-07

### API 076 — `POST /api/v1/admin/community-groups`

- **DD filename:** `API_076_POST_admin_community_groups.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator có quyền
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Tạo nhóm cộng đồng và gắn phạm vi áp dụng.
- **Input baseline:** Body: name, description, scope_type, scope_ids[], join_url, rules[], moderator_ids[], visibility, status
- **Output baseline:** data: created_group, audit_id
- **Business rules:** Module 4.6

### API 077 — `GET /api/v1/admin/community-groups/{group_id}`

- **DD filename:** `API_077_GET_admin_community_groups_by_group_id.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Lấy chi tiết quản trị nhóm, link, quy tắc, phạm vi và báo cáo.
- **Input baseline:** Path: group_id
- **Output baseline:** data: full_group, scopes[], moderators[], reports_summary, open_link_metrics
- **Business rules:** Module 4.6

### API 078 — `PATCH /api/v1/admin/community-groups/{group_id}`

- **DD filename:** `API_078_PATCH_admin_community_groups_by_group_id.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator có quyền
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-09
- **Purpose:** Cập nhật tên, mô tả, link, quy tắc và điều kiện hiển thị.
- **Input baseline:** Path: group_id; Body: mutable fields, reason? khi đổi link
- **Output baseline:** data: updated_group, changed_fields[], audit_id
- **Business rules:** RBAC audit nhóm cộng đồng

### API 079 — `PUT /api/v1/admin/community-groups/{group_id}/status`

- **DD filename:** `API_079_PUT_admin_community_groups_by_group_id_status.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator có quyền
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Chuyển trạng thái hoạt động, tạm dừng, đầy thành viên hoặc lưu trữ.
- **Input baseline:** Path: group_id; Body: status=ACTIVE|PAUSED|FULL|ARCHIVED, reason
- **Output baseline:** data: status, changed_at, affected_learners_count, notification_created?, audit_id
- **Business rules:** COM-07

### API 080 — `PUT /api/v1/admin/community-groups/{group_id}/moderators`

- **DD filename:** `API_080_PUT_admin_community_groups_by_group_id_moderators.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Gán hoặc thay người phụ trách nhóm.
- **Input baseline:** Path: group_id; Body: moderator_ids[], reason?
- **Output baseline:** data: moderators[], changed_at, audit_id
- **Business rules:** RBAC audit

### API 081 — `GET /api/v1/admin/community-reports`

- **DD filename:** `API_081_GET_admin_community_reports.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Lấy hàng đợi báo cáo cộng đồng.
- **Input baseline:** Query: status?, issue_type?, group_id?, page, page_size
- **Output baseline:** data[]: report summary; meta
- **Business rules:** Module 4.5

### API 082 — `PATCH /api/v1/admin/community-reports/{report_id}`

- **DD filename:** `API_082_PATCH_admin_community_reports_by_report_id.xlsx`
- **Module:** 08. Cộng đồng Zalo
- **Authentication/Authorization:** Admin/Moderator
- **Basis:** SUY DẪN
- **Source:** BD-08
- **Purpose:** Xử lý báo cáo cộng đồng và ghi kết quả.
- **Input baseline:** Path: report_id; Body: status=IN_REVIEW|RESOLVED|REJECTED, resolution, action_taken?
- **Output baseline:** data: report, resolved_by, resolved_at, affected_group_status?, audit_id
- **Business rules:** COM-07

## 5. Trọng tâm thiết kế của batch

- Lifecycle ACTIVE/PAUSED/FULL/ARCHIVED và điều kiện chuyển trạng thái.
- Phạm vi gắn group theo path/course/topic và tránh cấu hình xung đột.
- Moderator assignment phải kiểm tra role/scope.
- Report resolution phải lưu kết quả, người xử lý, thời điểm và audit.

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
