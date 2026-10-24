# Open Questions — API #53 Xóa nội dung Mentor

**Trạng thái DD:** Draft — Needs Confirmation
**Endpoint:** DELETE /api/v1/mentor/content/{content_id}

## Q-53-01 — Dependency nào chặn xóa?

**Bằng chứng**

- Catalog nêu conditional delete và dependency check.
- Reusable Content khai báo parent_id tùy chọn; generic Content DDL chưa có.

**Đề xuất cần xác nhận**

- Chặn khi còn Content con chưa xóa với parent_id bằng ID target; không cascade hoặc reparent.
- Xác nhận dependency ngoài cây Content như asset, assessment, progress, enrollment hoặc reference trong payload.

**Ảnh hưởng:** Chặn chốt điều kiện 422 và physical query.

## Q-53-02 — Có phải unpublish trước khi xóa Content PUBLISHED?

AC-22 có API #52 publish/unpublish riêng nhưng không nêu quan hệ với DELETE. Đề xuất PUBLISHED trả 422 và Mentor gọi #52 unpublish trước. Cần xác nhận thứ tự mutation và xử lý khi AC-33 approve đang gộp APPROVED/PUBLISHED.

## Q-53-03 — Có thể xóa PENDING_REVIEW, APPROVED hoặc REJECTED không?

AC-33 có pending queue, approval và rejection; AC-22 không nói xóa có withdraw khỏi review hay không. Cần xác nhận quyền xóa từng trạng thái, queue visibility, audit/notification và giữ review reason.

## Q-53-04 — Soft delete và history được lưu thế nào?

AC-22 chỉ nêu soft delete; DeleteResult có deleted_at nhưng không chỉ định cột. Legacy DDL thiếu generic Content, pilot content_blocks là UUID/lesson-bound. Cần chọn tombstone field/table, timestamp source/timezone, transaction, retention và audit policy.

## Q-53-05 — DELETE lặp với ID đã soft-delete trả gì?

Đề xuất target đã soft-delete là unavailable và trả 404. Cần xác nhận 404 hay idempotent 200 với DeleteResult để khóa retry semantics.

## Q-53-06 — Mentor và course permission được xác định ra sao?

Cần JWT claim/principal mapping, direct owner versus assigned Mentor policy và thứ tự 403/404 khi Content/Course thiếu hoặc không thuộc quyền.

## Q-53-07 — API #49 và moderation queue lọc Content đã xóa thế nào?

AC-22 yêu cầu reload tree sau delete; #49 trả singular Content dù purpose nói cây. AC-33 không nói queue có loại soft-deleted item. Cần xác nhận active tree/public view/review queue filtering để target không xuất hiện lại sau reload.

## Q-53-08 — Middleware map lỗi thế nào?

Endpoint hiện không có trong route hoặc DESIGN_CONTRACT_PATHS. Khi implement cần xác nhận malformed/out-of-range content_id, dependency 422 và 500 integration mapping; giữ đúng business code catalog.
