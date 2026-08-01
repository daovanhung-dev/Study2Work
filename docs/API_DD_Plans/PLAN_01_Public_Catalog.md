# Plan 01 — Public Catalog

## 1. Mục tiêu

Hoàn thành **6 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **1–6**.

- API trực tiếp từ tài liệu/sequence: **3**.
- API suy dẫn từ BD: **3**.
- Module: 01. Public Catalog (6).
- Lý do quy mô batch: 6 API đọc công khai, cùng mô hình filter/pagination và kiểm soát publication; xử lý trong một batch giúp thống nhất contract catalog.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Chuẩn response envelope.
- Quy ước pagination.
- Publication status của lộ trình/khóa học/bài học.
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
- `BD/01. Study2Work_Study_BasicDesign_Public_Catalog.md`
- `BD/diagram/SEQUENCE/02. Study2Work_Study_SEQ_Public_Catalog.md`
- `BD/diagram/AC/02. Study2Work_Study_AC_Public_Catalog.md`

## 4. Danh sách API phải hoàn thành

### API 001 — `GET /api/v1/catalog/overview`

- **DD filename:** `API_001_GET_catalog_overview.xlsx`
- **Module:** 01. Public Catalog
- **Authentication/Authorization:** Public
- **Basis:** SUY DẪN
- **Source:** BD-01
- **Purpose:** Lấy nội dung giới thiệu Study và điều hướng đến danh mục.
- **Input baseline:** Query: locale?
- **Output baseline:** data: title, value_proposition, target_users[], content_structure[], featured_paths[], featured_courses[]
- **Business rules:** PC-01

### API 002 — `GET /api/v1/catalog/learning-paths`

- **DD filename:** `API_002_GET_catalog_learning_paths.xlsx`
- **Module:** 01. Public Catalog
- **Authentication/Authorization:** Public/Optional Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-02
- **Purpose:** Tìm kiếm, lọc và phân trang lộ trình đã công khai.
- **Input baseline:** Query: q?, goal?, difficulty?, duration_min?, duration_max?, sort=admin_order|relevance|updated_at, page, page_size
- **Output baseline:** data[]: id, slug, name, short_description, outcomes[], target_users[], course_count, estimated_duration, difficulty, image_url, labels[], publication_status; learner_state?; meta pagination
- **Business rules:** PC-01, PC-05, PC-06

### API 003 — `GET /api/v1/catalog/learning-paths/{slug}`

- **DD filename:** `API_003_GET_catalog_learning_paths_by_slug.xlsx`
- **Module:** 01. Public Catalog
- **Authentication/Authorization:** Public/Optional Learner
- **Basis:** SUY DẪN
- **Source:** BD-01
- **Purpose:** Xem chi tiết lộ trình công khai và hành động phù hợp trạng thái người xem.
- **Input baseline:** Path: slug
- **Output baseline:** data: path profile, prerequisites[], outcomes[], courses[{required, order}], duration, completion_conditions[], community_summary?, learner_state?, primary_action
- **Business rules:** PC-01, PC-05, PC-06

### API 004 — `GET /api/v1/catalog/courses`

- **DD filename:** `API_004_GET_catalog_courses.xlsx`
- **Module:** 01. Public Catalog
- **Authentication/Authorization:** Public/Optional Learner
- **Basis:** SUY DẪN
- **Source:** BD-01
- **Purpose:** Tìm kiếm, lọc danh sách khóa học công khai.
- **Input baseline:** Query: q?, technology?, topic?, level?, path_id?, duration_min?, duration_max?, sort?, page, page_size
- **Output baseline:** data[]: id, slug, name, short_description, level, duration, chapter_count, lesson_count, assignment_count, sample_lesson_count, related_paths[], learner_access?; meta
- **Business rules:** PC-01

### API 005 — `GET /api/v1/catalog/courses/{slug}`

- **DD filename:** `API_005_GET_catalog_courses_by_slug.xlsx`
- **Module:** 01. Public Catalog
- **Authentication/Authorization:** Public/Optional Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-02
- **Purpose:** Xem thông tin khóa học, curriculum công khai và lộ trình sử dụng khóa học.
- **Input baseline:** Path: slug
- **Output baseline:** data: course details, goals[], prerequisites[], skills[], public_curriculum[], counts, sample_lessons[], related_paths[], access_state, primary_action
- **Business rules:** PC-01, CRS-02

### API 006 — `GET /api/v1/catalog/sample-lessons/{lesson_id}`

- **DD filename:** `API_006_GET_catalog_sample_lessons_by_lesson_id.xlsx`
- **Module:** 01. Public Catalog
- **Authentication/Authorization:** Public
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-02
- **Purpose:** Xem phần bài học mẫu được Admin cho phép công khai; không tạo tiến độ.
- **Input baseline:** Path: lesson_id
- **Output baseline:** data: lesson_id, title, objectives[], preview_content, public_resources[], course_summary, path_summary?
- **Business rules:** PC-02, PC-03, CRS-02

## 5. Trọng tâm thiết kế của batch

- Phân biệt Guest và Learner đăng nhập tùy chọn; không làm lộ learner state khi không có token.
- Chỉ trả nội dung PUBLISHED và đúng phạm vi public.
- Danh sách phải thống nhất search, filter, sort, pagination và empty result.
- Bài học mẫu không được tạo enrollment hoặc progress.

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
