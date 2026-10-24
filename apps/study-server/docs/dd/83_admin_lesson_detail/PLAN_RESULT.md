# Plan Result — API #83 Lấy lesson detail

## Kết quả

Đã tạo DD Markdown theo 8 sheet đã đăng ký và 3 report chuẩn Study. Tài liệu dùng catalog #83, reusable Lesson, AC-34 diagram/index, API #82/#74/#09 references, current Study source và legacy/V1-PILOT schema artifacts.

## Quyết định ghi trong DD

- Giữ nguyên `GET /api/v1/admin/lessons/{lesson_id}`, `lesson_id:int64!`, response `ApiEnvelope<Lesson>` và exact catalog error set.
- Candidate query đọc đúng một legacy `lessons` row theo ID; không áp dụng public `PUBLISHED` filter.
- Không thêm dependency fields/query cho tới khi AC-34 “lesson + dependencies” có output/use rule; API #86 phải kiểm tra references tại thời điểm delete.
- Giữ legacy/pilot schema mismatch, nullable `course_id`, status enum/casing, Admin guard, soft-delete visibility, malformed-path mapping và error-envelope behavior thành open questions.

## Phạm vi

Chỉ tạo DD #83 và worklog/inventory liên quan. Không sửa router, module, tests, database, catalog, diagram hoặc scope context. Không tạo ZIP. AC-34 macro-review chờ đến khi DD #86 có mặt.
