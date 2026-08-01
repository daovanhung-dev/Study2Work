# Review API DD — S2W-STUDY-API-034

- DD nguồn: `docs/DD/Study2Work_DD_API/04_Lo_trinh_hoc/S2W-STUDY-API-034_GET_me_learning_paths_enrollment_id_summary.xlsx`
- Endpoint: `GET /api/v1/me/learning-paths/{enrollment_id}/summary`
- Verdict: **CẦN SỬA**

## Findings

| Mức | Sheet/cell | Finding | Căn cứ BD | Cách sửa |
|---|---|---|---|---|
| P0 | `3.Data mapping!A12:H12`, `A20` | Predicate `learning_paths.enrollment_id/user_id` sai; enrollment là bảng riêng. | SQL `docs/BD/diagram/CLASS/study2work_study_full_schema_seed.sql:387-414` | Query `learning_path_enrollments.id=:enrollmentId AND user_id=:actor`, rồi JOIN path/courses. |
| P0 | `2.Response!A16:H22` | `completion_time`, completed courses, skills, achievement, review access, suggestions đều gán nguồn path và phần lớn không tồn tại. Contract cũng thiếu `pathProgressPercent`/remaining required items của sequence progress gần nhất. | `docs/BD/diagram/SEQUENCE/08. Study2Work_Study_SEQ_Hoan_Thanh_Khoa_Lo_Trinh.md:38-78`; SQL `:387-437` | Khóa vai trò API034 so với API063/069; dùng enrollment progress/courses/remaining requirements, hoặc đổi tên thành completion summary có nguồn thật. |
| P1 | `2.Response!A17:H22` | API không phân biệt active summary và completion summary: `completion_time` bắt buộc kiểu date-time, `next suggestions` xuất hiện dù path có thể ACTIVE. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:127-151` | Thiết kế discriminated state/nullability theo ACTIVE/COMPLETED; chỉ gợi ý next path khi đủ điều kiện. |
| P1 | `4.Error!A16:H17` | `ACTIVE_PATH_EXISTS`/`PATH_NOT_PUBLISHED` không nên chặn owner xem summary/history. | `docs/BD/04. Study2Work_Study_BasicDesign_Lo_Trinh_Hoc.md:143-151` | Bỏ activation errors; giữ owner/not-found/historical-policy errors. |
| P0 | `2.Response!A9:E11` | Envelope singleton không canonical và có pagination mẫu thừa. | `docs/BD/base/0. Study2Work_System_Architecture.md:632-700` | Canonical envelope/camelCase. |

## Điều kiện duyệt lại

- [ ] API034 được phân ranh rõ với API063/API069 và SEQ08.
- [ ] Query owner-safe, state-aware, dùng sources thật.
- [ ] Active/completed nullability và remaining requirements có test.
- [ ] Endpoint suy dẫn được duyệt.
