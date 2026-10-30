# Câu hỏi còn mở — API #79 Lấy chi tiết Content

Trạng thái: `Draft — Needs Confirmation`. Runtime có local route/read projection trên legacy `contents` candidate. AC-33 đọc thêm version/author nhưng catalog trả `ApiEnvelope<Content>`; metadata projection và revision identity chưa được quyết định.

## Q-79-01 — Version và author được trả về hay chỉ đọc nội bộ?

**Bằng chứng**

- AC-33 node n6 yêu cầu đọc `content/version/author`.
- Catalog #79 trả `ApiEnvelope<Content>`; reusable Content chỉ có tám field, không có version/author.
- Runtime giữ response đúng catalog và không thêm metadata vào `data` hoặc `meta`.

**Cần xác nhận**

1. Version/author chỉ là dữ liệu nội bộ để xử lý, còn response vẫn là Content?
2. Nếu UI cần metadata, catalog có cần response projection riêng không? Cần schema/type và field allowlist trước khi thêm.

**Ảnh hưởng:** Chặn xác định output đầy đủ cho “metadata review” mà API name/diagram yêu cầu.

## Q-79-02 — Legacy `contents` có phải nguồn được duyệt cho API #79 không?

Checked-in `DB.sql`/migrations 006/007 định nghĩa BIGINT `contents`/`content_versions`, và APIs #49–#53/#78/#79 hiện dùng `contents`. Runtime dùng `contents` làm source candidate. Cần xác nhận live schema/deployment và xem đây có phải persistence chuẩn AC-33 hay pilot UUID model mới thay thế.

## Q-79-03 — Version nào là phiên bản được review?

`content_versions` lưu snapshot cũ trước update, nhưng #79 nhận `content_id` và không có version field trong response. Chưa rõ queue/detail chọn pending revision, latest draft, latest published hay current logical row; cần version selector và quy tắc giữ đúng revision qua #78 → #79 → #80/#81.

## Q-79-04 — Author có nghĩa là ai và join từ đâu?

`contents` không có author/creator field; #50 không ghi creator. `content_versions.archived_by` là updater lưu snapshot, còn `content_review_decisions.reviewer_subject_id` là reviewer. Cần nguồn, ID space và response PII policy được duyệt; không suy ra từ course Mentor hoặc pilot creator.

## Q-79-05 — #79 có chỉ trả Content còn pending không?

#78 lọc `status=PENDING_REVIEW`, nhưng #79 trả status hiện tại và không áp dụng status predicate. Chốt hành vi khi item đổi trạng thái sau lúc mở queue; catalog không có conflict code.

## Q-79-06 — #80/#81 khóa quyết định vào đúng version ra sao?

Catalog #80/#81 chỉ nhận `content_id`; AC-33 n6 có version nhưng decision request không mang version ID/row version. Cần concurrency/locking/version identity rule để không duyệt nhầm revision mới hơn.

## Q-79-07 — Admin access và concealment policy là gì?

Runtime dùng shared `validate_current_user_request(..., role="ADMIN")` trước DB. Catalog không chỉ rõ moderation-specific permission, tenant scope hoặc 403/404 concealment khi Admin thiếu quyền trên một Content cụ thể. Cần owner policy trước khi thêm scope guard.

## Q-79-08 — Invalid path và error envelope có khớp catalog không?

Runtime truyền raw path để guard chạy trước parse; malformed/out-of-range int64 trả catalog 404 theo #69 precedent. Dynamic path đã vào `DESIGN_CONTRACT_PATHS`; shared `error_response()` trả `data:null`. Xác nhận các fallback này làm behavior chuẩn cho #79.

## Ranh giới proposal

- Runtime Q1 dùng active `contents` row theo `content_id` và map direct Content schema; đây là source-backed local implementation, chưa phải live schema proof.
- #79 trả status hiện có và không tự lọc `PENDING_REVIEW`; policy stale-item vẫn mở.
- Q2/Q3 không có SQL/join vì revision selector và author source chưa có.
- Không thêm response field, status, business code, table/column hoặc decision write ngoài catalog/source evidence.
