# Review API DD — S2W-STUDY-API-108

- DD source: `docs/DD/Study2Work_DD_API/10_Admin_quan_tri_noi_dung/S2W-STUDY-API-108_POST_admin_courses_course_id_lifecycle.xlsx`
- Method + endpoint: `POST /api/v1/admin/courses/{course_id}/lifecycle`
- Kết luận: **CẦN SỬA**
- Quy ước căn cứ: “BD-10”, “SEQ-11” và “SQL/schema” lần lượt là `docs/BD/10. Study2Work_Study_BasicDesign_Admin_Quan_Tri_Noi_Dung.md`, `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md` và `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql`; dải `:n-m` trong bảng là số dòng.

## Findings

| Severity | Sheet + cell | Mô tả cụ thể | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P1 | `00.Hướng dẫn!A4:B4`, `Cover!B19` | Nguồn 44 file/không schema đã stale. | SQL `:1-31`; canonical `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Cập nhật inventory và precedence. |
| P0 | `2.Response!D9:D11`, `2.Response!A36` | Envelope/error cũ, không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Dùng canonical fields, stable business code và `traceId`. |
| P1 | `2.Response!A24` | Lifecycle mutation có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:693-700` | Bỏ pagination. |
| P1 | `3.Data mapping!A20`, `00.Hướng dẫn!A13:B18` | UPDATE_ACTION là placeholder, không có transition predicate cụ thể dù checklist tick hoàn tất. | `docs/BD/base/0. Study2Work_System_Architecture.md:601-628,738-752` | Viết transition matrix, lock/version, UPDATE/audit/outbox cụ thể. |
| P0 | `1.Request!D22:I24`, `5.DB_Update_Main!B8:I12` | `action` là Object không enum; DD ghi `action/reason/effective_at/updated_*` vào `courses`, nhưng schema chỉ có `publish_status/published_at`. | Lifecycle BD-10 `:35-51,72-85`; SQL `:70-76,361-374` | Dùng enum/targetStatus; update `publish_status`, set `published_at`; reason/actor vào audit. |
| P0 | `3.Data mapping!C13:G15`, `4.Error!A12:H18` | Không validate checklist nguồn/quyền, cấu trúc, completion trước publish; không nêu transition hợp lệ hoặc tác động mọi path. | BD-10 `:146-167,175-182` | Chạy pre-publish check trên toàn course graph; trả error codes theo từng issue; tính learner/path impact. |
| P0 | `3.Data mapping!D15:H15`, `6.DB_Update_Related!A12:I12` | Audit/notification generic, chưa bảo đảm state + audit + outbox atomic và notify sau commit. | SEQ-11 `docs/BD/diagram/SEQUENCE/11. Study2Work_Study_SEQ_Admin_Quan_Tri_Noi_Dung.md:28-36`; architecture `docs/BD/base/0. Study2Work_System_Architecture.md:601-628` | Persist status/audit/outbox cùng transaction; worker notify affected learners có dedupe/idempotency. |

## Checklist duyệt lại

- [ ] Source/envelope/pagination đã sửa.
- [ ] Action/targetStatus có enum và transition matrix.
- [ ] Mapping dùng `publish_status/published_at`.
- [ ] Pre-publish check traverse toàn course graph.
- [ ] Impact mọi path/learner được tính.
- [ ] Concurrency/idempotency rõ.
- [ ] Audit before/after/reason + outbox atomic.
- [ ] OpenAPI/test bao phủ invalid transition, failed checklist, retry/race.
