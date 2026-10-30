# Câu hỏi còn mở — API #78 Lấy pending content

Trạng thái: `Draft — Needs Confirmation`. API #78 đã được wire dựa trên current legacy `contents` source và fallback Page; các mismatch catalog/policy/live DB vẫn cần owner review.

## Q-78-01 — Catalog có đổi response thành Page không?

Catalog #78 và AC-33 ghi `ApiEnvelope<Content>` đơn, trong khi endpoint mở queue và có query `page`. Runtime hiện trả `ApiEnvelope<Page<Content>>` để biểu diễn nhiều item và empty queue. Cần owner xác nhận và đồng bộ `docs/lists/list_api.md`/reusable response; không sửa catalog tự động.

## Q-78-02 — Pagination, default và ordering

Runtime dùng page 1-based/default 1, fixed size 20, `id ASC`, count cùng filters và 200 cho empty/out-of-range Page theo API #73. Catalog không có size/order và không xác định pagination behavior. Cần phê duyệt page bounds, size và thứ tự review (FIFO hiện không được chứng minh bởi id).

## Q-78-03 — Live schema/migration

Checked-in legacy DDL/migrations 006/007 và current APIs #49–#53 xác nhận local candidate `contents`/`content_versions`; fake-session tests không chứng minh migration đã apply hoặc live columns/constraints. Cần xác nhận database runtime thật.

## Q-78-04 — ContentType members/casing

Runtime giữ raw `type` string và exact-match `contents.content_type`, không whitelist/normalize. Cần owner định nghĩa enum nếu client cần validate trước request.

## Q-78-05 — Queue row và revision cho #79–#81

API #50 tạo logical row với `PENDING_REVIEW`; #51 lưu state cũ vào `content_versions` rồi đổi current row về `PENDING_REVIEW`. API #78 chỉ trả current `contents` row, không version metadata. Cần xác nhận version/revision mà detail #79 và quyết định #80/#81 sẽ đọc/ghi, cùng cách xử lý stale queue.

## Q-78-06 — Deleted/stale visibility

Runtime loại `deleted_at IS NOT NULL` theo fallback DERIVED phù hợp active views #49/#53. AC-33 không nói item bị soft-delete hoặc revision cũ có còn trong queue không; cần owner xác nhận cùng lifecycle #51/#53.

## Q-78-07 — Admin moderation permission

Runtime dùng shared role `ADMIN` trước parse/query. Source hiện tại không chứng minh permission moderation riêng; cần xác nhận nếu AC-33 yêu cầu scope hẹp hơn role Admin.

## Q-78-08 — Error contract

Catalog chỉ liệt kê 401/403/500. Runtime thêm 422 `DESIGN_VALIDATION_ERROR` cho numeric query parse/range theo API #73; cần cập nhật catalog hoặc xác nhận behavior khác. Empty queue vẫn trả Page 200.

## Ranh giới đã triển khai

- Direct predicate `status=PENDING_REVIEW`; local source mapping `contents` và active-row filter `deleted_at IS NULL`.
- Exact `type`/`course` filters; page default 1, size 20, `id ASC`; collection response Page; query validation 422. Các lựa chọn ngoài predicate direct đều là `DERIVED`.
- API #78 chỉ đọc current Content fields; không thêm author/version/review metadata và không thực hiện #79–#81 decisions/audit.
- Local tests/OpenAPI xác nhận route code hiện hành; không xác minh live DB, migration deployment hoặc policy approval.
