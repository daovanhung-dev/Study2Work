# Plan Result — API #83 Lấy lesson detail

## Kết quả

Đã tạo DD Markdown theo 8 sheet đã đăng ký và 3 report chuẩn Study. Task coding đã wire API #83, thêm TestClient coverage và đồng bộ tài liệu với catalog, reusable Lesson, AC-34 diagram/index, API #82/#74/#09 references, current Study source và legacy/V1-PILOT schema artifacts. DD vẫn `Draft — Needs Confirmation`.

## Quyết định ghi trong DD

- Giữ nguyên `GET /api/v1/admin/lessons/{lesson_id}`, `lesson_id:int64!`, response `ApiEnvelope<Lesson>` và exact catalog error set.
- Runtime query đọc đúng một legacy `lessons` candidate row bằng bind parameter; không áp dụng public `PUBLISHED` filter.
- Không thêm dependency fields/query cho tới khi AC-34 “lesson + dependencies” có output/use rule; API #86 phải kiểm tra references tại thời điểm delete.
- Runtime dùng shared `ADMIN` role guard; fine-grained lesson-management permission chưa được source-backed.
- Raw `lesson_id` parse signed-int64 sau auth; malformed/out-of-range -> 404 theo local DERIVED choice/API #74 precedent. Absent row -> 404; query/projection failure -> safe 500 + rollback.
- Optional `content`/`video_url` NULL được serialize thành JSON null theo API #09 model precedent; `video_url` giữ kiểu string nullable, không thêm URI rule.
- Giữ legacy/pilot schema mismatch, nullable `course_id`, status enum/casing và soft-delete visibility thành open questions.
- Không thêm dependency query/field, DDL, migration hoặc mutation; API #86 cần kiểm tra quan hệ tại thời điểm xóa.

## Phạm vi

Runtime phạm vi #83 gồm module, route, middleware path-template allowlist và focused tests; tài liệu scope/context được đồng bộ. Không sửa schema, catalog hoặc diagram. Không tạo ZIP. AC-34 macro-review giữ lại các open questions hiện có.
