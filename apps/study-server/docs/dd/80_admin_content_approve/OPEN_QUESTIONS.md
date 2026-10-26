# Câu hỏi còn mở — API #80 Phê duyệt nội dung

Trạng thái: Draft — Needs Confirmation
Endpoint: PATCH /api/v1/admin/content/{content_id}/approve

Các quyết định dưới đây là fallback để triển khai local theo chỉ dẫn của user. Chúng không thay thế xác nhận của contract owner hoặc bằng chứng live schema.

## Đã chọn cho implementation local

| Vấn đề | Quyết định | Trạng thái |
|---|---|---|
| Approve state | `PENDING_REVIEW` → `APPROVED`; API #52 giữ publication transition `APPROVED` ↔ `PUBLISHED`. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Eligible row | Chỉ active `contents` row đang `PENDING_REVIEW`; non-pending trả catalog 422. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Physical schema | Legacy BIGINT `contents`; thêm `content_review_audit_logs` và migration 011 với nullable `reason`. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED; LIVE_UNVERIFIED` |
| Actor | Shared `ADMIN` guard; numeric JWT `sub` ghi vào `actor_user_id`. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Atomicity | Row lock, status update, audit insert, response projection và commit thuộc một transaction; failure rollback. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |
| Response | Direct reusable eight-field `Content`; không thêm audit/reason/reviewer/version metadata. | `DIRECT CONTRACT` |
| Invalid input | Malformed/out-of-range int64 path và non-pending state dùng catalog 422. | `RESOLVED_FOR_IMPLEMENTATION — DERIVED` |

## Q-80-01 — #80 có tác động đúng revision mà Admin đã xem ở #79 không?

#79/#80 chỉ truyền `content_id`; không có revision ID hoặc expected row version. #80 khóa và quyết định trên active row tại thời điểm gọi, nhưng không thể chứng minh đó là cùng revision đã hiển thị trước đó. Revision continuity, stale-item policy và optimistic concurrency cần contract owner xác nhận.

## Q-80-02 — Legacy candidate và migration 011 có được deploy/live xác nhận không?

`DB.sql` và migration 011 là checked-in source artifacts; focused tests dùng fake DB session. Live metadata, FK/index presence, grants, migration application và deployment chưa được kiểm tra.

## Q-80-03 — Role ADMIN có đủ cho moderation không?

Implementation dùng shared role `ADMIN`, như các API Admin hiện có. AC-33 không có source-backed dedicated moderation permission; policy chi tiết cần xác nhận riêng.

## Q-80-04 — API #81 có dùng cùng audit record để lưu rejection reason không?

API #81 hiện được wire locally và dùng một row trong `content_review_audit_logs` để lưu actor, chuyển trạng thái và rejection reason. Đây là mapping DERIVED từ migration 011 candidate; cần owner xác nhận và không chứng minh migration/schema đã triển khai live. Transaction của #81 thuộc implementation riêng, không phụ thuộc việc reuse handler #80.

## Ranh giới

- Không thêm published, reason, version, reviewer hoặc expected-row-version vào #80 request.
- Không thêm version, author, audit hoặc review metadata vào response.
- Không tuyên bố API #80 thao tác chính xác revision Admin đã xem ở #79.
- Không coi migration 011/fake DB tests là bằng chứng live schema hoặc deployed behavior.
- #80 DD vẫn `Draft — Needs Confirmation`.
