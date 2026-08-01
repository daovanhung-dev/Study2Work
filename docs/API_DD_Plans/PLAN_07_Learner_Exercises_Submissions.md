# Plan 07 — Learner Exercises and Submissions

## 1. Mục tiêu

Hoàn thành **9 file Detail Design API** theo `Detail_Design_API_Template_Optimized.xlsx` cho phạm vi API từ STT **48–56**.

- API trực tiếp từ tài liệu/sequence: **2**.
- API suy dẫn từ BD: **7**.
- Module: 06. Bài tập và đánh giá (9).
- Lý do quy mô batch: 9 API learner tạo thành một submission lifecycle hoàn chỉnh: xem đề, draft, nộp, xem kết quả và nộp lại.

> API có `Basis = SUY DẪN` chỉ được chốt ở trạng thái **Draft — Needs Confirmation** cho đến khi endpoint, contract và business rule được xác nhận. Không biến suy luận thành dữ kiện.

## 2. Điều kiện tiên quyết

- Plan 06.
- Exercise state machine.
- Progress recalculation.
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
- `BD/07. Study2Work_Study_BasicDesign_Tien_Do_Hoan_Thanh.md`

## 4. Danh sách API phải hoàn thành

### API 048 — `GET /api/v1/exercises`

- **DD filename:** `API_048_GET_exercises.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Lấy danh sách bài tập theo khóa/chương/bài học và trạng thái cá nhân.
- **Input baseline:** Query: course_id?, chapter_id?, lesson_id?, status?, required?, due_before?, page, page_size
- **Output baseline:** data[]: assignment_id, title, scope, required, due_at?, submission_status, latest_result, allowed_actions[]; meta
- **Business rules:** EX-01, EX-02

### API 049 — `GET /api/v1/exercises/{assignment_id}`

- **DD filename:** `API_049_GET_exercises_by_assignment_id.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-07
- **Purpose:** Xem đề bài, tiêu chí, hint, tài liệu, hình thức nộp và trạng thái bài nộp.
- **Input baseline:** Path: assignment_id
- **Output baseline:** data: assignment definition, expected_input_output?, completion_criteria[], hints[], resources[], submission_methods[], due_at?, rubric_summary?, access_state, latest_submission
- **Business rules:** EX-01

### API 050 — `GET /api/v1/exercises/{assignment_id}/draft`

- **DD filename:** `API_050_GET_exercises_by_assignment_id_draft.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Lấy bản nháp bài làm hiện tại.
- **Input baseline:** Path: assignment_id
- **Output baseline:** data: draft_id?, answer_payload, attachments[], links[], notes?, updated_at?, status=NOT_STARTED|DRAFT
- **Business rules:** EX-03

### API 051 — `PUT /api/v1/exercises/{assignment_id}/draft`

- **DD filename:** `API_051_PUT_exercises_by_assignment_id_draft.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Tạo/cập nhật bản nháp; chưa tính là đã nộp hoặc hoàn thành.
- **Input baseline:** Path: assignment_id; Body: answers?, text?, links[]?, file_ids[]?, progress_notes?
- **Output baseline:** data: draft_id, status=DRAFT, saved_at, validation_warnings[]
- **Business rules:** EX-03

### API 052 — `POST /api/v1/exercises/{assignment_id}/submissions`

- **DD filename:** `API_052_POST_exercises_by_assignment_id_submissions.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** TRỰC TIẾP
- **Source:** SEQ-07
- **Purpose:** Nộp bài lần đầu và chuyển sang chấm tự động hoặc chờ review.
- **Input baseline:** Path: assignment_id; Body: draft_id? hoặc answers/text/links/file_ids, confirm_submit=true
- **Output baseline:** data: submission_id, attempt_no, submitted_at, status=SUBMITTED|UNDER_REVIEW|PASSED|FAILED, auto_score?, validation_results[]
- **Business rules:** EX-01, EX-04, EX-06

### API 053 — `GET /api/v1/exercises/{assignment_id}/submissions/latest`

- **DD filename:** `API_053_GET_exercises_by_assignment_id_submissions_latest.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Lấy bài nộp và kết quả đánh giá mới nhất.
- **Input baseline:** Path: assignment_id
- **Output baseline:** data: submission_id, attempt_no, payload_summary, status, score?, result?, feedback, errors_to_fix[], resubmit_allowed, resubmit_deadline?
- **Business rules:** EX-06, EX-08

### API 054 — `GET /api/v1/exercises/{assignment_id}/submissions`

- **DD filename:** `API_054_GET_exercises_by_assignment_id_submissions.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Lấy lịch sử các lần nộp bài.
- **Input baseline:** Path: assignment_id; Query: page, page_size
- **Output baseline:** data[]: submission_id, attempt_no, submitted_at, status, score?, result, feedback_summary; meta
- **Business rules:** EX-07

### API 055 — `GET /api/v1/submissions/{submission_id}`

- **DD filename:** `API_055_GET_submissions_by_submission_id.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner/Reviewer
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Lấy chi tiết một lần nộp và phản hồi tương ứng.
- **Input baseline:** Path: submission_id
- **Output baseline:** data: assignment_summary, learner_submission, attachments, grading, rubric_results[], feedback, audit_summary?
- **Business rules:** EX-08

### API 056 — `POST /api/v1/exercises/{assignment_id}/resubmissions`

- **DD filename:** `API_056_POST_exercises_by_assignment_id_resubmissions.xlsx`
- **Module:** 06. Bài tập và đánh giá
- **Authentication/Authorization:** Learner
- **Basis:** SUY DẪN
- **Source:** BD-06
- **Purpose:** Nộp lại khi NEEDS_REVISION hoặc được mở quyền.
- **Input baseline:** Path: assignment_id; Body: based_on_submission_id, answers/text/links/file_ids, confirm_submit=true
- **Output baseline:** data: submission_id, attempt_no, status, submitted_at, previous_attempt_id
- **Business rules:** EX-07

## 5. Trọng tâm thiết kế của batch

- Draft khác submission; draft không tạo completion hoặc attempt.
- Submission phải idempotent hoặc có cơ chế chống gửi trùng.
- Attempt history bất biến; resubmission chỉ hợp lệ theo trạng thái/quyền.
- Mô tả auto-grading/manual review, rubric, score, feedback và async processing nếu có.

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
