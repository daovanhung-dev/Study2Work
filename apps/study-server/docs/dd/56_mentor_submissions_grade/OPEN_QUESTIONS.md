---
title: "Open Questions — Study API #56 Lưu điểm"
order: 10
dd_id: "56"
api_name: "Lưu điểm bài làm Mentor"
source_sheet: "Open Questions"
status: "Draft — Needs Confirmation"
---

# Open Questions — Study API #56 Lưu điểm

**Endpoint:** POST /api/v1/mentor/submissions/{submission_id}/grade

Các câu hỏi dưới đây ngăn chốt implementation contract hoặc persistence. API catalog và AC-23 vẫn được giữ nguyên trong DD cho tới khi owner cập nhật nguồn chính thức.

## Q-56-01 — Wire key và định dạng rubric items

**Evidence**

- Catalog row #56 ghi body descriptor rubric items:string!.
- Descriptor có khoảng trắng và không nêu JSON property spelling thay thế.
- Không có item schema, serialization, escaping hay validation rule.

**Cần xác nhận**

1. JSON property thực tế có tên chính xác là gì?
2. Chuỗi chứa JSON, text hiển thị, hay định dạng có version?
3. Các item và điểm thành phần có field, ID, thứ tự và validation rule nào?

**Ảnh hưởng:** Request validation, client compatibility và cách dữ liệu có thể được kiểm tra.

## Q-56-02 — Nơi lưu rubric items

**Evidence**

- Legacy assignment_submissions có score, feedback, status; không có cột hoặc bảng rubric detail.
- V1-PILOT rubrics và rubric_criteria thuộc assessment UUID; không có quan hệ đã duyệt tới legacy BIGINT assignments/submissions.
- AC-23 chỉ ghi “UPDATE grade + status = GRADED”; không nêu rubric table hoặc snapshot.

**Cần xác nhận**

1. Rubric items có phải được lưu không?
2. Nếu có, bảng/khóa/column nào là canonical, và rubric snapshot hay rubric definition được lưu?
3. Rubric ghi cùng transaction với score/status hay qua một endpoint khác?

**Ảnh hưởng:** Không thể hoàn thành persistence cho field bắt buộc nếu chưa có target/schema.

## Q-56-03 — Score bounds, scale và chuyển kiểu

**Evidence**

- Request contract yêu cầu score:int32.
- Submission response dùng score?:decimal-string.
- Candidate assignments.max_score là NUMERIC(6,2); candidate submissions.score cũng là NUMERIC(6,2).
- Catalog/AC-23 không định nghĩa thang điểm hoặc giới hạn.

**Cần xác nhận**

1. Score có phải >= 0 và <= max_score không?
2. Có cho phép điểm thập phân/rubric tổng lẻ không, trong khi request hiện là int32?
3. Quy tắc chuyển integer sang decimal và decimal-string là gì?
4. Nếu max_score khác 10 hoặc thay đổi sau khi tạo assignment, so sánh theo giá trị nào?

**Ảnh hưởng:** Validation 422, dữ liệu DB, response formatting và tương thích contract.

## Q-56-04 — Mentor identity và phạm vi quyền

**Evidence**

- Catalog yêu cầu role Mentor; AC-23 yêu cầu Mentor có quyền chấm submission của course.
- Shared Study guard hiện hành chỉ hỗ trợ Student.
- Legacy courses.mentor_id là direct-owner candidate; không có bằng chứng rằng Mentor được phân công cũng được phép chấm.
- JWT subject-to-numeric Study user mapping cho Mentor chưa được source xác nhận.

**Cần xác nhận**

1. Claim nào định danh Mentor và map tới users.id thế nào?
2. Quyền chỉ dành cho course.mentor_id hay cả Mentor được phân công?
3. Resource tồn tại nhưng ngoài quyền trả 403 hay được mask thành 404?

**Ảnh hưởng:** Guard, query predicate và disclosure semantics.

## Q-56-05 — Trạng thái đủ điều kiện và chấm lại

**Evidence**

- AC-17 đặt trạng thái nhận bài SUBMITTED; AC-23 đặt target GRADED.
- Catalog không có 409.
- Không có rule về trạng thái nguồn, số lần chấm, resubmit hoặc audit/history.

**Cần xác nhận**

1. Chỉ SUBMITTED mới được chấm hay có thể chấm lại GRADED?
2. Resubmission sau GRADED có được phép và score/status xử lý ra sao?
3. Có cần lịch sử chấm, người chấm hoặc updated_at/audit không?
4. Nếu trạng thái không hợp lệ, contract có cần business code/error branch mới không?

**Ảnh hưởng:** WHERE/precondition, repeat-call semantics, concurrency and audit schema.

## Q-56-06 — Response files và asset resolver

**Evidence**

- Submission schema yêu cầu files:UploadAsset[].
- Legacy assignment_submissions chỉ có một file_url.
- API #55 đã ghi unresolved asset ID/name/content_type/size/status source.

**Cần xác nhận**

1. Asset nào cung cấp UploadAsset[] và quan hệ với submission?
2. Một file_url có được chuyển thành UploadAsset hay cần asset table/service?
3. URL là public hay signed, và quyền đọc được áp dụng thế nào?

**Ảnh hưởng:** API #56 không thể dựng đủ Submission contract từ legacy row đơn lẻ.

## Q-56-07 — Score update, feedback và transaction

**Evidence**

- AC-23 gọi #56 grade/status rồi #57 feedback.
- Candidate legacy row có feedback nullable.
- Current DB query helper không tự commit; không có transaction rule của API #56.

**Cần xác nhận**

1. #56 có giữ nguyên feedback hiện có hay grading mới xóa feedback cũ?
2. Quy tắc Student nhận kết quả áp dụng sau #56 hay sau #57?
3. Authorization check, UPDATE và response read cần transaction/locking/isolation nào?
4. Behavior khi submission bị xóa giữa check và UPDATE là gì?

**Ảnh hưởng:** Mutation isolation, response disclosure và retry/concurrency.

## Q-56-08 — Error envelope và middleware contract mapping

**Evidence**

- API Guidelines requires error data=null and safe field details under meta.fieldErrors.
- Current apps/study-server/app/core/responses.py serializes data as {} when error_response(data=None) is used.
- Current apps/study-server/app/core/middleware.py only emits DESIGN_VALIDATION_ERROR and DESIGN_INTERNAL_ERROR for paths in DESIGN_CONTRACT_PATHS; API #56 is absent and its path contains a dynamic submission_id.
- API #56 has no current route, so this is a future wiring discrepancy, not current endpoint behavior.

**Cần xác nhận**

1. Should the shared error helper change to emit data=null for contract errors, or should API #56 use a different explicit response path?
2. How will validation and unhandled errors on dynamic Mentor routes retain the catalog DESIGN_* business codes?

**Ảnh hưởng:** Error envelope shape and exact business codes can drift when the route is implemented.

## Trạng thái

Giữ **Draft — Needs Confirmation**. Không tự tạo cột/table, wire field, score rule, error code hoặc quyền assigned-Mentor để đóng các câu hỏi này.


Macro-review AC-23 #54–#57 đã hoàn tất ở mức tài liệu. API #57 giữ mutation feedback riêng sau #56; các gap về rubric, assets, quyền truy cập, schema và error mapping vẫn mở.