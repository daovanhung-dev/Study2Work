# Câu hỏi còn mở — API #81 Từ chối nội dung

Trạng thái: Draft — Needs Confirmation
Endpoint: `PATCH /api/v1/admin/content/{content_id}/reject`

## Q-81-01 — Reason được lưu/giữ bao lâu và ai có thể đọc?

**Bằng chứng và implementation local**

- Catalog yêu cầu body `reason:string!`; AC-33 yêu cầu status `REJECTED` cùng review reason.
- Legacy `contents` không có reason column. Runtime dùng một row trong `content_review_audit_logs`, row đó lưu `content_id`, actor, old/new status và request reason.
- API #80 migration 011 tạo cột `reason TEXT NULL`; dùng làm #81 destination là DERIVED fallback. Response Content không trả reason.

**Cần owner xác nhận** retention, quyền truy cập lịch sử, và nơi UI/API cần hiển thị reason.

## Q-81-02 — Có validation policy ngoài string type không?

Runtime yêu cầu strict JSON string, từ chối field thừa và giữ nguyên chuỗi; empty string hiện được chấp nhận. Catalog không định nghĩa trim, max length, blank-only, reason code hay locale. Owner có thể chốt policy nếu cần.

## Q-81-03 — API thao tác đúng revision nào?

#79/#81 chỉ truyền `content_id`, trong khi #79 có ý định đọc version và #51 có thể thay current row. Runtime khóa active row lúc #81 chạy nhưng không thể chứng minh đó là revision Admin đã xem. Cần revision selector/optimistic-lock contract và stale error mapping.

## Q-81-04 — Có cần audit event riêng ngoài reason-bearing row không?

Runtime ghi đúng một `content_review_audit_logs` row để vừa lưu reason vừa ghi decision actor/old/new status. Không có một append thứ hai. Đây là DERIVED vì reject node không chỉ rõ audit riêng; xác nhận nếu audit policy yêu cầu event khác.

## Q-81-05 — Legacy schema có phải persistence chuẩn và đã deploy chưa?

Runtime dùng checked-in BIGINT `contents` cùng migration 011 audit candidate. V1-PILOT decisions dùng UUID và không map trực tiếp với int64 contract. Cần xác nhận schema live, migration, FK/grants và legacy/V1-PILOT ownership.

## Q-81-06 — Moderation permission và state policy là gì?

Runtime dùng shared role `ADMIN` và yêu cầu current status `PENDING_REVIEW`; non-pending trả 422. Role mapping và state gate là local fallbacks; dedicated moderation permission, concealment policy và state-machine owner chưa có source.

## Q-81-07 — Revision, concurrency và transaction policy

Runtime dùng `SELECT ... FOR UPDATE`, conditional pending update, reason-bearing insert và commit atomically; failures rollback. Đây là derived pattern từ AC-33 cùng #80/#76, không xử lý revision token/stale item. Cần xác nhận nếu contract cần optimistic concurrency hoặc khác biệt 404/422.

## Q-81-08 — REJECTED Content có thể publish/delete không?

AC-22 API #52 và #53 là lifecycle calls riêng; chưa định nghĩa cách rejected content tham gia publish hoặc delete, Mentor resubmission và queue/history visibility.

## Ranh giới proposal

- Giữ exact body/path/error/response catalog contract; không thêm field, status code hay response metadata.
- Một decision row trong nullable reason candidate là physical mapping DERIVED; migration 011 chưa được xác nhận trên live DB.
- Không thêm revision ID, version, author, reason response field, schema mới hoặc second audit write.
- `PENDING_REVIEW` eligibility, empty-string acceptance, shared ADMIN permission and atomicity remain implementation choices while DD stays Draft.
- Local HTTP tests use fake DB sessions and do not prove database deployment or actual authorization policy.
