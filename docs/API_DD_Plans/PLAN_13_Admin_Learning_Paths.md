# Plan 13 — Admin Learning Paths

## 1. Mục tiêu

Hoàn thành **7 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **94–100**.

- API trực tiếp từ tài liệu/sequence: **0**.
- API suy dẫn từ BD: **7**.
- Module: 10. Admin quản trị nội dung (7).
- Lý do quy mô batch: 7 API cùng quản trị learning path aggregate, course assignment, impact analysis và lifecycle.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Content lifecycle.
- Plan 05.
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
- `BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`
- `BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md`
- `BD/diagram/AC/11. Study2Work_Study_AC_Admin_Quan_Tri_Noi_Dung.md`
- `BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md`

## 4. Danh sách API phải hoàn thành

### API 094 — `GET /api/v1/admin/learning-paths`

- **DD filename:** `API_094_GET_admin_learning_paths.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tra cứu lộ trình ở mọi trạng thái vòng đời.
- **Input baseline:** Query: q?, status?, difficulty?, updated_by?, page, page_size, sort?
- **Output baseline:** data[]: admin path summary, publication_status, course_count, learner_impact_count; meta
- **Business rules:** ADM-CONT

### API 095 — `POST /api/v1/admin/learning-paths`

- **DD filename:** `API_095_POST_admin_learning_paths.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tạo lộ trình bản nháp.
- **Input baseline:** Body: name, slug, short_description, description, image_url?, difficulty, target_users[], excluded_users[], prerequisites[], outcomes[], estimated_duration, completion_conditions[], next_path_id?, community_group_ids[]?
- **Output baseline:** data: path, status=DRAFT, created_at
- **Business rules:** ADM-CONT-01

### API 096 — `GET /api/v1/admin/learning-paths/{path_id}`

- **DD filename:** `API_096_GET_admin_learning_paths_by_path_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Lấy chi tiết quản trị lộ trình và cấu hình khóa học.
- **Input baseline:** Path: path_id
- **Output baseline:** data: full path, courses[], lifecycle, validation_summary, impact_summary, audit_summary
- **Business rules:** ADM-CONT

### API 097 — `PATCH /api/v1/admin/learning-paths/{path_id}`

- **DD filename:** `API_097_PATCH_admin_learning_paths_by_path_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Cập nhật thông tin và điều kiện lộ trình.
- **Input baseline:** Path: path_id; Body: mutable path fields; reason? nếu đã xuất bản
- **Output baseline:** data: updated_path, changed_fields[], impact_warning?, audit_id?
- **Business rules:** ADM-CONT-03, ADM-CONT-08

### API 098 — `PUT /api/v1/admin/learning-paths/{path_id}/courses`

- **DD filename:** `API_098_PUT_admin_learning_paths_by_path_id_courses.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Gán và sắp xếp khóa học bắt buộc/tùy chọn trong lộ trình.
- **Input baseline:** Path: path_id; Body: courses[{course_id, order, required, unlock_rule?}]
- **Output baseline:** data: ordered_courses[], validation_warnings[], affected_learners_count, audit_id?
- **Business rules:** LP-06, ADM-CONT-06

### API 099 — `GET /api/v1/admin/learning-paths/{path_id}/impact`

- **DD filename:** `API_099_GET_admin_learning_paths_by_path_id_impact.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Xem số học viên, khóa học và tiến độ bị ảnh hưởng trước thay đổi.
- **Input baseline:** Path: path_id; Query: proposed_change_type?
- **Output baseline:** data: active_learners, completed_learners, related_courses, progress_risk_summary, notification_recommended
- **Business rules:** ADM-CONT-03

### API 100 — `POST /api/v1/admin/learning-paths/{path_id}/lifecycle`

- **DD filename:** `API_100_POST_admin_learning_paths_by_path_id_lifecycle.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Admin có quyền xuất bản
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Chuyển trạng thái DRAFT/IN_REVIEW/PUBLISHED/UPDATED/ARCHIVED.
- **Input baseline:** Path: path_id; Body: action=SUBMIT_REVIEW|PUBLISH|ARCHIVE|RESTORE|MARK_UPDATED, reason, effective_at?
- **Output baseline:** data: old_status, new_status, validation, affected_learners_count, audit_id
- **Business rules:** ADM-CONT-01, 02, 08

## 5. Trọng tâm thiết kế của batch

- DRAFT/IN_REVIEW/PUBLISHED/UPDATED/ARCHIVED state machine.
- Course assignment/order phải atomic và kiểm tra duplicate.
- Impact preview phải chạy trước thay đổi ảnh hưởng learner.
- Published update cần versioning, notification và audit.

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

- **7 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 7/7 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
