# Kết quả Plan 07 — Learner Exercises and Submissions

- Phạm vi: API 048–056.
- Hoàn thành workbook: 9/9.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 048 | GET | `/api/v1/exercises` | SUY DẪN | Draft — Needs Confirmation | `API_048_GET_exercises.xlsx` | Không |
| 049 | GET | `/api/v1/exercises/{assignment_id}` | TRỰC TIẾP | Draft | `API_049_GET_exercises_by_assignment_id.xlsx` | Không |
| 050 | GET | `/api/v1/exercises/{assignment_id}/draft` | SUY DẪN | Draft — Needs Confirmation | `API_050_GET_exercises_by_assignment_id_draft.xlsx` | Không |
| 051 | PUT | `/api/v1/exercises/{assignment_id}/draft` | SUY DẪN | Draft — Needs Confirmation | `API_051_PUT_exercises_by_assignment_id_draft.xlsx` | exercise_submission_drafts |
| 052 | POST | `/api/v1/exercises/{assignment_id}/submissions` | TRỰC TIẾP | Draft | `API_052_POST_exercises_by_assignment_id_submissions.xlsx` | exercise_submissions |
| 053 | GET | `/api/v1/exercises/{assignment_id}/submissions/latest` | SUY DẪN | Draft — Needs Confirmation | `API_053_GET_exercises_by_assignment_id_submissions_latest.xlsx` | Không |
| 054 | GET | `/api/v1/exercises/{assignment_id}/submissions` | SUY DẪN | Draft — Needs Confirmation | `API_054_GET_exercises_by_assignment_id_submissions.xlsx` | Không |
| 055 | GET | `/api/v1/submissions/{submission_id}` | SUY DẪN | Draft — Needs Confirmation | `API_055_GET_submissions_by_submission_id.xlsx` | Không |
| 056 | POST | `/api/v1/exercises/{assignment_id}/resubmissions` | SUY DẪN | Draft — Needs Confirmation | `API_056_POST_exercises_by_assignment_id_resubmissions.xlsx` | exercise_submissions |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
