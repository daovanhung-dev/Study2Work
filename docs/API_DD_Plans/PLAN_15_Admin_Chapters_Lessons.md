# Plan 15 — Admin Chapters and Lessons

## 1. Mục tiêu

Hoàn thành **9 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **109–117**.

- API trực tiếp từ tài liệu/sequence: **0**.
- API suy dẫn từ BD: **9**.
- Module: 10. Admin quản trị nội dung (9).
- Lý do quy mô batch: 9 API cùng thay đổi cây nội dung cấp chapter/lesson; cần xử lý chung ordering, deletion safety, preview và versioning.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 14.
- Progress history.
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
- `BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md`

## 4. Danh sách API phải hoàn thành

### API 109 — `POST /api/v1/admin/courses/{course_id}/chapters`

- **DD filename:** `API_109_POST_admin_courses_by_course_id_chapters.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tạo chương trong khóa học.
- **Input baseline:** Path: course_id; Body: title, objectives[], estimated_duration?, unlock_conditions[], completion_conditions[], order?
- **Output baseline:** data: chapter, course_validation
- **Business rules:** ADM-CONT mục 4.3

### API 110 — `PATCH /api/v1/admin/chapters/{chapter_id}`

- **DD filename:** `API_110_PATCH_admin_chapters_by_chapter_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Cập nhật tiêu đề, mục tiêu, điều kiện mở khóa/hoàn thành chương.
- **Input baseline:** Path: chapter_id; Body: mutable fields; reason?
- **Output baseline:** data: updated_chapter, impact_warning?, audit_id?
- **Business rules:** ADM-CONT-03

### API 111 — `DELETE /api/v1/admin/chapters/{chapter_id}`

- **DD filename:** `API_111_DELETE_admin_chapters_by_chapter_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Xóa chương khi được phép hoặc từ chối nếu ảnh hưởng nội dung đã xuất bản.
- **Input baseline:** Path: chapter_id; Body: reason?
- **Output baseline:** data: deleted=true hoặc blocked_reason, affected_items_count, audit_id?
- **Business rules:** ADM-CONT-03, 07

### API 112 — `PUT /api/v1/admin/chapters/{chapter_id}/items/order`

- **DD filename:** `API_112_PUT_admin_chapters_by_chapter_id_items_order.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Sắp xếp bài học/bài tập trong chương.
- **Input baseline:** Path: chapter_id; Body: items[{type, id, order}]
- **Output baseline:** data: ordered_items[], impact_warning?, audit_id?
- **Business rules:** ADM-CONT mục 4.7

### API 113 — `POST /api/v1/admin/chapters/{chapter_id}/lessons`

- **DD filename:** `API_113_POST_admin_chapters_by_chapter_id_lessons.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Tạo bài học mới trong chương.
- **Input baseline:** Path: chapter_id; Body: title, description?, objectives[], content_blocks[], video?, required, completion_conditions[], order?
- **Output baseline:** data: lesson, status=DRAFT
- **Business rules:** ADM-CONT mục 4.4

### API 114 — `PATCH /api/v1/admin/lessons/{lesson_id}`

- **DD filename:** `API_114_PATCH_admin_lessons_by_lesson_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Cập nhật nội dung, video, ví dụ, điều kiện và tính bắt buộc của bài học.
- **Input baseline:** Path: lesson_id; Body: mutable lesson fields; reason? nếu published
- **Output baseline:** data: updated_lesson, changed_fields[], impact_warning?, audit_id?
- **Business rules:** ADM-CONT-03, 04

### API 115 — `DELETE /api/v1/admin/lessons/{lesson_id}`

- **DD filename:** `API_115_DELETE_admin_lessons_by_lesson_id.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Xóa/ẩn bài học khi hợp lệ, bảo toàn lịch sử nếu đã có người học.
- **Input baseline:** Path: lesson_id; Body: reason?
- **Output baseline:** data: deleted_or_archived, affected_learners_count, audit_id
- **Business rules:** ADM-CONT-07

### API 116 — `PUT /api/v1/admin/lessons/{lesson_id}/preview`

- **DD filename:** `API_116_PUT_admin_lessons_by_lesson_id_preview.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Content Admin/Admin
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Bật/tắt và cấu hình phạm vi bài học mẫu công khai.
- **Input baseline:** Path: lesson_id; Body: enabled, public_blocks[], public_resource_ids[]
- **Output baseline:** data: preview_config, validation, audit_id?
- **Business rules:** PC-03, ADM-CONT-05

### API 117 — `POST /api/v1/admin/lessons/{lesson_id}/lifecycle`

- **DD filename:** `API_117_POST_admin_lessons_by_lesson_id_lifecycle.xlsx`
- **Module:** 10. Admin quản trị nội dung
- **Authentication/Authorization:** Admin có quyền
- **Basis:** SUY DẪN
- **Source:** BD-10
- **Purpose:** Xuất bản, cập nhật, ẩn hoặc lưu trữ bài học.
- **Input baseline:** Path: lesson_id; Body: action, reason
- **Output baseline:** data: old_status, new_status, impact, audit_id
- **Business rules:** ADM-CONT-08

## 5. Trọng tâm thiết kế của batch

- Create/update/delete phải giữ tính toàn vẹn curriculum order.
- Không hard-delete nội dung đã phát sinh lịch sử học nếu BD yêu cầu bảo toàn.
- Preview public phải tách khỏi learner study và không tạo progress.
- Published lesson update cần version/audit và đánh giá ảnh hưởng.

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
