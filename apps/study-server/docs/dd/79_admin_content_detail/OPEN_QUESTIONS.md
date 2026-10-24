# Câu hỏi còn mở — API #79 Lấy chi tiết Content

Trạng thái: `Draft — Needs Confirmation`. Catalog xác nhận path, Admin actor, Content response và error set; AC-33 đọc thêm version/author nhưng persistence, projection và revision identity chưa được xác định.

## Q-79-01 — Version và author được trả về hay chỉ đọc nội bộ?

**Bằng chứng**

- AC-33 node n6 yêu cầu đọc `content/version/author`.
- Catalog #79 trả `ApiEnvelope<Content>`; reusable Content chỉ có tám field và không có version/author.
- #78 cùng flow trả Content đơn và không mang revision metadata.

**Cần xác nhận**

1. Version/author chỉ là dữ liệu nội bộ để xử lý, còn response vẫn là Content?
2. Nếu UI cần metadata, catalog có cần response projection riêng không? Cần schema/type và field allowlist trước khi thêm.

**Ảnh hưởng:** Chặn xác định output của phần “metadata review” mà API name/diagram yêu cầu.

## Q-79-02 — Content BIGINT được lưu ở đâu?

Legacy DDL không có generic Content. V1-PILOT `content_blocks` dùng UUID, gắn `lesson_id` và có `content_json`; không map thẳng sang Content BIGINT với `course_id/content_type/title/payload`. Cần bảng/model/key/foreign keys và live schema đã duyệt.

## Q-79-03 — Version nào là phiên bản được review?

Chưa rõ queue/detail chọn pending revision, latest draft, latest published hay Content logical hiện hành. `content_id` không định danh version; cần version selector và quy tắc giữ cùng revision qua #78 → #79 → #80/#81.

## Q-79-04 — Author có nghĩa là ai và join từ đâu?

Chưa có author field hoặc identity mapping cho Content. `content_review_decisions.reviewer_subject_id` là reviewer, không phải author. `course_versions.created_by_subject_id` trong pilot chỉ nói về Course version, không chứng minh tác giả Content. Cần định nghĩa nguồn, ID space và response PII policy.

## Q-79-05 — #79 có chỉ trả Content còn pending không?

#78 lọc `status=PENDING_REVIEW`, nhưng diagram không chỉ định status recheck tại #79. Chốt hành vi khi item đã approved/rejected/withdrawn sau lúc mở queue; catalog không có conflict code.

## Q-79-06 — #80/#81 khóa quyết định vào đúng version ra sao?

Catalog #80/#81 chỉ nhận `content_id`; AC-33 n6 có version nhưng decision request không mang version ID/row version. Cần concurrency/locking/version identity rule để không duyệt nhầm revision mới hơn.

## Q-79-07 — Admin access và concealment policy là gì?

Catalog yêu cầu role Admin; Study helper hiện chỉ cho Student và không có Admin guard/claim policy. Cần guard/scope và quy tắc 403 so với 404 khi Content ngoài phạm vi.

## Q-79-08 — Invalid path và error envelope được xử lý thế nào?

Catalog không nêu 422 cho path parse; middleware allowlist thiếu endpoint; guideline yêu cầu error `data:null` nhưng helper mặc định `{}`. Cần đồng bộ khi route được wire mà không thêm code ngoài catalog.

## Ranh giới proposal

- Q1 tìm Content theo `content_id` và map direct Content schema là proposal `DERIVED`; không chọn physical table.
- #79 trả trạng thái hiện có và không tự lọc `PENDING_REVIEW` là proposal `DERIVED`; stale-item policy vẫn mở.
- Q2/Q3 đọc version/author chỉ ở logical level theo AC-33; không có SQL/join cụ thể được duyệt.
- Không thêm response field, status, business code, table/column hoặc decision write ngoài catalog/diagram evidence.
