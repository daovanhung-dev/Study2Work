# Kết quả Plan 16 — Admin Resources Exercises and Publishing

- Phạm vi: API 118–127.
- Hoàn thành workbook: 10/10.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 118 | POST | `/api/v1/admin/resources` | SUY DẪN | Draft — Needs Confirmation | `API_118_POST_admin_resources.xlsx` | course_materials, audit_logs |
| 119 | PATCH | `/api/v1/admin/resources/{resource_id}` | SUY DẪN | Draft — Needs Confirmation | `API_119_PATCH_admin_resources_by_resource_id.xlsx` | course_materials, audit_logs |
| 120 | DELETE | `/api/v1/admin/resources/{resource_id}` | SUY DẪN | Draft — Needs Confirmation | `API_120_DELETE_admin_resources_by_resource_id.xlsx` | course_materials, audit_logs |
| 121 | GET | `/api/v1/admin/exercises` | SUY DẪN | Draft — Needs Confirmation | `API_121_GET_admin_exercises.xlsx` | Không |
| 122 | POST | `/api/v1/admin/exercises` | SUY DẪN | Draft — Needs Confirmation | `API_122_POST_admin_exercises.xlsx` | exercises, audit_logs |
| 123 | GET | `/api/v1/admin/exercises/{assignment_id}` | SUY DẪN | Draft — Needs Confirmation | `API_123_GET_admin_exercises_by_assignment_id.xlsx` | Không |
| 124 | PATCH | `/api/v1/admin/exercises/{assignment_id}` | SUY DẪN | Draft — Needs Confirmation | `API_124_PATCH_admin_exercises_by_assignment_id.xlsx` | exercises, audit_logs |
| 125 | DELETE | `/api/v1/admin/exercises/{assignment_id}` | SUY DẪN | Draft — Needs Confirmation | `API_125_DELETE_admin_exercises_by_assignment_id.xlsx` | exercises, audit_logs |
| 126 | POST | `/api/v1/admin/content/{content_type}/{content_id}/pre-publish-check` | TRỰC TIẾP | Draft | `API_126_POST_admin_content_by_content_type_by_content_id_pre_publish_check.xlsx` | Không |
| 127 | POST | `/api/v1/admin/content/{content_type}/{content_id}/publish` | TRỰC TIẾP | Draft | `API_127_POST_admin_content_by_content_type_by_content_id_publish.xlsx` | content_publications, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
- API 127 được thiết kế theo SEQ-11 là hành động publish; sửa mô tả plan bị lệch sang impact.
- API 126 được thiết kế theo SEQ-11 cho một content theo path; sửa mô tả plan bị lệch sang batch items[].
