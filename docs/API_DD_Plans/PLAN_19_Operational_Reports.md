# Plan 19 — Operational Reports

## 1. Mục tiêu

Hoàn thành **8 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **142–149**.

- API trực tiếp từ tài liệu/sequence: **2**.
- API suy dẫn từ BD: **6**.
- Module: 12. Báo cáo vận hành (8).
- Lý do quy mô batch: 8 read-only API dùng chung metric definitions, date filter, aggregation và performance strategy.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Metric dictionary.
- Event/audit data.
- Reporting timezone.
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
- `BD/12. Study2Work_Study_BasicDesign_Admin_Bao_Cao_Van_Hanh.md`
- `BD/diagram/SEQUENCE/13. Study2Work_Study_SEQ_Bao_Cao_Van_Hanh.md`
- `BD/diagram/AC/13. Study2Work_Study_AC_Admin_Bao_Cao_Van_Hanh.md`
- `BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md`
- `BD/09. Study2Work_Study_BasicDesign_Thong_Bao_Nghiep_Vu.md`

## 4. Danh sách API phải hoàn thành

### API 142 — `GET /api/v1/admin/reports/overview`

- **DD filename:** `API_142_GET_admin_reports_overview.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Super Admin
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-13
- **Purpose:** Lấy dashboard tổng quan tài khoản, onboarding, học tập, bài tập và cộng đồng.
- **Input baseline:** Query: from, to, path_id?, course_id?, level?, learner_group?, account_status?, path_status?, granularity=day|week|month
- **Output baseline:** data: new_accounts, verification_rate, onboarding_completion_rate, activated_learners, first_course_start_rate, path_completion_rate, high_dropout_lessons[], high_failure_assignments[], path_change_request_count, zalo_link_open_count, trends[]
- **Business rules:** RPT-01, RPT-02

### API 143 — `GET /api/v1/admin/reports/registrations`

- **DD filename:** `API_143_GET_admin_reports_registrations.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Learner Support
- **Basis:** SUY DẪN
- **Source:** BD-12
- **Purpose:** Báo cáo đăng ký và xác thực.
- **Input baseline:** Query: from, to, granularity
- **Output baseline:** data: new_registrations_series, verification_success_rate, pending_verification_count, avg_verification_time, pre_verification_dropout_rate
- **Business rules:** RPT-01

### API 144 — `GET /api/v1/admin/reports/onboarding`

- **DD filename:** `API_144_GET_admin_reports_onboarding.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Learner Support
- **Basis:** SUY DẪN
- **Source:** BD-12
- **Purpose:** Báo cáo bắt đầu/hoàn thành onboarding và điểm rơi theo bước.
- **Input baseline:** Query: from, to, path_id?, course_id?, level?, learner_group?, account_status?, path_status?, granularity=day|week|month
- **Output baseline:** data: started_rate, completed_rate, funnel_by_step[], popular_goals[], programming_levels[], recommendation_selection_rate
- **Business rules:** RPT-01

### API 145 — `GET /api/v1/admin/reports/learning-paths`

- **DD filename:** `API_145_GET_admin_reports_learning_paths.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Content Admin
- **Basis:** SUY DẪN
- **Source:** BD-12
- **Purpose:** Báo cáo kích hoạt, đang học, hoàn thành, thời gian và đổi/reset theo lộ trình.
- **Input baseline:** Query: from, to, path_id?, course_id?, level?, learner_group?, account_status?, path_status?, granularity=day|week|month
- **Output baseline:** data[]: path_id, activated_count, active_count, completed_count, completion_rate, avg_completion_time, dropout_courses[], change_reset_request_count
- **Business rules:** RPT-01, RPT-06

### API 146 — `GET /api/v1/admin/reports/courses`

- **DD filename:** `API_146_GET_admin_reports_courses.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Content Admin
- **Basis:** SUY DẪN
- **Source:** BD-12
- **Purpose:** Báo cáo bắt đầu/hoàn thành khóa và điểm nghẽn bài học.
- **Input baseline:** Query: from, to, path_id?, course_id?, level?, learner_group?, account_status?, path_status?, granularity=day|week|month
- **Output baseline:** data[]: course metrics, start_rate, completion_rate, dropout_lessons[], issue_count_by_lesson, avg_learning_time?, most_revisited_content[]
- **Business rules:** RPT-04, RPT-06

### API 147 — `GET /api/v1/admin/reports/assignments`

- **DD filename:** `API_147_GET_admin_reports_assignments.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Content Admin
- **Basis:** SUY DẪN
- **Source:** BD-12
- **Purpose:** Báo cáo nộp bài, kết quả, thời gian nộp và backlog review.
- **Input baseline:** Query: from, to, path_id?, course_id?, level?, learner_group?, account_status?, path_status?, granularity=day|week|month
- **Output baseline:** data[]: assignment_id, submission_count, pass_rate, fail_rate, revision_rate, avg_open_to_submit_time, under_review_count, avg_review_wait_time
- **Business rules:** RPT-04

### API 148 — `GET /api/v1/admin/reports/community`

- **DD filename:** `API_148_GET_admin_reports_community.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin/Moderator
- **Basis:** SUY DẪN
- **Source:** BD-12
- **Purpose:** Báo cáo lượt mở link và vấn đề nhóm cộng đồng.
- **Input baseline:** Query: from, to, path_id?, course_id?, level?, learner_group?, account_status?, path_status?, granularity=day|week|month
- **Output baseline:** data[]: group_id, opens_count, path_or_course_breakdown, report_count, broken_link_count, spam_count, status
- **Business rules:** RPT-03

### API 149 — `GET /api/v1/admin/reports/alerts`

- **DD filename:** `API_149_GET_admin_reports_alerts.xlsx`
- **Module:** 12. Báo cáo vận hành
- **Authentication/Authorization:** Admin theo phạm vi
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-13
- **Purpose:** Lấy cảnh báo vận hành theo ngưỡng đã cấu hình.
- **Input baseline:** Query: severity?, category?, status?, from?, to?, page, page_size
- **Output baseline:** data[]: alert_id, category, metric, observed_value, threshold, severity, scope, detected_at, status, recommended_action; meta
- **Business rules:** RPT mục 5.7

## 5. Trọng tâm thiết kế của batch

- Định nghĩa metric, numerator/denominator, event time và timezone rõ ràng.
- Filter date/path/course phải nhất quán giữa overview và drill-down.
- Không trộn current state với event history nếu chưa định nghĩa.
- Mô tả index/materialized view/cache và giới hạn dữ liệu để tránh full scan.

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
