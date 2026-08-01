# Review API DD — S2W-STUDY-API-119

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-119_PATCH_admin_resources_resource_id.xlsx`
- Method + endpoint: `PATCH /api/v1/admin/resources/{resource_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error cũ trái canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical response/camelCase. |
| P1 | `2.Response!A22` | PATCH response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE `<mapping>`/predicate generic nhưng checklist tự tick hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết field mapping/version predicate cụ thể. |
| P0 | `1.Request!D22:F22`, `5.DB_Update_Main!B8:I10` | Body chỉ có `reason`; không có description/source/rights/link/required như Overview. Sau đó lại update `reason/updated_*`, các cột không có trong `course_materials`. | BD-10 `:112-121`; SQL `:472-484` | Thêm field patchable theo schema; reason lưu audit; field mới cần migration. |
| P0 | `3.Data mapping!F12:F14` | WHERE dùng `course_materials.resource_id`; PK thật là `id`. Version/status được nhắc nhưng bảng không có. | SQL `:472-484` | Dùng `course_materials.id=:resourceId`; thêm version/archival schema hoặc lock/precondition thực. |
| P0 | `2.Response!C17:C18`, `3.Data mapping!C13:G15` | Không revalidate source/usage right/file scan/link khi đổi resource; impact/audit chỉ virtual, dù thay đổi có thể ảnh hưởng learner đang học. | BD-10 `:120-121,154-166,176-182` | Validate rights/link/asset state, tính impacted content/learners, audit before/after và notify nếu important. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] PATCH có field thực, không chỉ reason.
- [ ] WHERE dùng `course_materials.id`.
- [ ] Mapping dùng cột/relations thật.
- [ ] Source/rights/link/file scan được revalidate.
- [ ] Version/lock chống lost update.
- [ ] Impact/reason/audit/notify rõ.
- [ ] OpenAPI/test bao phủ rights downgrade, invalid URL và race.
