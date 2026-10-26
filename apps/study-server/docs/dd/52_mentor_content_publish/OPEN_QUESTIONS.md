# Open Questions — API #52 Publish/unpublish nội dung Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** PATCH /api/v1/mentor/content/{content_id}/publish

## Q-52-01 — Request gửi ý định publish/unpublish bằng cách nào?

**Bằng chứng**

- Catalog row #52 và AC-22 PATCH node chỉ khai báo path content_id.
- Tên API có cả publish và unpublish, nhưng không có body/query/action field.

**Trạng thái hiện tại / cần xác nhận**

- Local runtime dùng body {published:boolean!} để biểu diễn trạng thái đích một cách tường minh.
- Đây vẫn là DERIVED proposal và chưa có trong catalog/AC-22; contract owner cần xác nhận hoặc thay thế.

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

**Ảnh hưởng:** Local fallback chỉ dùng APPROVED status gate; contract readiness đầy đủ vẫn chưa thể chốt. Không suy ra bộ rule từ legacy lessons hay pilot content_blocks.

## Q-52-04 — Content/version được lưu và chọn current revision thế nào?

**Bằng chứng**

- Legacy DDL/migration 006 now defines base `contents`; it does not define version history or establish live deployment.
- V1-PILOT content_blocks dùng UUID, lesson_id, block_type, content_json; không khớp BIGINT Content.
- AC-22 chỉ nêu UPDATE publication status; #51 có update + version.

**Cần xác nhận**

Approved physical table/model, current revision selector, status column ownership, live migration and response projection.

**Ảnh hưởng:** Local fallback uses `contents.status` and returns the API #49 Content projection; approved revision selection, canonical storage ownership, and live schema remain unresolved.

## Q-52-05 — Mentor principal và course permission được xác định ra sao?

**Bằng chứng**

- Catalog requires role Mentor; AC-22 requires permission to manage course.
- Current Study shared guard validates role MENTOR; APIs #49 and #51–#52 compare numeric JWT `sub` to direct `courses.mentor_id`.
- Assigned-Mentor/co-owner relation is absent from the inspected local schema/source; direct ownership remains a fallback, not approved policy.

**Cần xác nhận**

JWT claim/key mapping, direct owner versus assigned Mentor policy, and error ordering for missing versus inaccessible Content.

**Ảnh hưởng:** Local direct-owner access fallback is implemented; identity namespace, assigned-Mentor policy, and canonical 403/404 ordering remain open.

## Q-52-06 — Publish/unpublish có idempotent và concurrency-safe không?

**Đề xuất cần xác nhận**

- Proposed target-state body makes repeated identical requests a no-op.
- Confirm stale revision/concurrent updates behavior. Catalog has no 409 code; do not add one without contract change.

**Ảnh hưởng:** Local fallback is target-idempotent and serializes through row locks; canonical retry/concurrency policy and cross-endpoint locking remain unconfirmed.

## Q-52-07 — Content response phản ánh state/revision nào?

**Bằng chứng**

- Response is one Content object; Content has status but no version metadata.
- #51 proposal keeps a published revision active while a new revision is pending.

**Cần xác nhận**

Whether response contains current approved revision, newly published revision, or an aggregate Content projection; define parent_id null/omit and status serialization.

**Ảnh hưởng:** Local fallback returns the locked current `contents` row; published-revision selection and consistency with Admin review/#49 reload remain unresolved.

## Q-52-08 — Middleware and validation codes are wired how?

**Local status:** The route template is now present in `DESIGN_CONTRACT_PATHS`. Fake DB HTTP tests confirm body validation uses `DESIGN_VALIDATION_ERROR`, malformed/out-of-range path IDs map to catalog 404, and query/commit errors map to `DESIGN_INTERNAL_ERROR`. Live middleware/database behavior remains unverified. The request body itself remains a catalog discrepancy; do not add undeclared error codes.

## Q-52-09 — Delete PUBLISHED Content có yêu cầu unpublish trước không?

API #53 đề xuất trả 422 khi Content PUBLISHED và yêu cầu gọi #52 unpublish trước; #52 proposal chuyển PUBLISHED về APPROVED. AC-22 không nêu thứ tự này và AC-33 approve còn mơ hồ. Cần xác nhận state transition và thứ tự #52 → #53.
