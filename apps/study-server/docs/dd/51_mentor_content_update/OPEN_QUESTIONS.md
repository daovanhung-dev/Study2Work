# Open Questions — API #51 Cập nhật nội dung Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** `PUT /api/v1/mentor/content/{content_id}`

## Q-51-01 — PUT có body nào và field nào được sửa?

**Bằng chứng**

- Catalog row #51 và AC-22 PUT node chỉ khai báo `path{content_id:int64!}`.
- AC-22 lại yêu cầu `UPDATE Content + version`.
- API #50 create body có `course_id`, `content_type`, `title`, `payload`; reusable Content còn có `status`, `parent_id?`, `order`.

**Đề xuất cần xác nhận**

- PUT nhận full replacement `{content_type:ContentType!, title:string!, payload:object!}`.
- `content_id` lấy từ path; `course_id` lấy và giữ từ stored Content.
- `status`, `parent_id`, `order`, `id` là server-managed và không nằm trong request body.

**Ảnh hưởng:** Chặn request model, validation, OpenAPI contract và khả năng implementation đúng semantics PUT.

## Q-51-02 — “Content + version” dùng mô hình version nào?

**Bằng chứng**

- AC-22 ghi “UPDATE Content + version”.
- AC-33 đọc `content/version/author` khi Admin review.
- Catalog Content không có version field. Legacy DDL thiếu Content/version; V1-PILOT `content_blocks.row_version` thuộc UUID/lesson model khác.

**Đề xuất cần xác nhận**

- Mỗi PUT tạo revision mới; giữ bản cũ để audit/review; cùng transaction cập nhật current revision.
- Không coi `row_version` của pilot hoặc một cột `version_no` chưa tồn tại là mapping đã duyệt.

**Ảnh hưởng:** Chặn SQL, transaction, concurrency, revision response và rollback design.

## Q-51-03 — Revision mới có cần review lại không?

**Bằng chứng**

- AC-33 moderation queue lọc `status=PENDING_REVIEW` và Admin đọc content/version/author.
- AC-22 update node không nêu status transition.
- API #50 DD đề xuất cùng trạng thái ban đầu `PENDING_REVIEW` nhưng chưa được xác nhận.

**Đề xuất cần xác nhận**

- Revision mới vào `PENDING_REVIEW`; bản published trước đó vẫn phục vụ đến khi revision mới được duyệt và publish.
- Chốt status ở Content hay version, và status response đại diện bản nào.

**Ảnh hưởng:** Có thể thay đổi nội dung công khai, moderator queue và phối hợp API #52.

## Q-51-04 — Mentor identity và quyền course được kiểm tra ra sao?

**Bằng chứng**

- Catalog yêu cầu Bearer JWT role Mentor; AC-22 yêu cầu quyền quản lý course.
- Study hiện có Student auth guard; không có Mentor identity/assignment relation source.
- Legacy `courses.mentor_id` chỉ là candidate direct owner.

**Cần xác nhận**

- JWT claim nào map tới Mentor?
- Có cho phép co-owner/assigned Mentor không?
- Thứ tự 404 Content với 403 access và thông điệp chống ID enumeration là gì?

**Ảnh hưởng:** Chặn executable authorization query; error code 403/404 vẫn giữ theo catalog.

## Q-51-05 — Content/version lưu ở schema nào?

**Bằng chứng**

- Legacy DB có `courses`/`lessons`, không generic Content/version.
- V1-PILOT có UUID `content_blocks`, gắn `lesson_id`, khác BIGINT Content/`course_id`.
- Live schema chưa được xác minh.

**Cần xác nhận**

- Bảng/model và migration đã duyệt; khóa/field mapping; cách đọc current version; giữ lịch sử; audit fields; ID strategy; projection `ApiEnvelope<Content>`.

**Ảnh hưởng:** Chặn physical Query/Mutation Mapping và implementation.

## Q-51-06 — Validation và concurrency policy là gì?

**Bằng chứng**

- Catalog khai báo 422 `DESIGN_VALIDATION_ERROR` nhưng body rỗng.
- Không có 409 trong API #51.

**Cần xác nhận**

- Enum `ContentType`, payload schema, title constraints và content-state eligibility.
- Hai PUT đồng thời được serialize, reject hay last-write-wins? Nếu cần conflict response, contract phải được cập nhật thay vì tự thêm 409 vào DD.

**Ảnh hưởng:** Chặn validation, optimistic/pessimistic locking và error mapping.

## Q-51-07 — Publish và approval tương tác thế nào?

**Bằng chứng**

- AC-22 có API #52 riêng publish/unpublish.
- AC-33 approve node ghi `APPROVED/PUBLISHED`; reject ghi `REJECTED`.
- API #51 update có version side effect.

**Cần xác nhận trong macro-review #50–#53 + AC-33**

- Approve tự publish hay chỉ chấp thuận revision?
- API #52 publish Content hay revision cụ thể?
- Revision mới pending có giữ published revision cũ phục vụ không?

**Ảnh hưởng:** Trạng thái response, danh sách public, rollback và review audit.

## Q-51-08 — Middleware allowlist có được cập nhật khi route được wire?

API #51 hiện chưa có route và path không nằm trong `DESIGN_CONTRACT_PATHS`. Khi implementation, cập nhật allowlist hoặc xác nhận cơ chế khác để validation/internal exceptions phát `DESIGN_VALIDATION_ERROR`/`DESIGN_INTERNAL_ERROR` đúng catalog.

## Q-51-08 — Xóa Content ảnh hưởng các revision thế nào?

API #51 đề xuất tạo revision mới và giữ revision đã publish trong lúc review. API #53 đề xuất soft-delete logical Content và bảo toàn version/review history. Cần xác nhận deletion ẩn toàn bộ revision hay chỉ current projection, và cách bảo toàn published revision/history.
