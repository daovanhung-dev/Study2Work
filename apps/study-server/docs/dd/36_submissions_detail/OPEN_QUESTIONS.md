# Open Questions — Study API #36 Xác nhận dữ liệu đã nộp

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** GET /api/v1/submissions/{submission_id}

Các câu hỏi này giữ lại chính sách truy cập và mapping chưa được API catalog, AC-17, AC-23 hoặc schema design chốt. DD không tự chọn thay Product/API/Architecture owner.

<a id="q-36-01-access-policy"></a>

## Q-36-01 — Student access và 403/404

**Bằng chứng**

- API #36 yêu cầu Student Bearer JWT và liệt kê cả 403 DESIGN_ACCESS_DENIED lẫn 404 DESIGN_RESOURCE_NOT_FOUND.
- AC-17 chỉ mô tả Student đọc submission summary sau khi nộp.
- Không có rule xác nhận caller phải là owner, đang enrolled, còn quyền truy cập course, hay predicate khác.
- Không có mapping giữa submission không tồn tại và submission tồn tại nhưng không thuộc caller.

**Cần xác nhận**

1. Student chỉ được đọc submission của chính mình hay có thể đọc submission được chia sẻ theo course?
2. Predicate course/enrollment/assignment nào áp dụng tại thời điểm gọi API?
3. Resource không thuộc caller trả 403 hay được mask thành 404?
4. Quyền đọc có thay đổi khi enrollment hoặc trạng thái assignment thay đổi không?

**Ảnh hưởng:** Query predicate, authorization order, 403/404 mapping và chống lộ sự tồn tại của submission.

<a id="q-36-02-grade-disclosure"></a>

## Q-36-02 — Thời điểm hiển thị score và feedback

**Bằng chứng**

- Reusable Submission schema có score?:decimal-string và feedback?:string.
- AC-23 cho phép Mentor đọc submission, lưu điểm và feedback.
- AC-17 chỉ yêu cầu UI hiển thị trạng thái đã nộp; không nêu thời điểm công bố kết quả cho Student.

**Cần xác nhận**

1. API #36 có luôn trả score và feedback khi các giá trị tồn tại không?
2. Nếu cần chờ công bố, trạng thái hoặc hành động nào cho phép hiển thị?
3. Khi chưa được công bố, hai field được omit hay trả null?

**Ảnh hưởng:** Response projection, privacy policy và kết quả Student nhìn thấy.

<a id="q-36-03-files-mapping"></a>

## Q-36-03 — Mapping files[] và API #34

**Bằng chứng**

- Submission.files là UploadAsset[]; UploadAsset gồm id, name, url, content_type, size_bytes và status.
- Candidate assignment_submissions chỉ có một nullable file_url.
- API #34 có flow upload/Object Storage nhưng asset identity, metadata persistence và association với submission chưa được chốt.

**Cần xác nhận**

1. Submission có hỗ trợ một hay nhiều file asset?
2. file_url ánh xạ sang UploadAsset nào, hay cần canonical asset/association schema?
3. URL trả về là public URL, signed URL hay identifier được resolve riêng?
4. API #36 có lọc asset theo ownership, purpose, trạng thái hoặc lifecycle nào?

**Ảnh hưởng:** Query/join, response mapping, file access control và tương thích với API #34.

<a id="q-36-04-status-time-schema"></a>

## Q-36-04 — Status, timestamp và baseline schema

**Bằng chứng**

- AC-17 đặt trạng thái ban đầu là SUBMITTED; AC-23 cập nhật bài nộp qua chấm điểm và feedback.
- DDL đặt default status là SUBMITTED nhưng SubmissionStatus đầy đủ chưa được định nghĩa.
- DDL dùng submitted_at TIMESTAMP; quy tắc timezone và serialization chưa có.
- DB_UNICA_TABLES.md mô tả assignment_id/user_id là required, trong khi checked-in DB.sql cho phép NULL.
- Live database metadata chưa được kiểm tra.

**Cần xác nhận**

1. SubmissionStatus có những giá trị/transition nào sau khi Mentor chấm hoặc ghi feedback?
2. submitted_at dùng timezone, precision và serialization nào?
3. Baseline nullability nào là canonical cho assignment_id và user_id?
4. Có cần xác minh hoặc migrate live schema trước khi API được triển khai không?

**Ảnh hưởng:** Response validity, null handling, data mapping và readiness triển khai.

<a id="q-36-05-invalid-path"></a>

## Q-36-05 — submission_id không parse được

**Bằng chứng**

- API catalog khai báo submission_id:int64! nhưng error set chỉ có 401/403/404/500.
- Catalog không quy định positive range, malformed path handling hoặc 400/422.

**Cần xác nhận**

1. Giá trị path không parse thành int64 được trả status/code nào?
2. Giá trị int64 không hợp lệ về miền nghiệp vụ có trả 404 hay status khác?
3. Nếu cần 400/422, API catalog có được cập nhật trước implementation không?

**Ảnh hưởng:** Router validation, error contract và client behavior.

<a id="q-36-06-message"></a>

## Q-36-06 — Message và meta chi tiết

**Bằng chứng**

- API Guidelines yêu cầu envelope fields và safe client message.
- API catalog chỉ khóa HTTP status và business code; không định nghĩa localized message hoặc meta fields riêng cho API #36.

**Cần xác nhận**

1. Message success/error có cần localization hoặc message key cụ thể không?
2. meta có cần thêm resource/access diagnostic nào không?

**Ảnh hưởng:** Response message contract và backward compatibility.

## Trạng thái cần duy trì

Giữ Draft — Needs Confirmation cho tới khi owner/access policy, grade disclosure, file mapping và schema semantics được chốt. Không sửa API catalog, AC diagrams, ERD hoặc DDL để tự giải quyết các câu hỏi này.
