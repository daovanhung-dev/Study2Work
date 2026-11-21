# Open Questions — Study API #35 Tạo/nộp submission

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** POST /api/v1/assignments/{assignment_id}/submissions

Các câu hỏi dưới đây giữ lại contract, business rule và persistence gaps chưa được API catalog, AC-17 hoặc schema design chốt. DD không tự chọn thay Product/API/Architecture owner.

<a id="q-35-01-file-reference"></a>

## Q-35-01 — Tên và biểu diễn file refs

**Bằng chứng**

- API catalog khai báo file refs:string! nhưng không ghi JSON key chính thức hoặc encoding.
- Logical Submission trả files:UploadAsset[].
- API #34 tạo UploadAsset, nhưng enum, asset ID, URL policy và metadata persistence của API #34 còn mở.
- Candidate assignment_submissions có một nullable file_url column.

**Cần xác nhận**

1. Tên JSON property wire thực tế là file refs, file_refs hay tên khác?
2. Chuỗi có chứa một asset ID, một URL, nhiều references, JSON text hay format khác?
3. Bao nhiêu asset được phép gắn vào submission?
4. API #35 nhận asset nào và kiểm tra ownership/purpose/course binding bằng cách nào?

**Ảnh hưởng:** Request schema, validation, authorization, files[] response và DB mapping.

<a id="q-35-02-text-content"></a>

## Q-35-02 — Required text và Submission.content

**Bằng chứng**

- API #35 catalog yêu cầu text:string!.
- Reusable Submission schema khai báo content?:string.
- DB table notes và checked-in DDL cho phép assignment_submissions.content NULL.

**Cần xác nhận**

1. Submission text luôn bắt buộc hay cho phép file-only submission?
2. Chuỗi rỗng/whitespace có hợp lệ không; có trimming hoặc giới hạn độ dài không?
3. Requiredness/nullable policy nào là canonical cho request, response và persistence?

**Ảnh hưởng:** Request validation, insert/update value và response serialization.

<a id="q-35-03-access-deadline"></a>

## Q-35-03 — Student eligibility, deadline và 403/409

**Bằng chứng**

- AC-17 yêu cầu assignment còn hạn và Student có quyền nộp.
- AC-17 mô tả nhánh quá hạn/không quyền là 403/409.
- API #35 catalog gồm cả 403 và 409 nhưng không gắn từng điều kiện với một mã cụ thể.
- assignments.due_at nullable; DB table notes nói NULL nghĩa là không có deadline.

**Cần xác nhận**

1. Predicate nào chứng minh Student được nộp: enrollment, course/assignment visibility, hay rule khác?
2. Khi assignment tồn tại nhưng Student không đủ quyền, trả 403 hay mask thành 404?
3. Deadline boundary và timezone là gì; due_at=NULL có tiếp tục nghĩa là không deadline không?
4. Điều kiện nào trả 409 DESIGN_STATE_CONFLICT?

**Ảnh hưởng:** Query/authorization predicates và status/business-code mapping.

<a id="q-35-04-resubmission-upsert"></a>

## Q-35-04 — INSERT/UPDATE, resubmission và concurrency

**Bằng chứng**

- AC-17 ghi INSERT/UPDATE Submission = SUBMITTED.
- DB design mô tả quan hệ assignments và assignment_submissions là 1:N.
- Checked-in DDL không có unique constraint trên assignment_id,user_id.

**Cần xác nhận**

1. Một Student được có một submission hay nhiều attempt cho cùng assignment?
2. Khi đã có submission, API tạo row mới hay cập nhật row hiện có; key nào chọn row?
3. Status hiện tại nào cho phép resubmit; score/feedback có được giữ hay reset?
4. Duplicate/concurrent request, transaction, locking và rollback được xử lý thế nào?

**Ảnh hưởng:** Query key, INSERT/UPDATE branch, status transition, uniqueness và 409 behavior.

<a id="q-35-05-file-persistence"></a>

## Q-35-05 — Persistence của files[] và liên kết API #34

**Bằng chứng**

- Logical Submission.files là UploadAsset[].
- Candidate assignment_submissions chỉ có một file_url.
- AC-17 gọi API #34 upload trước khi tạo submission; API #34 chưa có bảng Uploads được xác nhận.
- Không có association table hoặc asset ownership contract trong các nguồn được xem.

**Cần xác nhận**

1. Bổ sung schema/table quan hệ asset-submission hay đổi logical response sang field khác?
2. File references trỏ tới ID, URL hay object key nào; API #35 có cần query/claim asset không?
3. Xử lý upload thành công nhưng tạo submission thất bại, file bị thay thế hoặc orphaned object thế nào?

**Ảnh hưởng:** Data model, response projection, access control và lifecycle cleanup.

<a id="q-35-06-status-time-grade"></a>

## Q-35-06 — Status, submitted_at, score và feedback

**Bằng chứng**

- AC-17 cho biết trạng thái nhận bài là SUBMITTED; DB DDL đặt default SUBMITTED.
- SubmissionStatus không có enum values/lifecycle đầy đủ trong catalog.
- submitted_at là TIMESTAMP NOT NULL trong DDL nhưng không có timezone rule.
- score và feedback là nullable candidate columns; API #35 không mô tả chấm điểm.

**Cần xác nhận**

1. Ai tạo submitted_at, timezone/precision nào được dùng và response serialize ra sao?
2. Các SubmissionStatus hợp lệ và transition sau nộp là gì?
3. Initial score/feedback được bỏ qua, để NULL hay trả về theo policy nào?
4. Khi UPDATE/resubmit, thời gian và các trường chấm bài được giữ hay thay đổi?

**Ảnh hưởng:** Insert/update mapping và response semantics.

<a id="q-35-07-schema-nullability"></a>

## Q-35-07 — Canonical schema và nullability

**Bằng chứng**

- DB_UNICA_TABLES.md mô tả assignment_id/user_id là FK bắt buộc.
- Checked-in infra/postgres/study-server/DB.sql khai báo hai FK này nullable.
- DDL/diagram là design evidence; live database metadata chưa được kiểm tra.

**Cần xác nhận**

1. Tài liệu schema nào là baseline canonical cho assignment_submissions?
2. Có cần constraint/backfill trước implementation không?
3. Live schema cần được xác minh trước khi chuyển DD sang approved/implementation-ready không?

**Ảnh hưởng:** Requiredness, candidate insert, query joins và migration planning.

<a id="q-35-08-idempotency"></a>

## Q-35-08 — Retry và Idempotency-Key

**Bằng chứng**

- Shared API Guidelines quy định Idempotency-Key cho retryable mutations.
- API #35 tạo/cập nhật submission nhưng catalog không khai báo header hoặc retry semantics.
- INSERT/UPDATE branch và uniqueness policy chưa được xác định.

**Cần xác nhận**

1. API #35 có được retry tự động sau timeout không?
2. Nếu có, Idempotency-Key có thuộc request contract không và phạm vi lưu key là gì?
3. Retry cùng key trả lại response cũ, tiếp tục upsert hay báo 409?

**Ảnh hưởng:** Request headers, duplicate prevention, persistence và response behavior.

## Trạng thái cần duy trì

Giữ Draft — Needs Confirmation cho tới khi các quyết định ảnh hưởng file references, authorization/deadline, resubmission, schema và response được xác nhận. Không sửa API catalog, AC diagram, ERD hoặc DDL để tự giải quyết các câu hỏi này.
