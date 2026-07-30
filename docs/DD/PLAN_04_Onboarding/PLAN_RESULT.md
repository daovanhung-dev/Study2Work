# Kết quả Plan 04 — Onboarding

- Phạm vi: API 021–027.
- Hoàn thành workbook: 7/7.
- Trạng thái: Draft; API suy dẫn cần xác nhận.
- Naming contract: camelCase cho JSON/query; path placeholder giữ nguyên catalog; DB dùng snake_case.
- Lưu ý nguồn: bundle hiện tại thiếu System Architecture, Study Architecture, schema seed SQL và API catalog CSV được plan viện dẫn.

| API | Method | Endpoint | Basis | Status | Workbook | DB ghi |
|---:|---|---|---|---|---|---|
| 021 | GET | `/api/v1/onboarding/config` | SUY DẪN | Draft — Needs Confirmation | `API_021_GET_onboarding_config.xlsx` | Không |
| 022 | GET | `/api/v1/onboarding/current` | TRỰC TIẾP | Draft | `API_022_GET_onboarding_current.xlsx` | Không |
| 023 | PATCH | `/api/v1/onboarding/draft` | TRỰC TIẾP | Draft | `API_023_PATCH_onboarding_draft.xlsx` | onboarding_records |
| 024 | GET | `/api/v1/onboarding/recommended-paths` | TRỰC TIẾP | Draft | `API_024_GET_onboarding_recommended_paths.xlsx` | Không |
| 025 | PUT | `/api/v1/onboarding/selected-path` | SUY DẪN | Draft — Needs Confirmation | `API_025_PUT_onboarding_selected_path.xlsx` | onboarding_records |
| 026 | GET | `/api/v1/onboarding/review` | SUY DẪN | Draft — Needs Confirmation | `API_026_GET_onboarding_review.xlsx` | Không |
| 027 | POST | `/api/v1/onboarding/confirm` | TRỰC TIẾP | Draft | `API_027_POST_onboarding_confirm.xlsx` | onboarding_records, learning_path_enrollments, course_enrollments, audit_logs |

## Reviewer notes

- Đối chiếu endpoint/contract suy dẫn với PO/BA trước khi đổi trạng thái Final.
- Đối chiếu logical table/column với schema seed SQL khi được cung cấp.
