# Kết quả Plan 19 — Operational Reports

- Phạm vi: API 142–149.
- Hoàn thành workbook: 8/8.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 142 | GET | `/api/v1/admin/reports/overview` | TRỰC TIẾP | Draft | `API_142_GET_admin_reports_overview.xlsx` | Không |
| 143 | GET | `/api/v1/admin/reports/registrations` | SUY DẪN | Draft — Needs Confirmation | `API_143_GET_admin_reports_registrations.xlsx` | Không |
| 144 | GET | `/api/v1/admin/reports/onboarding` | SUY DẪN | Draft — Needs Confirmation | `API_144_GET_admin_reports_onboarding.xlsx` | Không |
| 145 | GET | `/api/v1/admin/reports/learning-paths` | SUY DẪN | Draft — Needs Confirmation | `API_145_GET_admin_reports_learning_paths.xlsx` | Không |
| 146 | GET | `/api/v1/admin/reports/courses` | SUY DẪN | Draft — Needs Confirmation | `API_146_GET_admin_reports_courses.xlsx` | Không |
| 147 | GET | `/api/v1/admin/reports/assignments` | SUY DẪN | Draft — Needs Confirmation | `API_147_GET_admin_reports_assignments.xlsx` | Không |
| 148 | GET | `/api/v1/admin/reports/community` | SUY DẪN | Draft — Needs Confirmation | `API_148_GET_admin_reports_community.xlsx` | Không |
| 149 | GET | `/api/v1/admin/reports/alerts` | TRỰC TIẾP | Draft | `API_149_GET_admin_reports_alerts.xlsx` | Không |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
