# Review API DD — S2W-STUDY-API-124

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-124_PATCH_admin_exercises_assignment_id.xlsx`
- Method + endpoint: `PATCH /api/v1/admin/exercises/{assignment_id}`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Source inventory 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật 48 file/schema. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope. |
| P1 | `2.Response!A22` | Mutation response có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE `<mapping>`/predicate generic nhưng checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:738-752` | Viết field mapping/version predicate cụ thể. |
| P0 | `1.Request!D22:F22`, `5.DB_Update_Main!B8:I10` | PATCH chỉ nhận `reason`, không nhận đề/hạn/đáp án/rubric/required/resubmit như Overview; `reason/updated_*` không tồn tại trong exercises. | BD-10 `:123-135`; SQL `:486-500` | Khai từng field patchable và map cột/config thật; reason lưu audit. |
| P0 | `3.Data mapping!F12:F14` | WHERE dùng `exercises.exercise_id` thay vì PK `id`; version được nhắc nhưng bảng không có. | SQL `:486-506` | Dùng `exercises.id=:assignmentId`; thêm ETag/version hoặc lock/precondition cụ thể. |
| P0 | `2.Response!C17:C18`, `3.Data mapping!C13:G15` | Không đặc tả tác động lên submission đã có khi đổi max score, đáp án, rubric, due date hay resubmit; impact/audit chỉ placeholder. | BD-10 `:159-167,177-182`; submissions SQL `:508-529` | Phân loại immutable/important fields sau first submission; version assignment hoặc require migration/regrade plan, reason, audit và notify. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] PATCH có field cụ thể, không chỉ reason.
- [ ] WHERE dùng `exercises.id`.
- [ ] Mapping/config schema được chốt.
- [ ] Version/lock chống lost update.
- [ ] Policy field immutable sau submission rõ.
- [ ] Impact/regrade/audit/notification rõ.
- [ ] OpenAPI/test bao phủ existing submissions và race.
