# Kết quả Plan 08 — Admin Exercise Review

- Phạm vi: API 057–060.
- Hoàn thành workbook: 4/4.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 057 | GET | `/api/v1/admin/exercise-submissions` | SUY DẪN | Draft — Needs Confirmation | `API_057_GET_admin_exercise_submissions.xlsx` | Không |
| 058 | GET | `/api/v1/admin/exercise-submissions/{submission_id}` | SUY DẪN | Draft — Needs Confirmation | `API_058_GET_admin_exercise_submissions_by_submission_id.xlsx` | Không |
| 059 | PATCH | `/api/v1/admin/exercise-submissions/{submission_id}/review` | TRỰC TIẾP | Draft | `API_059_PATCH_admin_exercise_submissions_by_submission_id_review.xlsx` | exercise_reviews, exercise_submissions, lesson_progress, outbox_events |
| 060 | POST | `/api/v1/admin/exercise-submissions/{submission_id}/reopen` | SUY DẪN | Draft — Needs Confirmation | `API_060_POST_admin_exercise_submissions_by_submission_id_reopen.xlsx` | exercise_submissions, audit_logs, outbox_events |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
