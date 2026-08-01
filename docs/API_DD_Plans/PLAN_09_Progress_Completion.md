# Plan 09 — Progress and Completion

## 1. Mục tiêu

Hoàn thành **9 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **61–69**.

- API trực tiếp từ tài liệu/sequence: **1**.
- API suy dẫn từ BD: **8**.
- Module: 07. Tiến độ và hoàn thành (9).
- Lý do quy mô batch: 9 API dùng chung progress hierarchy và completion engine; cần làm cùng batch để tránh công thức roll-up khác nhau.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 05.
- Plan 06.
- Plan 07.
- Completion rules.
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
- `BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md`
- `BD/diagram/SEQUENCE/06. Study2Work_Study_SEQ_Hoc_Bai_Cap_Nhat_Tien_Do.md`
- `BD/diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md`
- `BD/diagram/AC/08. Study2Work_Study_AC_Tien_Do_Hoan_Thanh.md`

## 4. Danh sách API phải hoàn thành

### API 061 — `GET /api/v1/me/dashboard`

- **DD filename:** `API_061_GET_me_dashboard.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy dashboard ưu tiên hành động học tiếp theo.
- **Input baseline:** Không có
- **Output baseline:** data: active_path, path_progress, active_course, continue_item, pending_assignments[], recent_completions[], unread_notifications, community_groups[], inactivity_prompt?
- **Business rules:** PRG-01

### API 062 — `GET /api/v1/me/continue-learning`

- **DD filename:** `API_062_GET_me_continue_learning.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Xác định nội dung học tiếp theo trên toàn lộ trình.
- **Input baseline:** Không có
- **Output baseline:** data: item_type, item_id, title, course_id, path_id, reason=LAST_ACTIVE|FIRST_REQUIRED_INCOMPLETE|REQUIRED_ASSIGNMENT|NEXT_UNLOCKED, route
- **Business rules:** PRG mục 4.2

### API 063 — `GET /api/v1/me/progress/learning-paths/{path_id}`

- **DD filename:** `API_063_GET_me_progress_learning_paths_by_path_id.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy tiến độ chi tiết lộ trình và điều kiện còn thiếu.
- **Input baseline:** Path: path_id
- **Output baseline:** data: percent, status, required_courses_completed, required_courses_total, courses[], missing_conditions[], completed_at?
- **Business rules:** PRG-01, PRG-05

### API 064 — `GET /api/v1/me/progress/courses/{course_id}`

- **DD filename:** `API_064_GET_me_progress_courses_by_course_id.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy tiến độ khóa học theo chương, bài học và đánh giá.
- **Input baseline:** Path: course_id
- **Output baseline:** data: percent, status, chapters[], required_items_summary, score_summary?, final_project_status?, completed_at?
- **Business rules:** PRG-01, PRG-05

### API 065 — `GET /api/v1/me/progress/chapters/{chapter_id}`

- **DD filename:** `API_065_GET_me_progress_chapters_by_chapter_id.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy tiến độ chương và trạng thái từng nội dung.
- **Input baseline:** Path: chapter_id
- **Output baseline:** data: percent, status, lessons[], assignments[], missing_conditions[], next_unlock?
- **Business rules:** PRG-01

### API 066 — `GET /api/v1/me/progress/lessons/{lesson_id}`

- **DD filename:** `API_066_GET_me_progress_lessons_by_lesson_id.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy các điều kiện hoàn thành bài học và trạng thái từng điều kiện.
- **Input baseline:** Path: lesson_id
- **Output baseline:** data: status, percent, video_requirement, video_progress, manual_confirmation, required_resources[], self_check, assignments[], missing_conditions[]
- **Business rules:** PRG mục 4.3

### API 067 — `PATCH /api/v1/lessons/{lesson_id}/progress`

- **DD filename:** `API_067_PATCH_lessons_by_lesson_id_progress.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-06
- **Purpose:** Ghi sự kiện xem video, đọc tài liệu hoặc xác nhận hoàn thành; tái tính tiến độ bài/chương/khóa/lộ trình.
- **Input baseline:** Path: lesson_id; Body: event_type=VIDEO_PROGRESS|RESOURCE_READ|MANUAL_COMPLETE|SELF_CHECK, position_seconds?, duration_seconds?, resource_id?, confirmed?, answers?, occurred_at
- **Output baseline:** data: lesson_progress, met_conditions[], missing_conditions[], chapter_update, course_update, path_update, next_item
- **Business rules:** SEQ-06, CRS-04, PRG-04, PRG-05

### API 068 — `GET /api/v1/me/learning-history`

- **DD filename:** `API_068_GET_me_learning_history.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy lịch sử lộ trình, khóa học, bài tập và nội dung gần đây.
- **Input baseline:** Query: type?, from?, to?, page, page_size
- **Output baseline:** data[]: event_type, entity, status/result, occurred_at, metadata; meta
- **Business rules:** PRG mục 4.7

### API 069 — `GET /api/v1/me/completion-summaries/{entity_type}/{entity_id}`

- **DD filename:** `API_069_GET_me_completion_summaries_by_entity_type_by_entity_id.xlsx`
- **Module:** 07. Tiến độ và hoàn thành
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-07
- **Purpose:** Lấy tổng kết khi hoàn thành khóa học hoặc lộ trình.
- **Input baseline:** Path: entity_type=course|learning-path, entity_id
- **Output baseline:** data: completion_time, completed_items, scores?, skills[], achievements[], next_recommendations[]
- **Business rules:** PRG mục 4.5-4.6

## 5. Trọng tâm thiết kế của batch

- Sự kiện progress phải idempotent và có quy tắc merge/update rõ.
- Roll-up lesson → chapter → course → learning path phải dùng cùng completion rules.
- Nội dung optional không được chặn completion.
- Khi hoàn thành phải mô tả unlock, notification, summary và transaction/outbox.

### Xung đột/rủi ro riêng của plan

- **BLOCKER:** SEQ-08 khai báo GET /api/v1/progress/summary và POST /api/v1/progress/recalculate nhưng catalog 157 API không chứa hai endpoint này.
- **BLOCKER:** Phải quyết định chúng là public API, internal use case hay được thay thế bởi nhóm /me/progress và completion-summaries trước khi chốt DD.

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
