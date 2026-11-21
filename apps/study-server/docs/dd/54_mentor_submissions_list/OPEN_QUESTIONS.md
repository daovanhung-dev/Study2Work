---
title: "Open Questions — Study API #54 Lấy submissions"
order: 10
dd_id: "54"
api_name: "Lấy submissions"
source_sheet: "Open Questions"
status: "Draft — Needs Confirmation"
---

# Câu hỏi còn mở — Study API #54

**Endpoint:** GET /api/v1/mentor/submissions
**Status:** Draft — Needs Confirmation

## Đã chọn fallback theo chỉ dẫn của người dùng

- Collection response được chọn để phục vụ AC-23 list/select: `ApiEnvelope<Page<Submission>>`.
- `page` dùng trang 1 mặc định, kích thước cố định 20 và stable order `submitted_at DESC, id DESC`.
- File asset được resolve bằng exact URL, owner, purpose và course; đây là `DERIVED`, không phải FK.
- Direct-owner Mentor scope tái sử dụng API #46/#49; assigned Mentors chưa được hỗ trợ.

Các lựa chọn trên đã được triển khai để API #54 chạy nhất quán. Chúng vẫn cần API/schema owner xác nhận trước khi DD được coi là approved.

## Q-54-01 — Producer contract cho file URL

**Bằng chứng:** API #35 nhận `file refs:string!`, còn DDL lưu một nullable `assignment_submissions.file_url`; API #34 trả URL và metadata UploadAsset, nhưng không có association table.

**Cần xác nhận:** API #35 có lưu đúng URL của API #34 vào `file_url` hay cần bảng liên kết asset-submission? Nếu khác, cung cấp khóa chính thức để API #54 tra files.

**Ảnh hưởng:** Submission.files completeness và tương thích producer #35.

## Q-54-02 — Assigned Mentor và access policy

**Bằng chứng:** API #46/#49 và API #34 lecture upload chỉ dùng `courses.mentor_id`; không có relation assigned Mentor trong các nguồn đã đọc.

**Cần xác nhận:** AC-23 có cho phép Mentor được phân công chấm course của owner khác không? Nếu có, cung cấp relation/predicate.

**Ảnh hưởng:** Authorization coverage; API #54 hiện chỉ cho direct owner.

## Q-54-03 — Status lifecycle và grading 409

**Bằng chứng:** Catalog nhận `status:string`; DDL có `VARCHAR(20)`; AC-17 cho trạng thái đầu `SUBMITTED`, AC-23 đưa trạng thái `GRADED`; catalog #54 giữ 409 nhưng không chỉ ra trigger.

**Cần xác nhận:** Enum/status lifecycle đầy đủ là gì và điều kiện nào (nếu có) tạo `409 DESIGN_STATE_CONFLICT`?

**Ảnh hưởng:** Filter compatibility và 409 contract; hiện không có nhánh 409 runtime.

## Q-54-04 — Nullability, timestamp và live schema

**Bằng chứng:** Guide/ERD yêu cầu assignment/course/student relations, trong khi checked-in DDL cho phép FK NULL; `submitted_at` là TIMESTAMP không có timezone; live metadata chưa được kiểm tra.

**Cần xác nhận:** Schema artifact nào là baseline? Quan hệ null/orphan và timezone serialization được xử lý theo rule nào? Migration/API runtime đã triển khai ở môi trường đích chưa?

**Ảnh hưởng:** Row completeness, date-time contract và deployment readiness.

## Q-54-05 — Error catalog confirmation

**Bằng chứng:** Route query constraints trả 422 `DESIGN_VALIDATION_ERROR`, đã được bổ sung vào API catalog và AC-23 node; 409 vẫn khai báo nhưng không có trigger.

**Cần xác nhận:** Chủ sở hữu contract chấp thuận việc bổ sung 422 và giữ 409 unreachable cho tới khi có business rule không?

**Ảnh hưởng:** API client generation và final contract approval.
