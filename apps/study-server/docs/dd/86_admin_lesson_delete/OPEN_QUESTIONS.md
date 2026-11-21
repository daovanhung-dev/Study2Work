# Câu hỏi còn mở — API #86

Trạng thái: Draft — Needs Confirmation. API contract là trực tiếp; cục bộ đã chọn fallback từ schema legacy và API #77. Owner approval và live-schema verification vẫn còn mở.

1. **Delete policy approval:** Cục bộ dùng status tombstone `lessons.status='DELETED'`; cần owner xác nhận policy này.
2. **Dependency completeness:** Cục bộ chặn `lesson_progress`, `resources`, `lesson_uploads`; owner xác nhận set này đã đủ quan hệ cần bảo vệ.
3. **Blocker semantics:** Cục bộ coi mọi progress row là blocker, không lọc status; cần owner xác nhận.
4. **Selected/live schema:** Code dùng legacy BIGINT candidate. Live table/column/FK metadata và migration deployment chưa được xác nhận; V1-PILOT UUID model vẫn tách biệt.
5. **Timestamp mapping:** Cục bộ trả DB `updated_at` từ mutation làm `deleted_at`, theo API #77; owner xác nhận ý nghĩa/precision nếu cần contract riêng.
6. **Visibility:** Source ẩn tombstone trong Admin #82/#83/#84/#85 và Mentor/resource #48/#12; live behavior chưa được kiểm chứng.
7. **Repeated DELETE:** Cục bộ trả 404 khi Lesson đã `DELETED`; catalog không định nghĩa idempotency.
8. **Concurrency:** View khóa row, kiểm tra blockers và update trong một transaction; live FK lock behavior chưa được kiểm chứng.
9. **Admin authorization:** Shared ADMIN role được thực thi; AC-34 lesson-management permission chưa có policy source.
10. **Audit boundary:** #86 không thêm audit; các row audit hiện có của #85 được giữ.

## Ranh giới proposal

- DIRECT: method/path/auth/role/input/output/status/error set; DeleteResult fields; AC-34 delete-policy/reload intent.
- DERIVED local behavior: status tombstone, timestamp alias, progress/reference blocker set, 422 blocker response, active visibility, repeat-delete 404 and view-owned transaction.
- SOURCE_REQUIRED/unverified: owner approval, complete live dependency graph, deployed schema/FKs, and fine-grained lesson-management permission.

## Kết quả macro-review AC-34

- Status: `SOURCE_BACKED_WITH_OPEN_QUESTIONS` — đã đối chiếu diagram/catalog/schema và local runtime #82–#86; đây không phải owner approval hoặc live DB verification.
- Bảng cross-API, các discrepancy và open question còn lại nằm trong [báo cáo macro-review](./VERIFICATION_REPORT.md#ac-34-macro-review).
