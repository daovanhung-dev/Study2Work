# Kết quả Plan 18 — Admin Learner Exceptional Actions

- Phạm vi: API 134–141.
- Hoàn thành workbook: 8/8.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 134 | POST | `/api/v1/admin/learners/{learner_id}/progress-reset` | SUY DẪN | Draft — Needs Confirmation | `API_134_POST_admin_learners_by_learner_id_progress_reset.xlsx` | lesson_progress, audit_logs, course_enrollments, learning_path_enrollments, outbox_events |
| 135 | POST | `/api/v1/admin/learners/{learner_id}/active-path/cancel` | SUY DẪN | Draft — Needs Confirmation | `API_135_POST_admin_learners_by_learner_id_active_path_cancel.xlsx` | learning_path_enrollments, audit_logs, outbox_events |
| 136 | POST | `/api/v1/admin/learners/{learner_id}/active-path/transfer` | SUY DẪN | Draft — Needs Confirmation | `API_136_POST_admin_learners_by_learner_id_active_path_transfer.xlsx` | learning_path_enrollments, audit_logs, course_enrollments, lesson_progress, outbox_events |
| 137 | POST | `/api/v1/admin/learners/{learner_id}/suspend` | SUY DẪN | Draft — Needs Confirmation | `API_137_POST_admin_learners_by_learner_id_suspend.xlsx` | users, audit_logs, outbox_events |
| 138 | POST | `/api/v1/admin/learners/{learner_id}/unsuspend` | SUY DẪN | Draft — Needs Confirmation | `API_138_POST_admin_learners_by_learner_id_unsuspend.xlsx` | users, audit_logs, outbox_events |
| 139 | GET | `/api/v1/admin/learners/{learner_id}/support-notes` | SUY DẪN | Draft — Needs Confirmation | `API_139_GET_admin_learners_by_learner_id_support_notes.xlsx` | Không |
| 140 | POST | `/api/v1/admin/learners/{learner_id}/support-notes` | SUY DẪN | Draft — Needs Confirmation | `API_140_POST_admin_learners_by_learner_id_support_notes.xlsx` | support_notes, audit_logs, outbox_events |
| 141 | GET | `/api/v1/admin/learners/{learner_id}/audit` | SUY DẪN | Draft — Needs Confirmation | `API_141_GET_admin_learners_by_learner_id_audit.xlsx` | Không |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
