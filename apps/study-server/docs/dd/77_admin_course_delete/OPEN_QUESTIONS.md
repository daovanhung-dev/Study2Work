# Câu hỏi còn mở — API #77

Trạng thái tài liệu: `Draft — Needs Confirmation`. Catalog và AC-32 xác nhận intent soft-delete có điều kiện, nhưng policy, schema và runtime chưa chốt.

1. **Dependency policy:** Enrollment/content nào ngăn xóa? Có tính cả inactive/completed records, bản nháp, dữ liệu lịch sử hoặc bản ghi đã archive không? Catalog nêu cần kiểm tra enrollment/content nhưng không định nghĩa predicate.
2. **Content relation:** Content được quản lý qua `lessons`, hay còn resource/quiz/assignment/discussion/payment và bảng khác? Legacy FK là candidate, không chứng minh đây là tập dependency đầy đủ.
3. **Blocked behavior:** Khi policy chặn, có dùng HTTP 422 `DESIGN_VALIDATION_ERROR` theo catalog không? Message/fieldErrors nào được trả? Không thêm business code hoặc field `reason` chưa có contract.
4. **Soft-delete persistence:** Schema được duyệt có marker, timestamp và semantics nào? Legacy `courses` không có deletion marker; V1-PILOT `archived_at` là archive trên UUID model và không tự động tương đương `deleted_at`.
5. **`DeleteResult.deleted_at`:** Timestamp lấy từ DB hay application clock, timezone/precision nào? Reusable response yêu cầu field này nhưng physical source chưa có.
6. **Schema/live DB:** Chọn legacy BIGINT course hay V1-PILOT UUID/versioned model? Live schema, migration, grants và FK metadata chưa xác minh.
7. **Admin authorization:** JWT claim/guard nào xác nhận Admin có quyền quản lý course? Actor/scope/tenant boundary lấy từ đâu? AC-32 là yêu cầu, current Study helper chỉ có Student guard.
8. **Repeated DELETE/idempotency:** Xóa lại trả 200 cùng result hay 404/422? Có cần `Idempotency-Key` cho retry và semantics replay/TTL nào? Catalog không quy định.
9. **Concurrency/transaction:** Dependency check và soft-delete mutation cần một transaction/locking strategy nào để tránh enrollment/content phát sinh giữa hai bước? Atomicity là proposal `DERIVED`.
10. **Visibility và mutation boundary:** Sau delete, #73 list và #74 detail có ẩn course không? #75 metadata và #76 status phải xử lý target đã soft-deleted thế nào? Marker/filter chưa được chọn.
11. **Audit boundary:** AC-32 ghi audit log cho nhánh #76 status; nhánh #77 chỉ nói soft-delete theo policy. Có yêu cầu audit riêng cho #77 không? Không sao chép side effect audit của #76 khi chưa có nguồn.
12. **Error integration:** Khi wire dynamic `/api/v1/admin/courses/{course_id}`, middleware exact-path allowlist và error `data:null` được đồng bộ ra sao? Hiện allowlist không có Admin course path và helper trả `{}` khi data bị bỏ trống.

## Ranh giới proposal

- Nếu policy được duyệt xác định dependency blocker, trả catalog 422 là proposal `DERIVED`; blocker set và exact response vẫn cần owner duyệt.
- Khi không bị chặn, AC-32 yêu cầu logical soft-delete. Không chọn hard delete, cascade, child mutation hoặc physical column.
- `DeleteResult.status="deleted"` và ba field của schema là contract trực tiếp; mapping timestamp và mutation source hiện `SOURCE_REQUIRED`.
- Không thêm audit, idempotency behavior, error code, response field hoặc visibility rule bằng suy đoán.

## Rà nhóm AC-32 #73–#77

Đã rà ở mức tài liệu sau khi #77 được tạo. Nhóm giữ ranh giới: #73 list, #74 detail, #75 metadata-only update, #76 status + diagram audit, #77 soft-delete theo policy. Các điểm chưa thống nhất thành implementation contract vẫn là category relation, counters, response wrapper của #74–#76, Admin guard, status enum/casing và soft-delete visibility/persistence. Chi tiết ở `VERIFICATION_REPORT.md`.
