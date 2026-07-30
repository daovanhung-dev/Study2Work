# Kết quả Plan 14 — Admin Courses

- Phạm vi: API 101–108.
- Hoàn thành workbook: 8/8.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 101 | GET | `/api/v1/admin/courses` | SUY DẪN | Draft — Needs Confirmation | `API_101_GET_admin_courses.xlsx` | Không |
| 102 | POST | `/api/v1/admin/courses` | SUY DẪN | Draft — Needs Confirmation | `API_102_POST_admin_courses.xlsx` | courses, audit_logs |
| 103 | GET | `/api/v1/admin/courses/{course_id}` | SUY DẪN | Draft — Needs Confirmation | `API_103_GET_admin_courses_by_course_id.xlsx` | Không |
| 104 | PATCH | `/api/v1/admin/courses/{course_id}` | SUY DẪN | Draft — Needs Confirmation | `API_104_PATCH_admin_courses_by_course_id.xlsx` | courses, audit_logs |
| 105 | PUT | `/api/v1/admin/courses/{course_id}/paths` | SUY DẪN | Draft — Needs Confirmation | `API_105_PUT_admin_courses_by_course_id_paths.xlsx` | learning_path_courses, audit_logs |
| 106 | PUT | `/api/v1/admin/courses/{course_id}/chapters/order` | SUY DẪN | Draft — Needs Confirmation | `API_106_PUT_admin_courses_by_course_id_chapters_order.xlsx` | chapters, audit_logs |
| 107 | GET | `/api/v1/admin/courses/{course_id}/impact` | SUY DẪN | Draft — Needs Confirmation | `API_107_GET_admin_courses_by_course_id_impact.xlsx` | Không |
| 108 | POST | `/api/v1/admin/courses/{course_id}/lifecycle` | SUY DẪN | Draft — Needs Confirmation | `API_108_POST_admin_courses_by_course_id_lifecycle.xlsx` | courses, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
