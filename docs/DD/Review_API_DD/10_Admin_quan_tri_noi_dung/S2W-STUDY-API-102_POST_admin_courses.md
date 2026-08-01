# Review API DD — S2W-STUDY-API-102

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-102_POST_admin_courses.xlsx`
- Method + endpoint: `POST /api/v1/admin/courses`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale; hiện có 48 file và SQL. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source inventory và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A32` | Envelope/error cũ, không có `success/businessCode/message/traceId`. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Áp dụng canonical envelope và camelCase. |
| P1 | `2.Response!A21` | Create response có pagination mẫu thừa và ví dụ trạng thái `ACTIVE`, trong khi course mới phải là `DRAFT`. | Lifecycle BD-10 `:35-51`; canonical meta `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ `meta`; trả `publishStatus: DRAFT`. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | `INSERT ... SET <mapping>` không hợp lệ với PostgreSQL và vẫn còn placeholder. | SQL target PostgreSQL `:1-25`; contract rule `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Dùng `INSERT(columns) VALUES(...) RETURNING`; bỏ placeholder/check giả. |
| P0 | `1.Request!D21:I31`, `7.DB_Insert_Main!B8:I20` | DTO/mapping sai schema: `descriptions`, `image_url`, `goals`, `prerequisites`, `skills`, `completion_conditions`, `community_group_ids`, `created_*` không có; `estimated_duration` là String nhưng map vào integer. | SQL `:361-374`; chức năng course BD-10 `:72-85` | Chốt core DTO `title,slug,summary,level,estimatedMinutes`; phần mở rộng phải có migration/relations riêng và kiểu integer. |
| P0 | `7.DB_Insert_Main!B17:I17`, `3.Data mapping!E14` | Completion conditions bị lưu JSON trên course dù schema đã có `completion_rules` cho target COURSE. | SQL `:560-580`; BD-10 `:83,178` | Insert/upsert `completion_rules(target_type='COURSE',target_id=...)` trong cùng transaction; validate nội dung bắt buộc. |
| P1 | `1.Request!B11`, `3.Data mapping!G15` | Idempotency chỉ “khuyến nghị”, không có storage/scope/hash/replay policy cho create. | `docs/BD/base/0. Study2Work_System_Architecture.md:723-736` | Đặc tả `Idempotency-Key`, uniqueness theo actor+endpoint, request hash, TTL và response snapshot. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] Course mới trả `DRAFT`.
- [ ] DTO và DB mapping khớp `courses`.
- [ ] Field mở rộng có schema/relations được duyệt.
- [ ] Completion rule ghi vào bảng đúng.
- [ ] PostgreSQL INSERT cụ thể, atomic và không placeholder.
- [ ] Idempotency/duplicate slug được xử lý.
- [ ] OpenAPI/test bao phủ enum level, duration, slug conflict và retry.
