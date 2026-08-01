# Review API DD — S2W-STUDY-API-117

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-117_POST_admin_lessons_lesson_id_lifecycle.xlsx`
- Method + endpoint: `POST /api/v1/admin/lessons/{lesson_id}/lifecycle`
- Kết luận: **CẦN SỬA**

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Inventory 44 file/không schema đã stale. | SQL `:1-31`; `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật source/precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A34` | Envelope/error cũ không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical envelope/camelCase. |
| P1 | `2.Response!A23` | Lifecycle mutation có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE_ACTION còn `<mapping>`/state predicate generic nhưng checklist đã tick. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết transition matrix, lock/version, audit/outbox cụ thể. |
| P0 | `1.Request!D22:I23`, `5.DB_Update_Main!B8:I11` | `action` là Object không enum; DD ghi `action/reason/updated_*` vào lesson, trong khi cột lifecycle thật là `publish_status`. | Lifecycle BD-10 `:35-51,98-110`; SQL `:70-76,458-470` | Dùng targetStatus/action enum; update `publish_status`; reason/actor vào audit. |
| P0 | `3.Data mapping!C13:G15` | Không chạy checklist required completion, tài liệu/link/source/usage right và preview scope trước publish lesson. | BD-10 `:146-157,175-182`; SQL `:458-500` | Traverse lesson materials/exercises; fail với issue codes cụ thể trước transition PUBLISHED. |
| P0 | `2.Response!C18:C19`, `3.Data mapping!D15:H15` | Impact/audit/notification chỉ là field generic; không bảo đảm lịch sử/notify khi archive/update lesson có learner. | BD-10 `:159-167,181-182`; SEQ-11 `:28-35`; architecture `docs/BD/base/0. Study2Work_System_Architecture.md:601-628` | Tính affected progress/enrollments; persist status+audit+outbox atomic; notify sau commit có dedupe. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] Action/targetStatus có enum + transition matrix.
- [ ] Mapping cập nhật `publish_status`.
- [ ] Pre-publish checklist traverse lesson graph.
- [ ] Version/lock/idempotency rõ.
- [ ] Impact/history bảo toàn.
- [ ] Audit before/after/reason + outbox atomic.
- [ ] OpenAPI/test invalid transition, failed check, retry/race.
