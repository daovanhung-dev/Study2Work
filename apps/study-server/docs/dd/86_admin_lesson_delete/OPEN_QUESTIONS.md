# Câu hỏi còn mở — API #86

Trạng thái: Draft — Needs Confirmation. API contract và DeleteResult là trực tiếp; policy dependency và persistence dưới đây còn cần owner xác nhận.

1. **Delete policy:** Xác nhận soft-delete là policy mặc định hay cho phép hard delete? Proposal hiện ưu tiên soft-delete để giữ lịch sử.
2. **Dependency set:** Ngoài resources và lesson_progress trong legacy DDL, relation/reference nào cần kiểm tra?
3. **Blocker semantics:** Có reference/progress thì có chặn xóa và trả 422 DESIGN_VALIDATION_ERROR không? Trạng thái progress nào tính là blocker?
4. **Persistence:** Marker soft-delete được lưu ở relation/column nào? Legacy và V1-PILOT Lesson hiện không có marker.
5. **DeleteResult.deleted_at:** Timestamp lấy từ đâu, timezone/precision nào? Response yêu cầu field này nhưng chưa có persistence source.
6. **Selected/live schema:** Runtime dùng legacy BIGINT lessons hay V1-PILOT UUID/versioned model? Live migration/FK metadata đã được xác nhận chưa?
7. **Visibility:** Sau soft-delete, API #82 list và #83 detail ẩn lesson thế nào? #84 update/#85 status với lesson đã xóa trả gì?
8. **Repeated DELETE:** Xóa lại trả success, 404 hay 422? Catalog không quy định idempotency/replay behavior.
9. **Transaction/concurrency:** Q1/Q2 và soft-delete có cần một transaction/lock strategy nào để tránh reference xuất hiện giữa check và mutation?
10. **Admin authorization:** JWT claim, lesson-management permission và scope boundary nào được duyệt?
11. **Error integration:** Khi wire route, middleware path mapping và error data:null-vs-{} được đồng bộ ra sao?
12. **Audit boundary:** AC-34 yêu cầu audit cho #85 status branch; xác nhận #86 delete không thêm audit nếu không có policy riêng.

## Ranh giới proposal

- DIRECT: method/path/auth/role/input/output/status/error set; DeleteResult fields; AC-34 delete-policy/reload intent.
- DERIVED: prefer soft-delete; block with 422 if approved progress/reference exists; atomic checks/mutation; candidate legacy dependency EXISTS checks.
- SOURCE_REQUIRED: complete dependency graph, active schema/live DB, soft-delete marker, persisted deleted_at, visibility, Admin guard, transaction and repeat-delete semantics.

## Kết quả macro-review AC-34

- Status: `VERIFIED_WITH_OPEN_QUESTIONS` — đã đối chiếu tài liệu #82–#86; đây không phải owner approval hoặc runtime verification.
- Bảng cross-API, các discrepancy và open question còn lại nằm trong [báo cáo macro-review](./VERIFICATION_REPORT.md#ac-34-macro-review).
