# Câu hỏi còn mở — API #81 Từ chối nội dung

Trạng thái: Draft — Needs Confirmation
Endpoint: PATCH /api/v1/admin/content/{content_id}/reject

## Q-81-01 — Lý do từ chối được lưu và hiển thị thế nào?

**Bằng chứng**

- Catalog body có reason:string!.
- AC-33 reject node yêu cầu UPDATE status = REJECTED + review reason.
- Reusable Content response có tám field nhưng không có reason.

**Cần xác nhận**

Physical relation/field, retention/history, whether the reason is only persisted internally or needs an API/UI response projection. Không thêm review_reason vào Content response nếu catalog chưa đổi.

## Q-81-02 — Có rule nào ngoài required string không?

Catalog không khai báo max length, trim/normalization, blank-only behavior, format, reason codes hoặc locale. Cần chốt nếu muốn thêm rule. DD hiện chỉ coi missing body/field là request schema validation; không tự suy ra giới hạn.

## Q-81-03 — API #81 thao tác lên revision nào và xử lý stale item ra sao?

#79 đọc version nhưng #78/#79/#81 chỉ mang content_id. Cần revision selector, stale queue behavior, optimistic lock/concurrency policy và error mapping khi revision đổi sau detail.

## Q-81-04 — Rejection có ghi audit decision riêng không?

#80 diagram ghi status update + audit; #81 diagram ghi status REJECTED + review reason, không nêu audit append. Cần xác nhận cả hai nhánh có cùng audit/history model hay reason update đã là audit record.

## Q-81-05 — Content và reason dùng schema nào?

Legacy Study DDL không có generic Content/review relation. V1-PILOT content_review_decisions có reason_codes/comment nhưng dùng UUID resource_version_id/reviewer; không phải mapping trực tiếp cho Content int64. Cần physical model, key, status owner và live migration.

## Q-81-06 — Admin principal, permission và state check xác định ra sao?

Catalog yêu cầu Admin; current Study helper chỉ hỗ trợ Student. Cần claim/guard/scope, check order, pending state enforcement và policy 403/404 khi target ngoài quyền hoặc không còn reviewable.

## Q-81-07 — Request validation, error envelope và middleware được wire thế nào?

Catalog có 422 DESIGN_VALIDATION_ERROR nhưng không nêu đầy đủ trigger. Middleware allowlist chưa có #81; expected error data:null khác helper default {}. Cần integration behavior khi endpoint được triển khai, không thêm code ngoài catalog.

## Q-81-08 — Từ chối ảnh hưởng tới publish/delete lifecycle ra sao?

AC-22 có publish API #52 và conditional delete #53; chưa chỉ rõ Content REJECTED có thể publish trực tiếp hay xóa thế nào. Cần state ownership và policy cùng với AC-33 approval result.

## Ranh giới proposal

- Không thêm reason, reviewer, version hoặc audit field vào response.
- Không thêm request fields ngoài content_id và reason.
- Không chốt bảng/cột, version selector, state machine, transaction hoặc separate audit append.
- Khi status thành REJECTED, item không còn khớp predicate PENDING_REVIEW của #78; persistence/current revision behavior vẫn cần schema/rule owner confirmation.
