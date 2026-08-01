# Review API DD — S2W-STUDY-API-120

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-120_DELETE_admin_resources_resource_id.xlsx`
- Method + endpoint: `DELETE /api/v1/admin/resources/{resource_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory/preference. |
| P0 | `2.Response!D9:D11`, `2.Response!A33` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical response nếu có body. |
| P0 | `2.Response!B9:E9`, `2.Response!A22` | Chọn `204` nhưng vẫn trả `hidden_or_deleted`, affected content, audit ID và pagination mẫu; 204 không có body. | Chính DD `2.Response!E9`; canonical meta `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Chọn `200`+body hoặc `204` no-body; bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | SOFT_DELETE còn `<mapping>` và generic condition dù checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết hide/archive/delete guard, lock và audit cụ thể. |
| P0 | `5.DB_Update_Main!B8:I10` | DD giả định `status/deleted_at/updated_*`; `course_materials` không có các cột đó. | SQL `:472-484` | Bổ sung `visibility/archive` model có migration hoặc chỉ cho hard delete DRAFT/unused; không dùng cột ảo. |
| P0 | `3.Data mapping!D12:D14`, `2.Response!C17:H17` | Không xác định tất cả lesson/course/published graph bị ảnh hưởng; schema hiện chỉ gắn một lesson, trong khi DD create từng tuyên bố nhiều lesson/course. | SQL `:458-484`; BD-10 `:117-121,154-166` | Chốt attachment model, query toàn reference graph và block/hide theo lifecycle trước khi mutation. |
| P1 | `1.Request!D22:E22`, `6.DB_Update_Related!A11:I11` | Reason bắt buộc là đúng, nhưng audit generic chưa nói before/after và file-object retention/deletion. | BD-10 `:121,182-193`; audit SQL `:691-719` | Ghi audit atomic; tách unlink/archive metadata khỏi xóa blob, định nghĩa retention và cleanup async an toàn. |

## Checklist duyệt lại

- [ ] Source/envelope/status-body consistency đã sửa.
- [ ] Không còn pagination.
- [ ] Hide/archive schema thật được chốt.
- [ ] Attachment/reference graph được kiểm tra.
- [ ] Published/used content không bị phá.
- [ ] Blob retention/cleanup policy rõ.
- [ ] Reason/audit/lock atomic.
- [ ] Test used/ununsed/multi-reference, retry và race.
