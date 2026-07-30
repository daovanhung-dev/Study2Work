# Kết quả Plan 17 — Admin Learner Lookup and Support Resolution

- Phạm vi: API 128–133.
- Hoàn thành workbook: 6/6.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 128 | GET | `/api/v1/admin/learners` | SUY DẪN | Draft — Needs Confirmation | `API_128_GET_admin_learners.xlsx` | Không |
| 129 | GET | `/api/v1/admin/learners/{learner_id}/support-profile` | TRỰC TIẾP | Draft | `API_129_GET_admin_learners_by_learner_id_support_profile.xlsx` | Không |
| 130 | GET | `/api/v1/admin/learners/{learner_id}/progress` | SUY DẪN | Draft — Needs Confirmation | `API_130_GET_admin_learners_by_learner_id_progress.xlsx` | Không |
| 131 | GET | `/api/v1/admin/support-requests` | SUY DẪN | Draft — Needs Confirmation | `API_131_GET_admin_support_requests.xlsx` | Không |
| 132 | GET | `/api/v1/admin/support-requests/{request_id}` | SUY DẪN | Draft — Needs Confirmation | `API_132_GET_admin_support_requests_by_request_id.xlsx` | Không |
| 133 | POST | `/api/v1/admin/support-requests/{request_id}/resolve` | TRỰC TIẾP | Draft | `API_133_POST_admin_support_requests_by_request_id_resolve.xlsx` | support_requests, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
