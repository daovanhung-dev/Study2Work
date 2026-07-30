# Kết quả Plan 15 — Admin Chapters and Lessons

- Phạm vi: API 109–117.
- Hoàn thành workbook: 9/9.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 109 | POST | `/api/v1/admin/courses/{course_id}/chapters` | SUY DẪN | Draft — Needs Confirmation | `API_109_POST_admin_courses_by_course_id_chapters.xlsx` | courses, audit_logs |
| 110 | PATCH | `/api/v1/admin/chapters/{chapter_id}` | SUY DẪN | Draft — Needs Confirmation | `API_110_PATCH_admin_chapters_by_chapter_id.xlsx` | chapters, audit_logs |
| 111 | DELETE | `/api/v1/admin/chapters/{chapter_id}` | SUY DẪN | Draft — Needs Confirmation | `API_111_DELETE_admin_chapters_by_chapter_id.xlsx` | chapters, audit_logs |
| 112 | PUT | `/api/v1/admin/chapters/{chapter_id}/items/order` | SUY DẪN | Draft — Needs Confirmation | `API_112_PUT_admin_chapters_by_chapter_id_items_order.xlsx` | content_items, audit_logs |
| 113 | POST | `/api/v1/admin/chapters/{chapter_id}/lessons` | SUY DẪN | Draft — Needs Confirmation | `API_113_POST_admin_chapters_by_chapter_id_lessons.xlsx` | chapters, audit_logs |
| 114 | PATCH | `/api/v1/admin/lessons/{lesson_id}` | SUY DẪN | Draft — Needs Confirmation | `API_114_PATCH_admin_lessons_by_lesson_id.xlsx` | lessons, audit_logs |
| 115 | DELETE | `/api/v1/admin/lessons/{lesson_id}` | SUY DẪN | Draft — Needs Confirmation | `API_115_DELETE_admin_lessons_by_lesson_id.xlsx` | lessons, audit_logs |
| 116 | PUT | `/api/v1/admin/lessons/{lesson_id}/preview` | SUY DẪN | Draft — Needs Confirmation | `API_116_PUT_admin_lessons_by_lesson_id_preview.xlsx` | lessons, audit_logs |
| 117 | POST | `/api/v1/admin/lessons/{lesson_id}/lifecycle` | SUY DẪN | Draft — Needs Confirmation | `API_117_POST_admin_lessons_by_lesson_id_lifecycle.xlsx` | lessons, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
