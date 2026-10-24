# Câu hỏi còn mở — API #80 Phê duyệt nội dung

Trạng thái: Draft — Needs Confirmation
Endpoint: PATCH /api/v1/admin/content/{content_id}/approve

## Q-80-01 — Approve chuyển sang APPROVED hay đồng thời PUBLISHED?

**Bằng chứng**

- AC-33 node n9 ghi UPDATE status = APPROVED/PUBLISHED + audit.
- AC-22 có API #52 riêng để đổi publication status.
- DD #52 ghi nhận chính sự mơ hồ này và chưa có state machine được duyệt.

**Cần xác nhận**

1. Admin approve chỉ đưa revision tới APPROVED hay cũng publish ngay?
2. Nếu approve đồng thời publish, API #52 vẫn chịu trách nhiệm cho trường hợp nào?
3. Status thuộc Content logic hay từng revision?

**Ảnh hưởng:** Chặn status transition của #80 và lifecycle liên kết #50–#53.

## Q-80-02 — Quyết định được khóa vào revision nào?

**Bằng chứng**

- AC-33 #79 đọc content/version/author.
- Catalog #80 chỉ nhận content_id; không có revision ID hoặc expected row version.
- #78/#79 hiện chưa chọn quy tắc pending/latest/current revision.

**Cần xác nhận**

Revision selector, stale detail behavior, concurrency/optimistic lock và branch khi revision đổi sau #79. Không chọn latest ngầm.

## Q-80-03 — Content và audit được lưu trong schema nào?

Legacy Study DDL không có generic Content/review/audit relation. V1-PILOT content_review_decisions dùng UUID resource_version_id, UUID reviewer và expected_row_version; đây là artifact khác ID space, không phải mapping trực tiếp cho Content int64.

Cần physical Content/revision/audit model, key/FK, status ownership, live migration evidence và retention policy đã được duyệt.

## Q-80-04 — Admin principal và authorization scope lấy từ đâu?

Catalog yêu cầu Admin, nhưng Study shared auth helper hiện chỉ có Student guard. Cần JWT claim/role parser, Admin guard, quyền moderation scope, thứ tự check và policy 403 so với 404.

## Q-80-05 — 422 dùng cho điều kiện nào?

Catalog khai báo 422 DESIGN_VALIDATION_ERROR nhưng không nêu trigger. Cần xác nhận parse/validation behavior, invalid transition và stale revision mapping mà không thêm code ngoài catalog. Chưa giả định state khác PENDING_REVIEW sẽ trả 422.

## Q-80-06 — Status update và audit có cùng transaction không?

AC-33 yêu cầu cả update status và audit nhưng không chỉ rõ thứ tự atomicity, rollback hoặc behavior khi chỉ một write thành công. Cần chọn transaction boundary sau khi physical schema được duyệt.

## Q-80-07 — Response phản ánh version/status nào?

Catalog trả một Content với tám field; AC-33 cũng đọc version/author nhưng request/response không chứa revision metadata. Cần xác nhận status sau approve và liệu metadata chỉ nội bộ hay catalog cần đổi.

## Q-80-08 — Error envelope và route integration được đồng bộ ra sao?

Middleware allowlist chưa có #80; framework fallback có thể phát generic codes. API guideline mong error data:null, còn current error_response() mặc định {} nếu caller không truyền data. Cần cập nhật wiring khi implementation được duyệt, đồng thời giữ exact code set từ catalog.

## Ranh giới proposal

- Không thêm published, reason, version, reviewer hoặc expected-row-version vào #80 request.
- Không thêm version, author, audit hoặc review metadata vào response.
- Không chọn physical Content/audit table hoặc SQL.
- Không đổi APPROVED/PUBLISHED thành một state machine nếu owner chưa quyết định.
- Macro-review tài liệu AC-33 #78–#81 đã hoàn tất; các điểm chưa quyết định được ghi trong [báo cáo nhóm](../81_admin_content_reject/VERIFICATION_REPORT.md).
