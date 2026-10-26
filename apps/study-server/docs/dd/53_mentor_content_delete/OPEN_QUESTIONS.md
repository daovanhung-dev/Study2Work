# Open Questions — API #53 Xóa nội dung Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** DELETE /api/v1/mentor/content/{content_id}

## Q-53-01 — Dependency nào chặn xóa?

**Bằng chứng**

- Catalog nêu conditional delete và dependency check.
- Reusable Content khai báo `parent_id`; local migration 006 has the column and composite course relation. Live schema unverified.
- API #53 currently blocks an active direct child with 422 to keep API #49 active tree valid; this guard is DERIVED and does not cover unmodeled dependencies.

**Đề xuất cần xác nhận**

- Chặn khi còn Content con chưa xóa với parent_id bằng ID target; không cascade hoặc reparent.
- Xác nhận dependency ngoài cây Content như asset, assessment, progress, enrollment hoặc reference trong payload.

**Ảnh hưởng:** Chặn chốt điều kiện 422 và physical query.

## Q-53-02 — Có phải unpublish trước khi xóa Content PUBLISHED?

AC-22 có API #52 publish/unpublish riêng nhưng không nêu quan hệ với DELETE. Đề xuất PUBLISHED trả 422 và Mentor gọi #52 unpublish trước. Cần xác nhận thứ tự mutation và xử lý khi AC-33 approve đang gộp APPROVED/PUBLISHED.

## Q-53-03 — Có thể xóa PENDING_REVIEW, APPROVED hoặc REJECTED không?

AC-33 có pending queue, approval và rejection; AC-22 không nói xóa có withdraw khỏi review hay không. Cần xác nhận quyền xóa từng trạng thái, queue visibility, audit/notification và giữ review reason.

## Q-53-04 — Soft delete và history được lưu thế nào?

Local migration 006 defines `contents.deleted_at TIMESTAMP`; API #53 updates it with `CURRENT_TIMESTAMP`, validates `RETURNING`, and commits transactionally. This does not verify live migration state. Timestamp timezone interpretation, audit, and formal history retention policy remain to confirm.

## Q-53-05 — DELETE lặp với ID đã soft-delete trả gì?

Runtime active-row lookup returns 404 for a target already soft-deleted. This is DERIVED; confirm 404 versus idempotent 200 for retry semantics.

## Q-53-06 — Mentor và course permission được xác định ra sao?

Cần JWT claim/principal mapping, direct owner versus assigned Mentor policy và thứ tự 403/404 khi Content/Course thiếu hoặc không thuộc quyền.

## Q-53-07 — API #49 và moderation queue lọc Content đã xóa thế nào?

AC-22 yêu cầu reload tree sau delete; #49 trả singular Content dù purpose nói cây. AC-33 không nói queue có loại soft-deleted item. Cần xác nhận active tree/public view/review queue filtering để target không xuất hiện lại sau reload.

## Q-53-08 — Middleware map lỗi thế nào?

DELETE route and local HTTP tests now exist; the same parameterized route template is registered by API #51 in `DESIGN_CONTRACT_PATHS`. Invalid path IDs currently map to 404 by Content API convention; child/PUBLISHED guards map to catalog 422. These mappings are source-backed local behavior, while policy remains DERIVED.
