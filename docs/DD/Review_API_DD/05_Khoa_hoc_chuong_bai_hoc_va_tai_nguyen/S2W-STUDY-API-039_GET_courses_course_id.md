# Review API DD — S2W-STUDY-API-039

- DD nguồn: `docs/DD/Study2Work_DD_API/05_Khoa_hoc_chuong_bai_hoc_va_tai_nguyen/S2W-STUDY-API-039_GET_courses_course_id.xlsx`
- Endpoint: `GET /api/v1/courses/{course_id}`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `1.Request!A10:D10`, `2.Response!A21:H26` | API được đánh Public nhưng trả learner/access/progress/community state. Không có optional-token semantics nên public response có nguy cơ lộ dữ liệu cá nhân hoặc private community. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:24-30,99-114,209-220` | Tách public projection khỏi authenticated learner context hoặc đặc tả optional auth + field gating. |
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate `courses.course_id=:course_id` sai; PK là `id`. Response aggregates bị SELECT như cột và thiếu JOIN community/progress. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:361-437,623-640` | Query `courses.id`, JOIN/aggregate đúng nguồn và owner. |
| P0 | `2.Response!A16:H26` | Course/counts/progress dùng String và gán toàn bộ vào `courses`; schema không có goals/prerequisites/skills/counts/sample list/community fields. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:47-60,99-114`; SQL `:361-374` | Chốt data model/migration cho metadata thiếu; định nghĩa nested response/type/cardinality. |
| P1 | `4.Error!A12:H13` | `CONTENT_LOCKED` áp cho public course detail nhưng BD cho Guest xem public detail; phải phân biệt public metadata và private study content. | `docs/BD/05. Study2Work_Study_BasicDesign_Khoa_Hoc_Noi_Dung_Hoc.md:28-29,198-205` | Public detail trả metadata an toàn; private content/access action mới bị khóa. |
| P0 | `2.Response!A9:E11`, `A27:H27` | Envelope/pagination mẫu thừa không canonical. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical singleton envelope/camelCase. |

## Điều kiện duyệt lại

- [ ] Public/learner projections và optional auth được tách rõ.
- [ ] Query/source/types dùng schema thật, không lộ private state.
- [ ] Visibility/error và canonical response có test.
- [ ] Endpoint suy dẫn được phê duyệt.
