# Kết quả Plan 06 — Courses Chapters Lessons Resources

- Phạm vi: API 039–047.
- Hoàn thành workbook: 9/9.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 039 | GET | `/api/v1/courses/{course_id}` | SUY DẪN | Draft — Needs Confirmation | `API_039_GET_courses_by_course_id.xlsx` | Không |
| 040 | GET | `/api/v1/courses/{course_id}/curriculum` | SUY DẪN | Draft — Needs Confirmation | `API_040_GET_courses_by_course_id_curriculum.xlsx` | Không |
| 041 | GET | `/api/v1/chapters/{chapter_id}` | SUY DẪN | Draft — Needs Confirmation | `API_041_GET_chapters_by_chapter_id.xlsx` | Không |
| 042 | GET | `/api/v1/lessons/{lesson_id}/study` | TRỰC TIẾP | Draft | `API_042_GET_lessons_by_lesson_id_study.xlsx` | Không |
| 043 | GET | `/api/v1/courses/{course_id}/continue` | SUY DẪN | Draft — Needs Confirmation | `API_043_GET_courses_by_course_id_continue.xlsx` | Không |
| 044 | GET | `/api/v1/lessons/{lesson_id}/resources` | SUY DẪN | Draft — Needs Confirmation | `API_044_GET_lessons_by_lesson_id_resources.xlsx` | Không |
| 045 | GET | `/api/v1/resources/{resource_id}/access` | SUY DẪN | Draft — Needs Confirmation | `API_045_GET_resources_by_resource_id_access.xlsx` | Không |
| 046 | POST | `/api/v1/content-issues` | SUY DẪN | Draft — Needs Confirmation | `API_046_POST_content_issues.xlsx` | content_issues |
| 047 | GET | `/api/v1/me/content-issues` | SUY DẪN | Draft — Needs Confirmation | `API_047_GET_me_content_issues.xlsx` | Không |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
