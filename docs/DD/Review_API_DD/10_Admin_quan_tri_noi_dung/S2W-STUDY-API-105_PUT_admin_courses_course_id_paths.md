# Review API DD — S2W-STUDY-API-105

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-105_PUT_admin_courses_course_id_paths.xlsx`
- Method + endpoint: `PUT /api/v1/admin/courses/{course_id}/paths`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật nguồn 48 file và schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical fields và camelCase. |
| P1 | `2.Response!A22` | Mutation response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; chỉ trả result + `traceId`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE dùng `<mapping>`; replace semantics không được mô tả dù checklist đánh dấu hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Nêu rõ PUT thay toàn bộ association set, transaction và SQL upsert/delete. |
| P0 | `1.Request!D22:I25` | `paths` optional gây mơ hồ; `required` và `order` bị khai String thay vì boolean/integer, không có enum/range/duplicate rules. | BD-10 `:81,140,180`; SQL `:376-385` | Bắt buộc array; dùng `pathId: UUID`, `required: boolean`, `orderIndex: integer >=0`; validate unique path/order. |
| P0 | `3.Data mapping!D14:E14`, `5.DB_Update_Main!B8:I10` | DD ghi `courses.paths` JSON và `updated_*`, nhưng quan hệ thật là `learning_path_courses`; `courses` không có các cột này. | SQL `:361-385` | Lock course/paths; replace rows trong `learning_path_courses` theo `(learning_path_id,course_id)` và `order_index`. |
| P0 | `2.Response!C17:C18`, `3.Data mapping!C13:G15` | `validation_warnings`/`impact_summary` không có rule/query; chưa kiểm tra tất cả lộ trình liên quan và learner đang học trước khi tháo/gán course. | BD-10 `:159-167,180-182`; SQL `:387-437` | Tính impact mọi path/enrollment liên quan, yêu cầu reason/acknowledgement cho published structure và ghi audit. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] PUT replace semantics và empty array rõ.
- [ ] Kiểu UUID/boolean/integer đúng.
- [ ] Ghi `learning_path_courses`, không ghi JSON vào `courses`.
- [ ] Validate unique pair/order và FK.
- [ ] Impact mọi path/learner được tính.
- [ ] Transaction/lock/audit được đặc tả.
- [ ] OpenAPI/test bao phủ unassign-all, duplicate và concurrent update.
