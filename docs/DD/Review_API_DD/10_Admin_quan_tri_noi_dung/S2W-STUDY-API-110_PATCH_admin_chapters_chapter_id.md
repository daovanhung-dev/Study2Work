# Review API DD — S2W-STUDY-API-110

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-110_PATCH_admin_chapters_chapter_id.xlsx`
- Method + endpoint: `PATCH /api/v1/admin/chapters/{chapter_id}`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source inventory 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật đủ 48 file/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Response/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A22` | PATCH response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE còn `<mapping>`/điều kiện generic dù checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết mapping/WHERE/version predicate cụ thể. |
| P0 | `1.Request!D22:F22`, `5.DB_Update_Main!B8:I10` | Body chỉ có `reason`, không có title/objective/unlock/completion dù Overview tuyên bố cập nhật chúng; lại ghi `reason`, `updated_at`, `updated_by` vào cột không tồn tại. | BD-10 `:87-97`; SQL `:446-456` | Thêm các field patchable theo schema; reason lưu audit; completion mới cần schema/rule riêng. |
| P0 | `3.Data mapping!F12:F14` | WHERE dùng `chapters.chapter_id`, trong khi PK thật là `chapters.id`; “status/version” cũng không tồn tại trên chapter. | SQL `:446-456` | Dùng `chapters.id=:chapterId`; thêm version/parent-course lifecycle check có thiết kế rõ. |
| P1 | `2.Response!C16:H18`, `3.Data mapping!C15:H15` | `updated_chapter`, impact/audit chỉ là virtual field; không có impact query khi sửa unlock/completion của course đang học. | BD-10 `:91-97,159-167,177-182` | Trả chapter DTO cụ thể; tính affected learners, bắt reason cho high impact, audit before/after. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] PATCH có field nghiệp vụ thực.
- [ ] WHERE dùng `chapters.id`.
- [ ] Mapping chỉ dùng cột thật.
- [ ] Parent course lifecycle/precondition rõ.
- [ ] Version/lock chống lost update.
- [ ] Impact/reason/audit được đặc tả.
- [ ] OpenAPI/test bao phủ empty patch, enum và concurrent update.
