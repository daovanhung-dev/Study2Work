# Open Questions — API #52 Publish/unpublish nội dung Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** PATCH /api/v1/mentor/content/{content_id}/publish

## Q-52-01 — Request gửi ý định publish/unpublish bằng cách nào?

**Bằng chứng**

- Catalog row #52 và AC-22 PATCH node chỉ khai báo path content_id.
- Tên API có cả publish và unpublish, nhưng không có body/query/action field.

**Đề xuất cần xác nhận**

- Body {published:boolean!} biểu diễn trạng thái đích một cách tường minh.
- Đây là DERIVED proposal, chưa phải contract.

**Ảnh hưởng:** Nếu không có target input hoặc rule toggle được duyệt, client không thể chọn chiều mutation an toàn và retry có thể đảo trạng thái.

## Q-52-02 — Admin approve có tự publish không?

**Bằng chứng**

- AC-33 queue chọn PENDING_REVIEW.
- AC-33 approve node ghi UPDATE status = APPROVED/PUBLISHED + audit.
- AC-22 có API #52 riêng để cập nhật publication status.

**Cần xác nhận**

1. Approve chỉ đưa revision tới APPROVED hay đồng thời xuất bản?
2. Nếu approve tự publish, mục đích của API #52 là gì?
3. Unpublish có quay về APPROVED, DRAFT hay state khác?
4. State nằm ở Content hay revision?

**Ảnh hưởng:** Đây là blocker lifecycle cho #50–#53 và Admin AC-33.

## Q-52-03 — Điều kiện readiness gồm những gì?

**Bằng chứng**

- API catalog gọi rõ validate readiness.
- Catalog chỉ nêu ContentType và payload object, không liệt kê enum values hoặc subtype schema.

**Cần xác nhận**

Required fields per ContentType, asset readiness/ownership, title and payload constraints, course/version eligibility, and whether publication needs moderation approval.

**Ảnh hưởng:** Chặn request validation, response state and implementation. Không suy ra bộ rule từ legacy lessons hay pilot content_blocks.

## Q-52-04 — Content/version được lưu và chọn current revision thế nào?

**Bằng chứng**

- Legacy DDL không có generic Content/version relation.
- V1-PILOT content_blocks dùng UUID, lesson_id, block_type, content_json; không khớp BIGINT Content.
- AC-22 chỉ nêu UPDATE publication status; #51 có update + version.

**Cần xác nhận**

Approved physical table/model, current revision selector, status column ownership, live migration and response projection.

**Ảnh hưởng:** Chặn query/update SQL và trạng thái trả về.

## Q-52-05 — Mentor principal và course permission được xác định ra sao?

**Bằng chứng**

- Catalog requires role Mentor; AC-22 requires permission to manage course.
- Current Study auth is Student-oriented; Mentor claim/assignment relation is absent.
- Legacy courses.mentor_id is only a direct-owner candidate.

**Cần xác nhận**

JWT claim/key mapping, direct owner versus assigned Mentor policy, and error ordering for missing versus inaccessible Content.

**Ảnh hưởng:** Chặn executable access check and 403/404 behavior.

## Q-52-06 — Publish/unpublish có idempotent và concurrency-safe không?

**Đề xuất cần xác nhận**

- Proposed target-state body makes repeated identical requests a no-op.
- Confirm stale revision/concurrent updates behavior. Catalog has no 409 code; do not add one without contract change.

**Ảnh hưởng:** Chặn retry and concurrent mutation semantics.

## Q-52-07 — Content response phản ánh state/revision nào?

**Bằng chứng**

- Response is one Content object; Content has status but no version metadata.
- #51 proposal keeps a published revision active while a new revision is pending.

**Cần xác nhận**

Whether response contains current approved revision, newly published revision, or an aggregate Content projection; define parent_id null/omit and status serialization.

**Ảnh hưởng:** Chặn response source mapping and consistency with #49 tree reload.

## Q-52-08 — Middleware and validation codes are wired how?

The current path is absent from DESIGN_CONTRACT_PATHS. When the route is implemented, confirm an integration path that emits the exact catalog codes DESIGN_VALIDATION_ERROR and DESIGN_INTERNAL_ERROR. Also confirm framework handling for malformed/overflowing content_id; do not add an undeclared error code.

## Q-52-09 — Delete PUBLISHED Content có yêu cầu unpublish trước không?

API #53 đề xuất trả 422 khi Content PUBLISHED và yêu cầu gọi #52 unpublish trước; #52 proposal chuyển PUBLISHED về APPROVED. AC-22 không nêu thứ tự này và AC-33 approve còn mơ hồ. Cần xác nhận state transition và thứ tự #52 → #53.
