# Review API DD — S2W-STUDY-API-114

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-114_PATCH_admin_lessons_lesson_id.xlsx`
- Method + endpoint: `PATCH /api/v1/admin/lessons/{lesson_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory nguồn 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical fields và camelCase. |
| P1 | `2.Response!A23` | Mutation response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE còn `<mapping>`/predicate generic dù checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết mapping/update/version cụ thể. |
| P0 | `1.Request!D22:F23`, `5.DB_Update_Main!B8:I11` | PATCH chỉ có `mutable: String` và reason, không nhận title/objective/video/content/required/completion như Overview; `mutable`, `reason`, `updated_*` không tồn tại. | BD-10 `:98-110`; SQL `:458-470` | Định nghĩa từng field patchable; map `title,objective,required,completion_condition,sample_public`; content/video qua model thích hợp. |
| P0 | `3.Data mapping!F12:F14` | WHERE dùng `lessons.lesson_id` thay vì PK `lessons.id`; version được nhắc nhưng không tồn tại. | SQL `:458-470` | Dùng `lessons.id=:lessonId`; thêm ETag/version hoặc lock + parent lifecycle predicate. |
| P0 | `2.Response!C18:C19`, `3.Data mapping!C15:H15` | Không đặc tả impact khi đổi required/completion của lesson đã publish; audit/notification chỉ generic. | BD-10 `:159-167,177-182`; SEQ-11 `:28-35` | Tính affected lesson progress/enrollments, phân loại important update, audit before/after và outbox notification. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] PATCH có field cụ thể, không `mutable` String.
- [ ] WHERE dùng `lessons.id`.
- [ ] Mapping chỉ dùng schema thật.
- [ ] Parent/publish state precondition rõ.
- [ ] Version/lock chống lost update.
- [ ] Impact/audit/notification cho important change.
- [ ] OpenAPI/test bao phủ required/completion update và race.
