---
title: "Open Questions — Study API #57 Lưu feedback"
order: 10
dd_id: "57"
api_name: "Lưu feedback bài nộp Mentor"
source_sheet: "Open Questions"
status: "Draft — Needs Confirmation"
---

# Câu hỏi còn mở — Study API #57

**Endpoint:** POST /api/v1/mentor/submissions/{submission_id}/feedback

Các câu hỏi dưới đây giữ contract ở trạng thái draft. Không câu trả lời nào được tự suy ra từ tên endpoint hoặc từ việc API xuất hiện trong diagram.

## Q-57-01 — Wire key của feedback text

**Bằng chứng**

- Catalog ghi descriptor nguyên văn feedback text:string!.
- Reusable Submission đặt response field là feedback:string?.
- Không có request model hoặc route runtime cho API #57.

**Cần xác nhận**

1. JSON property có đúng literal là feedback text hay key là feedback?
2. Có normalization, giới hạn độ dài hoặc rule chuỗi rỗng nào không?

**Ảnh hưởng:** Tương thích client, request validation và map sang feedback column.

**Implementation fallback (DERIVED):** Runtime nhận `feedback_text` strict string, không trim/giới hạn độ dài/ép non-empty. Catalog owner vẫn cần xác nhận wire spelling.

## Q-57-02 — Định dạng và persistence của attachments

**Bằng chứng**

- Catalog yêu cầu attachments:string!, nhưng không ghi cấu trúc/encoding.
- Legacy assignment_submissions có file_url cho file học viên nộp; không có relation cho feedback attachment.
- Reusable Submission có files:UploadAsset[] nhưng không có feedback_attachments.

**Cần xác nhận**

1. attachments là chuỗi URL, chuỗi JSON, ID asset hay dữ liệu đã upload qua API #34?
2. Asset được lưu/liên kết với submission ở đâu và quyền truy cập URL được áp dụng thế nào?
3. Chuỗi rỗng có hợp lệ không; giới hạn số lượng/kích thước/status nào được áp dụng?
4. API #57 phải trả các attachment này ở field nào nếu response hiện là Submission?

**Ảnh hưởng:** Request contract, storage access control, transaction boundary và khả năng hoàn tất response.

**Implementation fallback:** Runtime nhận `attachments` strict string nhưng không parse, persist, echo hoặc ánh xạ sang student `file_url`/`Submission.files`. Không có storage target nào được chọn.

## Q-57-03 — INSERT/UPDATE, ghi đè và lịch sử feedback

**Bằng chứng**

- AC-23 diagram ghi INSERT/UPDATE feedback.
- Legacy candidate có một cột nullable assignment_submissions.feedback TEXT.
- Không tìm thấy history table hoặc relation feedback riêng cho assignment submission.

**Đề xuất đơn giản (DERIVED)**

- Nếu xác nhận dùng legacy column, UPDATE field hiện có là phương án ít thành phần nhất.

**Cần xác nhận**

1. Gọi lại API #57 thay thế feedback cũ hay tạo một bản ghi lịch sử?
2. Nếu cần lịch sử, bảng/khóa/timestamp/author nào là nguồn chính thức?
3. Có yêu cầu idempotency cho retry không?

**Ảnh hưởng:** Mutation target, transaction, concurrency và audit.

**Implementation fallback (DERIVED):** Runtime cập nhật duy nhất `assignment_submissions.feedback`; lần gọi sau ghi đè giá trị hiện có. Không tạo history row; schema/live behavior và approval vẫn chưa xác nhận.

## Q-57-04 — Submission response, rubric và hai loại file

**Bằng chứng**

- Catalog yêu cầu ApiEnvelope<Submission>; Submission có files:UploadAsset[] và feedback, nhưng không có rubric hoặc feedback attachments.
- AC-23 API #55 node nói đọc Submission + files + rubric.
- API #56 nhận rubric_items theo fallback wire key nhưng không persist vì chưa có schema/persistence target được duyệt.
- APIs #54–#56 use the same DERIVED constrained file lookup; API #35 producer compatibility remains open.

**Cần xác nhận**

1. Rubric được trả cho client qua API #55 hay được xử lý riêng; nếu trả thì thuộc field/schema nào?
2. UploadAsset của bài nộp được lưu/liên kết ở đâu để dựng Submission.files?
3. Feedback attachments có response field riêng hay chỉ được xác nhận đã lưu?

**Ảnh hưởng:** Response schema và tính nhất quán của #54–#57.

## Q-57-05 — Mentor identity và access scope

**Bằng chứng**

- AC-23 yêu cầu Mentor có quyền chấm submission của course.
- The shared Study guard supports explicit MENTOR role; #57 uses it before database access.
- courses.mentor_id là direct-owner candidate; Mentor claim mapping và assignment relation chưa được xác nhận.
- DDL cho phép assignment_submissions.assignment_id và assignments.course_id NULL, khác với guide/ERD yêu cầu quan hệ.

**Cần xác nhận**

1. JWT claim nào xác định Mentor và ánh xạ tới users.id ra sao?
2. Quyền chỉ dựa trên direct owner hay gồm Mentor được phân công?
3. Submission ngoài quyền trả 403 hay được mask thành 404?
4. Submission có relation null/orphan được xử lý ra sao?

**Ảnh hưởng:** Bảo vệ dữ liệu học viên, predicate truy vấn và phân biệt 403/404.

**Implementation fallback (DERIVED):** Runtime dùng numeric JWT subject với `courses.mentor_id`; trả 403 cho owner khác và 500 cho broken required relation. Assigned-Mentor support chưa có nguồn.

## Q-57-06 — Thời điểm status và Student visibility

**Bằng chứng**

- AC-23 UI flow gọi #56 rồi #57.
- API #56 hiện cập nhật score/status thành GRADED rồi commit sau khi response projection hợp lệ; score range và direct-owner scope là DERIVED. API #57 được mô tả là bước lưu feedback.
- AC-23 postcondition nói Student có thể nhận kết quả, nhưng không quy định thời điểm release.

**Đề xuất đơn giản (DERIVED)**

- Giữ nguyên score/status trong #57 và không thêm trạng thái hoặc precondition mới.

**Cần xác nhận**

1. Student được thấy điểm sau #56 hay chỉ sau khi #57 lưu feedback?
2. Có cần #57 từ chối nếu status chưa GRADED khi gọi trực tiếp không?

**Ảnh hưởng:** API direct-call behavior và thời điểm công bố kết quả.

**Implementation fallback (DERIVED):** Runtime không yêu cầu `status=GRADED` và chỉ cập nhật feedback; score/status được kiểm tra là không đổi.

## Q-57-07 — Error envelope và route mapping

**Bằng chứng**

- API Guidelines yêu cầu data=null trên error.
- Current error_response(data=None) serializes data as null.
- Middleware matches registered FastAPI route templates; #57's dynamic route is registered in DESIGN_CONTRACT_PATHS.
- Current `error_response()` returns `data:null`; RequestValidationError maps to `DESIGN_VALIDATION_ERROR` on the registered route.

**Cần xác nhận**

1. Catalog owner có chấp thuận wire key và các fallback mapping hiện tại không?
2. Có yêu cầu bổ sung nào về ErrorDetail field/code/message ngoài business code catalog không?

**Ảnh hưởng:** Phê duyệt compatibility của wire contract và error details.

## Trạng thái

Giữ Draft — Needs Confirmation. AC-23 macro-review #54–#57 đã hoàn tất ở mức tài liệu; #54 Page<Submission>/pagination/file lookup và #56 rubric wire-key/score-range/direct-owner policy là DERIVED. Rubric persistence, API #35 producer compatibility, assigned-Mentor access và feedback attachment storage vẫn chờ nguồn/owner xác nhận.
