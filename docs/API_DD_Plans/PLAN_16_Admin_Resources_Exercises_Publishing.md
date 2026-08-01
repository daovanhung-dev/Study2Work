# Plan 16 — Admin Resources Exercises and Publishing

## 1. Mục tiêu

Hoàn thành **10 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **118–127**.

- API trực tiếp từ tài liệu/sequence: **2**.
- API suy dẫn từ BD: **8**.
- Module: 10. Admin quản trị nội dung (10).
- Lý do quy mô batch: 10 API gồm resource, exercise và publish gate; cùng phụ thuộc quyền nội dung, integrity, impact và audit.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 13-15.
- Plan 07-08.
- Notification outbox.
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
- `BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md`
- `BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md`

## 4. Danh sách API phải hoàn thành

### API 118 — `POST /api/v1/admin/resources`

- **DD filename:** `API_118_POST_admin_resources.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tạo tài liệu/tài nguyên và gắn nguồn, quyền sử dụng.
- **Input baseline:** Body: type=PDF|SLIDE|MARKDOWN|LINK|CODE|FILE, title, description?, source, usage_rights, owner, file_id_or_url, required, lesson_ids[]?, course_ids[]?
- **Output baseline:** data: resource, validation
- **Business rules:** ADM-CONT-02

### API 119 — `PATCH /api/v1/admin/resources/{resource_id}`

- **DD filename:** `API_119_PATCH_admin_resources_by_resource_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Cập nhật mô tả, nguồn, quyền, liên kết và tính bắt buộc.
- **Input baseline:** Path: resource_id; Body: mutable fields; reason?
- **Output baseline:** data: updated_resource, impact_warning?, audit_id?
- **Business rules:** ADM-CONT-02, 03

### API 120 — `DELETE /api/v1/admin/resources/{resource_id}`

- **DD filename:** `API_120_DELETE_admin_resources_by_resource_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Ẩn/xóa tài nguyên không còn hợp lệ.
- **Input baseline:** Path: resource_id; Body: reason
- **Output baseline:** data: hidden_or_deleted, affected_content[], audit_id
- **Business rules:** ADM-CONT-07

### API 121 — `GET /api/v1/admin/exercises`

- **DD filename:** `API_121_GET_admin_exercises.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tra cứu cấu hình bài tập.
- **Input baseline:** Query: q?, type?, status?, course_id?, chapter_id?, lesson_id?, page, page_size
- **Output baseline:** data[]: assignment admin summary; meta
- **Business rules:** ADM-CONT mục 4.6

### API 122 — `POST /api/v1/admin/exercises`

- **DD filename:** `API_122_POST_admin_exercises.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tạo bài tập và cấu hình hình thức nộp/chấm.
- **Input baseline:** Body: title, type, scope, objectives[], requirements, expected_input_output?, completion_criteria[], max_score?, hints[], resources[], due_at?, submission_methods[], rubric?, required, allow_resubmit, quiz_answers?
- **Output baseline:** data: assignment, status=DRAFT, validation
- **Business rules:** EX-04, ADM-CONT

### API 123 — `GET /api/v1/admin/exercises/{assignment_id}`

- **DD filename:** `API_123_GET_admin_exercises_by_assignment_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Lấy đầy đủ cấu hình bài tập, đáp án/rubric và thống kê ảnh hưởng.
- **Input baseline:** Path: assignment_id
- **Output baseline:** data: full assignment, linkage, submissions_summary, lifecycle, impact
- **Business rules:** ADM-CONT

### API 124 — `PATCH /api/v1/admin/exercises/{assignment_id}`

- **DD filename:** `API_124_PATCH_admin_exercises_by_assignment_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Cập nhật đề, hạn, đáp án, rubric, bắt buộc và quyền nộp lại.
- **Input baseline:** Path: assignment_id; Body: mutable fields; reason? nếu published
- **Output baseline:** data: updated_assignment, impact_warning?, audit_id?
- **Business rules:** ADM-CONT-03

### API 125 — `DELETE /api/v1/admin/exercises/{assignment_id}`

- **DD filename:** `API_125_DELETE_admin_exercises_by_assignment_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Xóa/ẩn bài tập nếu hợp lệ, không phá lịch sử bài nộp.
- **Input baseline:** Path: assignment_id; Body: reason
- **Output baseline:** data: deleted_or_archived, submission_count, audit_id
- **Business rules:** ADM-CONT-07

### API 126 — `POST /api/v1/admin/content/{content_type}/{content_id}/pre-publish-check`

- **DD filename:** `API_126_POST_admin_content_by_content_type_by_content_id_pre_publish_check.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-11
- **Purpose:** Chạy checklist trước xuất bản cho một hoặc nhiều nội dung.
- **Input baseline:** Body: items[{type, id}]
- **Output baseline:** data: valid, errors[], warnings[], checks[{code, passed, message, entity}]
- **Business rules:** ADM-CONT mục 4.8

### API 127 — `POST /api/v1/admin/content/{content_type}/{content_id}/publish`

- **DD filename:** `API_127_POST_admin_content_by_content_type_by_content_id_publish.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-11
- **Purpose:** Xem tác động và thông báo cần gửi trước khi xuất bản/cập nhật quan trọng.
- **Input baseline:** Path: content_type, content_id; Body: proposed_action, change_summary?
- **Output baseline:** data: validation, affected_learners_count, progress_impacts[], related_paths[], notification_recommendation, versioning_recommendation
- **Business rules:** ADM-CONT mục 4.9

## 5. Trọng tâm thiết kế của batch

- Resource source/license/access policy và safe deletion.
- Exercise rubric/answer/attempt policy và bảo toàn submission history.
- Pre-publish check phải trả lỗi/warning có cấu trúc, không thay đổi nội dung.
- Publish/update quan trọng cần transaction, impact summary, audit và notification outbox.

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

- **10 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 10/10 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
