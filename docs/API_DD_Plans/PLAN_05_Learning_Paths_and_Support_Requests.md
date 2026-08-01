# Plan 05 — Learning Paths and Learner Support Requests

## 1. Mục tiêu

Hoàn thành **11 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **28–38**.

- API trực tiếp từ tài liệu/sequence: **2**.
- API suy dẫn từ BD: **9**.
- Module: 04. Lộ trình học (11).
- Lý do quy mô batch: 11 API cùng xoay quanh lifecycle tham gia lộ trình; gom support request để giữ trọn quy tắc đổi/reset/hủy và một ACTIVE path.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 04.
- Course structure.
- Support request state machine.
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
- `BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md`
- `BD/diagram/SEQUENCE/05. Study2Work_Study_SEQ_Kich_Hoat_Lo_Trinh.md`
- `BD/diagram/AC/05. Study2Work_Study_AC_Lo_Trinh_Hoc.md`
- `BD/11. Study2Work_Study_BasicDesign_Admin_Quan_Ly_Hoc_Vien_Ho_Tro_Ngoai_Le.md`
- `BD/diagram/SEQUENCE/12. Study2Work_Study_SEQ_Admin_Ho_Tro_Ngoai_Le.md`
- `BD/diagram/AC/12. Study2Work_Study_AC_Admin_Hoc_Vien_Ho_Tro_Ngoai_Le.md`

## 4. Danh sách API phải hoàn thành

### API 028 — `GET /api/v1/learning-paths`

- **DD filename:** `API_028_GET_learning_paths.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Lấy danh sách lộ trình đã xuất bản kèm trạng thái cá nhân.
- **Input baseline:** Query: q?, goal?, difficulty?, status?, page, page_size, sort?
- **Output baseline:** data[]: public path fields, learner_enrollment_state, progress_percent, activation_allowed, blocking_reason?; meta
- **Business rules:** LP-01, LP-07

### API 029 — `GET /api/v1/learning-paths/{path_id}`

- **DD filename:** `API_029_GET_learning_paths_by_path_id.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Xem cấu trúc lộ trình, trạng thái từng khóa và điều kiện còn thiếu.
- **Input baseline:** Path: path_id
- **Output baseline:** data: path details, courses[{order, required, unlock_state, learner_state, progress}], completion_conditions[], missing_conditions[], community_groups[], activation_state
- **Business rules:** LP-02, LP-05

### API 030 — `POST /api/v1/learning-paths/{path_id}/activation-preview`

- **DD filename:** `API_030_POST_learning_paths_by_path_id_activation_preview.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Kiểm tra điều kiện và hiển thị xác nhận trước khi kích hoạt.
- **Input baseline:** Path: path_id
- **Output baseline:** data: eligible, checks[{code, passed, message}], path_summary, course_order, duration, completion_conditions, community_summary, confirmation_token?
- **Business rules:** LP-02, LP-03, LP-07

### API 031 — `POST /api/v1/learning-paths/{path_id}/activate`

- **DD filename:** `API_031_POST_learning_paths_by_path_id_activate.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Ready-to-learn Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-05
- **Purpose:** Kích hoạt lộ trình duy nhất và mở nội dung đầu tiên.
- **Input baseline:** Path: path_id; Body: accepted_rules=true, confirmation_token?
- **Output baseline:** data: enrollment_id, status=ACTIVE, activated_at, first_unlocked_course, dashboard_snapshot, next_route
- **Business rules:** LP-02, LP-03

### API 032 — `GET /api/v1/me/learning-paths/active`

- **DD filename:** `API_032_GET_me_learning_paths_active.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Lấy lộ trình ACTIVE hiện tại và hành động tiếp theo.
- **Input baseline:** Không có
- **Output baseline:** data: enrollment_id, path, progress_percent, courses[], missing_conditions[], continue_learning, community_groups[]
- **Business rules:** LP-02

### API 033 — `GET /api/v1/me/learning-paths/history`

- **DD filename:** `API_033_GET_me_learning_paths_history.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Lấy lịch sử các lộ trình đã tham gia, kể cả hoàn thành/hủy/reset.
- **Input baseline:** Query: status?, page, page_size
- **Output baseline:** data[]: enrollment_id, path, status, activated_at, completed_at?, cancelled_at?, progress_snapshot; meta
- **Business rules:** LP-04

### API 034 — `GET /api/v1/me/learning-paths/{enrollment_id}/summary`

- **DD filename:** `API_034_GET_me_learning_paths_by_enrollment_id_summary.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Xem tổng kết lộ trình hoặc dữ liệu ôn tập lịch sử.
- **Input baseline:** Path: enrollment_id
- **Output baseline:** data: status, completion_time, completed_courses[], skills[], achievement_summary, review_access, next_path_suggestions[]
- **Business rules:** LP-03, mục 4.5-4.6

### API 035 — `GET /api/v1/me/learning-paths/next-recommendations`

- **DD filename:** `API_035_GET_me_learning_paths_next_recommendations.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Gợi ý lộ trình tiếp theo sau khi hoàn thành lộ trình hiện tại.
- **Input baseline:** Không có
- **Output baseline:** data[]: path_id, reason[], prerequisites_met, estimated_duration, activation_allowed
- **Business rules:** LP-03

### API 036 — `POST /api/v1/support-requests`

- **DD filename:** `API_036_POST_support_requests.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-12
- **Purpose:** Gửi yêu cầu đổi/reset/hủy lộ trình theo quy trình ngoại lệ.
- **Input baseline:** Body: request_type=CHANGE|RESET|CANCEL, current_enrollment_id, target_path_id?, reason, note?
- **Output baseline:** data: request_id, status=OPEN, submitted_at, expected_next_step
- **Business rules:** LP-04, ONB-08

### API 037 — `GET /api/v1/support-requests`

- **DD filename:** `API_037_GET_support_requests.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Xem danh sách yêu cầu hỗ trợ lộ trình của bản thân.
- **Input baseline:** Query: status?, page, page_size
- **Output baseline:** data[]: request_id, type, current_path, target_path?, status, submitted_at, decision_summary?; meta
- **Business rules:** LP-04

### API 038 — `GET /api/v1/support-requests/{request_id}`

- **DD filename:** `API_038_GET_support_requests_by_request_id.xlsx`
- **Module:** 04. Lộ trình học
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-04
- **Purpose:** Xem chi tiết và kết quả xử lý yêu cầu lộ trình.
- **Input baseline:** Path: request_id
- **Output baseline:** data: request fields, status, admin_response?, decision_at?, resulting_path_state?
- **Business rules:** ADM-LRN-07

## 5. Trọng tâm thiết kế của batch

- Không cho phép đồng thời hai learning path enrollment ở trạng thái ACTIVE.
- Activation preview và activate phải dùng cùng rule engine để tránh kết quả lệch.
- Mô tả unlock course, completion, history và next recommendation.
- Đổi/reset/hủy chỉ đi qua support request; learner không sửa trực tiếp enrollment/progress.

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

- **11 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 11/11 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
