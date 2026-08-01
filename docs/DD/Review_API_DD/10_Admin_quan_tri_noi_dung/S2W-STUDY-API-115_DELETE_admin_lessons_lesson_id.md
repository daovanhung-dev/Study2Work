# Review API DD — S2W-STUDY-API-115

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-115_DELETE_admin_lessons_lesson_id.xlsx`
- Method + endpoint: `DELETE /api/v1/admin/lessons/{lesson_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source inventory. |
| P0 | `2.Response!D9:D11`, `2.Response!A33` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical response nếu trả body. |
| P0 | `2.Response!B9:E9`, `2.Response!A22` | Chọn HTTP `204` nhưng vẫn có JSON `deleted_or_archived`, affected count, audit ID và pagination mẫu. | Chính DD `2.Response!E9`; canonical meta `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Chọn `200`+body hoặc `204` không body; bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SOFT_DELETE vẫn `<mapping>`/condition generic, trái checklist. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết archive/delete decision, lock và audit cụ thể. |
| P0 | `5.DB_Update_Main!B8:I10` | DD dùng `status/deleted_at/updated_*`; lesson chỉ có `publish_status`, không có deleted/audit timestamps. | SQL `:458-470` | Archive bằng `publish_status='ARCHIVED'` nếu policy cho phép; metadata khác cần migration, không giả lập cột. |
| P0 | `3.Data mapping!D12:D14` | Delete vật lý lesson cascade materials, lesson_progress và exercises; lịch sử learner bị phá, trái ngay mục tiêu API. | SQL `:458-555`; BD-10 `:110,163-167,181` | Nếu đã publish/có progress/submission thì chỉ archive/version; không hard delete. Chỉ hard delete DRAFT chưa tham chiếu với guard rõ. |
| P1 | `1.Request!D22:E22`, `6.DB_Update_Related!A12:I12` | Reason optional, trong khi archive/delete nội dung đã dùng phải audit và có lý do. | BD-10 `:182-193`; audit schema `:691-719` | Bắt buộc reason cho archive/delete; audit before/after cùng transaction. |

## Checklist duyệt lại

- [ ] Source/envelope đã sửa.
- [ ] `200` body hoặc `204` no-body nhất quán.
- [ ] Không còn pagination.
- [ ] Archive dùng cột thật/migration được duyệt.
- [ ] Không cascade history/progress/submission.
- [ ] Hard-delete guard chỉ cho DRAFT unused.
- [ ] Reason/audit/lock atomic.
- [ ] Test used/ununsed/published lesson, retry và race.
