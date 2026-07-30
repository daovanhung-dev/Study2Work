# Kết quả Plan 05 — Learning Paths and Learner Support Requests

- Phạm vi: API 028–038.
- Hoàn thành workbook: 11/11.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 028 | GET | `/api/v1/learning-paths` | SUY DẪN | Draft — Needs Confirmation | `API_028_GET_learning_paths.xlsx` | Không |
| 029 | GET | `/api/v1/learning-paths/{path_id}` | SUY DẪN | Draft — Needs Confirmation | `API_029_GET_learning_paths_by_path_id.xlsx` | Không |
| 030 | POST | `/api/v1/learning-paths/{path_id}/activation-preview` | SUY DẪN | Draft — Needs Confirmation | `API_030_POST_learning_paths_by_path_id_activation_preview.xlsx` | Không |
| 031 | POST | `/api/v1/learning-paths/{path_id}/activate` | TRỰC TIẾP | Draft | `API_031_POST_learning_paths_by_path_id_activate.xlsx` | learning_path_enrollments, course_enrollments, audit_logs |
| 032 | GET | `/api/v1/me/learning-paths/active` | SUY DẪN | Draft — Needs Confirmation | `API_032_GET_me_learning_paths_active.xlsx` | Không |
| 033 | GET | `/api/v1/me/learning-paths/history` | SUY DẪN | Draft — Needs Confirmation | `API_033_GET_me_learning_paths_history.xlsx` | Không |
| 034 | GET | `/api/v1/me/learning-paths/{enrollment_id}/summary` | SUY DẪN | Draft — Needs Confirmation | `API_034_GET_me_learning_paths_by_enrollment_id_summary.xlsx` | Không |
| 035 | GET | `/api/v1/me/learning-paths/next-recommendations` | SUY DẪN | Draft — Needs Confirmation | `API_035_GET_me_learning_paths_next_recommendations.xlsx` | Không |
| 036 | POST | `/api/v1/support-requests` | TRỰC TIẾP | Draft | `API_036_POST_support_requests.xlsx` | support_requests |
| 037 | GET | `/api/v1/support-requests` | SUY DẪN | Draft — Needs Confirmation | `API_037_GET_support_requests.xlsx` | Không |
| 038 | GET | `/api/v1/support-requests/{request_id}` | SUY DẪN | Draft — Needs Confirmation | `API_038_GET_support_requests_by_request_id.xlsx` | Không |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
