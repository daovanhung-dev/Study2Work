# Review API DD — S2W-STUDY-API-098

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-098_PUT_admin_learning_paths_path_id_courses.xlsx`
- Method + endpoint: `PUT /api/v1/admin/learning-paths/{path_id}/courses`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source inventory 44 file và tuyên bố thiếu schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file, schema và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A35` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical fields và camelCase. |
| P1 | `2.Response!A23` | Non-list mutation có `meta.page/page_size`; pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination; `traceId` top-level. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE dùng `<mapping>`/điều kiện chung chung trong khi checklist báo hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Nêu rõ replace semantics, DELETE/UPSERT relation, lock và SQL cụ thể. |
| P0 | `1.Request!D22:I26` | `courses` lại optional dù PUT cần payload thay thế rõ; `order` và `required` bị khai String; `unlock_rule` không có enum/không tồn tại trong relation. | BD-10 `:65-67,136-145`; SQL `:376-385` | Bắt buộc `courses`; `courseId: UUID`, `orderIndex: integer >=0`, `required: boolean`; bỏ `unlockRule` hoặc bổ sung schema/rule có phê duyệt. |
| P0 | `3.Data mapping!D14:E14`, `5.DB_Update_Main!B8:I10` | DD UPDATE `learning_paths.courses` JSON, nhưng quan hệ thật là `learning_path_courses`; bảng cha không có `courses`, `updated_at`, `updated_by`. | SQL `:323-338,376-385` | Lock path; validate tất cả course; replace/upsert `learning_path_courses` trong một transaction và dựa vào unique pair/order constraints. |
| P0 | `3.Data mapping!C13:G15`, `2.Response!C17:C19` | Không đặc tả duplicate course/order, course không tồn tại, course chưa publish, hay cảnh báo learner đang học; các output warning/impact/audit chỉ là field ảo. | BD-10 `:140-145,159-167,177-182`; SQL `:376-414` | Thêm validations/errors cụ thể, impact query, audit before/after; yêu cầu acknowledgement/reason nếu cấu trúc published bị ảnh hưởng. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã chuẩn hóa.
- [ ] PUT replace semantics và payload rỗng được định nghĩa.
- [ ] Kiểu `orderIndex`/`required`/UUID đúng.
- [ ] Ghi `learning_path_courses`, không ghi JSON vào bảng cha.
- [ ] Validate uniqueness, FK, publication và toàn bộ course list.
- [ ] Có transaction/lock và rollback toàn bộ.
- [ ] Impact/audit/reason cho thay đổi published được đặc tả.
- [ ] OpenAPI/test bao phủ duplicate order, missing course, retry và race.
