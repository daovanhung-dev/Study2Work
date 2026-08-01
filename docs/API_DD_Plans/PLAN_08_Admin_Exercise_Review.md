# Plan 08 — Admin Exercise Review

## 1. Mục tiêu

Hoàn thành **4 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **57–60**.

- API trực tiếp từ tài liệu/sequence: **1**.
- API suy dẫn từ BD: **3**.
- Module: 06. Bài tập và đánh giá (4).
- Lý do quy mô batch: 4 API ít về số lượng nhưng độ rủi ro cao do liên quan chấm điểm, sửa trạng thái và mở lại quyền nộp.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 07.
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
- `BD/06. Study2Work_Study_BasicDesign_Bai_Tap_Danh_Gia.md`
- `BD/diagram/SEQUENCE/07. Study2Work_Study_SEQ_Bai_Tap_Nop_Cham_Nop_Lai.md`
- `BD/diagram/AC/07. Study2Work_Study_AC_Bai_Tap_Danh_Gia.md`
- `BD/13. Study2Work_Study_BasicDesign_Vai_Tro_Phan_Quyen_Audit_Log.md`

## 4. Danh sách API phải hoàn thành

### API 057 — `GET /api/v1/admin/exercise-submissions`

- **DD filename:** `API_057_GET_admin_exercise_submissions.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Admin/Mentor
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Lấy hàng đợi bài cần chấm và lọc theo trạng thái.
- **Input baseline:** Query: status=UNDER_REVIEW?, assignment_id?, course_id?, learner_id?, due_before?, sort=oldest|newest, page, page_size
- **Output baseline:** data[]: submission summary, waiting_time, rubric, learner_summary; meta
- **Business rules:** Module 5.5

### API 058 — `GET /api/v1/admin/exercise-submissions/{submission_id}`

- **DD filename:** `API_058_GET_admin_exercise_submissions_by_submission_id.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Admin/Mentor
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Xem đầy đủ bài nộp, rubric và lịch sử chấm.
- **Input baseline:** Path: submission_id
- **Output baseline:** data: assignment, learner, submission_payload, attachments, rubric, previous_attempts[], prior_reviews[]
- **Business rules:** Module 5.5

### API 059 — `PATCH /api/v1/admin/exercise-submissions/{submission_id}/review`

- **DD filename:** `API_059_PATCH_admin_exercise_submissions_by_submission_id_review.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Admin/Mentor
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-07
- **Purpose:** Chấm bài thủ công, ghi điểm, kết quả và phản hồi.
- **Input baseline:** Path: submission_id; Body: result=PASSED|NEEDS_REVISION|FAILED, score?, rubric_scores[]?, feedback, errors_to_fix[]?, resubmit_deadline?
- **Output baseline:** data: review_id, final_status, score?, reviewed_by, reviewed_at, progress_effect, notification_created
- **Business rules:** EX-06, EX-08

### API 060 — `POST /api/v1/admin/exercise-submissions/{submission_id}/reopen`

- **DD filename:** `API_060_POST_admin_exercise_submissions_by_submission_id_reopen.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Admin có quyền
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Mở lại quyền nộp bài trong trường hợp ngoại lệ.
- **Input baseline:** Path: submission_id; Body: reason, allowed_until?
- **Output baseline:** data: reopened=true, resubmit_allowed, allowed_until?, audit_id, learner_notified
- **Business rules:** EX-07, RBAC-05

## 5. Trọng tâm thiết kế của batch

- Reviewer scope, permission và phân tách Mentor/Admin.
- Optimistic locking hoặc version check khi nhiều reviewer thao tác cùng submission.
- Review phải ghi rubric, score, result, feedback và audit trail.
- Reopen phải có lý do, giới hạn và không xóa lịch sử attempt.

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

- **4 workbook `.xlsx`**, đúng tên trong mục 4.
- `PLAN_RESULT.md` của batch: trạng thái từng API, nguồn đã dùng, assumption, conflict, reviewer note và lỗi còn mở.
- `BUSINESS_CODE_DELTA.md` nếu phát sinh business code mới hoặc xung đột ý nghĩa.
- `OPEN_QUESTIONS.md` chỉ chứa câu hỏi có ảnh hưởng contract/nghiệp vụ/bảo mật/dữ liệu; không đưa câu hỏi có thể tự giải quyết từ nguồn.

## 8. Definition of Done

- [ ] Đủ 4/4 API, không thiếu STT và không trùng endpoint.
- [ ] Overview khớp method, endpoint, auth, module và source.
- [ ] Mọi request field được sử dụng hoặc ghi rõ không sử dụng.
- [ ] Mọi response field có source/mapping và null/empty rule.
- [ ] Flow Data Mapping đúng execution order và đủ query params/result handling.
- [ ] Transaction, locking, idempotency, concurrency và rollback được mô tả khi áp dụng.
- [ ] Mọi lỗi trong flow xuất hiện trong sheet Error và có Data Mapping Ref.
- [ ] DB table sheets chỉ có cho bảng bị thay đổi.
- [ ] Không còn placeholder `<...>` chưa được giải thích.
- [ ] API suy dẫn được gắn cờ và không tự chuyển thành Final.
