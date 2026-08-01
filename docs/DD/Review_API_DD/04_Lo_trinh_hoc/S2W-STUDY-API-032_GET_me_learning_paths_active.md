# Review API DD — S2W-STUDY-API-032

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-032_GET_me_learning_paths_active.xlsx`
- Endpoint: `GET /api/v1/me/learning-paths/active`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Query lọc `learning_paths.user_id`, cột không tồn tại; active ownership nằm ở `learning_path_enrollments.user_id/status`. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:323-338,387-414` | Bắt đầu từ enrollment `user_id=:actor AND status='ACTIVE'`, JOIN path/courses. |
| P0 | `2.Response!A16:H22` | Enrollment ID/progress bị gán nguồn path, percent khai String, còn `path/courses/continue/community` không có nested schema/source. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:97-110`; SQL `:387-437` | Định nghĩa typed active-path projection, course states, missing requirements và next action. |
| P1 | `2.Response!A15:H23`, `4.Error!A14:H14` | Không định nghĩa trường hợp không có active path: `data=null`, empty state hay error; lại liệt kê `ACTIVE_PATH_EXISTS` như lỗi của GET active. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:97-110` | Chốt no-active success semantics/next action; bỏ conflict activation. |
| P1 | `3.Data mapping!A12:H12` | Không join `course_enrollments`/lesson progress nên không thể tính courses, continue item và missing conditions như response cam kết. | SQL `:416-437,539-580` | Nêu query/composition/derived calculation thật và as-of consistency. |
| P0 | `2.Response!A9:E11` | Envelope/snake_case/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton response. |

## Điều kiện duyệt lại

- [ ] Active lookup owner-safe từ enrollment.
- [ ] Projection/course/continue/missing calculation có nguồn thật và kiểu đúng.
- [ ] No-active semantics + error matrix rõ.
- [ ] Endpoint suy dẫn được phê duyệt.
