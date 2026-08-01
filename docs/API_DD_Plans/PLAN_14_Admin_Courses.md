# Plan 14 — Admin Courses

## 1. Mục tiêu

Hoàn thành **8 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **101–108**.

- API trực tiếp từ tài liệu/sequence: **0**.
- API suy dẫn từ BD: **8**.
- Module: 10. Admin quản trị nội dung (8).
- Lý do quy mô batch: 8 API cùng quản trị course aggregate, path assignment, chapter order, impact và lifecycle.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 13.
- Plan 06.
- Content lifecycle.
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
- `BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md`

## 4. Danh sách API phải hoàn thành

### API 101 — `GET /api/v1/admin/courses`

- **DD filename:** `API_101_GET_admin_courses.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tra cứu khóa học ở mọi trạng thái.
- **Input baseline:** Query: q?, status?, level?, path_id?, page, page_size
- **Output baseline:** data[]: admin course summary, path_count, chapter_count, learner_impact_count; meta
- **Business rules:** ADM-CONT

### API 102 — `POST /api/v1/admin/courses`

- **DD filename:** `API_102_POST_admin_courses.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tạo khóa học bản nháp.
- **Input baseline:** Body: name, slug, descriptions, image_url?, level, estimated_duration, goals[], prerequisites[], skills[], completion_conditions[], community_group_ids[]?
- **Output baseline:** data: course, status=DRAFT
- **Business rules:** ADM-CONT-01

### API 103 — `GET /api/v1/admin/courses/{course_id}`

- **DD filename:** `API_103_GET_admin_courses_by_course_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Lấy cấu hình đầy đủ khóa học, curriculum và tác động.
- **Input baseline:** Path: course_id
- **Output baseline:** data: full course, chapters[], related_paths[], sample_lessons[], lifecycle, validation, impact
- **Business rules:** ADM-CONT-06

### API 104 — `PATCH /api/v1/admin/courses/{course_id}`

- **DD filename:** `API_104_PATCH_admin_courses_by_course_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Cập nhật thông tin, điều kiện hoàn thành và nhóm cộng đồng khóa học.
- **Input baseline:** Path: course_id; Body: mutable fields; reason? nếu published
- **Output baseline:** data: updated_course, changed_fields[], impact_warning?, audit_id?
- **Business rules:** ADM-CONT-03, ADM-CONT-08

### API 105 — `PUT /api/v1/admin/courses/{course_id}/paths`

- **DD filename:** `API_105_PUT_admin_courses_by_course_id_paths.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Gán khóa học vào một hoặc nhiều lộ trình.
- **Input baseline:** Path: course_id; Body: paths[{path_id, required?, order?}]
- **Output baseline:** data: related_paths[], validation_warnings[], impact_summary
- **Business rules:** ADM-CONT-06

### API 106 — `PUT /api/v1/admin/courses/{course_id}/chapters/order`

- **DD filename:** `API_106_PUT_admin_courses_by_course_id_chapters_order.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Sắp xếp thứ tự chương trong khóa học.
- **Input baseline:** Path: course_id; Body: chapter_ids_in_order[]
- **Output baseline:** data: chapters_order, impact_warning?, audit_id?
- **Business rules:** ADM-CONT mục 4.7

### API 107 — `GET /api/v1/admin/courses/{course_id}/impact`

- **DD filename:** `API_107_GET_admin_courses_by_course_id_impact.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Xem học viên và lộ trình bị ảnh hưởng trước cập nhật khóa học.
- **Input baseline:** Path: course_id
- **Output baseline:** data: active_learners, related_paths[], completed_learners, progress_risk_summary, versioning_recommended
- **Business rules:** ADM-CONT-03, 06

### API 108 — `POST /api/v1/admin/courses/{course_id}/lifecycle`

- **DD filename:** `API_108_POST_admin_courses_by_course_id_lifecycle.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Admin có quyền xuất bản
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Chuyển trạng thái vòng đời khóa học.
- **Input baseline:** Path: course_id; Body: action, reason, effective_at?
- **Output baseline:** data: old_status, new_status, validation, affected_learners_count, audit_id
- **Business rules:** ADM-CONT-08

## 5. Trọng tâm thiết kế của batch

- Điều kiện hoàn thành và association với paths phải được validate.
- Chapter order update phải atomic, không trùng/thất lạc item.
- Impact endpoint không được thay đổi dữ liệu.
- Lifecycle phải kiểm tra curriculum completeness và learner impact.

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
