# Câu hỏi còn mở — API #78 Lấy pending content

Trạng thái: `Draft — Needs Confirmation`. Catalog/diagram đã xác nhận queue predicate và endpoint sequence; contract response, Content persistence và Admin wiring chưa đủ để implementation.

## Q-78-01 — Queue trả một Content hay một danh sách?

**Bằng chứng**

- Tên API là “Lấy pending content”; AC-33 mở hàng đợi và có query `page`.
- Catalog success response là `ApiEnvelope<Content>` đơn, không phải `Page<Content>` hoặc collection.
- API #68 có mismatch tương tự; #73 khai báo `Page<Course>` trực tiếp.

**Cần xác nhận**

1. Giữ `ApiEnvelope<Content>` và giải thích page/cardinality nghĩa gì, hay sửa catalog/reusable response thành `ApiEnvelope<Page<Content>>`?
2. Nếu là Page, có thêm `PageMeta` chuẩn và trả `items=[]` khi queue rỗng không?

**Ảnh hưởng:** Chặn xác định Q1 row cardinality, response JSON, count query, empty behavior và dùng thực tế của `page`.

## Q-78-02 — Pagination, default và ordering là gì?

Catalog chỉ có `page?:int32`, không có `size` hoặc `sort`; không có Page response hiện hành. Nếu contract đổi sang Page, đề xuất đơn giản là page 1-based/default 1, size cố định 20, thứ tự `id ASC`. Cần xác nhận page <= 0/overflow và thứ tự ưu tiên review; `id ASC` không chứng minh FIFO.

## Q-78-03 — Content được lưu ở đâu và row nào đại diện queue item?

Legacy DDL/ERD không có generic Content/version relation. V1-PILOT `content_blocks` dùng UUID + `lesson_id`; `content_review_decisions` là append-only decision log theo UUID `resource_version_id`. Chúng không khớp Content BIGINT response. Cần model/table/columns/PK/version schema và live migration đã duyệt.

## Q-78-04 — `type` filter khớp field/enum nào?

Catalog nhận `type:string`, response dùng `Content.content_type:ContentType`. Cần xác nhận equality/case, allowed values và cách xử lý unknown/blank. Không tự dựng ContentType whitelist.

## Q-78-05 — Queue chọn version hiện hành nào?

AC-33 node #79 đọc `content/version/author`, nhưng #78 response Content không có version metadata. Cần xác nhận queue chứa logical Content hay từng pending revision, revision nào hiển thị khi có bản PUBLISHED cũ và revision mới đang chờ review.

## Q-78-06 — Producer nào đưa item vào `PENDING_REVIEW`?

AC-33 trực tiếp lọc `status=PENDING_REVIEW`; #50 create và #51 update/version chỉ đề xuất trạng thái này trong các DD liên quan. Cần xác nhận trạng thái khởi tạo/chuyển revision, cập nhật nội dung khi đang review và ai có quyền rút pending item.

## Q-78-07 — Deleted/stale content có nằm trong queue không?

AC-33 không chỉ rõ filter deleted/revision-stale. #53 đề xuất soft-delete và ẩn khỏi active views/queue nhưng marker và policy chưa được duyệt. Cần xác nhận queue có loại item đã xóa, revision superseded hoặc Content bị xóa trong lúc Admin review không.

## Q-78-08 — Admin guard và query scope được xác định ra sao?

Catalog yêu cầu role Admin; current shared Study guard chỉ chấp nhận Student. Cần claim/guard/Admin scope source và cách bảo đảm request chỉ đọc moderation queue. Không tái dùng Student guard hoặc tạo permission table.

## Q-78-09 — Empty queue và invalid query dùng behavior nào?

Catalog chỉ có lỗi 401/403/500, không có 404/422. Cần xác nhận empty queue, invalid `type`, `course` âm/overflow và `page` ngoài range mà không phát sinh code ngoài contract.

## Q-78-10 — AC-33 approval/rejection có giữ cùng version với queue item không?

Diagram đưa #80 approve sang `APPROVED/PUBLISHED` + audit và #81 reject sang `REJECTED` + reason. Cần chọn revision/row identity mà queue #78 và detail #79 truyền tiếp, đồng thời giữ audit/state transitions thống nhất khi #80/#81 được thiết kế.

## Q-78-11 — Current error integration được đồng bộ thế nào?

`DESIGN_CONTRACT_PATHS` chưa có `/api/v1/admin/content/pending`; framework fallback có thể trả 422/500 `VALIDATION_ERROR`/`INTERNAL_SERVER_ERROR`. API guideline yêu cầu error `data:null`, còn helper hiện trả `{}` khi không truyền data. Xác nhận allowlist/path handling và envelope khi wire route.

## Ranh giới proposal

- `status=PENDING_REVIEW` là direct queue predicate từ AC-33.
- Exact `type`/`course` filter, page 1/default 1, size cố định 20, `id ASC` và empty Page 200 đều là `DERIVED`.
- `ApiEnvelope<Page<Content>>` là đề xuất response shape cần catalog correction; DD vẫn ghi `ApiEnvelope<Content>` là direct contract.
- Không thêm Content/version/review fields, status, business code, SQL table/column, audit write hoặc Admin claim bằng suy đoán.
