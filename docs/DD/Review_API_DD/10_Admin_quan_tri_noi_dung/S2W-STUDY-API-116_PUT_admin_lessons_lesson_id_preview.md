# Review API DD — S2W-STUDY-API-116

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-116_PUT_admin_lessons_lesson_id_preview.xlsx`
- Method + endpoint: `PUT /api/v1/admin/lessons/{lesson_id}/preview`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source inventory 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope. |
| P1 | `2.Response!A22` | Non-list mutation có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE `<mapping>`/predicate generic nhưng checklist tự tick hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết mapping/version/validation cụ thể. |
| P0 | `1.Request!D22:I24`, `5.DB_Update_Main!B8:I12` | Schema chỉ có `lessons.sample_public`; DD lại ghi `enabled`, `public_blocks`, `public_resource_ids`, `updated_*` vào lesson, các cột không tồn tại. | SQL `:458-480`; preview rule BD-10 `:108,157,179` | Map `enabled` → `sample_public`; public block/resource scope cần bảng/JSON schema + migration được duyệt. |
| P0 | `1.Request!D23:I24`, `3.Data mapping!C13:G14` | Khi `enabled=false` vẫn bắt public arrays; item types/UUID/ownership không rõ. Không chặn resource thiếu nguồn/quyền hoặc private/raw URL. | BD-10 `:112-121,146-157,176-179`; SQL `:472-480` | Dùng conditional validation; resource IDs là UUID thuộc lesson, usage right hợp lệ; chỉ trả signed/public-safe asset, không raw URL. |
| P1 | `2.Response!C16:H18`, `6.DB_Update_Related!A11:I11` | `preview_config` là String ảo và audit generic; không có output thể hiện effective public surface. | BD-10 `:108,157,179`; audit `:691-719` | Trả structured config `{enabled,publicBlocks,publicResources}`; audit before/after và test authorization public. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] `enabled` map đúng `sample_public`.
- [ ] Public block/resource có data model được duyệt.
- [ ] Conditional validation theo enabled.
- [ ] Resource ownership/source/usage-right được kiểm tra.
- [ ] Không lộ raw private URL; dùng signed/public-safe access.
- [ ] Version/lock/audit before-after rõ.
- [ ] OpenAPI/test bao phủ enable/disable và public authorization.
