# Plan 06 — Courses Chapters Lessons Resources

## 1. Mục tiêu

Hoàn thành **9 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **39–47**.

- API trực tiếp từ tài liệu/sequence: **1**.
- API suy dẫn từ BD: **8**.
- Module: 05. Khóa học, chương, bài học và tài nguyên (9).
- Lý do quy mô batch: 9 API read/access cùng sử dụng content tree, access control, lock state và resource policy.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 05.
- Content lifecycle.
- Resource storage/access policy.
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
- `BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md`
- `BD/diagram/SEQUENCE/06. Study2Work_Study_SEQ_Hoc_Bai_Cap_Nhat_Tien_Do.md`
- `BD/diagram/AC/06. Study2Work_Study_AC_Khoa_Hoc_Noi_Dung_Hoc.md`
- `BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`

## 4. Danh sách API phải hoàn thành

### API 039 — `GET /api/v1/courses/{course_id}`

- **DD filename:** `API_039_GET_courses_by_course_id.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner/Optional Public
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Lấy chi tiết khóa học theo quyền truy cập của người xem.
- **Input baseline:** Path: course_id
- **Output baseline:** data: course details, goals[], prerequisites[], skills[], counts, learner_state, access_state, progress_percent?, sample_lessons[], related_paths[], community_groups[]
- **Business rules:** CRS-01, CRS-02

### API 040 — `GET /api/v1/courses/{course_id}/curriculum`

- **DD filename:** `API_040_GET_courses_by_course_id_curriculum.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner/Optional Public
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Lấy cây chương, bài học và bài tập cùng trạng thái khóa/hoàn thành.
- **Input baseline:** Path: course_id
- **Output baseline:** data: chapters[{id, order, title, objectives, unlock_state, completion_state, lessons[], assignments[]}], next_item
- **Business rules:** CRS-01, CRS-03

### API 041 — `GET /api/v1/chapters/{chapter_id}`

- **DD filename:** `API_041_GET_chapters_by_chapter_id.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Lấy chi tiết chương và các điều kiện mở khóa/hoàn thành.
- **Input baseline:** Path: chapter_id
- **Output baseline:** data: chapter, course_summary, items[], unlock_conditions[], completion_conditions[], missing_conditions[]
- **Business rules:** CRS-01

### API 042 — `GET /api/v1/lessons/{lesson_id}/study`

- **DD filename:** `API_042_GET_lessons_by_lesson_id_study.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner/Preview-capable Admin
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-06
- **Purpose:** Mở bài học, tải nội dung, tài nguyên, tiến độ hiện tại và điều hướng.
- **Input baseline:** Path: lesson_id
- **Output baseline:** data: title, objectives[], content_blocks[], video, resources[], self_check?, linked_assignments[], progress, previous_lesson?, next_lesson?, course_progress, community_link_summary?, access_state
- **Business rules:** CRS-01, CRS-03, CRS-07

### API 043 — `GET /api/v1/courses/{course_id}/continue`

- **DD filename:** `API_043_GET_courses_by_course_id_continue.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Xác định bài đang học hoặc nội dung bắt buộc tiếp theo trong khóa.
- **Input baseline:** Path: course_id
- **Output baseline:** data: next_item_type, next_item_id, title, reason, resume_position?, route
- **Business rules:** CRS-07

### API 044 — `GET /api/v1/lessons/{lesson_id}/resources`

- **DD filename:** `API_044_GET_lessons_by_lesson_id_resources.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Lấy tài liệu đính kèm theo quyền và phân loại bắt buộc/tham khảo.
- **Input baseline:** Path: lesson_id
- **Output baseline:** data[]: resource_id, type, title, description, required, source, usage_rights_summary?, access_url_or_action
- **Business rules:** CRS-05

### API 045 — `GET /api/v1/resources/{resource_id}/access`

- **DD filename:** `API_045_GET_resources_by_resource_id_access.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Tạo/nhận quyền truy cập hoặc URL tải tài nguyên hợp lệ.
- **Input baseline:** Path: resource_id
- **Output baseline:** data: resource_id, access_type=inline|download|external, url, expires_at?, required, tracking_required
- **Business rules:** CRS-01, CRS-05

### API 046 — `POST /api/v1/content-issues`

- **DD filename:** `API_046_POST_content_issues.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Báo lỗi video, tài liệu, nội dung, link hoặc bản quyền ngay tại màn học.
- **Input baseline:** Body: content_type, content_id, issue_type, description, evidence_url?
- **Output baseline:** data: issue_id, status=OPEN, submitted_at
- **Business rules:** CRS mục 4.6

### API 047 — `GET /api/v1/me/content-issues`

- **DD filename:** `API_047_GET_me_content_issues.xlsx`
- **Module:** 05. Khóa học, chương, bài học và tài nguyên
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-05
- **Purpose:** Theo dõi các báo lỗi nội dung đã gửi.
- **Input baseline:** Query: status?, page, page_size
- **Output baseline:** data[]: issue_id, content_ref, issue_type, status, response?, created_at, resolved_at?; meta
- **Business rules:** CRS mục 4.6

## 5. Trọng tâm thiết kế của batch

- Curriculum ordering và trạng thái locked/available/in-progress/completed phải nhất quán.
- Lesson study phải trả nội dung theo quyền, không trả nội dung chưa publish ngoài phạm vi.
- Resource access cần signed URL hoặc quyền truy cập có TTL; không lộ storage path.
- Content issue phải lưu source context, loại lỗi và trạng thái xử lý.

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
