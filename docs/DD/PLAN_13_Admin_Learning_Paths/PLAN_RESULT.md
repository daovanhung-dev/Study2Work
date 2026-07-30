# Kết quả Plan 13 — Admin Learning Paths

- Phạm vi: API 094–100.
- Hoàn thành workbook: 7/7.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 094 | GET | `/api/v1/admin/learning-paths` | SUY DẪN | Draft — Needs Confirmation | `API_094_GET_admin_learning_paths.xlsx` | Không |
| 095 | POST | `/api/v1/admin/learning-paths` | SUY DẪN | Draft — Needs Confirmation | `API_095_POST_admin_learning_paths.xlsx` | learning_paths, audit_logs |
| 096 | GET | `/api/v1/admin/learning-paths/{path_id}` | SUY DẪN | Draft — Needs Confirmation | `API_096_GET_admin_learning_paths_by_path_id.xlsx` | Không |
| 097 | PATCH | `/api/v1/admin/learning-paths/{path_id}` | SUY DẪN | Draft — Needs Confirmation | `API_097_PATCH_admin_learning_paths_by_path_id.xlsx` | learning_paths, audit_logs |
| 098 | PUT | `/api/v1/admin/learning-paths/{path_id}/courses` | SUY DẪN | Draft — Needs Confirmation | `API_098_PUT_admin_learning_paths_by_path_id_courses.xlsx` | learning_path_courses, audit_logs |
| 099 | GET | `/api/v1/admin/learning-paths/{path_id}/impact` | SUY DẪN | Draft — Needs Confirmation | `API_099_GET_admin_learning_paths_by_path_id_impact.xlsx` | Không |
| 100 | POST | `/api/v1/admin/learning-paths/{path_id}/lifecycle` | SUY DẪN | Draft — Needs Confirmation | `API_100_POST_admin_learning_paths_by_path_id_lifecycle.xlsx` | learning_paths, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
